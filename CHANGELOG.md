# Changelog

## v3.0 — 2026-10-13 «الخط الواحد»
- NEW engine module `engine/line.js`: one-line films (LINE path + LCAM Hermite camera + BLOOM fills + world-anchored Kinetic-type words; Lucide icons drawn by the pen; LTR digit words + LTR pen reveals).
- NEW `library/one_line_engine.md`: the five-act grammar (touch → identity → services → care&reveal → contact/outro) + the non-negotiable mechanics, each tied to a real production failure.
- `rules/pitfalls.md` v3 additions (NaN tf/sample trap, world text spacing, hero frame gate, swoop+sub6, kit rebuild drift, orientation squish…).
- `rules/qa_checklist.md`: orientation gate, hero-appear gate, one-line gates.
- `tools/encode_release.sh`: orientation-aware (portrait reels were being squished to 1920×1080 and still passing QA).
- NEW reference `examples/one_line_reel/`: Lamset Shifa v3 (64.8s one-take reel) — brief, canon scene sources, QA artefacts; `examples/lamset_reel/`: the v2 «رحلة الورقة» reel reference.


## v2.1.0: Creative Director intake, pro kinetic typography, 5× faster renders (2026-10-13)
- **Creative Director / prompt engineer** (`skills/motion-director/`, sub-agent `agents/creative-director.md`,
  `workflow/00_intake.md` rewritten, `templates/brief.md`). It turns a messy idea into a pro brief: understand → ONE question
  round with options and defaults (duration, aspect, VO provided/generated, images provided/generated, music, style) →
  research → 3 concepts → `docs/production_prompt.md` → one confirmation → hand-off. **`START.md`**: one link that installs
  and starts a project. INSTALL step 4 now starts the intake right after installing. The installer links 3 skills.
- **Kinetic typography system:** `engine/type.js` (`KT`) with word objects, Arabic **kashida** tracking (legal joints,
  never inside لا), 20 entrances, 12 exits, holds (drift, wiggle, breathe, dim, echo, chroma), `group()` parenting/3D flip,
  14 motion-pair partners (dot, leader, comet, ring, underline, bar, line, hinge, bubble, panel, orbit, streak, bokeh),
  spatial `spots()`, `timeline()` and `post()`. `library/kinetic_type_motion.md` merges the user's report (roles, motion pairs, recipes
  A–D, timing table, easing, AE/CapCut mapping) with frame analysis of 3 reference lyric videos
  (`examples/reference_dna/kinetic_lyrics/DNA.md`) and creative-adaptation rules. `engine/kinetic.html` page (any aspect), with
  `scenes/kt_demo.js` as the 10 s template. Demo: `examples/kinetic_demo/` (1080×1920).
- **Render speed** (`workflow/11_render_speed.md`): Chromium no longer forces 2D canvas through SwiftShader (329 → 60 ms
  per frame, PSNR 45 dB vs old). `render.mjs` v2 reads the canvas directly and adds `--draft` (1 sub-frame, 960 px,
  veryfast), `--workers N|auto` (parallel segments, lossless concat, RAM-aware), `--gl`, `--capture`, `--width`, ETA, auto
  canvas size, tv-range yuv420p output. Measured on 2 vCPU/2 GB: **4.8× faster finals, 11× faster drafts**. `still.mjs`
  reads the canvas at native size (9:16/1:1 safe).
- `tools/new_film.sh --kinetic --aspect 9:16|1:1|4:5|16:9`. `selftest` now covers every KT entrance, exit and partner, plus the kashida rules.
- Docs: SKILL.md (non-negotiables 14–15, pipeline rows T and ⚡), AGENTS/CLAUDE/GEMINI/Cursor/Copilot entry points, pitfalls, gl_transitions.

## v2.0.0: Sound Layer + installable plugin/skills for every agent (2026-10-13)
**Breaking:** the canonical skill moved from `SKILL.md` to `skills/motion-doc-studio/SKILL.md`. Old manual copies
of the repo folder into `~/.claude/skills/` should be replaced by the installer (`install.sh`), which backs them up.
- **SOUND LAYER** (`skills/motion-sound-layer/`): the user's SOUND LAYER prompt is kept **verbatim** in `PROMPT.md`, with notes
  against the pinned scripts (kit size now 1,139 sounds / 19 types, hero recipe, browse/add, `appear` is checked by qa.py).
  `workflow/10_sound_layer.md` gives the full procedure and FAIL → fix table. `rules/audio_rules.md` was rewritten. The QA checklist
  and workflow 07 now use qa.py gates. New templates: `LISTEN.md` and `sound.json`.
