# Motion vocabulary — named techniques with code

All functions are in `engine/core.js` / `engine/helpers.js`. `t` = current time, `t0` = start (VO word time).

## Entrances
| Name | Use for | Code |
|---|---|---|
| **Card drop** | any text card; lands like a sheet on a desk, then text writes on | `drawCard(cd, t, t0, x, y, {rot, from:'drop'\|'right'\|'left', t1})` |
| **Photo drop** | artefacts, portraits, prints | `const r = dropP(photo(img, w, {crop}), t, t0, x, y, rot, id, {from, t1})` |
| **Slide-in RTL** | lists, timelines in Arabic | `from: 'right'` (enters from the right, exits left) |
| **Stagger list** | N items, one per beat | `staggerIn(items, t, t0, .25)` or loop with `t0 + i*step` |
| **Snap dot** | measurement units, bullets, ticks | `nuqta(g, x, y, size * sp(t, t0, 'snap'), color)` |
| **Cut-out object** | crown, compass, pen, tools (alpha PNG with shadow) | `drawCut(cutout(img), x, y, w, {rot, lift})` |
| **Soft rise** | heroes, crowns, finale words | `k = sp(t, t0, 'soft')`; scale `lerp(1.15, 1, k)`, alpha `clamp(k*2)` |

## Text
| Name | Use for | Code |
|---|---|---|
| **Write-on RTL** | every caption/name | `writeOn(textImg([...]), x, y, easeOut(t0, t0+.7, t))` |
| **Name block** | person intro: name / divider / role / dates | `nameBlock(textImg([{t:name,size:116},{divider:300},{t:role,size:40,font:UI}]), t, t0, x, y)` |
| **Ink stroke reveal** | calligraphy hero word written in stroke order | order-map technique (see examples/thuluth/code/ink3.js + `prep_assets` note below) |
| **Counter** | numbers that matter (years, counts) | `liveText(counter(t, t0, t1, 0, 1200), x, y, 96)` |
| **Gold word** | finale / climax | `goldify(textImg(...))` then soft rise + rays |
| **Stamp** | verdicts ("not a calligrapher", "forbidden") | dark/red card with `snap`, `shake(t, t0, 6)`, SFX stamp |

## Explaining / measuring
| Name | Use for | Code |
|---|---|---|
| **Dot ruler** | "measured in dots": stack rhombus dots beside a letter/object | loop `nuqta` with `t0 + i*.085` |
| **Construction geometry** | proportions, design systems, sacred geometry | `line(pts, p)`, `arc(cx, cy, r, p)`, `geoHalo()` |
| **Compass draw** | circle construction with a cut-out compass rotating as the arc grows | rotate `drawCut(compass)` by the arc angle |
| **Pin-on-photo** | marks glued to a real image while the camera pushes | `const M = plateM(img,...); M.map(px,py)` / `onPiece(p, r, fn)` |
| **Callout** | point at a detail and name it | `callout(x0, y0, x1, y1, t, t0)` + a small tag card |
| **Error blot** | "one small mistake ruins everything" | `blob(x, y, r, seed, PAL.ink)` growing with `sp`, + red ring |
| **Split/compare** | before/after, right/wrong | two cards side by side, wrong one gets a red X `line` |
| **Balance bar** | "balance", "void vs fill" | `line` beam + `nuqta` sliding with `spring(t - t0, 60, 9)` |
| **Scan sweep** | digitisation, analysis | bright bar moving across an image with a clip revealing the "processed" version |
| **Vector reveal** | "curves", "digital" | outline + anchor points + handles drawn with `line`/`arc` over the word |

## Camera & space
| Name | Use for | Code |
|---|---|---|
| **Plate drift** | every background | `plate(img, t, a, b, {s0:1, s1:1.06, fx0, fy0, fx1, fy1, dim})` |
| **Push to subject** | when the VO names a detail | `camOn(lerp(1, 1.12, ease(a, b, t)), fx, fy)` … `camOff()` |
| **Breathing** | keep holds alive | built into cards/photos via `breathe(id, t)` |
| **God rays** | atmosphere, sacredness, reveal | `rays(t, {x, y, ang, n, int})` |
| **Grade** | unify everything | `grade(t)` (warm soft-light, 12 fps grain, vignette) — automatic |

## Transitions
| Name | Use for | Code |
|---|---|---|
| **Paper tear RTL** | default shot change (history = turning pages) | automatic between SHOTS (`tin:'tear'`), 0.62 s |
| **Hard cut** | on a hard beat ("But…", a stamp) | `tin: 'cut'` |
| **Exit up/left** | clear the stage before the next idea | `t1` param of drawCard/dropP |
| **Match on motif** | continuity between sections (the dot becomes the crown's jewel) | end shot A and start shot B with the motif at the same position/scale |

## Ink stroke-order reveal (calligraphy / handwriting)
1. Get a high-res ink image of the word (real scan or verified generation), alpha = darkness.
2. Label connected components; choose the writing order of components and the start pixel of each.
3. Compute geodesic distance inside each component from its start → normalise into time segments → save as an
   8-bit "order map" PNG. Dots/diacritics get late segments.
4. At runtime: pixel alpha = ink alpha × clamp((p·255 − order)/7). Cache per p. (See examples/thuluth/code/ink3.js.)

## More techniques
The pro layer `engine/fx.js` adds 16 transitions, 8 kinetic-type modes, a 2.5D camera rig, post FX and
graphics primitives — see library/transitions.md, kinetic_typography.md, camera_language.md, compositing_fx.md.
