#!/usr/bin/env bash
# Motion-Doc Studio installer: any coding agent, Linux / macOS / WSL. Idempotent (re-run = update).
#
#   curl -fsSL https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/install.sh | bash
#
# What it does
#   1. clones (or fast-forwards) the studio into $MDS_HOME (default ~/.motion-doc-studio-orchestrated)
#   2. installs dependencies: ffmpeg, uv, node packages, Playwright Chromium   (skip: MDS_DEPS=0)
#   3. links the skills  motion-director + motion-doc-studio + motion-sound-layer  into every agent skill folder it finds:
#        ~/.agents/skills (always: Codex, Gemini CLI, OpenCode, Amp and other Agent-Skills readers)
#        ~/.claude/skills  ~/.cursor/skills  ~/.copilot/skills  ~/.config/opencode/skills  ~/.windsurf/skills
#        (only if that agent's folder exists; force a list with MDS_AGENTS="claude cursor …")
#   4. verifies: skill frontmatter, studio locator, vendored sound-layer checksums, engine selftest
# Options (env)
#   MDS_HOME=~/.motion-doc-studio-orchestrated   MDS_REF=main   MDS_DEPS=0   MDS_KIT=1 (also build the 1,139-sound CC0 kit, ≈220 MB)
#   MDS_PROJECT=/path/to/project    also link into <project>/.claude/skills and <project>/.agents/skills
#   MDS_COPY=1  copy instead of symlink      MDS_UNINSTALL=1  remove the skill links (keeps $MDS_HOME)
set -eu
REPO="${MDS_REPO:-https://github.com/zoih6/motion-doc-studio-orchestrated}"
H="${MDS_HOME:-$HOME/.motion-doc-studio-orchestrated}"; REF="${MDS_REF:-main}"
SKILLS="motion-system-orchestrator motion-director motion-doc-studio motion-sound-layer"
say() { printf '\033[1;33m▸\033[0m %s\n' "$*"; }; ok() { printf '\033[1;32m✓\033[0m %s\n' "$*"; }; warn() { printf '\033[1;31m!\033[0m %s\n' "$*"; }
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

targets() {
  if [ -n "${MDS_AGENTS:-}" ]; then
    for a in $MDS_AGENTS; do case $a in
      agents|codex|gemini|amp) echo "$HOME/.agents/skills" ;; claude) echo "$HOME/.claude/skills" ;;
      cursor) echo "$HOME/.cursor/skills" ;; copilot) echo "$HOME/.copilot/skills" ;;
      opencode) echo "$HOME/.config/opencode/skills" ;; windsurf) echo "$HOME/.windsurf/skills" ;;
      *) warn "unknown agent '$a'" >&2 ;; esac; done | sort -u
  else
    echo "$HOME/.agents/skills"
    [ -d "$HOME/.claude" ] && echo "$HOME/.claude/skills"
    [ -d "$HOME/.cursor" ] && echo "$HOME/.cursor/skills"
    [ -d "$HOME/.copilot" ] && echo "$HOME/.copilot/skills"
    [ -d "$HOME/.config/opencode" ] && echo "$HOME/.config/opencode/skills"
    [ -d "$HOME/.windsurf" ] && echo "$HOME/.windsurf/skills"
  fi
  if [ -n "${MDS_PROJECT:-}" ]; then echo "$MDS_PROJECT/.claude/skills"; echo "$MDS_PROJECT/.agents/skills"; fi
  return 0
}

if [ -n "${MDS_UNINSTALL:-}" ]; then
  for t in $(targets); do for s in $SKILLS; do [ -L "$t/$s" ] && rm "$t/$s" && ok "removed $t/$s"; done; done
  echo "Studio files kept in $H (rm -rf it to remove everything)."; exit 0
fi

# 1 · studio
command -v git >/dev/null || { warn "git is required"; exit 1; }
if [ -d "$H/.git" ]; then
  CURRENT=$(git -C "$H" remote get-url origin 2>/dev/null || true)
  CURRENT=${CURRENT%.git}; EXPECTED=${REPO%.git}
  if [ "$CURRENT" != "$EXPECTED" ]; then
    BACKUP="$H.backup-old-$(date +%Y%m%d%H%M%S)"
    mv "$H" "$BACKUP"
    warn "existing studio origin differs; preserved old copy at $BACKUP"
    say "cloning $REPO → $H"
    git clone -q --depth 1 --branch "$REF" "$REPO" "$H"
  else
    say "updating $H"
    git -C "$H" fetch -q --depth 1 origin "$REF" && git -C "$H" checkout -q -B "$REF" FETCH_HEAD
  fi
elif [ -e "$H" ]; then
  warn "$H exists but is not a git clone. Set MDS_HOME or move it"; exit 1
else
  say "cloning $REPO → $H"
  git clone -q --depth 1 --branch "$REF" "$REPO" "$H"
