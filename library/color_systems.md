# Colour systems (palettes, OKLCH, grading)

Code: `engine/fx.js` §3 — `oklch(L,C,H)`, `mixOK(a,b,k)`, `contrast(a,b)`, `rgba(hex,a)`; §6 `fxGrade`, `LOOKS`.
Measure a reference's palette: `tools/video_dna.py` (hex + coverage + OKLCH). Sources: iart-ai color-motion,
Björn Ottosson's OKLab, WCAG 2.2.

## 1 · Build a palette (restraint)
- **1 primary/accent + 1 rare pop + 2–3 neutrals.** Depth comes from lightness and chroma, not more hues.
- **60 / 30 / 10:** light (or dark) neutral 60 %, opposite neutral 30 %, accent 10 %; pop colour ≤ 1–2 %
  and only on a beat.
- **Tint the neutrals** toward the film's temperature (warm cream `#f8f4e9`, warm black `#1c1917`) — pure
  #fff/#000 next to colour looks disconnected and cheap.
- **Temperature contrast:** one cool accent on warm neutrals (or the reverse) reads instantly.
- On dark backgrounds an accent pops by **high lightness, moderate chroma** — max saturation vibrates.
- Think in OKLCH: same L and C with different H = hues of equal visual weight (impossible in HSL).
```js
const accent = oklch(.64, .11, 196);           // teal, L .64
const pop    = oklch(.82, .15, 80);            // warm yellow, lighter so it pops
const cream  = oklch(.97, .016, 89), ink = oklch(.22, .007, 51);
contrast(ink, cream)   // → ≥ 4.5 for captions
```

## 2 · Interpolate perceptually
Animating colours in sRGB passes through grey/mud (blue→yellow = grey). Use `mixOK(a, b, k)` for every
animated colour, gradient stop and theme wash. Colour state changes: 150–300 ms `CURVE.expoOut`; full-frame
washes 400–800 ms.

## 3 · Gradients that read premium
Mesh = several radial gradients over a base, slow drift (8–20 s), plus 3–5 % grain to kill banding.
Fast-moving gradients look like screensavers.

## 4 · Grading order (fxGrade does steps 1–4 in this order)
1. exposure / white balance (gain) → 2. contrast / black & white points (lift, contrast) → 3. midtones &
saturation (gamma, sat) → 4. split-tone (shadows / highlights tints) → 5. unify (look, vignette, grain).
Grade the whole film consistently so shots cut together.

## 5 · Curated palettes (hex · role)
| name | bg | ink | accent | pop | extra | mood |
|---|---|---|---|---|---|---|
| Sepia Manuscript (A) | #0c0906 | #24180e | #c99a45 gold | #a8321f red | parch #e8d7b2 | heritage, gravitas |
| Sticker-Pop (F, DNA) | #f8f4e9 | #1c1917 | #05a1a2 teal | #f8bb3e yellow | panel #e5e4d5, night #080706 | witty, social |
| Clean VOX (C) | #f4f1ea | #1b1b1b | #f2c94c | #eb5757 | blue #2f80ed | news, data |
| Dark Archive (D) | #0b0b0c | #d9d4c7 | #b3261e | #e6c15a | — | investigation |
| Blueprint (E) | #0d2a4a | #e8f1ff | #ffb000 | #58c4ff | — | tech |
| Desert Night | #14100c | #f3e6cf | #e07a3f ember | #7fb3c8 | sand #c9a46a | Arabia, travel |
| Nile Paper | #efe6d2 | #22303a | #1f7a6d | #d9573b | ochre #c99b4a | culture, education |
| Neo Mono | #0f0f10 | #f2f2f2 | #c6ff3d acid | — | grey #8a8a8a | tech launch |
| Soft Editorial | #f6efe9 | #2a2320 | #c2583d terracotta | #2f5d50 | blush #e9c9bd | lifestyle, food |
| Midnight Data | #0a1020 | #e6ecff | #4cc9f0 | #f72585 | violet #7209b7 | data, future |
Always validate: `contrast(ink, bg) ≥ 4.5`, accent on bg ≥ 3 for display text.

## 6 · Colour = meaning
Assign semantic roles and never break them: e.g. accent = "the thing we talk about", red = error/danger,
green = success, grey = past/inactive. Colour coding across a film is a narrative tool (VOX).

## 7 · Delivery colour management
Render in sRGB canvas → encode H.264 **tagged BT.709** (`-colorspace bt709 -color_primaries bt709
-color_trc bt709`), verify with `ffprobe`. Approve in Chrome/VLC, never in QuickTime (gamma shift).
Limited-range banding in dark gradients → add grain before encoding.

## 8 · Palette packs (v1.2) — vendored + original
Code: [`engine/assets.js`](../engine/assets.js) §1 · data: `engine/kit/data/palettes.js` · sheet: [specimens/palettes.jpg](specimens/palettes.jpg)
- **HERITAGE** (20 original named palettes with roles): `sanaaOldCity`, `iznikTile`, `mamlukGold`, `andalusZellige`, `damascusNight`, `ottomanManuscript`, `desertDune`, `hijazCoral`, `saffronIndigo`, `palmyraStone`, `nileReed`, `kufiBlueprint`, `voxExplainer`, `newsroom`, `archiveSepia`, `riso`, `neonNoir`, `swissPoster`, `forestData`, `pastelEdu`.
  `heritage('mamlukGold')` returns `{bg, ink, paper, accent, accent2, muted}`.
- **NICE_PALETTES**: the 1000 most-loved ColourLovers palettes (MIT, Jam3). `palette(i)` → 5 hex values; `paletteRoles(p)` assigns bg/ink/accent automatically, with ink ≥ 4.5:1 contrast guaranteed (it falls back to off-white/off-black if needed).
  Use `palettesBy({dark:true, minChroma:.12, hue:[20,70]})` to filter by mood.
- **OPEN_COLOR**: 15 hues × 10 shades (MIT). `oc('teal', 7)` gives UI-grade neutrals and data series.
- Apply to the engine: `applyPalette(heritage('iznikTile'))` (or `applyPalette(paletteRoles(palette(42)))`) inside a scene `INITS` function. It maps the roles onto `PAL` keys, so all core helpers recolour.
- Rule: a found palette is a **starting point**. Still fix one accent, run `contrast()`, and keep 60/30/10.
