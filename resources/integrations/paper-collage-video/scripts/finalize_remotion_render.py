#!/usr/bin/env python3
"""Promote a reviewed rough Remotion render to the final delivery path."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


REQUIRED_CHECKS = {
    "subjects_readable_at_thumbnail",
    "metaphor_and_reading_path_clear",
    "no_unplanned_overlap_or_clipping",
    "motion_payoff_matches_content",
    "adjacent_scenes_are_distinct",
    "final_hold_is_stable",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize a visually reviewed Remotion render.")
    parser.add_argument("--project", required=True, help="Paper collage project root")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    audit = project / "05_render" / "layout-audit"
    contact_sheet = audit / "contact-sheet.jpg"
    review_path = audit / "review.json"
    rough = project / "07_remotion" / "out" / "rough.mp4"
    final = project / "05_render" / "final.mp4"
    errors: list[str] = []
    if not rough.is_file():
        errors.append(f"Rough render is missing: {rough}")
    if not contact_sheet.is_file():
        errors.append(f"Layout contact sheet is missing: {contact_sheet}")
    if not review_path.is_file():
        errors.append(f"Layout review is missing: {review_path}")
        review = {}
    else:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("status") != "approved":
        errors.append("Layout review status must be approved after viewing the contact sheet.")
    if not str(review.get("reviewer", "")).strip():
        errors.append("Layout review must record a reviewer.")
    checks = review.get("checks", {})
    if not isinstance(checks, dict) or any(checks.get(key) is not True for key in REQUIRED_CHECKS):
        errors.append("Every required layout review check must be true.")
    if contact_sheet.is_file():
        digest = hashlib.sha256(contact_sheet.read_bytes()).hexdigest()
        if review.get("contact_sheet_sha256") != digest:
            errors.append("Layout approval is stale because the contact sheet changed.")
    if errors:
        print(json.dumps({"gate": "Layout approval gate", "status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(3)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rough, final)
    print(json.dumps({"gate": "Layout approval gate", "status": "pass", "final": str(final)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
