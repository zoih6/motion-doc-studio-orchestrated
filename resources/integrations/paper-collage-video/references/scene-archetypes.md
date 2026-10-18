# Scene Archetypes

## Purpose

Use these archetypes to turn a narration beat into a scene module quickly. They are distilled from the Empire Downfall pack and are intended to be mixed within one locked visual system.

## 1. Cutout Rise

Best for:

- leaders
- workers
- symbolic objects
- paired characters in tension or comparison

Structure:

- scene-specific paper background using the shared sequence palette and texture grammar
- one or more transparent cut-outs in the midground
- offset silhouette or red marker stroke behind each cut-out
- foreground occluder or architectural anchor

Motion:

- staggered `spring()` rise
- light opacity fade
- slight scale settle if needed

Use when the beat introduces a person, faction, or visual conflict.

## 2. Editorial Page

Best for:

- newspaper headlines
- reports
- policy documents
- op-ed framing

Structure:

- background stays locked
- midground is a generated newspaper/page/layout image asset
- no heavy foreground needed unless it clarifies depth

Motion:

- page settles into frame
- slow push-in
- highlight sweep over the key phrase

Use when the beat is fundamentally textual and should be represented as one approved page image animated in Remotion, rather than drawn live as code typography.

## 3. Alpha Plate

Best for:

- waves
- fire
- smoke
- money burning
- other natural motion that is painful to fake with pure transforms

Structure:

- paper background
- transparent `.webm` or alpha video in the midground
- optional cut-out prop or generated number / metric card asset
- simple foreground band or object for anchoring

Motion:

- alpha video plays through
- approved image assets rise, count, or label the event

Use when motion texture matters more than precise cut-out styling.

## 4. Data Viz Pivot

Best for:

- inflation
- rankings
- debt
- growth or collapse curves
- benchmark comparisons

Structure:

- generated chart / map / comparison image asset, or a small set of layered PNG assets from the same visual family
- one supporting cut-out such as a map or icon
- one large numeric headline or label delivered as an approved image asset in the foreground

Motion:

- line or bars draw on
- chart repositions
- headline pops when the spoken number lands

Use when the narration contains a metric that should be seen, not merely mentioned, but keep the visible chart art asset-based rather than defaulting to live SVG drawing.

## 5. Compare and Contrast

Best for:

- labour vs military
- cost A vs cost B
- before vs after
- rival blocs

Structure:

- scene-specific background, unless continuity reuse was explicitly authorized
- left and right subject groups
- central or top label that frames the comparison
- optional common background subject like a map

Motion:

- entrances are compressed in short beats
- left side lands first if it sets the baseline
- right side lands second if it reframes the claim

Use when the narration makes an argument through contrast.

## 6. Speech Bubble Exchange

Best for:

- diplomatic beats
- trade deals
- implied dialogue
- sarcastic or illustrative editorial humor

Structure:

- hero cut-out pair or group
- one or two generated speech-bubble image assets
- foreground architecture or location plate

Motion:

- subjects land first
- bubbles pop in after the audience understands the scene
- slight float or tilt keeps the bubbles alive

Use when the beat benefits from compressing a geopolitical or economic shift into one readable exchange.

## 7. Typewriter Punchline

Best for:

- final thesis
- quote card
- concluding warning
- rhetorical payoff

Structure:

- background remains locked
- optional symbolic alpha plate or object below
- centered or block text reveal delivered as an approved text-card image asset
- optional vignette for closure

Motion:

- cumulative character reveal
- punctuation pauses
- blinking cursor
- final darkening or hold

Use when the beat is the takeaway line and should dominate the frame.

## How to choose

Map beats to archetypes by the thing the viewer most needs to understand:

- person or symbol: `cutout-rise`
- article or institution: `editorial-page`
- organic motion plate: `alpha-plate`
- metric or claim: `data-viz-pivot`
- opposition: `compare-and-contrast`
- implied conversation: `speech-bubble-exchange`
- thesis line: `typewriter-punchline`

## Composition archetypes for metaphor-led Remotion scenes

The module names above describe content treatment. The following layout archetypes define spatial composition and must be implemented through actual asset anchors and motion. Do not use them as labels only.

- `asymmetric-stage`: one oversized focal subject occupies one side or corner while supporting evidence assembles through a deliberate negative-space corridor.
- `diagonal-cascade`: causes and consequences descend or rise along a diagonal; each item lands after the previous item changes the path.
- `split-contrast`: two unequal zones oppose each other across a seam, scale, tear, or central pressure point; avoid symmetrical card boxes unless symmetry is the argument.
- `radial-cycle`: assets orbit, converge, or propagate around a center to explain loops, feedback, contagion, or circulation.
- `depth-tunnel`: foreground, midground, and background form a corridor; subjects advance, retreat, narrow, or disappear through depth.
- `stacked-consequence`: claims accumulate vertically like weights, documents, shelves, sediment, or domino layers until the stack tips or compresses.
- `map-route`: a path, border, network, or journey is the main reading device; the route draws first and subjects travel along it.
- `full-frame-data`: chart axes or a stable data field occupy most of the frame; lines, bars, markers, and annotations are separate assets that draw, grow, or land in sequence.

Choose the archetype by asking what physical relationship best explains the sentence: opposition, accumulation, circulation, narrowing, replacement, propagation, distance, or scale. Across a sequence, do not repeat the same archetype in adjacent Scenes and do not let one archetype dominate by convenience.

## Metaphor transformation library

Use this as a thinking aid, not a list of mandatory symbols:

| Narrative relationship | Possible physical metaphor | Motion that proves it |
| --- | --- | --- |
| scarcity, contraction, reduced flow | narrowing funnel, draining reservoir, shrinking doorway | units drain, squeeze, or fail to pass through |
| delay, waiting, deferred action | frozen conveyor, held hand, calendar shadow moving past a still object | time marker advances while the subject remains locked |
| feedback loop, vicious cycle | tightening spiral, conveyor loop, domino ring | the result visibly feeds back into the cause |
| tradeoff, opposition | weighted scale, torn seam, tug-of-war field | sides counter-move and one side changes the balance |
| accumulation, pressure | stacked papers, weights, sediment, shelves | layers pile up until the stack compresses, tips, or breaks |
| propagation, contagion, transmission | fuse, route, ripple, branching network | a signal travels node by node in content order |
| replacement, displacement | peeled page, sliding nameplate, receding silhouette | old state remains readable before the new state covers or pushes it away |
| inequality, concentration, dominance | unequal shadows, oversized container, one magnet pulling many pieces | scale or attraction changes the spatial hierarchy |
| threshold, tipping point | bending plank, filling vessel, stretched paper seam | gradual build reaches one decisive snap, spill, or tear |

Avoid generic icon substitution. A coin standing for “money” is literal; coins being squeezed through a narrowing aperture to show contraction is explanatory.
