# Design rules — composition, hierarchy, typography, colour

These are hard rules unless the style bible for the film explicitly overrides one (and says why).

## 1. Frame & grid (1920×1080)
- **Safe margin 96 px** on every side for all text and key subjects. Nothing important touches the edge
  unless it is deliberately bleeding off-frame (≥30 % outside).
- **Rule-of-thirds anchors:** x = 640 / 1280, y = 360 / 720. Put the hero's centre of mass or eye line on
  an anchor, not dead centre — centre is reserved for *statement* moments (single word, finale).
- **Opposite-third card rule:** subject in the right third → text card in the left third (and vice versa).
  For a portrait on the right, the name typography goes left with a faint gold construction halo behind
  the portrait.
- RTL films (Arabic, Persian, Urdu, Hebrew): the reading entry point is the **right**. First element enters
  on the right; secondary info flows leftwards.

## 2. Density (the #1 client complaint is "crowded")
- Per shot: **1 hero + 1 text card + ≤ 2 supporting elements.** Tags/labels count as supporting elements.
- ≤ 12 words on screen at once (≤ 7 is better). A card has 1–3 lines.
- If a sentence lists N items, reveal them **one per beat**, never all at once, and remove the previous
  layer before adding a 5th element.
- Negative space is a feature: ≥ 35 % of the frame should be "quiet" (background only).

## 3. Hierarchy
- One focal point per moment. Achieve it with **size (×1.6 steps), contrast, and motion** — the thing
  that moves last is what the eye follows.
- Type scale (before TS multiplier): h1 96 · h2 72 · h3 52 · caption 30 · tag 26. With TS=1.3 the minimum
  rendered caption is ≈34 px. Never smaller.
- Key nouns of the VO (names, dates, the rule, the number) get on-screen echo; filler words never do.

## 4. Typography
- **One display face + one UI face** per film (e.g. Amiri + Noto Kufi Arabic; Playfair + Inter). A third
  face only as a *specimen* (e.g. showing a historical script), never for UI.
- All text is set **live in code** (canvas), so it can write on, re-time and be corrected. Never rely on
  text inside generated images (it is usually wrong, especially Arabic).
- Line height 1.25–1.4; letter-spacing 0 for Arabic (never track Arabic).
- Dates/numbers: match the film's language (Arabic-Indic ٠١٢٣ for Arabic films) unless the brand says otherwise.

## 5. Colour
- Palette = background, surface, ink, **one accent** (+ one alarm colour for errors/"wrong", optional).
- Contrast ≥ 4.5:1 for text. Check every overlay: gold hairlines on light parchment disappear → use deep
  gold (#86520f) at ≥3 px; black ink on dark backgrounds is invisible → switch to cream.
- Grade the whole frame once at the end (warm soft-light, grain, vignette) so real photos, AI plates and
  vector shapes sit in the same world.

## 6. Surfaces & depth
- Everything that holds content is a physical object: torn parchment, card, photo print, cut-out object —
  with a soft drop shadow (offset grows with "lift" while it moves).
- 3 depth layers max: plate (background) · objects · overlays (lines/labels). Overlays stay thin and
  sparse.
- Light comes from one direction per shot (god rays / vignette agree with the plate's light).

## 7. Framing people & artefacts
- Portraits: chest-up, eyes on the upper third line, looking *into* the frame (towards the text).
- Real artefacts (manuscripts, maps, photos): crop to the meaningful part, then push in towards the
  detail the VO mentions. Pin overlays (rulers, circles, callouts) **in image pixels** so they stay glued
  during camera moves (`plateM().map`, `onPiece`).
- Show provenance quietly: a small caption tag (e.g. "Qur'an folio · 10th c.") under the artefact — not in a corner.

## 8. Narrative line (visual storytelling)
- Each section has a **visual thesis** (one metaphor), each sentence a **beat**, each beat **one action**.
- Recurring motif (a dot, a crown, a line) ties the film together and returns transformed in the finale.
- Escalate: scale and intensity grow towards each section's climax; the finale reprises the hook.
- Transitions carry meaning (tear = turning a page of history; push-through = going deeper; match-cut on
  a shape = continuity).

## Advanced (v1.1) — colour, type, finishing
- **Colour:** 1 accent + 1 rare pop + 2–3 *tinted* neutrals, 60/30/10; build and check in OKLCH (`oklch()`,
  `contrast()`), animate colours with `mixOK()` (never sRGB lerp). Colour = meaning; keep roles fixed.
  → library/color_systems.md
- **Type roles:** caption / emphasis (one word per line, accent colour, hand-lettered face) / display / meta
  (mono). Max 3 faces + meta. → library/fonts.md, library/kinetic_typography.md
- **Finishing:** one look per *register* (e.g. bright = `pop`, dark = `film`); grain always a little;
  effects must not drop caption contrast below 4.5:1. → library/compositing_fx.md
- **Registers:** a film may have two visual registers (e.g. bright info vs dark under-lit punchline) —
  switch with a hard cut on the beat, never blend them.
- **One subject, many shot sizes:** vary framing of the same character/object (wide → close-up → macro)
  instead of adding new elements. → library/camera_language.md §4
