---
name: motion-doc-studio
description: >-
  Build documentary / explainer MOTION-GRAPHICS films (VOX-style, cinematic, RTL/Arabic-ready) from a
  voice-over, end to end: brief → VO timing → treatment → style bible → real + AI assets → code-driven
  animation engine → critique loops → chunked render → SOUND LAYER (real CC0 SFX + music placed from the
  picture's own springs, measured by QA) → GitHub delivery. Use whenever a user asks for a motion-graphics
  video, animated documentary, explainer, "VOX style" piece, reel, or wants an existing video remade or
  restyled. Works with any coding agent that can run bash, node, python, ffmpeg.
license: MIT
metadata:
  version: 3.0.0
  repository: https://github.com/zoih6/motion-doc-studio-orchestrated
---

# Motion-Doc Studio — canonical skill (v3.0)

You are a **director + motion designer + engineer** in one. The film is a *program*: every frame is
`render(t)`, a pure function of time, drawn on a 1920×1080 canvas, captured by Playwright, encoded by
FFmpeg. This gives frame-exact sync with the voice-over, deterministic re-renders, and crash-safe
chunked rendering on small machines.

This file is the source of truth. Detailed rules live in `rules/`, step-by-step procedures in
`workflow/`, reusable recipes and dictionaries in `library/`, runnable code in `engine/` + `tools/`, vendored
open-licence expert material in `resources/` (offline), and a complete
real production in `examples/thuluth/` (3:56 Arabic documentary — watch it before your first film).

**Where the files are.** Every path in this file (`rules/`, `workflow/`, `library/`, `engine/`, `tools/`,
`vendor/`, `templates/`, `examples/`) is relative to the **studio root**. Find it once per session:
```bash
STUDIO=$(bash <folder of this SKILL.md>/scripts/studio.sh)   # plugin / clone / ~/.motion-doc-studio; clones it if missing
"$STUDIO/tools/setup.sh"                                      # ffmpeg, node deps, chromium, uv (idempotent)
```
**New project?** The companion skill **`motion-director`** (`skills/motion-director/`) runs first: the Creative
Director turns the user's messy idea into `docs/brief.md` + `docs/production_prompt.md` (one question round with
options, research, 3 concepts, one confirmation). Never make the user write a prompt.
**Text motion** (lyrics, quotes, captions, text-only films): `library/kinetic_type_motion.md` + `engine/type.js`.
**«الخط الواحد» one-line films** (one continuous line draws the whole film in one take — brand reels, premium pure-MG):
`engine/line.js` + `library/one_line_engine.md` (mandatory rules; reference: `examples/one_line_reel/`).
Sound for any film: the companion skill **`motion-sound-layer`** (`skills/motion-sound-layer/`) runs
the SOUND LAYER prompt verbatim on top of this engine.

---

## 0 · Non-negotiables (read these even if you read nothing else)

1. **The VO is the master clock.** Transcribe word timings first. Every shot starts on a spoken word;
   every on-screen word appears when it is said (±0.15 s). Never animate to a guessed tempo.
2. **Real motion graphics, never a slideshow.** No "image + Ken Burns + crossfade". Things *enter,
   build, transform, measure, collide, get written*. Every shot has an action verb.
3. **Something new every 2–4 s; a hook in the first 2 s.** One idea per VO sentence.
4. **Never crowded.** Per shot: 1 hero + 1 text card + ≤2 supporting elements. 96 px safe margins.
   Text card lives in the empty third opposite the subject. If in doubt, remove.
5. **Content must be legible.** Minimum caption 34 px @1080p (type scale TS=1.3); contrast ≥ 4.5:1
   (gold on parchment → use deep gold `#86520f`; never black on dark).
6. **Real, content-true, high-res assets first;** AI-generated only for gaps (portraits of historical
   people, atmospheric plates, objects). Never random/irrelevant stock. All text is typeset by us —
   never baked into generated images.
