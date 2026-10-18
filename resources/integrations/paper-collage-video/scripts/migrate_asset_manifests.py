#!/usr/bin/env python3
"""Migrate legacy Remotion ASSETS.json files to the current scaffold schema."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from bootstrap_collage_video import ASSET_MANIFEST_VERSION, scene_asset_manifest


def merge_defaults(current: Any, default: Any) -> Any:
    if isinstance(current, dict) and isinstance(default, dict):
        merged = dict(current)
        for key, value in default.items():
            merged[key] = merge_defaults(merged[key], value) if key in merged else value
        return merged
    return current


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate legacy collage asset manifests.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    parser.add_argument("--dry-run", action="store_true", help="Report files without writing")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    config = json.loads((project / "project-config.json").read_text(encoding="utf-8"))
    aspect_ratio = str(config.get("delivery", {}).get("aspect_ratio", "16:9"))
    background_policy = str(config.get("background_policy", "per-scene"))
    sharing = config.get("background_sharing_authorized") is True
    changed: list[str] = []
    for path in sorted(project.glob("02_assets/scenes/*/ASSETS.json")):
        current = json.loads(path.read_text(encoding="utf-8"))
        if current.get("manifest_version") == ASSET_MANIFEST_VERSION:
            continue
        public_slug = path.parent.name
        scene_slug = str(current.get("scene_slug", public_slug))
        assets = current.get("assets")
        if isinstance(assets, dict) and "metaphor_driver_optional" in assets and "metaphor_driver" not in assets:
            assets["metaphor_driver"] = assets.pop("metaphor_driver_optional")
        default = scene_asset_manifest(scene_slug, public_slug, aspect_ratio, background_policy, sharing)
        migrated = merge_defaults(current, default)
        migrated["manifest_version"] = ASSET_MANIFEST_VERSION
        migrated["status"] = "pending"
        for lock in (
            "composition_blueprint_locked",
            "content_order_locked",
            "composition_locked",
            "motion_plan_locked",
        ):
            migrated[lock] = False
        changed.append(str(path.relative_to(project)))
        if args.dry_run:
            continue
        backup = path.with_name(f"ASSETS.v{current.get('manifest_version', 'legacy')}.backup.json")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest_version": ASSET_MANIFEST_VERSION, "dry_run": args.dry_run, "changed": changed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
