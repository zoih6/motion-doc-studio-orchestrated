#!/usr/bin/env python3
"""
Submit and poll a Seedance 1.5 Pro first+last-frame task from a SEEDANCE_SCENE.json spec.
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

from runtime_support import (
    ARK_BASE_URL,
    SKILL_ENV_PATH,
    build_ark_headers,
    deep_find_first,
    download_file,
    env_value,
    find_project_root,
    find_scene_spec,
    load_json,
    path_to_data_uri,
    request_json,
    resolve_path,
    write_json,
)
from validate_seedance_keyframes import validate_keyframe_continuity

TERMINAL_STATES = {"succeeded", "failed", "canceled", "expired"}
FIXED_RULES = {"pixel-locked", "anchored-micro-motion"}
DRAW_MODES = {"progressive-tip-growth", "segment-by-segment-reveal"}
ENTERING_PRIMITIVES = {
    "slide-in",
    "rise",
    "stamp-in",
    "page-place",
    "pin-drop",
    "serial-placement",
    "direct-placement",
    "unfold",
    "wipe-reveal",
    "tape-press",
}
TIMELINE_BEHAVIORS = ENTERING_PRIMITIVES | {"draw-path", "hold"}
REQUIRED_FORBIDDEN_EVENTS = {
    "object replacement",
    "object morphing",
    "duplicate surfaces",
    "cross-zone travel",
}
FIXED_ENTRANCE_RE = re.compile(
    r"\b(?:enter|drop|place|flip|replace|cover|duplicate|resize|redraw|reveal|slide|rise|move|animate)\w*\b|"
    r"进场|进入|落下|放置|翻转|替换|覆盖|复制|缩放|重绘|揭示|滑入|升起|移动|动画",
    re.IGNORECASE,
)
NEGATION_RE = re.compile(r"\b(?:never|no|not|do not|must not|cannot|can't|keep fixed|stay fixed)\b|不|禁止|不得|不可|保持固定", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a Seedance 1.5 Pro first+last-frame task."
    )
    parser.add_argument("--project", help="Project root used to resolve relative paths.")
    parser.add_argument("--scene-spec", help="Path to SEEDANCE_SCENE.json.")
    parser.add_argument(
        "--scene-slug",
        help="Scene slug when resolving the scene spec automatically.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=1200,
        help="Maximum wall time for polling.",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the finished video into the path defined by the scene spec.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the payload and print it without submitting the request.",
    )
    return parser.parse_args()


def resolve_scene_spec(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.scene_spec:
        spec_path = Path(args.scene_spec).expanduser().resolve()
        project_root = find_project_root(args.project or spec_path.parent.parent.parent)
        return project_root, spec_path
    if not args.project:
        raise ValueError("Pass --project when --scene-spec is omitted.")
    project_root = find_project_root(args.project)
    return project_root, find_scene_spec(
        project_root,
        args.scene_slug,
        filename="SEEDANCE_SCENE.json",
    )


def _frame_by_role(spec: dict, role: str) -> dict:
    for frame in spec.get("frames", []):
        if frame.get("role") == role:
            return frame
    raise RuntimeError(f"Scene spec is missing a frame with role `{role}`.")


def _require_list(contract: dict, field: str, *, allow_empty: bool = False) -> list:
    value = contract.get(field)
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise RuntimeError(f"motion_contract.{field} must be {qualifier}.")
    return value


def compile_motion_contract(spec: dict) -> str:
    contract = spec.get("motion_contract")
    if not isinstance(contract, dict):
        raise RuntimeError("Scene spec needs a structured motion_contract object.")
    if contract.get("frame_state_audit_locked") is not True:
        raise RuntimeError("motion_contract.frame_state_audit_locked must be true after comparing the first and last frames.")
    if contract.get("prompt_contract_consistency_locked") is not True:
        raise RuntimeError("motion_contract.prompt_contract_consistency_locked must be true after removing prompt/contract contradictions.")

    fixed_objects = _require_list(contract, "fixed_objects")
    entering_objects = _require_list(contract, "entering_objects", allow_empty=True)
    draw_paths = _require_list(contract, "draw_on_paths", allow_empty=True)
    timeline = _require_list(contract, "timeline")
    forbidden_events = _require_list(contract, "forbidden_events")

    object_ids: set[str] = set()
    fixed_ids: set[str] = set()
    fixed_aliases: dict[str, list[str]] = {}
    lines = [
        "HARD MOTION CONTRACT - this overrides any ambiguous prose above.",
        "Fixed persistent objects already present in the first frame:",
    ]
    for item in fixed_objects:
        if not isinstance(item, dict):
            raise RuntimeError("Every fixed_objects entry must be an object.")
        object_id = str(item.get("id", "")).strip()
        description = str(item.get("description", "")).strip()
        rule = str(item.get("rule", "")).strip()
        aliases = item.get("prompt_aliases")
        if (
            not object_id
            or not description
            or rule not in FIXED_RULES
            or not isinstance(aliases, list)
            or not aliases
            or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)
        ):
            raise RuntimeError("Every fixed object needs id, description, prompt_aliases, and a supported rule.")
        if object_id in object_ids:
            raise RuntimeError(f"Duplicate motion object id: {object_id}.")
        object_ids.add(object_id)
        fixed_ids.add(object_id)
        fixed_aliases[object_id] = [alias.strip().casefold() for alias in aliases]
        lines.append(f"- [{object_id}] {description}; rule={rule}; never enter, leave, flip, duplicate, or get replaced.")

    prose = f"{spec.get('prompt', '')} {spec.get('motion_intent', '')}"
    sentences = [sentence.strip() for sentence in re.split(r"[.!?。！？;；\n]+", prose) if sentence.strip()]
    clauses = [
        clause.strip()
        for sentence in sentences
        for clause in re.split(
            r"[,，:：]|\b(?:while|then|after|before|followed by|and then)\b|随后|然后|同时|之后|之前",
            sentence,
            flags=re.IGNORECASE,
        )
        if clause.strip()
    ]
    folded_prose = prose.casefold()
    for object_id, aliases in fixed_aliases.items():
        if not any(alias in folded_prose for alias in aliases):
            raise RuntimeError(f"Fixed object {object_id!r} must be named in prompt or motion_intent using one prompt_alias.")
        for alias in aliases:
            for clause in clauses:
                folded = clause.casefold()
                if alias in folded and FIXED_ENTRANCE_RE.search(clause) and not NEGATION_RE.search(clause):
                    raise RuntimeError(
                        f"Prompt contradiction: fixed object {object_id!r} alias {alias!r} receives an entrance/change instruction: {clause!r}."
                    )

    lines.append("Entering rigid objects:")
    for item in entering_objects:
        if not isinstance(item, dict):
            raise RuntimeError("Every entering_objects entry must be an object.")
        object_id = str(item.get("id", "")).strip()
        description = str(item.get("description", "")).strip()
        motion = str(item.get("motion_primitive", "")).strip()
        final_region = str(item.get("final_region", "")).strip()
        if not all((object_id, description, motion, final_region)) or motion not in ENTERING_PRIMITIVES:
            raise RuntimeError(
                f"Every entering object needs id, description, final_region, and motion_primitive from {sorted(ENTERING_PRIMITIVES)}."
            )
        if object_id in object_ids:
            raise RuntimeError(f"Duplicate motion object id: {object_id}.")
        object_ids.add(object_id)
        lines.append(
            f"- [{object_id}] {description}; use only {motion}; remain a rigid cutout at near-final scale; "
            f"land in {final_region} and never cross into another object's zone."
        )

    lines.append("Draw-on paths that are strokes, never cards or flying objects:")
    for item in draw_paths:
        if not isinstance(item, dict):
            raise RuntimeError("Every draw_on_paths entry must be an object.")
        path_id = str(item.get("id", "")).strip()
        surface_id = str(item.get("surface_id", "")).strip()
        description = str(item.get("path_description", "")).strip()
        direction = str(item.get("direction", "")).strip()
        mode = str(item.get("draw_mode", "")).strip()
        marker_rule = str(item.get("marker_rule", "")).strip()
        if not all((path_id, surface_id, description, direction, marker_rule)) or mode not in DRAW_MODES:
            raise RuntimeError("Every draw path needs id, fixed surface_id, path_description, direction, supported draw_mode, and marker_rule.")
        if path_id in object_ids:
            raise RuntimeError(f"Duplicate motion object id: {path_id}.")
        if surface_id not in fixed_ids:
            raise RuntimeError(f"Draw path {path_id} must target a fixed surface, got {surface_id!r}.")
        object_ids.add(path_id)
        lines.append(
            f"- [{path_id}] stays entirely on [{surface_id}]. {description}. Draw {direction} by {mode}; "
            f"{marker_rule}. Existing stroke remains visible behind the growing tip."
        )

    duration = float(spec.get("timing", {}).get("request_duration_seconds") or 0)
    max_action_groups = 4 if duration <= 5 else 7
    previous_end = 0.0
    action_groups = 0
    has_final_hold = False
    lines.append("Strict serial timeline:")
    for index, item in enumerate(timeline, start=1):
        if not isinstance(item, dict):
            raise RuntimeError("Every timeline entry must be an object.")
        start = item.get("start_pct")
        end = item.get("end_pct")
        behavior = str(item.get("behavior", "")).strip()
        refs = item.get("object_ids")
        instruction = str(item.get("instruction", "")).strip()
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not 0 <= start < end <= 100:
            raise RuntimeError("Every timeline entry needs 0 <= start_pct < end_pct <= 100.")
        if start < previous_end:
            raise RuntimeError("motion_contract.timeline must be serial and non-overlapping.")
        if not isinstance(refs, list) or not refs or any(ref not in object_ids for ref in refs):
            raise RuntimeError("Every timeline object_ids list must reference declared motion objects.")
        if behavior not in TIMELINE_BEHAVIORS or not instruction:
            raise RuntimeError(f"Every timeline entry needs instruction and behavior from {sorted(TIMELINE_BEHAVIORS)}.")
        if behavior == "hold":
            has_final_hold = index == len(timeline) and end == 100 and start <= 75
        else:
            action_groups += 1
        previous_end = float(end)
        lines.append(f"- {start:g}-{end:g}% [{behavior}] {', '.join(refs)}: {instruction}")
    if action_groups > max_action_groups:
        raise RuntimeError(f"A {duration:g}s Seedance scene supports at most {max_action_groups} action groups; found {action_groups}.")
    if not has_final_hold:
        raise RuntimeError("The final timeline entry must be a hold ending at 100% and starting no later than 75%.")

    normalized_forbidden = "\n".join(str(item).lower() for item in forbidden_events)
    missing_forbidden = sorted(term for term in REQUIRED_FORBIDDEN_EVENTS if term not in normalized_forbidden)
    if missing_forbidden:
        raise RuntimeError(f"motion_contract.forbidden_events must explicitly forbid: {', '.join(missing_forbidden)}.")
    lines.append("Forbidden events:")
    lines.extend(f"- {item}" for item in forbidden_events)
    return "\n".join(lines)


def build_request_payload(spec: dict, project_root: Path) -> dict:
    continuity_report = validate_keyframe_continuity(project_root, spec)
    if continuity_report["status"] != "pass":
        details = "\n- ".join(continuity_report["errors"])
        raise RuntimeError(
            "Keyframe continuity gate failed before Seedance submission:\n- " + details
        )
    first_frame = _frame_by_role(spec, "first_frame")
    last_frame = _frame_by_role(spec, "last_frame")
    first_path = resolve_path(project_root, first_frame["path"])
    last_path = resolve_path(project_root, last_frame["path"])
    if not first_path.exists():
        raise FileNotFoundError(f"First-frame image does not exist: {first_path}")
    if not last_path.exists():
        raise FileNotFoundError(f"Last-frame image does not exist: {last_path}")

    prompt = spec.get("prompt", "").strip()
    motion_intent = spec.get("motion_intent", "").strip()
    if not prompt:
        raise RuntimeError("Scene spec prompt is empty.")
    if not motion_intent:
        raise RuntimeError("Scene spec motion_intent is empty.")

    timing = spec.get("timing", {})
    duration = int(timing.get("request_duration_seconds") or round(timing["duration_seconds"]))
    if duration < 4 or duration > 12:
        raise RuntimeError(
            f"Seedance 1.5 Pro supports 4-12 second clips, got `{duration}` for scene `{spec.get('scene_slug')}`."
        )

    resolution = spec.get("resolution", {})
    aspect_ratio = str(resolution.get("aspect_ratio", "")).strip()
    if aspect_ratio not in {"16:9", "9:16"}:
        raise RuntimeError(
            "SEEDANCE_SCENE.json must contain the Gate 1 resolution.aspect_ratio; "
            "submission will not silently default to 16:9."
        )
    seedance = spec.get("seedance", {})
    compiled_contract = compile_motion_contract(spec)
    text_prompt = f"{prompt}\n\nMotion intent: {motion_intent}\n\n{compiled_contract}"
    return {
        "model": spec.get("video_model", "doubao-seedance-1-5-pro-251215"),
        "content": [
            {
                "type": "text",
                "text": text_prompt,
            },
            {
                "type": "image_url",
                "image_url": {"url": path_to_data_uri(first_path)},
                "role": "first_frame",
            },
            {
                "type": "image_url",
                "image_url": {"url": path_to_data_uri(last_path)},
                "role": "last_frame",
            },
        ],
        "generate_audio": bool(seedance.get("generate_audio", False)),
        "ratio": aspect_ratio,
        "resolution": resolution.get("resolution_tier", "720p"),
        "duration": duration,
        "watermark": bool(seedance.get("watermark", False)),
        "return_last_frame": bool(seedance.get("return_last_frame", False)),
    }


def poll_task(task_id: str, api_key: str, *, poll_interval: int, timeout_seconds: int) -> dict:
    deadline = time.time() + timeout_seconds
    last_response: dict | None = None
    while time.time() < deadline:
        response = request_json(
            "GET",
            f"{ARK_BASE_URL}/{task_id}",
            headers=build_ark_headers(api_key),
            timeout=120,
        )
        last_response = response
        status = str(response.get("status", "")).lower()
        print(f"status={status or 'unknown'}")
        if status in TERMINAL_STATES:
            return response
        time.sleep(max(1, poll_interval))
    raise TimeoutError(
        f"Timed out waiting for Seedance task {task_id}. Last response: {last_response}"
    )


def _extract_media_url(response: dict, *, suffix: str) -> str:
    direct = deep_find_first(response, ("video_url",)) if suffix == ".mp4" else deep_find_first(
        response, ("last_frame_url",)
    )
    if isinstance(direct, str) and direct:
        return direct

    def walk(payload: object) -> str:
        if isinstance(payload, dict):
            for value in payload.values():
                found = walk(value)
                if found:
                    return found
        elif isinstance(payload, list):
            for item in payload:
                found = walk(item)
                if found:
                    return found
        elif isinstance(payload, str):
            lowered = payload.lower()
            if payload.startswith("http") and suffix in lowered:
                return payload
        return ""

    return walk(response)


def write_run_artifacts(project_root: Path, spec: dict, response: dict) -> tuple[Path, Path]:
    output = spec.get("output", {})
    metadata_path = resolve_path(project_root, output["metadata_path"])
    write_json(metadata_path, response)
    video_path = resolve_path(project_root, output["video_path"])
    return metadata_path, video_path


def main() -> None:
    args = parse_args()
    project_root, scene_spec_path = resolve_scene_spec(args)
    spec = load_json(scene_spec_path)
    api_key = env_value("ARK_API_KEY")
    if not api_key:
        raise RuntimeError(f"Missing ARK_API_KEY in process env or {SKILL_ENV_PATH}.")

    payload = build_request_payload(spec, project_root)
    if args.dry_run:
        print(f"Scene spec: {scene_spec_path}")
        print(payload)
        return

    submission = request_json(
        "POST",
        ARK_BASE_URL,
        headers=build_ark_headers(api_key),
        payload=payload,
        timeout=180,
    )
    task_id = submission.get("id") or submission.get("task_id")
    if not task_id:
        raise RuntimeError(f"Seedance submission did not return a task id: {submission}")

    spec["seedance_run"] = {
        "submitted_at": int(time.time()),
        "request": payload,
        "submission": submission,
    }
    write_json(scene_spec_path, spec)
    print(f"Submitted Seedance task for {scene_spec_path.name}: {task_id}")

    final_response = poll_task(
        str(task_id),
        api_key,
        poll_interval=args.poll_interval,
        timeout_seconds=args.timeout_seconds,
    )
    metadata_path, video_path = write_run_artifacts(project_root, spec, final_response)
    spec["seedance_run"]["final_response_path"] = str(metadata_path)

    status = str(final_response.get("status", "")).lower()
    if status != "succeeded":
        spec["seedance_run"]["status"] = status
        write_json(scene_spec_path, spec)
        raise RuntimeError(f"Seedance task ended with status `{status}`: {final_response}")

    video_url = _extract_media_url(final_response, suffix=".mp4")
    if not video_url:
        raise RuntimeError(f"Seedance completed without a video_url: {final_response}")

    if args.download:
        download_file(video_url, video_path)
        spec["seedance_run"]["downloaded_video_path"] = str(video_path)
        print(f"Downloaded video to {video_path}")
    else:
        print(f"Video URL: {video_url}")

    last_frame_url = _extract_media_url(final_response, suffix=".png")
    spec["seedance_run"]["status"] = "succeeded"
    spec["seedance_run"]["video_url"] = video_url
    if last_frame_url:
        spec["seedance_run"]["last_frame_url"] = last_frame_url
    write_json(scene_spec_path, spec)
    print(f"Saved Seedance metadata to {metadata_path}")


if __name__ == "__main__":
    main()
