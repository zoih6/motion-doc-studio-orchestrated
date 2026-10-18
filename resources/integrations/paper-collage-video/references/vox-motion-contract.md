# Vox Scene Asset and Motion Contract

## Purpose

Use this contract for every `vox-mixed-media` scene built with `remotion-code`.
It prevents repeated poster layouts, underspecified asset packs, and motion that ignores narration order.

## 0. Metaphor-first composition gate

Do not begin with asset slots. Begin by translating the Scene's abstract claim into one concrete visual mechanism.

Every Scene manifest must lock these fields before image generation:

```yaml
visual_metaphor:
  abstract_claim: the exact idea the narration must explain
  concrete_metaphor: one physical image or mechanism that makes the idea visible
  mapping: a specific A-means-B mapping between image parts and the claim
  motion_payoff: the visible change that proves the claim instead of merely decorating it
  asset_ids: [the assets that perform the metaphor]
composition:
  layout_archetype: asymmetric-stage | diagonal-cascade | split-contrast | radial-cycle | depth-tunnel | stacked-consequence | map-route | full-frame-data
  reading_path: left-to-right | right-to-left | top-to-bottom | bottom-to-top | diagonal-down | diagonal-up | radial-in | radial-out | serpentine | center-out
  dominant_axis: horizontal | vertical | diagonal | radial | depth
  foreground_strategy: none | corner-occluder | side-frame | lower-band | full-depth-prop | entering-subject
  negative_space_intent: which later entrance or relationship the empty area serves
motion_rhythm: sequential-build | cause-then-effect | counter-motion | radial-convergence | path-follow | scale-shift | replacement | cascade | draw-and-land
```

The mapping must be causal and concrete. “Use economic icons” is not a metaphor. “Coins drain through a narrowing funnel; the narrowing mouth represents reduced money supply and the shrinking shop silhouettes below represent contracting demand” is a usable metaphor.

Composition rules:

- The chosen layout must be derived from the metaphor's spatial relationship, not selected because a template already exists.
- `module_type` or `layout_archetype` is not a documentation label. Asset anchors, depth order, reading path, entrance directions, and action motion must visibly implement it.
- A lower strip is optional. Use `foreground_strategy=lower-band` only when the narration actually needs ground, accumulation, consequence, or occlusion at the bottom.
- Do not default to a center hero, one left support, one right support, and one full-width lower band.
- Adjacent Scenes may not reuse the same `layout_archetype` or the same derived composition signature.
- A sequence of 4 or more Scenes must use at least 3 layout archetypes and at least 3 motion rhythms.
- `lower-band` may appear in at most one third of a sequence's Scenes, rounded up, and never in adjacent Scenes.
- Across the sequence, vary at least three of these: focal position, reading path, dominant axis, depth strategy, scale relationship, entrance origin, and final silhouette.
- Keep style continuity through palette, paper texture, edge treatment, and annotation language. Do not confuse continuity with repeating coordinates.

Metaphor motion rules:

- Every Scene needs one dominant motion that completes `motion_payoff`.
- Motion must change a relationship: drain, squeeze, split, stack, orbit, replace, collide, tip, pull, reveal a path, or propagate a consequence.
- Merely sliding three finished pictures into empty boxes does not satisfy the metaphor contract.
- When the content describes a process, split the process into independently timed parts so the viewer sees cause before effect.
- When the content describes a chart or route, separate the stable frame/axes from the line, bars, markers, or path so the information draws or travels rather than swapping whole cards.
- The final hold must preserve the completed metaphor and make its mapping readable without narration.

## 0A. Bright-paper color script gate

Apply `0720-bright-paper-style.md` before the background-stage gate. Every Scene
must lock this schema before any image generation:

```yaml
color_script:
  style_reference: 0720-bright-paper
  dominant_field: sky blue fibrous paper
  support_colors: [deep ocean blue, leaf green]
  focal_accent: marigold orange
  dark_anchor: deep navy
  paper_neutral: fibrous cream white
  area_budget:
    dominant_pct: 45
    support_pct: 28
    neutral_pct: 18
    accent_pct: 9
    archival_brown_gray_pct: 8
  hero_background_contrast: how hue and lightness separate every focal asset from its landing zone
  adjacent_scene_shift: how this Scene changes dominant hue or color balance from its neighbor
  prompt_palette_sentence: one exact palette sentence copied into every image prompt
  negative_palette_terms:
    - no sepia wash
    - no all-beige palette
    - no muddy brown-gray cast
    - no desaturated vintage filter
    - no monochrome kraft-paper scene
    - no faded low-contrast look
  user_palette_override: false
  override_reason: ""
  review:
    three_chromatic_hues_present: false
    hero_separates_at_thumbnail: false
    no_muddy_global_cast: false
    palette_match_across_assets: false
```

