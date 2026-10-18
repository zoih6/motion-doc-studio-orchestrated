# Style catalogue — 40 production styles mapped to the engine · كتالوج الأساليب

Each style is a **ready recipe**: every value is something that exists in this repo (palette key, font family, MOVES name, TRANS key, LOOKS key, pattern kind).
Workflow: pick a style here, then write the film's style bible ([workflow/03_style_bible.md](../workflow/03_style_bible.md)). Deep presets with production notes: [style_presets.md](style_presets.md) (A–F).
Legend: **Pal** = `heritage('<key>')` from `engine/assets.js` (or `paletteRoles(palette(i))`) · **Type** = families in [fonts.md](fonts.md) · **Persona** = `PERSONA.*` · **Moves** = [motion_recipes.md](motion_recipes.md) · **Tin** = transition key ([transitions.md](transitions.md), [gl_transitions.md](gl_transitions.md)) · **Post** = `FILM.post = t => fxLook(t, '<key>')` · **BG** = `pattern()` kind.
Trend sources (2026): kinetic & elastic type, liquid glass, collage + stop-motion, hand-drawn texture, grain, retro-futurism, new minimalism, procedural pattern motion, maximalism (see [resources.md](resources.md)).

## Picker — by subject
| subject | first choice | alternatives |
|---|---|---|
| Islamic history, calligraphy, heritage | 1 Sepia Manuscript | 2 Mamluk Gold, 3 Iznik, 5 Andalusian, 9 Ottoman Archive |
| Poetry, Sufism, literature | 6 Persian Miniature Poetry | 8 Ink & Wash, 26 Editorial Essay |
| Architecture, cities | 4 Monument Geometry | 15 Blueprint, 17 Isometric City |
| Yemen / Arabia / Gulf | 7 Sanaa Gypsum | 10 Desert Dune, 11 Hijaz Coral |
| News, economics, geopolitics | 12 Clean VOX | 13 Newsroom Data, 14 Map Explainer |
| Science, tech, AI | 15 Blueprint | 19 Liquid Glass, 20 Neon Noir, 21 Retro-Futurism |
| True crime, war, investigation | 23 Dark Archive | 24 Redacted Dossier |
| Kids, education | 30 Pastel Edu | 31 Paper-Craft, 32 Chalkboard |
| Social ads, promos | 27 Sticker-Pop | 28 Riso Print, 29 Maximalist Collage |
| Biographies | 1 Sepia Manuscript | 25 Film Noir Portrait, 33 Scrapbook |

---
## A · Heritage & Islamic arts
**1 · Sepia Manuscript Cinema** (preset A, Thuluth film v3). Walnut desk plates, torn parchment cards, gold construction lines.
Pal `archiveSepia` · Type Amiri 700 / Kufi 600 · Persona documentary · Moves `dropIn` `riseIn` `drawIn` `hover` · Tin `tear`, `gl:FilmBurn` (rare) · Post `sepia` · BG `rosette` at 6% under parchment.

**2 · Mamluk Gold Illumination.** Black lacquer, gold tazhib borders, lapis-teal accents, square-kufi titles drawing on stroke by stroke.
Pal `mamlukGold` · Type Qahiri / Naskh / ReemKufi (emphasis) · Persona premium · Moves `drawIn` `unfoldIn` `blurIn` · Tin `iris` with gold ring, `gl:powerKaleido` (chapter) · Post `film` · BG `star12` gold 1.2 px draw-on.

**3 · Iznik Tile.** Frit-white ground, cobalt line-work, tomato-red accents. Panels slide like tiles snapping into a wall grid.
Pal `iznikTile` · Type Mirza / Tajawal · Persona corporate · Moves `flipInY` `staggerMove('popIn',{order:'center'})` · Tin `gl:hexagonalize`, `blinds` · Post `clean` · BG `rosette` cobalt 10%.

**4 · Monument Geometry.** Architecture explained through construction: compass arcs, star polygons growing into façades, measured callouts.
Pal `kufiBlueprint` or `palmyraStone` · Type Qahiri / PlexArabic / Mono · Persona documentary · Moves `drawIn` `unfoldIn` `zoomInUp` · Tin `zoom` (into a detail), `gl:polar_function` · Post `clean` · BG `girihNet` / `star8` as construction layer.

**5 · Andalusian Zellige.** Patio light, zellige green & ochre, horseshoe arches as frames (mihrab-shaped masks).
Pal `andalusZellige` · Type ReemKufi / Harmattan / Ruqaa · Persona premium · Moves `riseIn` `swingIn` `sway` (plants) · Tin `iris` (arch mask), `gl:Dreamy` · Post `dream` low · BG `star8`.

