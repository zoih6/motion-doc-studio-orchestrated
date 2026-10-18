#!/usr/bin/env bash
# SOUND LAYER setup for a film folder (the folder you render from, e.g. film/).
#   tools/sound_layer.sh setup  [DIR]   → DIR/sound-layer  (git clone upstream @ pinned commit; offline → vendored copy)
#   tools/sound_layer.sh verify [DIR]   → checksums of DIR/sound-layer vs the pinned release (scripts must stay unmodified)
#   tools/sound_layer.sh kit    [DIR]   → uv run sound-layer/scripts/sfx.py kit  (1st run ≈ 3–10 min, ~220 MB, CC0)
#   tools/sound_layer.sh deps           → ffmpeg + uv (idempotent)
#   LATEST=1 tools/sound_layer.sh setup DIR   → stay on upstream HEAD instead of the pinned, tested commit
# The scripts are vendored UNMODIFIED from https://github.com/Bodila51/opus-sound-layer (MIT) — see vendor/README.md.
# Never edit them and never loosen a threshold to make a check pass.
set -e
S="$(cd "$(dirname "$0")/.." && pwd)"; UP=https://github.com/Bodila51/opus-sound-layer
PIN=$(sed -n 's/^pinned_commit: *//p' "$S/vendor/README.md" | head -1)
cmd=${1:-setup}; D=$(cd "${2:-.}" && pwd)
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
deps() {
  command -v ffmpeg >/dev/null || { sudo apt-get update -qq >/dev/null 2>&1 && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/dev/null 2>&1 || brew install ffmpeg; }
  command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
  command -v uv >/dev/null && command -v ffmpeg >/dev/null && echo "deps ok: $(uv --version), $(ffmpeg -version | head -1 | cut -d' ' -f1-3)"
}
verify() {
  [ -d "$D/sound-layer/scripts" ] || { echo "no $D/sound-layer — run: $0 setup $D"; exit 1; }
  if (cd "$D/sound-layer" && sha256sum -c --quiet "$S/vendor/opus-sound-layer.sha256" 2>/dev/null); then echo "sound-layer OK: unmodified, pinned ${PIN:0:7}"
  elif [ -d "$D/sound-layer/.git" ] && [ -z "$(git -C "$D/sound-layer" status --porcelain -- scripts)" ]; then echo "sound-layer OK: clean upstream checkout $(git -C "$D/sound-layer" rev-parse --short HEAD) (not the pinned ${PIN:0:7})"
  else echo "sound-layer MODIFIED — restore it (rm -rf $D/sound-layer && $0 setup $D). Never edit the scripts or thresholds."; exit 1; fi
}
case $cmd in
  deps) deps ;;
  setup)
    if [ ! -d "$D/sound-layer/scripts" ]; then
      if git clone -q "$UP" "$D/sound-layer" 2>/dev/null; then
        [ -n "$LATEST" ] || git -C "$D/sound-layer" -c advice.detachedHead=false checkout -q "$PIN"
        echo "cloned $UP → $D/sound-layer @ $(git -C "$D/sound-layer" rev-parse --short HEAD)"
      else cp -r "$S/vendor/opus-sound-layer" "$D/sound-layer"; echo "offline: copied vendored sound-layer @ ${PIN:0:7} → $D/sound-layer"; fi
    fi
    mkdir -p "$D/audio" "$D/out"
    grep -qs '^sound-layer/' "$D/.gitignore" || printf 'sound-layer/\naudio/kit/\naudio/stems/\naudio/candidates/\naudio/_raw/\nout/\n' >> "$D/.gitignore"
    deps; verify ;;
  verify) verify ;;
  kit) verify; cd "$D" && uv run sound-layer/scripts/sfx.py kit ;;
  *) sed -n 2,9p "$0"; exit 1 ;;
esac