7. **Springs, not fades.** Fill the motion-language spec first (`library/easing_timing.md §0`): one
   persona, one signature curve, ≤3 house springs (card / snap / soft by default), one transition family. Banned: everything
   fading in, centered title on gradient, corner labels, frame borders, glow on UI, generic particles,
   hard cuts without a motivated transition.
8. **Pure function of t.** Seeded RNG only. No `Math.random`, `Date`, timers, CSS transitions,
   video elements. Pre-render text/paper canvases in `INITS`, never inside `draw`.
9. **Sample first.** Deliver a 20–60 s sample in the final style and get approval before the full film.
   After approval: build the rest in order, render in parts, upload each part.
10. **Verify before you upload.** Work → render stills → contact sheet → critique (≥3 rounds) → fix →
    render → check duration/frames/loudness/sync → upload. Never report "done" without these checks.
11. **GitHub is the home; the workspace is a cache.** Push after every meaningful step (sandboxes
    reset and wipe untracked files). Big videos go to Releases, not git. Keep the user's workspace clean
    (render in `/var/tmp`, delete temp files after upload) — users complain when it fills up.
12. **Talk to the user in their language** and keep reports short: link, what changed, what was checked,
    what's next. State tool limits honestly (e.g. image generation is capped at 10 per turn).
13. **Sound is placed and measured, never guessed.** You can't hear. Real CC0 recordings only (never
    synthesize hits, clicks or whooshes), cues computed from the picture's own springs (`engine/cues.js`),
    one mix by `sound-layer/scripts/mix.py`, and `qa.py` must pass (0 FAIL) on every delivered file.
    Never edit the vendored scripts or loosen a threshold. A human does the final ear check (`LISTEN.md`).
14. **Text moves like a pro, never like a slideshow.** Word-level Arabic (never per-letter, never letter-spacing:
    use kashida), one hero per moment, a partner shape for key words (shape and text never start/end on the same
    frame), holds with micro-life, exits shorter than entrances, continuous hand-offs instead of cuts
    (`library/kinetic_type_motion.md` §0). Adapt the grammar to each text's meaning; never copy a reference.
15. **Render fast, honestly.** Iterate with stills and `render.mjs --draft`; render finals once with `--workers auto`;
    estimate the time before long renders (`workflow/11_render_speed.md`).

---

## 1 · Pipeline (each step has a detailed file in `workflow/`)

| # | Step | Output | File |
|---|------|--------|------|
| 0 | **Creative Director intake** (skill `motion-director`): messy idea → one question round → research → 3 concepts → production prompt → one confirmation | `docs/brief.md`, `docs/production_prompt.md`, `docs/research.md` | workflow/00_intake.md |
| 1 | Setup repo + env, VO → word timings | `docs/vo_word_timings.json`, `docs/vo_timeline.md` | workflow/01_setup_and_vo.md |
| 2 | Treatment: core visual metaphor, section map, beat sheet per sentence | `docs/treatment.md`, `docs/shotlist.md` | workflow/02_treatment.md |
| 3 | Style bible: palette, type, surfaces, light, motion presets, composition grid | `docs/STYLE.md` | workflow/03_style_bible.md |
| 4 | Assets: real sourcing (Commons…), AI batches, processing (crop/upscale/cutout) | `assets/…`, `docs/CREDITS.md` | workflow/04_assets.md |
| 5 | Build: engine config + one scene file per VO section | `film/index.html`, `film/scenes/*.js` | workflow/05_build.md |
| 6 | Critique loop: stills → contact sheet → fix (≥3 rounds per section) | `docs/contact_*.jpg` | workflow/06_critique.md |
| ♪ | **Sound layer**: cues from code → real CC0 SFX + music → mix.py → qa.py (≤2 fix rounds) → LISTEN.md | `out/final.mp4`, `audio/qa.png`, `LISTEN.md` | workflow/10_sound_layer.md |
| 7 | Sample → approval → full build → part renders → final mix → release | Release `vX.Y` | workflow/07_render_deliver.md |
| 8 | GitHub ops, progress doc, cleanup, resume-from-zero | `docs/PROGRESS.md` | workflow/08_github_ops.md |
| T | **Kinetic text films** (lyrics/quotes/text-only, black stage, any aspect): `new_film.sh --kinetic --aspect 9:16` → motion pairs, kashida | `film/kinetic.html`, `film/scenes/*.js` | library/kinetic_type_motion.md |
| ⚡ | **Render speed**: draft while iterating, workers for finals, honest estimates | — | workflow/11_render_speed.md |
| ↺ | **Reference DNA** (whenever the user sends a reference video): measure + describe its grammar, never copy it | `docs/ref_dna/` | workflow/09_reference_dna.md |