Rules:

- Use at least three meaningful chromatic hues in every Scene unless the user explicitly authorizes a limited-palette override.
- The default neutral area may not exceed 25%; brown, gray, tan, and archival desk tones combined may not exceed 20%.
- Background can be colorful and still quiet. Lower edge density and detail inside reserved zones instead of draining saturation.
- Hero and landing zone need a stated hue and lightness separation. A drop shadow alone is not sufficient.
- Every background and asset prompt must copy `prompt_palette_sentence` and all `negative_palette_terms` verbatim.
- Adjacent Scenes must shift dominant hue, warm/cool balance, or color-area proportions. Reusing the same faded palette is not continuity.
- Set the four review fields only after inspecting the actual generated background and assets together at thumbnail size.

## 0B. Background-stage and collision blueprint gate

Before generating the background or any moving asset, create one shared composition blueprint. Background and foreground prompts must be derived from the same blueprint; never prompt them independently and hope they fit later.

Required manifest fields:

```yaml
background_contract:
  role: stage-only
  allowed_elements: [broad terrain, wall, horizon, floor plane, low-contrast architecture]
  forbidden_subjects: [prompt-language aliases for every major moving subject and metaphor object]
  max_saliency: very-low | low
  semantic_overlap_forbidden: true
  reserved_zones:
    - id:
      asset_ids: []
      x_pct:
      y_pct:
      width_pct:
      height_pct:
      purpose:
      background_detail: none | very-low
  review:
    reserved_zones_clear: false
    no_duplicate_subjects: false
    focal_competition: fail | pass
collision_plan:
  default_max_overlap_pct: 8
  safe_gap_pct: 3
  motion_paths_reviewed: false
  allowed_overlaps:
    - asset_a:
      asset_b:
      max_overlap_pct:
      reason:
```

Planning order:

1. Place normalized rest boxes for every moving asset using `frame_occupancy`.
2. Apply `action_motion` to calculate each final box.
3. Reserve background zones that cover those boxes and their meaningful motion corridors.
4. Check pairwise overlap. Default overlap may not exceed 8% of the smaller box.
5. Allow larger overlap only for a stated semantic relationship such as an arrow touching its target, a subject entering a container, or a foreground occluder creating depth. Record the exact pair, maximum percentage, and reason.
6. Check entrance and action paths. A moving asset may not sweep through another readable subject unless the collision is intentional and allowlisted.
7. Generate the background only.
8. Inspect the actual background at thumbnail size. Reserved zones must be quiet, and the background must not contain a duplicate of any moving subject or metaphor object.
9. Set all three background review fields and `motion_paths_reviewed=true` only after inspection. Then generate foreground assets.

Background rules:

- Background is a stage, not a completed illustration.
- If the hero is a shop, house, vehicle, chart, machine, document, person, or other major object, do not place another detailed object of the same class behind its landing zone.
- Prefer broad floor, wall, street, horizon, terrain, shadow field, framing edge, or abstract geometry over detailed scene furniture.
- Keep strongest contrast, sharpest edges, warmest accent, and highest texture density out of reserved zones.
- “Empty storefront pad” is still a storefront-shaped object and can compete with a later storefront cutout. Use abstract side masses or a quiet street plane instead when storefronts are moving assets.
- Background prompts must explicitly repeat every `forbidden_subjects` alias in their negative constraints.

Collision rules:

- Use actual projected visible bounds after alpha crop for the final check, not only source-canvas size.
- Preserve at least `safe_gap_pct` between unrelated focal objects whenever the composition does not call for overlap.
- Text, charts, faces, price tags, and other high-information regions may not be casually occluded.
- Z-index does not make a collision valid. It only decides which mistake appears on top.
- If assets cannot fit without excessive overlap, reduce asset count, change layout archetype, split the Scene, or route it to Seedance.

## 1. Scene diversity contract

Default `background_policy` is `per-scene`.