**6 · Persian Miniature Poetry.** Flat miniature planes, gold skies, verses in Nastaʿlīq, slow parallax.
Pal `ottomanManuscript` or nice palette filtered `palettesBy({hue:[30,70]})` · Type Nastaliq / Naskh / Gulzar · Persona premium · Moves `blurIn` `float` `fadeInRight` · Tin `gl:ripple`, `dip` · Post `film` · BG `rosette` faint.

**7 · Sanaa Gypsum & Qamariya.** Burnt-brick tower houses, white gypsum friezes, light through coloured qamariya glass.
Pal `sanaaOldCity` · Type ReemKufi / Cairo / Ruqaa · Persona documentary · Moves `riseIn` `dropIn` `hover` · Tin `gl:luminance_melt`, `push` · Post `tealOrange` low · BG `mashrabiya` white 8%.

**8 · Ink & Wash (Sumi-e/Hibr).** Ink blooms on paper, one brush stroke per idea, huge negative space. Ref: [anidoodle sumiE](../resources/skills/anidoodle-styles/styles/sumiE.md).
Pal monochrome `#f2ede1/#151515` + one red seal · Type Amiri / Naskh · Persona premium · Moves `drawIn` `blurIn` · Tin `luma`, `gl:perlin` · Post `clean` + grain · BG none (paper texture).

**9 · Ottoman Archive.** Firmans, tughras, ebru marbling borders, wax seals, carmine & indigo.
Pal `ottomanManuscript` · Type Mirza / Markazi / RuqaaInk · Persona documentary · Moves `stampIn` `unfoldIn` `dropIn` · Tin `gl:Swirl` (ebru), `tear` · Post `sepia` · BG none.

**10 · Desert Dune.** Wind-sculpted gradients, long shadows, sand particles, caravan lines drawing across maps.
Pal `desertDune` · Type Alexandria / Almarai · Persona documentary · Moves `slideInRight` `drift` `drawIn` · Tin `gl:wind`, `push` · Post `tealOrange` · BG `waves` low contrast / `topo`.

**11 · Hijaz Coral-Stone.** Coral-stone houses, rawasheen wooden windows, sea light; calm editorial.
Pal `hijazCoral` · Type ElMessiri / Readex · Persona premium · Moves `fadeInUp` `riseIn` `hover` · Tin `slide`, `gl:Dreamy` · Post `clean` · BG `mashrabiya`.

## B · Explainers & journalism
**12 · Clean VOX Explainer** (preset C). Off-white paper, flat maps/charts, duotone cut-out archives, highlighter.
Pal `voxExplainer` · Type Cairo 900 / Readex 500 · Persona corporate · Moves `popIn` `drawIn` `fadeInRight` `punch` · Tin `band`, `whip`, `zoom` · Post `clean` · BG `dots` 4%.

**13 · Newsroom Data.** Dark UI, live tickers, counters, bar races, red alert accent.
Pal `newsroom` · Type Alexandria / PlexArabic / JetBrains · Persona energetic · Moves `zoomInUp` `staggerMove('fadeInUp')` `heartBeat` (final value) · Tin `blinds`, `glitch` (rare), `whipUp` · Post `clean` · BG `grid`.

**14 · Map Explainer.** One map that the camera travels; routes draw on; pins bounce; borders morph.
Pal `forestData` or `voxExplainer` · Type Cairo / Tajawal · Persona documentary · Moves `bounceInDown` (pins) `drawIn` (routes) `pulse` · Tin camera moves instead of cuts (`camKeys`) · Post `clean` · BG `topo`.

**15 · Blueprint / Tech** (preset E). Cyanotype grid, hairlines constructing themselves, dimension arrows. Ref: [anidoodle blueprint](../resources/skills/anidoodle-styles/styles/blueprint.md).
Pal `kufiBlueprint` · Type Handjet or Alexandria / Mono · Persona corporate · Moves `drawIn` `unfoldIn` `spinOnce` · Tin `blinds`, `gl:GridFlip` · Post `clean` · BG `grid` + `iso`.

**16 · Swiss Poster.** Grid, giant numerals, one red, asymmetric type blocks sliding on rails.
Pal `swissPoster` · Type Cairo 1000 / Inter · Persona energetic · Moves `slideInRight` `wipeOut` `punch` · Tin `cut`, `push` · Post `clean` · BG `lines`.

**17 · Isometric City.** 2:1 isometric cutaways, buildings extruding, people as dots. Ref: [anidoodle isometric](../resources/skills/anidoodle-styles/styles/isometric.md).
Pal `pastelEdu` or `palette(…)` · Type Alexandria / Almarai · Persona playful · Moves `bounceIn` `staggerMove('dropIn',{order:'center'})` · Tin `gl:cube`, `push` · Post `clean` · BG `iso`.

**18 · Kinetic Type Only.** No images: words are the visuals (elastic, weight-pumping, masks).
Pal any 2-colour + accent · Type Readex/Cairo variable / Ruqaa emphasis · Persona energetic · Moves `stampIn` `rubberBand` `jello` `riseIn` · Tin `smear`, `cut` · Post `clean` · BG none.