## 2 · Rules (read before designing)
- **Arabic render gate:** if the project contains Arabic text, run `python3 tools/validate_arabic_project.py <project>` before any render. It must pass RTL direction, local Arabic font, font preload, and no horizontal mirroring; then inspect a rendered still for shaping, dots, numerals, and reading direction.
- `rules/design_rules.md` — composition, hierarchy, framing, typography, colour, density.
- `rules/motion_rules.md` — springs, pacing, transitions, camera, banned list, RTL motion.
- `rules/arabic_rtl.md` — Arabic typography & canvas pitfalls, numerals, diacritics, direction.
- `rules/audio_rules.md` — VO priority, what gets a sound, sonic families, SOUND LAYER gates, loudness.
- `rules/qa_checklist.md` — gates for every shot / section / final.
- `rules/pitfalls.md` — every failure we hit and the fix. Skim it once per project.

## 3 · Library (reusable know-how)
- `library/motion_vocabulary.md` — 30+ named techniques with code (card drop, write-on, paper tear,
  dot ruler, construction geometry, plate push, pin-on-photo, stagger list, compass draw, counter…).
- `library/style_presets.md` — ready style bibles: Sepia Manuscript Cinema, Paper Collage, Clean VOX
  Explainer, Dark Archive Documentary, Blueprint/Tech.
- `library/prompt_templates.md` — image-generation prompts per asset type & style (plates,
  portraits, objects for cutout, textures), with negative rules.
- `library/asset_sourcing.md` — Wikimedia Commons / museum open-access recipes, licences, crops.
- `library/user_feedback_patterns.md` — what clients actually ask for and reject (learned the hard way).
- **Pro layer (v1.1)** — read the one matching your current decision:
  - `library/easing_timing.md` — motion-language spec, personalities, duration/easing/spring/stagger tables.
  - `library/camera_language.md` — 2.5D depth planes, 15 camera moves, shot sizes, composition, multi-aspect.
  - `library/transitions.md` — 17 transitions with when/avoid, in-shot transitions, rhythm recipes, SFX pairing.
  - `library/kinetic_typography.md` — Arabic-safe kinetic type: roles, 8 entrance modes, VO sync, 20 techniques.
  - **`library/kinetic_type_motion.md` (v2.1)** — the pro kinetic-text system: 10 laws, Hero/Supporting/Accent, motion
    pairs (text + shape, 2–6 f offsets), 20 entrances / 12 exits / 14 partners → `engine/type.js`, kashida tracking,
    timing table, transitions, AE/CapCut mapping, creative-adaptation rules. Reference: `examples/reference_dna/kinetic_lyrics/DNA.md`.
  - `library/color_systems.md` — palettes in OKLCH, 60/30/10, perceptual mixing, grading order, 10 palettes.
  - `library/compositing_fx.md` — blend modes, grain/bloom/halation/CA/leaks/LGG grade, 8 finished LOOKS.
  - `library/fonts.md`: 41 bundled OFL families by role, 17 pairings, Arabic type rules for motion.
  - `library/resources.md` — the 2026 open-source motion ecosystem and what was distilled from each.
