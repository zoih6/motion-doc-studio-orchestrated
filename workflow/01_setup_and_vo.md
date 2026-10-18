# 01 · Setup & voice-over timing

## Project layout (one repo per film)
```
<film-repo>/
  film/index.html            (copy of engine/index.html, edit window.FILM)
  film/core.js helpers.js    (copied from this skill — freeze a version per film)
  film/kit/{fonts,textures}/ (copied)
  film/scenes/s01.js …       (one file per VO section)
  film/assets/{real,gen,cut}/ processed assets used by the film
  assets/vo.mp3              original VO (never re-encoded)
  docs/ brief.md treatment.md STYLE.md shotlist.md vo_word_timings.json vo_timeline.md CREDITS.md PROGRESS.md
  tools/ (copied from this skill)
```
Render work happens in `/var/tmp/<film>` (a clone), never in the user's visible workspace.

## Commands
```bash
cd /var/tmp && git clone https://github.com/<user>/<film-repo>.git film && cd film
cp -r <skill>/tools . && cp -r <skill>/engine film && ./tools/setup.sh   # first time only
pip install faster-whisper   # once per sandbox
python3 tools/transcribe.py assets/vo.mp3 docs/vo_word_timings.json ar medium
python3 tools/find_word.py docs/vo_word_timings.json التاج الثلث     # anchors for shots
mkdir -p film/tmp && ffmpeg -v error -y -i assets/vo.mp3 -ar 48000 -ac 2 film/tmp/vo.wav
```

## Section map
From `docs/vo_timeline.md`, cut the VO into **sections** at topic changes (typically 10–60 s each) and
record exact boundaries (seconds, 2 decimals). Each section → one scene file → one render part
(parts may group small sections; part boundaries must be integer frames: `F = round(t × 30)`).
Write the map in `docs/treatment.md` as a table: `section | start | end | VO summary | visual idea`.