- Generate one scene-specific background plate for every scene.
- Record a unique `background_concept` and `background_distinction_reason` in every scene manifest before image generation.
- Keep palette, paper grain, accent color, and annotation language shared across the sequence.
- Change the environment, dominant shape field, depth arrangement, and foreground anchor when the narration changes location, action, institution, or consequence.
- Adjacent scenes must differ on at least two axes: environment/location, dominant silhouette, depth arrangement, dominant geometry, foreground anchor, or negative-space direction. State those axes in `background_distinction_reason`.
- Do not reuse the same background file across scenes.
- Only use `shared-continuity` when the user explicitly asks for one continuous location or one recurring visual metaphor. Record `background_sharing_authorized: true` and explain the continuity reason.
- Do not generate all scenes on one image sheet. A generation sheet may contain assets for one scene only.

Every Remotion scene must have:

- 1 unique `background_plate`
- 1 independent `hero_cutout`
- at least 2 additional independent narrative assets chosen from the Scene's metaphor; their IDs and roles are content-specific
- optionally 0-4 additional support, environment, editorial, foreground, path, or accent assets
- 4-8 approved raster assets total, including the background
- at least 3 approved independently timed moving assets, excluding the background

Do not merge several independently moving story elements into one hero PNG. If the narration names or implies separate actors, props, causes, or consequences, generate them as separate assets.

## 2. Visible size and placement contract

Do not confuse an image element's CSS box with its visible subject. Transparent padding and `objectFit: contain` can make a nominally large asset look tiny. The Asset Gate measures the non-transparent alpha bounds and projects those bounds into the final frame.

Before composition:

- preserve the unmodified imagegen result under `02_assets/imagegen-originals/`
- alpha-trim every non-background final PNG to 3-5% transparent padding; visible alpha must cover at least 72% of both source-canvas axes
- classify every asset with `content_kind`
- choose one `sizing_mode`; do not set width and height as two competing target sizes
- inspect the real silhouette, not the source canvas, before locking the anchor

Content kinds and sizing modes:

| Content kind | Required sizing mode | Typical use |
| --- | --- | --- |
| `portrait-subject` | `height-driven` | one standing or seated person |
| `wide-group` | `width-driven` | army, crowd, comparison pair, landscape band |
| `object-prop` | `box-contain` | book, seal, weapon, well, isolated symbol |
| `editorial-card` | `width-driven` | map, quote card, chart or document |
| `foreground-strip` | `width-driven` | lower-edge terrain, table, rubble or consequence band |
| `accent-mark` | `width-driven` | circle, underline, arrow or stamp |

Minimum projected visible occupancy for horizontal `16:9`:

| Content kind | Hero minimum | Support minimum |
| --- | --- | --- |
| `portrait-subject` | 22% W and 50% H | 14% W and 28% H |
| `wide-group` | 44% W and 20% H | 30% W and 12% H |
| `object-prop` | 26% W and 24% H | 14% W and 14% H |
| `editorial-card` | 38% W and 22% H | same |
| `foreground-strip` | 72% W and 8% H | same |
| `accent-mark` | 10% W and 4% H | same |

Minimum projected visible occupancy for vertical `9:16`:

| Content kind | Hero minimum | Support minimum |
| --- | --- | --- |
| `portrait-subject` | 48% W and 30% H | 26% W and 18% H |
| `wide-group` | 68% W and 12% H | 52% W and 9% H |
| `object-prop` | 32% W and 12% H | 24% W and 12% H |
| `editorial-card` | 64% W and 18% H | same |
| `foreground-strip` | 86% W and 7% H | same |
| `accent-mark` | 18% W and 3% H | same |

These are minimum visible sizes, not recommended maxima. A support army may be wider than a portrait hero when the story requires pursuit, encirclement, or scale comparison. Keep ordinary subjects within a 4% frame bleed allowance and lower-edge foreground strips within 8%, both at rest and at the end of `action_motion`. Avoid a tiny hero floating in empty space, but preserve one clear negative-space corridor for the next entrance.

After a rough render, extract two review frames per Scene: one immediately after the main assembly and one during the final hold. Reject the Scene when the dominant metaphor cannot be named at thumbnail size, when empty space has no stated entrance/readability purpose, or when the largest meaningful subject feels secondary to the background. Manifest percentages are not a substitute for this visual review.

## 3. Narrative appearance order

Build `narrative_sequence` from the spoken or written content before writing motion code.

After checking every `narrative_token`, `appearance_reason`, size, and timing against the source, set `content_order_locked`, `composition_locked`, and `motion_plan_locked` to `true`. The asset Gate must fail while any lock remains false.

Rules:

