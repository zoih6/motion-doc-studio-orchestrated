#!/usr/bin/env python3
"""Runtime helpers for the paper-collage-video Seedance workflow."""

from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_ENV_PATH = SKILL_ROOT / ".env"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
DEFAULT_NEGATIVE_PROMPT = (
    "flicker, jitter, warping, broken anatomy, duplicated objects, distorted hands, "
    "mushy paper texture, unreadable text, low detail, deformed faces"
)
ASPECT_RATIO_SIZES = {
    "16:9": (1536, 864),
    "9:16": (864, 1536),
}


def load_skill_env(path: Path = SKILL_ENV_PATH) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        value = raw_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


SKILL_ENV = load_skill_env()


def env_value(name: str, fallback: str = "") -> str:
    return SKILL_ENV.get(name, os.environ.get(name, fallback)).strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def guess_content_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def resolve_path(project_root: Path, maybe_relative: str) -> Path:
    candidate = Path(maybe_relative).expanduser()
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def aspect_ratio_dimensions(aspect_ratio: str) -> tuple[int, int]:
    try:
        return ASPECT_RATIO_SIZES[aspect_ratio]
    except KeyError as exc:
        raise ValueError(f"Unsupported Gate 1 aspect ratio: {aspect_ratio!r}") from exc


def normalize_num_frames(num_frames: int) -> int:
    capped = max(9, min(441, num_frames))
    remainder = (capped - 1) % 8
    return capped if remainder == 0 else capped + (8 - remainder)


def frames_for_duration(seconds: float, frame_rate: int) -> int:
    return normalize_num_frames(max(9, round(seconds * frame_rate)))


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    body = None
    merged_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        merged_headers.setdefault("Content-Type", "application/json")
    request = Request(url=url, method=method.upper(), data=body, headers=merged_headers)
    with urlopen(request, timeout=timeout) as response:
        data = response.read()
    if not data:
        return {}
    return json.loads(data.decode("utf-8"))


def download_file(
    url: str,
    destination: Path,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 120,
) -> Path:
    ensure_dir(destination.parent)
    request = Request(url=url, headers=headers or {})
    with urlopen(request, timeout=timeout) as response:
        destination.write_bytes(response.read())
    return destination


def find_project_root(path: str | Path) -> Path:
    candidate = Path(path).expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent
    return candidate


def find_scene_spec(
    project_root: Path,
    scene_slug: str | None = None,
    *,
    filename: str = "SEEDANCE_SCENE.json",
) -> Path:
    if scene_slug:
        direct = project_root / "06_sequence" / "scenes" / scene_slug / filename
        if direct.exists():
            return direct
    single_scene = project_root / "03_animation" / filename
    if single_scene.exists() and scene_slug is None:
        return single_scene
    matches = sorted(project_root.glob(f"06_sequence/scenes/*/{filename}"))
    if scene_slug and not matches:
        raise FileNotFoundError(
            f"No scene spec `{filename}` found for `{scene_slug}` in {project_root}"
        )
    if len(matches) == 1 and scene_slug is None:
        return matches[0]
    if scene_slug is None and len(matches) > 1:
        raise FileNotFoundError(
            f"Multiple scene specs `{filename}` found. Pass --scene-slug or --scene-spec explicitly."
        )
    raise FileNotFoundError(f"No scene spec `{filename}` found in {project_root}")


def build_ark_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def path_to_data_uri(path: Path) -> str:
    content_type = guess_content_type(path)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{content_type};base64,{encoded}"


def deep_find_first(payload: Any, keys: tuple[str, ...]) -> Any | None:
    if isinstance(payload, dict):
        for key in keys:
            if key in payload and payload[key]:
                return payload[key]
        for value in payload.values():
            found = deep_find_first(value, keys)
            if found:
                return found
    if isinstance(payload, list):
        for item in payload:
            found = deep_find_first(item, keys)
            if found:
                return found
    return None
