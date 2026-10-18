#!/usr/bin/env python3
"""Validate Scene layout, background reservations, and collisions before imagegen."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\[fill|todo|tbd|unused", re.IGNORECASE)
CURRENT_ASSET_MANIFEST_VERSION = 2
COMPOSITION_FIELDS = {
    "layout_archetype",
    "reading_path",
    "dominant_axis",
    "foreground_strategy",
    "negative_space_intent",
}
LAYOUT_ARCHETYPES = {"asymmetric-stage", "diagonal-cascade", "split-contrast", "radial-cycle", "depth-tunnel", "stacked-consequence", "map-route", "full-frame-data"}
READING_PATHS = {"left-to-right", "right-to-left", "top-to-bottom", "bottom-to-top", "diagonal-down", "diagonal-up", "radial-in", "radial-out", "serpentine", "center-out"}
DOMINANT_AXES = {"horizontal", "vertical", "diagonal", "radial", "depth"}
FOREGROUND_STRATEGIES = {"none", "corner-occluder", "side-frame", "lower-band", "full-depth-prop", "entering-subject"}
MOTION_RHYTHMS = {"sequential-build", "cause-then-effect", "counter-motion", "radial-convergence", "path-follow", "scale-shift", "replacement", "cascade", "draw-and-land"}
COLOR_SCRIPT_FIELDS = {
    "style_reference",
    "dominant_field",
    "support_colors",
    "focal_accent",
    "dark_anchor",
    "paper_neutral",
    "area_budget",
    "hero_background_contrast",
    "adjacent_scene_shift",
    "prompt_palette_sentence",
    "negative_palette_terms",
    "user_palette_override",
    "override_reason",
    "review",
}
AREA_BUDGET_FIELDS = {
    "dominant_pct",
    "support_pct",
    "neutral_pct",
    "accent_pct",
    "archival_brown_gray_pct",
}
REQUIRED_NEGATIVE_PALETTE_TERMS = {
    "no sepia wash",
    "no all-beige palette",
    "no muddy brown-gray cast",
    "no desaturated vintage filter",
    "no monochrome kraft-paper scene",
    "no faded low-contrast look",
}
NEUTRAL_DOMINANT_RE = re.compile(
    r"\b(?:beige|tan|kraft|brown|gray|grey|off[- ]?white|cream|米黄|褐|棕|灰|奶油)\b",
    re.IGNORECASE,
)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def add_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def concrete_text(value: Any, minimum: int = 4) -> bool:
    text = str(value).strip()
    return len(text) >= minimum and PLACEHOLDER_RE.search(text) is None


def validate_color_script(
    color_script: Any,
    relative: Path,
    errors: list[str],
) -> tuple[str, str, bool] | None:
    if not isinstance(color_script, dict):
        add_error(errors, f"{relative}: color_script is required before image generation.")
        return None
    missing = sorted(COLOR_SCRIPT_FIELDS - set(color_script))
    if missing:
        add_error(errors, f"{relative}: color_script is missing {', '.join(missing)}.")

    override = color_script.get("user_palette_override") is True
    if color_script.get("style_reference") != "0720-bright-paper" and not override:
        add_error(errors, f"{relative}: color_script.style_reference must be 0720-bright-paper by default.")
    if override and not concrete_text(color_script.get("override_reason"), 12):
        add_error(errors, f"{relative}: user palette override needs a concrete override_reason.")

    dominant = str(color_script.get("dominant_field", "")).strip()
    support = color_script.get("support_colors")
    accent = str(color_script.get("focal_accent", "")).strip()
    dark = str(color_script.get("dark_anchor", "")).strip()
    neutral = str(color_script.get("paper_neutral", "")).strip()
    for field, value in (
        ("dominant_field", dominant),
        ("focal_accent", accent),
        ("dark_anchor", dark),
        ("paper_neutral", neutral),
    ):
        if not concrete_text(value):
            add_error(errors, f"{relative}: color_script.{field} must name a concrete color and material role.")
    if not override and NEUTRAL_DOMINANT_RE.search(dominant):
        add_error(errors, f"{relative}: dominant_field must be chromatic; beige/brown/gray/cream may only support the default palette.")
    if not isinstance(support, list) or len(support) < (1 if override else 2) or any(
        not concrete_text(item) for item in (support if isinstance(support, list) else [])
    ):
        add_error(errors, f"{relative}: color_script.support_colors needs at least two concrete chromatic support colors.")
        support = []
    normalized_roles = [dominant.casefold(), accent.casefold(), dark.casefold()] + [
        str(item).strip().casefold() for item in support
    ]
    if len(set(normalized_roles)) != len(normalized_roles):
        add_error(errors, f"{relative}: dominant, support, accent, and dark-anchor color roles must be distinct.")

    area = color_script.get("area_budget")
    if not isinstance(area, dict):
        add_error(errors, f"{relative}: color_script.area_budget is required.")
        area = {}
    missing_area = sorted(AREA_BUDGET_FIELDS - set(area))
    if missing_area:
        add_error(errors, f"{relative}: color_script.area_budget is missing {', '.join(missing_area)}.")
    values = {field: area.get(field) for field in AREA_BUDGET_FIELDS}
    if not all(is_number(value) for value in values.values()):
        add_error(errors, f"{relative}: every color_script.area_budget value must be numeric.")
    elif not override:
        if not 35 <= values["dominant_pct"] <= 60:
            add_error(errors, f"{relative}: dominant_pct must be 35-60 for the default bright-paper palette.")
        if not 20 <= values["support_pct"] <= 40:
            add_error(errors, f"{relative}: support_pct must be 20-40 for the default bright-paper palette.")
        if not 5 <= values["neutral_pct"] <= 25:
            add_error(errors, f"{relative}: neutral_pct must be 5-25; neutrals may not dominate.")
        if not 3 <= values["accent_pct"] <= 15:
            add_error(errors, f"{relative}: accent_pct must be 3-15 so the focal color stays controlled.")
        if not 0 <= values["archival_brown_gray_pct"] <= 20:
            add_error(errors, f"{relative}: archival_brown_gray_pct may not exceed 20 by default.")
        planned_total = sum(values[field] for field in ("dominant_pct", "support_pct", "neutral_pct", "accent_pct"))
        if not 95 <= planned_total <= 105:
            add_error(errors, f"{relative}: dominant/support/neutral/accent area budget must total about 100, got {planned_total:.1f}.")

    for field in ("hero_background_contrast", "adjacent_scene_shift"):
        if not concrete_text(color_script.get(field), 18):
            add_error(errors, f"{relative}: color_script.{field} must state a concrete visual decision.")
    palette_sentence = str(color_script.get("prompt_palette_sentence", "")).strip()
    if not concrete_text(palette_sentence, 50):
        add_error(errors, f"{relative}: prompt_palette_sentence must be a concrete reusable palette lock.")
    else:
        palette_folded = palette_sentence.casefold()
        for role in [dominant, accent, dark] + list(support):
            if role and str(role).casefold() not in palette_folded:
                add_error(errors, f"{relative}: prompt_palette_sentence must name palette role {role!r} verbatim.")

    negatives = color_script.get("negative_palette_terms")
    normalized_negatives = {
        str(item).strip().casefold() for item in negatives
    } if isinstance(negatives, list) else set()
    missing_negatives = sorted(REQUIRED_NEGATIVE_PALETTE_TERMS - normalized_negatives)
    if missing_negatives and not override:
        add_error(errors, f"{relative}: negative_palette_terms is missing {missing_negatives}.")
    return dominant.casefold(), accent.casefold(), override


def final_box(entry: dict[str, Any]) -> tuple[float, float, float, float] | None:
    occupancy = entry.get("frame_occupancy", {})
    values = [occupancy.get(key) for key in ("width_pct", "height_pct", "anchor_x_pct", "anchor_y_pct")]
    if not all(is_number(value) for value in values):
        return None
    width, height, center_x, center_y = values
    action = entry.get("action_motion", {})
    if action.get("type") != "none":
        translate_x = action.get("translate_x_pct", 0)
        translate_y = action.get("translate_y_pct", 0)
        points = action.get("path_points_pct")
        if isinstance(points, list) and points and isinstance(points[-1], dict):
            translate_x = points[-1].get("x_pct", translate_x)
            translate_y = points[-1].get("y_pct", translate_y)
        scale = action.get("scale_to", 1)
        if not all(is_number(value) for value in (translate_x, translate_y, scale)):
            return None
        center_x += translate_x
        center_y += translate_y
        width *= scale
        height *= scale
    return (
        center_x - width / 2,
        center_y - height / 2,
        center_x + width / 2,
        center_y + height / 2,
    )


def action_box(entry: dict[str, Any], progress: float) -> tuple[float, float, float, float] | None:
    occupancy = entry.get("frame_occupancy", {})
    values = [occupancy.get(key) for key in ("width_pct", "height_pct", "anchor_x_pct", "anchor_y_pct")]
    if not all(is_number(value) for value in values):
        return None
    width, height, center_x, center_y = (float(value) for value in values)
    action = entry.get("action_motion", {})
    if action.get("type") != "none":
        translate_x = float(action.get("translate_x_pct", 0)) * progress
        translate_y = float(action.get("translate_y_pct", 0)) * progress
        points = action.get("path_points_pct")
        if isinstance(points, list) and len(points) >= 2:
            segment_float = min(len(points) - 1, progress * (len(points) - 1))
            segment = min(len(points) - 2, int(segment_float))
            local = segment_float - segment
            first = points[segment]
            second = points[segment + 1]
            if isinstance(first, dict) and isinstance(second, dict):
                translate_x = float(first.get("x_pct", 0)) + (float(second.get("x_pct", 0)) - float(first.get("x_pct", 0))) * local
                translate_y = float(first.get("y_pct", 0)) + (float(second.get("y_pct", 0)) - float(first.get("y_pct", 0))) * local
        scale_to = float(action.get("scale_to", 1))
        scale = 1 + (scale_to - 1) * progress
        if action.get("type") in {"emphasize", "stamp", "pulse"}:
            scale += math.sin(progress * math.pi) * float(action.get("pulse_scale", max(0.04, scale_to - 1)))
        center_x += translate_x
        center_y += translate_y
        width *= scale
        height *= scale
    return (
        center_x - width / 2,
        center_y - height / 2,
        center_x + width / 2,
        center_y + height / 2,
    )


def overlap_pct(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> float:
    width = max(0.0, min(first[2], second[2]) - max(first[0], second[0]))
    height = max(0.0, min(first[3], second[3]) - max(first[1], second[1]))
    intersection = width * height
    first_area = max(0.0, first[2] - first[0]) * max(0.0, first[3] - first[1])
    second_area = max(0.0, second[2] - second[0]) * max(0.0, second[3] - second[1])
    smaller = min(first_area, second_area)
    return 0.0 if smaller <= 0 else intersection / smaller * 100


def gap_pct(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> float:
    horizontal = max(first[0] - second[2], second[0] - first[2], 0.0)
    vertical = max(first[1] - second[3], second[1] - first[3], 0.0)
    return math.hypot(horizontal, vertical)


def validate_layout_geometry(
    composition: dict[str, Any],
    moving: dict[str, dict[str, Any]],
    relative: Path,
    errors: list[str],
) -> None:
    ordered = sorted(moving.items(), key=lambda item: item[1].get("appearance_order", 999))
    points: list[tuple[str, float, float, float, float]] = []
    for slot, entry in ordered:
        occupancy = entry.get("frame_occupancy", {})
        values = [occupancy.get(key) for key in ("anchor_x_pct", "anchor_y_pct", "width_pct", "height_pct")]
        if all(is_number(value) for value in values):
            points.append((slot, *(float(value) for value in values)))
    if len(points) < 3:
        return
    xs = [point[1] for point in points]
    ys = [point[2] for point in points]
    widths = [point[3] for point in points]
    heights = [point[4] for point in points]
    layout = str(composition.get("layout_archetype", ""))
    reading = str(composition.get("reading_path", ""))

    if layout == "asymmetric-stage" and all(abs(x - 50) < 7 for x in xs):
        add_error(errors, f"{relative}: asymmetric-stage needs an off-center focal anchor.")
    elif layout == "diagonal-cascade":
        if max(xs) - min(xs) < 22 or max(ys) - min(ys) < 22:
            add_error(errors, f"{relative}: diagonal-cascade needs at least 22% spread on both axes.")
        else:
            mean_x = sum(xs) / len(xs)
            mean_y = sum(ys) / len(ys)
            covariance = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
            if abs(covariance) < 80:
                add_error(errors, f"{relative}: diagonal-cascade anchors do not form a readable diagonal.")
    elif layout == "split-contrast" and not (min(xs) <= 38 and max(xs) >= 62):
        add_error(errors, f"{relative}: split-contrast needs meaningful subjects on both sides of the frame.")
    elif layout == "radial-cycle":
        quadrants = {(x >= 50, y >= 50) for x, y in zip(xs, ys) if math.hypot(x - 50, y - 50) >= 14}
        if len(quadrants) < 3:
            add_error(errors, f"{relative}: radial-cycle needs moving assets distributed across at least three quadrants.")
    elif layout == "depth-tunnel":
        areas = [width * height for width, height in zip(widths, heights) if width > 0 and height > 0]
        if not areas or max(areas) / min(areas) < 1.7:
            add_error(errors, f"{relative}: depth-tunnel needs a clear near/far scale ratio of at least 1.7.")
    elif layout == "stacked-consequence" and max(ys) - min(ys) < 28:
        add_error(errors, f"{relative}: stacked-consequence needs at least 28% vertical separation.")
    elif layout == "map-route":
        action_types = {str(entry.get("action_motion", {}).get("type", "")) for entry in moving.values()}
        if not action_types.intersection({"path-follow", "draw", "reveal", "highlight", "wipe"}):
            add_error(errors, f"{relative}: map-route needs a path-follow or directional draw/reveal action.")
    elif layout == "full-frame-data":
        data_assets = [entry for entry in moving.values() if entry.get("content_kind") == "editorial-card"]
        if not any(float(entry.get("frame_occupancy", {}).get("width_pct", 0)) >= 55 for entry in data_assets):
            add_error(errors, f"{relative}: full-frame-data needs an editorial-card at least 55% frame width.")

    first_x, first_y = points[0][1], points[0][2]
    last_x, last_y = points[-1][1], points[-1][2]
    if reading == "left-to-right" and last_x < first_x + 8:
        add_error(errors, f"{relative}: appearance order does not implement reading_path=left-to-right.")
    elif reading == "right-to-left" and last_x > first_x - 8:
        add_error(errors, f"{relative}: appearance order does not implement reading_path=right-to-left.")
    elif reading == "top-to-bottom" and last_y < first_y + 8:
        add_error(errors, f"{relative}: appearance order does not implement reading_path=top-to-bottom.")
    elif reading == "bottom-to-top" and last_y > first_y - 8:
        add_error(errors, f"{relative}: appearance order does not implement reading_path=bottom-to-top.")


def validate_manifest(path: Path, project: Path, errors: list[str]) -> None:
    relative = path.relative_to(project)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"{relative}: invalid JSON: {exc}")
        return
    if manifest.get("manifest_version") != CURRENT_ASSET_MANIFEST_VERSION:
        add_error(
            errors,
            f"{relative}: manifest_version must be {CURRENT_ASSET_MANIFEST_VERSION}. Run the Skill migration command before validating this project.",
        )
        return

    if manifest.get("composition_blueprint_locked") is not True:
        add_error(errors, f"{relative}: composition_blueprint_locked must be true before image generation.")

    metaphor = manifest.get("visual_metaphor")
    if not isinstance(metaphor, dict):
        add_error(errors, f"{relative}: visual_metaphor is required.")
    else:
        for field in ("abstract_claim", "concrete_metaphor", "mapping", "motion_payoff"):
            value = str(metaphor.get(field, "")).strip()
            if len(value) < 12 or PLACEHOLDER_RE.search(value):
                add_error(errors, f"{relative}: visual_metaphor.{field} must be concrete.")

    composition = manifest.get("composition")
    if not isinstance(composition, dict):
        add_error(errors, f"{relative}: composition is required.")
    else:
        missing = sorted(COMPOSITION_FIELDS - set(composition))
        if missing:
            add_error(errors, f"{relative}: composition is missing {', '.join(missing)}.")
        for field in COMPOSITION_FIELDS:
            value = str(composition.get(field, "")).strip()
            if not value or PLACEHOLDER_RE.search(value):
                add_error(errors, f"{relative}: composition.{field} must be locked.")
        if composition.get("layout_archetype") not in LAYOUT_ARCHETYPES:
            add_error(errors, f"{relative}: composition.layout_archetype is unsupported.")
        if composition.get("reading_path") not in READING_PATHS:
            add_error(errors, f"{relative}: composition.reading_path is unsupported.")
        if composition.get("dominant_axis") not in DOMINANT_AXES:
            add_error(errors, f"{relative}: composition.dominant_axis is unsupported.")
        if composition.get("foreground_strategy") not in FOREGROUND_STRATEGIES:
            add_error(errors, f"{relative}: composition.foreground_strategy is unsupported.")

    if not str(manifest.get("motion_rhythm", "")).strip() or PLACEHOLDER_RE.search(str(manifest.get("motion_rhythm", ""))):
        add_error(errors, f"{relative}: motion_rhythm must be locked.")
    elif manifest.get("motion_rhythm") not in MOTION_RHYTHMS:
        add_error(errors, f"{relative}: motion_rhythm is unsupported.")

    validate_color_script(manifest.get("color_script"), relative, errors)

    assets = manifest.get("assets", {})
    moving = {
        slot: entry
        for slot, entry in assets.items()
        if slot != "background_plate"
        and isinstance(entry, dict)
        and isinstance(entry.get("appearance_order"), int)
        and entry.get("appearance_order", 0) > 0
    }
    if len(moving) < 3:
        add_error(errors, f"{relative}: plan at least 3 independently moving assets before image generation.")
    boxes: dict[str, tuple[float, float, float, float]] = {}
    for slot, entry in moving.items():
        box = final_box(entry)
        if box is None:
            add_error(errors, f"{relative}: {slot} needs numeric final occupancy and action-end geometry.")
        else:
            boxes[slot] = box
    if isinstance(composition, dict):
        validate_layout_geometry(composition, moving, relative, errors)

    background = manifest.get("background_contract")
    if not isinstance(background, dict):
        add_error(errors, f"{relative}: background_contract is required.")
        background = {}
    if background.get("role") != "stage-only":
        add_error(errors, f"{relative}: background_contract.role must be stage-only.")
    if background.get("max_saliency") not in {"very-low", "low"}:
        add_error(errors, f"{relative}: background max_saliency must be very-low or low.")
    if background.get("semantic_overlap_forbidden") is not True:
        add_error(errors, f"{relative}: semantic_overlap_forbidden must be true.")
    if not isinstance(background.get("allowed_elements"), list) or not background.get("allowed_elements"):
        add_error(errors, f"{relative}: list allowed fixed background elements.")
    forbidden = background.get("forbidden_subjects")
    if not isinstance(forbidden, list) or not forbidden:
        add_error(errors, f"{relative}: list prompt-language forbidden moving-subject aliases.")

    zones = background.get("reserved_zones")
    covered: set[str] = set()
    if not isinstance(zones, list) or not zones:
        add_error(errors, f"{relative}: reserve low-detail background zones for every moving asset.")
        zones = []
    for index, zone in enumerate(zones, start=1):
        if not isinstance(zone, dict):
            add_error(errors, f"{relative}: reserved zone {index} must be an object.")
            continue
        asset_ids = zone.get("asset_ids")
        values = [zone.get(key) for key in ("x_pct", "y_pct", "width_pct", "height_pct")]
        if not isinstance(asset_ids, list) or not asset_ids or not all(is_number(value) for value in values):
            add_error(errors, f"{relative}: reserved zone {index} needs asset IDs and numeric geometry.")
            continue
        if zone.get("background_detail") not in {"none", "very-low"}:
            add_error(errors, f"{relative}: reserved zone {index} background_detail must be none or very-low.")
        center_x, center_y, width, height = values
        zone_box = (center_x - width / 2, center_y - height / 2, center_x + width / 2, center_y + height / 2)
        for asset_id in asset_ids:
            if asset_id not in moving:
                add_error(errors, f"{relative}: reserved zone {index} references unknown asset {asset_id!r}.")
                continue
            covered.add(asset_id)
            box = boxes.get(asset_id)
            if box and (box[0] < zone_box[0] or box[1] < zone_box[1] or box[2] > zone_box[2] or box[3] > zone_box[3]):
                add_error(errors, f"{relative}: reserved zone {index} does not contain {asset_id}'s full final box.")
    uncovered = sorted(set(moving) - covered)
    if uncovered:
        add_error(errors, f"{relative}: reserved zones do not cover {uncovered}.")

    collision = manifest.get("collision_plan")
    if not isinstance(collision, dict):
        add_error(errors, f"{relative}: collision_plan is required.")
        collision = {}
    default_limit = collision.get("default_max_overlap_pct")
    safe_gap = collision.get("safe_gap_pct")
    if not is_number(default_limit) or not 0 <= default_limit <= 20:
        add_error(errors, f"{relative}: default_max_overlap_pct must be 0-20.")
        default_limit = 8
    if not is_number(safe_gap) or not 0 <= safe_gap <= 10:
        add_error(errors, f"{relative}: safe_gap_pct must be 0-10.")
        safe_gap = 3
    if collision.get("motion_paths_reviewed") is not True:
        add_error(errors, f"{relative}: motion_paths_reviewed must be true.")
    allowances: dict[frozenset[str], float] = {}
    raw_allowances = collision.get("allowed_overlaps", [])
    if not isinstance(raw_allowances, list):
        add_error(errors, f"{relative}: allowed_overlaps must be an array.")
        raw_allowances = []
    for allowance in raw_allowances:
        if not isinstance(allowance, dict):
            continue
        first = str(allowance.get("asset_a", ""))
        second = str(allowance.get("asset_b", ""))
        limit = allowance.get("max_overlap_pct")
        reason = str(allowance.get("reason", "")).strip()
        if first not in moving or second not in moving or first == second or not is_number(limit) or len(reason) < 10:
            add_error(errors, f"{relative}: every allowed overlap needs two moving assets, a numeric limit, and a concrete reason.")
            continue
        allowances[frozenset((first, second))] = float(limit)

    box_items = sorted(boxes.items())
    for index, (first_id, first_box) in enumerate(box_items):
        for second_id, second_box in box_items[index + 1 :]:
            pair = frozenset((first_id, second_id))
            overlap = overlap_pct(first_box, second_box)
            limit = allowances.get(pair, float(default_limit))
            if overlap > limit + 0.1:
                add_error(errors, f"{relative}: planned {first_id}/{second_id} overlap is {overlap:.1f}%; limit is {limit:.1f}%.")
            elif overlap <= 0.1 and pair not in allowances:
                gap = gap_pct(first_box, second_box)
                if gap < safe_gap:
                    add_error(errors, f"{relative}: planned {first_id}/{second_id} gap is {gap:.1f}%; minimum is {safe_gap:.1f}%.")
            first_entry = moving[first_id]
            second_entry = moving[second_id]
            for progress in (0.25, 0.5, 0.75):
                first_motion_box = action_box(first_entry, progress)
                second_motion_box = action_box(second_entry, progress)
                if first_motion_box is None or second_motion_box is None:
                    continue
                motion_overlap = overlap_pct(first_motion_box, second_motion_box)
                if motion_overlap > limit + 0.1:
                    add_error(
                        errors,
                        f"{relative}: {first_id}/{second_id} motion corridors overlap {motion_overlap:.1f}% at {progress * 100:.0f}% action progress; limit is {limit:.1f}%.",
                    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate composition blueprints before image generation.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    config_path = project / "project-config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        config = {}
    if config.get("production_mode") == "video-model":
        report = {
            "gate": "Composition blueprint gate",
            "status": "not-applicable",
            "project": str(project),
            "reason": (
                "video-model uses exactly first-frame.png and last-frame.png per Scene. "
                "Do not create ASSETS.json or a Remotion cutout pack."
            ),
            "errors": [],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(0)
    manifests = sorted(project.glob("02_assets/scenes/*/ASSETS.json"))
    errors: list[str] = []
    if not manifests:
        errors.append("No Scene ASSETS.json manifests were found.")
    for manifest in manifests:
        validate_manifest(manifest, project, errors)
    color_signatures: list[tuple[Path, tuple[str, str, bool]]] = []
    for manifest_path in manifests:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if manifest.get("manifest_version") != CURRENT_ASSET_MANIFEST_VERSION:
            continue
        color_script = manifest.get("color_script")
        if not isinstance(color_script, dict):
            continue
        signature = (
            str(color_script.get("dominant_field", "")).strip().casefold(),
            str(color_script.get("focal_accent", "")).strip().casefold(),
            color_script.get("user_palette_override") is True,
        )
        color_signatures.append((manifest_path.relative_to(project), signature))
    for (current_path, current), (next_path, following) in zip(color_signatures, color_signatures[1:]):
        if current[:2] == following[:2] and not current[2] and not following[2]:
            add_error(errors, f"{current_path} and {next_path}: adjacent Scenes may not repeat the same dominant_field/focal_accent pair.")
    report = {
        "gate": "Composition blueprint gate",
        "status": "pass" if not errors else "fail",
        "project": str(project),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 3)


if __name__ == "__main__":
    main()