- `background_plate` is order `0`; it establishes place and does not count as a narrated element.
- Give every independently moving narrative asset one unique integer `appearance_order`, starting at `1` with no gaps.
- Give every asset a concrete `appearance_reason` explaining which phrase, first mention, or causal step places it at that position.
- Elements enter in the same semantic order as their first mention or causal appearance in the content.
- A support asset may appear early only when it is fixed environmental context; record that reason explicitly.
- Do not show the consequence before the cause, the replacement before the replaced subject, or an annotation before the object it explains.
- Marker circles, arrows, route lines, labels, and redaction blocks appear after their target is readable.
- The manifest `narrative_sequence` array must list asset IDs in exact entrance order.

Example:

```yaml
narration: 赵王命赵括替代廉颇，抵御秦军。
narrative_sequence:
  - king_order
  - lian_po
  - zhao_kuo
  - qin_threat
appearance_logic:
  king_order: the command enters first
  lian_po: the current general appears next
  zhao_kuo: Zhao Kuo replaces and occludes Lian Po
  qin_threat: the opposing force appears last as the consequence and destination
```

## 4. Vox motion timing

Use scene-relative percentages so the contract survives retiming.

The following is only a safe timing envelope, not a reusable Scene template:

- `0-10%`: scene-specific background cuts or settles in
- `8-32%`: first narrated subject enters
- `22-52%`: support elements enter one by one in narrative order
- `45-70%`: editorial surface or annotation explains the relationship
- `70-100%`: final composition holds as a living editorial poster

Choose timing from `motion_rhythm` and the content order. Do not copy the same start percentages into every Scene. Typical rhythm shapes:

- `sequential-build`: one new element every 12-20% of the Scene
- `cause-then-effect`: cause enters and acts first; effect enters only after the action is readable
- `counter-motion`: opposing elements enter from different zones and move toward or away from a shared seam
- `radial-convergence`: elements arrive around the perimeter, then converge or orbit
- `path-follow`: the path draws first; subjects begin traveling only after enough route is visible
- `scale-shift`: the focal subject establishes, then its scale change drives the claim
- `replacement`: old state is readable before the new state displaces or covers it
- `cascade`: repeated elements enter in tight serial steps along a diagonal or vertical stack
- `draw-and-land`: stable frame appears first, line/path draws, marker or conclusion lands last

At 30 fps, stagger separate entrances by 4-10 frames. Do not launch every element on the same frame.

Use these motion families:

| Layer | Entrance | Settle | Hold |
| --- | --- | --- | --- |
| Background | hard cut, 6-12 frame fade, or 1-2% scale settle | no bounce | 1-2% total drift maximum |
| Hero | 12-20 frame spring or decisive slide, 8-14% frame travel, scale 0.92-1.0 | one small overshoot | 0.5-1.5% vertical drift or 0.3-0.8 degree tilt |
| Support | 8-16 frame slide/pop, 5-10% frame travel | short staggered settle | smaller amplitude than hero |
| Editorial surface | 12-24 frame wipe, unfold, page place, or mask reveal | no elastic wobble | usually locked |
| Marker/accent | 8-16 frame draw-on, sweep, circle, underline, or redaction wipe | stop cleanly | optional 1-2 frame pulse once |
| Foreground anchor | 12-18 frame rise from lower edge, 4-8% frame height | light settle | locked or 0.5% parallax |

Supported manifest values:

- `entrance`: `cut-or-fade`, `fade-in`, `spring-rise`, `slide-in`, `rise`, `pop-in`, `wipe-on`, `draw-on`, `page-place`, `mask-reveal`, `unfold`
- `direction`: `none`, `bottom`, `top`, `left`, `right`, `side`, `left-to-right`, `right-to-left`, `target-dependent`
- `settle`: `none`, `small-overshoot`, `short-settle`, `light-settle`, `clean-stop`, `no-bounce`
- `exit`: `hold-to-cut`

Entrance motion only answers how an asset arrives. If the narration describes an action, add a separate `action_motion` after the entrance:

Optional action fields:

- `path_points_pct`: two or more frame-relative translation points for route/path motion
- `reveal_direction`: `left-to-right | right-to-left | top-to-bottom | bottom-to-top` for draw/reveal/highlight assets
- `pulse_scale`: one-shot scale amplitude for emphasize/stamp/pulse actions

