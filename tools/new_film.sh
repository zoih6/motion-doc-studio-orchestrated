#!/usr/bin/env bash
# Scaffold a new film repo folder from this skill:  tools/new_film.sh /var/tmp/my-film [--kinetic] [--aspect 16:9|9:16|1:1|4:5]
# → my-film/{film (engine copy), tools, docs (templates), assets/{real,gen}}
#   --kinetic   text-only / lyric film: film/kinetic.html (engine/type.js) is the page; scene template scenes/kt_demo.js
#   --aspect    sets the canvas size of index.html + kinetic.html (render.mjs/still.mjs read it automatically)
set -e
S="$(cd "$(dirname "$0")/.." && pwd)"
usage() { sed -n '2,8p' "$0"; }
if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then usage; exit 0; fi
D=$1
case "$D" in --*) echo "destination must be the first argument, not an option: $D" >&2; usage >&2; exit 2 ;; esac
shift; KIN=0; ASP=""
while [ $# -gt 0 ]; do
  case "$1" in
    --kinetic) KIN=1 ;;
    --aspect)
      [ $# -ge 2 ] || { echo "--aspect requires a value" >&2; exit 2; }
      ASP=$2; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done
case "$ASP" in 16:9|9:16|1:1|4:5|"") ;; *) echo "unknown aspect $ASP" >&2; exit 2 ;; esac
mkdir -p "$D"/{docs,assets/real,assets/gen,film/assets}
cp -r "$S/engine/." "$D/film/"; rm -rf "$D/film/tmp" "$D/film/segments" "$D/film/renders"
cp -r "$S/tools" "$D/"; cp "$S/package.json" "$S/.gitignore" "$D/"
cp "$S/templates/brief.md" "$S/templates/shotlist.md" "$S/templates/PROGRESS.md" "$D/docs/"
cp "$S/rules/qa_checklist.md" "$D/docs/QA.md"
cp "$S/templates/LISTEN.md" "$D/docs/LISTEN.md"; mkdir -p "$D/film/audio"; cp "$S/templates/sound.json" "$D/film/audio/sound.json"
mkdir -p "$D/vendor"; cp -r "$S/vendor/." "$D/vendor/"   # pinned sound-layer for offline setup (tools/sound_layer.sh)
cat > "$D/AGENTS.md" <<EOT
# Film project — built with Motion-Doc Studio
Follow the Motion-Doc Studio skill (skills/motion-doc-studio/SKILL.md of zoih6/motion-doc-studio-orchestrated) and, for sound,
skills/motion-sound-layer (workflow/10_sound_layer.md). Project memory: docs/PROGRESS.md.
Film page: film/index.html · scenes: film/scenes/*.js (sound cues: cue.* from film/cues.js) · tools: tools/ (run from film/)
Sound: cd film && ../tools/sound_layer.sh setup . && ../tools/sound_layer.sh kit . → PAGE=index.html node ../tools/export_cues.mjs
EOT
case "$ASP" in 16:9) WH="1920 1080" ;; 9:16) WH="1080 1920" ;; 1:1) WH="1080 1080" ;; 4:5) WH="1080 1350" ;; "") WH="" ;; esac
if [ -n "$WH" ]; then set -- $WH; for f in "$D/film/index.html" "$D/film/kinetic.html"; do
  sed -i.bak -E "s/<canvas id=\"c\" width=\"[0-9]+\" height=\"[0-9]+\">/<canvas id=\"c\" width=\"$1\" height=\"$2\">/" "$f" && rm -f "$f.bak"; done; fi
PAGE=index.html; [ $KIN = 1 ] && PAGE=kinetic.html
echo "PAGE=$PAGE" > "$D/film/.page"
[ $KIN = 1 ] && printf '\nKinetic text film: page film/kinetic.html (PAGE=kinetic.html) · grammar: library/kinetic_type_motion.md of the studio · engine: film/type.js (KT)\n' >> "$D/AGENTS.md"
echo "scaffolded $D  (page: film/$PAGE${ASP:+, aspect $ASP}) — next: cd $D && ./tools/setup.sh && git init -b main  (sound: cd film && ../tools/sound_layer.sh setup .)"
