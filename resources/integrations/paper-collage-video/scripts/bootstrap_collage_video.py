#!/usr/bin/env python3
"""
Scaffold a paper-collage video project from the production grammar used in the
Skool practice kit.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from pathlib import Path

from preflight import run_checks as run_preflight_checks


CANONICAL_BEATS = [
    ("closed-scroll", "Closed or hidden state", 1.0),
    ("unfolding", "Reveal mechanic opens the scene", 1.2),
    ("reveal-complete", "Scene spans the frame", 1.0),
    ("hero-arrival", "Hero element enters", 1.8),
    ("living-scene", "Looping tableau or hold", 5.0),
]

DEFAULT_SEQUENCE_SCENE_COUNT = 7
DEFAULT_ASPECT_RATIO = "16:9"
SUPPORTED_ASPECT_RATIOS = ["16:9", "9:16"]
ASPECT_CANVASES = {
    "16:9": {"width": 1536, "height": 864, "orientation": "horizontal"},
    "9:16": {"width": 864, "height": 1536, "orientation": "vertical"},
}
REMOTION_CANVASES = {
    "16:9": {"width": 1920, "height": 1080},
    "9:16": {"width": 1080, "height": 1920},
}
ASSET_MANIFEST_VERSION = 2
SUPPORTED_STYLE_FAMILIES = ["vox-mixed-media"]
SUPPORTED_SCENE_DURATION_POLICIES = [
    "not-applicable",
    "auto-by-content",
]
EDGE_TTS_VOICE = "zh-CN-YunjianNeural"
SRT_TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})"
)
SKILL_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a paper-collage video planning workspace."
    )
    parser.add_argument("--output", required=True, help="Output project directory")
    parser.add_argument("--scene", required=True, help="One-sentence scene concept")
    parser.add_argument(
        "--mode",
        choices=["single-scene", "vo-sequence"],
        default="single-scene",
        help="Planning workflow shape to scaffold",
    )
    parser.add_argument(
        "--production-mode",
        choices=["remotion-code", "video-model"],
        required=True,
        help="Gate 1 production mode selected by the user",
    )
    parser.add_argument("--reference-url", default="", help="Reference clip URL")
    parser.add_argument(
        "--duration",
        type=float,
        required=True,
        help="Whole-video total duration in seconds, never a per-scene Seedance duration",
    )
    parser.add_argument(
        "--duration-source",
        choices=["user", "audio", "generated-voiceover", "estimated", "authorized-default"],
        required=True,
        help="What should be treated as the canonical whole-video duration source",
    )
    parser.add_argument(
        "--scene-duration-policy",
        choices=SUPPORTED_SCENE_DURATION_POLICIES,
        default=None,
        help="Optional compatibility flag; policy is derived from production mode",
    )
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument("--engine", default="remotion", help="Animation engine")
    parser.add_argument(
        "--video-model",
        default="doubao-seedance-1-5-pro-251215",
        help="Primary video generation model for complex scenes",
    )
    parser.add_argument(
        "--image-model",
        default="imagegen / Imagen",
        help="Primary image generation stack",
    )
    parser.add_argument(
        "--audio-model",
        default="Edge TTS voiceover + optional music/foley",
        help="Audio stack; generated narration is fixed to Edge TTS",
    )
    parser.add_argument(
        "--kit-path",
        default="",
        help="Optional path to an existing practice kit with assets/ and audio/",
    )
    parser.add_argument(
        "--narration-file",
        default="",
        help="Optional text file with one narration beat per non-empty line",
    )
    parser.add_argument(
        "--subtitle-file",
        default="",
        help="Optional SRT file; required for generated voiceover and used as the beat timeline",
    )
    parser.add_argument(
        "--voiceover-metadata-file",
        default="",
        help="Optional metadata JSON produced by generate_edge_voiceover.py",
    )
    parser.add_argument(
        "--srt-scene-plan-file",
        default="",
        help="Optional semantic scene plan keyed by 1-based SRT cue ranges; required for generated voiceover vo-sequence projects",
    )
    parser.add_argument(
        "--scene-count",
        type=int,
        default=0,
        help="Target number of scenes for vo-sequence mode; 0 lets the scaffold derive it from content duration",
    )
    parser.add_argument(
        "--style-family",
        choices=SUPPORTED_STYLE_FAMILIES,
        default="vox-mixed-media",
        help="Visual grammar; this skill supports vox-mixed-media only",
    )
    parser.add_argument(
        "--background-policy",
        choices=["per-scene", "shared-continuity"],
        default="per-scene",
        help="Use unique scene backgrounds unless the user explicitly authorizes continuity reuse",
    )
    parser.add_argument(
        "--background-sharing-authorized",
        action="store_true",
        help="Record explicit user authorization for shared-continuity backgrounds",
    )
    parser.add_argument(
        "--scene-complexity",
        choices=["auto", "simple", "complex"],
        default="auto",
        help="How demanding the scene structure is expected to be",
    )
    parser.add_argument(
        "--animation-strategy",
        choices=["auto", "remotion-cutout", "seedance-first-last"],
        default="auto",
        help="Preferred production route for approved scenes",
    )
    parser.add_argument(
        "--keyframe-count",
        type=int,
        default=2,
        help="How many still frames to prepare when using the Seedance first+last route",
    )
    parser.add_argument(
        "--aspect-ratio",
        choices=SUPPORTED_ASPECT_RATIOS,
        required=True,
        help="Delivery aspect ratio",
    )
    parser.add_argument(
        "--orientation",
        choices=["horizontal", "vertical", "square", "auto"],
        default="auto",
        help="Primary layout orientation",
    )
    parser.add_argument(
        "--audio-mode",
        choices=["use-source-audio", "generate-voiceover", "no-audio"],
        required=True,
        help="Gate 1 audio mode derived from source-audio presence or the user's voiceover choice",
    )
    parser.add_argument(
        "--source-audio-file",
        default="",
        help="Required when --audio-mode=use-source-audio",
    )
    parser.add_argument(
        "--gate1-source",
        choices=["user-selection", "user-authorized-defaults"],
        required=True,
        help="How Gate 1 choices were authorized",
    )
    parser.add_argument(
        "--with-remotion-template",
        action="store_true",
        help="Compatibility flag; remotion-code now always generates 07_remotion/ automatically",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist",
    )
    args = parser.parse_args()
    if args.production_mode == "video-model" and args.with_remotion_template:
        parser.error(
            "--with-remotion-template is incompatible with --production-mode=video-model. "
            "Video-model projects use exactly two keyframes per Scene and must not scaffold Remotion assets."
        )
    if args.production_mode == "video-model" and args.animation_strategy == "remotion-cutout":
        parser.error(
            "--animation-strategy=remotion-cutout conflicts with --production-mode=video-model. "
            "Use auto or seedance-first-last."
        )
    if args.production_mode == "remotion-code" and args.animation_strategy == "seedance-first-last":
        parser.error(
            "--animation-strategy=seedance-first-last conflicts with --production-mode=remotion-code. "
            "Choose video-model at Gate 1 instead of mixing engines inside one project."
        )
    args.engine = "remotion" if args.production_mode == "remotion-code" else "seedance"
    if args.production_mode == "remotion-code":
        args.with_remotion_template = True
    args.scene_duration_policy = (
        "auto-by-content"
        if args.production_mode == "video-model"
        else "not-applicable"
    )
    return args


def canvas_contract(aspect_ratio: str) -> dict[str, int | str]:
    try:
        canvas = ASPECT_CANVASES[aspect_ratio]
    except KeyError as exc:
        raise ValueError(f"Unsupported Gate 1 aspect ratio: {aspect_ratio!r}") from exc
    return {
        "source": "gate-1",
        "aspect_ratio": aspect_ratio,
        "width": int(canvas["width"]),
        "height": int(canvas["height"]),
        "orientation": str(canvas["orientation"]),
    }


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Re-run with --force to overwrite.")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def copy_tree_if_present(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return True


def scaled_beats(duration: float) -> list[dict]:
    factor = duration / 10.0
    beats = []
    cursor = 0.0
    for slug, title, canonical_seconds in CANONICAL_BEATS:
        beat_duration = round(canonical_seconds * factor, 2)
        start = round(cursor, 2)
        end = round(cursor + beat_duration, 2)
        beats.append(
            {
                "slug": slug,
                "title": title,
                "start_seconds": start,
                "end_seconds": end,
                "duration_seconds": beat_duration,
            }
        )
        cursor = end
    beats[-1]["end_seconds"] = round(duration, 2)
    beats[-1]["duration_seconds"] = round(duration - beats[-1]["start_seconds"], 2)
    return beats


def slugify(value: str) -> str:
    lowered = value.lower()
    cleaned = []
    prev_dash = False
    for char in lowered:
        if char.isalnum():
            cleaned.append(char)
            prev_dash = False
        elif not prev_dash:
            cleaned.append("-")
            prev_dash = True
    slug = "".join(cleaned).strip("-")
    return slug or "beat"


def infer_orientation(aspect_ratio: str, orientation: str) -> str:
    if orientation != "auto":
        return orientation
    return {
        "16:9": "horizontal",
        "4:3": "horizontal",
        "9:16": "vertical",
        "3:4": "vertical",
        "1:1": "square",
    }.get(aspect_ratio, "horizontal")


def keyframe_count_for_strategy(args: argparse.Namespace) -> int:
    if args.production_mode == "video-model" or args.animation_strategy == "seedance-first-last":
        return 2
    return max(0, min(2, args.keyframe_count))


def recommend_scene_route(args: argparse.Namespace) -> str:
    if args.production_mode == "video-model":
        return "seedance-first-last"
    return "remotion-cutout"


def style_family_notes(style_family: str) -> dict[str, list[str] | str]:
    return {
        "label": "Vox-style mixed-media editorial collage",
        "materials": [
            "bright tactile cut-paper layers with rough fibrous white borders",
            "broad chromatic color fields with warm-cool contrast",
            "crisp halftone, corrugated, watercolor, and paper-grain textures",
        ],
        "motion": [
            "snappy pop-ins and slide-ins",
            "marker sweeps, circles, and underlines",
            "one dominant emphasis action per beat",
        ],
        "editorial": [
            "favor charts, maps, compare-and-contrast frames, and redaction blocks",
            "avoid long readable text inside generated imagery",
            "keep the frame magazine-editorial rather than investigative-tableau by default",
            "keep backgrounds quiet, broad, and low-clutter so the hero layer stays dominant",
            "treat quiet as low-detail rather than beige or desaturated",
            "follow the 0720-bright-paper color hierarchy unless the user explicitly overrides it",
        ],
    }


def stable_scene_slug(value: str, limit: int = 40) -> str:
    slug = slugify(value)[:limit].strip("-")
    return slug or "scene"


def make_check(check_id: str, ok: bool, detail: str, fix: str) -> dict:
    return {
        "id": check_id,
        "status": "pass" if ok else "needs-action",
        "detail": detail,
        "fix": fix,
    }


def self_check(args: argparse.Namespace) -> dict:
    return run_preflight_checks()


def resolve_gate_file(args: argparse.Namespace, value: str) -> Path | None:
    if not value:
        return None
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    project_relative = (Path(args.output).expanduser().resolve() / candidate).resolve()
    return project_relative if project_relative.exists() else candidate.resolve()


def gate1_check(args: argparse.Namespace) -> dict:
    source_audio = resolve_gate_file(args, args.source_audio_file)
    source_audio_ok = source_audio is not None and source_audio.is_file()
    subtitle_file = resolve_gate_file(args, args.subtitle_file)
    subtitle_ok = subtitle_file is not None and subtitle_file.is_file()
    voiceover_metadata = resolve_gate_file(args, args.voiceover_metadata_file)
    voiceover_metadata_ok = voiceover_metadata is not None and voiceover_metadata.is_file()
    srt_scene_plan = resolve_gate_file(args, args.srt_scene_plan_file)
    srt_scene_plan_ok = srt_scene_plan is not None and srt_scene_plan.is_file()
    voiceover_metadata_payload = {}
    if voiceover_metadata_ok:
        try:
            voiceover_metadata_payload = json.loads(
                voiceover_metadata.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            voiceover_metadata_payload = {}
    measured_voiceover_duration = voiceover_metadata_payload.get("duration_seconds")
    voiceover_duration_matches = (
        isinstance(measured_voiceover_duration, (int, float))
        and not isinstance(measured_voiceover_duration, bool)
        and abs(float(measured_voiceover_duration) - args.duration) <= 0.25
    )
    checks = [
        make_check(
            "production_mode_locked",
            args.production_mode in {"remotion-code", "video-model"},
            f"Production mode is locked to {args.production_mode}.",
            "Ask the user to select remotion-code or video-model.",
        ),
        make_check(
            "style_family_locked",
            args.style_family in SUPPORTED_STYLE_FAMILIES,
            f"Style family is locked to {args.style_family}.",
            "Ask the user to select a supported style family.",
        ),
        make_check(
            "aspect_ratio_locked",
            args.aspect_ratio in SUPPORTED_ASPECT_RATIOS,
            f"Aspect ratio is locked to {args.aspect_ratio}.",
            "Ask the user to select 16:9 or 9:16.",
        ),
        make_check(
            "total_duration_locked",
            args.duration > 0,
            f"Whole-video duration is locked to {args.duration:.2f}s from {args.duration_source}.",
            "Use the source-audio duration, a user-specified total, or a content estimate.",
        ),
        make_check(
            "audio_mode_consistent",
            (args.audio_mode == "use-source-audio" and args.duration_source == "audio" and source_audio_ok)
            or (
                args.audio_mode == "generate-voiceover"
                and args.duration_source == "generated-voiceover"
                and source_audio_ok
                and subtitle_ok
                and voiceover_metadata_ok
                and (args.mode != "vo-sequence" or srt_scene_plan_ok)
            )
            or (
                args.audio_mode == "no-audio"
                and args.duration_source not in {"audio", "generated-voiceover"}
                and not args.source_audio_file
                and not args.subtitle_file
            ),
            "Audio mode and duration source are consistent.",
            "Use source audio with --duration-source audio; generated voiceover requires its MP3, SRT, metadata, semantic SRT scene plan for vo-sequence, and --duration-source generated-voiceover; otherwise use no-audio.",
        ),
        make_check(
            "scene_duration_policy",
            (
                args.production_mode == "video-model"
                and args.scene_duration_policy == "auto-by-content"
            )
            or (
                args.production_mode == "remotion-code"
                and args.scene_duration_policy == "not-applicable"
            ),
            f"Per-scene duration policy is {args.scene_duration_policy}.",
            "Policy must be derived automatically: auto-by-content for video-model and not-applicable for remotion-code.",
        ),
        make_check(
            "voiceover_duration_locked",
            args.audio_mode != "generate-voiceover"
            or (
                voiceover_metadata_payload.get("provider") == "edge-tts-online"
                and voiceover_metadata_payload.get("voice") == EDGE_TTS_VOICE
                and voiceover_duration_matches
            ),
            (
                "Generated voiceover metadata, fixed voice, and measured duration are locked."
                if args.audio_mode == "generate-voiceover" and voiceover_duration_matches
                else "Generated voiceover metadata or measured duration does not match."
                if args.audio_mode == "generate-voiceover"
                else "Voiceover duration lock is not required for this audio mode."
            ),
            "Pass the duration_seconds from voiceover-metadata.json as --duration and keep the fixed Edge TTS voice.",
        ),
        make_check(
            "choice_origin",
            (
                args.gate1_source == "user-selection"
                and args.duration_source in {"user", "audio", "generated-voiceover", "estimated"}
            )
            or (
                args.gate1_source == "user-authorized-defaults"
                and args.duration_source
                in {"authorized-default", "audio", "generated-voiceover", "estimated"}
            ),
            f"Gate 1 choice origin is {args.gate1_source}.",
            "Record whether the whole-video duration came from the user, source audio, a content estimate, or authorized defaults.",
        ),
        make_check(
            "background_policy",
            args.background_policy == "per-scene" or args.background_sharing_authorized,
            f"Background policy is {args.background_policy}; sharing authorization is {args.background_sharing_authorized}.",
            "Use per-scene backgrounds, or record explicit user authorization before selecting shared-continuity.",
        ),
    ]
    return {
        "gate": "Gate 1",
        "status": "pass" if all(check["status"] == "pass" for check in checks) else "fail",
        "source": args.gate1_source,
        "checks": checks,
        "locked_values": {
            "production_mode": args.production_mode,
            "style_family": args.style_family,
            "aspect_ratio": args.aspect_ratio,
            "total_duration_seconds": args.duration,
            "total_duration_source": args.duration_source,
            "scene_duration_policy": args.scene_duration_policy,
            "audio_mode": args.audio_mode,
            "source_audio_file": str(source_audio) if source_audio_ok else "",
            "subtitle_file": str(subtitle_file) if subtitle_ok else "",
            "voiceover_metadata_file": str(voiceover_metadata)
            if voiceover_metadata_ok
            else "",
            "srt_scene_plan_file": str(srt_scene_plan) if srt_scene_plan_ok else "",
            "background_policy": args.background_policy,
            "background_sharing_authorized": args.background_sharing_authorized,
            "asset_source_policy": "imagegen-or-user-supplied",
        },
    }


def load_narration_lines(path: str) -> list[str]:
    if not path:
        return []
    narration_path = Path(path).expanduser().resolve()
    return [
        line.strip()
        for line in narration_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def split_narration_text(text: str) -> list[str]:
    normalized = re.sub(r"\r\n?", "\n", text).strip()
    if not normalized:
        return []
    sentences = [part.strip() for part in re.split(r"(?<=[。！？!?；;\.])\s*|\n+", normalized) if part.strip()]
    if len(sentences) == 1 and len(normalized) >= 48:
        clauses = [part.strip() for part in re.split(r"(?<=[，,：:])\s*", normalized) if part.strip()]
        if len(clauses) > 1:
            sentences = clauses
    return sentences


def srt_timestamp_seconds(value: str) -> float:
    hours, minutes, remainder = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(remainder)


def load_srt_cues(path: str) -> list[dict]:
    if not path:
        return []
    subtitle_path = Path(path).expanduser().resolve()
    text = subtitle_path.read_text(encoding="utf-8-sig")
    cues = []
    for block in re.split(r"\r?\n\s*\r?\n", text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next(
            (index for index, line in enumerate(lines) if SRT_TIME_RE.search(line)),
            None,
        )
        if timing_index is None:
            continue
        match = SRT_TIME_RE.search(lines[timing_index])
        narration = " ".join(lines[timing_index + 1 :]).strip()
        if not match or not narration:
            continue
        cues.append(
            {
                "start_seconds": srt_timestamp_seconds(match.group("start")),
                "end_seconds": srt_timestamp_seconds(match.group("end")),
                "narration": narration,
            }
        )
    if not cues:
        raise ValueError(f"No valid subtitle cues found in {subtitle_path}")
    return sorted(cues, key=lambda cue: cue["start_seconds"])


def srt_beats(path: str, total_duration: float) -> list[dict]:
    cues = load_srt_cues(path)
    beats = []
    for index, cue in enumerate(cues):
        start = 0.0 if index == 0 else cue["start_seconds"]
        end = (
            cues[index + 1]["start_seconds"]
            if index + 1 < len(cues)
            else total_duration
        )
        # Edge word/sentence boundaries can overlap by a few milliseconds.
        # Use the next cue start as the visual cut so scene windows stay contiguous.
        end = max(end, start + 0.01)
        narration = cue["narration"]
        beats.append(
            {
                "slug": f"beat-{index + 1:02d}-{slugify(narration[:28])}",
                "title": f"Beat {index + 1}",
                "narration": narration,
                "start_seconds": round(start, 3),
                "end_seconds": round(end, 3),
                "duration_seconds": round(end - start, 3),
                "timing_source": "srt",
                "srt_cue_index": index + 1,
            }
        )
    return beats


def scenes_from_srt_plan(beats: list[dict], path: str) -> list[dict]:
    plan_path = Path(path).expanduser().resolve()
    payload = json.loads(plan_path.read_text(encoding="utf-8"))
    entries = payload.get("scenes", []) if isinstance(payload, dict) else []
    if not entries:
        raise ValueError(f"SRT scene plan contains no scenes: {plan_path}")

    scenes = []
    assigned_indices: list[int] = []
    for scene_index, entry in enumerate(entries, start=1):
        cue_start = int(entry.get("cue_start", 0))
        cue_end = int(entry.get("cue_end", 0))
        if cue_start < 1 or cue_end < cue_start or cue_end > len(beats):
            raise ValueError(
                f"Invalid cue range {cue_start}-{cue_end} in SRT scene plan {plan_path}"
            )
        chunk = beats[cue_start - 1 : cue_end]
        assigned_indices.extend(range(cue_start, cue_end + 1))
        requested_slug = str(entry.get("scene_slug", "")).strip()
        slug = requested_slug or f"scene-{scene_index:02d}-{chunk[0]['slug']}"
        scenes.append(
            {
                "scene_index": scene_index,
                "slug": slug,
                "scene_goal": str(entry.get("scene_goal", "")).strip(),
                "cue_start": cue_start,
                "cue_end": cue_end,
                "beat_slugs": [beat["slug"] for beat in chunk],
                "start_seconds": chunk[0]["start_seconds"],
                "end_seconds": chunk[-1]["end_seconds"],
                "duration_seconds": round(
                    chunk[-1]["end_seconds"] - chunk[0]["start_seconds"], 3
                ),
                "beats": chunk,
                "timing_source": "srt",
            }
        )

    expected_indices = list(range(1, len(beats) + 1))
    if assigned_indices != expected_indices:
        raise ValueError(
            "SRT scene plan must assign every cue exactly once in contiguous source order."
        )
    return scenes


def narration_beats(lines: list[str], duration: float) -> list[dict]:
    if not lines:
        return []
    beat_duration = duration / len(lines)
    beats = []
    cursor = 0.0
    for index, line in enumerate(lines, start=1):
        start = round(cursor, 2)
        end = round(duration if index == len(lines) else cursor + beat_duration, 2)
        beats.append(
            {
                "slug": f"beat-{index:02d}-{slugify(line[:28])}",
                "title": f"Beat {index}",
                "narration": line,
                "start_seconds": start,
                "end_seconds": end,
                "duration_seconds": round(end - start, 2),
            }
        )
        cursor = end
    return beats


def group_beats_into_scenes(beats: list[dict], scene_count: int) -> list[dict]:
    if not beats:
        return []
    target = max(1, min(scene_count, len(beats)))
    scenes = []
    total = len(beats)
    for index in range(target):
        start_idx = round(index * total / target)
        end_idx = round((index + 1) * total / target)
        chunk = beats[start_idx:end_idx]
        if not chunk:
            continue
        scenes.append(
            {
                "scene_index": index + 1,
                "slug": f"scene-{index + 1:02d}-{chunk[0]['slug']}",
                "beat_slugs": [beat["slug"] for beat in chunk],
                "start_seconds": chunk[0]["start_seconds"],
                "end_seconds": chunk[-1]["end_seconds"],
                "duration_seconds": round(
                    chunk[-1]["end_seconds"] - chunk[0]["start_seconds"], 2
                ),
                "beats": chunk,
            }
        )
    return scenes


def resolve_scene_count(args: argparse.Namespace, beats: list[dict]) -> int:
    if args.mode != "vo-sequence":
        return 1
    if args.production_mode != "video-model":
        return args.scene_count if args.scene_count > 0 else DEFAULT_SEQUENCE_SCENE_COUNT

    target_seconds = 8
    preferred_count = math.ceil(args.duration / target_seconds)
    minimum_api_safe_count = math.ceil(args.duration / 12)
    requested_count = args.scene_count if args.scene_count > 0 else preferred_count
    # Content beats remain the hard upper bound; an oversized beat will fail later
    # with an explicit instruction to split the narration semantically.
    return max(1, min(len(beats), max(requested_count, minimum_api_safe_count)))


def project_config(scene: str, args: argparse.Namespace) -> dict:
    narration_lines = load_narration_lines(args.narration_file)
    if args.mode == "vo-sequence" and not narration_lines and not args.subtitle_file:
        narration_lines = split_narration_text(scene)
    resolved_subtitle = resolve_gate_file(args, args.subtitle_file)
    if args.subtitle_file:
        beats = srt_beats(str(resolved_subtitle), args.duration)
        narration_lines = [beat["narration"] for beat in beats]
    elif args.mode == "vo-sequence":
        beats = narration_beats(narration_lines, args.duration)
    else:
        beats = scaled_beats(args.duration)
    resolved_orientation = infer_orientation(args.aspect_ratio, args.orientation)
    resolved_canvas = canvas_contract(args.aspect_ratio)
    route = recommend_scene_route(args)
    keyframe_count = keyframe_count_for_strategy(args)
    check_report = self_check(args)
    gate1_report = gate1_check(args)
    resolved_scene_plan = resolve_gate_file(args, args.srt_scene_plan_file)
    planned_scenes = (
        scenes_from_srt_plan(beats, str(resolved_scene_plan))
        if args.mode == "vo-sequence" and resolved_scene_plan
        else []
    )
    resolved_scene_count = (
        len(planned_scenes) if planned_scenes else resolve_scene_count(args, beats)
    )
    config = {
        "mode": args.mode,
        "production_mode": args.production_mode,
        "scene": scene,
        "reference_url": args.reference_url,
        "total_duration_seconds": args.duration,
        "total_duration_source": args.duration_source,
        "duration_seconds": args.duration,
        "duration_source": args.duration_source,
        "fps": args.fps,
        "engine": "remotion" if args.production_mode == "remotion-code" else "seedance",
        "style_family": args.style_family,
        "video_model": args.video_model,
        "image_model": args.image_model,
        "audio_model": args.audio_model,
        "delivery": {
            "aspect_ratio": args.aspect_ratio,
            "orientation": resolved_orientation,
            "canvas": resolved_canvas,
            "audio_mode": args.audio_mode,
            "source_audio_file": gate1_report["locked_values"]["source_audio_file"],
            "subtitle_file": gate1_report["locked_values"]["subtitle_file"],
            "voiceover_metadata_file": gate1_report["locked_values"][
                "voiceover_metadata_file"
            ],
            "srt_scene_plan_file": gate1_report["locked_values"][
                "srt_scene_plan_file"
            ],
        },
        "voiceover": {
            "provider": "edge-tts-online"
            if args.audio_mode == "generate-voiceover"
            else "none",
            "voice": EDGE_TTS_VOICE
            if args.audio_mode == "generate-voiceover"
            else "",
            "timeline_source": "srt" if args.subtitle_file else "narration-lines",
        },
        "background_policy": args.background_policy,
        "background_sharing_authorized": args.background_sharing_authorized,
        "image_generation_policy": {
            "asset_source_policy": "imagegen-or-user-supplied",
            "actual_tool_call_required": True,
            "provenance_required": True,
            "preserve_original_output": True,
            "local_procedural_fallback": False,
        },
        "scene_complexity": args.scene_complexity,
        "animation_strategy": {
            "selected": args.animation_strategy,
            "recommended_route": route,
            "engine_locked": args.production_mode,
            "complex_scene_recipe": (
                "Generate first_frame once with imagegen, edit that exact image into last_frame with referenced_image_paths, validate protected-background continuity, then submit both local files to doubao-seedance-1-5-pro-251215."
                if route == "seedance-first-last"
                else "Decompose dense content into additional independent raster assets and semantic motion phases while staying in Remotion."
            ),
        },
        "integrations": {
            "ark_api_key_env": "ARK_API_KEY",
        },
        "self_check": check_report,
        "gate_1": gate1_report,
        "style_rules": {
            "family": args.style_family,
            "family_label": style_family_notes(args.style_family)["label"],
            "materials": style_family_notes(args.style_family)["materials"],
            "motion": style_family_notes(args.style_family)["motion"],
            "editorial": style_family_notes(args.style_family)["editorial"],
            "asset_pipeline": "Call image_gen for every new visible asset, preserve prompt/original/receipt/hashes, then use Remotion only for animation assembly, timing, camera moves, and compositing.",
            "audio": [
                "one music bed",
                "one reveal cue",
                "one ambience bed",
                "one accent cue maximum unless justified",
            ],
        },
        "beats": beats,
    }
    if args.production_mode == "video-model":
        config["video_generation"] = {
            "provider": "volcengine-ark",
            "mode": "first-last-frame",
            "base64_input": True,
            "complex_scene_frames": 2,
            "scene_duration_policy": args.scene_duration_policy,
            "scene_duration_range_seconds": [4, 12],
            "duration_semantics": "Per-scene request duration; whole-video duration is stored separately.",
        }
    if args.mode == "vo-sequence":
        config["sequence_rules"] = {
            "background_policy": args.background_policy,
            "background_sharing_authorized": args.background_sharing_authorized,
            "unique_scene_backgrounds_required": args.background_policy == "per-scene",
            "locked_visual_system": True,
            "cutout_stroke_accent": "#E04329",
            "voiceover_drives_timing": True,
            "requested_scene_count": args.scene_count,
            "target_scene_count": resolved_scene_count,
            "engine_locked": args.production_mode,
            "minimum_approved_assets_per_remotion_scene": 4,
            "maximum_approved_assets_per_remotion_scene": 8,
            "minimum_independently_timed_assets_per_remotion_scene": 3,
            "appearance_order_follows_content": True,
        }
        config["scenes"] = planned_scenes or group_beats_into_scenes(
            beats, resolved_scene_count
        )
        config["narration_lines"] = narration_lines
    return config


def render_beat_rows(beats: list[dict]) -> str:
    rows = []
    for beat in beats:
        rows.append(
            "| {slug} | {start:.2f}s-{end:.2f}s | [claim -> physical metaphor -> payoff] | [layout archetype / reading path] | [unique background concept] | [content-specific asset IDs in causal order] | [hero projected visible width/height %] | [motion rhythm + dominant action] | [remotion / seedance] | [fill gate] |".format(
                slug=beat["slug"],
                start=beat["start_seconds"],
                end=beat["end_seconds"],
            )
        )
    return "\n".join(rows)


def brief_md(
    scene: str,
    args: argparse.Namespace,
    beats: list[dict],
    kit_copied: bool,
    scenes: list[dict],
) -> str:
    route = recommend_scene_route(args)
    resolved_orientation = infer_orientation(args.aspect_ratio, args.orientation)
    style_notes = style_family_notes(args.style_family)
    reference_line = args.reference_url or "[add reference clip or stills]"
    kit_line = (
        "Source kit copied into `source-kit/`." if kit_copied else "No kit files copied yet."
    )
    mode_line = "Narration-led multi-scene sequence" if args.mode == "vo-sequence" else "Single handcrafted collage scene"
    beat_lines = (
        chr(10).join(
            f"- {beat['slug']}: {beat['start_seconds']:.2f}s-{beat['end_seconds']:.2f}s"
            for beat in beats
        )
        if beats
        else "- [fill beats]"
    )
    sequence_lines = (
        chr(10).join(
            f"- {scene_meta['slug']}: {scene_meta['start_seconds']:.2f}s-{scene_meta['end_seconds']:.2f}s carrying {', '.join(scene_meta['beat_slugs'])}"
            for scene_meta in scenes
        )
        if scenes
        else ""
    )
    return f"""# Project Brief