| Narrated intent | `action_motion.type` | Required motion |
| --- | --- | --- |
| retreat or withdraw | `retreat` | move 8-20% away from the threat |
| advance or chase | `advance` or `chase` | move 8-20% toward the target |
| encircle or converge | `converge` | use separate assets moving 8-18% toward the center |
| scatter or collapse | `diverge` | move separate assets 8-18% away from the impact |
| replace one subject | `replace` | new and old subjects use opposing 6-14% moves |
| reveal a fact | `reveal` | controlled wipe or short positional reveal |
| emphasize a conclusion | `emphasize` or `stamp` | scale by at least 0.04, then hold |

Use one dominant semantic action per beat. `action_motion` begins when the entrance is readable, ends no later than 75% of the scene, and must not replace the final hold. Never use passive drift as a substitute for retreat, pursuit, convergence, replacement, defeat, rise, or fall.

The Gate scans the complete scene narration, not only asset labels. A scene mentioning retreat requires at least one `retreat` action; pursuit requires `chase` or `advance`; encirclement requires `converge`; replacement requires `replace`; defeat requires `diverge`, `emphasize`, or `stamp` on the relevant result layer.

Vox energy rules:

- Land one dominant motion cue per beat.
- Use clean word-synced motion for most elements.
- Reserve stepped stop-motion quantization for one chosen emphasis element, not the whole scene.
- Keep the camera locked by default. A push-in may be 2-4% over the scene only when it clarifies emphasis.
- Do not give background, hero, support, markers, and typography equally strong simultaneous motion.
- Complete the meaningful assembly by 70% of the scene, then hold long enough to read.

## 5. Required per-asset fields

Every approved moving asset in `ASSETS.json` must include:

```json
{
  "path": "07_remotion/public/scenes/scene-01/hero-cutout.png",
  "source": "imagegen",
  "approved": true,
  "provenance": {
    "method": "built-in-image_gen",
    "tool_called": true,
    "result_receipt": "generated image output hint",
    "prompt_file": "02_assets/prompts/scene-01/hero-cutout.md",
    "prompt_sha256": "...",
    "original_path": "02_assets/imagegen-originals/scene-01/hero-cutout.png",
    "original_sha256": "...",
    "final_sha256": "...",
    "postprocess": "remove-chroma-key",
    "fallback_user_approved": false
  },
  "narrative_token": "赵括熟读兵书",
  "appearance_reason": "赵括是文案首先提到的主体，因此第一个进入",
  "appearance_order": 1,
  "z_index": 22,
  "content_kind": "portrait-subject",
  "frame_occupancy": {
    "width_pct": 40,
    "height_pct": 62,
    "anchor_x_pct": 58,
    "anchor_y_pct": 56,
    "sizing_mode": "height-driven"
  },
  "motion": {
    "entrance": "spring-rise",
    "direction": "bottom",
    "start_pct": 10,
    "end_pct": 32,
    "travel_pct": 11,
    "settle": "small-overshoot",
    "hold": "vertical-drift-0.8pct",
    "exit": "hold-to-cut"
  },
  "action_motion": {
    "type": "advance",
    "start_pct": 34,
    "end_pct": 58,
    "translate_x_pct": 12,
    "translate_y_pct": 0,
    "scale_to": 1.04,
    "rotate_deg": 0,
    "easing": "ease-in-out"
  }
}
```

An approved manifest is invalid if these fields are omitted, left as placeholders, or contradict the narration order.

## 6. Acceptance

Reject the scene when any of these is true:

- a background path is reused without explicit shared-continuity authorization
- a background file was copied or renamed across scenes, or two scenes reuse the same normalized `background_concept`
- fewer than 4 or more than 8 raster assets are approved
- fewer than 3 non-background assets have independent motion specifications
- `visual_metaphor`, `composition`, or `motion_rhythm` is missing or generic
- metaphor asset IDs do not resolve to approved moving assets
- the dominant motion does not perform the stated metaphor payoff
- the layout is a repeated center/left/right/lower-band poster rather than the chosen archetype
- a non-background raster is not alpha-tight or its projected visible subject is below the content-kind minimum
- `content_kind` and `sizing_mode` disagree, such as a wide army using portrait sizing
- all scene assets came from one cross-scene composite sheet
- a narrated action is represented only by entrance motion or passive hold drift
- appearance orders are duplicated, missing, or inconsistent with `narrative_sequence`
- an accent appears before its target
- all assets enter together
- the scene spends less than 25% of its duration in the final readable hold

Reject the sequence when adjacent Scenes share a layout archetype, when a 4+ Scene sequence has fewer than 3 layout archetypes or motion rhythms, when `lower-band` exceeds one third of the Scenes, or when two Scenes share the same derived composition signature.
