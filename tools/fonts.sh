#!/usr/bin/env bash
# Download OFL font families from google/fonts (GitHub) by directory name — see library/fonts.md
#   tools/fonts.sh [DEST] family_dir...      e.g.  tools/fonts.sh film/kit/fonts cairo reemkufi
# DEST defaults to engine/kit/fonts. Uses $GH_TOKEN_FILE (/tmp/.ghtok) if present (higher API rate limit).
set -e; D=engine/kit/fonts; [ -d "$1" ] || [[ "$1" == */* ]] && { D=$1; shift; }; mkdir -p "$D"
TF=${GH_TOKEN_FILE:-/tmp/.ghtok}; H=(); [ -f "$TF" ] && H=(-H "Authorization: Bearer $(cat "$TF")")
for f in "$@"; do
  curl -sf "${H[@]}" "https://api.github.com/repos/google/fonts/contents/ofl/$f" | python3 -c "
import sys,json
for e in json.load(sys.stdin):
    if e['name'].endswith('.ttf'): print(e['download_url'])" | while read -r u; do n=$(basename "$u" | sed 's/%5B/[/g;s/%5D/]/g'); curl -sfL "$u" -o "$D/$n" && echo "$D/$n"; done || echo "not found: $f"
done