fi
V=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$H/.claude-plugin/plugin.json" | head -1); ok "studio v$V at $H"

# 2 · dependencies
SUDO=""; [ "$(id -u)" != 0 ] && command -v sudo >/dev/null && SUDO=sudo
if [ "${MDS_DEPS:-1}" != 0 ]; then
  if ! command -v ffmpeg >/dev/null; then say "installing ffmpeg"
    if command -v apt-get >/dev/null; then $SUDO apt-get update -qq >/dev/null 2>&1; $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/dev/null 2>&1 || true
    elif command -v brew >/dev/null; then brew install ffmpeg >/dev/null 2>&1 || true
    elif command -v dnf >/dev/null; then $SUDO dnf install -y ffmpeg >/dev/null 2>&1 || true; fi
  fi
  command -v ffmpeg >/dev/null && ok "ffmpeg" || warn "ffmpeg missing: install it (https://ffmpeg.org) and re-run"
  command -v uv >/dev/null || { say "installing uv"; curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1 || true; }
  command -v uv >/dev/null && ok "uv $(uv --version | cut -d' ' -f2)" || warn "uv missing: https://docs.astral.sh/uv/ (needed by the sound layer)"
  if command -v node >/dev/null; then
    (cd "$H" && { [ -d node_modules/playwright ] || npm i --no-audit --no-fund --silent >/dev/null 2>&1; } \
      && npx --yes playwright install chromium >/dev/null 2>&1 \
      && { [ "$(uname)" = Linux ] && $SUDO npx --yes playwright install-deps chromium >/dev/null 2>&1 || true; }) \
      && ok "node $(node -v) + Playwright Chromium" || warn "Playwright setup incomplete: run  cd $H && ./tools/setup.sh"
  else warn "node ≥18 missing (https://nodejs.org): the renderer needs it"; fi
  python3 -c "import numpy, PIL" 2>/dev/null || python3 -m pip install -q numpy pillow >/dev/null 2>&1 || python3 -m pip install -q --break-system-packages numpy pillow >/dev/null 2>&1 || true
fi

# 3 · skills
n=0
for t in $(targets); do
  mkdir -p "$t"
  for s in $SKILLS; do
    d="$t/$s"
    if [ -e "$d" ] && [ ! -L "$d" ]; then mv "$d" "$d.bak-$(date +%s)"; warn "backed up an older $d"; fi
    if [ -n "${MDS_COPY:-}" ]; then rm -rf "$d"; cp -R "$H/skills/$s" "$d"; else ln -sfn "$H/skills/$s" "$d"; fi
    n=$((n+1))
  done
  ok "skills → $t"
done

# 4 · verify
fail=0
for s in $SKILLS; do head -5 "$H/skills/$s/SKILL.md" | grep -q "^name: $s\$" || { warn "bad frontmatter: $s"; fail=1; }; done
loc=$(bash "$(targets | head -1)/motion-doc-studio/scripts/studio.sh" 2>/dev/null || true)
[ "$loc" = "$(cd "$H" && pwd -P)" ] && ok "skills locate the studio" || { warn "studio locator returned '$loc'"; fail=1; }
SHA="sha256sum"; command -v sha256sum >/dev/null || SHA="shasum -a 256"
(cd "$H/vendor/opus-sound-layer" && $SHA -c --quiet ../opus-sound-layer.sha256 >/dev/null 2>&1) && ok "sound-layer scripts unmodified (pinned $(sed -n 's/^pinned_commit: *//p' "$H/vendor/README.md" | cut -c1-7))" || { warn "vendored sound-layer checksum mismatch"; fail=1; }
if [ "${MDS_DEPS:-1}" != 0 ] && [ -d "$H/node_modules/playwright" ]; then
  (cd "$H" && node tools/selftest.mjs >/tmp/mds-selftest.log 2>&1) && ok "engine selftest" || warn "engine selftest failed: see /tmp/mds-selftest.log"
fi
if [ -n "${MDS_KIT:-}" ]; then say "building the CC0 sound kit (≈3–10 min)"; (cd "$H/engine" && ../tools/sound_layer.sh setup . >/dev/null && ../tools/sound_layer.sh kit . | tail -3); fi

echo
[ $fail = 0 ] && ok "Motion-Doc Studio v$V installed ($n skill links)." || warn "installed with problems (see above)"
cat <<EOF

  Studio:  $H        (update: re-run this installer · uninstall: MDS_UNINSTALL=1)
  Skills:  motion-director (START HERE: intake + pro brief) · motion-doc-studio (films + kinetic type) ·
           motion-sound-layer (SFX + music + mix, measured)
  Next (agent): read $H/skills/motion-system-orchestrator/SKILL.md, then $H/skills/motion-director/SKILL.md and ask the user «ما فكرة الفيديو؟» (START.md, section C).
  Users: just say "start a new video project" or send https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/START.md
EOF
