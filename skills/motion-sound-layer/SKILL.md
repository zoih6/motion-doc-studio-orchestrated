---
name: motion-sound-layer
description: >-
  Sound design for motion-graphics videos when you cannot hear: real CC0 recordings (no synthesized
  hits, clicks or whooshes), cues exported from the picture's own springs and easings, a
  peak-aligned −14 LUFS mix, and a measured QA gate (sync, loudness, audibility, picture match) with
  a human ear check at the end. Use it whenever a motion video, explainer, reel, logo animation,
  Remotion/HyperFrames/HTML-canvas render or Motion-Doc Studio film needs SFX, music or a final mix.
license: MIT
metadata:
  version: 2.0.0
  part-of: motion-doc-studio
  engine: vendor/opus-sound-layer @ 52ac266 (MIT, Bodila51), unmodified
---

# Motion Sound Layer

You can't hear, so you don't judge sound by taste. You place real recordings from the timeline,
look at every sound (waveform + spectrogram sheets) and let `qa.py` measure the result. A human does
the final ear check.

**The prompt this skill runs is in [PROMPT.md](PROMPT.md).** It is canonical and stays verbatim; read it
first. This file only maps it onto Motion-Doc Studio.

## 0 · Locate the studio (once per session)
```bash
STUDIO=$(bash <folder of this SKILL.md>/scripts/studio.sh)   # finds or clones zoih6/motion-doc-studio-orchestrated
"$STUDIO/tools/sound_layer.sh" setup film/                    # = the prompt's SETUP, pinned + verified
```
Run every sound command **from the folder you render from** (in a studio film: `film/`), so the
prompt's relative paths work as written: `sound-layer/`, `audio/`, `video.mp4`, `out/`.
`setup` runs `git clone https://github.com/Bodila51/opus-sound-layer sound-layer`, checks out the
pinned, tested commit (`LATEST=1` keeps upstream HEAD), copies the vendored copy if you're offline,
installs ffmpeg and uv, and verifies checksums. **Never edit `sound-layer/` and never change a
threshold.** `tools/sound_layer.sh verify film/` proves the scripts are untouched.

## 1 · CUES: computed from the picture, never typed
In a studio film, register cues in each scene file with the **same t0 and spring/easing the draw call
uses** (`engine/cues.js`, loaded by `engine/index.html`):
```js
cue.land('title', when.spring(.25, 'card'), { sound: 'tap', pan: .4 });   // motion stops
cue.move('tear',  when.ease(4, 4 + TEAR),   { sound: 'paper' });          // frame of peak speed
cue.cut('s3', 24.0, { sound: 'transition' });                             // full-frame change
cue.appear('dot', when.spring(5.8, 'snap'), { sound: 'pop', pitch: 2 });  // pops in
const h = cue.hero('logo', when.spring(12.4, 'soft'));                    // "thump+tap", stop_before, build
```
Then export (from `film/`): `PAGE=index.html node ../tools/export_cues.mjs`. It writes `audio/cues.json`
in the `mix.py --schema` format, merges `audio/sound.json` (energy, music, voice, silence_ok,
cues_extra), and fails on a duplicate id, a cue outside the film, or `synth:` hits. It warns when heroes
are under ~4 s apart. `when.*` measures frames the way `qa.py` does, so `land` and `move` agree with
the picture check.
Other renderers: compute the same frames from their timing source (Remotion `spring()` frames, GSAP
labels, `data-start`), never by eye.

Rules: sound only on real actions. One hero per ~4 s (logo, reveal). Don't put two sounds on one action.
Pan by screen position (±0.6 max).

## 2 · SOUNDS: real recordings only
`uv run sound-layer/scripts/sfx.py kit` builds 1,139 CC0 sounds in 19 types on the first run (~3.5 min, ~220 MB,
git-ignored). Run it in the background or with a 10-minute timeout.
For each type you use, `uv run sound-layer/scripts/sfx.py browse --type paper --like "dry light"` →
**LOOK at `audio/browse.png`** → put the id in the cue (`"paper/kenney-…"`). Keep one sonic family per film.
For a missing type, run `sfx.py search "<material action>" --type <type>`, then `sfx.py sheet …` and LOOK. Reject
any clip with two events in it, steady noise, clicks inside a whoosh, or clean sine lines on a physical sound. Keepers go in with
`sfx.py add FILE --type <type> --credit "<source, licence>"`. Never synthesize hits, clicks or whooshes;
no meme sounds. Music: the user's track, or a CC0 loop (credit it).

## 3 · BUILD · 4 · VERIFY · 5 · DELIVER
Exactly the prompt's commands, with the muted render from `tools/render.mjs`:
```bash
PAGE=index.html node ../tools/render.mjs --fps 30 --from 0 --to <dur> --out video.mp4   # muted picture
uv run sound-layer/scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
uv run sound-layer/scripts/qa.py out/final.mp4          # exit 1 = FAIL
```
Fix every FAIL by changing cues or sounds, at most 2 rounds; never change the scripts. Open
`audio/qa.png` and describe in words what you see at each hero cue.
Deliver `out/final.mp4`, `audio/kit/CREDITS.md` (plus music credit) and `LISTEN.md` with 5 timecodes to check by ear
(template: `$STUDIO/templates/LISTEN.md`). Report what the checks show. **Never call the sound "good".**

Full procedure, FAIL → fix table, VO films, and the 1080p/720p release encode:
`$STUDIO/workflow/10_sound_layer.md`. Worked example with real QA output: `$STUDIO/examples/demo/sound/`.
