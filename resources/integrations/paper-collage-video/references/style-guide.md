# Style Guide

## Style thesis

This look works because it combines handmade paper textures with deliberately coded motion. The scene feels tactile, but the timing feels designed.

This skill supports one visual family: `vox-mixed-media`. It combines tactile source materials with flat, bright, snappy editorial composition and motion.

## Visual system

### `vox-mixed-media`

- archival cutouts with rough white borders
- flat bold color fields
- halftone and paper grain texture
- hand-drawn circles, underlines, arrows
- abstract charts and maps
- redaction or highlight blocks
- quiet backgrounds with only one environment idea at a time

Always translate the brief into this Vox explainer grammar rather than a dense investigative evidence board.

### Materials

Use visibly fibrous paper, kraft or watercolor textures, and imperfect cut edges. Favor transparent PNG cutouts with their final treatment baked in.

### Edges

Use one or more of these edge treatments:

- Torn ragged edge with white fibers
- Thin white sticker outline around silhouettes
- Rough scissor-cut geometric accents

Avoid clean vector-perfect edges unless they are a deliberate contrast shape.

### Palette

The default palette direction is `0720-bright-paper`. Read
`0720-bright-paper-style.md` before writing prompts. Use a small but genuinely
chromatic palette. The source reference succeeds with:

- Sky blue paper background
- Near-white to deep navy wave stack
- Mustard or marigold accents
- Black ink or halftone line art
- One warm secondary accent such as pink

Keep the palette legible in thumbnail view. Quiet means low detail, not low
saturation. Off-white, tan, kraft brown, gray, and muted green may support the
paper material, but they may not become the default dominant palette.

For `vox-mixed-media`, shift the palette logic:

- one dominant chromatic background field per scene
- at least two chromatic support colors plus one warm/cool focal counterpoint
- bright editorial accents such as marigold, coral red, turquoise, leaf green, deep navy, or cacao orange
- use off-white as fiber, edge, foam, cloud, label, or negative space rather than washing the whole frame beige
- keep one accent system locked across the whole sequence
- do not mix too many archival browns and muted desk tones
- keep background contrast broad and simple rather than filling it with many collage scraps
- preserve separate lightness roles for background, structure, hero, and accent
- change the dominant/support balance between adjacent Scenes while keeping the material grammar consistent

### Composition

Use broad horizontal strips for environment layers and a few vertically distinctive hero props. Give the scene a clear foreground strip, a readable horizon, and one hero object that breaks the layer rhythm.

Background discipline:

- one quiet background idea per scene
- one stable horizon or wall plane
- only large environment shapes in the background
- no decorative sticker clutter in the background by default
- no surprise extra props or people behind the hero
- marker circles, underlines, and paper scraps should appear only when they clarify meaning and should usually live as separate accent assets

### Derived depth trick

Create depth by reusing the same source asset as multiple layers. The canonical example is the sandwich:

- back object
- character or insert
- front slice cut from the same object

Use this whenever a subject must feel inside a boat, car, frame, doorway, or window.

## Motion system

### `vox-mixed-media`

- snappy ease-out entrances
- fast pop, slide, sweep, underline, circle-draw
- deliberate push-ins on emphasis beats
- one loud motion at a time, but keep something moving

### Reveal grammar

Start from a hidden or compressed state, then let the scene open mechanically. The source kit uses a scroll opening into layered ocean strips, but the deeper rule is:

- begin closed
- reveal via a simple physical metaphor
- hold on a living tableau

### Layer behavior

Assign different motion classes to different depths:

- Back layers: slow, smooth drift
- Mid layers: slightly faster drift or horizon bob
- Front layers: largest amplitude and fastest parallax
- Characters: stepped, irregular stop-motion feel

### Uneven holds

Use stepped motion with irregular hold lengths on characters and hero props. Even 2-frame holds look like low frame rate. Uneven 2- to 3-frame holds look hand-placed.

### Contrast rule

Do not posterize the whole scene. Keep backgrounds smooth and characters stepped so the contrast reads as intentional.

For `vox-mixed-media`, allow flatter motion-design behavior in charts, maps, and color panels, but still preserve one readable focal action per beat.

Keep the background visually calmer than the moving subject layer. If the background competes for attention, simplify it before changing motion.

## Vox migration rules

When migrating Vox style into this skill, preserve these imported rules:

- the frame is a motion-designed editorial collage, never a filmed scene
- narration lines should visualize ideas, not talking heads
- charts, maps, and comparison graphics can carry meaning as primary subjects
- marker circles, sweeps, and blocks are structural devices, not decoration
- long readable text should generally stay out of generated imagery
- backgrounds should stay broad, quiet, and low-clutter unless the brief explicitly asks for a dense evidence-board look

Do not import these blindly:

- hyperactive fake-oner camera language into every scene
- cinematic sepia diorama grammar when the brief only asks for standard Vox mixed-media
- lots of prop text inside generated frames

## Asset prompt rules

Include these ideas directly in prompts when needed:

- torn ragged edge
- visible white paper fibers
- paper grain
- sticker border
- transparent background
- vintage engraving or halftone texture
- watercolor or gouache wash for broad environmental strips

Prompt for the material, not just the subject.

## Sound system

Use sound as support, not spectacle.

Typical mix:

- one stylized music bed
- one reveal foley cue
- one light ambience or texture layer
- one accent cue

Cut cues aggressively in short runtimes.

## What not to do

- Do not flatten all layers onto one plane
- Do not rely on postprocess filters to invent texture that prompts should provide
- Do not add many tiny props that clutter the silhouette
- Do not let the background become a second foreground
- Do not use perfectly regular step timing on characters
- Do not over-score a short scene with too many cues
