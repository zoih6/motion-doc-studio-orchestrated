# 10 · Sound Layer: real SFX + music, placed from the timeline, measured by QA

> Canonical prompt (verbatim): [`skills/motion-sound-layer/PROMPT.md`](../skills/motion-sound-layer/PROMPT.md).
> Engine: `vendor/opus-sound-layer` (MIT, pinned `52ac266`, **unmodified**). Cue API: `engine/cues.js`.
> When: after the picture is locked for a section (sample) and again for the final, *before* the release.
> Replaces the old synth-SFX path (`tools/cues_auto.py` + `tools/sfx.mjs`, now legacy).

You can't hear. So you never judge sound by taste. Real recordings are placed from the picture's own
timing. You look at every sound, `qa.py` decides, and a human does the final ear check.

## 0 · Setup (once per film, re-run after a sandbox reset)
```bash
cd film/                                   # everything below runs from the folder with index.html
../tools/sound_layer.sh setup .            # git clone upstream → sound-layer/ @ pinned commit (offline → vendored copy)
                                           # + ffmpeg + uv + checksum verify + .gitignore (sound-layer/, audio/kit/, stems, out/)
../tools/sound_layer.sh kit .              # = uv run sound-layer/scripts/sfx.py kit   (≈3.5 min, ≈220 MB, 1,139 CC0 sounds / 19 types)
```
Give the kit a 10-minute timeout, or run it in the background while you write cues. If uv fails with
`invalid peer certificate`, run `export UV_NATIVE_TLS=1`.

## 1 · Cues: from the picture's own timing, never typed
`engine/index.html` loads `cues.js` after `core.js`/`fx.js`. In each scene file, register cues at load
time, next to the shots, with **the same t0 and the same spring/easing as the draw call**:

| Action in the picture | Call | Frame it gets |
|---|---|---|
| card/sheet drops and settles (`drawCard`, `dropP`, `sp(t,t0,kind)`) | `cue.land(id, when.spring(t0, kind), o)` | first frame after peak speed where change ≤ 5 % of peak |
| fast travel (slide-in, whip, camera move, tear sweep `ease(a,b)`) | `cue.move(id, when.ease(a, b), o)` / `when.spring(..)` | frame of peak speed |
| hard cut / full-frame change at `a` (`tin:'cut'`, flash) | `cue.cut(id, a, o)` | first frame at/after `a` |
| element pops in (dot, icon, sticker) | `cue.appear(id, when.spring(t0,'snap'), o)` or `cue.appear(id, t, o)` | first visible frame |
| logo / reveal (one per ~4 s) | `cue.hero(id, when.spring(t0, kind), {on:'land'})` | thump+tap, `stop_before`, `build` |
| riser/reverse peaking on a hero, no picture check | `cue.raw(id, hero.frame, {sound:'riser'})` | that frame |
| custom motion (path, counter, camera) | `when.path(t => [x(t), y(t)], t0, t1)` | start / peak / land |

`o` = any mix.py cue field: `sound` (type | `type/id` | file | `"a+b"`), `weight`, `align`, `pan`,
`stop_before`, `build`, `pitch`, `note`. The demo (`engine/scenes/demo.js`, bottom) is the template.

```bash
PAGE=index.html node ../tools/export_cues.mjs        # → audio/cues.json (+ audio/sound.json merged)
```
`audio/sound.json` (copy `templates/sound.json`) holds what isn't a picture cue: `energy`
(`punchy` −14 LUFS · `calm` −18), `music`, `voice` (VO file + start), `duck_db`, `silence_ok`
(planned silences only), and `cues_extra` for cues you can't derive from code (rare; give a `src`
reason). The exporter **fails** on duplicate ids, cues outside the film, missing sounds and `synth:` hits,
and **warns** about heroes closer than ~4 s.

**What deserves a sound:** real actions only. These are a landing, a fast move, a cut, a pop-in, and the hero reveal.
Breathing, slow camera drift, grain, rays and write-on progress get no sound. Don't put two sounds on one action.
A tight series (dots) gets 2–3 pops, not 7. Pan = screen x (`x/960 − 1`, mix.py clamps to ±0.6).

