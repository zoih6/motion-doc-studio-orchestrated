# Compositing, blend modes & finishing effects

Code: `engine/fx.js` §5–6. Apply finishing in `FILM.post = t => fxLook(t, 'film')` (or a custom chain);
per-section looks: `post: t => t < 30 ? fxLook(t, 'film') : fxLook(t, 'pop')`.

## 1 · Blend modes (canvas `globalCompositeOperation`)
| mode | effect | use it for | avoid |
|---|---|---|---|
| `source-over` | normal | everything by default | — |
| `multiply` | darkens, white disappears | paper/texture over art, ink, shadows, scans on paper | dark-on-dark |
| `screen` | lightens, black disappears | light rays, leaks, fire, glows, bloom | bright bg |
| `overlay` | contrast; darks darker, lights lighter | grain, texture, punchy colour wash | skin close-ups |
| `soft-light` | gentle overlay | warm/cool grade washes (sepia), subtle texture | — |
| `color-dodge` / `lighter` | intense additive light | sparks, lens hits, additive channels (CA) | large areas (blows out) |
| `color-burn` | intense dark contrast | burnt paper edges, vignette tint | — |
| `hard-light` | strong overlay | duotone posters | text |
| `difference` / `exclusion` | inverts by luminance | glitch, graphic inversions on beats | readable text |
| `hue` / `saturation` / `color` / `luminosity` | component swaps | recolour a photo to the palette (`color`), desaturate (`saturation`) | — |
| `source-in` | keep src inside dst alpha | tinting (`tint()`), clipping images into text | — |
| `destination-in` / `-out` | mask / cut-out | masks, wipes, holes, luma mattes | — |

## 2 · Finishing effects (fx.js)
| effect | call | typical values | notes |
|---|---|---|---|
| film grain | `fxGrain(t, amt, blend, fps)` | .03–.06 clean, .08–.12 film; 12–24 fps | always a little: kills banding, glues CG |
| vignette | `fxVignette(amt, {inner, cx, cy, color})` | .15–.25 flat styles, .45–.66 cinematic | colour-tinted vignettes unify |
| bloom | `fxBloom(strength, radius)` | .3–.5, 14–26 px | highlights only (self-multiply isolation) |
| halation | `fxHalation(strength, radius)` | .2–.35, 8–12 px | red-orange edge glow of film stock |
| chromatic aberration | `fxChroma(amt, 'lens'|'shift')` | 1.5–3 px lens; 3–6 shift for VHS | full-frame cost ×3, use on short beats |
| light leak | `fxLeak(t, {int, colors, seed})` | .15–.35 | warm drifting blobs, nostalgia/dream |
| LGG grade | `fxGrade({lift, gamma, gain, contrast, sat, shadows, highlights, split})` | split .1–.18 | ~25 ms/frame @1080p |
| sepia house grade | `grade(t)` (core) | — | the Thuluth look |
| element RGB split | `rgbSplit(img, x, y, amt)` | 4–8 px | text emphasis only |
| offset echo / extrude | `echo()`, `extrude()` | 6–14 px | sticker-3D type |
| sticker outline | `outline(img, px, '#fff')` | 8–12 px | die-cut look for cutouts |
| pixelate | `pixelate(img, block)` + `drawCrisp()` | 4–8 px blocks | pixel-art characters/icons |
| motion blur | render `--sub 2` (+ `smearDraw` for whips) | — | never on text that must be read |
| depth of field | `layer()` with `CAM.ap`, `CAM.fd` | 6–10 px max | rack focus, depth |

## 3 · LOOKS presets
| look | chain | for |
|---|---|---|
| `sepia` | core warm soft-light + grain + vignette | heritage documentary |
| `clean` | grain .035 | UI, data |
| `pop` | grain .045 + vignette .18 | flat sticker / explainer |
| `film` | halation + grain 24 fps + vignette .45 | cinematic beats, dark registers |
| `tealOrange` | LGG split-tone teal shadows / orange highlights + grain + vignette | modern cinematic |
| `noir` | desaturate, contrast 1.25, heavy grain, vignette .6 | crime, archive |
| `dream` | bloom + light leak + grain | memories, flashbacks |
| `vhs` | shift CA + heavy grain | retro, internet culture |

## 4 · Rules
- Effects serve the story beat; a look per **register**, not per shot.
- Banned (still): glow on UI text, generic bokeh/particles, lens flares as decoration, CA on body captions.
- Effects never reduce caption contrast below 4.5:1 — check a still after the look.
- Heavy effects (fxGrade, fxChroma) cost render time — budget them, and never re-create buffers per frame
  (fx.js caches buffers, LUTs, tints).