## Scene

{scene}

## Goal

Rebuild or adapt this concept as a short paper-collage animation using a code-first pipeline.

## Inputs

- Mode: {mode_line}
- Production mode: {args.production_mode}
- Gate 1 source: {args.gate1_source}
- Style family: {style_notes["label"]} (`{args.style_family}`)
- Reference: {reference_line}
- Engine: {args.engine}
- Video model: {args.video_model}
- Whole-video duration: {args.duration:.2f}s at {args.fps} fps
- Whole-video duration source: {args.duration_source}
- Per-scene duration policy: {args.scene_duration_policy}
- Delivery: {args.aspect_ratio} / {resolved_orientation} / {args.audio_mode}
- Background policy: {args.background_policy}; sharing authorized: {args.background_sharing_authorized}
- Image stack: {args.image_model}
- Default image generation path: `imagegen` skill
- Audio stack: {args.audio_model}
- Scene complexity: {args.scene_complexity}
- Recommended route: {route}
- Kit status: {kit_line}

## Non-negotiable style rules

- Bake the chosen style family directly into the image prompts instead of relying on post styling.
- Material rules: {", ".join(style_notes["materials"])}
- Motion rules: {", ".join(style_notes["motion"])}
- Editorial rules: {", ".join(style_notes["editorial"])}
- Lock the storyboard before generating a full asset pack.
- In `remotion-code` mode, keep visible charts, pages, maps, bubbles, and other primary art asset-based. Remotion should animate those assets rather than draw the art from scratch in SVG.
- A PNG extension is not provenance. Call the built-in `image_gen` tool for each distinct new asset and preserve its prompt, original result, receipt, and hashes.
- If image generation fails or is unavailable, stop at the Asset gate. Do not create Pillow, Canvas, OpenCV, SVG, CSS, or other procedural asset generators.
- In `remotion-code` mode, always decompose the scene into separate asset slots before generating any art. Do not validate style by making one flattened scene image first.
- Background rule: generate one quiet scene-specific background plate per scene. Share texture and palette, not the same file, unless shared-continuity was explicitly authorized.
- Color rule: follow `0720-bright-paper-style.md`; use a chromatic dominant field, at least two chromatic supports, one focal accent, a dark anchor, and controlled paper neutrals. Quiet means low detail, not low saturation.
- Every Remotion scene needs 4-8 approved raster assets and at least 3 independently timed non-background assets.
- Generate separate PNGs for every element that needs separate motion; never use one cross-scene hero sheet or one composite hero to hide missing layers.
- Record each element's frame occupancy, anchor, appearance order, entrance window, settle, hold, and exit according to `vox-motion-contract.md`.
- Make element entrances follow the content order. Accents and annotations enter only after their target is visible.
- Keep background layers smooth and reserve stepped motion for characters or hero inserts.
- Use front/back layer splitting when a subject must feel inside a prop.
- Keep audio restrained and functional.
- For complex scenes, generate the first-frame empty plate once, then create the last-frame final tableau only by editing that exact first frame with built-in `image_gen` and `referenced_image_paths`.
{"- Let the narration drive the beat and scene timing." if args.mode == "vo-sequence" else ""}
{"- Keep one locked palette, paper texture, and accent language across the sequence while changing the background environment per scene." if args.mode == "vo-sequence" else ""}

## Route plan

- Simple scenes: `remotion-cutout`
- Complex scenes: `seedance-first-last`
- Complex-scene frame count: {max(2, keyframe_count_for_strategy(args))}
- Input transport: local files encoded to base64 at submit time
- Video model route: first-frame empty scene -> last-frame final hold

## Canonical beat skeleton

{beat_lines}

{"## Scene grouping" if scenes else ""}

{sequence_lines}

## Approval gates

- Gate 0 before everything else: environment and capability self-check
- Gate 1 before planning: user-choice lock
- Storyboard gate before full asset generation
- Asset gate before animation implementation
- Motion gate before sound generation
- Audio gate before final render
"""


def storyboard_md(beats: list[dict]) -> str:
    return f"""# Storyboard

Fill one row per beat before building the animation.

| Beat | Timing | Visual metaphor | Composition | Scene-specific background | Narrative appearance order | Hero occupancy | Motion rhythm | Route hint | Approval notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{render_beat_rows(beats)}

Lock the visual metaphor and composition before naming assets. The narrative appearance order must follow the source content. Do not approve a panel until every listed moving element maps to its own raster asset and motion specification.
"""


def narration_timeline_md(beats: list[dict]) -> str:
    rows = []
    for beat in beats:
        rows.append(
            "| {slug} | {start:.2f}s-{end:.2f}s | {narration} | [fill trigger word] |".format(
                slug=beat["slug"],
                start=beat["start_seconds"],
                end=beat["end_seconds"],
                narration=beat.get("narration", "[fill narration]"),
            )
        )
    return """# Narration Timeline

Use the voiceover as the master timing source.

| Beat | Timing | Narration line | Visual trigger |
| --- | --- | --- | --- |
{rows}
""".format(rows="\n".join(rows))


def asset_manifest_md() -> str:
    return """# Asset Manifest

Track every visible layer needed to build the approved scene system.

Important rules:

- For `remotion` scenes, do not treat one flattened `scene-xx.png` as the primary deliverable.
- Break every scene into separate assets that can be animated independently.
- Only `seedance` scenes should use full-frame `first-frame` and `last-frame` stills as the main package.
- Lock the Scene's visual metaphor, layout archetype, reading path, and motion rhythm before naming assets.
- Lock `background_contract` and `collision_plan`: reserve every final asset box and motion corridor, keep unrelated assets under the default overlap limit, and document intentional overlap pairs.
- Generate in order: scene-specific `background` -> dominant metaphor subject -> at least two content-specific moving assets -> optional foreground/editorial/accent layers.
- Stop after the background. Inspect it alone and approve reserved zones, duplicate-subject absence, and focal competition before generating moving assets.
- Background plates must stay quiet: fixed environment only, no decorative sticker clutter, no extra characters, no surprise props, no arrows/circles/stamps unless those are separate approved accent assets.
- Do not reuse a background file across scenes unless shared-continuity was explicitly authorized.
- Require 4-8 approved raster assets and at least 3 independently timed moving assets per Remotion scene.
- Record `appearance_order` and `appearance_reason` from content order before generating or animating assets.
- Record frame width/height percentage, anchor, entrance interval, travel, settle, hold, and exit for every moving asset.
- For every generated asset, preserve its prompt, unmodified imagegen original, tool result receipt, and prompt/original/final hashes.
- Do not create a project-local raster drawing script; PNG output from Pillow or Canvas is still forbidden generated art.

Content-driven slot pattern per Remotion scene:

| Asset | Role | Required | Narrative order | Frame occupancy | Motion | Status |
| --- | --- | --- | ---: | --- | --- | --- |
| scene-xx/background | unique fixed back plate | yes | 0 | 100% x 100% | cut/fade + subtle drift | todo |
| scene-xx/hero-cutout | primary subject | yes | 1 | [width/height/anchor %] | [entrance/settle/hold/exit] | todo |
| scene-xx/[content-specific-id-1] | first causal, contrast, path, or consequence element | yes | 2 | [width/height/anchor %] | [entrance/action/hold] | todo |
| scene-xx/[content-specific-id-2] | second element needed to complete the metaphor | yes | 3 | [width/height/anchor %] | [entrance/action/hold] | todo |
| scene-xx/[optional-foreground-id] | corner, side, lower, or depth anchor only when content requires it | optional | 4 | [width/height/anchor %] | [entrance/action/hold] | todo |
"""


def motion_plan_md(args: argparse.Namespace) -> str:
    if args.production_mode == "video-model":
        return f"""# Motion Plan

## Production route

- Locked route: seedance-first-last
- Video model: {args.video_model}
- Aspect ratio: {args.aspect_ratio}
- Scene duration policy: auto-by-content

## Per-Scene contract

- Generate `first-frame` once as the empty or near-empty fixed background plate.
- Inspect it with `view_image`, then create `last-frame` only through built-in `image_gen` edit mode using that exact first-frame path.
- Preserve all background pixels outside declared change regions.
- Fill `keyframe_generation_contract`, `motion_contract`, and one content-specific `motion_intent`.
- Pass the first-frame canvas and first/last-frame continuity gates before submission.
- Keep both local PNG files; the submit script encodes them to base64.
"""
    return f"""# Motion Plan

## Production route

- Selected strategy: {args.animation_strategy}
- Recommended route: {recommend_scene_route(args)}
- Engine lock: Remotion only; decompose complex Scenes into more raster layers instead of switching engines

## Layer stack

- Unique scene background plate
- Hero metaphor subject
- At least two content-specific moving assets derived from the metaphor mapping
- Optional environment, editorial, path, foreground, and annotation assets

## Vox composition contract

