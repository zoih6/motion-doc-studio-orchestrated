#!/usr/bin/env python3
"""Hard Gate 0 checks for the paper-collage-video skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_ENV_PATH = SKILL_ROOT / ".env"
VOICEOVER_VENV_PYTHON = SKILL_ROOT / ".venv-voiceover" / "bin" / "python"


def load_env(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def check_item(check_id: str, ok: bool, detail: str, fix: str) -> dict[str, str]:
    return {
        "id": check_id,
        "status": "pass" if ok else "fail",
        "detail": detail,
        "fix": fix,
    }


def first_existing(candidates: list[Path]) -> Path | None:
    return next((path for path in candidates if path.is_file()), None)


def find_remotion_skill() -> Path | None:
    direct_candidates = [
        Path.home() / ".agents/skills/remotion/SKILL.md",
        Path.home() / ".codex/skills/remotion/SKILL.md",
    ]
    direct = first_existing(direct_candidates)
    if direct:
        return direct
    plugin_root = Path.home() / ".codex/plugins/cache"
    if not plugin_root.is_dir():
        return None
    plugin_candidates = sorted(plugin_root.glob("**/remotion/*/skills/remotion*/SKILL.md"))
    return next(iter(plugin_candidates), None)


def run_checks(*, require_edge_tts: bool = False) -> dict:
    skill_env = load_env(SKILL_ENV_PATH)
    ark_value = skill_env.get("ARK_API_KEY", "").strip()
    imagegen_skill = first_existing(
        [
            Path.home() / ".codex/skills/.system/imagegen/SKILL.md",
            Path.home() / ".codex/skills/imagegen/SKILL.md",
            Path.home() / ".agents/skills/imagegen/SKILL.md",
        ]
    )
    remotion_skill = find_remotion_skill()
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    pillow_available = importlib.util.find_spec("PIL") is not None
    edge_tts_available = importlib.util.find_spec("edge_tts") is not None
    if not edge_tts_available and VOICEOVER_VENV_PYTHON.is_file():
        edge_tts_available = (
            subprocess.run(
                [str(VOICEOVER_VENV_PYTHON), "-c", "import edge_tts"],
                capture_output=True,
                text=True,
            ).returncode
            == 0
        )
    seedance_scripts = [
        SKILL_ROOT / "scripts/run_seedance_scene.py",
        SKILL_ROOT / "scripts/submit_seedance_video.py",
        SKILL_ROOT / "scripts/validate_seedance_first_frame.py",
        SKILL_ROOT / "scripts/validate_seedance_keyframes.py",
    ]
    composition_gate_scripts = [
        SKILL_ROOT / "scripts/validate_composition_blueprint.py",
        SKILL_ROOT / "scripts/validate_collage_project.py",
        SKILL_ROOT / "scripts/extract_layout_audit.py",
        SKILL_ROOT / "scripts/finalize_remotion_render.py",
        SKILL_ROOT / "scripts/verify_remotion_output.py",
        SKILL_ROOT / "scripts/migrate_asset_manifests.py",
        SKILL_ROOT / "references/0720-bright-paper-style.md",
    ]
    remotion_runtime_script = SKILL_ROOT / "scripts/ensure_remotion_runtime.py"
    remotion_cache = Path.home() / ".codex" / "cache" / "paper-collage-video" / "remotion-runtime"
    cached_remotion_clis = list(remotion_cache.glob("*/node_modules/.bin/remotion")) if remotion_cache.is_dir() else []
    cached_browsers = list(remotion_cache.glob("*/node_modules/.remotion/**/chrome-headless-shell")) if remotion_cache.is_dir() else []
    gitignore_path = SKILL_ROOT / ".gitignore"
    gitignore_text = gitignore_path.read_text(encoding="utf-8") if gitignore_path.is_file() else ""
    env_ignored = any(line.strip() == ".env" for line in gitignore_text.splitlines())

    checks = [
        check_item(
            "skill_env_file",
            SKILL_ENV_PATH.is_file(),
            f"Skill-local env path: {SKILL_ENV_PATH}",
            f"Create {SKILL_ENV_PATH}.",
        ),
        check_item(
            "skill_local_ark_api_key",
            bool(ark_value) and ark_value not in {"...", "changeme", "your-key-here"},
            "ARK_API_KEY is configured in the skill-local .env." if ark_value else "ARK_API_KEY is missing from the skill-local .env.",
            f"Add a non-empty ARK_API_KEY to {SKILL_ENV_PATH}. Process environment values do not satisfy this gate.",
        ),
        check_item(
            "imagegen_skill",
            imagegen_skill is not None,
            f"Image generation skill: {imagegen_skill}" if imagegen_skill else "Image generation skill was not found.",
            "Install or restore the imagegen skill before generating collage assets.",
        ),
        check_item(
            "remotion_skill",
            remotion_skill is not None,
            f"Remotion skill/plugin: {remotion_skill}" if remotion_skill else "Remotion skill/plugin was not found.",
            "Install or enable the Remotion skill/plugin.",
        ),
        check_item(
            "node",
            node_path is not None,
            f"Node executable: {node_path}" if node_path else "Node executable was not found.",
            "Install Node.js before using remotion-code.",
        ),
        check_item(
            "npm",
            npm_path is not None,
            f"npm executable: {npm_path}" if npm_path else "npm executable was not found.",
            "Install npm before using remotion-code.",
        ),
        check_item(
            "remotion_shared_runtime",
            remotion_runtime_script.is_file() and node_path is not None and npm_path is not None,
            (
                f"Shared Remotion runtime is ready at {cached_remotion_clis[0].parent.parent}."
                if cached_remotion_clis
                else "Shared Remotion runtime bootstrap is available; the first Remotion project installs once and later projects reuse it."
            ),
            "Restore ensure_remotion_runtime.py and make sure Node/npm are available.",
        ),
        check_item(
            "ffmpeg_tools",
            ffmpeg_path is not None and ffprobe_path is not None,
            f"ffmpeg: {ffmpeg_path}; ffprobe: {ffprobe_path}" if ffmpeg_path and ffprobe_path else "ffmpeg and/or ffprobe were not found.",
            "Install ffmpeg and ffprobe before rendering or running the Layout audit gate.",
        ),
        check_item(
            "pillow_inspector",
            pillow_available,
            "Pillow is available for read-only alpha-bound inspection." if pillow_available else "Pillow is unavailable.",
            "Install Pillow for the Asset Gate. It may inspect/crop existing rasters but must not draw visible assets.",
        ),
        check_item(
            "seedance_scripts",
            all(path.is_file() for path in seedance_scripts),
            "Seedance first-frame canvas, first/last-frame runner, and continuity gate scripts are present.",
            "Restore run_seedance_scene.py, submit_seedance_video.py, validate_seedance_first_frame.py, and validate_seedance_keyframes.py.",
        ),
        check_item(
            "composition_gate_scripts",
            all(path.is_file() for path in composition_gate_scripts),
            "Composition blueprint, project validation, layout audit/finalization, migration, media verification, and bright-paper style contracts are present.",
            "Restore the Remotion validation, audit, finalization, migration, and media-verification scripts before generating assets.",
        ),
        check_item(
            "env_gitignored",
            env_ignored,
            "The skill-local .env is excluded by .gitignore." if env_ignored else "The skill-local .env is not excluded by .gitignore.",
            f"Add .env to {gitignore_path} before any Git synchronization.",
        ),
    ]
    if require_edge_tts:
        checks.append(
            check_item(
                "edge_tts",
                edge_tts_available,
                "The edge-tts Python package is available."
                if edge_tts_available
                else "The edge-tts Python package is unavailable.",
                "Create the skill-local runtime with `uv venv ~/.codex/skills/paper-collage-video/.venv-voiceover`, then install with `uv pip install --python ~/.codex/skills/paper-collage-video/.venv-voiceover/bin/python -r ~/.codex/skills/paper-collage-video/requirements-voiceover.txt`.",
            )
        )
    return {
        "gate": "Gate 0",
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "checks": checks,
        "optional_capabilities": {
            "edge_tts": "available" if edge_tts_available else "unavailable",
            "remotion_runtime_cache": "ready" if cached_remotion_clis else "prepare-on-first-project",
            "remotion_browser_cache": "ready" if cached_browsers else "download-on-first-render-only",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paper-collage-video Gate 0 checks.")
    parser.add_argument("--json", action="store_true", help="Emit compact JSON instead of formatted JSON")
    parser.add_argument(
        "--require-edge-tts",
        action="store_true",
        help="Fail when the optional Edge TTS voiceover capability is unavailable",
    )
    args = parser.parse_args()
    report = run_checks(require_edge_tts=args.require_edge_tts)
    print(json.dumps(report, ensure_ascii=False, indent=None if args.json else 2))
    raise SystemExit(0 if report["status"] == "pass" else 2)


if __name__ == "__main__":
    main()