- **vendor/opus-sound-layer** (MIT, Bodila51) @ `52ac266`, byte-identical, with `opus-sound-layer.sha256` and a pin/update
  procedure in `vendor/README.md`.
- **engine/cues.js** (new): `when.spring/ease/path` measure `{start, peak, land}` frames the way qa.py measures video, and
  `cue.land/move/cut/appear/hero/raw` fill `window.CUES`. `engine/index.html` loads it. `scenes/demo.js` registers 13 cues.
  The demo's end word now uses the `card` spring, because a `soft` settle is too gradual for a measurable hero landing.
- **tools:** `export_cues.mjs` (page → `audio/cues.json`, validation, hero spacing), `sound_layer.sh`
  (setup = upstream clone @ pin with an offline vendored fallback, verify, kit, deps), `encode_release.sh` (1080p/720p plus qa.py on
  each file). `setup.sh` installs uv and works from any cwd. `new_film.sh` scaffolds `vendor/`, `audio/sound.json` and `docs/LISTEN.md`.
  `selftest.mjs` checks the cue registry. `sfx.mjs` / `cues_auto.py` / `mix_final.sh` are marked legacy.
- **examples/demo/sound/:** real run, measured: 13 cues, 42 pass / 3 warn / 0 FAIL, −14.01 LUFS, both release encodes 0 FAIL,
  QA rounds documented, qa.png described at each hero, plus CREDITS.md and LISTEN.md. `demo_16s.mp4` now has sound.
- **Packaging:** Claude Code plugin + marketplace (`.claude-plugin/`, validated with `claude plugin validate`), Codex plugin
  (`.codex-plugin/`, `.agents/plugins/marketplace.json`), Gemini CLI extension (`gemini-extension.json` + `GEMINI.md`),
  Agent Skills layout for `npx skills add zoih6/motion-doc-studio-orchestrated` (2 skills discovered). `install.sh` is a universal installer
  (clone/update, deps, symlinks into every detected agent, verify, uninstall). `INSTALL.md` is an agent-readable procedure:
  its raw URL is the one-message install link. `skills/*/scripts/studio.sh` lets skills find or clone the studio from anywhere.
- **Docs:** new bilingual README (install message, per-agent table, layout tree). AGENTS.md, CLAUDE.md, GEMINI.md, Cursor and
  Copilot pointers were updated, as were the kickoff prompt, glossary (sound terms), transitions SFX table (kit types) and resources.
- CI: `.github/workflows/validate.yml` checks the manifests, skill frontmatter, vendored checksums, JS syntax and the engine selftest.

## v1.2.0: embedded dictionaries & resource packs (2026-10-12)
Everything is vendored into the repo (offline, licences preserved). Nothing is link-only any more.
- **Fonts:** 31 new OFL families, **41 in total** (Cairo, Tajawal, Almarai, IBM Plex Sans Arabic, Alexandria, Noto Naskh,
  Scheherazade New, Lateef, Markazi, Mirza, Aref Ruqaa Ink (colour), Noto Nastaliq, Gulzar, Qahiri, Reem Kufi / Fun / Ink,
  Kufam, Blaka, Lemonada, Baloo Bhaijaan 2, Jomhuria, Katibeh, Vibes, Harmattan, Mada, Handjet, Inter, Space Grotesk,
  Fraunces, JetBrains Mono). Generated `fonts.css`, `fonts.js` registry (`FONT_REGISTRY`, `fontsBy`, `fontLoads`) and licence
  table (`tools/build_fonts.py`); `library/fonts.md` rewritten (roles, 17 pairings, Arabic motion-type rules).
- **engine/gl.js + kit/data/gl_transitions.js:** 125 gl-transitions shaders (MIT/BSD, authors kept) registered as
  `TRANS['gl:<Name>']` with `shot.glParams`; procedural luma/displacement maps; `library/gl_transitions.md`.
