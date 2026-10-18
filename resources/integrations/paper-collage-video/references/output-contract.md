# Output Contract

## Purpose

Use this file as the hard contract for `paper-collage-video`.

The other references explain style, prompts, and workflow.
This file defines:

- what inputs are minimally required
- what defaults apply when inputs are missing
- what outputs must exist
- what each output must contain
- how to decide `remotion` vs `seedance`
- how to accept or reject the result

If another reference is more poetic and this file is more rigid, follow this file.

## 1. Input contract

The skill may start from any of these:

- a story
- a narration draft
- a scene request
- a reference clip plus a remake request

Before formal planning, normalize the input into this structure:

```yaml
input_intake:
  source_type: story | narration | brief | reference-remake
  production_mode: remotion-code | video-model
  style_family: vox-mixed-media
  selection_source: user-selection | user-authorized-defaults
  content_shape: single-scene | vo-sequence
  scene_statement: one-sentence description of the video or scene
  reference_present: true | false
  aspect_ratio: 16:9 | 9:16
  orientation: horizontal | vertical
  audio_mode: use-source-audio | generate-voiceover | no-audio
  total_duration_rule: follow-source-audio | follow-generated-voiceover | user-specified | estimated-from-content
  total_duration_seconds: number
  voiceover_provider: edge-tts-online | none
  voiceover_voice: zh-CN-YunjianNeural | none
  source_audio_file: path | none
  subtitle_file: path | none
  srt_scene_plan_file: path | none
  scene_duration_policy: not-applicable | auto-by-content
  video_model: doubao-seedance-1-5-pro-251215
  image_path: imagegen
```

## 2. Missing-field interaction rule

If the user starts the skill without specifying `production_mode` or `aspect_ratio`, do not silently continue. `style_family` is not a user choice and is always locked to `vox-mixed-media`. Runtime handling and per-Scene duration are automatic decisions, not Gate 1 user choices.

Treat this as `Gate 1`.
If a user-facing field in `Gate 1` is incomplete, planning must stop. Automatically derived duration fields never require a user response.

Ask the user to choose only these user-facing fields first, while deriving duration fields automatically:

- `production_mode`: `remotion-code` or `video-model`
- `style_family`: automatically lock `vox-mixed-media`; do not ask
- `aspect_ratio`: `16:9 / 9:16`
- automatically lock total-duration handling:
  if source audio exists, lock the whole-video runtime to that audio duration
  if generated voiceover is selected, skip the duration question and lock runtime after TTS succeeds
  if the user supplied a whole-video runtime, lock it as `user-specified`
  otherwise lock `estimated-from-content`
- automatically lock scene-duration policy:
  `production_mode=video-model` -> `auto-by-content`
  `production_mode=remotion-code` -> `not-applicable`
- `audio_mode`:
  if source audio exists, use it
  if no source audio exists, ask `generate Mandarin male voiceover / no audio`

Preferred interaction order:

1. Use Tool Call / Function Calling popup selection when the host supports it.
2. Fall back to a short text choice list when popup UI is unavailable.
3. Use defaults only if the user explicitly says to decide for them. Popup unavailability requires a text question and a wait; it is not default authorization.

If function-calling popup support exists, follow `popup-tool-contract.md` and request the choice through `show_select_popup` rather than a natural-language options list.

## 2A. Gate 0: environment and capability check

Before any planning or generation begins, run:

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/preflight.py
```

Pass only if the required capabilities for the chosen route are available.

Minimum checks:

- skill-local env file presence
- non-empty `ARK_API_KEY` in the skill-local `.env` specifically
- `imagegen` skill availability
- Remotion skill/plugin availability
- local Node and npm availability
- popup tool support state is known from the current tool inventory

If `Gate 0` fails:

- stop the workflow
- report which capability is missing
- do not advance to user-choice collection or asset work
- do not create a partial scaffold containing a failed self-check report

## 3. Default decisions

If the user authorizes defaults, lock these values:

```yaml
defaults:
  production_mode: remotion-code
  style_family: vox-mixed-media
  content_shape:
    single visual request: single-scene
    narration-led or multi-part request: vo-sequence
  aspect_ratio: 16:9
  orientation:
    16:9: horizontal
    9:16: vertical
  audio_mode:
    with source audio: use-source-audio
    without source audio: no-audio only after explicit default delegation
  total_duration_rule:
    with source audio: follow-source-audio
    with generated voiceover: follow-generated-voiceover
    without source audio: estimated-from-content
  scene_duration_policy:
    video-model: auto-by-content
    remotion-code: not-applicable
  video_model: doubao-seedance-1-5-pro-251215
  image_path: imagegen
  route_default: remotion-cutout