- **Dictionaries & resource packs (v1.2)**: everything below is embedded in the repo and works offline:
  - `library/glossary.md`: bilingual EN⇄AR motion-design dictionary (≈170 terms → where each lives in code).
  - `library/motion_recipes.md`: **84 named moves** (`engine/moves.js`: entrances/exits/emphasis/loops) + 12 combos.
  - `library/style_catalog.md`: **40 styles** mapped to engine values (palette, fonts, persona, moves, transitions, look, pattern).
  - `library/effects_dictionary.md`: effect name → engine call → reference shot card.
  - `library/gl_transitions.md`: **125 GPU transitions** (`tin:'gl:<Name>'`) with curated picks by intent.
  - `library/shot_cards_index.md`: English index of **124 vendored shot cards** (frame-timed recipes).
  - `library/fonts.md`: **41 bundled OFL families** (Kufi, Naskh, Thuluth-like, Ruqʿa, Nastaʿlīq, square Kufi, colour fonts…) by role + 17 pairings.
  - `library/icons.md`: **1877 Lucide icons** with exact draw-on. `library/patterns.md`: 13 procedural patterns (Islamic geometry + textures).
  - `library/color_systems.md §8`: 20 original heritage palettes + 1000 vendored palettes + Open Color.
  - Visual sheets: `library/specimens/*.jpg`. Vendored originals + licences: `resources/README.md`, `resources/NOTICE.md`.
- Reference DNA examples: `examples/reference_dna/DNA.md` (20 s Arabic app ad → preset F in style_presets) ·
  `examples/reference_dna/kinetic_lyrics/DNA.md` (3 Arabic lyric videos → kinetic grammar). Kinetic demo: `examples/kinetic_demo/`.