- **engine/moves.js:** `MOVES` dictionary of 84 named moves (34 entrances, 18 exits, 21 emphasis, 11 loops), plus
  `move()`, `seqMove()`, `staggerMove()` (rtl/ltr/center/random). Original implementations. `library/motion_recipes.md`.
- **engine/assets.js:** palettes (`palette`, `paletteRoles`, `applyPalette`, `palettesBy`, `oc`, 20 original `HERITAGE`
  palettes), icons (`icon` with exact draw-on, `iconSearch`), 13 procedural patterns (`star8`, `rosette`, `star6`, `star12`,
  `girihNet`, `mashrabiya`, `dots`, `halftone`, `grid`, `lines`, `waves`, `iso`, `topo`).
- **kit/data:** `palettes.js` (1000 nice-color-palettes + Open Color, MIT), `icons_lucide.js` (1877 Lucide icons, ISC,
  per-element path + measured length).
- **library/ dictionaries (new):** `glossary.md` (bilingual, ≈170 terms → code), `style_catalog.md` (40 styles → engine
  values), `effects_dictionary.md`, `shot_cards_index.md` (124 cards, English), `icons.md`, `patterns.md`, `gl_transitions.md`,
  `motion_recipes.md`; `library/specimens/*.jpg` visual sheets.
- **resources/ (new):** vendored skills with their licences: LottieFiles motion-design, iart motion-design-skills (9),
  Emil Kowalski (animation-vocabulary, review, improve, animate, performance), GSAP skills (8), video-shotcraft shot cards
  (124 + sequences + aesthetic/beat/sound/review docs), anidoodle (22 style sheets, motion grammar, camera, craft bar), orca
  motion, collage-broll, html-animation. Plus `resources/README.md`, `resources/NOTICE.md`, `resources/licenses/`.
- **tools:** `build_data.mjs`, `build_fonts.py`, `build_docs.mjs`, `specimens.mjs`, `selftest.mjs`; render/still launch Chromium
  with SwiftShader WebGL. `engine/index.html` loads all packs; `engine/specimens.html` is a visual browser.

## v1.1.0 — pro layer (2026-10-12)
- **engine/fx.js** (new): Penner + cubic-bezier easings, named industry curves, keyframes `kf()`, spring
  library, motion personalities; seeded simplex noise, wiggle, handheld; OKLab/OKLCH colour mixing and WCAG
  contrast; 2.5D camera rig (`cam`, `layer`: dolly, truck, pedestal, roll, orbit, vertigo, rack focus,
  impact shake); image ops (tint, sticker outline, extrude, echo, RGB split, pixelate, polaroid); post FX
  (grain, vignette, bloom, halation, chromatic aberration, light leak, lift/gamma/gain + split-tone) and 8
  LOOKS; Arabic-safe kinetic typography (word layout with accent markup, 8 entrance modes, VO-synced
  karaoke, mask reveal, marker, blur swap, variable-weight morph); graphics (panels, hand-drawn circle,
  SVG path draw-on, burst, sparkles, bubbles, pill CTA, cursor + ripple, pixel sprites, phone mock,
  stickers, seeded scatter); 16 transitions in `TRANS`.
- **core.js**: pluggable transitions (`shot.tin` = any TRANS key, `shot.tdur`, `FILM.tin`) and finishing
  chain (`FILM.post`); default behaviour unchanged (tear + sepia grade).
- **library/**: easing_timing, camera_language, transitions, kinetic_typography, color_systems,
  compositing_fx, fonts, resources (2026 open-source ecosystem); style preset **F · Sticker-Pop Dialect Ad**.
- **rules/**: motion-language spec (direction first), 2026 craft rules, advanced colour/type/finishing rules.
- **workflow/09_reference_dna.md** + **tools/video_dna.py**: measure a reference video's DNA (cuts,
  transition frame counts, flashes, palette + OKLCH, loudness, onsets, sheets) without copying it.
- **examples/reference_dna/**: full DNA breakdown of a 20 s Arabic app ad.
- **fonts**: + Readex Pro, Changa, El Messiri, Lalezar, Aref Ruqaa, Marhey, Rakkas, IBM Plex Mono (OFL);
  `tools/fonts.sh` downloads more by name.
- **tools/mix_final.sh**: outputs tagged BT.709.

## v1.0.0 — first release
Rules, workflow 00–08, library, canvas engine, tools, Thuluth example film.
