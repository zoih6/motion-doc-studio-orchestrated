# Remotion Build

## Use this reference

Read this file when the task moves from planning into implementation or tuning of a Remotion-based collage scene or a voiceover-led editorial sequence.

## Favor a stable composition structure

Use a composition tree that separates environment, hero props, characters, overlays, and audio.

Suggested structure:

```text
Composition
|- SceneBackground
|- RevealRig
|- LayerStack
|  |- Sky and clouds
|  |- Back wave layers
|  |- Hero insert depth slot
|  |- Front wave layers
|  |- Foreground accents
|- CharacterRig
|- AudioRig
```

Keep each major prop in its own file or prop object so it remains tunable.

For multi-scene sequences, keep each scene in its own component and create one master sequence component that owns durations, scene order, and audio policy.

## Use a data-first prop model

Expose controls for:

- position x/y
- scale
- rotation
- entry and exit frames
- loop amplitudes and durations
- hold length for stepped motion
- shadow or offset amount when stylistically needed
- audio start frame and gain

Store defaults in a single config object or JSON file so the user can tune the scene without rewriting component logic.

For `vox-mixed-media`, treat the scene `ASSETS.json` as the source of truth. Every moving asset must expose `content_kind`, `frame_occupancy`, `appearance_order`, entrance `motion`, and semantic `action_motion`. Implement entrances in ascending `appearance_order`; do not infer a new order inside the React component. Size portrait subjects by height, wide groups/cards/strips by width, and isolated props by a bounded box. The non-driving dimension is a maximum cap. Follow `vox-motion-contract.md` and validate projected visible alpha occupancy, not merely the CSS container.

The generated `VoxManifestScene` must execute, not merely mention, `layout_archetype`, `reading_path`, `dominant_axis`, `foreground_strategy`, `motion_rhythm`, `action_motion.type`, `motion.exit`, and `final_hold_start_pct`. Semantic action types may share interpolation helpers, but they may not collapse into one undifferentiated slide. Path-follow actions use `path_points_pct`; draw/reveal/highlight actions use a directionally revealed isolated raster; emphasize/stamp actions use a bounded one-shot pulse. Ambient drift must decay to zero by the final hold.

Run semantic action after entrance and before the final hold. A retreating subject, pursuing army, converging pair, or replacement pair must visibly change position by the manifest amount; ambient drift begins only after that action finishes.

For editorial sequences, mirror saved `defaultProps` at the composition layer and keep sequence-time retiming in the master assembly component.

## Build motion from loops

Prefer sine, triangle, or eased interpolation loops over dense keyframe data.

Typical mappings:

- cloud drift: very long duration x-axis movement
- wave parallax: per-layer drift with larger amplitude up front
- boat rock: rotation around a low pivot near the waterline
- boat bob: small y-axis loop offset from rock phase
- gull glide: long arc with a small wing tilt or float

Typical editorial mappings:

- portrait or object entrance: `spring()` rise with opacity fade
- chart draw: `interpolate()` over stroke length or point reveal
- highlight sweep: easing-driven width mask over text
- counter: integer interpolation timed to a spoken noun or number
- typewriter punchline: cumulative character reveal with punctuation pauses

## Add stepped motion with quantized frames

Use frame quantization for characters and hero inserts. Keep the render at full fps while only updating those elements on held frames.

Pseudo-logic:

```ts
const pattern = [0, 1, 0, 0, 1, 0, 1, 1, 0, 0];

function quantizeFrame(frame: number, hold: number, uneven: boolean) {
  if (hold <= 1) return frame;
  if (!uneven) return Math.floor(frame / hold) * hold;

  const holds = pattern.map((extra) => hold + extra);
  const cycle = holds.reduce((sum, value) => sum + value, 0);
  const base = Math.floor(frame / cycle) * cycle;

  let acc = 0;
  for (const bucket of holds) {
    if (frame - base < acc + bucket) return base + acc;
    acc += bucket;
  }

  return base + acc;
}
```

Use the quantized frame to drive only the stepped layer's transforms.

In Vox-style explainers, reserve stepped quantization for rare emphasis moments. Most editorial motion should feel clean and word-synced.

## Build the silhouette stroke

When the style calls for the Vox-like marker treatment, render a tinted silhouette behind the cut-out using CSS mask images.

Pattern:

```tsx
<div
  style={{
    ...sameBox,
    backgroundColor: "#E04329",
    maskImage: `url(${assetUrl})`,
    WebkitMaskImage: `url(${assetUrl})`,
    maskSize: "100% 100%",
    WebkitMaskSize: "100% 100%",
    transform: `translate(-50%, ${offsetY}px)`,
  }}
/>
<Img src={assetUrl} style={{ ...sameBox }} />
```

This is best for portraits, leaders, workers, buildings, and other editorial cut-outs.

## Implement the sandwich depth trick

Split a container prop into:

- full or back plate
- inserted character layer
- front slice cut from the same source art

Use the same original image for front and back whenever possible so the seam stays invisible.

## Stage the reveal

Build a dedicated reveal rig instead of burying reveal math inside every component.

Common reveal options:

- two roll edges move apart
- a mask widens over time
- layers slide in with a small bounce settle
- a highlight wipe sweeps across a headline
- a chart line draws from left to right
- a label or bubble pops on after the subject lands

Hand the reveal rig an overall progress value, then derive child offsets from it.

## Keep audio declarative

Define each cue with:

- src
- startFrame
- endFrame or duration
- volume
- fadeInFrames
- fadeOutFrames

Keep cue timing near the same config object as visual timings so scene revisions stay coordinated.

For narration-led sequences, expose a `BAKE_AUDIO` or equivalent switch so the project can render either:

- silent picture plus stems
- fully mixed reference video

## Assemble a master sequence

For multi-scene explainers, use:

```text
MasterSequence
|- optional Audio stem layer(s)
|- Series
|  |- Scene 01
|  |- Scene 02
|  |- Scene 03
```

Keep one duration constant per scene and a total-duration export.

## Keep scenes self-contained

A strong packaging pattern is one folder per scene containing:

- `SCENE.md`
- `SceneName.tsx`
- local image or alpha-video assets
- scene-specific `background.png`; share only palette and texture rules unless continuity reuse was explicitly authorized

This keeps coding agents and collaborators aligned when rebuilding from a pack.

## Final tuning checklist

- Verify silhouette readability with motion disabled
- Verify parallax ordering with backgrounds alone
- Verify stepped motion only affects chosen props
- Verify front-slice layering hides the insert correctly
- Verify audio cues do not crowd the music bed
- Verify render settings match runtime, fps, and resolution

## Use the shared runtime and hard render gates

- Never run project-local `npm install` by default. Run `npm run runtime`; it creates or reuses the fingerprinted runtime under `~/.codex/cache/paper-collage-video/remotion-runtime/` and writes a matching lockfile.
- `npm run preflight` must pass composition blueprint, asset/provenance, and TypeScript checks before Studio or render.
- `npm run render` creates a rough render, samples establishment, every narrative entrance, the dominant action payoff, and final hold, then verifies duration, fps, resolution, and audio presence.
- Inspect `05_render/layout-audit/contact-sheet.jpg`, approve the hash-bound `review.json`, and run `npm run finalize`. Do not call the rough output a final deliverable.
