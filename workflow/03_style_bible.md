# 03 · Style bible — `docs/STYLE.md`

Write it before building. Keep it to one page. Template:

```markdown
# <Film> — <Style name>
## Look
- Base/background: …            - Surfaces: …           - Light: …
- Portraits: …                  - Real artefacts: …      - Grade: warm/cool, grain, vignette
## Palette   bg #…  surface #…  ink #…  accent #… (+ dark/light variants)  alarm #…
## Type      Display: …  UI: …  Hero word: …   TS = 1.3, min caption 34 px
## Grid      1920×1080, 96 px margins, thirds anchors 640/1280 · 360/720
## Density   1 hero + 1 card + ≤2 supports
## Motion    presets card/snap/soft = […]; entrances: …; transitions: …; camera: …
## Narrative motif: …
## Do / Don't (specific to this film)
```

## How to derive it from references
1. Sample 5 colours from each reference (background, surface, ink, accent, highlight); unify into the palette.
2. Name the surface material (torn parchment, flat paper, glass, blueprint) and the light (god rays,
   soft top light, flat).
3. Decide portrait treatment (painterly sepia, engraving, flat vector, photo duotone).
4. Map to engine settings: `window.FILM.palette`, fonts, `grade()` tint, `paper()` options, `rays()`.
5. Make a **style frame**: one fully finished still (hero + card + plate) and show it in the first sample.

Ready-made bibles: `library/style_presets.md` (6 deep presets) and **`library/style_catalog.md` (40 styles mapped to engine values: palette key, fonts, persona, moves, transitions, look, pattern)**. Real example: `examples/thuluth/STYLE_v3.md`.

## Pro checklist (v1.1) — fill these lines in STYLE.md too
- **Motion language:** persona · signature curve · exit curve · base unit · springs · transition family + accent
  · stagger · hold → `library/easing_timing.md §0`
- **Palette in OKLCH** with roles (60/30/10, tinted neutrals, rare pop) and `contrast()` checks → `library/color_systems.md`
- **Palette source:** `heritage('<key>')` or a filtered `palette(i)` → `paletteRoles()` (`library/color_systems.md §8`)
- **Pattern family (optional):** one `pattern()` kind (`library/patterns.md`)
- **Type roles:** caption / emphasis / display / meta faces from the 41 bundled families in `library/fonts.md`; kinetic modes → `library/kinetic_typography.md`
- **Camera:** depth planes + allowed moves → `library/camera_language.md`
- **Look per register:** `FILM.post` chain → `library/compositing_fx.md`
- From a reference video: run `tools/video_dna.py` first → `workflow/09_reference_dna.md`
