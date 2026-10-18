#!/usr/bin/env python3
"""Generate the fixed Mandarin voiceover, SRT timeline, and duration metadata."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


VOICE = "zh-CN-YunjianNeural"
SKILL_ROOT = Path(__file__).resolve().parents[1]
VOICEOVER_VENV_PYTHON = SKILL_ROOT / ".venv-voiceover" / "bin" / "python"
SRT_TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Mandarin male Edge TTS voiceover and SRT timeline."
    )
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--text-file", required=True, help="UTF-8 narration text file")
    parser.add_argument("--rate", default="+0%", help="Edge TTS speaking rate")
    parser.add_argument("--pitch", default="+0Hz", help="Edge TTS pitch")
    parser.add_argument("--volume", default="+0%", help="Edge TTS volume")
    parser.add_argument(
        "--audio-output",
        default="04_audio/voiceover.mp3",
        help="Audio path relative to the project root",
    )
    parser.add_argument(
        "--subtitle-output",
        default="04_audio/voiceover.srt",
        help="SRT path relative to the project root",
    )
    parser.add_argument(
        "--metadata-output",
        default="04_audio/voiceover-metadata.json",
        help="Metadata path relative to the project root",
    )
    return parser.parse_args()


def resolve_output(project: Path, value: str) -> Path:
    candidate = Path(value).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (project / candidate).resolve()


def timestamp_seconds(value: str) -> float:
    hours, minutes, remainder = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(remainder)


def duration_from_srt(path: Path) -> float:
    matches = list(SRT_TIME_RE.finditer(path.read_text(encoding="utf-8-sig")))
    if not matches:
        raise RuntimeError(f"Edge TTS produced no valid SRT timing entries: {path}")
    return timestamp_seconds(matches[-1].group("end"))


def duration_from_ffprobe(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
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


def edge_tts_python() -> Path | None:
    if importlib.util.find_spec("edge_tts") is not None:
        return Path(sys.executable).resolve()
    if VOICEOVER_VENV_PYTHON.is_file():
        result = subprocess.run(
            [str(VOICEOVER_VENV_PYTHON), "-c", "import edge_tts"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return VOICEOVER_VENV_PYTHON
    return None


def main() -> None:
    args = parse_args()
    edge_python = edge_tts_python()
    if edge_python is None:
        raise SystemExit(
            "Edge TTS is unavailable. Create `.venv-voiceover` with uv and install requirements-voiceover.txt, then rerun this command."
        )

    project = Path(args.project).expanduser().resolve()
    text_file = Path(args.text_file).expanduser().resolve()
    if not text_file.is_file():
        raise SystemExit(f"Narration text file does not exist: {text_file}")
    if not text_file.read_text(encoding="utf-8").strip():
        raise SystemExit(f"Narration text file is empty: {text_file}")

    audio_path = resolve_output(project, args.audio_output)
    subtitle_path = resolve_output(project, args.subtitle_output)
    metadata_path = resolve_output(project, args.metadata_output)
    for path in (audio_path, subtitle_path, metadata_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(edge_python),
        "-m",
        "edge_tts",
        "--file",
        str(text_file),
        "--voice",
        VOICE,
        f"--rate={args.rate}",
        f"--pitch={args.pitch}",
        f"--volume={args.volume}",
        "--write-media",
        str(audio_path),
        "--write-subtitles",
        str(subtitle_path),
    ]
    subprocess.run(command, check=True)

    if not audio_path.is_file() or audio_path.stat().st_size == 0:
        raise RuntimeError("Edge TTS did not produce a non-empty audio file.")
    if not subtitle_path.is_file() or subtitle_path.stat().st_size == 0:
        raise RuntimeError("Edge TTS did not produce a non-empty SRT file.")

    srt_duration = duration_from_srt(subtitle_path)
    measured_duration = duration_from_ffprobe(audio_path) or srt_duration
    payload = {
        "provider": "edge-tts-online",
        "voice": VOICE,
        "locale": "zh-CN",
        "gender": "male",
        "rate": args.rate,
        "pitch": args.pitch,
        "volume": args.volume,
        "source_text_file": str(text_file),
        "audio_file": str(audio_path),
        "subtitle_file": str(subtitle_path),
        "duration_seconds": round(measured_duration, 3),
        "srt_end_seconds": round(srt_duration, 3),
        "timeline_source": "srt",
    }
    metadata_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