**Heroes need a decisive stop.** `land` is measured as "motion stops". A very gradual settle (the `soft`
spring, slow ease-outs on small elements) lands inside the compression noise, so the check flips between
encodes. Give hero moments the `card`/`snap` spring, a cut or a fast move (demo, QA round 2).

## 2 · Sounds: real recordings, chosen by looking
1. For each type you use: `uv run sound-layer/scripts/sfx.py browse --type paper --like "dry light tear"`
   → **open `audio/browse.png`** → pick the id → `"sound": "paper/<id>"`. Reject clips with two events,
   steady noise, clicks inside a whoosh, or clean sine lines on a physical sound. A bare type uses the defaults, and
   mix.py varies repeats on its own.
2. One sonic family per film: paper + wood for manuscript/sepia films, glass + air for clean tech, metal +
   sub for trailers.
3. Missing type: `sfx.py search "<material action>" --type <type>` → `sfx.py sheet <files>` → LOOK →
   `sfx.py add FILE --type <type> --credit "<source, licence>"`.
4. **Never synthesize hits, clicks or whooshes; no meme sounds.** (`synth:pluck`/`synth:bell` exist in
   mix.py for tonal accents only.)
5. Music: the user's track, or a CC0 loop (Openverse `license=cc0`, Freesound CC0, credit it in
   `docs/CREDITS.md`). VO films: put the VO in `voice`. mix.py sets it to −16 LUFS and ducks music by `duck_db`.

## 3 · Build
```bash
PAGE=index.html node ../tools/render.mjs --fps 30 --from 0 --to <dur> --out video.mp4     # muted picture
uv run sound-layer/scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
uv run sound-layer/scripts/qa.py out/final.mp4
```
Long films rendered in parts: concatenate the silent parts first (`concat -c copy`, check frame count).
mix.py then makes **one** mix for the whole film. Never mix per part.

## 4 · Verify (≤ 2 fix rounds)
Fix every FAIL by changing **cues or sounds**. Never touch `sound-layer/`, never raise a threshold, never
declare a fake `silence_ok`.

| FAIL | Usual cause | Fix |
|---|---|---|
| `audible <id>` | masked by music/VO in its band | brighter/darker sound from `browse`, move it off a dense moment, or drop it |
| `hero body <id>` | thump too thin for the bed | deeper `thump/<id>+tap` (look at the sheet: energy at 125–500 Hz) |
| `picture <id>` (hero) | wrong tag or a weak visual event | re-tag (`appear` for a pop-in during a camera move), or give the hero a decisive stop |
| `sync <id>` | slow attack / long pre-roll | a sound with a sharper rise (browse shows `rise`) |
| `voice` | music too loud under VO | raise `duck_db`, `energy: calm`, or a sparser loop |
| `silence` | gaps with no music/room | a music bed or room tone; `silence_ok` only for silences you planned |
| `loudness` / `true peak` | encode changed the audio | mux with `-c:a aac -b:a 256k` exactly; don't re-normalise |

Then **open `audio/qa.png`** and write, for each hero cue, what you see. In the waveform, look for a dead stop before the hero.
In the spectrogram, look for a broadband stroke on the red line. In the motion curve, look for a peak or settle on the line.
Release copies: `../tools/encode_release.sh out/final.mp4 out/final` re-encodes 1080p/720p (audio
copied) and runs qa.py on each file. Heavy compression can move the measured landing.

## 5 · Deliver
- `out/final.mp4` (+ `final_1080p/720p.mp4` from `encode_release.sh`) on the GitHub Release.
- `audio/kit/CREDITS.md` → keep only the sounds actually used (from `audio/mix-report.json` → `files`) plus
  the music credit, in `docs/CREDITS.md`.
- `LISTEN.md` (template `templates/LISTEN.md`): 5 timecodes for a human ear check. Include each hero, every
  warning, and the densest moment.
- Report **what the checks show**: pass/warn/FAIL counts, loudness, true peak, rounds used, what you saw at the heroes in
  qa.png. Never call the sound "good"; the human decides that.
- Commit `audio/cues.json`, `audio/sound.json`, `audio/qa-report.json`, `audio/mix-report.json`,
  `audio/qa.png`, `LISTEN.md`. Never commit `audio/kit/`, `audio/stems/` or `sound-layer/`, which are rebuilt by setup.

Worked example with real measurements: [`examples/demo/sound/`](../examples/demo/sound/README.md).
