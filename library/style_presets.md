# Style presets (ready style bibles — pick one, then adapt)

## A · Sepia Manuscript Cinema  (used in the Thuluth film v3 — approved, the strongest)
- **When:** history, heritage, religion, art history, biographies of old masters.
- **Look:** dark walnut desk/workshop plates under god rays; torn aged parchment cards with burnt edges;
  painterly-realistic sepia portraits on torn parchment; real manuscripts; faint gold construction lines.
- **Palette:** bg #0c0906 · ink #24180e · parchment #e8d7b2 · cream #f1e4c4 · gold #c99a45 (light #e9c77c,
  deep #86520f for lines on parchment) · alarm red #a8321f.
- **Type:** Amiri (display) + Noto Kufi Arabic (UI). Latin pair: Cormorant Garamond + Inter.
- **Motion:** card [150,19] · snap [320,28] · soft [60,15]; RTL paper tears; slow pushes; dots land with snap.
- **Grade:** warm soft-light rgba(214,150,70,.22), grain 9 %, vignette .66.

## B · Paper Collage (v1 of the Thuluth film)
- **When:** playful explainers, culture, kids/education, social formats.
- **Look:** flat torn coloured papers (cream, black, kraft, red, gold leaf), tape, stop-motion breathing at 12 fps,
  cut-out photos with white borders, hand-drawn circles/arrows.
- **Palette:** cream #efe4cc · black #151210 · kraft #b98c5a · red #c0392b · gold #d4a64a.
- **Motion:** paper boil (12 fps jitter), tape-in, hand-circle reveals; snappier springs.

## C · Clean VOX Explainer
- **When:** news, economics, science, data, geopolitics.
- **Look:** off-white paper background with subtle grain, flat vector maps and charts, archival photos as
  duotone cut-outs, highlighter marks, one bold accent.
- **Palette:** bg #f4f1ea · ink #1b1b1b · accent #f2c94c (or brand) · secondary #2f80ed · alarm #eb5757.
- **Type:** a bold grotesk (Inter Tight / IBM Plex Sans Arabic) + a serif for quotes.
- **Motion:** quick snaps for data, highlighter wipes, map pushes, number counters, line charts drawing on.

## D · Dark Archive Documentary
- **When:** true crime, war, investigations, mysteries.
- **Look:** near-black backgrounds, grainy archival photos with film-burn edges, red string connections,
  typewriter labels, redaction bars, flashlight-like vignettes.
- **Palette:** bg #0b0b0c · paper #d9d4c7 · accent red #b3261e · highlight #e6c15a.
- **Motion:** slow, heavy pushes; stamps; flicker only on transitions; red lines connecting evidence.

## E · Blueprint / Tech
- **When:** engineering, architecture, inventions, AI/tech history.
- **Look:** deep blue grid, white hairline drawings that construct themselves, measurement callouts,
  exploded views, photos as cyan-tinted inserts.
- **Palette:** bg #0d2a4a · lines #e8f1ff · accent #ffb000 · secondary #58c4ff.
- **Motion:** draw-on lines (path reveal), dimension arrows, rotating parts, snap-to-grid.

## F · Sticker-Pop Dialect Ad  (DNA measured from a reference — examples/reference_dna/DNA.md)
- **When:** short social ads/explainers in a spoken dialect, app/product promos, witty PSAs, 15–60 s.
- **Look:** flat warm-cream world; ONE pixel-art (or flat) character anchored bottom-left whose shot size
  changes (corner → bust → extreme close-up); rounded split-screen panels; polaroid stickers; pixel icons;
  phone mock with a living feed; speech/thought bubbles with hard shadows; hand-drawn circles.
- **Two registers:** bright flat (info/comedy) ↔ dark warm under-light close-up (set-up & punchline).
- **Palette (60/30/10):** cream `#f8f4e9` + panel `#e5e4d5` · ink `#1c1917` + night `#080706` · accent teal
  `#05a1a2` (oklch .64 .11 196) · pop yellow `#f8bb3e` (≤1 %, beat strobes only). Tinted neutrals, never pure.
- **Type:** caption Noto Kufi 800 (word-by-word) · emphasis word Aref Ruqaa in teal (one per line) · display
  Lalezar with teal offset `extrude()` · meta Plex Mono `// tags` and dictionary glosses · rebus icons.
- **Motion:** persona `stickerpop` — entrances 0.17–0.3 s, snap/wobbly springs, 5–10 % overshoot, motion
  blur; text beat every ≈0.5 s, shots 2–3 s; holds 0.3–0.5 s with ambient life (twinkle, cursor drift).
- **Transitions (≤10 frames):** hard cut on register switch · `zoom` punch-in to a circled detail · `whip` ·
  `smear` word morph · `flash` 3-frame impact · caption-card colour strobe on the beat · panel builds.
- **Hook:** ≤0.3 s (strobe/bubble/pop), **end card** builds in 1 s: logo, icon pin, tagline, pill CTA,
  cursor glides + click ripple, stickers settle; hold 2–3 s alive.
- **Look:** `fxLook(t,'pop')` for bright shots, `fxLook(t,'film')` for the dark register.
- **Sound:** VO-led, light bed that swells on the end card; whoosh on whips, thump on zooms, hit on flashes.
- **Don't:** reuse the reference's character/brand/jokes; more than one pop colour; captions over the face.

### Mapping a preset to the engine
`window.FILM = { palette: {bg, ink, parch, cream, gold, goldL, goldD, red}, display, ui, typeScale }`,
plus: `grade()` tint, `paper()` cream veil/burn, `rays()` intensity, textures in `kit/textures/`.
For light styles (C), set light `bg`, lower vignette, use `paper()` with `burn: 0` and flat cards.
Flat/digital styles (C, E, F): load `fx.js`, set `FILM.post = t => fxLook(t, 'pop'|'clean')` (replaces the
sepia grade), `FILM.tin = 'cut'` (or a TRANS key), and use fx.js panels / words / stickers instead of paper.
```js
window.FILM = { palette: { bg:'#f8f4e9', ink:'#1c1917', teal:'#05a1a2', sun:'#f8bb3e', night:'#080706', gold:'#05a1a2' },
  display:'Lalezar', ui:'Kufi', typeScale:1.3, tin:'cut', whipDir:1,
  fonts:['800 60px Kufi','700 60px Ruqaa','400 60px Lalezar','500 30px Mono'],
  post: t => fxLook(t, 'pop') };
```
