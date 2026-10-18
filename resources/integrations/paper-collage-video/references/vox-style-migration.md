# Vox Style Migration

## Purpose

Use this file when the user wants `paper-collage-video` to lean closer to a standard Vox mixed-media explainer look.

This migration is based on the `vox-motion-graphics.skill` Mixed Media branch, not its more cinematic paper-diorama branch.

The goal is not to replace the current skill.
The goal is to import the most useful Vox grammar into the current paper-collage workflow.

## What gets imported

Import these five things:

1. a flatter editorial visual system
2. a stronger motion-graphics rhythm
3. clearer chart / map / compare-and-contrast language
4. a stronger block-by-block script engine
5. stricter image prompt guidance for mixed-media scenes

## What does NOT get imported by default

Do not treat these as the new default:

- cinematic sepia diorama worlds
- fake-oner FPV camera in every scene
- prop-heavy letterpress text in generated frames
- hands-off full auto topic research pipeline

Those belong to the other skill's broader video factory logic, not to the core identity of `paper-collage-video`.

## Visual changes

### Original house look

The original `paper-collage-video` look is:

- tactile
- archival
- layered
- poster-like
- often locked-camera
- stronger on evidence boards, desk scenes, map walls, labels

### Vox mixed-media look

The imported Vox look should feel:

- flatter
- brighter
- more magazine-editorial
- more motion-graphics-driven
- better at charts, maps, comparisons, and symbolic explainers

Use this visual vocabulary:

- archival photo cutouts with rough white borders
- flat warm yellow, off-white, deep navy, coral red color fields
- halftone and paper grain textures
- hand-drawn marker circles, arrows, underlines
- abstract charts with no tiny real labels baked into the image
- flat maps with route lines and pulsing dots
- redaction bars and highlight blocks

## Motion changes

The current skill already supports layered motion and scene routing.
The Vox migration changes the energy profile:

- entrances can be faster and snappier
- one strong motion cue should land every few seconds
- push-ins and sweeps are allowed when they clarify emphasis
- one action should dominate a beat, not many equal actions at once

Do not over-import cinematic motion.
This is still motion graphics, not live-action emulation.

## Script changes

Import these story-engine rules:

- open with a question, stat, or reversal
- keep one idea per beat
- escalate through evidence beats
- use one recurring object or visual metaphor when possible
- land on a reframing ending, not a generic conclusion

Good imported pattern:

1. cold open
2. stakes
3. evidence beat
4. evidence beat
5. turn
6. kicker

This works especially well for `vo-sequence`.

## Scene-module changes

Vox migration strengthens these scene types:

- `data-viz`
- `editorial-page`
- `compare-and-contrast`
- `map-tracking`
- `marker-annotation`

If the beat is fundamentally about a number, relationship, route, or contrast, do not force it into an evidence-board tableau.
Let it become a flatter editorial motion-graphics scene instead.

## Prompt rules for Vox mixed-media

When `style_family=vox-mixed-media`, prefer prompts that explicitly say:

- editorial mixed-media collage
- archival cutouts with white paper borders
- flat bold color fields
- hand-drawn annotations
- abstract charts or maps
- non-photorealistic
- no live-action

Avoid prompt drift toward:

- cinematic concept art
- painterly digital illustration
- over-detailed historical diorama
- glossy 3D infographic renders

## Text rule

This is a big difference.

In the standard Vox mixed-media branch:

- generated imagery should usually avoid long readable text
- subtitles, labels, and explanatory copy are better handled in code or final assembly
- only very short label-like text should appear when absolutely necessary

Short dates, names, or evidence tags should also stay separate from generated imagery whenever code or final assembly can render them more clearly.

## Best-fit use cases

Prefer `vox-mixed-media` when the brief is:

- "make it feel like Vox"
- data-led
- comparison-led
- map-led
- question-driven
- more explainer than investigative board
- more editorial than tactile

## Migration summary

The skill now uses one visual system only: `vox-mixed-media`, an editorial motion-design paper world. Archival, mystery, evidence, and investigation topics must be translated into that same system through clear maps, comparison frames, timelines, chart devices, cutouts, and restrained annotations.
