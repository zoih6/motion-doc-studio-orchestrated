#!/usr/bin/env python3
"""Fail closed when a Seedance last frame was not edited from its first frame."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageChops, ImageDraw, ImageStat
except ImportError:  # pragma: no cover - reported as a gate error below.
    Image = ImageChops = ImageDraw = ImageStat = None

from runtime_support import find_project_root, find_scene_spec, load_json, resolve_path


REVIEW_FIELDS = {
    "same_canvas_and_crop",
    "background_geometry_match",
    "fixed_objects_match",
    "no_background_regeneration",
}
REGION_FIELDS = {"id", "x_pct", "y_pct", "width_pct", "height_pct", "purpose"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame_by_role(spec: dict[str, Any], role: str) -> dict[str, Any] | None:
    for frame in spec.get("frames", []):
        if isinstance(frame, dict) and frame.get("role") == role:
            return frame
    return None


def normalized_paths(project: Path, values: Any) -> list[Path]:
    if not isinstance(values, list):
        return []
    return [resolve_path(project, str(value)) for value in values if str(value).strip()]


def continuity_metrics(
    first_path: Path,
    last_path: Path,
    regions: list[dict[str, Any]],
) -> dict[str, float]:
    if Image is None or ImageChops is None or ImageDraw is None or ImageStat is None:
        raise RuntimeError("Pillow is required for the Keyframe continuity gate.")
    with Image.open(first_path) as first_source, Image.open(last_path) as last_source:
        first = first_source.convert("RGB")
        last = last_source.convert("RGB")
    if first.size != last.size:
        raise RuntimeError(f"First/last dimensions differ: {first.size} vs {last.size}.")

    width, height = first.size
    changed_mask = Image.new("L", first.size, 0)
    draw = ImageDraw.Draw(changed_mask)
    for region in regions:
        center_x = float(region["x_pct"]) / 100 * width
        center_y = float(region["y_pct"]) / 100 * height
        region_width = float(region["width_pct"]) / 100 * width
        region_height = float(region["height_pct"]) / 100 * height
        draw.rectangle(
            (
                round(center_x - region_width / 2),
                round(center_y - region_height / 2),
                round(center_x + region_width / 2),
                round(center_y + region_height / 2),
            ),
            fill=255,
        )
    protected_mask = ImageChops.invert(changed_mask)
    changed_pixels = changed_mask.histogram()[255]
    protected_pixels = protected_mask.histogram()[255]
    if protected_pixels <= 0:
        raise RuntimeError("Change regions cover the entire frame; no background remains to validate.")

    difference = ImageChops.difference(first, last)
    means = ImageStat.Stat(difference, protected_mask).mean
    normalized_mae = sum(means) / len(means) / 255
    gray_difference = difference.convert("L")
    protected_difference = Image.composite(
        gray_difference,
        Image.new("L", first.size, 0),
        protected_mask,
    )
    histogram = protected_difference.histogram()
    significant_threshold = round(255 * 0.12)
    significant_pixels = sum(histogram[significant_threshold + 1 :])
    return {
        "change_region_coverage_pct": changed_pixels / (width * height) * 100,
        "outside_region_mae": normalized_mae,
        "outside_region_significant_change_pct": significant_pixels / protected_pixels * 100,
    }


def validate_keyframe_continuity(
    project: Path,
    spec: dict[str, Any],
    *,
    spec_path: Path | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    label = str(spec_path.relative_to(project)) if spec_path and spec_path.is_relative_to(project) else str(spec_path or "SEEDANCE_SCENE.json")
    first_frame = frame_by_role(spec, "first_frame")
    last_frame = frame_by_role(spec, "last_frame")
    if first_frame is None or last_frame is None:
        errors.append(f"{label}: frames must contain first_frame and last_frame roles.")
        return {"gate": "Keyframe continuity gate", "status": "fail", "errors": errors, "metrics": {}}

    first_path = resolve_path(project, str(first_frame.get("path", "")))
    last_path = resolve_path(project, str(last_frame.get("path", "")))
    if not first_path.is_file():
        errors.append(f"{label}: first-frame file is missing: {first_path}")
    if not last_path.is_file():
        errors.append(f"{label}: last-frame file is missing: {last_path}")

    dimensions_match = False
    if first_path.is_file() and last_path.is_file() and Image is not None:
        with Image.open(first_path) as first_image, Image.open(last_path) as last_image:
            first_size = first_image.size
            last_size = last_image.size
        dimensions_match = first_size == last_size
        if not dimensions_match:
            errors.append(f"{label}: first/last canvas dimensions must match exactly, got {first_size} and {last_size}.")
        expected_ratio = str(spec.get("resolution", {}).get("aspect_ratio", "")).strip()
        canvas_contract = spec.get("keyframe_generation_contract", {}).get("canvas", {})
        expected_width = canvas_contract.get("width") or spec.get("resolution", {}).get("width")
        expected_height = canvas_contract.get("height") or spec.get("resolution", {}).get("height")
        if isinstance(expected_width, int) and isinstance(expected_height, int):
            for role, size in (("first-frame", first_size), ("last-frame", last_size)):
                if size != (expected_width, expected_height):
                    errors.append(
                        f"{label}: {role} dimensions {size} do not match the Gate 1 canonical canvas "
                        f"{expected_width}x{expected_height}."
                    )
        if ":" in expected_ratio:
            try:
                ratio_width, ratio_height = (float(part) for part in expected_ratio.split(":", 1))
                target_ratio = ratio_width / ratio_height
            except (TypeError, ValueError, ZeroDivisionError):
                errors.append(f"{label}: resolution.aspect_ratio is invalid: {expected_ratio!r}.")
            else:
                for role, size in (("first-frame", first_size), ("last-frame", last_size)):
                    if abs(size[0] / size[1] - target_ratio) > 0.01:
                        errors.append(f"{label}: {role} dimensions {size} do not match required aspect ratio {expected_ratio}.")

    contract = spec.get("keyframe_generation_contract")
    if not isinstance(contract, dict):
        errors.append(f"{label}: keyframe_generation_contract is required.")
        contract = {}
    first_generation = contract.get("first_frame")
    last_generation = contract.get("last_frame")
    review = contract.get("continuity_review")
    if not isinstance(first_generation, dict):
        errors.append(f"{label}: keyframe_generation_contract.first_frame is required.")
        first_generation = {}
    if not isinstance(last_generation, dict):
        errors.append(f"{label}: keyframe_generation_contract.last_frame is required.")
        last_generation = {}

    if first_generation.get("mode") != "generate" or first_generation.get("source") != "imagegen":
        errors.append(f"{label}: first_frame must use source=imagegen and mode=generate.")
    if first_generation.get("execution_method") != "built-in-image_gen-generate":
        errors.append(f"{label}: first_frame.execution_method must be built-in-image_gen-generate.")
    if first_generation.get("tool_called") is not True:
        errors.append(f"{label}: first_frame.tool_called must be true.")
    if last_generation.get("mode") != "edit" or last_generation.get("source") != "imagegen":
        errors.append(f"{label}: last_frame must use source=imagegen and mode=edit, never an independent generation.")
    if last_generation.get("execution_method") != "built-in-image_gen-edit":
        errors.append(f"{label}: last_frame.execution_method must be built-in-image_gen-edit.")
    if last_generation.get("tool_called") is not True:
        errors.append(f"{label}: last_frame.tool_called must be true.")
    if last_generation.get("edit_target_role") != "first_frame":
        errors.append(f"{label}: last_frame.edit_target_role must be first_frame.")
    if last_generation.get("preserve_outside_change_regions") is not True:
        errors.append(f"{label}: last_frame.preserve_outside_change_regions must be true.")

    for generation_label, generation in (("first_frame", first_generation), ("last_frame", last_generation)):
        for field in ("prompt_file", "result_receipt", "output_sha256"):
            value = str(generation.get(field, "")).strip()
            if not value:
                errors.append(f"{label}: {generation_label}.{field} is required.")
        prompt_file = str(generation.get("prompt_file", "")).strip()
        if prompt_file and not resolve_path(project, prompt_file).is_file():
            errors.append(f"{label}: {generation_label}.prompt_file does not exist: {prompt_file}")

    if first_path.is_file():
        first_digest = sha256_file(first_path)
        if str(first_generation.get("output_sha256", "")).lower() != first_digest:
            errors.append(f"{label}: first_frame.output_sha256 does not match first-frame.png.")
        edit_target = resolve_path(project, str(last_generation.get("edit_target_path", "")))
        if edit_target != first_path:
            errors.append(f"{label}: last_frame.edit_target_path must resolve to the exact first-frame path.")
        if str(last_generation.get("edit_target_sha256", "")).lower() != first_digest:
            errors.append(f"{label}: last_frame.edit_target_sha256 must match the exact first-frame bytes used for editing.")
        references = normalized_paths(project, last_generation.get("referenced_image_paths"))
        if references != [first_path]:
            errors.append(f"{label}: last_frame.referenced_image_paths must contain only the exact first-frame path.")
    if last_path.is_file() and str(last_generation.get("output_sha256", "")).lower() != sha256_file(last_path):
        errors.append(f"{label}: last_frame.output_sha256 does not match last-frame.png.")

    regions = last_generation.get("change_regions")
    if not isinstance(regions, list) or not regions:
        errors.append(f"{label}: last_frame.change_regions must list every allowed addition zone.")
        regions = []
    valid_regions: list[dict[str, Any]] = []
    for index, region in enumerate(regions, start=1):
        if not isinstance(region, dict):
            errors.append(f"{label}: change_regions[{index}] must be an object.")
            continue
        missing = sorted(REGION_FIELDS - set(region))
        if missing:
            errors.append(f"{label}: change_regions[{index}] is missing {', '.join(missing)}.")
            continue
        values = [region.get(field) for field in ("x_pct", "y_pct", "width_pct", "height_pct")]
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            errors.append(f"{label}: change_regions[{index}] geometry must be numeric.")
            continue
        x, y, width, height = values
        if not 0 <= x <= 100 or not 0 <= y <= 100 or not 0 < width <= 100 or not 0 < height <= 100:
            errors.append(f"{label}: change_regions[{index}] geometry is outside 0-100 percent bounds.")
            continue
        if len(str(region.get("purpose", "")).strip()) < 10:
            errors.append(f"{label}: change_regions[{index}].purpose must name the approved added element.")
            continue
        valid_regions.append(region)

    if not isinstance(review, dict):
        errors.append(f"{label}: keyframe_generation_contract.continuity_review is required.")
    else:
        for field in REVIEW_FIELDS:
            if review.get(field) is not True:
                errors.append(f"{label}: continuity_review.{field} must be true after viewing both frames.")

    max_mae = contract.get("max_outside_region_mae", 0.06)
    max_significant = contract.get("max_outside_significant_change_pct", 12)
    if not isinstance(max_mae, (int, float)) or isinstance(max_mae, bool) or not 0 < max_mae <= 0.08:
        errors.append(f"{label}: max_outside_region_mae must be greater than 0 and at most 0.08.")
        max_mae = 0.06
    if not isinstance(max_significant, (int, float)) or isinstance(max_significant, bool) or not 0 < max_significant <= 15:
        errors.append(f"{label}: max_outside_significant_change_pct must be greater than 0 and at most 15.")
        max_significant = 12

    metrics: dict[str, float] = {}
    if first_path.is_file() and last_path.is_file() and dimensions_match and valid_regions:
        try:
            metrics = continuity_metrics(first_path, last_path, valid_regions)
        except RuntimeError as exc:
            errors.append(f"{label}: {exc}")
        else:
            if metrics["change_region_coverage_pct"] > 65:
                errors.append(f"{label}: change regions cover {metrics['change_region_coverage_pct']:.1f}% of the frame; maximum is 65%.")
            if metrics["outside_region_mae"] > float(max_mae):
                errors.append(
                    f"{label}: background outside change regions has MAE {metrics['outside_region_mae']:.4f}; maximum is {float(max_mae):.4f}. Regenerate the last frame by editing the first frame."
                )
            if metrics["outside_region_significant_change_pct"] > float(max_significant):
                errors.append(
                    f"{label}: {metrics['outside_region_significant_change_pct']:.1f}% of protected background pixels changed significantly; maximum is {float(max_significant):.1f}%."
                )

    return {
        "gate": "Keyframe continuity gate",
        "status": "pass" if not errors else "fail",
        "scene_slug": spec.get("scene_slug"),
        "errors": errors,
        "metrics": metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Seedance keyframe edit provenance and background continuity.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--scene-spec", help="Path to SEEDANCE_SCENE.json")
    parser.add_argument("--scene-slug", help="Scene slug used to locate SEEDANCE_SCENE.json")
    args = parser.parse_args()
    project = find_project_root(args.project)
    spec_path = (
        Path(args.scene_spec).expanduser().resolve()
        if args.scene_spec
        else find_scene_spec(project, args.scene_slug, filename="SEEDANCE_SCENE.json")
    )
    report = validate_keyframe_continuity(project, load_json(spec_path), spec_path=spec_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 3)


if __name__ == "__main__":
    main()
