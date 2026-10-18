#!/usr/bin/env python3
"""
One-command Seedance scene runner:
1. Validate that last-frame is an approved edit of the exact first-frame
2. Read the validated local first-frame and last-frame stills
3. Submit the Seedance first+last-frame job
4. Poll until completion
5. Download the finished video into the project
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from runtime_support import find_project_root, find_scene_spec

SCRIPTS_DIR = Path(__file__).resolve().parent
SUBMIT_SCRIPT = SCRIPTS_DIR / "submit_seedance_video.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Seedance scene end to end."
    )
    parser.add_argument("--project", required=True, help="Project root.")
    parser.add_argument("--scene-spec", help="Path to SEEDANCE_SCENE.json.")
    parser.add_argument(
        "--scene-slug",
        help="Scene slug when resolving the scene spec automatically.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=1200,
        help="Maximum Seedance polling time.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the pipeline without calling remote services.",
    )
    return parser.parse_args()


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> None:
    args = parse_args()
    project_root = find_project_root(args.project)
    scene_spec = (
        Path(args.scene_spec).expanduser().resolve()
        if args.scene_spec
        else find_scene_spec(
            project_root,
            args.scene_slug,
            filename="SEEDANCE_SCENE.json",
        )
    )

    submit_cmd = [
        sys.executable,
        str(SUBMIT_SCRIPT),
        "--project",
        str(project_root),
        "--scene-spec",
        str(scene_spec),
        "--poll-interval",
        str(args.poll_interval),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--download",
    ]
    if args.dry_run:
        submit_cmd.append("--dry-run")
    run_command(submit_cmd)


if __name__ == "__main__":
    main()
