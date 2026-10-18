#!/usr/bin/env python3
"""Fail closed when a collage project bypasses gates or fakes generated art provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:  # The gate reports a clear dependency error below.
    Image = None


CURRENT_ASSET_MANIFEST_VERSION = 2
RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
IGNORED_PARTS = {".git", "node_modules", "out", "dist", "build"}
SVG_SOURCE_PATTERNS = {
    "inline <svg>": re.compile(r"<\s*svg\b", re.IGNORECASE),
    "SVG data URI": re.compile(r"data:image/svg\+xml", re.IGNORECASE),
    "programmatic SVG element": re.compile(r"createElement\(\s*['\"]svg['\"]", re.IGNORECASE),
}
PROCEDURAL_RASTER_PATTERNS = {
    "Pillow import": re.compile(r"(?:from\s+PIL\s+import|import\s+PIL)\b", re.IGNORECASE),
    "Pillow drawing API": re.compile(r"\b(?:ImageDraw|Image\.new)\b"),
    "Canvas drawing API": re.compile(r"\b(?:createCanvas|CanvasRenderingContext2D|getContext\(\s*['\"]2d['\"])\b"),
    "OpenCV drawing API": re.compile(r"\bcv2\.(?:rectangle|circle|line|putText|polylines|fillPoly)\s*\("),
    "Cairo drawing API": re.compile(r"\b(?:cairo|cairosvg|svgwrite)\b", re.IGNORECASE),
    "Matplotlib drawing API": re.compile(r"\b(?:matplotlib|pyplot)\b", re.IGNORECASE),
    "ImageMagick drawing command": re.compile(r"\b(?:magick|convert)\b[^\n]*(?:-draw|-annotate)\b", re.IGNORECASE),
}
CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".sh", ".zsh"}
IMAGEGEN_METHODS = {"built-in-image_gen", "imagegen-cli"}
ALLOWED_POSTPROCESS = {
    "none",
    "remove-chroma-key",
    "crop",
    "remove-chroma-key+crop",
    "matte-cleanup",
    "color-correction",
}
SIZING_MODES = {"height-driven", "width-driven", "box-contain"}
CONTENT_KINDS = {
    "background",
    "portrait-subject",
    "wide-group",
    "object-prop",
    "editorial-card",
    "foreground-strip",
    "accent-mark",
}
ACTION_FIELDS = {
    "type",
    "start_pct",
    "end_pct",
    "translate_x_pct",
    "translate_y_pct",
    "scale_to",
    "rotate_deg",
    "easing",
}
ACTION_TYPES = {
    "none",
    "retreat",
    "advance",
    "chase",
    "converge",
    "diverge",
    "replace",
    "reveal",
    "emphasize",
    "stamp",
    "sweep",
    "path-follow",
    "draw",
    "highlight",
    "wipe",
    "pulse",
    "orbit",
    "stack",
    "split",
    "collapse",
    "rise",
    "fall",
    "tip",
    "pull",
}
ACTION_REQUIRED_RE = re.compile(
    r"后撤|退避|撤退|追击|冒进|合围|包围|夹击|落入|取代|替代|击败|溃败|上升|下降|"
    r"\b(?:retreat|withdraw|chase|advance|surround|converge|replace|defeat|rise|fall)\b",
    re.IGNORECASE,
)
SCENE_ACTION_INTENTS = (
    ("retreat", re.compile(r"后撤|退避|撤退|\b(?:retreat|withdraw)\b", re.IGNORECASE), {"retreat"}),
    ("pursuit", re.compile(r"追击|冒进|\b(?:chase|pursue|advance)\b", re.IGNORECASE), {"chase", "advance"}),
    ("convergence", re.compile(r"合围|包围|夹击|\b(?:surround|encircle|converge)\b", re.IGNORECASE), {"converge"}),
    ("replacement", re.compile(r"取代|替代|\b(?:replace|replacement)\b", re.IGNORECASE), {"replace"}),
    ("collapse", re.compile(r"击败|溃败|大败|\b(?:defeat|collapse|rout)\b", re.IGNORECASE), {"diverge", "emphasize", "stamp"}),
    ("rise", re.compile(r"上升|崛起|\b(?:rise|ascend)\b", re.IGNORECASE), {"advance", "reveal", "emphasize"}),
    ("fall", re.compile(r"下降|坠落|\b(?:fall|drop|decline)\b", re.IGNORECASE), {"diverge", "reveal", "emphasize"}),
)
REQUIRED_SCENE_ASSETS = {
    "background_plate",
    "hero_cutout",
}
VISUAL_METAPHOR_FIELDS = {"abstract_claim", "concrete_metaphor", "mapping", "motion_payoff", "asset_ids"}
COMPOSITION_FIELDS = {
    "layout_archetype",
    "reading_path",
    "dominant_axis",
    "foreground_strategy",
    "negative_space_intent",
}
LAYOUT_ARCHETYPES = {
    "asymmetric-stage",
    "diagonal-cascade",
    "split-contrast",
    "radial-cycle",
    "depth-tunnel",
    "stacked-consequence",
    "map-route",
    "full-frame-data",
}
READING_PATHS = {
    "left-to-right",
    "right-to-left",
    "top-to-bottom",
    "bottom-to-top",
    "diagonal-down",
    "diagonal-up",
    "radial-in",
    "radial-out",
    "serpentine",
    "center-out",
}
DOMINANT_AXES = {"horizontal", "vertical", "diagonal", "radial", "depth"}
FOREGROUND_STRATEGIES = {
    "none",
    "corner-occluder",
    "side-frame",
    "lower-band",
    "full-depth-prop",
    "entering-subject",
}
MOTION_RHYTHMS = {
    "sequential-build",
    "cause-then-effect",
    "counter-motion",
    "radial-convergence",
    "path-follow",
    "scale-shift",
    "replacement",
    "cascade",
    "draw-and-land",
}
BACKGROUND_CONTRACT_FIELDS = {
    "role",
    "allowed_elements",
    "forbidden_subjects",
    "max_saliency",
    "semantic_overlap_forbidden",
    "reserved_zones",
    "review",
}
RESERVED_ZONE_FIELDS = {
    "id",
    "asset_ids",
    "x_pct",
    "y_pct",
    "width_pct",
    "height_pct",
    "purpose",
    "background_detail",
}
COLLISION_PLAN_FIELDS = {
    "default_max_overlap_pct",
    "safe_gap_pct",
    "motion_paths_reviewed",
    "allowed_overlaps",
}
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
COLOR_REVIEW_FIELDS = {
    "three_chromatic_hues_present",
    "hero_separates_at_thumbnail",
    "no_muddy_global_cast",
    "palette_match_across_assets",
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
MOTION_FIELDS = {
    "entrance",
    "direction",
    "start_pct",
    "end_pct",
    "travel_pct",
    "settle",
    "hold",
    "exit",
}
OCCUPANCY_FIELDS = {"width_pct", "height_pct", "anchor_x_pct", "anchor_y_pct", "sizing_mode"}
PLACEHOLDER_RE = re.compile(r"\[fill|todo|tbd|unused", re.IGNORECASE)
ALLOWED_ENTRANCES = {
    "cut-or-fade",
    "fade-in",
    "spring-rise",
    "slide-in",
    "rise",
    "pop-in",
    "wipe-on",
    "draw-on",
    "page-place",
    "mask-reveal",
    "unfold",
}
ALLOWED_DIRECTIONS = {
    "none",
    "bottom",
    "top",
    "left",
    "right",
    "side",
    "left-to-right",
    "right-to-left",
    "target-dependent",
}
ALLOWED_SETTLES = {"none", "small-overshoot", "short-settle", "light-settle", "clean-stop", "no-bounce"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_project_files(project: Path):
    for path in project.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        yield path


def add_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def concrete_text(value: Any, minimum: int = 4) -> bool:
    text = str(value).strip()
    return len(text) >= minimum and PLACEHOLDER_RE.search(text) is None


def validate_color_script(
    project: Path,
    manifest_path: Path,
    color_script: Any,
    approved_assets: dict[str, dict[str, Any]],
    errors: list[str],
) -> tuple[str, str, bool] | None:
    label = str(manifest_path.relative_to(project))
    if not isinstance(color_script, dict):
        add_error(errors, f"{label}: color_script is required.")
        return None
    missing = sorted(COLOR_SCRIPT_FIELDS - set(color_script))
    if missing:
        add_error(errors, f"{label}: color_script is missing {', '.join(missing)}.")

    override = color_script.get("user_palette_override") is True
    if color_script.get("style_reference") != "0720-bright-paper" and not override:
        add_error(errors, f"{label}: color_script.style_reference must be 0720-bright-paper by default.")
    if override and not concrete_text(color_script.get("override_reason"), 12):
        add_error(errors, f"{label}: user palette override needs a concrete override_reason.")

    dominant = str(color_script.get("dominant_field", "")).strip()
    supports = color_script.get("support_colors")
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
            add_error(errors, f"{label}: color_script.{field} must name a concrete color and material role.")
    if not override and NEUTRAL_DOMINANT_RE.search(dominant):
        add_error(errors, f"{label}: dominant_field must be chromatic; beige/brown/gray/cream may only support the default palette.")
    if not isinstance(supports, list) or len(supports) < (1 if override else 2) or any(
        not concrete_text(item) for item in (supports if isinstance(supports, list) else [])
    ):
        add_error(errors, f"{label}: color_script.support_colors needs at least two concrete chromatic support colors.")
        supports = []
    normalized_roles = [dominant.casefold(), accent.casefold(), dark.casefold()] + [
        str(item).strip().casefold() for item in supports
    ]
    if len(set(normalized_roles)) != len(normalized_roles):
        add_error(errors, f"{label}: dominant, support, accent, and dark-anchor color roles must be distinct.")

    area = color_script.get("area_budget")
    if not isinstance(area, dict):
        add_error(errors, f"{label}: color_script.area_budget is required.")
        area = {}
    missing_area = sorted(AREA_BUDGET_FIELDS - set(area))
    if missing_area:
        add_error(errors, f"{label}: color_script.area_budget is missing {', '.join(missing_area)}.")
    values = {field: area.get(field) for field in AREA_BUDGET_FIELDS}
    if not all(is_number(value) for value in values.values()):
        add_error(errors, f"{label}: every color_script.area_budget value must be numeric.")
    elif not override:
        limits = {
            "dominant_pct": (35, 60),
            "support_pct": (20, 40),
            "neutral_pct": (5, 25),
            "accent_pct": (3, 15),
            "archival_brown_gray_pct": (0, 20),
        }
        for field, (lower, upper) in limits.items():
            if not lower <= values[field] <= upper:
                add_error(errors, f"{label}: color_script.area_budget.{field} must be {lower}-{upper} by default.")
        planned_total = sum(values[field] for field in ("dominant_pct", "support_pct", "neutral_pct", "accent_pct"))
        if not 95 <= planned_total <= 105:
            add_error(errors, f"{label}: dominant/support/neutral/accent area budget must total about 100, got {planned_total:.1f}.")

    for field in ("hero_background_contrast", "adjacent_scene_shift"):
        if not concrete_text(color_script.get(field), 18):
            add_error(errors, f"{label}: color_script.{field} must state a concrete visual decision.")
    palette_sentence = str(color_script.get("prompt_palette_sentence", "")).strip()
    if not concrete_text(palette_sentence, 50):
        add_error(errors, f"{label}: prompt_palette_sentence must be a concrete reusable palette lock.")
    else:
        palette_folded = palette_sentence.casefold()
        for role in [dominant, accent, dark] + list(supports):
            if role and str(role).casefold() not in palette_folded:
                add_error(errors, f"{label}: prompt_palette_sentence must name palette role {role!r} verbatim.")

    negatives = color_script.get("negative_palette_terms")
    normalized_negatives = {
        str(item).strip().casefold() for item in negatives
    } if isinstance(negatives, list) else set()
    missing_negatives = sorted(REQUIRED_NEGATIVE_PALETTE_TERMS - normalized_negatives)
    if missing_negatives and not override:
        add_error(errors, f"{label}: negative_palette_terms is missing {missing_negatives}.")

    review = color_script.get("review")
    if not isinstance(review, dict):
        add_error(errors, f"{label}: color_script.review is required after inspecting the assembled assets.")
    else:
        for field in COLOR_REVIEW_FIELDS:
            if review.get(field) is not True:
                add_error(errors, f"{label}: color_script.review.{field} must be true before approval.")

    required_prompt_phrases = [palette_sentence] + sorted(normalized_negatives)
    for slot, entry in approved_assets.items():
        if entry.get("source") != "imagegen":
            continue
        prompt_raw = str(entry.get("provenance", {}).get("prompt_file", "")).strip()
        if not prompt_raw:
            continue
        prompt_path = resolve_asset_path(project, prompt_raw)
        if not prompt_path.is_file():
            continue
        prompt_text = prompt_path.read_text(encoding="utf-8", errors="ignore").casefold()
        for phrase in required_prompt_phrases:
            if phrase and phrase.casefold() not in prompt_text:
                add_error(errors, f"{label}: {slot} prompt must include approved palette phrase {phrase!r} verbatim.")
    return dominant.casefold(), accent.casefold(), override


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_motion_contract(
    project: Path,
    manifest_path: Path,
    slot: str,
    entry: dict[str, Any],
    aspect_ratio: str,
    errors: list[str],
) -> None:
    label = f"{manifest_path.relative_to(project)}: {slot}"
    token = str(entry.get("narrative_token", "")).strip()
    appearance_reason = str(entry.get("appearance_reason", "")).strip()
    order = entry.get("appearance_order")
    occupancy = entry.get("frame_occupancy")
    motion = entry.get("motion")
    action = entry.get("action_motion")
    z_index = entry.get("z_index")

    if not token or PLACEHOLDER_RE.search(token):
        add_error(errors, f"{label} needs a concrete narrative_token from the scene content.")
    if not appearance_reason or PLACEHOLDER_RE.search(appearance_reason):
        add_error(errors, f"{label} needs a concrete appearance_reason tied to content order.")
    if not isinstance(z_index, int) or isinstance(z_index, bool) or not 0 <= z_index <= 60:
        add_error(errors, f"{label} needs an integer z_index between 0 and 60.")
    expected_order = 0 if slot == "background_plate" else None
    if not isinstance(order, int) or order < 0:
        add_error(errors, f"{label} needs a non-negative integer appearance_order.")
    elif expected_order is not None and order != expected_order:
        add_error(errors, f"{label} must use appearance_order 0.")

    if not isinstance(occupancy, dict):
        add_error(errors, f"{label} needs frame_occupancy.")
    else:
        missing = sorted(OCCUPANCY_FIELDS - set(occupancy))
        if missing:
            add_error(errors, f"{label} frame_occupancy is missing {', '.join(missing)}.")
        for field in ("width_pct", "height_pct", "anchor_x_pct", "anchor_y_pct"):
            value = occupancy.get(field)
            upper_bound = 115 if field == "width_pct" else 100
            if not is_number(value) or not 0 <= value <= upper_bound:
                add_error(errors, f"{label} frame_occupancy.{field} must be between 0 and {upper_bound}.")

    if not isinstance(motion, dict):
        add_error(errors, f"{label} needs a motion object.")
        return
    missing_motion = sorted(MOTION_FIELDS - set(motion))
    if missing_motion:
        add_error(errors, f"{label} motion is missing {', '.join(missing_motion)}.")
    for field in ("entrance", "direction", "settle", "hold", "exit"):
        value = str(motion.get(field, "")).strip()
        if not value or PLACEHOLDER_RE.search(value):
            add_error(errors, f"{label} motion.{field} must be concrete.")
    if motion.get("entrance") not in ALLOWED_ENTRANCES:
        add_error(errors, f"{label} motion.entrance must use a supported Vox entrance: {sorted(ALLOWED_ENTRANCES)}.")
    if motion.get("direction") not in ALLOWED_DIRECTIONS:
        add_error(errors, f"{label} motion.direction must use a supported direction: {sorted(ALLOWED_DIRECTIONS)}.")
    if motion.get("settle") not in ALLOWED_SETTLES:
        add_error(errors, f"{label} motion.settle must use a supported settle: {sorted(ALLOWED_SETTLES)}.")
    if motion.get("exit") != "hold-to-cut":
        add_error(errors, f"{label} motion.exit must be hold-to-cut so the final composition remains readable.")
    start_pct = motion.get("start_pct")
    end_pct = motion.get("end_pct")
    travel_pct = motion.get("travel_pct")
    if not is_number(start_pct) or not is_number(end_pct) or not 0 <= start_pct < end_pct <= 100:
        add_error(errors, f"{label} needs 0 <= motion.start_pct < motion.end_pct <= 100.")
    if not is_number(travel_pct) or not 0 <= travel_pct <= 25:
        add_error(errors, f"{label} motion.travel_pct must be between 0 and 25.")

    if not isinstance(action, dict):
        add_error(errors, f"{label} needs an action_motion object separate from entrance motion.")
    else:
        missing_action = sorted(ACTION_FIELDS - set(action))
        if missing_action:
            add_error(errors, f"{label} action_motion is missing {', '.join(missing_action)}.")
        action_type = action.get("type")
        if action_type not in ACTION_TYPES:
            add_error(errors, f"{label} action_motion.type must be one of {sorted(ACTION_TYPES)}.")
        if slot != "background_plate" and ACTION_REQUIRED_RE.search(token) and action_type == "none":
            add_error(errors, f"{label} narrates an action and cannot use action_motion.type=none.")
        action_start = action.get("start_pct")
        action_end = action.get("end_pct")
        if action_type == "none":
            if not is_number(action_start) or not is_number(action_end) or action_start != action_end:
                add_error(errors, f"{label} inactive action_motion must use equal numeric start_pct and end_pct.")
        elif (
            not is_number(action_start)
            or not is_number(action_end)
            or not is_number(end_pct)
            or not end_pct - 2 <= action_start < action_end <= 75
        ):
            add_error(errors, f"{label} action motion must begin after entrance and finish by 75%.")
        for field in ("translate_x_pct", "translate_y_pct", "rotate_deg"):
            value = action.get(field)
            if not is_number(value) or not -35 <= value <= 35:
                add_error(errors, f"{label} action_motion.{field} must be between -35 and 35.")
        scale_to = action.get("scale_to")
        if not is_number(scale_to) or not 0.75 <= scale_to <= 1.35:
            add_error(errors, f"{label} action_motion.scale_to must be between 0.75 and 1.35.")
        if action.get("easing") not in {"linear", "ease-in", "ease-out", "ease-in-out", "spring"}:
            add_error(errors, f"{label} action_motion.easing is unsupported.")
        if action_type in {"retreat", "advance", "chase", "converge", "diverge"}:
            x = action.get("translate_x_pct")
            y = action.get("translate_y_pct")
            if is_number(x) and is_number(y) and max(abs(x), abs(y)) < 8:
                add_error(errors, f"{label} action_motion.type={action_type} needs at least 8% directional travel.")
        if action_type in {"emphasize", "stamp", "pulse"} and is_number(scale_to) and abs(scale_to - 1) < 0.04 and not is_number(action.get("pulse_scale")):
            add_error(errors, f"{label} action_motion.type={action_type} needs a scale change of at least 0.04.")
        if action_type == "replace":
            x = action.get("translate_x_pct")
            y = action.get("translate_y_pct")
            if is_number(x) and is_number(y) and is_number(scale_to) and max(abs(x), abs(y)) < 6 and abs(scale_to - 1) < 0.05:
                add_error(errors, f"{label} action_motion.type=replace needs at least 6% travel or a 0.05 scale change.")
        if action_type == "path-follow":
            points = action.get("path_points_pct")
            if not isinstance(points, list) or len(points) < 2:
                add_error(errors, f"{label} action_motion.type=path-follow needs at least two path_points_pct entries.")
            else:
                for index, point in enumerate(points, start=1):
                    if not isinstance(point, dict) or not all(is_number(point.get(axis)) and -35 <= point[axis] <= 35 for axis in ("x_pct", "y_pct")):
                        add_error(errors, f"{label} action_motion.path_points_pct[{index}] needs x_pct/y_pct between -35 and 35.")
        if action_type in {"draw", "highlight", "wipe", "reveal"} and action.get("reveal_direction", "left-to-right") not in {
            "left-to-right",
            "right-to-left",
            "top-to-bottom",
            "bottom-to-top",
        }:
            add_error(errors, f"{label} action_motion.reveal_direction is unsupported.")

    width_pct = occupancy.get("width_pct") if isinstance(occupancy, dict) else None
    height_pct = occupancy.get("height_pct") if isinstance(occupancy, dict) else None
    if slot == "background_plate" and (width_pct != 100 or height_pct != 100):
        add_error(errors, f"{label} must occupy 100% width and 100% height.")
    if slot == "background_plate" and entry.get("content_kind") != "background":
        add_error(errors, f"{label} must use content_kind=background.")
    if slot == "background_plate" and isinstance(occupancy, dict) and occupancy.get("sizing_mode") != "box-contain":
        add_error(errors, f"{label} must use sizing_mode=box-contain.")
    # Slot names describe narrative purpose, not shape. Actual size is validated
    # below from content_kind, sizing_mode, and the raster's visible alpha bounds.


def validate_asset_geometry(
    project: Path,
    manifest_path: Path,
    slot: str,
    entry: dict[str, Any],
    aspect_ratio: str,
    errors: list[str],
) -> None:
    if slot == "background_plate":
        return
    label = f"{manifest_path.relative_to(project)}: {slot}"
    if Image is None:
        add_error(errors, "Pillow is required by the Asset Gate to inspect alpha bounds; it may not be used to draw assets.")
        return
    asset_path = resolve_asset_path(project, str(entry.get("path", "")))
    if not asset_path.is_file():
        return
    try:
        with Image.open(asset_path) as image:
            if "A" not in image.getbands():
                add_error(errors, f"{label} must have an alpha channel after cutout preparation.")
                return
            alpha = image.getchannel("A")
            bbox = alpha.getbbox()
            if bbox is None:
                add_error(errors, f"{label} has no visible alpha content.")
                return
            canvas_w, canvas_h = image.size
    except OSError as exc:
        add_error(errors, f"{label} could not be inspected: {exc}.")
        return

    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]
    bbox_w_ratio = bbox_w / canvas_w
    bbox_h_ratio = bbox_h / canvas_h
    if bbox_w_ratio < 0.72 or bbox_h_ratio < 0.72:
        add_error(
            errors,
            f"{label} needs alpha-tight cropping; visible content covers only {bbox_w_ratio:.1%} x {bbox_h_ratio:.1%} of its canvas.",
        )

    occupancy = entry.get("frame_occupancy", {})
    sizing_mode = occupancy.get("sizing_mode")
    content_kind = entry.get("content_kind")
    if sizing_mode not in SIZING_MODES:
        add_error(errors, f"{label} frame_occupancy.sizing_mode must be one of {sorted(SIZING_MODES)}.")
        return
    if content_kind not in CONTENT_KINDS:
        add_error(errors, f"{label} content_kind must be one of {sorted(CONTENT_KINDS)}.")
        return
    if content_kind == "background":
        add_error(errors, f"{label} cannot use content_kind=background outside background_plate.")
        return
    expected_mode = {
        "portrait-subject": "height-driven",
        "wide-group": "width-driven",
        "object-prop": "box-contain",
        "editorial-card": "width-driven",
        "foreground-strip": "width-driven",
        "accent-mark": "width-driven",
    }.get(content_kind)
    if expected_mode and sizing_mode != expected_mode:
        add_error(errors, f"{label} content_kind={content_kind} requires sizing_mode={expected_mode}.")

    width_pct = occupancy.get("width_pct")
    height_pct = occupancy.get("height_pct")
    anchor_x = occupancy.get("anchor_x_pct")
    anchor_y = occupancy.get("anchor_y_pct")
    if not all(is_number(value) for value in (width_pct, height_pct, anchor_x, anchor_y)):
        return
    frame_w, frame_h = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)
    box_w = frame_w * width_pct / 100
    box_h = frame_h * height_pct / 100
    # The non-driving dimension is a maximum cap in the Remotion component.
    scale = min(box_w / canvas_w, box_h / canvas_h)
    visible_w_pct = bbox_w * scale / frame_w * 100
    visible_h_pct = bbox_h * scale / frame_h * 100

    if aspect_ratio == "16:9":
        minimums = {
            "portrait-subject": (22 if slot == "hero_cutout" else 14, 50 if slot == "hero_cutout" else 28),
            "wide-group": (44 if slot == "hero_cutout" else 30, 20 if slot == "hero_cutout" else 12),
            "object-prop": (26 if slot == "hero_cutout" else 14, 24 if slot == "hero_cutout" else 14),
            "editorial-card": (38 if slot == "hero_cutout" else 32, 22 if slot == "hero_cutout" else 18),
            "foreground-strip": (72, 8),
            "accent-mark": (10, 4),
        }
    else:
        minimums = {
            "portrait-subject": (48 if slot == "hero_cutout" else 26, 30 if slot == "hero_cutout" else 18),
            "wide-group": (68 if slot == "hero_cutout" else 52, 12 if slot == "hero_cutout" else 9),
            "object-prop": (32 if slot == "hero_cutout" else 24, 12),
            "editorial-card": (64, 18),
            "foreground-strip": (86, 7),
            "accent-mark": (18, 3),
        }
    min_w, min_h = minimums[content_kind]
    if visible_w_pct < min_w or visible_h_pct < min_h:
        add_error(
            errors,
            f"{label} renders too small: projected visible occupancy is {visible_w_pct:.1f}% x {visible_h_pct:.1f}%; minimum for {content_kind} is {min_w}% x {min_h}%.",
        )

    overflow = 8 if content_kind == "foreground-strip" else 4

    def exceeds_bounds(center_x: float, center_y: float, width: float, height: float) -> bool:
        return (
            center_x - width / 2 < -overflow
            or center_x + width / 2 > 100 + overflow
            or center_y - height / 2 < -overflow
            or center_y + height / 2 > 100 + overflow
        )

    if exceeds_bounds(anchor_x, anchor_y, visible_w_pct, visible_h_pct):
        add_error(errors, f"{label} exceeds its composition safe bounds at the selected anchor.")

    action = entry.get("action_motion", {})
    if action.get("type") != "none":
        action_x = action.get("translate_x_pct")
        action_y = action.get("translate_y_pct")
        action_scale = action.get("scale_to")
        if all(is_number(value) for value in (action_x, action_y, action_scale)) and exceeds_bounds(
            anchor_x + action_x,
            anchor_y + action_y,
            visible_w_pct * action_scale,
            visible_h_pct * action_scale,
        ):
            add_error(errors, f"{label} exceeds composition safe bounds at the end of action_motion.")


def projected_final_rect(
    project: Path,
    entry: dict[str, Any],
    aspect_ratio: str,
) -> tuple[float, float, float, float] | None:
    """Return the visible final-frame AABB in normalized frame percentages."""
    if Image is None:
        return None
    asset_path = resolve_asset_path(project, str(entry.get("path", "")))
    if not asset_path.is_file():
        return None
    try:
        with Image.open(asset_path) as image:
            if "A" not in image.getbands():
                return None
            bbox = image.getchannel("A").getbbox()
            if bbox is None:
                return None
            canvas_w, canvas_h = image.size
    except OSError:
        return None

    occupancy = entry.get("frame_occupancy", {})
    values = [
        occupancy.get("width_pct"),
        occupancy.get("height_pct"),
        occupancy.get("anchor_x_pct"),
        occupancy.get("anchor_y_pct"),
    ]
    if not all(is_number(value) for value in values):
        return None
    width_pct, height_pct, anchor_x, anchor_y = values
    frame_w, frame_h = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)
    box_w = frame_w * width_pct / 100
    box_h = frame_h * height_pct / 100
    scale = min(box_w / canvas_w, box_h / canvas_h)
    visible_w = (bbox[2] - bbox[0]) * scale / frame_w * 100
    visible_h = (bbox[3] - bbox[1]) * scale / frame_h * 100
    action = entry.get("action_motion", {})
    if action.get("type") != "none":
        translate_x = action.get("translate_x_pct", 0)
        translate_y = action.get("translate_y_pct", 0)
        points = action.get("path_points_pct")
        if isinstance(points, list) and points and isinstance(points[-1], dict):
            translate_x = points[-1].get("x_pct", translate_x)
            translate_y = points[-1].get("y_pct", translate_y)
        action_scale = action.get("scale_to", 1)
        if all(is_number(value) for value in (translate_x, translate_y, action_scale)):
            anchor_x += translate_x
            anchor_y += translate_y
            visible_w *= action_scale
            visible_h *= action_scale
    return (
        anchor_x - visible_w / 2,
        anchor_y - visible_h / 2,
        anchor_x + visible_w / 2,
        anchor_y + visible_h / 2,
    )


def overlap_percent_of_smaller(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> float:
    intersection_w = max(0.0, min(first[2], second[2]) - max(first[0], second[0]))
    intersection_h = max(0.0, min(first[3], second[3]) - max(first[1], second[1]))
    intersection = intersection_w * intersection_h
    first_area = max(0.0, first[2] - first[0]) * max(0.0, first[3] - first[1])
    second_area = max(0.0, second[2] - second[0]) * max(0.0, second[3] - second[1])
    smaller = min(first_area, second_area)
    return 0.0 if smaller <= 0 else intersection / smaller * 100


def rect_gap_percent(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> float:
    horizontal_gap = max(first[0] - second[2], second[0] - first[2], 0.0)
    vertical_gap = max(first[1] - second[3], second[1] - first[3], 0.0)
    return (horizontal_gap**2 + vertical_gap**2) ** 0.5


def validate_gate_state(project: Path, config: dict[str, Any], errors: list[str]) -> None:
    gate0 = config.get("self_check", {})
    if gate0.get("status") != "pass":
        add_error(errors, "Gate 0 is not pass in project-config.json.")
    gate1 = config.get("gate_1", {})
    if gate1.get("status") != "pass":
        add_error(errors, "Gate 1 is missing or not pass in project-config.json.")
    if gate1.get("source") not in {"user-selection", "user-authorized-defaults"}:
        add_error(errors, "Gate 1 source must be user-selection or user-authorized-defaults.")
    locked_values = gate1.get("locked_values", {})
    if locked_values.get("asset_source_policy") != "imagegen-or-user-supplied":
        add_error(errors, "Gate 1 must lock asset_source_policy=imagegen-or-user-supplied.")
    image_policy = config.get("image_generation_policy", {})
    required_policy = {
        "asset_source_policy": "imagegen-or-user-supplied",
        "actual_tool_call_required": True,
        "provenance_required": True,
        "preserve_original_output": True,
        "local_procedural_fallback": False,
    }
    for field, expected in required_policy.items():
        if image_policy.get(field) != expected:
            add_error(errors, f"image_generation_policy.{field} must be {expected!r}.")

    if locked_values.get("audio_mode") == "generate-voiceover":
        delivery = config.get("delivery", {})
        voiceover = config.get("voiceover", {})
        if voiceover.get("provider") != "edge-tts-online":
            add_error(errors, "Generated voiceover must use provider=edge-tts-online.")
        if voiceover.get("voice") != "zh-CN-YunjianNeural":
            add_error(errors, "Generated voiceover must use voice=zh-CN-YunjianNeural.")
        if voiceover.get("timeline_source") != "srt":
            add_error(errors, "Generated voiceover must use the SRT as its timeline source.")

        required_files = {
            "source_audio_file": delivery.get("source_audio_file", ""),
            "subtitle_file": delivery.get("subtitle_file", ""),
            "voiceover_metadata_file": delivery.get("voiceover_metadata_file", ""),
        }
        if config.get("mode") == "vo-sequence":
            required_files["srt_scene_plan_file"] = delivery.get(
                "srt_scene_plan_file", ""
            )
        resolved_files: dict[str, Path] = {}
        for label, raw_path in required_files.items():
            if not raw_path:
                add_error(errors, f"Generated voiceover is missing {label}.")
                continue
            path = resolve_asset_path(project, str(raw_path))
            resolved_files[label] = path
            if not path.is_file() or path.stat().st_size == 0:
                add_error(errors, f"Generated voiceover {label} is missing or empty: {path}")

        metadata_path = resolved_files.get("voiceover_metadata_file")
        if metadata_path and metadata_path.is_file():
            try:
                metadata = load_json(metadata_path)
            except (OSError, json.JSONDecodeError) as exc:
                add_error(errors, f"Voiceover metadata is invalid: {exc}")
            else:
                if metadata.get("voice") != "zh-CN-YunjianNeural":
                    add_error(errors, "Voiceover metadata contains the wrong Edge TTS voice.")
                measured = metadata.get("duration_seconds")
                configured = config.get("total_duration_seconds")
                if not is_number(measured) or measured <= 0:
                    add_error(errors, "Voiceover metadata duration_seconds must be positive.")
                elif not is_number(configured) or abs(float(configured) - float(measured)) > 0.25:
                    add_error(
                        errors,
                        "Whole-video duration must match measured voiceover duration within 0.25 seconds.",
                    )

        beats = config.get("beats", [])
        if not beats or any(beat.get("timing_source") != "srt" for beat in beats):
            add_error(errors, "Every generated-voiceover beat must be timed from the SRT.")

        scene_plan_path = resolved_files.get("srt_scene_plan_file")
        if scene_plan_path and scene_plan_path.is_file():
            try:
                scene_plan = load_json(scene_plan_path)
            except (OSError, json.JSONDecodeError) as exc:
                add_error(errors, f"SRT scene plan is invalid: {exc}")
            else:
                entries = scene_plan.get("scenes", [])
                assigned: list[int] = []
                for entry in entries:
                    cue_start = entry.get("cue_start")
                    cue_end = entry.get("cue_end")
                    if (
                        not isinstance(cue_start, int)
                        or not isinstance(cue_end, int)
                        or cue_start < 1
                        or cue_end < cue_start
                        or not str(entry.get("scene_goal", "")).strip()
                    ):
                        add_error(errors, "Every SRT scene-plan entry needs a valid cue range and scene_goal.")
                        continue
                    assigned.extend(range(cue_start, cue_end + 1))
                if assigned != list(range(1, len(beats) + 1)):
                    add_error(errors, "SRT scene plan must cover every cue exactly once in source order.")


def validate_no_svg(project: Path, errors: list[str]) -> None:
    for path in iter_project_files(project):
        relative = path.relative_to(project)
        if path.suffix.lower() == ".svg":
            add_error(errors, f"SVG asset is forbidden: {relative}")
            continue
        if path.suffix.lower() not in {".ts", ".tsx", ".js", ".jsx", ".css", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SVG_SOURCE_PATTERNS.items():
            if pattern.search(text):
                add_error(errors, f"{label} is forbidden in {relative}")


def validate_no_procedural_asset_generators(project: Path, errors: list[str]) -> None:
    for path in iter_project_files(project):
        if path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        if path.name == "validate_collage_project.py":
            continue
        relative = path.relative_to(project)
        if re.search(r"(?:generate|draw|make|build)[-_]?(?:assets?|images?|art)$", path.stem, re.IGNORECASE):
            add_error(
                errors,
                f"Project-local visible-asset generator is forbidden: {relative}; call the imagegen skill instead.",
            )
        content = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PROCEDURAL_RASTER_PATTERNS.items():
            if pattern.search(content):
                add_error(
                    errors,
                    f"Procedural visible-asset generation is forbidden ({label}) in {relative}; call the imagegen skill instead.",
                )


def validate_asset_provenance(
    project: Path,
    manifest_path: Path,
    slot: str,
    entry: dict[str, Any],
    asset_path: Path,
    errors: list[str],
) -> None:
    label = f"{manifest_path.relative_to(project)}: {slot}"
    source = entry.get("source")
    provenance = entry.get("provenance")
    if not isinstance(provenance, dict):
        add_error(errors, f"{label} needs a provenance object.")
        return

    final_digest = sha256_file(asset_path)
    recorded_final = str(provenance.get("final_sha256", "")).strip().lower()
    if recorded_final != final_digest:
        add_error(errors, f"{label} provenance.final_sha256 does not match the final asset.")

    if source == "imagegen":
        method = provenance.get("method")
        if method not in IMAGEGEN_METHODS:
            add_error(errors, f"{label} provenance.method must be built-in-image_gen or imagegen-cli.")
        if method == "imagegen-cli" and provenance.get("fallback_user_approved") is not True:
            add_error(errors, f"{label} imagegen-cli requires fallback_user_approved=true.")
        if provenance.get("tool_called") is not True:
            add_error(errors, f"{label} must record tool_called=true after an actual imagegen call.")

        receipt = str(provenance.get("result_receipt", "")).strip()
        if len(receipt) < 8 or PLACEHOLDER_RE.search(receipt):
            add_error(errors, f"{label} needs the concrete imagegen result receipt/output hint.")

        prompt_raw = str(provenance.get("prompt_file", "")).strip()
        if Path(prompt_raw).is_absolute() or not prompt_raw.startswith("02_assets/prompts/"):
            add_error(errors, f"{label} provenance.prompt_file must live under 02_assets/prompts/.")
        else:
            prompt_path = resolve_asset_path(project, prompt_raw)
            if not prompt_path.is_file():
                add_error(errors, f"{label} prompt file does not exist: {prompt_raw}.")
            else:
                prompt_text = prompt_path.read_text(encoding="utf-8", errors="ignore").strip()
                if len(prompt_text) < 80 or PLACEHOLDER_RE.search(prompt_text):
                    add_error(errors, f"{label} prompt file must contain a concrete per-asset imagegen prompt.")
                prompt_digest = sha256_file(prompt_path)
                if str(provenance.get("prompt_sha256", "")).strip().lower() != prompt_digest:
                    add_error(errors, f"{label} provenance.prompt_sha256 does not match the prompt file.")

        original_raw = str(provenance.get("original_path", "")).strip()
        if Path(original_raw).is_absolute() or not original_raw.startswith("02_assets/imagegen-originals/"):
            add_error(errors, f"{label} provenance.original_path must live under 02_assets/imagegen-originals/.")
        else:
            original_path = resolve_asset_path(project, original_raw)
            if not original_path.is_file() or original_path.suffix.lower() not in RASTER_EXTENSIONS:
                add_error(errors, f"{label} original imagegen raster does not exist: {original_raw}.")
            else:
                original_digest = sha256_file(original_path)
                if str(provenance.get("original_sha256", "")).strip().lower() != original_digest:
                    add_error(errors, f"{label} provenance.original_sha256 does not match the original imagegen output.")
                if provenance.get("postprocess") == "none" and original_digest != final_digest:
                    add_error(errors, f"{label} changed after imagegen while postprocess is none.")

        if provenance.get("postprocess") not in ALLOWED_POSTPROCESS:
            add_error(errors, f"{label} provenance.postprocess must be one of {sorted(ALLOWED_POSTPROCESS)}.")
    elif source == "user-supplied":
        if provenance.get("method") != "user-supplied":
            add_error(errors, f"{label} user-supplied assets must record provenance.method=user-supplied.")
        original_raw = str(provenance.get("original_path", "")).strip()
        if Path(original_raw).is_absolute() or not original_raw.startswith("02_assets/supplied-originals/"):
            add_error(errors, f"{label} user-supplied original_path must live under 02_assets/supplied-originals/.")
        else:
            original_path = resolve_asset_path(project, original_raw)
            if not original_path.is_file():
                add_error(errors, f"{label} must preserve the supplied original_path inside the project.")
            else:
                original_digest = sha256_file(original_path)
                if str(provenance.get("original_sha256", "")).strip().lower() != original_digest:
                    add_error(errors, f"{label} provenance.original_sha256 does not match the supplied original.")
        if provenance.get("postprocess") not in ALLOWED_POSTPROCESS:
            add_error(errors, f"{label} provenance.postprocess must be one of {sorted(ALLOWED_POSTPROCESS)}.")


def validate_vox_manifest_binding(project: Path, config: dict[str, Any], errors: list[str]) -> None:
    component_path = project / "07_remotion" / "src" / "templates" / "VoxManifestScene.tsx"
    if not component_path.is_file():
        add_error(errors, "VoxManifestScene.tsx is missing; vox-mixed-media must be manifest-driven.")
    else:
        component_source = component_path.read_text(encoding="utf-8", errors="ignore")
        if "<div" in component_source or "createElement(" in component_source or "canvas" in component_source.lower():
            add_error(errors, "VoxManifestScene.tsx may animate Img layers but must not draw visible art with div/createElement/canvas.")
        for required_token in (
            "sizing_mode",
            "content_kind",
            "appearance_order",
            "action_motion",
            "actionType",
            "motion.exit",
            "layout_archetype",
            "reading_path",
            "dominant_axis",
            "foreground_strategy",
            "motion_rhythm",
            "final_hold_start_pct",
            "z_index",
        ):
            if required_token not in component_source:
                add_error(errors, f"VoxManifestScene.tsx must consume manifest field {required_token}.")
    if config.get("mode") != "vo-sequence":
        sequence_path = project / "07_remotion" / "src" / "Sequence.tsx"
        if not sequence_path.is_file():
            add_error(errors, "07_remotion/src/Sequence.tsx is missing.")
            return
        content = sequence_path.read_text(encoding="utf-8", errors="ignore")
        if "ASSETS.json" not in content or "manifest" not in content:
            add_error(errors, "Single-scene Sequence.tsx must read scene-01/ASSETS.json; it may use VoxManifestScene or custom Scene choreography.")
        return
    scene_files = sorted((project / "07_remotion" / "src" / "scenes").glob("Scene*.tsx"))
    if not scene_files:
        add_error(errors, "No Remotion scene components were found under 07_remotion/src/scenes/.")
        return
    for scene_file in scene_files:
        content = scene_file.read_text(encoding="utf-8", errors="ignore")
        relative = scene_file.relative_to(project)
        if "ASSETS.json" not in content or "manifest" not in content:
            add_error(errors, f"{relative} must read its scene ASSETS.json; it may use VoxManifestScene or custom Scene choreography.")


def resolve_asset_path(project: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    return candidate if candidate.is_absolute() else (project / candidate).resolve()


def validate_asset_entry(
    project: Path,
    manifest_path: Path,
    slot: str,
    entry: Any,
    errors: list[str],
) -> None:
    relative_manifest = manifest_path.relative_to(project)
    if not isinstance(entry, dict):
        add_error(errors, f"{relative_manifest}: asset slot {slot} must be an object.")
        return
    raw_path = str(entry.get("path", "")).strip()
    source = entry.get("source")
    approved = entry.get("approved") is True
    if not raw_path:
        add_error(errors, f"{relative_manifest}: required asset {slot} has no path.")
        return
    if Path(raw_path).is_absolute() or not raw_path.startswith("07_remotion/public/"):
        add_error(errors, f"{relative_manifest}: {slot} must be copied under 07_remotion/public/ for staticFile().")
    if source not in {"imagegen", "user-supplied"}:
        add_error(errors, f"{relative_manifest}: {slot} has invalid source {source!r}.")
    if not approved:
        add_error(errors, f"{relative_manifest}: {slot} is not approved.")
    asset_path = resolve_asset_path(project, raw_path)
    if not asset_path.is_file():
        add_error(errors, f"{relative_manifest}: asset file does not exist: {raw_path}")
        return
    if asset_path.suffix.lower() not in RASTER_EXTENSIONS:
        add_error(errors, f"{relative_manifest}: {slot} must be a raster image, got {asset_path.suffix or '<none>'}.")
    if re.fullmatch(r"scene[-_]\d+", asset_path.stem, re.IGNORECASE):
        add_error(errors, f"{relative_manifest}: flattened full-scene image is not valid for slot {slot}: {raw_path}")
    validate_asset_provenance(project, manifest_path, slot, entry, asset_path, errors)


def validate_asset_manifests(project: Path, config: dict[str, Any], errors: list[str]) -> None:
    manifests = sorted(project.glob("02_assets/scenes/*/ASSETS.json"))
    if not manifests:
        add_error(errors, "No per-scene ASSETS.json manifests were found under 02_assets/scenes/.")
        return
    if config.get("mode") == "vo-sequence":
        expected_scenes = config.get("scenes", [])
        if isinstance(expected_scenes, list) and len(manifests) != len(expected_scenes):
            add_error(errors, f"Expected {len(expected_scenes)} scene manifests, found {len(manifests)}.")
    aspect_ratio = str(config.get("delivery", {}).get("aspect_ratio", "16:9"))
    background_policy = str(config.get("background_policy", "per-scene"))
    sharing_authorized = config.get("background_sharing_authorized") is True
    background_paths: dict[str, list[str]] = {}
    background_hashes: dict[str, list[str]] = {}
    background_concepts: dict[str, list[str]] = {}
    manifest_scene_slugs: list[str] = []
    sequence_designs: list[dict[str, str]] = []
    sequence_colors: list[dict[str, str | bool]] = []
    scene_narration: dict[str, str] = {}
    for scene in config.get("scenes", []):
        if not isinstance(scene, dict):
            continue
        slug = str(scene.get("slug", "")).strip()
        narration = " ".join(
            str(beat.get("narration", ""))
            for beat in scene.get("beats", [])
            if isinstance(beat, dict)
        )
        if slug:
            scene_narration[slug] = narration

    if background_policy not in {"per-scene", "shared-continuity"}:
        add_error(errors, f"Unknown background_policy: {background_policy!r}.")
    if background_policy == "shared-continuity" and not sharing_authorized:
        add_error(errors, "shared-continuity requires background_sharing_authorized=true.")

    for manifest_path in manifests:
        try:
            manifest = load_json(manifest_path)
        except (OSError, json.JSONDecodeError) as exc:
            add_error(errors, f"Invalid asset manifest {manifest_path.relative_to(project)}: {exc}")
            continue
        if manifest.get("manifest_version") != CURRENT_ASSET_MANIFEST_VERSION:
            add_error(
                errors,
                f"{manifest_path.relative_to(project)}: manifest_version must be {CURRENT_ASSET_MANIFEST_VERSION}. Run `python3 ~/.codex/skills/paper-collage-video/scripts/migrate_asset_manifests.py --project {project}` once, then review the migrated blueprint.",
            )
            continue
        if manifest.get("status") != "approved":
            add_error(errors, f"{manifest_path.relative_to(project)}: status must be approved.")
        for lock_field in ("composition_blueprint_locked", "content_order_locked", "composition_locked", "motion_plan_locked"):
            if manifest.get(lock_field) is not True:
                add_error(errors, f"{manifest_path.relative_to(project)}: {lock_field} must be true after content review.")
        scene_slug = str(manifest.get("scene_slug", "")).strip()
        if not scene_slug:
            add_error(errors, f"{manifest_path.relative_to(project)}: scene_slug is required.")
        else:
            manifest_scene_slugs.append(scene_slug)
        if manifest.get("background_policy") != background_policy:
            add_error(errors, f"{manifest_path.relative_to(project)}: background_policy must match project-config.json.")
        if background_policy == "shared-continuity" and manifest.get("background_sharing_authorized") is not True:
            add_error(errors, f"{manifest_path.relative_to(project)}: shared background authorization is not recorded.")
        background_concept = str(manifest.get("background_concept", "")).strip()
        distinction_reason = str(manifest.get("background_distinction_reason", "")).strip()
        if not background_concept or PLACEHOLDER_RE.search(background_concept):
            add_error(errors, f"{manifest_path.relative_to(project)}: background_concept must describe this scene's unique environment.")
        if not distinction_reason or PLACEHOLDER_RE.search(distinction_reason):
            add_error(errors, f"{manifest_path.relative_to(project)}: background_distinction_reason must explain how this scene differs.")
        if background_concept:
            normalized_concept = re.sub(r"\s+", " ", background_concept.casefold())
            background_concepts.setdefault(normalized_concept, []).append(str(manifest_path.relative_to(project)))
        assets = manifest.get("assets", {})
        if not isinstance(assets, dict):
            add_error(errors, f"{manifest_path.relative_to(project)}: assets must be an object.")
            continue

        for slot in sorted(REQUIRED_SCENE_ASSETS):
            validate_asset_entry(project, manifest_path, slot, assets.get(slot), errors)

        approved_assets: dict[str, dict[str, Any]] = {}
        for slot, entry in assets.items():
            if not isinstance(entry, dict):
                continue
            raw_path = str(entry.get("path", "")).strip()
            if raw_path and slot not in REQUIRED_SCENE_ASSETS:
                validate_asset_entry(project, manifest_path, slot, entry, errors)
            if raw_path and entry.get("approved") is True:
                approved_assets[slot] = entry
                validate_motion_contract(project, manifest_path, slot, entry, aspect_ratio, errors)
                validate_asset_geometry(project, manifest_path, slot, entry, aspect_ratio, errors)
                if entry.get("source") == "imagegen" and entry.get("generation_batch") != scene_slug:
                    add_error(
                        errors,
                        f"{manifest_path.relative_to(project)}: {slot} generation_batch must equal scene_slug; cross-scene sheets are forbidden.",
                    )

        if not 4 <= len(approved_assets) <= 8:
            add_error(errors, f"{manifest_path.relative_to(project)}: requires 4-8 approved raster assets, found {len(approved_assets)}.")

        moving_assets = {slot: entry for slot, entry in approved_assets.items() if slot != "background_plate"}
        if len(moving_assets) < 3:
            add_error(errors, f"{manifest_path.relative_to(project)}: requires at least 3 independently timed non-background assets.")

        visual_metaphor = manifest.get("visual_metaphor")
        if not isinstance(visual_metaphor, dict):
            add_error(errors, f"{manifest_path.relative_to(project)}: visual_metaphor is required before asset approval.")
            metaphor_asset_ids: list[str] = []
        else:
            missing = sorted(VISUAL_METAPHOR_FIELDS - set(visual_metaphor))
            if missing:
                add_error(errors, f"{manifest_path.relative_to(project)}: visual_metaphor is missing {', '.join(missing)}.")
            for field in ("abstract_claim", "concrete_metaphor", "mapping", "motion_payoff"):
                value = str(visual_metaphor.get(field, "")).strip()
                if not value or PLACEHOLDER_RE.search(value) or len(value) < 12:
                    add_error(errors, f"{manifest_path.relative_to(project)}: visual_metaphor.{field} must be concrete and content-specific.")
            raw_asset_ids = visual_metaphor.get("asset_ids")
            metaphor_asset_ids = raw_asset_ids if isinstance(raw_asset_ids, list) else []
            if not metaphor_asset_ids or any(not isinstance(asset_id, str) for asset_id in metaphor_asset_ids):
                add_error(errors, f"{manifest_path.relative_to(project)}: visual_metaphor.asset_ids must list approved moving asset IDs.")
                metaphor_asset_ids = []
            unresolved = sorted(set(metaphor_asset_ids) - set(moving_assets))
            if unresolved:
                add_error(errors, f"{manifest_path.relative_to(project)}: visual_metaphor.asset_ids are not approved moving assets: {unresolved}.")

        composition = manifest.get("composition")
        if not isinstance(composition, dict):
            add_error(errors, f"{manifest_path.relative_to(project)}: composition is required before asset approval.")
            composition = {}
        else:
            missing = sorted(COMPOSITION_FIELDS - set(composition))
            if missing:
                add_error(errors, f"{manifest_path.relative_to(project)}: composition is missing {', '.join(missing)}.")
        layout_archetype = str(composition.get("layout_archetype", "")).strip()
        reading_path = str(composition.get("reading_path", "")).strip()
        dominant_axis = str(composition.get("dominant_axis", "")).strip()
        foreground_strategy = str(composition.get("foreground_strategy", "")).strip()
        negative_space_intent = str(composition.get("negative_space_intent", "")).strip()
        if layout_archetype not in LAYOUT_ARCHETYPES:
            add_error(errors, f"{manifest_path.relative_to(project)}: composition.layout_archetype must be one of {sorted(LAYOUT_ARCHETYPES)}.")
        if reading_path not in READING_PATHS:
            add_error(errors, f"{manifest_path.relative_to(project)}: composition.reading_path must be one of {sorted(READING_PATHS)}.")
        if dominant_axis not in DOMINANT_AXES:
            add_error(errors, f"{manifest_path.relative_to(project)}: composition.dominant_axis must be one of {sorted(DOMINANT_AXES)}.")
        if foreground_strategy not in FOREGROUND_STRATEGIES:
            add_error(errors, f"{manifest_path.relative_to(project)}: composition.foreground_strategy must be one of {sorted(FOREGROUND_STRATEGIES)}.")
        if not negative_space_intent or PLACEHOLDER_RE.search(negative_space_intent) or len(negative_space_intent) < 12:
            add_error(errors, f"{manifest_path.relative_to(project)}: composition.negative_space_intent must explain a concrete entrance or readability purpose.")

        motion_rhythm = str(manifest.get("motion_rhythm", "")).strip()
        if motion_rhythm not in MOTION_RHYTHMS:
            add_error(errors, f"{manifest_path.relative_to(project)}: motion_rhythm must be one of {sorted(MOTION_RHYTHMS)}.")

        manifest_label = str(manifest_path.relative_to(project))
        color_signature = validate_color_script(
            project,
            manifest_path,
            manifest.get("color_script"),
            approved_assets,
            errors,
        )
        if color_signature is not None:
            sequence_colors.append(
                {
                    "manifest": manifest_label,
                    "dominant": color_signature[0],
                    "accent": color_signature[1],
                    "override": color_signature[2],
                }
            )
        background_contract = manifest.get("background_contract")
        if not isinstance(background_contract, dict):
            add_error(errors, f"{manifest_label}: background_contract is required before image generation.")
            background_contract = {}
        else:
            missing = sorted(BACKGROUND_CONTRACT_FIELDS - set(background_contract))
            if missing:
                add_error(errors, f"{manifest_label}: background_contract is missing {', '.join(missing)}.")
        if background_contract.get("role") != "stage-only":
            add_error(errors, f"{manifest_label}: background_contract.role must be stage-only.")
        allowed_elements = background_contract.get("allowed_elements")
        if not isinstance(allowed_elements, list) or not allowed_elements:
            add_error(errors, f"{manifest_label}: background_contract.allowed_elements must list quiet fixed stage elements.")
        forbidden_subjects = background_contract.get("forbidden_subjects")
        if not isinstance(forbidden_subjects, list) or not forbidden_subjects or any(
            not isinstance(item, str) or not item.strip() for item in forbidden_subjects
        ):
            add_error(errors, f"{manifest_label}: background_contract.forbidden_subjects must list prompt-language aliases for moving subjects.")
            forbidden_subjects = []
        if background_contract.get("max_saliency") not in {"very-low", "low"}:
            add_error(errors, f"{manifest_label}: background_contract.max_saliency must be very-low or low.")
        if background_contract.get("semantic_overlap_forbidden") is not True:
            add_error(errors, f"{manifest_label}: background_contract.semantic_overlap_forbidden must be true.")
        background_review = background_contract.get("review")
        if not isinstance(background_review, dict):
            add_error(errors, f"{manifest_label}: background_contract.review is required after inspecting the generated background.")
        else:
            if background_review.get("reserved_zones_clear") is not True:
                add_error(errors, f"{manifest_label}: background review must confirm reserved_zones_clear=true.")
            if background_review.get("no_duplicate_subjects") is not True:
                add_error(errors, f"{manifest_label}: background review must confirm no_duplicate_subjects=true.")
            if background_review.get("focal_competition") != "pass":
                add_error(errors, f"{manifest_label}: background review focal_competition must be pass.")

        background_entry_for_prompt = approved_assets.get("background_plate", {})
        background_prompt_raw = str(
            background_entry_for_prompt.get("provenance", {}).get("prompt_file", "")
        ).strip()
        background_prompt_text = ""
        if background_prompt_raw:
            background_prompt_path = resolve_asset_path(project, background_prompt_raw)
            if background_prompt_path.is_file():
                background_prompt_text = background_prompt_path.read_text(
                    encoding="utf-8", errors="ignore"
                ).casefold()
        for alias in forbidden_subjects:
            if alias.strip().casefold() not in background_prompt_text:
                add_error(errors, f"{manifest_label}: background prompt must explicitly forbid subject alias {alias!r}.")

        reserved_zones = background_contract.get("reserved_zones")
        covered_assets: set[str] = set()
        final_rects = {
            slot: rect
            for slot, entry in moving_assets.items()
            if (rect := projected_final_rect(project, entry, aspect_ratio)) is not None
        }
        if not isinstance(reserved_zones, list) or not reserved_zones:
            add_error(errors, f"{manifest_label}: background_contract.reserved_zones must reserve every moving asset landing area.")
            reserved_zones = []
        for index, zone in enumerate(reserved_zones, start=1):
            zone_label = f"{manifest_label}: reserved_zones[{index}]"
            if not isinstance(zone, dict):
                add_error(errors, f"{zone_label} must be an object.")
                continue
            missing = sorted(RESERVED_ZONE_FIELDS - set(zone))
            if missing:
                add_error(errors, f"{zone_label} is missing {', '.join(missing)}.")
            zone_assets = zone.get("asset_ids")
            if not isinstance(zone_assets, list) or not zone_assets:
                add_error(errors, f"{zone_label}.asset_ids must list the moving assets protected by this zone.")
                continue
            unknown_assets = sorted(set(zone_assets) - set(moving_assets))
            if unknown_assets:
                add_error(errors, f"{zone_label} references unknown moving assets: {unknown_assets}.")
            covered_assets.update(asset_id for asset_id in zone_assets if asset_id in moving_assets)
            zone_values = [zone.get(field) for field in ("x_pct", "y_pct", "width_pct", "height_pct")]
            if not all(is_number(value) for value in zone_values):
                add_error(errors, f"{zone_label} needs numeric x/y/width/height percentages.")
                continue
            zone_x, zone_y, zone_w, zone_h = zone_values
            if not 0 < zone_w <= 110 or not 0 < zone_h <= 110 or not 0 <= zone_x <= 100 or not 0 <= zone_y <= 100:
                add_error(errors, f"{zone_label} percentages are outside supported bounds.")
                continue
            if zone.get("background_detail") not in {"none", "very-low"}:
                add_error(errors, f"{zone_label}.background_detail must be none or very-low.")
            purpose = str(zone.get("purpose", "")).strip()
            if len(purpose) < 10 or PLACEHOLDER_RE.search(purpose):
                add_error(errors, f"{zone_label}.purpose must explain the protected landing or motion corridor.")
            zone_rect = (
                zone_x - zone_w / 2,
                zone_y - zone_h / 2,
                zone_x + zone_w / 2,
                zone_y + zone_h / 2,
            )
            for asset_id in zone_assets:
                rect = final_rects.get(asset_id)
                if rect and (
                    rect[0] < zone_rect[0] - 1
                    or rect[1] < zone_rect[1] - 1
                    or rect[2] > zone_rect[2] + 1
                    or rect[3] > zone_rect[3] + 1
                ):
                    add_error(errors, f"{zone_label} does not fully protect the final visible bounds of {asset_id}.")
        uncovered_assets = sorted(set(moving_assets) - covered_assets)
        if uncovered_assets:
            add_error(errors, f"{manifest_label}: reserved_zones do not cover moving assets {uncovered_assets}.")

        collision_plan = manifest.get("collision_plan")
        if not isinstance(collision_plan, dict):
            add_error(errors, f"{manifest_label}: collision_plan is required before image generation.")
            collision_plan = {}
        else:
            missing = sorted(COLLISION_PLAN_FIELDS - set(collision_plan))
            if missing:
                add_error(errors, f"{manifest_label}: collision_plan is missing {', '.join(missing)}.")
        default_max_overlap = collision_plan.get("default_max_overlap_pct")
        if not is_number(default_max_overlap) or not 0 <= default_max_overlap <= 20:
            add_error(errors, f"{manifest_label}: collision_plan.default_max_overlap_pct must be between 0 and 20.")
            default_max_overlap = 8
        safe_gap = collision_plan.get("safe_gap_pct")
        if not is_number(safe_gap) or not 0 <= safe_gap <= 10:
            add_error(errors, f"{manifest_label}: collision_plan.safe_gap_pct must be between 0 and 10.")
        if collision_plan.get("motion_paths_reviewed") is not True:
            add_error(errors, f"{manifest_label}: collision_plan.motion_paths_reviewed must be true before approval.")
        allowed_overlaps = collision_plan.get("allowed_overlaps")
        if not isinstance(allowed_overlaps, list):
            add_error(errors, f"{manifest_label}: collision_plan.allowed_overlaps must be an array.")
            allowed_overlaps = []
        overlap_limits: dict[frozenset[str], float] = {}
        for index, allowance in enumerate(allowed_overlaps, start=1):
            allowance_label = f"{manifest_label}: allowed_overlaps[{index}]"
            if not isinstance(allowance, dict):
                add_error(errors, f"{allowance_label} must be an object.")
                continue
            first_id = str(allowance.get("asset_a", "")).strip()
            second_id = str(allowance.get("asset_b", "")).strip()
            limit = allowance.get("max_overlap_pct")
            reason = str(allowance.get("reason", "")).strip()
            if first_id == second_id or first_id not in moving_assets or second_id not in moving_assets:
                add_error(errors, f"{allowance_label} must name two different approved moving assets.")
                continue
            if not is_number(limit) or not 0 <= limit <= 70:
                add_error(errors, f"{allowance_label}.max_overlap_pct must be between 0 and 70.")
                continue
            if len(reason) < 10 or PLACEHOLDER_RE.search(reason):
                add_error(errors, f"{allowance_label}.reason must explain the semantic occlusion.")
            overlap_limits[frozenset((first_id, second_id))] = float(limit)

        rect_items = sorted(final_rects.items())
        for index, (first_id, first_rect) in enumerate(rect_items):
            for second_id, second_rect in rect_items[index + 1 :]:
                overlap = overlap_percent_of_smaller(first_rect, second_rect)
                limit = overlap_limits.get(
                    frozenset((first_id, second_id)), float(default_max_overlap)
                )
                if overlap > limit + 0.1:
                    add_error(
                        errors,
                        f"{manifest_label}: {first_id} and {second_id} overlap {overlap:.1f}% of the smaller final visible box; limit is {limit:.1f}%. Reposition them or add an intentional overlap allowance.",
                    )
                elif (
                    overlap <= 0.1
                    and frozenset((first_id, second_id)) not in overlap_limits
                    and is_number(safe_gap)
                ):
                    gap = rect_gap_percent(first_rect, second_rect)
                    if gap < safe_gap:
                        add_error(
                            errors,
                            f"{manifest_label}: {first_id} and {second_id} have only {gap:.1f}% frame gap; collision_plan.safe_gap_pct is {safe_gap:.1f}%. Increase spacing or document intentional contact.",
                        )

        def anchor_zone(entry: dict[str, Any]) -> str:
            occupancy = entry.get("frame_occupancy", {})
            x = occupancy.get("anchor_x_pct")
            y = occupancy.get("anchor_y_pct")
            if not is_number(x) or not is_number(y):
                return "unknown"
            horizontal_zone = "left" if x < 38 else "right" if x > 62 else "center"
            vertical_zone = "top" if y < 38 else "bottom" if y > 70 else "middle"
            return f"{horizontal_zone}-{vertical_zone}"

        anchor_signature = ",".join(
            anchor_zone(entry)
            for _, entry in sorted(
                moving_assets.items(),
                key=lambda item: item[1].get("appearance_order", 999),
            )
        )
        sequence_designs.append(
            {
                "manifest": str(manifest_path.relative_to(project)),
                "layout": layout_archetype,
                "reading_path": reading_path,
                "axis": dominant_axis,
                "foreground": foreground_strategy,
                "rhythm": motion_rhythm,
                "signature": f"{layout_archetype}|{reading_path}|{dominant_axis}|{foreground_strategy}|{anchor_signature}",
            }
        )

        active_action_types = {
            str(entry.get("action_motion", {}).get("type", "none"))
            for entry in moving_assets.values()
        }
        narration = scene_narration.get(scene_slug, "")
        for intent_name, pattern, allowed_types in SCENE_ACTION_INTENTS:
            if pattern.search(narration) and not active_action_types.intersection(allowed_types):
                add_error(
                    errors,
                    f"{manifest_path.relative_to(project)}: narration requires {intent_name} action motion using one of {sorted(allowed_types)}.",
                )

        ordered_assets: list[tuple[int, str, dict[str, Any]]] = []
        for slot, entry in moving_assets.items():
            order = entry.get("appearance_order")
            if isinstance(order, int):
                ordered_assets.append((order, slot, entry))
        ordered_assets.sort(key=lambda item: item[0])
        orders = [item[0] for item in ordered_assets]
        expected_orders = list(range(1, len(moving_assets) + 1))
        if orders != expected_orders:
            add_error(errors, f"{manifest_path.relative_to(project)}: appearance_order must be unique and contiguous: {expected_orders}.")

        ordered_slots = [item[1] for item in ordered_assets]
        narrative_sequence = manifest.get("narrative_sequence")
        if narrative_sequence != ordered_slots:
            add_error(
                errors,
                f"{manifest_path.relative_to(project)}: narrative_sequence must exactly match appearance_order: {ordered_slots}.",
            )

        start_values = [item[2].get("motion", {}).get("start_pct") for item in ordered_assets]
        if len(start_values) >= 2 and (
            not all(is_number(value) for value in start_values)
            or any(current >= following for current, following in zip(start_values, start_values[1:]))
        ):
            add_error(errors, f"{manifest_path.relative_to(project)}: motion.start_pct must strictly increase in narrative order.")

        final_hold_start = manifest.get("final_hold_start_pct")
        if not is_number(final_hold_start) or not 65 <= final_hold_start <= 75:
            add_error(errors, f"{manifest_path.relative_to(project)}: final_hold_start_pct must be between 65 and 75.")
        elif any(
            not is_number(entry.get("motion", {}).get("end_pct"))
            or entry.get("motion", {}).get("end_pct") > final_hold_start
            or not is_number(entry.get("action_motion", {}).get("end_pct"))
            or entry.get("action_motion", {}).get("end_pct") > final_hold_start
            for entry in moving_assets.values()
        ):
            add_error(errors, f"{manifest_path.relative_to(project)}: all entrance and action motion must finish by final_hold_start_pct.")

        dominant_motion_asset = manifest.get("dominant_motion_asset")
        if dominant_motion_asset not in moving_assets:
            add_error(errors, f"{manifest_path.relative_to(project)}: dominant_motion_asset must name one approved moving asset.")
        elif metaphor_asset_ids and dominant_motion_asset not in metaphor_asset_ids:
            add_error(errors, f"{manifest_path.relative_to(project)}: dominant_motion_asset must perform the visual metaphor and appear in visual_metaphor.asset_ids.")

        background_entry = approved_assets.get("background_plate")
        if isinstance(background_entry, dict):
            raw_background = str(background_entry.get("path", "")).strip()
            if raw_background:
                background_file = resolve_asset_path(project, raw_background)
                resolved = str(background_file)
                background_paths.setdefault(resolved, []).append(str(manifest_path.relative_to(project)))
                if background_file.is_file():
                    digest = hashlib.sha256(background_file.read_bytes()).hexdigest()
                    background_hashes.setdefault(digest, []).append(str(manifest_path.relative_to(project)))

    if background_policy == "per-scene":
        for path, owners in background_paths.items():
            if len(owners) > 1:
                add_error(errors, f"Background path is reused under per-scene policy: {path} in {', '.join(owners)}.")
        for digest, owners in background_hashes.items():
            if len(owners) > 1:
                add_error(errors, f"Identical background image content is reused in {', '.join(owners)} (sha256 {digest[:12]}).")
        for concept, owners in background_concepts.items():
            if len(owners) > 1:
                add_error(errors, f"Background concept is repeated under per-scene policy: {concept!r} in {', '.join(owners)}.")

    for current, following in zip(sequence_designs, sequence_designs[1:]):
        if current["layout"] and current["layout"] == following["layout"]:
            add_error(errors, f"Adjacent Scenes repeat layout_archetype={current['layout']}: {current['manifest']} and {following['manifest']}.")
        if current["signature"] == following["signature"]:
            add_error(errors, f"Adjacent Scenes repeat the same composition signature: {current['manifest']} and {following['manifest']}.")
        if current["foreground"] == "lower-band" and following["foreground"] == "lower-band":
            add_error(errors, f"Adjacent Scenes may not both use foreground_strategy=lower-band: {current['manifest']} and {following['manifest']}.")

    for current, following in zip(sequence_colors, sequence_colors[1:]):
        if (
            current["dominant"] == following["dominant"]
            and current["accent"] == following["accent"]
            and current["override"] is not True
            and following["override"] is not True
        ):
            add_error(
                errors,
                f"Adjacent Scenes repeat the same dominant_field/focal_accent pair: {current['manifest']} and {following['manifest']}.",
            )

    if len(sequence_designs) >= 4:
        layout_count = len({item["layout"] for item in sequence_designs if item["layout"]})
        rhythm_count = len({item["rhythm"] for item in sequence_designs if item["rhythm"]})
        if layout_count < 3:
            add_error(errors, f"A {len(sequence_designs)}-Scene sequence needs at least 3 layout archetypes; found {layout_count}.")
        if rhythm_count < 3:
            add_error(errors, f"A {len(sequence_designs)}-Scene sequence needs at least 3 motion rhythms; found {rhythm_count}.")
        lower_band_count = sum(item["foreground"] == "lower-band" for item in sequence_designs)
        lower_band_limit = (len(sequence_designs) + 2) // 3
        if lower_band_count > lower_band_limit:
            add_error(errors, f"foreground_strategy=lower-band may appear in at most {lower_band_limit} of {len(sequence_designs)} Scenes; found {lower_band_count}.")

        signatures: dict[str, list[str]] = {}
        for item in sequence_designs:
            signatures.setdefault(item["signature"], []).append(item["manifest"])
        for signature, owners in signatures.items():
            if len(owners) > 1:
                add_error(errors, f"Composition signature is repeated across Scenes: {signature!r} in {', '.join(owners)}.")

    if config.get("mode") == "vo-sequence" and isinstance(config.get("scenes"), list):
        expected_slugs = [str(scene.get("slug", "")) for scene in config["scenes"] if isinstance(scene, dict)]
        if sorted(manifest_scene_slugs) != sorted(expected_slugs):
            add_error(errors, f"Scene manifest slugs must match project scenes: {expected_slugs}.")


def validate_manifest_versions(project: Path, errors: list[str]) -> bool:
    manifests = sorted(project.glob("02_assets/scenes/*/ASSETS.json"))
    if not manifests:
        return True
    current = True
    for manifest_path in manifests:
        try:
            manifest = load_json(manifest_path)
        except (OSError, json.JSONDecodeError):
            continue
        if manifest.get("manifest_version") != CURRENT_ASSET_MANIFEST_VERSION:
            current = False
            add_error(
                errors,
                f"{manifest_path.relative_to(project)}: manifest_version must be {CURRENT_ASSET_MANIFEST_VERSION}. Run `python3 ~/.codex/skills/paper-collage-video/scripts/migrate_asset_manifests.py --project {project}` once, then review the migrated blueprint.",
            )
    return current


def validate_project(project: Path) -> dict[str, Any]:
    errors: list[str] = []
    config_path = project / "project-config.json"
    if not config_path.is_file():
        add_error(errors, "project-config.json is missing.")
        config: dict[str, Any] = {}
    else:
        try:
            config = load_json(config_path)
        except (OSError, json.JSONDecodeError) as exc:
            add_error(errors, f"project-config.json is invalid: {exc}")
            config = {}

    validate_gate_state(project, config, errors)
    validate_no_svg(project, errors)
    validate_no_procedural_asset_generators(project, errors)
    if config.get("production_mode") == "remotion-code":
        if validate_manifest_versions(project, errors):
            validate_asset_manifests(project, config, errors)
            if config.get("style_family") == "vox-mixed-media":
                validate_vox_manifest_binding(project, config, errors)

    return {
        "gate": "Asset gate",
        "status": "pass" if not errors else "fail",
        "project": str(project),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a paper collage video project before preview or render.")
    parser.add_argument("--project", required=True, help="Project root containing project-config.json")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    report = validate_project(project)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 3)


if __name__ == "__main__":
    main()