- Aspect ratio: {args.aspect_ratio}
- Horizontal single hero: 32-48% frame width and 45-72% frame height
- Vertical single hero: 58-82% frame width and 32-56% frame height
- Support cutout: no more than 65% of hero width in the normal hierarchy
- Foreground elements are optional and content-driven; a lower band is never a default slot
- Every scene: 4-8 approved raster assets, including one unique background
- Every scene: at least 3 independently timed moving assets, excluding background
- Every moving asset: width/height/anchor percentages plus appearance reason, entrance, settle, hold, and exit
- Every moving asset: one protected background zone; every pair: overlap calculation at final action state
- Background: stage-only, low saliency, no duplicate of any moving subject class inside its landing zone
- Entrance order: exact `narrative_sequence` order derived from the content
- Composition: lock `visual_metaphor`, `layout_archetype`, `reading_path`, `dominant_axis`, `foreground_strategy`, and `motion_rhythm` before generating assets
- Diversity: adjacent Scenes cannot repeat a layout archetype; a 4+ Scene sequence needs at least 3 layouts and 3 motion rhythms

## Vox timing contract

- Select one content-driven `motion_rhythm`; do not reuse a universal 8/26/48% entrance template
- `sequential-build`: stagger assets through the content order
- `cause-then-effect`: finish the causal action before revealing the consequence
- `counter-motion`: establish opposing zones, then move toward or away from the seam
- `radial-convergence`: place perimeter elements before convergence/orbit
- `path-follow`: draw the route before subjects travel on it
- `scale-shift`: establish the focal subject before its size change
- `replacement`: keep the old state readable before displacement
- `cascade`: use tight serial steps along the chosen axis
- `draw-and-land`: stable frame -> drawn line/path -> final marker
- Complete meaningful motion by 65-75%, then preserve a readable final hold
- At 30 fps, stagger separate entrances by 4-10 frames unless simultaneous counter-motion is the stated rhythm
- Use one dominant metaphor payoff per beat; do not animate every layer with equal strength

## Motion recipes

| Element | Motion type | Controls | Notes |
| --- | --- | --- | --- |
| background | cut/fade + subtle drift | startPct, endPct, scale 1.00-1.02 | unique per scene; no bounce |
| hero | spring-rise or decisive slide | widthPct, heightPct, anchor, startPct, endPct, travel 8-14% | 12-20 frame entrance, one small settle |
| support | slide/pop | widthPct, anchor, startPct, endPct, travel 5-10% | 8-16 frames, stagger in content order |
| editorial surface | wipe/unfold/page-place | startPct, endPct, mask progress | 12-24 frames, usually locked on hold |
| marker/accent | draw-on/sweep/circle | targetAsset, startPct, endPct | enters after target, 8-16 frames |
| optional foreground | corner/side/lower/depth entrance chosen by metaphor | size, anchor, startPct, endPct | never add a lower strip only to fill space |

## Prop control checklist

- position x/y
- scale
- rotation
- entry frame
- exit frame
- drift amplitude
- step hold length
- shadow or offset styling
- narrative token and appearance order
- frame width/height percentages and normalized anchor
- entrance direction, travel percentage, settle, hold, and exit

"""


def sound_plan_md() -> str:
    return """# Sound Plan

## Music

List 2-3 directions before generating any track.

| Direction | Mood | Instrument ideas | Why it fits | Selected |
| --- | --- | --- | --- | --- |
| option-a | [fill] | [fill] | [fill] | no |
| option-b | [fill] | [fill] | [fill] | no |
| option-c | [fill] | [fill] | [fill] | no |

## Foley and ambience

| Cue | Trigger beat | Start frame | End frame | Volume | Notes |
| --- | --- | --- | --- | --- | --- |
| reveal-foley | unfolding | [fill] | [fill] | [fill] | scroll, rustle, curtain, etc. |
| ambience-bed | living-scene | [fill] | [fill] | [fill] | water, room tone, wind, etc. |
| accent-cue | hero-arrival | [fill] | [fill] | [fill] | gull, bell, scribble, etc. |

## Audio gate

Listen once without watching.

- If a cue pulls focus, lower it or remove it.
- If the music already sells the beat, prefer silence over extra foley.
"""


def render_notes_md(args: argparse.Namespace) -> str:
    route_check = (
        "- Every Seedance frame path resolves locally and matches the chosen aspect ratio"
        if args.production_mode == "video-model"
        else "- Rough render passes blueprint, asset, TypeScript, semantic layout sampling, and media metadata gates before finalization"
    )
    return f"""# Render Notes

## Final checks

- Silhouette reads at a glance
- Extract one frame immediately after assembly and one frame during final hold for every Scene
- Review the extracted frames as a contact sheet at thumbnail size before final render
- Dominant metaphor is identifiable without relying on narration
- Largest meaningful subject reads as the focal point rather than a small decoration in empty space
- Negative space has a stated entrance or readability purpose
- Adjacent Scenes do not repeat layout archetype, anchor pattern, final silhouette, or motion rhythm
- Depth order is correct
- Stepped motion affects only intended elements
- Front/back sandwich seam is invisible
- Audio mix stays below the music bed unless the cue is the point
- Runtime and fps match the brief
- Delivery matches {args.aspect_ratio} / {infer_orientation(args.aspect_ratio, args.orientation)}
{route_check}

## Deliverables

- final mp4
- poster frame
- prompt pack
- project config snapshot
"""


def self_check_md(args: argparse.Namespace, report: dict) -> str:
    rows = "\n".join(
        "| {id} | {status} | {detail} | {fix} |".format(
            id=check["id"],
            status=check["status"],
            detail=check["detail"],
            fix=check["fix"],
        )
        for check in report["checks"]
    )
    return """# Gate 0 Self Check

This is `Gate 0`.
Do not continue into user choice, planning, or generation until required checks pass.

| Check | Status | Detail | Next action |
| --- | --- | --- | --- |
{rows}
""".format(rows=rows)


def route_plan_md(args: argparse.Namespace, scene_slug: str) -> str:
    route = recommend_scene_route(args)
    keyframe_count = max(2, keyframe_count_for_strategy(args))
    if args.production_mode == "remotion-code":
        return f"""# Production Route

- Gate 1 mode: remotion-code
- Locked route: {route}
- Scene complexity input: {args.scene_complexity}

This project stays entirely in Remotion. Decompose complex content into more independent raster assets and semantic motion phases; do not silently escalate a Scene to Seedance, create keyframes, or install a second engine. If the user wants the video-model route, return to Gate 1 and create a separate video-model project.
"""
    return f"""# Scene Routing

## Default decision

- Selected strategy: {args.animation_strategy}
- Recommended route: {route}
- Scene complexity input: {args.scene_complexity}

## When to stay in Remotion

- A scene uses a small number of cutouts.
- Motion can be expressed as parallax, stepped holds, reveals, labels, counters, or alpha plates.
- The user wants granular layer control or editable timing in code.

## When to escalate to Seedance

- A single scene contains many interacting elements.
- Several elements need independent, intricate motion at the same time.
- The collage should behave like one integrated animated tableau instead of separable cutout rigs.
- The scene can be expressed as a clear before/after transformation from empty plate to final hold.
- The shot should stay within Seedance 1.5 Pro's 4-12 second range, or be split further.

## Seedance package

- Frame count: {keyframe_count}
- Image source: collage stills generated via the `imagegen` skill, with the full paper treatment baked in
- Input transport: local PNG files encoded as base64 by the submit script
- Example local frame paths:
  `02_assets/keyframes/{scene_slug}/first-frame.png`
  `02_assets/keyframes/{scene_slug}/last-frame.png`
- Motion intent to write before submit: assembly order, what stays anchored, whether the camera is effectively locked, and how the final hold should breathe
"""


def seedance_runbook_md(args: argparse.Namespace, mode: str) -> str:
    canvas = canvas_contract(args.aspect_ratio)
    scene_locator = (
        "--scene-spec ./03_animation/SEEDANCE_SCENE.json"
        if mode == "single-scene"
        else "--scene-slug <scene-slug>"
    )
    return f"""# Seedance Runbook

Use this only for scenes that route to `seedance-first-last`.

## Steps

1. Fill the relevant `SEEDANCE_SCENE.json` file with:
   - `prompt`
   - `motion_intent`
   - structured `motion_contract`: fixed objects, entering objects, draw-on paths, serial timeline, and forbidden events
   - local first-frame and last-frame image paths
2. Use the `imagegen` skill in two different modes:
   - generate `first-frame.png` once as the empty or near-empty background plate using Gate 1 canvas `{canvas["aspect_ratio"]}` / `{canvas["width"]}x{canvas["height"]}` / `{canvas["orientation"]}`
   - immediately run `python3 tools/validate_seedance_first_frame.py --project . --scene-spec [scene spec path]`; do not create the last frame until it passes
   - inspect that local image with `view_image`, then call built-in `image_gen` in edit mode with the exact first-frame path in `referenced_image_paths`; add only the approved foreground elements and save the result as `last-frame.png`
   - never create `last-frame.png` with an independent text-to-image generation call
3. Fill `keyframe_generation_contract`, including first-frame SHA-256, edit receipt, exact edit target path, change regions, and continuity review.
4. Run `python3 ~/.codex/skills/paper-collage-video/scripts/validate_seedance_keyframes.py --project [project-root] {scene_locator}` and stop if it fails.
5. Run the one-command scene pipeline:

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/run_seedance_scene.py \\
  --project [project-root] \\
  {scene_locator}
