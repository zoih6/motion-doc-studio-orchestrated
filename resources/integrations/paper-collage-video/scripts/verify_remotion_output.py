#!/usr/bin/env python3
"""Verify a rendered Remotion file against the locked project delivery contract."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


RENDER_SIZES = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
}


def probe(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffprobe failed")
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Remotion output metadata.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    parser.add_argument("--video", default="07_remotion/out/final.mp4", help="Video path relative to project")
    args = parser.parse_args()

    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe is required for the final media gate.")
    project = Path(args.project).expanduser().resolve()
    config = json.loads((project / "project-config.json").read_text(encoding="utf-8"))
    video = Path(args.video).expanduser()
    if not video.is_absolute():
        video = project / video
    if not video.is_file() or video.stat().st_size == 0:
        raise SystemExit(f"Rendered video is missing or empty: {video}")

    data = probe(video)
    streams = data.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    errors: list[str] = []
    if video_stream is None:
        errors.append("No video stream was found.")
    else:
        aspect_ratio = str(config.get("delivery", {}).get("aspect_ratio", "16:9"))
        expected_size = RENDER_SIZES.get(aspect_ratio)
        actual_size = (int(video_stream.get("width", 0)), int(video_stream.get("height", 0)))
        if expected_size and actual_size != expected_size:
            errors.append(f"Resolution is {actual_size[0]}x{actual_size[1]}; expected {expected_size[0]}x{expected_size[1]} for {aspect_ratio}.")
        expected_fps = float(config.get("fps", config.get("delivery", {}).get("fps", 30)))
        try:
            actual_fps = float(Fraction(str(video_stream.get("avg_frame_rate", "0/1"))))
        except (ValueError, ZeroDivisionError):
            actual_fps = 0
        if abs(actual_fps - expected_fps) > 0.05:
            errors.append(f"Frame rate is {actual_fps:.3f}; expected {expected_fps:.3f}.")

    expected_fps = float(config.get("fps", config.get("delivery", {}).get("fps", 30)))
    scenes = config.get("scenes")
    if isinstance(scenes, list) and scenes:
        expected_frames = sum(round(float(scene.get("duration_seconds", 0)) * expected_fps) for scene in scenes if isinstance(scene, dict))
    else:
        expected_frames = round(float(config.get("total_duration_seconds", 0)) * expected_fps)
    expected_duration = expected_frames / expected_fps if expected_fps > 0 else 0
    actual_duration = float(data.get("format", {}).get("duration", 0) or 0)
    if expected_duration > 0 and abs(actual_duration - expected_duration) > max(0.12, 1 / 24):
        errors.append(f"Duration is {actual_duration:.3f}s; expected {expected_duration:.3f}s.")
    audio_block = config.get("audio") if isinstance(config.get("audio"), dict) else {}
    audio_mode = str(
        audio_block.get(
            "mode",
            config.get("delivery", {}).get("audio_mode", config.get("audio_mode", "no-audio")),
        )
    )
    expects_audio = audio_mode not in {"", "no-audio"}
    if expects_audio and not audio_streams:
        errors.append(f"audio_mode={audio_mode} requires an audio stream.")
    if not expects_audio and audio_streams:
        errors.append("audio_mode=no-audio but the render contains an audio stream.")

    report = {
        "gate": "Final media gate",
        "status": "pass" if not errors else "fail",
        "video": str(video),
        "duration_seconds": actual_duration,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 3)


if __name__ == "__main__":
    main()
