#!/usr/bin/env python3
"""Validate the minimum Arabic/RTL render contract for a motion project."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ARABIC = re.compile(r"[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]")
RTL = re.compile(r"(?:ctx\.direction\s*=\s*['\"]rtl|direction\s*[:=]\s*['\"]?rtl|dir\s*=\s*['\"]rtl)", re.I)
FONT = re.compile(r"(?:@font-face|font-family|Amiri|Noto Kufi|Noto Naskh|Reem Kufi|El Messiri|Aref Ruqaa|Rakkas|Katibeh|Marhey|Lemonada|Scheherazade)", re.I)
PRELOAD = re.compile(r"(?:document\.fonts\.(?:load|ready)|fonts\.load\(|fontface)", re.I)
MIRROR = re.compile(r"(?:scaleX\s*\(\s*-1|ctx\.scale\s*\(\s*-1|scale\s*\(\s*-1)", re.I)
TEXT_EXT = {".js", ".mjs", ".cjs", ".html", ".htm", ".css", ".jsx", ".tsx", ".json"}


def files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.suffix.lower() in TEXT_EXT:
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.project).resolve()
    texts = []
    for p in files(root):
        try:
            texts.append((p, p.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    arabic_files = [(p, t) for p, t in texts if ARABIC.search(t)]
    result = {"project": str(root), "status": "not_applicable", "arabic_files": [str(p) for p, _ in arabic_files], "checks": {}}
    if not arabic_files:
        result["message"] = "No Arabic text found in code/assets manifest; RTL gate not applicable."
    else:
        blob = "\n".join(t for _, t in texts)
        checks = {
            "rtl_direction": bool(RTL.search(blob)),
            "arabic_font": bool(FONT.search(blob)),
            "font_preload": bool(PRELOAD.search(blob)),
            "no_horizontal_mirror": not bool(MIRROR.search(blob)),
        }
        result["checks"] = checks
        result["status"] = "ok" if all(checks.values()) else "fail"
        if result["status"] == "fail":
            result["message"] = "Arabic render contract failed; stop before render."
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"ok", "not_applicable"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