```

## 4. Route decision matrix

Do not route by vague instinct. Use this matrix.

### Choose `remotion-cutout` when all of these are true

- visible storytelling elements are `5 or fewer`
- independently timed motions are `2 or fewer`
- the scene can be separated into stable background, midground, and foreground planes
- the scene benefits from editable labels, counters, chart parts, or alpha layers

### Choose `seedance-first-last` when any `2 or more` of these are true

- visible storytelling elements are `6 or more`
- independently timed motions are `3 or more`
- the meaning depends on whole-frame simultaneous assembly
- the scene should resolve into one integrated poster-like tableau
- splitting the scene into editable cutout layers would likely break the look

### Mandatory Seedance triggers

If either of these is true, route to `seedance-first-last` even without scoring the rest:

- the brief explicitly asks for one dense collage scene where many pieces animate together
- the intended final image is a held Vox editorial poster or evidence-board tableau

## 5. Required outputs by mode

### `single-scene`

Must produce:

- `input intake summary`
- `style thesis`
- `beat list`
- `storyboard`
- `route decision`
- `motion_intent`
- if route is `seedance-first-last`, one `SEEDANCE_SCENE.json`
- if production mode is `video-model`, exactly two generated stills and no `ASSETS.json`, cutout pack, Composition Blueprint, contact sheet, or `07_remotion`

### `vo-sequence`

Must produce:

- `input intake summary`
- `style thesis`
- `narration timeline`
- `beat list`
- `scene list`
- `storyboard`
- one route decision per scene
- one `motion_intent` per Seedance scene
- one `SEEDANCE_SCENE.json` per Seedance scene
- for `video-model`, exactly two generated stills per Scene and no Remotion asset manifests or cutout packs

### Additional requirement for `generate-voiceover`

Must produce before beat or Scene planning:

- `04_audio/voiceover.mp3`
- `04_audio/voiceover.srt`
- `04_audio/voiceover-metadata.json`
- final narration text used for synthesis
- `01_storyboard/srt-scene-plan.json` for `vo-sequence`

The metadata must record `provider=edge-tts-online`, `voice=zh-CN-YunjianNeural`, and the measured MP3 duration. Every generated-voiceover beat must carry `timing_source=srt`.

The SRT scene plan must use this schema:

```yaml
timeline_source: srt
scenes:
  - scene_slug:
    cue_start: 1
    cue_end: 4
    scene_goal:
```

Cue ranges must be contiguous, ordered, non-overlapping, and cover every SRT cue exactly once.

### Additional requirement for `remotion-code`

Before any full scene rendering attempt, each Remotion scene must also produce an asset decomposition plan.

Minimum per-scene slots:

```yaml
scene_asset_pack:
  manifest_version: 2
  background_concept:
  background_distinction_reason:
  visual_metaphor:
    abstract_claim:
    concrete_metaphor:
    mapping:
    motion_payoff:
    asset_ids: []
  composition:
    layout_archetype:
    reading_path:
    dominant_axis:
    foreground_strategy:
    negative_space_intent:
  motion_rhythm:
  composition_blueprint_locked: false
  color_script:
    style_reference: 0720-bright-paper
    dominant_field:
    support_colors: []
    focal_accent:
    dark_anchor:
    paper_neutral:
    area_budget:
      dominant_pct:
      support_pct:
      neutral_pct:
      accent_pct:
      archival_brown_gray_pct:
    hero_background_contrast:
    adjacent_scene_shift:
    prompt_palette_sentence:
    negative_palette_terms: []
    user_palette_override: false
    override_reason:
    review:
      three_chromatic_hues_present: false
      hero_separates_at_thumbnail: false
      no_muddy_global_cast: false
      palette_match_across_assets: false
  background_contract:
    role: stage-only
    allowed_elements: []
    forbidden_subjects: []
    max_saliency: very-low | low
    semantic_overlap_forbidden: true
    reserved_zones: []
    review:
      reserved_zones_clear: false
      no_duplicate_subjects: false
      focal_competition: fail | pass
  collision_plan:
    default_max_overlap_pct: 8
    safe_gap_pct: 3
    motion_paths_reviewed: false
    allowed_overlaps: []
  content_order_locked: false
  composition_locked: false
  motion_plan_locked: false
  background_plate:
  hero_cutout:
  content_specific_moving_assets: []
  optional_environment_editorial_foreground_and_accents: []
  narrative_sequence: []
