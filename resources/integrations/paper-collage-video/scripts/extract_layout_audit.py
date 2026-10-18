#!/usr/bin/env python3
"""Extract assembly and final-hold review frames for every collage Scene."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path


def run(command: list[str]) -> None:
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffmpeg command failed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a per-Scene layout audit contact sheet.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    parser.add_argument("--video", default="07_remotion/out/rough.mp4", help="Video path relative to project")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required for the Layout audit gate.")

    project = Path(args.project).expanduser().resolve()
    config = json.loads((project / "project-config.json").read_text(encoding="utf-8"))
    video = Path(args.video).expanduser()
    if not video.is_absolute():
        video = project / video
    if not video.is_file():
        raise SystemExit(f"Rendered video was not found: {video}")

    scenes = config.get("scenes", [])
    if not scenes:
        scenes = [
            {
                "slug": "scene-01",
                "start_seconds": 0,
                "duration_seconds": config.get("total_duration_seconds", 0),
            }
        ]

    output = project / "05_render" / "layout-audit"
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("[0-9][0-9]-*.jpg"):
        stale.unlink()
    cursor = 0.0
    extracted: list[Path] = []
    samples: list[dict[str, object]] = []
    for index, scene in enumerate(scenes, start=1):
        start = float(scene.get("start_seconds", cursor))
        duration = float(scene.get("duration_seconds", 0))
        if duration <= 0:
            raise SystemExit(f"Scene {index} has no positive duration_seconds.")
        cursor = start + duration
        slug = str(scene.get("slug", f"scene-{index:02d}"))
        positions: list[tuple[str, float]] = [("establish", 0.08)]
        manifest_path = project / "02_assets" / "scenes" / f"scene-{index:02d}" / "ASSETS.json"
        manifest: dict[str, object] = {}
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            assets = manifest.get("assets", {})
            if isinstance(assets, dict):
                for slot in manifest.get("narrative_sequence", []):
                    entry = assets.get(slot)
                    if not isinstance(entry, dict) or entry.get("approved") is not True:
                        continue
                    motion = entry.get("motion", {})
                    end_pct = motion.get("end_pct") if isinstance(motion, dict) else None
                    if isinstance(end_pct, (int, float)):
                        positions.append((f"after-{slot}", min(0.82, float(end_pct) / 100 + 0.025)))
                dominant = str(manifest.get("dominant_motion_asset", ""))
                dominant_entry = assets.get(dominant)
                if isinstance(dominant_entry, dict):
                    action = dominant_entry.get("action_motion", {})
                    if isinstance(action, dict) and action.get("type") != "none":
                        end_pct = action.get("end_pct")
                        if isinstance(end_pct, (int, float)):
                            positions.append(("motion-payoff", min(0.82, float(end_pct) / 100 + 0.02)))
            hold_pct = manifest.get("final_hold_start_pct")
            if isinstance(hold_pct, (int, float)):
                positions.append(("final-hold-start", min(0.9, float(hold_pct) / 100 + 0.03)))
        positions.append(("final-hold", 0.9))
        deduped: list[tuple[str, float]] = []
        for label, position in positions:
            if any(abs(position - prior_position) < 0.018 for _, prior_position in deduped):
                continue
            deduped.append((label, position))
        for label, position in deduped:
            timestamp = start + duration * position
            destination = output / f"{index:02d}-{slug}-{label}.jpg"
            run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-ss",
                    f"{timestamp:.3f}",
                    "-i",
                    str(video),
                    "-frames:v",
                    "1",
                    "-q:v",
                    "2",
                    "-y",
                    str(destination),
                ]
            )
            extracted.append(destination)
            samples.append({"scene": slug, "label": label, "position_pct": round(position * 100, 2), "timestamp": round(timestamp, 3), "file": str(destination)})

    contact_sheet = output / "contact-sheet.jpg"
    columns = min(4, max(1, len(extracted)))
    rows = max(1, math.ceil(len(extracted) / columns))
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-pattern_type",
            "glob",
            "-i",
            str(output / "[0-9][0-9]-*.jpg"),
            "-vf",
            f"scale=420:-2,tile={columns}x{rows}:padding=8:margin=8:color=white",
            "-frames:v",
            "1",
            "-y",
            str(contact_sheet),
        ]
    )
    digest = hashlib.sha256(contact_sheet.read_bytes()).hexdigest()
    (output / "audit-manifest.json").write_text(
        json.dumps({"video": str(video), "samples": samples, "contact_sheet": str(contact_sheet), "contact_sheet_sha256": digest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "review.json").write_text(
        json.dumps(
            {
                "status": "pending",
                "contact_sheet_sha256": digest,
                "reviewer": "",
                "checks": {
                    "subjects_readable_at_thumbnail": False,
                    "metaphor_and_reading_path_clear": False,
                    "no_unplanned_overlap_or_clipping": False,
                    "motion_payoff_matches_content": False,
                    "adjacent_scenes_are_distinct": False,
                    "final_hold_is_stable": False,
                },
                "notes": "",
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"frames": [str(path) for path in extracted], "contact_sheet": str(contact_sheet), "review": str(output / "review.json")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
