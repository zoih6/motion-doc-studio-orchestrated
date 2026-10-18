# v3 — Sepia Manuscript Cinema · Style & Composition Rules

## Look
- Base: dark walnut desk plate (AI generated, `assets/v3/plate_*`) under god‑ray light, vignette, warm grade.
- Surfaces: torn parchment cards with fibre edges + soft drop shadow; light paper gets a cream veil.
- Portraits: painterly‑realistic sepia (AI, historical style) on torn parchment, never full colour.
- Real artefacts: Hijazi (Birmingham), Kufic, Tumar, Ibn al‑Bawwab, Baysunghur Muhaqqaq, Ottoman thuluth panel.
- Accent: one gold (`#c99a45`; `#86520f` when drawn over parchment for contrast).

## Type
- Display: Amiri Bold (names, statements). UI/captions: Noto Kufi Arabic. Hero word: real thuluth ink asset.
- Global scale `TS=1.3`; minimum caption 26px @1080p. All text typeset by us (never baked into AI images).

## Grid & framing
- 1920×1080, safe margin 96px. Rule‑of‑thirds anchors x=640/1280, y=360/720.
- One hero + one text card + max two supporting elements per shot.
- Card lives in the empty third opposite the subject (portrait right → name left with a faint gold geometry halo).

## Motion
- Everything springs (no linear fades); RTL entrances (from right), exits to left.
- Shot change = parchment tear / slide, never a hard cut. New idea every ~3 s, hook in first 2 s.
- Slow camera drift (1–3 %) on every shot; push‑ins only toward the subject of the VO line.
- Render is a pure function of t (seeded RNG only).

## Narrative
- Each VO sentence → one visual idea; on‑screen words echo only the key noun (name, date, rule).
