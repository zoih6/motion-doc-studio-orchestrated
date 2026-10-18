# 04 · Assets — real first, AI for gaps, processed to one look

## 0. Asset plan (`docs/assets.md`)
For every shot in the shot list: what the hero needs, source type, resolution needed (≥2× on-screen size
for push-ins), status. Group AI generations into **batches of ≤10** (tool limits), most important first.

## 1. Real assets (preferred — clients notice and value authenticity)
- Wikimedia Commons (`tools/commons.py search "…"`, then `get`), museum open access (Met CC0, Walters,
  Freer/Sackler, Rijksmuseum, LoC, British Library PD), national archives. See `library/asset_sourcing.md`.
- Check licence (PD / CC0 / CC BY / CC BY-SA → credit). `docs/CREDITS.md` is updated automatically.
- Download the largest version; store originals in `assets/real/`, crops in `film/assets/`.
- Crop to the meaningful region; record crops as `[x, y, w, h]` in **original pixels** in code so they can be
  re-cropped later. Measure key features (an alif, a face, a date) in image pixels for pinned overlays.

## 2. AI-generated assets (gaps only)
Use for: historical portraits with no photo (state "AI reconstruction" if relevant), atmospheric plates
(desk, workshop, city skyline, mosque interior, lab), objects to cut out (crown, compass, pen, tools),
paper/texture plates. **Never** for text, maps with labels, data, or real artefacts that exist.
- Use `library/prompt_templates.md`; one style suffix for the whole film (consistency!).
- Generate at 16:9 for plates, 4:5 for portraits, plain contrasting background for cut-outs.
- Review each image: anatomy, anachronisms, fake text (remove/cover), style match. Regenerate if off.
- Offer the user choices only for hero images; batch the rest.

## 3. Processing
- Upscale small images (Lanczos ×2 is fine for plates under the grade; avoid >2×).
- Cut-outs: `tools/cutout.sh in.png out.png` (rembg isnet-general-use, one process per image) → trim bbox.
- Colour: let the engine's grade unify; for strong outliers pre-tint (sepia multiply) in PIL.
- Text-free versions: paint out fake letters in generated images (inpaint or crop).
- Name files by role: `plate_desk.jpg`, `por_<name>.jpg`, `cut_crown.png`, `real_<artefact>.jpg`.
- Keep raw generations out of git if huge; commit processed assets (each < 5 MB; JPEG q88 for plates).

## 4. Fonts
Local TTF/OTF only (OFL/open licences), declared with `@font-face` in `index.html` and preloaded via
`window.FILM.fonts`.
