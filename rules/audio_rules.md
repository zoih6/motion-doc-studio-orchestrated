# Audio rules (v2.0: SOUND LAYER)

Procedure: `workflow/10_sound_layer.md`. Canonical prompt: `skills/motion-sound-layer/PROMPT.md`.

1. **You can't hear, so you measure.** Sound is placed from the timeline, chosen by looking (waveform +
   spectrogram sheets), mixed by `sound-layer/scripts/mix.py` and judged by `qa.py`. A human does the
   final ear check from `LISTEN.md`. Never call the sound "good"; report what the checks show.
2. **Real recordings only.** CC0 kit (`sfx.py kit`, 1,139 sounds / 19 types), `sfx.py search` for gaps, or
   the user's own files. **Never synthesize hits, clicks or whooshes; no meme sounds.** (`tools/sfx.mjs`
   is legacy. At most, use it for an abstract drone bed, never for hits.)
3. **Cues come from the code.** `engine/cues.js` computes the frame from the same spring/easing the shot
   uses (`cue.land/move/cut/appear/hero`). `tools/export_cues.mjs` writes `audio/cues.json`. Never type frames.
4. **Sound only on real actions.** Tag each: `cut` (full-frame change) · `move` (frame of peak speed) ·
   `land` (frame motion stops) · `appear` (element pops in). Don't put two sounds on one action. Series → 2–3 sounds.
5. **One hero per ~4 s** (logo, reveal): `"thump+tap"` with `stop_before` and `build` (`cue.hero`).
   Heroes need a decisive stop: card/snap spring, a cut, or a fast move. A gradual `soft` settle can't be measured reliably.
6. **One sonic family per film**, matched to the style bible: paper + wood (manuscript/sepia), glass + air
   (clean tech), metal + sub (trailer). Pan = screen position (≤ ±0.6).
7. **VO is king.** VO goes in `voice` (mix.py → −16 LUFS, music ducked `duck_db`, default 10 dB). qa.py `voice`:
   music ≥ 8 LU under the voice. Music: the user's track or a CC0 loop, credited.
8. **Loudness:** `energy: punchy` → −14 LUFS (default for this studio), `calm` → −18. True peak ≤ −1 dBTP
   (mix.py limits at −2). **One mix for the whole film.** Concatenate silent parts first, never mix per part.
9. **Gates:** `qa.py` 0 FAIL on `out/final.mp4` and on every release encode (`tools/encode_release.sh`),
   ≤ 2 fix rounds per cut, fixing cues or sounds only. **Never edit `sound-layer/` or loosen a threshold**
   (`tools/sound_layer.sh verify`).
10. **Deliver:** final video, credits for every file actually used (`audio/mix-report.json` → files), `LISTEN.md`
    (5 timecodes: heroes, warnings, densest moment), and a written description of `audio/qa.png` at each hero.