## C · Modern & cinematic
**19 · Liquid Glass.** Frosted translucent panels over blurred colour fields, specular rims, soft parallax (2026 trend).
Pal `damascusNight` + accent · Type Alexandria / Readex · Persona premium · Moves `blurIn` `hover` `springIn` · Tin `gl:CrossZoom`, `zoom` · Post `dream` · BG blurred blobs (`blob()`).

**20 · Neon Noir.** Black, magenta/cyan rim light, rain textures, bloom only on highlights.
Pal `neonNoir` · Type Blaka or Changa / Mada · Persona energetic · Moves `glitchIn` `whipIn` `flash` · Tin `gl:GlitchMemories`, `glitch` · Post `noir` + `fxBloom` · BG `lines` scanlines.

**21 · Retro-Futurism.** 70s–80s sci-fi: chrome type, sunset grids, VHS artefacts.
Pal nice palettes `palettesBy({dark:true, hue:[300,40]})` · Type Rakkas / Handjet · Persona playful · Moves `zoomInUp` `spin` `flipInX` · Tin `gl:DoomScreenTransition`, `gl:TVStatic` · Post `vhs` · BG `grid` in perspective.

**22 · New Minimalism.** One object, huge negative space, slow precise moves, hairline type.
Pal `swissPoster` desaturated · Type Alexandria 200 / Readex 300 · Persona premium · Moves `blurIn` `riseIn` `breathe` · Tin `dip`, `cut` · Post `clean` · BG none.

**23 · Dark Archive Documentary** (preset D). Near-black, grainy archives with burn edges, red string, typewriter labels.
Pal `archiveSepia` with red · Type Mada / JetBrains · Persona documentary · Moves `dropIn` `typeIn` `stampIn` · Tin `gl:FilmBurn`, `dip`, `flash` · Post `film` · BG none.

**24 · Redacted Dossier.** Paper files, black bars sliding over words, stamps, polaroids pinned.
Pal `#e9e4d8/#141414/#b3261e` · Type Markazi / Mono · Persona documentary · Moves `wipeOut` (redaction bars) `stampIn` `swingIn` (pinned photo) · Tin `slide`, `tear` · Post `film` · BG `lines` (ruled paper).

**25 · Film Noir Portrait.** Hard key light, venetian-blind shadows, B&W portraits, slow dolly.
Pal greys + one gold · Type Amiri / Mada · Persona premium · Moves `blurIn` `fadeInUp` · Tin `gl:windowblinds`, `dip` · Post `noir` · BG `lines` (blinds shadow).

**26 · Editorial Essay.** Magazine layouts, serif headlines, pull quotes, photo crops shifting.
Pal `hijazCoral` · Type Markazi / Mada / Amiri · Persona documentary · Moves `riseIn` `fadeInRight` `unfoldIn` · Tin `push`, `slide` · Post `clean` · BG none.

## D · Hand-made, collage, social
**27 · Sticker-Pop Dialect Ad** (preset F). Cream world, pixel character, polaroid stickers, bubbles with hard shadows.
Pal `#f8f4e9/#1c1917/#05a1a2/#f8bb3e` · Type Kufi 800 / Ruqaa · Persona stickerpop · Moves `popIn` `dropIn` `bob` `punch` · Tin `whip`, `zoom`, `flash` · Post `pop` · BG none.

**28 · Riso Print.** Two-ink overprint, misregistration, halftone. Ref: [anidoodle halftone](../resources/skills/anidoodle-styles/styles/halftone.md), shotcraft `riso-print-hits`.
Pal `riso` · Type Lalezar / Tajawal · Persona playful · Moves `stampIn` `jitter` `popIn` · Tin `gl:luma`, `band` · Post `pop` + `rgbSplit` 3 px · BG `halftone`.

**29 · Maximalist Collage.** Layers of cut photos, torn paper, tape, scribbles, everything moving on twos (2026 trend). Ref: [collage-broll skill](../resources/skills/collage-broll/SKILL.md).
Pal nice palette vivid `palettesBy({minChroma:.15})` · Type Lalezar / Marhey · Persona playful · Moves `dropIn` `jitter` `swingIn` `tada` · Tin `tear`, `gl:Mosaic` · Post `pop` · BG `halftone` + paper.

**30 · Pastel Edu.** Rounded shapes, soft shadows, friendly characters, icons drawing on.
Pal `pastelEdu` · Type Lemonada / Almarai · Persona playful · Moves `springIn` `bounce` `wobble` · Tin `iris`, `gl:circleopen` · Post `clean` · BG `dots`.