```

Rules:

- current validators accept `manifest_version: 2`; a missing or older version receives one migration instruction instead of downstream schema noise
- `background_plate` must contain only fixed environment and broad shape language
- `background_plate` must not contain extra sticker scraps, surprise labels, decorative arrows, or unplanned extra characters
- `hero_cutout` and support cutouts must not be baked into the background plate
- if a chart, map, bubble, quote card, or metric card matters to understanding the shot, it must be listed as its own asset
- a Remotion scene is not acceptable if its plan collapses back into one flattened `scene-xx.png`
- default `background_policy` is `per-scene`; background paths must be unique across scenes
- only permit background reuse when `background_policy=shared-continuity` and `background_sharing_authorized=true`
- require 4-8 approved raster assets per scene, including the background
- require at least 3 approved independently timed non-background assets
- require a concrete visual metaphor, composition archetype, reading path, foreground strategy, and motion rhythm before asset generation
- require a locked `0720-bright-paper` color script before asset generation; default scenes need one chromatic dominant, two chromatic supports, one focal accent, one dark anchor, and a controlled paper neutral
- reject default scenes whose neutral area exceeds 25%, whose brown/gray/tan area exceeds 20%, or whose prompts omit the approved palette sentence and negative palette terms
- reject Scenes where the hero and its landing zone do not have explicit hue and lightness separation at thumbnail size
- require a background-stage contract and collision plan before generating either background or moving assets
- reject backgrounds that duplicate moving-subject classes or place high-saliency detail inside reserved landing zones
- reject unapproved pairwise overlaps above the configured limit, even when z-index makes the overlap technically renderable
- do not require a foreground strip; reject repeated center/left/right/lower-band layouts
- do not generate one cross-scene composite sheet or merge elements that need separate motion
- leave all three lock fields false until content order, composition occupancy, and per-element motion have each been reviewed; an approved scene requires all three to be true

For `vox-mixed-media`, every approved moving asset must also include:

```yaml
asset_motion:
  narrative_token:
  appearance_reason:
  appearance_order:
  z_index: 0-60
  content_kind: portrait-subject | wide-group | object-prop | editorial-card | foreground-strip | accent-mark
  frame_occupancy:
    width_pct:
    height_pct:
    anchor_x_pct:
    anchor_y_pct:
    sizing_mode: height-driven | width-driven | box-contain
  motion:
    entrance:
    direction:
    start_pct:
    end_pct:
    travel_pct:
    settle:
    hold:
    exit:
  action_motion:
    type: none | retreat | advance | chase | converge | diverge | replace | reveal | emphasize | stamp | sweep | path-follow | draw | highlight | wipe | pulse | orbit | stack | split | collapse | rise | fall | tip | pull
    start_pct:
    end_pct:
    translate_x_pct:
    translate_y_pct:
    scale_to:
    rotate_deg:
    easing: linear | ease-in | ease-out | ease-in-out | spring
    path_points_pct: [] # required for path-follow
    reveal_direction: left-to-right | right-to-left | top-to-bottom | bottom-to-top
    pulse_scale:
```

Every Remotion Scene manifest must additionally include:

```yaml
visual_metaphor:
  abstract_claim:
  concrete_metaphor:
  mapping:
  motion_payoff:
  asset_ids: []
composition:
  layout_archetype: asymmetric-stage | diagonal-cascade | split-contrast | radial-cycle | depth-tunnel | stacked-consequence | map-route | full-frame-data
  reading_path: left-to-right | right-to-left | top-to-bottom | bottom-to-top | diagonal-down | diagonal-up | radial-in | radial-out | serpentine | center-out
  dominant_axis: horizontal | vertical | diagonal | radial | depth
  foreground_strategy: none | corner-occluder | side-frame | lower-band | full-depth-prop | entering-subject
  negative_space_intent:
motion_rhythm: sequential-build | cause-then-effect | counter-motion | radial-convergence | path-follow | scale-shift | replacement | cascade | draw-and-land
```

Every generated visible asset must additionally include the provenance schema from `asset-provenance-contract.md`. `source=imagegen` is invalid without an actual tool call, preserved original output, concrete prompt and receipt, and matching SHA-256 values.

Use the size and timing ranges in `vox-motion-contract.md`. `appearance_order` must be unique, contiguous from `1`, and match `narrative_sequence` exactly.

## 6. Required field schemas

### `style thesis`

One paragraph only. It must contain:

- material language
- palette direction
- motion character
- editorial structure

### `beat list`

Each beat must follow this schema:

```yaml
- beat_slug:
  start_seconds:
  end_seconds:
  duration_seconds:
  narration:
  visual_goal:
  primary_subject:
  support_subjects:
  route_hint: remotion | seedance
