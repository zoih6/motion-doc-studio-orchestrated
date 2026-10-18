#!/usr/bin/env bash
set -Eeuo pipefail
NAME=task
LOG_DIR="${TEMP_WORK:-/var/tmp/motion-doc-studio}/logs"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="$2"; shift 2;;
    --log-dir) LOG_DIR="$2"; shift 2;;
    --) shift; break;;
    *) echo "usage: $0 --name NAME [--log-dir DIR] -- COMMAND" >&2; exit 64;;
  esac
done
[[ $# -gt 0 ]] || { echo 'missing command' >&2; exit 64; }
mkdir -p "$LOG_DIR"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BASE="$LOG_DIR/${NAME}-${STAMP}"
LOG="$BASE.log"; PID="$BASE.pid"; STATUS="$BASE.status"
printf '%s\n' "queued $(date -u +%FT%TZ)" > "$STATUS"
(
  echo "started $(date -u +%FT%TZ)"
  "$@"
  code=$?
  echo "finished $(date -u +%FT%TZ) exit_code=$code" >> "$STATUS"
  exit "$code"
) >"$LOG" 2>&1 &
echo $! > "$PID"
echo "pid=$! log=$LOG status=$STATUS"
