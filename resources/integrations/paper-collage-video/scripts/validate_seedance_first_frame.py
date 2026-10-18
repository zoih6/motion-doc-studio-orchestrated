#!/usr/bin/env python3
"""Validate a Seedance first-frame canvas before the last-frame image call."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(project: Path, value: str) -> Path:
    candidate = Path(value).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (project / candidate).resolve()


def first_frame_entry(spec: dict[str, Any]) -> dict[str, Any] | None:
    for frame in spec.get("frames", []):
        if isinstance(frame, dict) and frame.get("role") == "first_frame":
            return frame
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stop Seedance production when the first frame does not match the Gate 1 canvas."
    )
    parser.add_argument("--project", required=True, help="Paper collage project root")
    parser.add_argument("--scene-spec", required=True, help="SEEDANCE_SCENE.json path")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    spec_path = resolve_path(project, args.scene_spec)
    errors: list[str] = []
    metrics: dict[str, Any] = {}

    try:
        spec = load_json(spec_path)
    except (OSError, json.JSONDecodeError) as exc:
        spec = {}
        errors.append(f"Cannot read Scene spec {spec_path}: {exc}")

    canvas = spec.get("keyframe_generation_contract", {}).get("canvas", {})
    resolution = spec.get("resolution", {})
    expected_ratio = str(canvas.get("aspect_ratio") or resolution.get("aspect_ratio") or "").strip()
    expected_width = canvas.get("width") or resolution.get("width")
    expected_height = canvas.get("height") or resolution.get("height")
    if expected_ratio not in {"16:9", "9:16"}:
        errors.append(f"Gate 1 canvas aspect ratio is missing or unsupported: {expected_ratio!r}.")
    if not isinstance(expected_width, int) or not isinstance(expected_height, int):
        errors.append("Gate 1 canonical canvas width and height must be integers in the Scene spec.")

    frame = first_frame_entry(spec)
    if frame is None:
        errors.append("Scene spec must contain one frame with role=first_frame.")
    else:
        first_path = resolve_path(project, str(frame.get("path", "")))
        metrics["first_frame_path"] = str(first_path)
        if not first_path.is_file():
            errors.append(f"First-frame file is missing: {first_path}")
        else:
            with Image.open(first_path) as image:
                actual_width, actual_height = image.size
            metrics.update(
                {
                    "actual_width": actual_width,
                    "actual_height": actual_height,
                    "actual_aspect_ratio": actual_width / actual_height,
                    "expected_width": expected_width,
                    "expected_height": expected_height,
                    "expected_aspect_ratio": expected_ratio,
                }
            )
            if isinstance(expected_width, int) and isinstance(expected_height, int):
                if (actual_width, actual_height) != (expected_width, expected_height):
                    errors.append(
                        "First-frame canvas does not match the Gate 1 canonical canvas: "
                        f"got {actual_width}x{actual_height}, expected {expected_width}x{expected_height}. "
                        "Stop before last-frame generation; normalize or regenerate the first frame, "
                        "record the postprocess, then rerun this gate."
                    )
            if ":" in expected_ratio:
                ratio_width, ratio_height = (float(part) for part in expected_ratio.split(":", 1))
                target_ratio = ratio_width / ratio_height
                if abs(actual_width / actual_height - target_ratio) > 0.001:
                    errors.append(
                        f"First-frame aspect ratio does not match Gate 1 {expected_ratio}: "
                        f"got {actual_width}x{actual_height}."
                    )

    report = {
        "gate": "Seedance first-frame canvas gate",
        "status": "pass" if not errors else "fail",
        "project": str(project),
        "scene_spec": str(spec_path),
        "metrics": metrics,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 3)


if __name__ == "__main__":
    main()