## 4 · Engine & tools (runnable)
```
engine/core.js        canvas engine: springs, paper/cards, photos, cutouts, write-on, lines/arcs,
                      plates+camera, god rays, grade (warm/grain/vignette), RTL paper-tear transitions,
                      SHOTS/INITS registry, window.seek(t)
engine/helpers.js     set(), plateM(), dropP(), onPiece(), nameBlock(), geoHalo(), blob(), goldify(),
                      counter(), liveText(), staggerIn(), callout()
engine/fx.js          PRO LAYER: Penner+bezier easings, CURVE, kf(), SPRINGS, PERSONA · simplex noise/wiggle/
                      handheld · OKLCH/mixOK/contrast · 2.5D camera cam()/layer() (dolly, truck, orbit,
                      vertigo, rack focus, impact) · tint/outline/extrude/echo/rgbSplit/pixelate/polaroid ·
                      post FX grain/vignette/bloom/halation/chroma/leak/fxGrade + LOOKS · kinetic type
                      layoutWords/drawWords/voTimes/maskReveal/marker/blurSwap/weightText · graphics panel/
                      handCircle/pathDraw/burst/sparkles/bubble/pill/cursor/ripple/sprite/phone/sticker/
                      scatter · TRANS: whip zoom flash dip iris clock blinds push slide barn luma glitch
                      smear band whipUp (shot.tin)
engine/gl.js          GPU runner: every shader of kit/data/gl_transitions.js → TRANS['gl:<Name>'] (shot.glParams)
engine/moves.js       MOVES dictionary (84 named moves) · move() · seqMove() · staggerMove() · movesBy()
engine/assets.js      palettes (palette/paletteRoles/applyPalette/palettesBy/HERITAGE/oc) · icon()/iconSearch() ·
                      pattern(kind, t, {k}): star8 rosette star6 star12 girihNet mashrabiya dots halftone grid lines waves iso topo
engine/kit/fonts/     41 OFL families + fonts.css + fonts.js (FONT_REGISTRY, fontsBy, fontLoads) + README (licences)
engine/kit/data/      palettes.js · icons_lucide.js · gl_transitions.js (vendored packs as JS globals, file://-safe)
engine/specimens.html visual browser of all packs (fonts, palettes, icons, patterns, moves, GL transitions)
engine/index.html     film page template (window.FILM config: palette, fonts, type scale; loads all packs)
engine/type.js        KINETIC TYPE (KT): word objects, kashida(), stretch(), show() with 20 entrances/12 exits/holds
                      (drift, wiggle, dim, echo, chroma), group() parenting/flip, partners dot leader comet ring underline
                      bar line hinge bubble panel orbit streak bokeh, spots()/place(), timeline(), post()
engine/kinetic.html   kinetic film page (9:16 default; canvas size = aspect) · scenes/kt_demo.js = 10 s template
engine/cues.js        SOUND LAYER cue registry: when.spring/ease/path → {start, peak, land} frames measured like qa.py;
                      cue.land/move/cut/appear/hero/raw → window.CUES
engine/scenes/demo.js 16 s demo = template for scene files (bottom: its sound cues)
tools/setup.sh        ffmpeg + playwright/chromium + uv (idempotent, re-run after resets)
tools/transcribe.py   VO → word timings (faster-whisper)      tools/find_word.py  word → time lookup
tools/still.mjs       stills at given times                    tools/cs.sh         contact sheet
tools/render.mjs      frame-exact render (2 sub-frames → motion blur) · --draft · --workers N|auto · reads canvas size
                      (v2.1: 4.8× faster final, 11× draft; workflow/11_render_speed.md)
tools/render_seg.py   chunked, resumable part render + preview mix
tools/sound_layer.sh  setup/verify/kit for film/sound-layer (upstream clone @ pinned commit, offline → vendor/)
tools/export_cues.mjs page → window.CUES (+ audio/sound.json) → audio/cues.json in mix.py --schema format
tools/encode_release.sh  1080p/720p release encodes (audio copied) + qa.py on each delivered file
vendor/opus-sound-layer/ sfx.py (1,139 CC0 sounds) · mix.py (peak-aligned −14 LUFS mix) · qa.py (measured gates). MIT, UNMODIFIED
tools/mix_final.sh    legacy VO+synth mix (pre-2.0). tools/cues_auto.py + tools/sfx.mjs: LEGACY synth SFX, not for hits/clicks/whooshes
tools/commons.py      Commons search/download with licence → docs/CREDITS.md
tools/cutout.sh       background removal (rembg, one process per image)
tools/gh.sh           push / create repo / upload release assets with a PAT file
tools/new_film.sh     scaffold a new film project (engine copy + tools + doc templates)
tools/video_dna.py    reference video → cuts, transitions (frame counts), flashes, palette+OKLCH, loudness,
                      onsets, contact sheets, shot keyframes, report.md (never copies the video)
tools/fonts.sh        download OFL Arabic/Latin families from google/fonts by name
tools/build_fonts.py  regenerate kit/fonts/{fonts.css,fonts.js,README.md}     tools/build_data.mjs  rebuild data packs from upstream
tools/build_docs.mjs  regenerate dictionary tables (moves, GL catalogue, icon index) from code
tools/specimens.mjs   regenerate library/specimens/*.jpg       tools/selftest.mjs  smoke-test engine + every pack
```
Start a film: `tools/new_film.sh /var/tmp/<film> [--kinetic] [--aspect 9:16]`. Quick check that everything works: `./tools/setup.sh && node tools/selftest.mjs && cd engine && PAGE=index.html ../tools/cs.sh demo 4 1.5 6.9 10.6 14.5`.

## 5 · Definition of done
- Final duration == VO duration (frames = round(dur × fps)).
- `uv run sound-layer/scripts/qa.py` → 0 FAIL on `out/final.mp4` **and** on each release encode (loudness −14 ±1 LUFS
  or −18 calm, TP ≤ −1, sync, audibility, voice clearance, picture match). What qa.png shows at each hero is written down;
  `LISTEN.md` (5 timecodes) + credits for every sound/music file used are delivered.
- Every section passed ≥3 critique rounds; no shot violates the density/legibility rules.
- Deliverables on a GitHub Release: `final_1080p.mp4` (≤ ~110 MB for 4 min), `final_720p.mp4`,
  `poster.jpg`, `contact.jpg`; code + assets + docs pushed; `docs/PROGRESS.md` explains how to resume.
- Workspace cleaned; tokens removed from disk; the user got a short report in their language.
