# Vox-Style Sequence

## Use this reference

Read this file when the project is an editorial explainer, B-roll sequence, or voiceover-led collage piece made of multiple scenes rather than one handcrafted shot.

## Core idea

The narration is the timeline. The scene list exists to serve the spoken beats, not the other way around.

After the Vox migration, strengthen that rule with a proper explainer engine:

- open with a question, stat, or reversal
- let each block answer one narrow sub-question
- escalate through evidence beats
- land the reframing line near the end

Treat the workflow like this:

1. Transcribe or finalize the narration.
2. Split the narration into beats.
3. Group beats into scenes.
4. Assign one visual grammar to the full sequence.
5. Build each scene as a self-contained module.
6. Assemble all scenes in one master Remotion sequence.

## Locked visual system

The Empire Downfall pack shows a stable editorial grammar that stays fixed while the subject matter changes:

- one shared paper-texture and palette system, with a scene-specific background plate by default
- compact but chromatic `0720-bright-paper` palette with one signature accent color
- transparent cut-outs for subjects
- an offset silhouette or marker stroke behind those cut-outs
- a foreground anchor, caption, chart, counter, or label that grounds the shot

Keep this locked across the whole piece so each scene feels like one show.

Do not confuse visual continuity with literal background reuse. Unless the user explicitly requests one continuous location, every scene must generate a different background plate that reflects its own environment and visual goal. Follow `vox-motion-contract.md` for asset counts, subject sizing, and motion order.

If the chosen style family is `vox-mixed-media`, lock these extra cues across the sequence:

- one dominant flat background color per scene
- at least three meaningful chromatic hues per scene, with a cool/warm counterpoint and a separate dark anchor
- cream, tan, brown, and gray remain supporting paper materials rather than the default dominant field
- one consistent accent system across all charts, markers, and maps
- one repeating annotation language such as circles, underlines, or redaction bars
- one quiet background logic across the whole sequence: broad shapes first, accents later, clutter never by default

## Scene grammar

Each scene usually uses three planes:

1. background
2. midground subject or generated visualization asset
3. foreground anchor or occluder

Examples of valid midgrounds:

- halftone leader cut-outs
- keyed alpha video like fire or water
- newspaper front page generated as an image asset
- line chart or map generated as an image asset
- speech bubbles, labels, or comparison boards generated as image assets

Examples of valid foreground anchors:

- White House facade
- price counter band
- debt label
- building silhouette
- typewriter text block

Background rules for Vox-style sequences:

- the background should communicate one environment idea, not many
- prefer one large wall / sky / map / terrain field plus one structural band
- keep decorative scraps and graphic stickers out of the background unless they carry narrative meaning
- if a red circle, arrow, dot grid, or paper scrap matters, promote it to its own accent asset rather than baking it into the background

## Timing grammar

Start from narration windows, then map them to scene durations.

Rules:

- let the voice line define the beat
- allow one scene to carry multiple beats when the visual idea stays coherent
- compress entrances in short windows instead of adding more scenes
- time key reveals or counters to specific spoken words

Imported Vox timing rules:

- one strong motion emphasis every few seconds
- one memorable reveal across the whole piece
- when possible, carry one recurring object or metaphor across multiple scenes

## Preferred scene modules

Reuse these module types when appropriate:

- `cutout-rise`: spring-in portraits or objects with a red stroke
- `editorial-page`: generated newspaper, article, or document asset with highlight sweeps
- `data-viz`: chart draw, map stage, number pop, benchmark compare
- `alpha-plate`: transparent `.webm` layer like keyed ocean or burning bill
- `speech-bubble`: comic bubble plus cut-out dialogue
- `typewriter-punchline`: timed text reveal with cursor and dwell
- `marker-annotation`: one subject clarified by circles, arrows, sweeps, or blocks
- `map-tracking`: flat map plus route draw-on and location pulses

## Sequence assembly

Use a master `Series` component to chain scene modules in order. Keep scene duration constants and prop presets close to the sequence assembly layer so retiming is easy.

Store:

- one duration constant per scene
- one prop object per scene
- one master total duration
- optional baked-audio switch so the render can stay silent while stems ship separately

## Audio handling

For editorial explainers, treat voiceover as the canonical time source.

Prefer this structure:

- VO stem
- music stem
- optional sparse effects

If the workflow benefits from external finishing, keep the comp render silent by default and ship stems separately.

## Asset production rules

- keep each scene folder self-contained
- store a short `SCENE.md` with beat, assets, timing, and tuned props
- favor transparent PNGs for people and objects
- use alpha video for complex natural motion
- in `remotion-code` mode, keep visible editorial surfaces asset-based by default: generate them with `imagegen` / Imagen, then animate them in Remotion
- keep each scene-specific background plate visually quiet and reusable across retiming of that scene

## What to preserve from the source style

- tactile paper base
- bright chromatic editorial hierarchy plus a controlled bold accent
- motion graphics discipline instead of cinematic camera language
- word-synced reveals
- per-scene modularity

## What Vox migration changes

When `style_family=vox-mixed-media`, shift the center of gravity slightly:

- from tactile evidence tableau toward clearer editorial communication
- from desk / board logic toward chart / map / comparison logic
- from mostly restrained motion toward snappier emphasis motion
- from embedded text objects toward cleaner non-text visual explanation