```

Rules:

- one beat = one visual idea
- beat windows must be contiguous
- duration must be positive

### `scene list`

Each scene must follow this schema:

```yaml
- scene_slug:
  beat_slugs:
  start_seconds:
  end_seconds:
  duration_seconds:
  request_duration_seconds: null | integer
  duration_reason:
  route: remotion-cutout | seedance-first-last
  module_type:
  visual_metaphor:
  layout_archetype:
  reading_path:
  motion_rhythm:
  scene_goal:
```

Rules:

- every beat belongs to exactly one scene
- no scene overlaps another
- scenes cover the intended runtime
- `duration_seconds` is the Scene's content window on the whole-video timeline
- Seedance scenes additionally declare an integer `request_duration_seconds` from `4-12`; Remotion scenes use `null`
- no Seedance Scene may hide an oversized content window by clamping it to 12 seconds

### `storyboard`

Each panel must contain:

```yaml
- panel_id:
  time_window:
  what_enters:
  what_changes:
  focal_subject:
  text_or_label:
  sound_sync:
  route:
  required_assets:
```

### `motion_intent`

Each `motion_intent` must explicitly answer:

- camera rule
- start state
- assembly order
- anchored element
- hold behavior

Recommended structure:

```yaml
motion_intent:
  camera:
  start_state:
  assembly_order:
  anchored_element:
  micro_motion_on_hold:
```

### `SEEDANCE_SCENE.json`

A valid Seedance scene spec must include:

```yaml
scene_slug:
scene_index:
scene_title:
route: seedance-first-last
video_model: doubao-seedance-1-5-pro-251215
prompt:
motion_intent:
motion_contract:
  frame_state_audit_locked: false
  prompt_contract_consistency_locked: false
  fixed_objects:
    - id:
      description:
      prompt_aliases: []
      rule: pixel-locked | anchored-micro-motion
  entering_objects:
    - id:
      description:
      motion_primitive: slide-in | rise | stamp-in | page-place | pin-drop | serial-placement | direct-placement | unfold | wipe-reveal | tape-press
      final_region:
  draw_on_paths:
    - id:
      surface_id:
      path_description:
      direction:
      draw_mode: progressive-tip-growth | segment-by-segment-reveal
      marker_rule:
  timeline:
    - start_pct:
      end_pct:
      behavior: slide-in | rise | stamp-in | page-place | pin-drop | serial-placement | direct-placement | unfold | wipe-reveal | tape-press | draw-path | hold
      object_ids: []
      instruction:
  forbidden_events: []
keyframe_generation_contract:
  canvas:
    source: gate-1
    aspect_ratio: 16:9 | 9:16
    width: 1536 | 864
    height: 864 | 1536
    orientation: horizontal | vertical
    validate_before_last_frame: true
    post_edit_crop_forbidden: true
  max_outside_region_mae: 0.06
  max_outside_significant_change_pct: 12
  first_frame:
    source: imagegen
    mode: generate
    execution_method: built-in-image_gen-generate
    tool_called: false
    prompt_file:
    result_receipt:
    output_sha256:
  last_frame:
    source: imagegen
    mode: edit
    execution_method: built-in-image_gen-edit
    tool_called: false
    prompt_file:
    result_receipt:
    output_sha256:
    edit_target_role: first_frame
    edit_target_path:
    edit_target_sha256:
    referenced_image_paths: []
    preserve_outside_change_regions: true
    change_regions:
      - id:
        x_pct:
        y_pct:
        width_pct:
        height_pct:
        purpose:
  continuity_review:
    same_canvas_and_crop: false
    background_geometry_match: false
    fixed_objects_match: false
    no_background_regeneration: false
resolution:
  aspect_ratio:
  width:
  height:
  resolution_tier:
timing:
  content_window_seconds:
  duration_seconds:
  request_duration_seconds:
  scene_duration_policy: auto-by-content
  duration_reason:
  frame_rate:
seedance:
  generate_audio:
  return_last_frame:
  watermark:
  input_mode: first-last-frame
  base64_transport: true
frames:
  - id: first-frame
    role: first_frame
    path:
  - id: last-frame
    role: last_frame
    path:
output:
  video_path:
  metadata_path:
