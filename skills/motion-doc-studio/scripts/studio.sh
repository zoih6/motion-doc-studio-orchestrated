#!/usr/bin/env bash
# Print the Motion-Doc Studio root (engine/, tools/, rules/, library/, vendor/…); install it if missing.
#   STUDIO=$(bash <this-skill>/scripts/studio.sh)
# Looks in: $MDS_HOME → the repo this skill lives in (plugin / clone / symlink) → ~/.motion-doc-studio-orchestrated.
# Not found → git clone --depth 1 https://github.com/zoih6/motion-doc-studio-orchestrated ~/.motion-doc-studio-orchestrated (or $MDS_HOME).
H="$(cd -P "$(dirname "$0")/.." && pwd -P)"
for d in "${MDS_HOME:-}" "$H/../.." "$HOME/.motion-doc-studio-orchestrated"; do
  [ -n "$d" ] && [ -f "$d/engine/core.js" ] && [ -f "$d/vendor/README.md" ] && { (cd "$d" && pwd -P); exit 0; }
done
D="${MDS_HOME:-$HOME/.motion-doc-studio-orchestrated}"
echo "motion-doc-studio not found — cloning into $D" >&2
git clone -q --depth 1 https://github.com/zoih6/motion-doc-studio-orchestrated "$D" >&2 && (cd "$D" && pwd -P)
