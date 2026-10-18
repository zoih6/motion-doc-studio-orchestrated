#!/usr/bin/env python3
"""Prepare one shared Remotion runtime and reuse it across generated projects."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_fingerprint(package: dict[str, Any]) -> str:
    contract = {
        "dependencies": package.get("dependencies", {}),
        "devDependencies": package.get("devDependencies", {}),
    }
    encoded = json.dumps(contract, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def executable_ready(node_modules: Path) -> bool:
    return (node_modules / ".bin" / "remotion").is_file()


def browser_ready(node_modules: Path) -> bool:
    return any(path.is_file() for path in (node_modules / ".remotion").glob("**/chrome-headless-shell"))


def ensure_browser(node_modules: Path, cwd: Path, *, prepare: bool) -> bool:
    if browser_ready(node_modules):
        return True
    if not prepare:
        return False
    timeout_seconds = int(os.environ.get("PAPER_COLLAGE_BROWSER_TIMEOUT_SECONDS", "180"))
    try:
        completed = subprocess.run(
            [str(node_modules / ".bin" / "remotion"), "browser", "ensure"],
            cwd=cwd,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise SystemExit(
            f"Shared Remotion browser download timed out after {timeout_seconds}s. "
            "Keep the shared cache and rerun `npm run runtime`; do not install Chrome separately in this project."
        ) from exc
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return browser_ready(node_modules)


def report(status: str, **details: Any) -> None:
    print(json.dumps({"gate": "Remotion runtime", "status": status, **details}, ensure_ascii=False, indent=2))


def sync_project_lock(runtime_root: Path, remotion_root: Path, package: dict[str, Any]) -> None:
    runtime_lock = runtime_root / "package-lock.json"
    if not runtime_lock.is_file():
        return
    lock_payload = load_json(runtime_lock)
    project_name = str(package.get("name", "paper-collage-video-template"))
    lock_payload["name"] = project_name
    packages = lock_payload.get("packages")
    if isinstance(packages, dict) and isinstance(packages.get(""), dict):
        packages[""]["name"] = project_name
    (remotion_root / "package-lock.json").write_text(json.dumps(lock_payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reuse a shared Remotion dependency and browser cache.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    parser.add_argument("--check-only", action="store_true", help="Do not install or create links")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    remotion_root = project / "07_remotion"
    package_path = remotion_root / "package.json"
    if not package_path.is_file():
        raise SystemExit(f"Remotion package.json was not found: {package_path}")

    package = load_json(package_path)
    fingerprint = runtime_fingerprint(package)
    cache_base = Path(
        os.environ.get(
            "PAPER_COLLAGE_REMOTION_CACHE",
            str(Path.home() / ".codex" / "cache" / "paper-collage-video" / "remotion-runtime"),
        )
    ).expanduser()
    runtime_root = cache_base / fingerprint
    shared_modules = runtime_root / "node_modules"
    project_modules = remotion_root / "node_modules"

    if project_modules.exists() and not project_modules.is_symlink() and executable_ready(project_modules):
        ready = ensure_browser(project_modules, remotion_root, prepare=not args.check_only)
        if not ready:
            report("needs-action", source="existing-project-runtime", fix="Run npm run runtime to prepare the shared browser.")
            raise SystemExit(2)
        report("pass", source="existing-project-runtime", node_modules=str(project_modules), browser="ready")
        return
    if project_modules.is_symlink() and executable_ready(project_modules):
        sync_project_lock(project_modules.resolve().parent, remotion_root, package)
        ready = ensure_browser(project_modules, project_modules.resolve().parent, prepare=not args.check_only)
        if not ready:
            report("needs-action", source="shared-runtime", fix="Run npm run runtime to prepare the shared browser.")
            raise SystemExit(2)
        report("pass", source="shared-runtime", node_modules=str(project_modules.resolve()), browser="ready")
        return

    if args.check_only:
        report(
            "needs-action",
            fingerprint=fingerprint,
            cache=str(runtime_root),
            fix=f"python3 {Path(__file__).resolve()} --project {project}",
        )
        raise SystemExit(2)
    if shutil.which("npm") is None:
        raise SystemExit("npm is required to prepare the shared Remotion runtime.")

    runtime_root.mkdir(parents=True, exist_ok=True)
    runtime_package = dict(package)
    runtime_package["name"] = f"paper-collage-video-runtime-{fingerprint}"
    runtime_package["private"] = True
    runtime_package.pop("scripts", None)
    (runtime_root / "package.json").write_text(
        json.dumps(runtime_package, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if not executable_ready(shared_modules):
        completed = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund", "--package-lock=true"],
            cwd=runtime_root,
            text=True,
        )
        if completed.returncode != 0:
            raise SystemExit(completed.returncode)

    sync_project_lock(runtime_root, remotion_root, package)

    if project_modules.is_symlink() and not project_modules.exists():
        project_modules.unlink()
    if not project_modules.exists():
        project_modules.symlink_to(shared_modules, target_is_directory=True)
    if not executable_ready(project_modules):
        raise SystemExit(f"Remotion CLI is unavailable after runtime preparation: {project_modules}")
    if not ensure_browser(project_modules, runtime_root, prepare=True):
        raise SystemExit("Remotion browser preparation completed without a usable chrome-headless-shell binary.")

    report(
        "pass",
        source="shared-runtime",
        fingerprint=fingerprint,
        node_modules=str(shared_modules),
        browser="ready",
        note="Remotion dependencies and the downloaded browser are reused by every matching project.",
    )


if __name__ == "__main__":
    main()
