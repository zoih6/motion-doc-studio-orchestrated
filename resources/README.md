# resources/ — vendored open-licence motion knowledge (offline, included in the repo)

Everything here is **third-party content redistributed under its original licence** (each folder keeps its `LICENSE`).
It's embedded so agents can work fully offline, read the original expert material, and so the repo's own dictionaries can link to exact sources.
Our own distilled and engine-mapped material lives in [`library/`](../library/). The runtime data packs (fonts, palettes, icons, GL transitions) live in [`engine/kit/`](../engine/kit/).

## 1 · Vendored skills & reference docs (`resources/skills/`)
| folder | upstream | licence | what's inside | read it when… | our mapping |
|---|---|---|---|---|---|
| [`lottiefiles-motion-design/`](skills/lottiefiles-motion-design/SKILL.md) | LottieFiles/motion-design-skill | MIT | director workflow, motion personalities, duration/easing tables, choreography, patterns, reference | deciding the film's motion language | [easing_timing.md](../library/easing_timing.md) |
| [`iart-motion-design/`](skills/iart-motion-design/) | iart-ai/motion-design-skills | MIT | 9 skills: animation-principles (12 principles, easing graph), color-motion, shot-composition, motion-art-direction, beat-sync-editing, logo-animation, motion-background, after-effects (expressions + scripts), remotion-video; plus verify scripts | principles, colour, composition, AE expressions | [color_systems.md](../library/color_systems.md), [camera_language.md](../library/camera_language.md) |
| [`emilkowalski/`](skills/emilkowalski/) | emilkowalski/skills | MIT | **animation-vocabulary** (reverse-lookup glossary), review-animations (standards), improve-animations (audit + plan), animate (recipes), animation-performance, find-animation-opportunities | naming an effect; reviewing motion quality | [glossary.md](../library/glossary.md), [rules/motion_rules.md](../rules/motion_rules.md) |
| [`gsap/`](skills/gsap/) | greensock/gsap-skills | MIT | 8 GSAP skills: core, timeline, plugins (SplitText, MorphSVG, DrawSVG…), utils, scrolltrigger, performance, frameworks, react | porting to HyperFrames/HTML+GSAP, timeline thinking | [resources.md](../library/resources.md) |
| [`shotcraft-shot-cards/`](skills/shotcraft-shot-cards/) | Vincentwei1021/video-shotcraft | Apache-2.0 | **124 shot cards** (camera, data, effects, interaction, opening, outro, rhythm, transition, typography, ui-entrance) with frame timings + sequences + aesthetic rules, beat sync, sound design, final review | designing a specific shot | **English index: [shot_cards_index.md](../library/shot_cards_index.md)** · [effects_dictionary.md](../library/effects_dictionary.md) |
| [`anidoodle-styles/`](skills/anidoodle-styles/) | alexgreensh/anidoodle | Apache-2.0 | 22 illustration-medium style sheets (sumi-e, woodcut, riso/halftone, paper-craft, pixel art, stipple, embroidery…), 32-style index, motion grammar, camera, craft bar, storytelling, motion-deck.json | writing image prompts and draw-on order for a hand-made style | [style_catalog.md](../library/style_catalog.md) |
| [`orca-motion/`](skills/orca-motion/) | zhenwusw/orca-motion-skill | MIT | motion principles, kinetic type, API, integration notes | kinetic-type ideas | [kinetic_typography.md](../library/kinetic_typography.md) |
| [`collage-broll/`](skills/collage-broll/SKILL.md) | pyang5166/gbro-collage-broll | MIT | halftone paper-collage b-roll method | collage / maximalist styles | style_catalog #29 |
| [`html-animation/`](skills/html-animation/SKILL.md) | acelera-agency/html-animation | MIT | HTML/CSS/JS animation production skill | web-native motion | — |

Notes: binaries (gif/mp4/showcase pages) were left out to keep the repo small. `shotcraft-shot-cards/shots/ATTRIBUTION.md` explains that those cards are re-implementations of public techniques. Keep that spirit: **re-implement the technique, never copy brand content**.

## 2 · Data packs (runtime, in `engine/kit/`)
| pack | file | upstream | licence | count | API / docs |
|---|---|---|---|---|---|
| Fonts | `engine/kit/fonts/*.ttf` + `fonts.css` + `fonts.js` | google/fonts (ofl/*) | SIL OFL 1.1 | 41 families / 48 files | [fonts.md](../library/fonts.md), [kit/fonts/README.md](../engine/kit/fonts/README.md) |
| GL transitions | `engine/kit/data/gl_transitions.js` | gl-transitions/gl-transitions | MIT (+2 BSD) per file | 125 | `tin:'gl:<Name>'` · [gl_transitions.md](../library/gl_transitions.md) |
| Palettes | `engine/kit/data/palettes.js` | Jam3/nice-color-palettes · yeun/open-color | MIT · MIT | 1000 × 5 + 15 hues × 10 | `palette(i)`, `paletteRoles()`, `oc()` · [color_systems.md](../library/color_systems.md) |
| Icons | `engine/kit/data/icons_lucide.js` | lucide-icons/lucide | ISC | 1877 | `icon()`, `iconSearch()` · [icons.md](../library/icons.md) |
| Licence texts | [`licenses/`](licenses/) | — | — | — | — |

Rebuild packs from upstream: `RES=<checkouts> node tools/build_data.mjs` · `python3 tools/build_fonts.py` · docs: `node tools/build_docs.mjs` · sheets: `node tools/specimens.mjs`.

## 3 · Deliberately NOT vendored (licence)
- animate.css: Hippocratic licence. We use only its common move **names** as vocabulary; every move in `engine/moves.js` is our own implementation.
- RuiC-motion-reel, live-panel-skill, motion-ui-design: no licence or unclear, so they are only linked in [resources.md](../library/resources.md).
- video-talkcraft: custom licence (commercial use needs permission), so it's linked only.
- Remotion: source-available, so it's linked only.