**31 · Paper-Craft.** Layered cut paper with real depth shadows, on twos. Ref: [anidoodle paperCraft](../resources/skills/anidoodle-styles/styles/paperCraft.md).
Pal nice palette warm · Type Baloo / Tajawal · Persona playful · Moves `dropIn` `sway` `jitter` · Tin `tear`, `push` · Post `clean` + grain · BG paper layers.

**32 · Chalkboard Lesson.** Dark green slate, chalk drawing on, dust. Ref: anidoodle `Chalkboard` (in [styles.md](../resources/skills/anidoodle-styles/styles.md)).
Pal `#1f3a2e/#f1f1e6/#f2c14e` · Type ReemKufiFun / Tajawal · Persona documentary · Moves `drawIn` `typeIn` · Tin `wipeOut` (eraser), `luma` · Post grain · BG none.

**33 · Vintage Scrapbook.** Engravings, cut-letter titles, taped cards on aged paper. Ref: [anidoodle scrapbook](../resources/skills/anidoodle-styles/styles/scrapbook.md).
Pal `archiveSepia` light · Type Katibeh / Markazi · Persona playful · Moves `swingIn` `dropIn` `hover` · Tin `tear`, `gl:BookFlip` · Post `sepia` · BG paper.

**34 · Woodcut / Linocut.** Carved black keylines, flat colour blocks. Ref: [anidoodle woodcut](../resources/skills/anidoodle-styles/styles/woodcut.md).
Pal `#efe6d2/#151515/#b23a2a` · Type Blaka / Mada · Persona documentary · Moves `stampIn` `wipeOut` · Tin `luma`, `cut` · Post grain · BG `lines` (gouge).

**35 · Pixel Art.** 16-colour palette on a low-res grid, crisp scaling. Ref: [anidoodle pixelArt](../resources/skills/anidoodle-styles/styles/pixelArt.md), `sprite()`.
Pal 16-colour from `palette(i)` pair · Type Handjet / Tajawal · Persona stickerpop · Moves `bob` `jitter` (fps 8) `popIn` · Tin `gl:pixelize`, `cut` · Post `vhs` light · BG `grid`.

**36 · Stipple / Engraving.** Dot-density tone like banknotes and old encyclopaedias. Ref: [anidoodle stipple](../resources/skills/anidoodle-styles/styles/stipple.md).
Pal `#f3ecdc/#1d1a16` · Type Scheherazade / Markazi · Persona premium · Moves `drawIn` `blurIn` · Tin `luma` · Post `sepia` · BG `halftone` mono.

**37 · Flat Vector Long-Shadow.** Crisp geometric shapes, grain, long shadows. Ref: [anidoodle flatVector](../resources/skills/anidoodle-styles/styles/flatVector.md).
Pal nice palette 5-colour · Type Cairo / Almarai · Persona corporate · Moves `popIn` `slideInRight` `spinOnce` · Tin `band`, `iris` · Post `clean` + grain · BG none.

**38 · Mid-Century Gouache.** Opaque matte shapes, dry-brush edges, 50s editorial charm. Ref: [anidoodle midCentury](../resources/skills/anidoodle-styles/styles/midCentury.md).
Pal `saffronIndigo` light or nice warm · Type Rakkas / Mada · Persona playful · Moves `swingIn` `float` `squash` · Tin `push`, `gl:Rolls` · Post `film` · BG none.

**39 · Low-Poly 3D.** Flat-shaded triangles, camera orbits. Ref: [anidoodle lowPoly](../resources/skills/anidoodle-styles/styles/lowPoly.md).
Pal `forestData` · Type Alexandria / PlexArabic · Persona corporate · Moves `zoomInUp` `orbit` · Tin `gl:cube`, `gl:doorway` · Post `clean` · BG `iso`.

**40 · Embroidery / Textile (Tatreez).** Cross-stitch motifs, thread drawing on, linen texture — Palestinian/Levantine tatreez. Ref: [anidoodle embroidery](../resources/skills/anidoodle-styles/styles/embroidery.md).
Pal `#efe7d6/#8f1d21/#1f2a2e/#2d5d7b` · Type Kufam / Tajawal · Persona documentary · Moves `drawIn` (stitches) `staggerMove('popIn',{order:'center'})` · Tin `gl:squareswire`, `gl:randomsquares` · Post grain · BG `grid` small (stitch grid).

---
## Illustration "hands" (vendored, Apache-2.0)
`resources/skills/anidoodle-styles/` contains 22 detailed style sheets (how the medium behaves physically, the mark, the edge, tone, order of drawing), the 32-style index ([styles.md](../resources/skills/anidoodle-styles/styles.md)), a motion grammar ([motion-grammar.md](../resources/skills/anidoodle-styles/motion-grammar.md)), camera and craft-bar docs.
Use them to **write image-generation prompts** and to **design draw-on order** (what gets drawn first in that medium) for the matching style above.
