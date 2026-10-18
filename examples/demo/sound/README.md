# Demo · Sound Layer worked example (real output, nothing staged)

The 16 s engine demo (`engine/index.html` + `engine/scenes/demo.js`) taken through the SOUND LAYER prompt
(`skills/motion-sound-layer/PROMPT.md`) with the pinned, unmodified `vendor/opus-sound-layer`.
Watch: [`../demo_16s.mp4`](../demo_16s.mp4) (720p, with sound) · 1080p: release asset `demo_sound_layer_1080p.mp4`.

| File | What it is |
|---|---|
| `sound.json` | the non-cue part of the cue sheet: energy punchy (−14 LUFS), CC0 music loop, duck 10 dB |
| `cues.json` | exported by `tools/export_cues.mjs`, with 13 cues **computed** from the scene's springs/easings (`src` says from which) |
| `mix-report.json` | what mix.py placed: files per cue, gain, band, peak time |
| `qa-report.json` · `qa.png` | qa.py on `out/final.mp4`: 42 pass · 3 warn · 0 FAIL |
| `qa-final_1080p.json` · `qa-final_720p.json` | qa.py on each release encode (`tools/encode_release.sh`): 0 FAIL |
| `browse_paper.png` | the LOOK step: `sfx.py browse --type paper` sheet used to choose the tear sound |
| `CREDITS.md` · `LISTEN.md` | deliverables: credits for the files actually used, plus 5 timecodes for the human ear |

## Reproduce (≈ 15 min, mostly the render)
```bash
cd engine
../tools/sound_layer.sh setup . && ../tools/sound_layer.sh kit .
mkdir -p audio && cp ../examples/demo/sound/sound.json audio/
curl -L -o audio/music.mp3 https://cdn.freesound.org/previews/727/727919_12708796-hq.mp3     # CC0 loop (Ehved)
PAGE=index.html node ../tools/export_cues.mjs
PAGE=index.html node ../tools/render.mjs --fps 30 --from 0 --to 16 --out video.mp4
uv run sound-layer/scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
uv run sound-layer/scripts/qa.py out/final.mp4
../tools/encode_release.sh out/final.mp4 out/final
```
(`engine/audio`, `engine/sound-layer`, `engine/out` and `video.mp4` are git-ignored.)

## What the QA rounds changed (only cues, sounds and one picture fix, never the scripts)
| Round | qa.py said | Change |
|---|---|---|
| first mix | 4 FAIL: `audible tear-rule` 1.1 dB, `audible dot-6` 0.4 dB, `audible caption` 0.8 dB, `hero body end` 2.7 dB | — |
| 1 | → 0 FAIL, 3 warn | tear-rule → brighter `paper/…packaging-paper-rub-sliding-1`. Dots 3 pops → 2. Caption re-tagged `appear` (the camera push in shot 2 never "stops") with `tap/…wood-knock`. Hero → deeper thump |
| 2 (release check) | 1080p/720p encodes: `picture end` FAIL, landing measured 5 frames early | The `soft` spring's settle was too gradual: compression noise moved the measured stop. Hero now uses the `card` spring (decisive stop). Re-rendered 12–16 s |
| new cut, 1 | `hero body end` 3.0 dB (needs 3) | thump → `thump/…thump-on-carpet-2` (196 Hz) → 3.7 dB. **0 FAIL on master, 1080p and 720p** |

## What qa.png shows at the heroes
- **title, 0.633 s:** the motion curve spikes at 0.35 s (card drop) and settles to baseline exactly on the red line.
  There is a broadband vertical stroke on the line while the music bed is still sparse.
- **end, 12.800 s:** the waveform is flat from ≈12.45 s to 12.75 s (the `stop_before` dead stop). Only the narrow
  tear stroke (12.33 s) and the riser show in that window. A broadband stroke sits on the red line, then the music returns
  at full width. In the motion curve, the tear peak at 12.33 s decays to baseline at the line.

The remaining warnings are support cues: the kicker tap lands while its text is still writing on, and the dots are
too small for the 160×90 motion curve. They are listed in `LISTEN.md` for the human ear check.
