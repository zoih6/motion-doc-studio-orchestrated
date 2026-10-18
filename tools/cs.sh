#!/usr/bin/env bash
# Contact sheet: PAGE=index.html ../tools/cs.sh NAME COLS t1 t2 ...  → tmp/cs_NAME.png  (run from the film folder)
# Times are zero-padded internally so the sheet is in time order.
D="$(cd "$(dirname "$0")" && pwd)"; N=$1; C=$2; shift 2; mkdir -p tmp; rm -f tmp/still_*.png
TS=(); for t in "$@"; do TS+=("$(printf '%07.2f' "$t")"); done
timeout 600 node "$D/still.mjs" "${TS[@]}" 2>&1 | grep -E "ERR|rror|MISSING" | head -5
ffmpeg -v error -y -pattern_type glob -i 'tmp/still_*.png' -vf "scale=640:-1,tile=${C}x$(( ($# + C - 1) / C )):padding=6:color=black" -frames:v 1 tmp/cs_$N.png && echo "tmp/cs_$N.png"