```

## What the command does

- reads the two local stills
- encodes them as base64 data URIs
- submits `doubao-seedance-1-5-pro-251215` in first-frame + last-frame mode
- polls until completion
- downloads the finished `.mp4` into `05_render/seedance/`
"""


def keyframes_readme_md(aspect_ratio: str) -> str:
    canvas = canvas_contract(aspect_ratio)
    return f"""# Seedance Frames

Generate the first Seedance still with the `imagegen` skill. Generate the last
still only by editing that exact first-frame image with built-in `image_gen` and
`referenced_image_paths`; independent last-frame text-to-image generation is
forbidden. Then place both images in scene-specific folders here.

Gate 1 canvas: `{canvas["aspect_ratio"]}` / `{canvas["width"]}x{canvas["height"]}` / `{canvas["orientation"]}`.
Validate the first frame before the last-frame call. Never crop either frame after the edit.

Recommended naming:

- `first-frame.png`
- `last-frame.png`
"""


def seedance_scene_spec(
    args: argparse.Namespace,
    scene_slug: str,
    scene_title: str,
    duration_seconds: float,
    frame_rate: int,
    *,
    scene_index: int | None = None,
) -> dict:
    duration_seconds = round(duration_seconds, 2)
    expected_canvas = canvas_contract(args.aspect_ratio)
    if args.production_mode == "video-model" and duration_seconds > 12:
        raise ValueError(
            f"Scene `{scene_slug}` spans {duration_seconds:.2f}s. Split it into semantic scenes before Seedance submission; do not clamp it to 12s."
        )
    effective_duration_policy = (
        "auto-by-content"
        if args.scene_duration_policy == "not-applicable"
        else args.scene_duration_policy
    )
    request_duration = max(4, min(12, int(round(duration_seconds))))
    duration_reason = "Rounded from this Scene's semantic content window and motion budget under the mandatory auto-by-content policy."
    keyframe_dir = f"02_assets/keyframes/{scene_slug}"
    prompt_scene_dir = f"scene-{scene_index:02d}" if scene_index is not None else "scene-01"
    return {
        "scene_slug": scene_slug,
        "scene_index": scene_index,
        "scene_title": scene_title,
        "route": "seedance-first-last",
        "video_model": args.video_model,
        "prompt": "[fill approved scene prompt]",
        "motion_intent": "[fill one paragraph describing assembly order, anchored elements, locked-camera feel, and final hold micro-motion]",
        "motion_contract": {
            "frame_state_audit_locked": False,
            "prompt_contract_consistency_locked": False,
            "fixed_objects": [
                {
                    "id": "[fill stable object id]",
                    "description": "[describe an object already present in first and last frames]",
                    "prompt_aliases": ["[exact nouns used for this object in prompt and motion_intent]"],
                    "rule": "pixel-locked",
                }
            ],
            "entering_objects": [
                {
                    "id": "[fill entering object or grouped sequence id]",
                    "description": "[describe exact rigid objects and count]",
                    "motion_primitive": "[slide-in, rise, stamp-in, page-place, pin-drop, serial-placement, direct-placement, unfold, wipe-reveal, or tape-press]",
                    "final_region": "[describe final frame region]",
                }
            ],
            "draw_on_paths": [],
            "timeline": [
                {
                    "start_pct": 0,
                    "end_pct": 70,
                    "behavior": "[fill one serial action group]",
                    "object_ids": ["[reference a declared object id]"],
                    "instruction": "[one concrete motion instruction]",
                },
                {
                    "start_pct": 70,
                    "end_pct": 100,
                    "behavior": "hold",
                    "object_ids": ["[reference final anchored object ids]"],
                    "instruction": "hold the completed poster with micro-motion only",
                },
            ],
            "forbidden_events": [
                "object replacement",
                "object morphing",
                "duplicate surfaces",
                "cross-zone travel",
            ],
        },
        "keyframe_generation_contract": {
            "canvas": {
                **expected_canvas,
                "validate_before_last_frame": True,
                "post_edit_crop_forbidden": True,
            },
            "max_outside_region_mae": 0.06,
            "max_outside_significant_change_pct": 12,
            "first_frame": {
                "source": "imagegen",
                "mode": "generate",
                "execution_method": "built-in-image_gen-generate",
                "tool_called": False,
                "prompt_file": f"02_assets/prompts/{prompt_scene_dir}/first-frame.md",
                "result_receipt": "",
                "output_sha256": "",
            },
            "last_frame": {
                "source": "imagegen",
                "mode": "edit",
                "execution_method": "built-in-image_gen-edit",
                "tool_called": False,
                "prompt_file": f"02_assets/prompts/{prompt_scene_dir}/last-frame.md",
                "result_receipt": "",
                "output_sha256": "",
                "edit_target_role": "first_frame",
                "edit_target_path": f"{keyframe_dir}/first-frame.png",
                "edit_target_sha256": "",
                "referenced_image_paths": [f"{keyframe_dir}/first-frame.png"],
                "preserve_outside_change_regions": True,
                "change_regions": [
                    {
                        "id": "[fill approved addition zone]",
                        "x_pct": None,
                        "y_pct": None,
                        "width_pct": None,
                        "height_pct": None,
                        "purpose": "[name the entering objects allowed in this zone]",
                    }
                ],
            },
            "continuity_review": {
                "same_canvas_and_crop": False,
                "background_geometry_match": False,
                "fixed_objects_match": False,
                "no_background_regeneration": False,
            },
        },
        "resolution": {
            "aspect_ratio": args.aspect_ratio,
            "width": expected_canvas["width"],
            "height": expected_canvas["height"],
            "resolution_tier": "720p",
        },
        "timing": {
            "content_window_seconds": duration_seconds,
            "duration_seconds": duration_seconds,
            "request_duration_seconds": request_duration,
            "scene_duration_policy": effective_duration_policy,
            "duration_reason": duration_reason,
            "frame_rate": frame_rate,
        },
        "seedance": {
            "generate_audio": False,
            "return_last_frame": False,
            "watermark": False,
            "input_mode": "first-last-frame",
            "base64_transport": True,
        },
        "frames": [
            {
                "id": "first-frame",
                "role": "first_frame",
                "label": "empty or near-empty establishing plate",
                "path": f"{keyframe_dir}/first-frame.png",
            },
            {
                "id": "last-frame",
                "role": "last_frame",
                "label": "final assembled tableau hold",
                "path": f"{keyframe_dir}/last-frame.png",
            },
        ],
        "output": {
            "video_path": f"05_render/seedance/{scene_slug}.mp4",
            "metadata_path": f"05_render/seedance/{scene_slug}.json",
        },
    }


def scene_plan_md(scenes: list[dict], fps: int) -> str:
    rows = []
    for scene_meta in scenes:
        frames = round(scene_meta["duration_seconds"] * fps)
        rows.append(
            "| {slug} | {beats} | {start:.2f}s-{end:.2f}s | {frames} | [claim -> physical metaphor -> motion payoff] | [layout] | [reading path] | [motion rhythm] | [unique background concept] | [remotion / seedance] | [hero visible size %] | [ordered asset ids] |".format(
                slug=scene_meta["slug"],
                beats=", ".join(scene_meta["beat_slugs"]),
                start=scene_meta["start_seconds"],
                end=scene_meta["end_seconds"],
                frames=frames,
            )
        )
    return """# Scene Plan

Map narration beats into reusable scene modules before coding.

| Scene | Beats | Window | Frames | Visual metaphor | Layout archetype | Reading path | Motion rhythm | Background concept | Route | Hero occupancy | Narrative sequence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{rows}

Each Scene must translate its claim into a concrete moving metaphor before assets are named. Adjacent Scenes must use different layout archetypes, and a 4+ Scene sequence needs at least 3 layouts and 3 motion rhythms. Each background concept must differ unless shared-continuity was explicitly authorized. List moving asset IDs in exact content order.
""".format(rows="\n".join(rows))


def scene_brief_md(scene_meta: dict, fps: int, style_family: str) -> str:
    style_notes = style_family_notes(style_family)
    beat_lines = "\n".join(
        f"- `{beat['slug']}` · {beat['start_seconds']:.2f}s-{beat['end_seconds']:.2f}s · {beat.get('narration', '[fill narration]')}"
        for beat in scene_meta["beats"]
    )
    return f"""# {scene_meta['slug']}

## Timing

- Window: {scene_meta['start_seconds']:.2f}s-{scene_meta['end_seconds']:.2f}s
- Duration: {scene_meta['duration_seconds']:.2f}s
- Frames at target fps: {round(scene_meta['duration_seconds'] * fps)}

## Beats carried

{beat_lines}

## Build notes

- Style family: {style_notes["label"]} (`{style_family}`)
- Module type: [content treatment from scene-archetypes.md]
- Visual metaphor: [abstract claim -> concrete physical mechanism -> exact mapping -> motion payoff]
- Layout archetype: [asymmetric-stage / diagonal-cascade / split-contrast / radial-cycle / depth-tunnel / stacked-consequence / map-route / full-frame-data]
- Reading path and dominant axis: [fill]
- Motion rhythm: [sequential-build / cause-then-effect / counter-motion / radial-convergence / path-follow / scale-shift / replacement / cascade / draw-and-land]
- Background contract: [allowed fixed stage elements / forbidden subject aliases / low-detail reserved zones / saliency budget]
- Collision plan: [final boxes / motion corridors / safe gap / allowed overlap pairs with reasons]
- Route: [remotion / seedance]
- Background contract: unique scene-specific environment using the shared paper texture and palette grammar
- Background concept: [fill environment and dominant shape field for this scene only]
- Hero subject and frame occupancy: [fill asset id, width %, height %, anchor x/y %]
- Support subjects: [fill at least one independently generated support asset]
- Foreground strategy: [none / corner-occluder / side-frame / lower-band / full-depth-prop / entering-subject]; lower-band is allowed only when the content needs it
- Optional additional narrative layer: [fill second support / editorial surface / accent]
- Visible asset rule: primary art should be generated or supplied image assets; Remotion handles motion and compositing rather than drawing the main scene art in SVG
- Word-synced reveal: [fill]
- Narrative sequence: [fill ordered asset IDs following the content]
- Per-element motion: [fill appearance order, entrance, direction, start/end %, travel %, settle, hold, exit for every moving asset]
- Background rule: [fill one sentence stating what is allowed in the background plate and what must stay out as separate assets]
- Seedance frame rule for complex scenes: first frame is the empty plate, last frame is the final hold tableau
- Style cues to preserve: {", ".join(style_notes["editorial"])}
- Asset needs:
  required `background.png` and `hero-cutout.png`; add at least two independently moving, content-specific metaphor/support assets; foreground is optional
- Minimum asset count: 4 approved raster assets total and 3 independently timed non-background assets
- Subject size and motion ranges: follow `references/vox-motion-contract.md`
- Tunable props: [fill]
"""


def package_json() -> str:
    return """{
  "name": "paper-collage-video-template",
  "private": true,
  "scripts": {
    "runtime": "python3 ../tools/ensure_remotion_runtime.py --project ..",
    "validate:blueprint": "python3 ../tools/validate_composition_blueprint.py --project ..",
    "validate:assets": "python3 ../tools/validate_collage_project.py --project ..",
    "validate": "npm run validate:blueprint && npm run validate:assets",
    "typecheck": "tsc --noEmit",
    "preflight": "npm run runtime && npm run validate && npm run typecheck",
    "studio": "npm run preflight && remotion studio src/index.ts --no-open",
    "render:raw": "npm run preflight && remotion render src/index.ts MainSequence out/rough.mp4",
    "audit": "python3 ../tools/extract_layout_audit.py --project ..",
    "verify": "python3 ../tools/verify_remotion_output.py --project .. --video 07_remotion/out/rough.mp4",
    "render": "npm run render:raw && npm run audit && npm run verify",
    "finalize": "python3 ../tools/finalize_remotion_render.py --project .. && python3 ../tools/verify_remotion_output.py --project .. --video 05_render/final.mp4"
  },
  "dependencies": {
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "remotion": "4.0.397"
  },
  "devDependencies": {
    "@remotion/cli": "4.0.397",
    "@types/react": "19.2.2",
    "@types/react-dom": "19.2.2",
    "typescript": "5.9.2"
  }
}
"""


def tsconfig_json() -> str:
    return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
"""


def remotion_config_ts() -> str:
    return """import {Config} from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setOverwriteOutput(true);
"""


def src_index_ts() -> str:
    return """import {registerRoot} from "remotion";
import {RemotionRoot} from "./Root";

registerRoot(RemotionRoot);
"""


def scene_background_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, staticFile} from "remotion";

export type SceneBackgroundProps = {
  backgroundAsset?: string;
};

export const SceneBackground: React.FC<SceneBackgroundProps> = ({
  backgroundAsset,
}) => {
  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      {backgroundAsset ? (
        <Img
          src={staticFile(backgroundAsset)}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      ) : null}
      <AbsoluteFill
        aria-hidden="true"
        style={{
          background:
            "linear-gradient(180deg, rgba(255,255,255,0.06), rgba(63,54,42,0.12)), radial-gradient(circle at 50% 60%, rgba(255,255,255,0.16), transparent 42%)",
          mixBlendMode: "soft-light",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
"""


def cutout_subject_tsx() -> str:
    return """import React from "react";
import {
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type CutoutSubjectProps = {
  src?: string;
  label: string;
  x: number;
  y: number;
  width: number;
  startFrame: number;
  endFrame: number;
  strokeColor?: string;
  strokeOpacity?: number;
  strokeX?: number;
  strokeY?: number;
  zIndex?: number;
};

export const CutoutSubject: React.FC<CutoutSubjectProps> = ({
  src,
  label,
  x,
  y,
  width,
  startFrame,
  endFrame,
  strokeColor = "#E04329",
  strokeOpacity = 0.92,
  strokeX = -22,
  strokeY = 8,
  zIndex = 12,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const durationInFrames = Math.max(1, endFrame - startFrame);
  const enter = spring({
    frame: frame - startFrame,
    fps,
    config: {damping: 18, stiffness: 110, mass: 0.8},
    durationInFrames,
  });
  const opacity = interpolate(frame, [startFrame, startFrame + 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rise = interpolate(enter, [0, 1], [220, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const box = {
    position: "absolute" as const,
    left: 960 + x,
    top: 540 + y,
    width,
    height: width * 1.12,
    transform: `translate(-50%, -50%) translateY(${rise}px)`,
    transformOrigin: "center bottom",
    opacity,
    zIndex,
  };

  if (!src) {
    return (
      <div
        style={{
          ...box,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "rgba(251,250,244,0.95)",
          border: "2px solid rgba(26,26,26,0.2)",
          color: "#1A1A1A",
          fontFamily: "Arial Black, Arial, sans-serif",
          fontSize: 28,
          lineHeight: 1.15,
          padding: 20,
          textAlign: "center",
          boxShadow: "0 26px 40px rgba(54,41,24,0.18)",
        }}
      >
        {label}
      </div>
    );
  }

  const assetUrl = staticFile(src);

  return (
    <>
      <div
        aria-hidden="true"
        style={{
          ...box,
          left: 960 + x + strokeX,
          top: 540 + y + strokeY,
          backgroundColor: strokeColor,
          opacity: opacity * strokeOpacity,
          maskImage: `url(${assetUrl})`,
          maskRepeat: "no-repeat",
          maskPosition: "center",
          maskSize: "100% 100%",
          WebkitMaskImage: `url(${assetUrl})`,
          WebkitMaskRepeat: "no-repeat",
          WebkitMaskPosition: "center",
          WebkitMaskSize: "100% 100%",
        }}
      />
      <Img
        src={assetUrl}
        alt={label}
        style={{
          ...box,
          objectFit: "contain",
          filter: "drop-shadow(0 24px 30px rgba(54,41,24,0.22))",
        }}
      />
    </>
  );
};
"""


def scene_shell_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";
import {SceneBackground} from "./SceneBackground";

export type SceneShellProps = {
  backgroundAsset?: string;
  title: string;
  subtitle?: string;
  accentColor?: string;
  foregroundLabel?: string;
};

export const SceneShell: React.FC<SceneShellProps> = ({
  backgroundAsset,
  title,
  subtitle,
  accentColor = "#E04329",
  foregroundLabel,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({
    frame,
    fps,
    config: {damping: 18, stiffness: 110, mass: 0.8},
    durationInFrames: 28,
  });
  const rise = interpolate(enter, [0, 1], [120, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <div
        style={{
          position: "absolute",
          left: 160,
          right: 160,
          top: 160 + rise,
          padding: "28px 34px",
          background: "rgba(251,250,244,0.92)",
          border: "1px solid rgba(26,26,26,0.12)",
          boxShadow: "0 28px 48px rgba(54,41,24,0.18)",
        }}
      >
        <div
          style={{
            width: 120,
            height: 10,
            background: accentColor,
            marginBottom: 18,
          }}
        />
        <div
          style={{
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 70,
            lineHeight: 1.02,
            color: "#1A1A1A",
          }}
        >
          {title}
        </div>
        {subtitle ? (
          <div
            style={{
              marginTop: 20,
              fontFamily: "Georgia, serif",
              fontSize: 32,
              lineHeight: 1.35,
              color: "rgba(26,26,26,0.74)",
            }}
          >
            {subtitle}
          </div>
        ) : null}
      </div>
      {foregroundLabel ? (
        <div
          style={{
            position: "absolute",
            left: 160,
            bottom: 140,
            padding: "14px 22px",
            background: accentColor,
            color: "#FFF4E5",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            letterSpacing: 0.4,
          }}
        >
          {foregroundLabel}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
"""


def cutout_rise_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, staticFile} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";
import {CutoutSubject, type CutoutSubjectProps} from "../templates/CutoutSubject";

export type CutoutRiseSceneProps = {
  backgroundAsset?: string;
  title: string;
  subtitle?: string;
  foregroundLabel?: string;
  foregroundAsset?: string;
  foregroundHeight?: number;
  subjects: CutoutSubjectProps[];
};

export const CutoutRiseScene: React.FC<CutoutRiseSceneProps> = ({
  backgroundAsset,
  title,
  subtitle,
  foregroundLabel,
  foregroundAsset,
  foregroundHeight = 280,
  subjects,
}) => {
  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 110,
          width: 1180,
          zIndex: 30,
        }}
      >
        <div
          style={{
            width: 120,
            height: 10,
            background: "#E04329",
            marginBottom: 18,
          }}
        />
        <div
          style={{
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 68,
            lineHeight: 1.03,
            color: "#1A1A1A",
          }}
        >
          {title}
        </div>
        {subtitle ? (
          <div
            style={{
              marginTop: 18,
              fontFamily: "Georgia, serif",
              fontSize: 30,
              lineHeight: 1.35,
              color: "rgba(26,26,26,0.76)",
            }}
          >
            {subtitle}
          </div>
        ) : null}
      </div>
      {subjects.map((subject, index) => (
        <CutoutSubject key={index} {...subject} zIndex={12 + index} />
      ))}
      {foregroundAsset ? (
        <Img
          src={staticFile(foregroundAsset)}
          style={{
            position: "absolute",
            left: 960,
            bottom: -40,
            width: 1700,
            height: foregroundHeight,
            objectFit: "contain",
            transform: "translateX(-50%)",
            zIndex: 34,
            filter: "drop-shadow(0 18px 24px rgba(54,41,24,0.18))",
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            height: foregroundHeight,
            background:
              "linear-gradient(180deg, rgba(204,195,172,0) 0%, rgba(204,195,172,0.88) 28%, rgba(188,176,149,0.96) 100%)",
            zIndex: 32,
          }}
        />
      )}
      {foregroundLabel ? (
        <div
          style={{
            position: "absolute",
            right: 110,
            bottom: 118,
            padding: "14px 22px",
            background: "#E04329",
            color: "#FFF4E5",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            zIndex: 36,
          }}
        >
          {foregroundLabel}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
"""


def editorial_page_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";

export type EditorialPageSceneProps = {
  backgroundAsset?: string;
  pageAsset?: string;
  pageAssetLabel?: string;
  noteLabel?: string;
};

export const EditorialPageScene: React.FC<EditorialPageSceneProps> = ({
  backgroundAsset,
  pageAsset,
  pageAssetLabel = "editorial page asset",
  noteLabel,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const place = spring({
    frame,
    fps,
    config: {damping: 18, mass: 0.9, stiffness: 95},
    durationInFrames: 32,
  });
  const rise = interpolate(place, [0, 1], [120, 0]);
  const scale = interpolate(place, [0, 1], [0.92, 1]);
  const rotate = interpolate(place, [0, 1], [-4, -1.4]);
  const noteOpacity = interpolate(frame, [34, 62], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center"}}>
        <div
          style={{
            position: "relative",
            width: 1220,
            height: 760,
            transform: `translateY(${rise}px) scale(${scale}) rotate(${rotate}deg)`,
            transformOrigin: "center center",
            background: "rgba(251,250,244,0.5)",
            border: "1px solid rgba(21,19,15,0.14)",
            boxShadow: "0 38px 58px rgba(54,41,24,0.26)",
            overflow: "hidden",
          }}
        >
          {pageAsset ? (
            <Img
              src={staticFile(pageAsset)}
              alt={pageAssetLabel}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
              }}
            />
          ) : (
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: "Arial Black, Arial, sans-serif",
                fontSize: 34,
                color: "rgba(21,19,15,0.54)",
                background: "rgba(251,250,244,0.82)",
                textAlign: "center",
                padding: 40,
              }}
            >
              Replace this with an Imagen-generated editorial page asset.
            </div>
          )}
          {noteLabel ? (
            <div
              style={{
                position: "absolute",
                left: 42,
                bottom: 42,
                opacity: noteOpacity,
                padding: "14px 22px",
                background: "#E04329",
                color: "#FFF4E5",
                fontFamily: "Arial Black, Arial, sans-serif",
                fontSize: 24,
                boxShadow: "0 14px 22px rgba(54,41,24,0.2)",
              }}
            >
              {noteLabel}
            </div>
          ) : null}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
"""


def alpha_plate_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";
import {CutoutSubject} from "../templates/CutoutSubject";

export type AlphaPlateSceneProps = {
  backgroundAsset?: string;
  title: string;
  alphaVideoAsset?: string;
  heroSrc?: string;
  heroLabel: string;
  heroX?: number;
  heroY?: number;
  metricCardAsset?: string;
  metricCardLabel?: string;
  foregroundBandAsset?: string;
  foregroundLabel?: string;
};

export const AlphaPlateScene: React.FC<AlphaPlateSceneProps> = ({
  backgroundAsset,
  title,
  alphaVideoAsset,
  heroSrc,
  heroLabel,
  heroX = 0,
  heroY = 40,
  metricCardAsset,
  metricCardLabel = "metric card asset",
  foregroundBandAsset,
  foregroundLabel,
}) => {
  const frame = useCurrentFrame();
  const metricOpacity = interpolate(frame, [24, 56], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 110,
          width: 900,
          fontFamily: "Arial Black, Arial, sans-serif",
          fontSize: 64,
          lineHeight: 1.02,
          color: "#1A1A1A",
          zIndex: 30,
        }}
      >
        {title}
      </div>
      {alphaVideoAsset ? (
        <OffthreadVideo
          src={staticFile(alphaVideoAsset)}
          muted
          transparent
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            width: "100%",
            height: 420,
            objectFit: "cover",
            zIndex: 8,
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            left: 90,
            right: 90,
            bottom: 60,
            height: 290,
            border: "2px dashed rgba(26,26,26,0.16)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 30,
            color: "rgba(26,26,26,0.56)",
            zIndex: 8,
            textAlign: "center",
            padding: 30,
          }}
        >
          Add approved alpha plate or midground video asset.
        </div>
      )}
      <CutoutSubject
        src={heroSrc}
        label={heroLabel}
        x={heroX}
        y={heroY}
        width={980}
        startFrame={14}
        endFrame={72}
        strokeX={-26}
        strokeY={8}
        zIndex={18}
      />
      {metricCardAsset ? (
        <Img
          src={staticFile(metricCardAsset)}
          alt={metricCardLabel}
          style={{
            position: "absolute",
            right: 110,
            bottom: 94,
            width: 360,
            height: 220,
            objectFit: "contain",
            opacity: metricOpacity,
            zIndex: 26,
            filter: "drop-shadow(0 24px 34px rgba(54,41,24,0.18))",
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            right: 110,
            bottom: 94,
            width: 360,
            height: 220,
            border: "2px dashed rgba(26,26,26,0.16)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            color: "rgba(26,26,26,0.56)",
            textAlign: "center",
            padding: 22,
            opacity: metricOpacity,
            zIndex: 26,
          }}
        >
          Add approved metric-card image asset.
        </div>
      )}
      {foregroundBandAsset ? (
        <Img
          src={staticFile(foregroundBandAsset)}
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            width: "100%",
            height: 300,
            objectFit: "cover",
            zIndex: 10,
          }}
        />
      ) : null}
      {foregroundLabel ? (
        <div
          style={{
            position: "absolute",
            left: 110,
            bottom: 114,
            padding: "14px 22px",
            background: "#E04329",
            color: "#FFF4E5",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            zIndex: 28,
          }}
        >
          {foregroundLabel}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
"""


def data_viz_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";

export type DataVizSceneProps = {
  backgroundAsset?: string;
  title: string;
  chartAsset?: string;
  chartAssetLabel?: string;
  footerLabel?: string;
  rightAsset?: string;
  rightAssetLabel?: string;
};

export const DataVizScene: React.FC<DataVizSceneProps> = ({
  backgroundAsset,
  title,
  chartAsset,
  chartAssetLabel = "chart asset",
  footerLabel,
  rightAsset,
  rightAssetLabel = "supporting visual",
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const chartEnter = spring({
    frame,
    fps,
    config: {damping: 18, stiffness: 110, mass: 0.82},
    durationInFrames: 34,
  });
  const chartScale = interpolate(chartEnter, [0, 1], [0.92, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rightEnter = spring({
    frame: frame - 56,
    fps,
    config: {damping: 20, stiffness: 120, mass: 0.82},
    durationInFrames: 34,
  });
  const rightScale = interpolate(rightEnter, [0, 1], [0.86, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rightOpacity = interpolate(frame, [56, 96], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 108,
          width: 1220,
          fontFamily: "Arial Black, Arial, sans-serif",
          fontSize: 62,
          lineHeight: 1.04,
          color: "#1A1A1A",
          zIndex: 30,
        }}
      >
        {title}
      </div>
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 300,
          width: 860,
          height: 460,
          background: "rgba(251,250,244,0.9)",
          border: "1px solid rgba(26,26,26,0.12)",
          boxShadow: "0 26px 40px rgba(54,41,24,0.18)",
          padding: 26,
          zIndex: 18,
          transform: `scale(${chartScale})`,
          transformOrigin: "center center",
          overflow: "hidden",
        }}
      >
        {chartAsset ? (
          <Img
            src={staticFile(chartAsset)}
            alt={chartAssetLabel}
            style={{width: "100%", height: "100%", objectFit: "contain"}}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "rgba(26,26,26,0.56)",
              fontFamily: "Arial Black, Arial, sans-serif",
              fontSize: 30,
              textAlign: "center",
              padding: 30,
            }}
          >
            Replace this with an Imagen-generated chart / map / data-viz asset.
          </div>
        )}
      </div>
      {rightAsset ? (
        <Img
          src={staticFile(rightAsset)}
          alt={rightAssetLabel}
          style={{
            position: "absolute",
            right: 120,
            top: 300,
            width: 620,
            height: 460,
            objectFit: "contain",
            opacity: rightOpacity,
            transform: `scale(${rightScale})`,
            transformOrigin: "center center",
            zIndex: 20,
            filter: "drop-shadow(0 22px 28px rgba(54,41,24,0.2))",
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            right: 120,
            top: 300,
            width: 620,
            height: 460,
            opacity: rightOpacity,
            transform: `scale(${rightScale})`,
            border: "2px dashed rgba(26,26,26,0.18)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "rgba(26,26,26,0.56)",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 30,
            textAlign: "center",
            padding: 30,
            zIndex: 20,
          }}
        >
          Add approved supporting image asset
        </div>
      )}
      {footerLabel ? (
        <div
          style={{
            position: "absolute",
            right: 120,
            bottom: 108,
            padding: "14px 22px",
            background: "#E04329",
            color: "#FFF4E5",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            zIndex: 28,
          }}
        >
          {footerLabel}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
"""


def speech_bubble_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";
import {CutoutSubject} from "../templates/CutoutSubject";

export type SpeechBubbleSceneProps = {
  backgroundAsset?: string;
  title: string;
  subjectSrc?: string;
  subjectLabel: string;
  foregroundSrc?: string;
  bubble1Asset?: string;
  bubble1Label?: string;
  bubble2Asset?: string;
  bubble2Label?: string;
  foregroundLabel?: string;
};

const BubbleAsset: React.FC<{
  src?: string;
  label: string;
  x: number;
  y: number;
  width: number;
  startFrame: number;
}> = ({src, label, x, y, width, startFrame}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({
    frame: frame - startFrame,
    fps,
    config: {damping: 18, stiffness: 120, mass: 0.82},
    durationInFrames: 24,
  });
  const scale = interpolate(enter, [0, 1], [0.6, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return src ? (
    <Img
      src={staticFile(src)}
      alt={label}
      style={{
        position: "absolute",
        left: 960 + x,
        top: 250 + y,
        width,
        objectFit: "contain",
        transform: `translate(-50%, -50%) scale(${scale}) rotate(-4deg)`,
        transformOrigin: "center center",
        opacity,
        zIndex: 26,
        filter: "drop-shadow(0 20px 28px rgba(54,41,24,0.18))",
      }}
    />
  ) : (
    <div
      style={{
        position: "absolute",
        left: 960 + x,
        top: 250 + y,
        width,
        minHeight: 160,
        transform: `translate(-50%, -50%) scale(${scale}) rotate(-4deg)`,
        transformOrigin: "center center",
        opacity,
        border: "2px dashed rgba(26,26,26,0.16)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "Arial Black, Arial, sans-serif",
        fontSize: 26,
        color: "rgba(26,26,26,0.56)",
        textAlign: "center",
        padding: 18,
        zIndex: 26,
        background: "rgba(251,250,244,0.72)",
      }}
    >
      Add approved speech-bubble image asset.
    </div>
  );
};

export const SpeechBubbleScene: React.FC<SpeechBubbleSceneProps> = ({
  backgroundAsset,
  title,
  subjectSrc,
  subjectLabel,
  foregroundSrc,
  bubble1Asset,
  bubble1Label = "speech bubble asset 1",
  bubble2Asset,
  bubble2Label = "speech bubble asset 2",
  foregroundLabel,
}) => {
  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 108,
          width: 1120,
          fontFamily: "Arial Black, Arial, sans-serif",
          fontSize: 62,
          lineHeight: 1.04,
          color: "#1A1A1A",
          zIndex: 30,
        }}
      >
        {title}
      </div>
      <CutoutSubject
        src={subjectSrc}
        label={subjectLabel}
        x={0}
        y={110}
        width={980}
        startFrame={16}
        endFrame={68}
        strokeX={-26}
        strokeY={8}
        zIndex={18}
      />
      <BubbleAsset src={bubble1Asset} label={bubble1Label} x={420} y={16} width={340} startFrame={58} />
      <BubbleAsset src={bubble2Asset} label={bubble2Label} x={640} y={118} width={340} startFrame={88} />
      {foregroundSrc ? (
        <Img
          src={staticFile(foregroundSrc)}
          style={{
            position: "absolute",
            left: 960,
            bottom: -40,
            width: 1700,
            height: 280,
            objectFit: "contain",
            transform: "translateX(-50%)",
            zIndex: 32,
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            height: 240,
            background:
              "linear-gradient(180deg, rgba(204,195,172,0) 0%, rgba(204,195,172,0.88) 28%, rgba(188,176,149,0.96) 100%)",
            zIndex: 30,
          }}
        />
      )}
      {foregroundLabel ? (
        <div
          style={{
            position: "absolute",
            left: 120,
            bottom: 106,
            padding: "14px 22px",
            background: "#E04329",
            color: "#FFF4E5",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 28,
            zIndex: 34,
          }}
        >
          {foregroundLabel}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
"""


def typewriter_punchline_scene_tsx() -> str:
    return """import React from "react";
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from "remotion";
import {SceneBackground} from "../templates/SceneBackground";

export type TypewriterPunchlineSceneProps = {
  backgroundAsset?: string;
  alphaVideoAsset?: string;
  alphaLabel?: string;
  textCardAsset?: string;
  textCardLabel?: string;
};

export const TypewriterPunchlineScene: React.FC<TypewriterPunchlineSceneProps> = ({
  backgroundAsset,
  alphaVideoAsset,
  alphaLabel = "symbolic plate",
  textCardAsset,
  textCardLabel = "punchline text card asset",
}) => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [10, 64], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{backgroundColor: "#78B8D8", overflow: "hidden"}}>
      <SceneBackground backgroundAsset={backgroundAsset} />
      {alphaVideoAsset ? (
        <OffthreadVideo
          src={staticFile(alphaVideoAsset)}
          muted
          transparent
          style={{
            position: "absolute",
            left: 960,
            top: 760,
            width: 960,
            height: 540,
            transform: "translate(-50%, -50%)",
            zIndex: 8,
          }}
        />
      ) : (
        <div
          style={{
            position: "absolute",
            left: 960,
            top: 770,
            width: 900,
            height: 260,
            transform: "translate(-50%, -50%)",
            border: "2px dashed rgba(26,26,26,0.16)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: "Arial Black, Arial, sans-serif",
            fontSize: 30,
            color: "rgba(26,26,26,0.56)",
            zIndex: 8,
          }}
        >
          {alphaLabel}
        </div>
      )}
      <div
        style={{
          position: "absolute",
          left: 160,
          right: 160,
          top: 180,
          height: 250,
          zIndex: 20,
          overflow: "hidden",
        }}
      >
        {textCardAsset ? (
          <Img
            src={staticFile(textCardAsset)}
            alt={textCardLabel}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
              clipPath: `inset(0 ${100 - reveal * 100}% 0 0)`,
            }}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              border: "2px dashed rgba(26,26,26,0.16)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: "Arial Black, Arial, sans-serif",
              fontSize: 30,
              color: "rgba(26,26,26,0.56)",
              textAlign: "center",
              padding: 24,
            }}
          >
            Add approved punchline text-card image asset.
          </div>
        )}
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 50%, transparent 46%, rgba(20,14,8,1) 100%)",
          opacity: Math.max(0, (frame - 170) / 44) * 0.32,
          pointerEvents: "none",
          zIndex: 32,
        }}
      />
    </AbsoluteFill>
  );
};
"""


def root_single_scene_tsx(duration: int, fps: int, aspect_ratio: str) -> str:
    canvas = REMOTION_CANVASES[aspect_ratio]
    return f"""import React from "react";
import {{Composition}} from "remotion";
import {{MainSequence}} from "./Sequence";

export const RemotionRoot: React.FC = () => {{
  return (
    <Composition
      id="MainSequence"
      component={{MainSequence}}
      durationInFrames={{{duration}}}
      fps={{{fps}}}
      width={{{canvas["width"]}}}
      height={{{canvas["height"]}}}
      defaultProps={{{{}}}}
    />
  );
}};
"""


def single_scene_sequence_tsx(
    duration: int,
    style_family: str,
    audio_public_name: str = "",
) -> str:
    audio_imports = ", Audio, staticFile" if audio_public_name else ""
    audio_layer = (
        f'<Audio src={{staticFile("audio/{audio_public_name}")}} />'
        if audio_public_name
        else ""
    )
    if style_family == "vox-mixed-media":
        return f"""import React from "react";
import {{AbsoluteFill{audio_imports}}} from "remotion";
import manifest from "../../02_assets/scenes/scene-01/ASSETS.json";
import {{VoxManifestScene}} from "./templates/VoxManifestScene";
import type {{SceneManifest}} from "./templates/VoxManifestScene";

export const MAIN_SEQUENCE_DURATION = {duration};

export const MainSequence: React.FC = () => (
  <AbsoluteFill>
    <VoxManifestScene
      manifest={{manifest as unknown as SceneManifest}}
      durationInFrames={{{duration}}}
    />
    {audio_layer}
  </AbsoluteFill>
);
"""
    return f"""import React from "react";
import {{AbsoluteFill}} from "remotion";
import {{SceneShell}} from "./templates/SceneShell";

export const MAIN_SEQUENCE_DURATION = {duration};

export const MainSequence: React.FC = () => {{
  return (
    <AbsoluteFill>
      <SceneShell
        backgroundAsset="background.png"
        title="Replace With Approved Scene"
        subtitle="Swap this shell for the real collage build once the storyboard and asset pack are approved."
        foregroundLabel="single-scene template"
      />
    </AbsoluteFill>
  );
}};
"""


def ts_literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def scene_narration(scene_meta: dict) -> str:
    return " ".join(beat.get("narration", "") for beat in scene_meta.get("beats", [])).strip()


def infer_scene_archetype(scene_meta: dict, index: int, total: int) -> str:
    text = scene_narration(scene_meta).lower()
    if index == total or any(word in text for word in ["bill", "empire", "they end", "can no longer pay"]):
        return "typewriter"
    if any(word in text for word in ["trade", "yuan", "dollar behind", "deal!"]):
        return "speech"
    if any(word in text for word in ["downfall", "begun", "op-ed", "newspaper", "collapse"]):
        return "editorial"
    if any(word in text for word in ["oil", "barrel", "strait", "hormuz", "hostage", "skyrocketed"]):
        return "alpha"
    if any(word in text for word in ["inflation", "trillion", "economy", "debt", "high"]):
        return "dataviz"
    return "cutout"


def safe_scene_title(scene_meta: dict) -> str:
    text = scene_narration(scene_meta)
    if not text:
        return f"Scene {scene_meta.get('scene_index', 0):02d}"
    return text[:58]


def lower_label(scene_meta: dict) -> str:
    text = scene_narration(scene_meta)
    return (text[:40] or "editorial scene").lower()


def vox_manifest_scene_tsx() -> str:
    return """import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Occupancy = {
  width_pct: number;
  height_pct: number;
  anchor_x_pct: number;
  anchor_y_pct: number;
  sizing_mode: "height-driven" | "width-driven" | "box-contain";
};

type Motion = {
  entrance: string;
  direction: string;
  start_pct: number;
  end_pct: number;
  travel_pct: number;
  settle: string;
  hold: string;
  exit: string;
};

type AssetEntry = {
  path: string;
  approved: boolean;
  z_index: number;
  narrative_token: string;
  appearance_reason: string;
  appearance_order: number;
  content_kind: "background" | "portrait-subject" | "wide-group" | "object-prop" | "editorial-card" | "foreground-strip" | "accent-mark";
  frame_occupancy: Occupancy;
  motion: Motion;
  action_motion: {
    type: string;
    start_pct: number;
    end_pct: number;
    translate_x_pct: number;
    translate_y_pct: number;
    scale_to: number;
    rotate_deg: number;
    easing: "linear" | "ease-in" | "ease-out" | "ease-in-out" | "spring";
    path_points_pct?: Array<{x_pct: number; y_pct: number}>;
    reveal_direction?: "left-to-right" | "right-to-left" | "top-to-bottom" | "bottom-to-top";
    pulse_scale?: number;
  };
};

export type SceneManifest = {
  visual_metaphor: {
    abstract_claim: string;
    concrete_metaphor: string;
    mapping: string;
    motion_payoff: string;
    asset_ids: string[];
  };
  composition: {
    layout_archetype: string;
    reading_path: string;
    dominant_axis: string;
    foreground_strategy: string;
    negative_space_intent: string;
  };
  motion_rhythm: string;
  narrative_sequence: string[];
  dominant_motion_asset: string;
  final_hold_start_pct: number;
  assets: Record<string, AssetEntry>;
};

type Props = {
  manifest: SceneManifest;
  durationInFrames: number;
};

const toPublicPath = (path: string) => path.replace(/^07_remotion\\/public\\//, "");

const zIndexFor = (slot: string) => {
  if (slot === "background_plate") return 0;
  if (slot.startsWith("environment_band")) return 6;
  if (slot.startsWith("editorial_surface")) return 12;
  if (slot.startsWith("support_cutout")) return 18;
  if (slot === "hero_cutout") return 22;
  if (slot.startsWith("accent_mark")) return 32;
  if (slot === "foreground_anchor") return 40;
  return 16;
};

const AnimatedAsset: React.FC<{
  slot: string;
  asset: AssetEntry;
  durationInFrames: number;
  dominant: boolean;
  readingPath: string;
  motionRhythm: string;
  finalHoldStartPct: number;
}> = ({slot, asset, durationInFrames, dominant, readingPath, motionRhythm, finalHoldStartPct}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const startFrame = Math.round((asset.motion.start_pct / 100) * durationInFrames);
  const endFrame = Math.round((asset.motion.end_pct / 100) * durationInFrames);
  const entranceFrames = Math.max(1, endFrame - startFrame);
  const linearProgress = interpolate(frame, [startFrame, endFrame], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const springProgress = spring({
    frame: Math.max(0, frame - startFrame),
    fps,
    durationInFrames: entranceFrames,
    config: asset.motion.settle === "small-overshoot"
      ? {damping: 15, stiffness: 125, mass: 0.8}
      : dominant
        ? {damping: 19, stiffness: 135, mass: 0.75}
        : {damping: 22, stiffness: 150, mass: 0.68},
  });
  const progress = /spring|pop|rise/.test(asset.motion.entrance)
    ? springProgress
    : linearProgress;
  const rhythmProgress = motionRhythm === "cascade" ? Math.floor(progress * 8) / 8 : progress;
  const travel = asset.motion.travel_pct;
  const requestedDirection = asset.motion.direction;
  const inferredDirection = /right-to-left/.test(readingPath)
    ? "right"
    : /top-to-bottom/.test(readingPath)
      ? "top"
      : /bottom-to-top/.test(readingPath)
        ? "bottom"
        : "left";
  const direction = requestedDirection === "target-dependent" ? inferredDirection : requestedDirection;
  const sideDirection = direction === "side"
    ? asset.frame_occupancy.anchor_x_pct <= 50 ? "left" : "right"
    : direction;
  const offsetX = sideDirection === "left"
    ? (1 - rhythmProgress) * -travel
    : sideDirection === "right"
      ? (1 - rhythmProgress) * travel
      : 0;
  const offsetY = direction === "bottom"
    ? (1 - rhythmProgress) * travel
    : direction === "top"
      ? (1 - rhythmProgress) * -travel
      : 0;
  const isPop = /spring|pop|rise/.test(asset.motion.entrance);
  const scale = isPop ? 0.92 + progress * 0.08 : 1;
  const isMaskReveal = /wipe|draw|mask|unfold/.test(asset.motion.entrance);
  const revealFromRight = asset.motion.direction === "right-to-left";
  const clipPath = isMaskReveal
    ? revealFromRight
      ? `inset(0 0 0 ${(1 - linearProgress) * 100}%)`
      : `inset(0 ${(1 - linearProgress) * 100}% 0 0)`
    : "none";
  const actionStartFrame = Math.round((asset.action_motion.start_pct / 100) * durationInFrames);
  const actionEndFrame = Math.round((asset.action_motion.end_pct / 100) * durationInFrames);
  const hasAction = asset.action_motion.type !== "none" && actionEndFrame > actionStartFrame;
  const rawActionProgress = hasAction
    ? interpolate(frame, [actionStartFrame, actionEndFrame], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;
  const actionProgress = asset.action_motion.easing === "ease-in"
    ? rawActionProgress * rawActionProgress
    : asset.action_motion.easing === "ease-out"
      ? 1 - (1 - rawActionProgress) ** 2
      : asset.action_motion.easing === "ease-in-out"
        ? rawActionProgress < 0.5
          ? 2 * rawActionProgress * rawActionProgress
          : 1 - ((-2 * rawActionProgress + 2) ** 2) / 2
        : asset.action_motion.easing === "spring" && hasAction
          ? spring({
              frame: Math.max(0, frame - actionStartFrame),
              fps,
              durationInFrames: Math.max(1, actionEndFrame - actionStartFrame),
              config: {damping: 20, stiffness: 120, mass: 0.8},
            })
          : rawActionProgress;
  const actionType = asset.action_motion.type;
  const pathPoints = asset.action_motion.path_points_pct ?? [];
  const pathPosition = (() => {
    if (pathPoints.length < 2) return null;
    const segmentFloat = Math.min(pathPoints.length - 1, actionProgress * (pathPoints.length - 1));
    const segment = Math.min(pathPoints.length - 2, Math.floor(segmentFloat));
    const local = segmentFloat - segment;
    const from = pathPoints[segment];
    const to = pathPoints[segment + 1];
    return {
      x: from.x_pct + (to.x_pct - from.x_pct) * local,
      y: from.y_pct + (to.y_pct - from.y_pct) * local,
    };
  })();
  const actionX = pathPosition?.x ?? asset.action_motion.translate_x_pct * actionProgress;
  const actionY = pathPosition?.y ?? asset.action_motion.translate_y_pct * actionProgress;
  const isPulseAction = /emphasize|stamp|pulse/.test(actionType);
  const pulseAmount = asset.action_motion.pulse_scale ?? Math.max(0.04, asset.action_motion.scale_to - 1);
  const semanticPulse = isPulseAction ? Math.sin(actionProgress * Math.PI) * pulseAmount : 0;
  const actionScale = 1 + (asset.action_motion.scale_to - 1) * actionProgress + semanticPulse;
  const actionRotate = asset.action_motion.rotate_deg * actionProgress;
  const holdFrame = Math.max(0, frame - Math.max(endFrame, actionEndFrame));
  const isLocked = /locked|none/.test(asset.motion.hold);
  const finalHoldFrame = Math.round((finalHoldStartPct / 100) * durationInFrames);
  const holdMotionWeight = interpolate(frame, [Math.max(0, finalHoldFrame - 5), finalHoldFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const drift = isLocked ? 0 : Math.sin(holdFrame / Math.max(1, fps * 0.8)) * (dominant ? 0.7 : 0.35) * holdMotionWeight;
  const tilt = isLocked ? 0 : Math.sin(holdFrame / Math.max(1, fps * 1.1)) * (dominant ? 0.45 : 0.2) * holdMotionWeight;
  const revealAction = /draw|reveal|wipe|highlight/.test(actionType);
  const revealDirection = asset.action_motion.reveal_direction ?? "left-to-right";
  const actionClipPath = revealAction
    ? revealDirection === "right-to-left"
      ? `inset(0 0 0 ${(1 - actionProgress) * 100}%)`
      : revealDirection === "top-to-bottom"
        ? `inset(0 0 ${(1 - actionProgress) * 100}% 0)`
        : revealDirection === "bottom-to-top"
          ? `inset(${(1 - actionProgress) * 100}% 0 0 0)`
          : `inset(0 ${(1 - actionProgress) * 100}% 0 0)`
    : clipPath;
  const exitProgress = /hold-to-cut|none/.test(asset.motion.exit)
    ? 0
    : interpolate(frame, [Math.round(durationInFrames * 0.9), durationInFrames - 1], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
  const {width_pct, height_pct, anchor_x_pct, anchor_y_pct, sizing_mode} = asset.frame_occupancy;
  const sizingStyle = sizing_mode === "height-driven"
    ? {width: "auto", height: `${height_pct}%`, maxWidth: `${width_pct}%`}
    : sizing_mode === "width-driven"
      ? {width: `${width_pct}%`, height: "auto", maxHeight: `${height_pct}%`}
      : {width: `${width_pct}%`, height: `${height_pct}%`};

  return (
    <Img
      src={staticFile(toPublicPath(asset.path))}
      alt={asset.narrative_token}
      style={{
        position: "absolute",
        left: `${anchor_x_pct}%`,
        top: `${anchor_y_pct}%`,
        ...sizingStyle,
        objectFit: "contain",
        clipPath: actionClipPath,
        opacity: interpolate(linearProgress, [0, 0.18, 1], [0, 1, 1]) * (1 - exitProgress),
        transform: `translate(-50%, -50%) translate(${offsetX + actionX}vw, ${offsetY + actionY + drift}vh) scale(${scale * actionScale}) rotate(${tilt + actionRotate}deg)`,
        transformOrigin: "center bottom",
        zIndex: Number.isFinite(asset.z_index) ? asset.z_index : zIndexFor(slot),
        filter: "drop-shadow(0 18px 22px rgba(37, 29, 20, 0.18))",
      }}
    />
  );
};

export const VoxManifestScene: React.FC<Props> = ({manifest, durationInFrames}) => {
  const frame = useCurrentFrame();
  const background = manifest.assets.background_plate;
  const ordered = manifest.narrative_sequence
    .map((slot) => [slot, manifest.assets[slot]] as const)
    .filter((item): item is readonly [string, AssetEntry] => Boolean(item[1]?.approved && item[1]?.path));
  ordered.sort((first, second) => first[1].appearance_order - second[1].appearance_order);
  const backgroundProgress = interpolate(
    frame,
    [0, Math.max(1, Math.round(durationInFrames * 0.1))],
    [0, 1],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"},
  );

  return (
    <AbsoluteFill
      data-layout-archetype={manifest.composition.layout_archetype}
      data-reading-path={manifest.composition.reading_path}
      data-dominant-axis={manifest.composition.dominant_axis}
      data-foreground-strategy={manifest.composition.foreground_strategy}
      data-motion-rhythm={manifest.motion_rhythm}
      style={{
        backgroundColor: "#78B8D8",
        overflow: "hidden",
        perspective: manifest.composition.layout_archetype === "depth-tunnel" ? 1200 : undefined,
      }}
    >
      <Img
        src={staticFile(toPublicPath(background.path))}
        alt={background.narrative_token}
        style={{
          position: "absolute",
          inset: "-1%",
          width: "102%",
          height: "102%",
          objectFit: "cover",
          opacity: backgroundProgress,
          transform: `scale(${1.015 - backgroundProgress * 0.015})`,
          zIndex: 0,
        }}
      />
      {ordered.map(([slot, asset]) => (
        <AnimatedAsset
          key={slot}
          slot={slot}
          asset={asset}
          durationInFrames={durationInFrames}
          dominant={slot === manifest.dominant_motion_asset}
          readingPath={manifest.composition.reading_path}
          motionRhythm={manifest.motion_rhythm}
          finalHoldStartPct={manifest.final_hold_start_pct}
        />
      ))}
    </AbsoluteFill>
  );
};
"""


def scene_component_tsx(
    scene_title: str,
    scene_meta: dict,
    total: int,
    style_family: str,
    fps: int,
) -> str:
    index = scene_meta.get("scene_index", 1)
    title = safe_scene_title(scene_meta)
    label = lower_label(scene_meta)
    archetype = infer_scene_archetype(scene_meta, index, total)
    scene_slug = scene_meta["slug"]

    if style_family == "vox-mixed-media":
        duration_in_frames = round(scene_meta["duration_seconds"] * fps)
        public_scene_slug = f"scene-{index:02d}"
        return f"""import React from "react";
import manifest from "../../../02_assets/scenes/{public_scene_slug}/ASSETS.json";
import {{VoxManifestScene}} from "../templates/VoxManifestScene";
import type {{SceneManifest}} from "../templates/VoxManifestScene";

export const {scene_title}: React.FC = () => (
  <VoxManifestScene
    manifest={{manifest as unknown as SceneManifest}}
    durationInFrames={{{duration_in_frames}}}
  />
);
"""

    if archetype == "editorial":
        return f"""import React from "react";
import {{EditorialPageScene}} from "../archetypes/EditorialPageScene";

export const {scene_title}: React.FC = () => {{
  return (
    <EditorialPageScene
      backgroundAsset=""
      pageAsset=""
      pageAssetLabel="approved editorial page image asset"
      noteLabel="editorial-page scene"
    />
  );
}};
"""

    if archetype == "alpha":
        return f"""import React from "react";
import {{AlphaPlateScene}} from "../archetypes/AlphaPlateScene";

export const {scene_title}: React.FC = () => {{
  return (
    <AlphaPlateScene
      backgroundAsset=""
      title={ts_literal(title)}
      alphaVideoAsset=""
      heroSrc=""
      heroLabel="primary cutout or plate"
      metricCardAsset=""
      metricCardLabel="approved metric-card image asset"
      foregroundBandAsset=""
      foregroundLabel="alpha-plate scene"
    />
  );
}};
"""

    if archetype == "dataviz":
        return f"""import React from "react";
import {{DataVizScene}} from "../archetypes/DataVizScene";

export const {scene_title}: React.FC = () => {{
  return (
    <DataVizScene
      backgroundAsset=""
      title={ts_literal(title)}
      chartAsset=""
      chartAssetLabel="approved chart or map image asset"
      footerLabel="data-viz scene"
      rightAsset=""
      rightAssetLabel="supporting cutout"
    />
  );
}};
"""

    if archetype == "speech":
        return f"""import React from "react";
import {{SpeechBubbleScene}} from "../archetypes/SpeechBubbleScene";

export const {scene_title}: React.FC = () => {{
  return (
    <SpeechBubbleScene
      backgroundAsset=""
      title={ts_literal(title)}
      subjectSrc=""
      subjectLabel="handshake or paired cutout"
      foregroundSrc=""
      bubble1Asset=""
      bubble1Label="approved speech-bubble image asset 1"
      bubble2Asset=""
      bubble2Label="approved speech-bubble image asset 2"
      foregroundLabel="speech-bubble scene"
    />
  );
}};
"""

    if archetype == "typewriter":
        return f"""import React from "react";
import {{TypewriterPunchlineScene}} from "../archetypes/TypewriterPunchlineScene";

export const {scene_title}: React.FC = () => {{
  return (
    <TypewriterPunchlineScene
      backgroundAsset=""
      alphaVideoAsset=""
      alphaLabel="symbolic alpha plate"
      textCardAsset=""
      textCardLabel="approved punchline text-card image asset"
    />
  );
}};
"""

    compare_scene = any(word in scene_narration(scene_meta).lower() for word in ["military", "worker", "interest", "costs more"])
    subjects = [
        """        {
          src: "",
          label: "primary cutout",
          x: -260,
          y: 120,
          width: 440,
          startFrame: 18,
          endFrame: 60,
          strokeX: -24,
          strokeY: 10,
        },"""
    ]
    if compare_scene:
        subjects.append(
            """        {
          src: "",
          label: "contrast cutout",
          x: 280,
          y: 130,
          width: 420,
          startFrame: 56,
          endFrame: 98,
          strokeX: 24,
          strokeY: 10,
        },"""
        )
    else:
        subjects.append(
            """        {
          src: "",
          label: "secondary cutout",
          x: 260,
          y: 140,
          width: 360,
          startFrame: 50,
          endFrame: 90,
          strokeX: 24,
          strokeY: 10,
        },"""
        )
    subjects_block = "\n".join(subjects)
    return f"""import React from "react";
import {{CutoutRiseScene}} from "../archetypes/CutoutRiseScene";

export const {scene_title}: React.FC = () => {{
  return (
    <CutoutRiseScene
      backgroundAsset=""
      title={ts_literal(title)}
      subtitle="Replace this cutout-rise scene with final approved assets and timings."
      foregroundLabel={ts_literal(label)}
      subjects={{[
{subjects_block}
      ]}}
    />
  );
}};
"""


def root_sequence_tsx(total_duration: int, fps: int, aspect_ratio: str) -> str:
    canvas = REMOTION_CANVASES[aspect_ratio]
    return f"""import React from "react";
import {{Composition}} from "remotion";
import {{MainSequence}} from "./Sequence";

export const RemotionRoot: React.FC = () => {{
  return (
    <Composition
      id="MainSequence"
      component={{MainSequence}}
      durationInFrames={{{total_duration}}}
      fps={{{fps}}}
      width={{{canvas["width"]}}}
      height={{{canvas["height"]}}}
      defaultProps={{{{}}}}
    />
  );
}};
"""


def sequence_tsx_for_scenes(
    scenes: list[dict],
    fps: int,
    audio_public_name: str = "",
) -> str:
    imports = []
    components = []
    for index, scene_meta in enumerate(scenes, start=1):
        component_name = f"Scene{index:02d}"
        imports.append(f'import {{{component_name}}} from "./scenes/{component_name}";')
        duration = round(scene_meta["duration_seconds"] * fps)
        components.append(
            f"""        <Series.Sequence durationInFrames={{{duration}}}>
          <{component_name} />
        </Series.Sequence>"""
        )
    imports_block = "\n".join(imports)
    components_block = "\n".join(components)
    total_duration = sum(round(scene["duration_seconds"] * fps) for scene in scenes)
    audio_imports = ", Audio, staticFile" if audio_public_name else ""
    audio_layer = (
        f'<Audio src={{staticFile("audio/{audio_public_name}")}} />'
        if audio_public_name
        else ""
    )
    return f"""import React from "react";
import {{AbsoluteFill, Series{audio_imports}}} from "remotion";
{imports_block}

export const MAIN_SEQUENCE_DURATION = {total_duration};

export const MainSequence: React.FC = () => {{
  return (
    <AbsoluteFill>
      <Series>
{components_block}
      </Series>
      {audio_layer}
    </AbsoluteFill>
  );
}};
"""


def public_readme() -> str:
    return """Place rendered or supplied assets here.

Recommended folders:
- audio/
- scenes/

Remotion rule:
- do not rely on one full-frame `scene-xx.png` as the main source for a Remotion scene
- place scene assets into `scenes/scene-xx/` folders as separate files: required `background.png`, `hero-cutout.png`, `support-cutout-01.png`, and `metaphor-driver.png`; rename or extend the latter two roles in the Manifest when the content calls for more specific assets
- every scene uses its own background file by default; do not point several manifests at one shared background
- alpha-trim every final non-background PNG to 3-5% transparent padding while preserving the original imagegen output
- lock the visual metaphor, composition archetype, reading path, foreground strategy, and motion rhythm before generating assets
- fill content kind, z-index, sizing mode, visible frame occupancy, narrative order, entrance motion, and semantic action motion before implementation
- use height-driven sizing for portrait subjects, width-driven sizing for groups/cards/strips, and box-contain for isolated props
- do not create or import SVG assets; visible art must be approved raster assets
- do not create visible art with Pillow, Canvas, OpenCV, Cairo, Matplotlib, Sharp, ImageMagick drawing, or another local generator
- `source=imagegen` requires a real tool call plus prompt/original/receipt/hash provenance under `02_assets/`
- update the matching `02_assets/scenes/scene-xx/ASSETS.json`, then run `python3 tools/validate_collage_project.py --project .` from the project root before Studio or render
"""


def scene_asset_manifest(
    scene_slug: str,
    public_scene_slug: str,
    aspect_ratio: str,
    background_policy: str,
    background_sharing_authorized: bool,
) -> dict:
    public_root = f"07_remotion/public/scenes/{public_scene_slug}"

    horizontal = aspect_ratio == "16:9"

    def asset(
        filename: str,
        required: bool,
        appearance_order: int | None,
        width_pct: float | None,
        height_pct: float | None,
        anchor_x_pct: float | None,
        anchor_y_pct: float | None,
        entrance: str,
        direction: str,
        start_pct: float | None,
        end_pct: float | None,
        travel_pct: float | None,
        settle: str,
        hold: str,
    ) -> dict:
        if filename == "background.png":
            content_kind = "background"
            sizing_mode = "box-contain"
            z_index = 0
        elif "foreground" in filename:
            content_kind = "foreground-strip"
            sizing_mode = "width-driven"
            z_index = 40
        elif "environment" in filename:
            content_kind = "wide-group"
            sizing_mode = "width-driven"
            z_index = 6
        elif "editorial" in filename:
            content_kind = "editorial-card"
            sizing_mode = "width-driven"
            z_index = 12
        elif "accent" in filename:
            content_kind = "accent-mark"
            sizing_mode = "width-driven"
            z_index = 32
        elif "metaphor" in filename:
            content_kind = "object-prop"
            sizing_mode = "box-contain"
            z_index = 20
        elif "hero" in filename:
            content_kind = "portrait-subject"
            sizing_mode = "height-driven"
            z_index = 22
        else:
            content_kind = "portrait-subject"
            sizing_mode = "height-driven"
            z_index = 18
        return {
            "path": f"{public_root}/{filename}" if required else "",
            "source": "imagegen",
            "approved": False,
            "generation_batch": scene_slug,
            "provenance": {
                "method": "built-in-image_gen" if required else "",
                "tool_called": False,
                "result_receipt": "",
                "prompt_file": f"02_assets/prompts/{public_scene_slug}/{Path(filename).stem}.md" if required else "",
                "prompt_sha256": "",
                "original_path": f"02_assets/imagegen-originals/{public_scene_slug}/{filename}" if required else "",
                "original_sha256": "",
                "final_sha256": "",
                "postprocess": "none",
                "fallback_user_approved": False,
            },
            "narrative_token": "[fill from scene content]" if appearance_order else "scene environment",
            "appearance_reason": "[explain why this asset appears at this point in the content]" if appearance_order else "establishes this scene before narrated elements enter",
            "appearance_order": appearance_order,
            "z_index": z_index,
            "content_kind": content_kind,
            "frame_occupancy": {
                "width_pct": width_pct,
                "height_pct": height_pct,
                "anchor_x_pct": anchor_x_pct,
                "anchor_y_pct": anchor_y_pct,
                "sizing_mode": sizing_mode,
            },
            "motion": {
                "entrance": entrance,
                "direction": direction,
                "start_pct": start_pct,
                "end_pct": end_pct,
                "travel_pct": travel_pct,
                "settle": settle,
                "hold": hold,
                "exit": "hold-to-cut",
            },
            "action_motion": {
                "type": "none",
                "start_pct": end_pct,
                "end_pct": end_pct,
                "translate_x_pct": 0,
                "translate_y_pct": 0,
                "scale_to": 1,
                "rotate_deg": 0,
                "easing": "ease-in-out",
            },
        }

    return {
        "manifest_version": ASSET_MANIFEST_VERSION,
        "scene_slug": scene_slug,
        "status": "pending",
        "background_policy": background_policy,
        "background_sharing_authorized": background_sharing_authorized,
        "background_concept": "[fill one unique environment and dominant shape field for this scene]",
        "background_distinction_reason": "[explain how this background differs from adjacent scenes while preserving the visual system]",
        "visual_metaphor": {
            "abstract_claim": "[state the exact abstract claim from this Scene]",
            "concrete_metaphor": "[name one physical image or mechanism that makes the claim visible]",
            "mapping": "[explain what each metaphor part means in the claim]",
            "motion_payoff": "[describe the visible relationship change that proves the claim]",
            "asset_ids": [],
        },
        "composition": {
            "layout_archetype": "[choose from vox-motion-contract.md]",
            "reading_path": "[choose from vox-motion-contract.md]",
            "dominant_axis": "[horizontal / vertical / diagonal / radial / depth]",
            "foreground_strategy": "[none / corner-occluder / side-frame / lower-band / full-depth-prop / entering-subject]",
            "negative_space_intent": "[state which entrance or relationship the empty area serves]",
        },
        "motion_rhythm": "[choose from vox-motion-contract.md]",
        "composition_blueprint_locked": False,
        "color_script": {
            "style_reference": "0720-bright-paper",
            "dominant_field": "[choose one chromatic dominant field; not beige, tan, brown, gray, or off-white by default]",
            "support_colors": [],
            "focal_accent": "[choose one warm/cool focal counterpoint]",
            "dark_anchor": "[choose one deep chromatic anchor]",
            "paper_neutral": "[choose one cream or fibrous white separator]",
            "area_budget": {
                "dominant_pct": 45,
                "support_pct": 28,
                "neutral_pct": 18,
                "accent_pct": 9,
                "archival_brown_gray_pct": 8,
            },
            "hero_background_contrast": "[state the hue and lightness separation for every focal landing zone]",
            "adjacent_scene_shift": "[state how dominant hue or color balance changes from the adjacent Scene]",
            "prompt_palette_sentence": "[write one exact palette lock sentence to copy into every image prompt]",
            "negative_palette_terms": [
                "no sepia wash",
                "no all-beige palette",
                "no muddy brown-gray cast",
                "no desaturated vintage filter",
                "no monochrome kraft-paper scene",
                "no faded low-contrast look",
            ],
            "user_palette_override": False,
            "override_reason": "",
            "review": {
                "three_chromatic_hues_present": False,
                "hero_separates_at_thumbnail": False,
                "no_muddy_global_cast": False,
                "palette_match_across_assets": False,
            },
        },
        "background_contract": {
            "role": "stage-only",
            "allowed_elements": [],
            "forbidden_subjects": [],
            "max_saliency": "low",
            "semantic_overlap_forbidden": True,
            "reserved_zones": [],
            "review": {
                "reserved_zones_clear": False,
                "no_duplicate_subjects": False,
                "focal_competition": "fail",
            },
        },
        "collision_plan": {
            "default_max_overlap_pct": 8,
            "safe_gap_pct": 3,
            "motion_paths_reviewed": False,
            "allowed_overlaps": [],
        },
        "content_order_locked": False,
        "composition_locked": False,
        "motion_plan_locked": False,
        "narrative_sequence": [],
        "dominant_motion_asset": "",
        "final_hold_start_pct": 70,
        "rules": {
            "raster_only": True,
            "svg_forbidden": True,
            "flattened_scene_image_forbidden": True,
            "cross_scene_generation_sheet_forbidden": True,
            "minimum_approved_assets": 4,
            "maximum_approved_assets": 8,
            "minimum_independently_timed_non_background_assets": 3,
            "appearance_order_must_follow_content": True,
            "alpha_tight_crop_required": True,
            "visible_occupancy_must_be_computed_from_alpha_bounds": True,
            "background_must_be_approved_before_foreground_generation": True,
            "background_reserved_zones_required": True,
            "pairwise_collision_check_required": True,
            "narrated_action_requires_action_motion": True,
            "remotion_component_must_read_this_manifest": True,
            "generation_order": [
                "visual_metaphor_and_composition_lock",
                "color_script_and_composition_blueprint_lock",
                "background_plate",
                "hero_cutout",
                "content_specific_support_assets",
                "content_specific_metaphor_assets",
                "environment_band_optional",
                "editorial_surface_optional",
                "foreground_anchor_optional",
                "accent_mark_optional",
            ],
        },
        "assets": {
            "background_plate": asset(
                "background.png", True, 0, 100, 100, 50, 50,
                "cut-or-fade", "none", 0, 10, 1.5, "none", "drift-1pct-max",
            ),
            "hero_cutout": asset(
                "hero-cutout.png", True, 1,
                40 if horizontal else 70, 60 if horizontal else 46, 56, 56,
                "spring-rise", "bottom", 8, 32, 11, "small-overshoot", "vertical-drift-0.8pct",
            ),
            "support_cutout_01": asset(
                "support-cutout-01.png", True, 2,
                30 if horizontal else 52, 42 if horizontal else 26,
                72 if horizontal else 50, 40 if horizontal else 66,
                "slide-in", "side", 24, 46, 9, "short-settle", "drift-0.4pct",
            ),
            "metaphor_driver": asset(
                "metaphor-driver.png", True, 3,
                30 if horizontal else 48, 24 if horizontal else 18,
                54 if horizontal else 50, 76 if horizontal else 84,
                "wipe-on", "left-to-right", 44, 64, 8, "clean-stop", "locked",
            ),
            "foreground_anchor_optional": asset(
                "foreground-anchor.png", False, None,
                None, None, None, None,
                "rise", "bottom", None, None, None, "light-settle", "locked",
            ),
            "environment_band_optional": asset(
                "environment-band.png", False, None, None, None, None, None,
                "slide-in", "side", None, None, None, "short-settle", "locked",
            ),
            "support_cutout_02_optional": asset(
                "support-cutout-02.png", False, None, None, None, None, None,
                "pop-in", "none", None, None, None, "short-settle", "drift-0.3pct",
            ),
            "editorial_surface_optional": asset(
                "editorial-surface.png", False, None, None, None, None, None,
                "wipe-on", "left-to-right", None, None, None, "none", "locked",
            ),
            "accent_mark_optional": asset(
                "accent-mark.png", False, None, None, None, None, None,
                "draw-on", "target-dependent", None, None, None, "clean-stop", "single-pulse",
            ),
        },
    }


def asset_prompt_stub(scene_text: str, asset_role: str, aspect_ratio: str) -> str:
    canvas = canvas_contract(aspect_ratio)
    is_background = "background" in asset_role
    background_instruction = (
        "Before writing this prompt, copy the approved background_contract into it: list allowed fixed stage elements, repeat every forbidden_subject alias verbatim in the negative constraints, and describe every reserved zone as low-detail negative space. Generate and review this background before generating moving assets."
        if is_background
        else "Use the approved composition blueprint for this asset's landing box, z-index, neighboring assets, and motion corridor. Do not change the planned silhouette or add unrelated props that expand into another asset's reserved zone."
    )
    canvas_instruction = (
        f"Create one full-frame {canvas['orientation']} background at exactly {canvas['width']}x{canvas['height']} pixels with aspect ratio {canvas['aspect_ratio']}. Do not return another ratio, a framed mockup, a contact sheet, or several alternatives."
        if is_background
        else f"The delivery frame is {canvas['orientation']} {canvas['aspect_ratio']} ({canvas['width']}x{canvas['height']}). Generate one isolated asset only, tightly framed for its locked landing box; do not generate a full scene or multiple options."
    )
    return f"""# Imagegen Prompt: {asset_role}

Source scene:
{scene_text}

[fill one concrete, standalone imagegen prompt for this asset only. Include subject, Vox mixed-media materials, composition, chroma-key or background rule, exclusions, crispness requirements, and a close framing that fills the source canvas. For non-background assets, request one isolated subject with no decorative stickers or unrelated props.]

Gate 1 canvas rule: {canvas_instruction}
Blueprint rule: {background_instruction}
Color rule: copy the approved `color_script.prompt_palette_sentence` verbatim and repeat every `negative_palette_terms` phrase verbatim. Follow `0720-bright-paper-style.md`: use colorful low-detail stage fields, crisp warm-cool separation, and controlled neutrals; do not interpret quiet as beige, faded, or desaturated.

Execution rule: call the built-in `image_gen` tool once for this asset. Do not replace the tool call with Pillow, Canvas, SVG, CSS, OpenCV, ImageMagick drawing, or another project-local generator.
Preparation rule: preserve the original output, then remove chroma key when needed and alpha-trim the final PNG to 3-5% transparent padding. Record `crop` or `remove-chroma-key+crop` in provenance. Do not place an uncropped source with large transparent margins into Remotion.
"""


def first_frame_prompt_stub(scene_text: str, aspect_ratio: str) -> str:
    canvas = canvas_contract(aspect_ratio)
    return f"""# Imagegen Generate Prompt: first-frame

Source scene:
{scene_text}

[Fill a concrete prompt for one empty or near-empty fixed background master. Include the approved color script, fixed surfaces, reserved change regions, and all forbidden entering subjects.]

Gate 1 canvas lock:
- aspect ratio: `{canvas["aspect_ratio"]}`
- orientation: `{canvas["orientation"]}`
- exact target canvas: `{canvas["width"]}x{canvas["height"]}` pixels

Repeat this sentence verbatim inside the final image prompt:
`Create one {canvas["orientation"]} {canvas["aspect_ratio"]} full-frame canvas at exactly {canvas["width"]}x{canvas["height"]} pixels. Do not return 3:2, 4:3, 1:1, or any other aspect ratio.`

Execution rule: call built-in `image_gen` in generate mode with no reference image. Save the selected result as `first-frame.png`, inspect it with `view_image`, and record its actual receipt and SHA-256 in `keyframe_generation_contract.first_frame`.
Immediate canvas gate: before creating `last-frame.png`, run `python3 tools/validate_seedance_first_frame.py --project . --scene-spec [scene spec path]`. If it fails, stop. Normalize or regenerate the first frame, preserve the original receipt and normalization record, then run the gate again. Never create the last frame from a nonconforming canvas.
Continuity rule: this exact file becomes the immutable edit target for `last-frame.png`. Do not regenerate the background after foreground planning begins.
"""


def last_frame_edit_prompt_stub(scene_text: str, aspect_ratio: str) -> str:
    canvas = canvas_contract(aspect_ratio)
    return f"""# Imagegen Edit Prompt: last-frame

Source scene:
{scene_text}

Edit target: the exact approved local `first-frame.png` for this Scene.
Tool input rule: inspect the target with `view_image`, then call built-in `image_gen` in edit mode with that exact local path as the sole `referenced_image_paths` entry. An independent text-to-image call is forbidden.

Change only these approved regions:
- [region id + x/y/width/height percentages]: [exact entering object]

Hard invariants outside those regions:
preserve the exact canvas, crop, camera, perspective, background geometry, horizon, contours, paper tears, edge positions, texture, grain, color, lighting, and every fixed object. Do not repaint, restyle, regenerate, extend, simplify, or move the background.

Canvas invariant inherited from Gate 1:
the edit target has aspect ratio `{canvas["aspect_ratio"]}` and exact canvas `{canvas["width"]}x{canvas["height"]}`. Preserve those dimensions exactly. Cropping either frame after this edit is forbidden.

Palette rule: copy `color_script.prompt_palette_sentence` and every `negative_palette_terms` phrase verbatim.
Output rule: save the edited result as `last-frame.png`; record the edit receipt, exact first-frame path and SHA-256, `referenced_image_paths`, change regions, and final SHA-256 in `keyframe_generation_contract.last_frame`.
"""


def write_asset_prompt_stubs(
    output: Path,
    public_scene_slug: str,
    scene_text: str,
    production_mode: str,
    aspect_ratio: str,
    force: bool,
) -> None:
    prompt_dir = output / "02_assets" / "prompts" / public_scene_slug
    ensure_dir(prompt_dir)
    if production_mode == "remotion-code":
        original_dir = output / "02_assets" / "imagegen-originals" / public_scene_slug
        ensure_dir(original_dir)
        roles = {
            "background": "quiet scene-specific background plate",
            "hero-cutout": "independent dominant metaphor subject",
            "support-cutout-01": "second independent narrative subject required by the content order",
            "metaphor-driver": "independent prop, path, chart line, or mechanism that performs the Scene motion payoff",
        }
        for filename, role in roles.items():
            write_text(
                prompt_dir / f"{filename}.md",
                asset_prompt_stub(scene_text, role, aspect_ratio),
                force,
            )
        return
    write_text(prompt_dir / "first-frame.md", first_frame_prompt_stub(scene_text, aspect_ratio), force)
    write_text(prompt_dir / "last-frame.md", last_frame_edit_prompt_stub(scene_text, aspect_ratio), force)


def write_remotion_template(output: Path, args: argparse.Namespace, config: dict, force: bool) -> None:
    root = output / "07_remotion"
    src = root / "src"
    templates_dir = src / "templates"
    archetypes_dir = src / "archetypes"
    scenes_dir = src / "scenes"
    public_dir = root / "public"
    ensure_dir(templates_dir)
    ensure_dir(archetypes_dir)
    ensure_dir(scenes_dir)
    ensure_dir(public_dir)
    ensure_dir(public_dir / "audio")
    ensure_dir(public_dir / "scenes")
    ensure_dir(root / "out")

    beats = config["beats"]
    scenes = config.get("scenes", [])
    duration_frames = round(args.duration * args.fps)
    audio_public_name = ""
    source_audio_path = resolve_gate_file(args, args.source_audio_file)
    if args.audio_mode != "no-audio" and source_audio_path and source_audio_path.is_file():
        audio_public_name = f"voiceover{source_audio_path.suffix.lower() or '.mp3'}"
        audio_destination = public_dir / "audio" / audio_public_name
        if source_audio_path.resolve() != audio_destination.resolve():
            shutil.copy2(source_audio_path, audio_destination)

    write_text(root / "package.json", package_json(), force)
    write_text(root / "tsconfig.json", tsconfig_json(), force)
    write_text(root / "remotion.config.ts", remotion_config_ts(), force)
    write_text(src / "index.ts", src_index_ts(), force)
    if args.style_family == "vox-mixed-media":
        write_text(templates_dir / "VoxManifestScene.tsx", vox_manifest_scene_tsx(), force)
    else:
        write_text(templates_dir / "SceneBackground.tsx", scene_background_tsx(), force)
        write_text(templates_dir / "CutoutSubject.tsx", cutout_subject_tsx(), force)
        write_text(templates_dir / "SceneShell.tsx", scene_shell_tsx(), force)
        write_text(archetypes_dir / "CutoutRiseScene.tsx", cutout_rise_scene_tsx(), force)
        write_text(archetypes_dir / "EditorialPageScene.tsx", editorial_page_scene_tsx(), force)
        write_text(archetypes_dir / "AlphaPlateScene.tsx", alpha_plate_scene_tsx(), force)
        write_text(archetypes_dir / "DataVizScene.tsx", data_viz_scene_tsx(), force)
        write_text(archetypes_dir / "SpeechBubbleScene.tsx", speech_bubble_scene_tsx(), force)
        write_text(
            archetypes_dir / "TypewriterPunchlineScene.tsx",
            typewriter_punchline_scene_tsx(),
            force,
        )
    write_text(public_dir / "README.txt", public_readme(), force)

    if args.mode == "vo-sequence":
        scene_total_frames = sum(
            round(scene["duration_seconds"] * args.fps) for scene in scenes
        )
        write_text(
            src / "Root.tsx",
            root_sequence_tsx(scene_total_frames, args.fps, args.aspect_ratio),
            force,
        )
        write_text(
            src / "Sequence.tsx",
            sequence_tsx_for_scenes(scenes, args.fps, audio_public_name),
            force,
        )
        for index, scene_meta in enumerate(scenes, start=1):
            component_name = f"Scene{index:02d}"
            scene_asset_dir = public_dir / "scenes" / f"scene-{index:02d}"
            ensure_dir(scene_asset_dir)
            write_text(
                scene_asset_dir / "README.txt",
                "Place approved scene assets here.\n"
                "Required files:\n"
                "- background.png\n"
                "- hero-cutout.png\n"
                "- support-cutout-01.png\n"
                "- metaphor-driver.png\n"
                "The latter two are placeholders for content-specific independent assets; update their narrative role before generation.\n"
                "Optional role examples:\n"
                "- support-cutout-01.png\n"
                "- metaphor-driver.png\n"
                "- foreground-anchor.png\n"
                "- editorial-surface.png\n"
                "- accent-mark.png\n"
                "Do not default to left/right cards plus a lower strip. Use the locked layout archetype and follow ASSETS.json appearance order.\n",
                force,
            )
            write_text(
                scenes_dir / f"{component_name}.tsx",
                scene_component_tsx(
                    component_name,
                    scene_meta,
                    len(scenes),
                    args.style_family,
                    args.fps,
                ),
                force,
            )
    else:
        write_text(
            src / "Root.tsx",
            root_single_scene_tsx(duration_frames, args.fps, args.aspect_ratio),
            force,
        )
        write_text(
            src / "Sequence.tsx",
            single_scene_sequence_tsx(
                duration_frames,
                args.style_family,
                audio_public_name,
            ),
            force,
        )


def prompt_1(scene: str, reference_url: str, style_family: str, production_mode: str) -> str:
    reference = reference_url or "[add reference link or local file path]"
    style_notes = style_family_notes(style_family)
    if production_mode == "video-model":
        return f"""Take a close look at this collage-style animation reference: {reference}

Plan one Seedance first+last scene for:
"{scene}"

Target style family: {style_notes["label"]} (`{style_family}`)

Do these tasks in order:
1. Write a concise style thesis and one concrete moving metaphor.
2. Define the empty or near-empty first-frame state and the final assembled last-frame state.
3. List fixed first-frame surfaces, entering objects, draw-on paths, forbidden objects, and approved change regions.
4. Write the serial assembly order, locked-camera rule, action budget, and final hold.
5. Lock the Gate 1 canvas contract before image generation.
6. Stop after the storyboard. Do not create an `ASSETS.json`, composition blueprint, Remotion cutout pack, transparent PNG assets, contact sheet, or `07_remotion` project.
"""
    return f"""Take a close look at this collage-style animation reference: {reference}

Break it down frame by frame and rebuild the production plan for this new scene:
"{scene}"

Target style family: {style_notes["label"]} (`{style_family}`)

Do these tasks in order:
1. Write a concise style thesis.
2. State the abstract claim, invent one concrete physical metaphor, map every metaphor part to the claim, and define the motion payoff.
3. Choose a composition archetype, reading path, dominant axis, foreground strategy, and motion rhythm that physically implement the metaphor.
4. Build the composition blueprint: final boxes, action-end boxes, motion corridors, safe gaps, allowed overlaps, background forbidden subjects, and low-detail reserved zones.
5. Produce a master asset sheet listing every independently moving cutout, every derived layer, and each depth plane.
6. Create a five-beat storyboard with timings and motion notes.
7. Mark each beat as `remotion` or `seedance` based on scene complexity.
8. Stop after the storyboard and ask for sign-off before generating assets or building animation code.
"""


def prompt_1_sequence(
    scene: str,
    reference_url: str,
    narration_lines: list[str],
    style_family: str,
    production_mode: str,
) -> str:
    reference = reference_url or "[add reference link or local file path]"
    style_notes = style_family_notes(style_family)
    narration_block = "\n".join(f"- {line}" for line in narration_lines) or "- [add narration lines]"
    if production_mode == "video-model":
        return f"""Take a close look at this editorial collage reference: {reference}

We are building a voiceover-led Seedance sequence for:
"{scene}"

Target style family: {style_notes["label"]} (`{style_family}`)

Use these narration beats as the timing source:
{narration_block}

Do these tasks in order:
1. Write one concise style thesis for the sequence.
2. Group narration beats into semantic Scenes inside the 4-12 second request window.
3. For each Scene, define one visual proposition, one moving metaphor, and distinct fixed background geometry.
4. For each Scene, define first-frame state, last-frame state, fixed surfaces, entering objects, draw-on paths, change regions, serial assembly order, and final hold.
5. Lock the Gate 1 canvas contract for every Scene before image generation.
6. Stop after the scene plan. Do not create `ASSETS.json` manifests, composition blueprints, Remotion cutout packs, transparent PNG assets, contact sheets, or a `07_remotion` project.
"""
    return f"""Take a close look at this editorial collage reference: {reference}

We are building a voiceover-led multi-scene explainer for:
"{scene}"

Target style family: {style_notes["label"]} (`{style_family}`)

Use these narration beats as the timing source:
{narration_block}

Do these tasks in order:
1. Write a concise style thesis for the full sequence.
2. Rewrite the narration where needed so it follows documentary script discipline: precise cold open, calm declaratives, one visual idea per sentence, and a short cliffhanger ending.
3. Turn each narration line into a beat with visual triggers.
4. Group the beats into a practical scene list.
5. For every Scene, write abstract claim -> concrete metaphor -> mapping -> motion payoff before naming assets.
6. Assign a layout archetype, reading path, dominant axis, foreground strategy, and motion rhythm to every Scene.
7. For every Scene, build a composition blueprint with final boxes, motion corridors, safe gaps, allowed overlaps, background forbidden subjects, and low-detail reserved zones.
8. Produce a sequence diversity matrix and revise it until adjacent layouts differ and a 4+ Scene sequence uses at least 3 layouts and 3 rhythms.
9. Mark which scenes stay in Remotion and which scenes should escalate to Seedance first+last scenes.
10. Create a sequence storyboard and a beat-to-scene map.
11. Stop for sign-off before generating a full asset pack or writing scene components.
"""


def prompt_2(scene: str, image_model: str, public_base_url: str, style_family: str) -> str:
    style_notes = style_family_notes(style_family)
    return f"""Use the approved storyboard and asset sheet to build the full cutout pack for:
"{scene}"

Generate or prepare each asset as a transparent PNG with the collage treatment baked into the image itself:
- {style_notes["materials"][0]}
- {style_notes["materials"][1]}
- {style_notes["materials"][2]}
- one dominant hero element per beat when possible
- at most 2-3 supporting elements
- generous negative space, no decorative clutter
- avoid long readable text inside generated imagery

Use the `imagegen` skill as the default image-generation path. The configured image stack is {image_model}. Make one actual built-in `image_gen` tool call per distinct asset; merely writing `source=imagegen` is invalid. Save one regenerable prompt per asset, preserve the unmodified selected output under `02_assets/imagegen-originals/`, and record the result receipt plus prompt/original/final hashes.
If the scene stays in Remotion, do not solve it with one flattened full-frame still; generate separate movable assets instead.
Generation order for Remotion scenes:
- first lock the abstract claim, concrete metaphor, mapping, motion payoff, layout archetype, reading path, and motion rhythm
- lock the per-Scene `color_script` from `0720-bright-paper-style.md`, including the exact palette sentence, area budget, hero/background separation, adjacent-Scene shift, and negative palette terms
- calculate final element boxes, reserve low-detail background zones, check pairwise overlap, and review motion paths
- set `composition_blueprint_locked=true` and run `python3 tools/validate_composition_blueprint.py --project .`; do not call imagegen until it passes
- first generate and approve a scene-specific `background.png`
- stop and inspect the background alone; reject duplicate subject classes, detailed objects in reserved zones, or background focal competition
- reject beige-dominant, muddy brown-gray, faded, low-contrast, or globally desaturated backgrounds; quiet must come from broad low-detail shapes
- second generate the dominant metaphor subject as `hero-cutout.png`
- third generate at least two independently moving content-specific assets named after their narrative roles
- fourth generate optional environment, path, editorial, foreground, and accent assets only when the metaphor needs them
Hard prohibition for Remotion scenes:
- if the image tool is unavailable or fails, stop and report the blocker; do not substitute Pillow, ImageDraw, Canvas, OpenCV, SVG, CSS, or another project-local generator
- do not create `generate_assets.py`, `draw_assets.py`, or an equivalent procedural visible-asset script, even if it writes PNG files
- do not replace a missing primary asset with SVG, CSS shapes, or live typography
- if the chart, page, bubble, counter card, or punchline card is important to the shot, generate it first as an approved image asset
- do not validate style by generating one whole scene poster before the asset list exists
- do not let the background plate contain decorative sticker clutter, surprise paper scraps, or extra subjects not listed in the asset plan
- do not reuse another scene's background or generate several scenes on one composite sheet
- do not merge independently moving subjects and props into one hero image
- do not default to a center hero, left support, right support, and full-width lower strip
- do not add a foreground strip unless the locked foreground strategy and metaphor require one
- fill each asset's frame occupancy, appearance order, entrance window, settle, hold, and exit before animation
If any beat is too dense for practical cutout animation, switch that beat to a Seedance package with exactly 2 full-frame stills:
- `first-frame.png`: empty or near-empty background plate
- `last-frame.png`: final assembled hold tableau
Show the pack on a contact sheet and stop for approval before building the scene.
"""


def prompt_2_video_model(scene: str, image_model: str, aspect_ratio: str) -> str:
    canvas = canvas_contract(aspect_ratio)
    return f"""Build only the Seedance first+last keyframe package for:
"{scene}"

Hard route lock:
- production mode: `video-model`
- image stack: {image_model}
- Gate 1 aspect ratio: `{canvas["aspect_ratio"]}`
- Gate 1 orientation: `{canvas["orientation"]}`
- canonical canvas: `{canvas["width"]}x{canvas["height"]}`
- required image count per Scene: exactly 2

Allowed image calls per Scene:
1. Generate `first-frame.png` once as the empty or near-empty fixed background master.
2. After the first-frame canvas gate passes, edit that exact local file into `last-frame.png` using it as the sole `referenced_image_paths` entry.

Forbidden work:
- do not generate a separate background plate, hero cutout, support cutout, ornament sheet, card, prop, contact sheet, or draft style frame
- do not create or fill `ASSETS.json`
- do not run `validate_composition_blueprint.py`
- do not create `07_remotion`, a Remotion template, or transparent cutout packs
- do not generate the last frame independently
- do not crop or resize either frame after the last-frame edit

Canvas sequence:
1. Copy the exact Gate 1 canvas sentence from `first-frame.md` into the image prompt.
2. Generate and inspect `first-frame.png`.
3. Run `python3 tools/validate_seedance_first_frame.py --project . --scene-spec [scene spec path]`.
4. If the canvas gate fails, stop before generating the last frame. Normalize or regenerate the first frame, preserve the original receipt and postprocess record, then rerun the gate.
5. Create `last-frame.png` only from the canvas-valid first frame.
6. Run the full keyframe continuity gate before Seedance submission.
"""


def prompt_2_sequence(scene: str, image_model: str, public_base_url: str, style_family: str) -> str:
    style_notes = style_family_notes(style_family)
    return f"""Use the approved narration map and scene plan to prepare the full asset system for:
"{scene}"

For each scene, separate assets into:
- one unique scene-specific background plate
- one dominant metaphor subject
- at least two independent content-specific moving assets that complete the metaphor
- optional support, editorial surface, environment, path, foreground, or accent assets
- 4-8 approved raster assets total
- at least 3 independently timed non-background assets

Generation order:
- write and lock `visual_metaphor`, `composition`, and `motion_rhythm`
- write and lock `color_script` from `0720-bright-paper-style.md`; every prompt must repeat its exact palette sentence and negative palette terms
- write and lock `background_contract` and `collision_plan` before any image call
- set `composition_blueprint_locked=true` and pass `python3 tools/validate_composition_blueprint.py --project .`
- derive `narrative_sequence` from the source content first
- approve each scene's unique `background plate` first
- inspect each background alone and set its three review fields before generating moving assets
- approve the dominant metaphor subject and content-specific moving assets separately in narrative order
- approve optional editorial, path, foreground, and accent assets last

Use the `imagegen` skill for generated cut-outs and generated editorial surfaces. The configured image stack is {image_model}. Make one actual built-in `image_gen` tool call per distinct asset. Preserve each concrete prompt, unmodified selected output, tool result receipt, and prompt/original/final hashes according to `asset-provenance-contract.md`. Keep every generated asset regenerable and preserve one locked visual system across the whole sequence.
Do not generate one cross-scene hero sheet. Do not use one composite hero image when its people, props, causes, or consequences need separate timing. Generate each independently moving element as its own transparent PNG.
Preserve these style cues across the sequence: {", ".join(style_notes["editorial"])}.
Image quality rules:
- keep silhouettes crisp and readable
- use at least three meaningful chromatic hues per Scene with a warm-cool counterpoint, dark anchor, and controlled fibrous neutral
- keep neutral area at or below 25% and brown/gray/tan archival tones at or below 20% unless a user palette override is recorded
- make every hero visibly separate from its landing zone by hue and lightness, not shadow alone
- avoid mushy painterly rendering or blurry atmospheric haze
- keep paper edges, white keylines, and halftone texture sharp enough to survive motion
- avoid long readable text inside the generated image
- leave enough negative space for editorial framing
- background plates must stay quiet, unified, and low-clutter
- background plates may include fixed terrain / architecture / sky / wall shapes only
- background plates must not include extra sticker scraps, marker doodles, decorative labels, or additional people unless those are explicitly listed as separate assets
- backgrounds must change with the scene's environment and visual goal while preserving the same palette, paper grain, and annotation language
- adjacent Scenes must use different layout archetypes; sequences of 4 or more Scenes need at least 3 layout archetypes and 3 motion rhythms
- vary reading path, dominant axis, final silhouette, focal position, and entrance origin across the sequence
- lower-band foreground may appear in at most one third of Scenes and never in adjacent Scenes
- the dominant action must physically perform the metaphor payoff; sliding finished cards into place is not enough
- the background is a low-saliency stage and may not duplicate any major moving subject or metaphor object
- reserve each element's final box and motion corridor in the background; keep those zones empty or very low detail
- calculate pairwise final overlap from alpha-visible bounds; reposition or explicitly justify every pair above the default 8% limit
- horizontal single hero target: 32-48% frame width and 45-72% frame height
- vertical single hero target: 58-82% frame width and 32-56% frame height
- support width should normally stay at or below 65% of hero width
- write width/height/anchor percentages for every asset
- write appearance order and per-element motion before approving the asset pack
- set `content_order_locked`, `composition_locked`, and `motion_plan_locked` to true only after reviewing the source-content mapping, frame occupancy, and motion plan
Hard prohibition for Remotion scenes:
- stop if image generation is unavailable or fails; never replace it with a local raster/vector drawing script
- do not create Pillow, ImageDraw, Canvas, OpenCV, Cairo, Matplotlib, Sharp, ImageMagick drawing, SVG, or CSS-generated visible art, regardless of final file extension
- do not output `scene-01.png` / `scene-02.png` style whole-scene illustrations as the main asset
- do not merge title text, subtitles, and all story information into a single generated image
- do not replace missing primary art with SVG, CSS shapes, or live typography built directly in Remotion
- if a speech bubble, metric card, quote card, chart, map, or page is narratively important, it must exist first as an approved image asset
- do not use the background plate as a dumping ground for secondary props, paper scraps, or accents that should animate independently
- do not mark a scene approved when fewer than 4 assets exist or fewer than 3 non-background assets have independent motion specs
- do not mark a scene approved when its metaphor, layout, reading path, foreground strategy, or motion rhythm is missing
- make appearance order follow the source content; annotations enter after their target
- leave the three review locks false until every scene has been checked against its source content
For any complex scene, also prepare exactly 2 Seedance stills:
- generate `first-frame.png` once as the empty or near-empty background plate
- edit that exact first-frame file into `last-frame.png`; independent last-frame generation is forbidden
Stop after the asset system and scene-by-scene manifest are approved.
"""

def prompt_3(engine: str, video_model: str, strategy: str, style_family: str) -> str:
    style_notes = style_family_notes(style_family)
    if strategy == "seedance-first-last":
        return f"""Build the approved complex collage scene as a Seedance first+last package.

Requirements:
- generate `first-frame.png` once with built-in `image_gen` generate mode
- immediately run `python3 tools/validate_seedance_first_frame.py --project . --scene-spec [scene spec path]`; do not create the last frame until it passes
- inspect the local first frame with `view_image`, then call built-in `image_gen` edit mode with that exact path as the sole `referenced_image_paths` input to produce `last-frame.png`
- change only declared addition regions; preserve canvas, crop, background geometry, fixed objects, torn edges, texture, and color outside them
- never use an independent text-to-image generation for `last-frame.png`
- never generate separate background, hero, support, card, ornament, or contact-sheet assets for this route
- keep the chosen style-family language consistent across both stills: {", ".join(style_notes["materials"])}
- `first-frame.png` is the empty or near-empty establishing plate
- `last-frame.png` is the finished composition the video should build toward
- allow snappy editorial emphasis motion, but keep the shot readable and non-cinematic
- let elements assemble back-to-front, then hold as a living paper poster
- write one precise `motion_intent` paragraph describing what moves, what stays anchored, and where the shot resolves
- fill the structured `motion_contract`; objects already visible in the first frame must be fixed, stroke animations must use `draw_on_paths`, and the timeline must be serial
- fill `keyframe_generation_contract` with actual imagegen receipts, first-frame edit-target hash, sole reference path, change regions, and continuity review
- pass `validate_seedance_keyframes.py` before running Seedance
- keep a 5-second scene to at most 4 non-hold action groups; group repeated identical objects into one controlled sequence
- submit the scene to {video_model} using first-frame + last-frame mode with local base64 image inputs
- summarize the final prompt, motion intent, and local frame paths back into the project

Execution command after the spec is filled:
python3 ~/.codex/skills/paper-collage-video/scripts/run_seedance_scene.py --project [project-root] --scene-spec ./03_animation/SEEDANCE_SCENE.json
"""
    return f"""Build the approved collage scene in {engine}.

Requirements:
- layer cutouts back to front with clear depth
- give each depth plane its own loopable motion
- use snappy editorial entrances and one dominant emphasis move per beat
- use stepped stop-motion holds with uneven durations on characters or hero inserts
- split any container prop into front and back layers so inserts can sit inside it
- do not draw the primary chart, page, map, bubble, counter card, or punchline card from scratch in SVG, CSS, or live typography; animate approved image assets instead
- expose full prop controls for position, size, timing, wobble, and audio sync

Stop after the scene feels correct at 1x playback and summarize any values that should be saved back into the project.
"""


def prompt_3_sequence(engine: str, video_model: str, style_family: str) -> str:
    style_notes = style_family_notes(style_family)
    if engine == "seedance":
        return f"""Build the approved first/last-frame collage sequence with {video_model}.

Requirements:
- use exactly one approved first frame and one imagegen-edited last frame per Scene
- preserve the first-frame background and camera exactly in the last frame
- execute each Scene with its validated SEEDANCE_SCENE.json and auto-by-content request duration
- keep the assembly order causal, the camera locked, and the final composition readable
- do not create ASSETS.json, transparent cutout packs, SVG assets, or a Remotion project
- preserve this style-family center of gravity: {", ".join(style_notes["editorial"])}

Run each Scene with `run_seedance_scene.py`, then assemble the returned clips on the locked narration timeline.
"""
    return f"""Build the approved editorial collage sequence in {engine}.

Requirements:
- make one reusable component per scene
- implement each Scene's locked visual metaphor; the dominant motion must perform its motion payoff
- make actual anchors, depth order, reading path, entrance origins, and final silhouette match the selected layout archetype
- do not build every Scene as a wrapper around the same center/left/right/lower-band composition
- use at least 3 layout archetypes and 3 motion rhythms in a sequence of 4 or more Scenes; adjacent Scenes must differ
- keep one shared palette, paper texture, and accent grammar while using a different background asset for each scene by default
- use snappy motion-graphics entrances, marker sweeps, chart draw-ons, and map reveals
- keep visible editorial surfaces asset-based: generate them with imagegen / Imagen, then animate them in Remotion
- read scene assets from scene-specific folders, not from one full-frame scene PNG
- read `narrative_sequence`, frame occupancy, and per-element motion from each scene's `ASSETS.json`
- enter assets in exact content order with unique contiguous `appearance_order` values
- target 32-48% frame width for a single horizontal hero, or 58-82% for a vertical hero; keep supports subordinate
- stagger entrances by 4-10 frames at 30 fps and finish meaningful assembly by 70% of the scene
- hold the final readable composition for the last 30% of the scene
- use one dominant Vox motion cue per beat; do not give every layer equally strong simultaneous movement
- treat text overlays, labels, counters, and note cards as separate motion layers rather than baking them into the main image
- do not let Remotion invent missing primary art with SVG, CSS blocks, or live typography when that art should have been approved as an image asset
- use a master Series assembly timed to the narration beats
- expose tunable props and keep scene duration constants explicit
- keep optional baked audio behind a switch if stems may ship separately
- preserve this style-family center of gravity: {", ".join(style_notes["editorial"])}

After the first complete Remotion render, run:
python3 ~/.codex/skills/paper-collage-video/scripts/extract_layout_audit.py --project [project-root]

Inspect the contact sheet at thumbnail size. Return to the manifests and choreography if the focal subject is too small, the metaphor is unclear, negative space is purposeless, or adjacent compositions repeat.

Stop after the sequence plays correctly against the narration timeline and summarize any saved prop values or retiming decisions.
"""


def prompt_4(audio_model: str, duration: float) -> str:
    return f"""Add sound to the approved collage scene.

Work in this order:
1. Pitch a few music directions with reasoning and do not generate anything yet.
2. After selection, create the chosen music bed and only the minimal supporting cues.
3. Add about three foley or ambience cues total unless the scene truly needs more.
4. Keep all cue timings and levels editable in code.
5. Render the final video.

Use {audio_model} where appropriate.
Final review rule: listen once without watching. Anything that reads as "a sound effect" instead of as part of the scene should be cut.

Target runtime: {duration:.2f} seconds.
"""


def prompt_4_sequence(audio_model: str, duration: float) -> str:
    return f"""Finish the editorial sequence audio and render workflow.

Work in this order:
1. Treat the voiceover as fixed timing.
2. Pitch 2-3 music directions that sit under narration.
3. Add only sparse effects where they sharpen a beat.
4. Decide whether the final workflow should ship as silent picture plus stems or as a baked reference mix.
5. Render the final sequence.

Use {audio_model} where appropriate.
Target runtime: {duration:.2f} seconds.
"""


def scaffold_project(args: argparse.Namespace) -> None:
    output = Path(args.output).expanduser().resolve()
    config = project_config(args.scene, args)
    gate0 = config["self_check"]
    gate1 = config["gate_1"]
    if gate0.get("status") != "pass":
        print(json.dumps(gate0, indent=2, ensure_ascii=False))
        raise SystemExit("Gate 0 failed. No project scaffold was created.")
    if gate1.get("status") != "pass":
        print(json.dumps(gate1, indent=2, ensure_ascii=False))
        raise SystemExit("Gate 1 failed. No project scaffold was created.")

    ensure_dir(output)

    directories = [
        output / "00_brief",
        output / "01_storyboard",
        output / "02_assets",
        output / "02_assets" / "prompts",
        output / "03_animation",
        output / "04_audio",
        output / "05_render",
        output / "prompts",
        output / "tools",
    ]
    if args.production_mode == "remotion-code":
        directories.extend(
            [
                output / "02_assets" / "scenes",
                output / "02_assets" / "imagegen-originals",
                output / "02_assets" / "supplied-originals",
            ]
        )
    else:
        directories.extend(
            [
                output / "02_assets" / "keyframes",
                output / "05_render" / "seedance",
            ]
        )
    if args.mode == "vo-sequence":
        directories.append(output / "06_sequence")
    if args.with_remotion_template:
        directories.append(output / "07_remotion")
    for directory in directories:
        ensure_dir(directory)

    kit_copied = False
    if args.kit_path:
        kit_root = Path(args.kit_path).expanduser().resolve()
        destination = output / "source-kit"
        ensure_dir(destination)
        copied_assets = copy_tree_if_present(kit_root / "assets", destination / "assets")
        copied_audio = copy_tree_if_present(kit_root / "audio", destination / "audio")
        kit_copied = copied_assets or copied_audio

    beats = config["beats"]
    scenes = config.get("scenes", [])
    report = config["self_check"]
    scene_slug = stable_scene_slug(args.scene)

    write_text(
        output / "project-config.json",
        json.dumps(config, indent=2, ensure_ascii=False),
        args.force,
    )
    write_text(
        output / "00_brief" / "project-brief.md",
        brief_md(args.scene, args, beats, kit_copied, scenes),
        args.force,
    )
    write_text(
        output / "00_brief" / "self-check.md",
        self_check_md(args, report),
        args.force,
    )
    write_text(
        output / "00_brief" / "gate-lock.json",
        json.dumps(config["gate_1"], indent=2, ensure_ascii=False),
        args.force,
    )
    if args.production_mode == "remotion-code":
        write_text(
            output / "tools" / "validate_collage_project.py",
            (SKILL_ROOT / "scripts" / "validate_collage_project.py").read_text(encoding="utf-8"),
            args.force,
        )
        write_text(
            output / "tools" / "validate_composition_blueprint.py",
            (SKILL_ROOT / "scripts" / "validate_composition_blueprint.py").read_text(encoding="utf-8"),
            args.force,
        )
        for script_name in (
            "ensure_remotion_runtime.py",
            "extract_layout_audit.py",
            "finalize_remotion_render.py",
            "verify_remotion_output.py",
        ):
            write_text(
                output / "tools" / script_name,
                (SKILL_ROOT / "scripts" / script_name).read_text(encoding="utf-8"),
                args.force,
            )
    else:
        write_text(
            output / "tools" / "validate_seedance_first_frame.py",
            (SKILL_ROOT / "scripts" / "validate_seedance_first_frame.py").read_text(encoding="utf-8"),
            args.force,
        )
    write_text(output / "01_storyboard" / "storyboard.md", storyboard_md(beats), args.force)
    if args.production_mode == "remotion-code":
        write_text(output / "02_assets" / "asset-manifest.md", asset_manifest_md(), args.force)
    if args.production_mode == "video-model":
        write_text(
            output / "02_assets" / "keyframes" / "README.md",
            keyframes_readme_md(args.aspect_ratio),
            args.force,
        )
    write_text(
        output / "03_animation" / "motion-plan.md",
        motion_plan_md(args),
        args.force,
    )
    write_text(
        output / "03_animation" / "scene-routing.md",
        route_plan_md(args, scene_slug),
        args.force,
    )
    if args.production_mode == "video-model":
        write_text(
            output / "03_animation" / "seedance-runbook.md",
            seedance_runbook_md(args, args.mode),
            args.force,
        )
    write_text(output / "04_audio" / "sound-plan.md", sound_plan_md(), args.force)
    write_text(
        output / "05_render" / "render-notes.md",
        render_notes_md(args),
        args.force,
    )
    if args.mode == "vo-sequence":
        write_text(
            output / "01_storyboard" / "narration-timeline.md",
            narration_timeline_md(beats),
            args.force,
        )
        write_text(
            output / "06_sequence" / "scene-plan.md",
            scene_plan_md(scenes, args.fps),
            args.force,
        )
        scene_root = output / "06_sequence" / "scenes"
        ensure_dir(scene_root)
        for scene_meta in scenes:
            scene_dir = scene_root / scene_meta["slug"]
            ensure_dir(scene_dir)
            if args.production_mode == "video-model":
                ensure_dir(output / "02_assets" / "keyframes" / scene_meta["slug"])
            public_scene_slug = f"scene-{scene_meta['scene_index']:02d}"
            if args.production_mode == "remotion-code":
                asset_manifest_dir = output / "02_assets" / "scenes" / public_scene_slug
                ensure_dir(asset_manifest_dir)
                write_text(
                    asset_manifest_dir / "ASSETS.json",
                    json.dumps(
                        scene_asset_manifest(
                            scene_meta["slug"],
                            public_scene_slug,
                            args.aspect_ratio,
                            args.background_policy,
                            args.background_sharing_authorized,
                        ),
                        indent=2,
                        ensure_ascii=False,
                    ),
                    args.force,
                )
            write_asset_prompt_stubs(
                output,
                public_scene_slug,
                scene_narration(scene_meta) or args.scene,
                args.production_mode,
                args.aspect_ratio,
                args.force,
            )
            write_text(
                scene_dir / "SCENE.md",
                scene_brief_md(scene_meta, args.fps, args.style_family),
                args.force,
            )
            if args.production_mode == "video-model":
                write_text(
                    scene_dir / "SEEDANCE_SCENE.json",
                    json.dumps(
                        seedance_scene_spec(
                            args,
                            scene_meta["slug"],
                            scene_meta["slug"],
                            scene_meta["duration_seconds"],
                            args.fps,
                            scene_index=scene_meta["scene_index"],
                        ),
                        indent=2,
                        ensure_ascii=False,
                    ),
                    args.force,
                )
        write_text(
            output / "prompts" / "01-decode-and-storyboard.md",
            prompt_1_sequence(
                args.scene,
                args.reference_url,
                config.get("narration_lines", []),
                args.style_family,
                args.production_mode,
            ),
            args.force,
        )
        write_text(
            output
            / "prompts"
            / (
                "02-generate-keyframes.md"
                if args.production_mode == "video-model"
                else "02-generate-asset-pack.md"
            ),
            prompt_2_video_model(args.scene, args.image_model, args.aspect_ratio)
            if args.production_mode == "video-model"
            else prompt_2_sequence(args.scene, args.image_model, "", args.style_family),
            args.force,
        )
        write_text(
            output / "prompts" / "03-build-living-scene.md",
            prompt_3_sequence(args.engine, args.video_model, args.style_family),
            args.force,
        )
        write_text(
            output / "prompts" / "04-score-and-render.md",
            prompt_4_sequence(args.audio_model, args.duration),
            args.force,
        )
    else:
        if args.production_mode == "video-model":
            ensure_dir(output / "02_assets" / "keyframes" / scene_slug)
        if args.production_mode == "remotion-code":
            asset_manifest_dir = output / "02_assets" / "scenes" / "scene-01"
            ensure_dir(asset_manifest_dir)
            write_text(
                asset_manifest_dir / "ASSETS.json",
                json.dumps(
                    scene_asset_manifest(
                        scene_slug,
                        "scene-01",
                        args.aspect_ratio,
                        args.background_policy,
                        args.background_sharing_authorized,
                    ),
                    indent=2,
                    ensure_ascii=False,
                ),
                args.force,
            )
        write_asset_prompt_stubs(
            output,
            "scene-01",
            args.scene,
            args.production_mode,
            args.aspect_ratio,
            args.force,
        )
        if args.production_mode == "video-model":
            write_text(
                output / "03_animation" / "SEEDANCE_SCENE.json",
                json.dumps(
                    seedance_scene_spec(
                        args,
                        scene_slug,
                        args.scene,
                        args.duration,
                        args.fps,
                    ),
                    indent=2,
                    ensure_ascii=False,
                ),
                args.force,
            )
        write_text(
            output / "prompts" / "01-decode-and-storyboard.md",
            prompt_1(args.scene, args.reference_url, args.style_family, args.production_mode),
            args.force,
        )
        write_text(
            output
            / "prompts"
            / (
                "02-generate-keyframes.md"
                if args.production_mode == "video-model"
                else "02-generate-asset-pack.md"
            ),
            prompt_2_video_model(args.scene, args.image_model, args.aspect_ratio)
            if args.production_mode == "video-model"
            else prompt_2(args.scene, args.image_model, "", args.style_family),
            args.force,
        )
        write_text(
            output / "prompts" / "03-build-living-scene.md",
            prompt_3(args.engine, args.video_model, recommend_scene_route(args), args.style_family),
            args.force,
        )
        write_text(output / "prompts" / "04-score-and-render.md", prompt_4(args.audio_model, args.duration), args.force)

    if args.with_remotion_template:
        write_remotion_template(output, args, config, args.force)

    print(f"Created project scaffold at {output}")
    print("Generated files:")
    print("- project-config.json")
    print("- 00_brief/project-brief.md")
    print("- 00_brief/self-check.md")
    print("- 00_brief/gate-lock.json")
    print("- 01_storyboard/storyboard.md")
    if args.production_mode == "remotion-code":
        print("- 02_assets/asset-manifest.md")
        print("- 02_assets/scenes/*/ASSETS.json")
        print("- tools/validate_composition_blueprint.py")
    else:
        print("- tools/validate_seedance_first_frame.py")
    if args.production_mode == "video-model":
        print("- 02_assets/keyframes/README.md")
    print("- 03_animation/motion-plan.md")
    print("- 03_animation/scene-routing.md")
    if args.production_mode == "video-model":
        print("- 03_animation/seedance-runbook.md")
    print("- 04_audio/sound-plan.md")
    print("- 05_render/render-notes.md")
    if args.mode == "vo-sequence":
        print("- 01_storyboard/narration-timeline.md")
        print("- 06_sequence/scene-plan.md")
        print("- 06_sequence/scenes/*/SCENE.md")
        if args.production_mode == "video-model":
            print("- 06_sequence/scenes/*/SEEDANCE_SCENE.json")
    elif args.production_mode == "video-model":
        print("- 03_animation/SEEDANCE_SCENE.json")
    if args.with_remotion_template:
        print("- 07_remotion/package.json")
        print("- 07_remotion/src/Root.tsx")
        print("- 07_remotion/src/Sequence.tsx")
        print("- 07_remotion/src/templates/VoxManifestScene.tsx")
    print("- prompts/01-decode-and-storyboard.md")
    print(
        "- prompts/02-generate-keyframes.md"
        if args.production_mode == "video-model"
        else "- prompts/02-generate-asset-pack.md"
    )
    print("- prompts/03-build-living-scene.md")
    print("- prompts/04-score-and-render.md")
    print("- tools/validate_collage_project.py")
    if kit_copied:
        print("- source-kit/assets and/or source-kit/audio")


def main() -> None:
    args = parse_args()
    scaffold_project(args)


if __name__ == "__main__":
    main()
