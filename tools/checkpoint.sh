#!/usr/bin/env bash
set -Eeuo pipefail
STAGE=''; RESULT=''; OUTPUT=''; NEXT=''; FILE="${PROGRESS_FILE:-docs/PROGRESS.md}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage) STAGE="$2"; shift 2;;
    --result) RESULT="$2"; shift 2;;
    --output) OUTPUT="$2"; shift 2;;
    --next) NEXT="$2"; shift 2;;
    --file) FILE="$2"; shift 2;;
    *) echo "unknown option: $1" >&2; exit 64;;
  esac
done
[[ -n "$STAGE" && -n "$RESULT" ]] || { echo 'stage and result are required' >&2; exit 64; }
mkdir -p "$(dirname "$FILE")"
if [[ ! -f "$FILE" ]]; then printf '# Progress\n\n' > "$FILE"; fi
{
  echo "## $(date -u +%FT%TZ) — $STAGE"
  echo "- result: $RESULT"
  [[ -n "$OUTPUT" ]] && echo "- output: $OUTPUT"
  [[ -n "$NEXT" ]] && echo "- next: $NEXT"
  echo
} >> "$FILE"
printf 'checkpoint written: %s\n' "$FILE"