```

## 7. Acceptance rules

### Intake acceptance

Pass only if:

- `scene_statement` exists
- `production_mode` is chosen
- `content_shape` is chosen or inferred
- `total_duration_rule` is automatically locked from audio, an explicit brief value, or content estimation
- `total_duration_seconds` is positive and represents the whole video, not one generated scene
- `scene_duration_policy` is automatically `auto-by-content` for `video-model`, or `not-applicable` for `remotion-code`
- if `audio_mode=generate-voiceover`, MP3, SRT, and voiceover metadata exist before beat planning
- generated voiceover uses `edge-tts-online` and `zh-CN-YunjianNeural`
- generated voiceover duration comes from the measured audio metadata
- `aspect_ratio` and `audio_mode` are known or defaulted
- if the user did not supply those fields, a choice step happened first unless the user explicitly delegated defaults
- the choice origin is recorded as `user-selection` or `user-authorized-defaults`

### Beat acceptance

Pass only if:

- every beat has all required fields
- every beat has exactly one `visual_goal`
- the full beat list covers the runtime
- no beat overlaps another
- generated-voiceover beats use SRT cue windows rather than evenly divided text timing
- Scene boundaries may merge adjacent SRT cues but may not invent timing outside their combined cue window

### Scene acceptance

Pass only if:

- every scene has all required fields
- every scene owns at least one beat
- route is explicit for every scene
- route choice is defensible under the matrix
- each scene has a distinct background concept and path unless explicit continuity reuse was authorized
- each Remotion scene has 4-8 approved assets and at least 3 independent moving assets
- each Remotion scene has a concrete metaphor mapping, layout archetype, reading path, foreground strategy, and motion rhythm
- adjacent Scenes do not repeat a layout archetype or composition signature; a 4+ Scene sequence uses at least 3 layouts and 3 rhythms
- every approved Remotion scene has all three content/composition/motion locks set to true
- every moving element has a valid subject size, anchor, entrance window, hold behavior, and appearance order
- `narrative_sequence` follows the source content order and matches the motion order

### Seedance acceptance

Pass only if:

- there are exactly 2 frame entries
- the keyframe canvas contract comes from Gate 1 rather than a hardcoded prompt value
- `16:9` uses the scaffold canvas `1536x864`; `9:16` uses `864x1536`
- both frame files exist
- the first-frame canvas gate passes before the last-frame image call
- both frame files use the same Gate 1 aspect ratio and exact canonical canvas
- `motion_contract` declares all fixed, entering, and draw-on identities referenced by its serial timeline
- both motion-contract audit locks are true after visual first/last comparison and prose consistency review
- first-frame persistent surfaces never receive entrance or replacement behavior
- `last-frame.png` is produced by an actual imagegen edit of the exact first-frame bytes, not by independent generation
- edit provenance, first-frame SHA-256, sole `referenced_image_paths` input, change regions, and post-edit hashes all validate
- neither frame is cropped or resized after the last-frame edit
- change regions cover no more than 65% of the canvas and protected background differences stay under the configured thresholds
- each draw-on path targets a declared fixed surface
- a 5-second scene has at most 4 non-hold action groups; a longer scene has at most 7
- the final timeline entry is a hold beginning no later than 75% and ending at 100%
- `request_duration_seconds` is an integer `4-12`
- `request_duration_seconds` belongs to one Scene and is never treated as the whole-video duration
- under `auto-by-content`, the request duration is derived from that Scene's narration/content window and motion budget
- a Scene whose content needs more than 12 seconds has been split rather than clamped or truncated
- no placeholder markers such as `[fill ...]` remain
- `prompt` describes the final tableau
- `motion_intent` covers camera, start state, order, anchor, and hold

### Final package acceptance

Pass only if:

- required outputs for the selected mode all exist
- no unresolved placeholders remain anywhere in the package
- route choices are recorded
- review status is explicitly `approved` or `revise`
- `python3 tools/validate_collage_project.py --project .` exits successfully
- no SVG file, inline SVG, SVG data URI, or unapproved/missing required raster asset exists

## 8. Quick validation commands

These are practical checks, not the only possible checks.

### Placeholder scan

```bash
rg -n "\\[fill|TODO|TBD" [project-root]
```

Expected result:

- no matches in approved output

### Seedance scene existence scan

```bash
find [project-root] -name 'SEEDANCE_SCENE.json'
```

Expected result:

- one file for each approved Seedance scene

### Render artifact expectation

For each approved Seedance scene, expect:

- one `first-frame.png`
- one `last-frame.png`
- one output `.json`
- one output `.mp4` after successful submission
