# Open-source motion ecosystem (researched Oct 2026) — what we took from each

**v1.2: the open-licence ones are now vendored in [`resources/`](../resources/README.md)** (offline, with licences) and the data packs in `engine/kit/`. This page stays as the map of the wider ecosystem.
This skill is self-contained: nothing below is required. These are the best open resources of 2026, what
each is good for, and which of their ideas are already distilled into this repo (with the file).

## Agent skills for motion / video
| resource | licence | what it is | distilled into |
|---|---|---|---|
| [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | MIT | 3 pillars, motion personalities, duration/easing tables, choreography, emotion & material maps, quality rules | library/easing_timing.md, rules/motion_rules.md §9 |
| [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills) | MIT | animation-principles, color-motion (OKLCH, grading order, colour management), shot-composition, motion-art-direction (motion-language spec), beat-sync, logo-animation, motion-background | library/color_systems.md, camera_language.md, easing_timing.md §0 |
| [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | MIT | ~50 skills: kinetic type, data-viz, explainers, WebGL, Manim | library/kinetic_typography.md |
| [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | Apache-2.0 | 150+ shot recipe cards (camera, transitions, typography, rhythm), 2.5D page camera, beat sync, SFX | library/transitions.md (rhythm recipes), camera_language.md §3 |
| [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | custom (commercial use: ask) | narration videos: word-level VO sync, anti-slideshow camera system (continuous curves, parallax planes, idle/yield, breathing environment), schematic line-art layer for text-only shots | camera_language.md §8, rules/motion_rules.md |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | see repo | official Remotion agent skills (`npx skills add remotion-dev/skills`) | — (alt. engine) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | HTML/CSS/GSAP → deterministic MP4, router skill loading sub-skills on demand | architecture parallels our `render(t)` design |
| [VideoZero/skills](https://github.com/VideoZero/skills) | Apache-2.0 | motion-canvas + motion-graphics fundamentals | — |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | review-animations: never scale from 0, asymmetric enter/exit, blur crossfades | rules/motion_rules.md §9 |
| [naranyala/awesome-motion-graphics](https://github.com/naranyala/awesome-motion-graphics) | list | 12 principles table, glossary (on-twos, overshoot, beat mapping, speed graph) | easing_timing.md |
| [hhenrichsen/motion-canvas-commons](https://github.com/hhenrichsen/motion-canvas-commons) | MIT | reusable Motion Canvas components | — |
| createmotion.io/resources | list | index of motion agent skills & repos | this file |

## Code-driven video frameworks (alternatives to our canvas engine)
| framework | licence | language | when to prefer |
|---|---|---|---|
| Remotion | source-available (free ≤3 employees) | React/TSX | big teams already on React, Lambda rendering |
| Motion Canvas | MIT | TS generators | audio-synced editor, vector animations |
| Revideo | MIT | TS (Motion Canvas fork) | programmatic rendering at scale |
| HyperFrames | Apache-2.0 | HTML + GSAP | web-native teams, GSAP timelines |
| Manim (CE) | MIT | Python | math/science explainers |
| Theatre.js | Apache-2.0 / AGPL studio | JS | keyframe editor on top of code |
| Lottie / dotLottie, Rive | MIT / proprietary editor | JSON / runtime | UI motion, loops, interactive |
Our engine stays dependency-free canvas so it renders anywhere with 2 GB RAM; port techniques, not stacks.

## Libraries whose maths we re-implemented (no dependency needed)
Penner easing equations (BSD) → `E.*` · CSS cubic-bezier solver → `bezier()` · react-spring presets →
`SPRINGS` · simplex noise (Gustavson, public domain) → `noise2/fbm/wiggle` · OKLab (Ottosson, public) →
`oklch/mixOK` · WCAG contrast → `contrast()` · GSAP-style stagger/timeline ideas → `drawWords`, `kf`.
Optional if you want them: GSAP (free incl. SplitText/MorphSVG since 2025), culori / chroma.js (colour),
flubber (shape morph), d3-ease, simplex-noise, lottie-web, three.js (WebGL scenes).

## Assets
**Embedded (v1.2):** 41 OFL fonts (`engine/kit/fonts`), 1877 Lucide icons, 1000 palettes + Open Color (`engine/kit/data`), 125 GL transitions. More on demand: Fonts: Google Fonts repo (OFL) → `tools/fonts.sh`, list in library/fonts.md · Icons: Lucide (ISC),
Tabler (MIT), Iconify sets · Images: Wikimedia Commons, museum open-access (Met, Rijksmuseum, Smithsonian,
NYPL) → library/asset_sourcing.md · SFX: SOUND LAYER kit (`vendor/opus-sound-layer`, 1,139 CC0 recordings) + `sfx.py search` (Openverse CC0);
never synthesized hits/whooshes · Music: user track or CC0 loop (Openverse/Freesound CC0), Mixkit · Textures: own scans, Poly Haven (CC0).

## Learning
VOX "how we make" breakdowns · School of Motion 12 principles · Material 3 motion docs · Apple HIG motion ·
"The Animator's Survival Kit" (spacing, timing) · Blender/AE camera tutorials for parallax planes.
