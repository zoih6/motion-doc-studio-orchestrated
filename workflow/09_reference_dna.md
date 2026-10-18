# 09 · Reference DNA — learn a style from a video without copying it

Use when the user sends a reference video ("make it like this", "take its style"). Goal: a written,
measured style grammar you can apply to *new* content. Never reuse the reference's characters, brand,
script, jokes or exact layouts, and never commit the reference file itself.

## Steps
1. **Measure** (2 min; `FULL=1 tools/setup.sh` adds opencv + scikit-learn for flow/k-means):
   `python3 tools/video_dna.py REF.mp4 docs/ref_dna/` → `report.md` (format, letterbox, cuts, shot lengths,
   animated transitions with frame counts, flash/strobe frames, palette with OKLCH + coverage, loudness,
   VO/music balance, onsets/s), `metrics.json`, 4 fps contact sheets, one keyframe per shot (`shots.jpg`).
2. **Watch the sheets** (read the images) and fill the "Observed" half of `report.md`:
   - Format & framing (aspect, safe areas, letterbox?).
   - Typography: how many faces, their roles (caption / emphasis / display / meta), how emphasis is marked.
   - Colour roles: 60 / 30 / 10 split, tinted neutrals?, how many accents, where the rare colour is used.
   - Subject/character treatment: anchor position, shot sizes, lighting registers.
   - Layout: grid, recurring compositions (split screen, hero + caption, macro type…).
   - Motion grammar: entrance duration (count frames), overshoot, blur, camera behaviour, hold length.
   - Transition toolbox: list each kind with its frame count from the report.
   - Graphic vocabulary: recurring props (circles, bubbles, stickers, arrows, icons…).
   - Sound: VO share, bed level, SFX on transitions, silence used as tension.
3. **Beat map**: a table `t → shot/register → what happens → transition in` (see the example).
4. **Adopt / don't-copy table** — the contract that keeps you original.
5. **Engine mapping**: map every adopted element to an `engine/fx.js` / `core.js` call; anything missing →
   write it as a reusable function (not inline in a scene) and document it.
6. **Preset**: write a style bible entry (palette roles with hex + OKLCH, fonts by role from
   `library/fonts.md`, persona from `library/easing_timing.md`, transition family, look from
   `library/compositing_fx.md`) into `docs/STYLE.md` — or into `library/style_presets.md` if reusable.
7. Show the user a short summary of the DNA (5–8 bullets) before building, in their language.

## Worked example
`examples/reference_dna/` — DNA.md (full breakdown of a 20 s Arabic app ad), measured_report.md,
metrics.json, contact sheets, keyframes. Resulting preset: `library/style_presets.md` → F.

## Pitfalls
- Frame-count transitions from the sheets/metrics; eyeballing at 1× speed underestimates how short they are
  (most pro transitions are 4–10 frames).
- Letterboxed sources: analyse the active picture only (the tool crops automatically).
- Palette k-means over-weights backgrounds; read *roles*, not just percentages.
- A reference's loudness may be wrong (e.g. true peak −0.3 dBFS); keep our audio rules.
