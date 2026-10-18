#!/usr/bin/env python3
"""Mux the authoritative voiceover onto an assembled video-model render."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mux voiceover audio onto an assembled video and trim to voiceover duration."
    )
    parser.add_argument("--video", required=True, help="Assembled silent video")
    parser.add_argument("--audio", required=True, help="Authoritative voiceover audio")
    parser.add_argument("--output", required=True, help="Final MP4 output")
    return parser.parse_args()


def media_duration(ffprobe: str, path: Path) -> float:
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    args = parse_args()
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise SystemExit("ffmpeg and ffprobe are required to mux the final voiceover.")

    video = Path(args.video).expanduser().resolve()
    audio = Path(args.audio).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    for path in (video, audio):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"Required media file is missing or empty: {path}")

    video_duration = media_duration(ffprobe, video)
    audio_duration = media_duration(ffprobe, audio)
    if video_duration + 0.25 < audio_duration:
        raise SystemExit(
            f"Assembled video is {video_duration:.3f}s but voiceover is {audio_duration:.3f}s. Retiming scenes is required before muxing."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-t",
            f"{audio_duration:.3f}",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=True,
    )
    print(
        json.dumps(
            {
                "video_input": str(video),
                "audio_input": str(audio),
                "output": str(output),
                "duration_seconds": round(audio_duration, 3),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
