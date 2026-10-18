#!/usr/bin/env bash
# One-shot environment setup (idempotent; re-run after every sandbox reset). Run from repo root.
set -e
cd "$(dirname "$0")/.."   # repo / project root (works from any cwd)
command -v ffmpeg >/dev/null || { sudo apt-get update -qq >/dev/null 2>&1; sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/tmp/apt.log 2>&1; }
[ -d node_modules/playwright ] || npm i --no-audit --no-fund >/dev/null 2>&1
ls ~/.cache/ms-playwright 2>/dev/null | grep -q chromium || { npx playwright install chromium >/dev/null 2>&1; sudo npx playwright install-deps chromium >/tmp/deps.log 2>&1 || true; }
# uv runs the SOUND LAYER scripts (vendor/opus-sound-layer)
export PATH="$HOME/.local/bin:$PATH"
if ! command -v uv >/dev/null; then curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1; export PATH="$HOME/.local/bin:$PATH"; fi
command -v uv >/dev/null || { echo "setup failed: uv is required by the SOUND LAYER" >&2; exit 1; }
# python deps for analysis tools (video_dna.py needs numpy+pillow; opencv/sklearn optional, used if present)
if ! python3 -c "import numpy, PIL" 2>/dev/null; then
  pip install -q numpy pillow >/dev/null 2>&1 || pip install -q --break-system-packages numpy pillow >/dev/null 2>&1 || { echo "setup failed: numpy and pillow are required" >&2; exit 1; }
fi
if [ "${FULL:-0}" = 1 ]; then
  pip install -q opencv-python-headless scikit-learn >/dev/null 2>&1 || pip install -q --break-system-packages opencv-python-headless scikit-learn >/dev/null 2>&1 || { echo "setup failed: FULL=1 requires opencv and scikit-learn" >&2; exit 1; }
fi
echo "setup ok: $(ffmpeg -version | head -1 | cut -c1-30), node $(node -v), $(uv --version)"
