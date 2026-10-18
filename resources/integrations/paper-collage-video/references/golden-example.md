# Golden Example

## Purpose

This is the canonical end-to-end example for `paper-collage-video`.

Use it when you need to answer:

- what a good normalized input looks like
- what a stable beat list looks like
- what qualifies for `seedance-first-last`
- what a finished `SEEDANCE_SCENE.json` should contain
- what “ready for approval” looks like

## 1. Raw user request

```text
我想做一个 35 秒左右的拼贴解说视频，讲 1971 年一个男子劫持飞机后跳伞失踪，最后一直没找到。风格偏档案、调查、地图、证据墙，旁白是平静纪录片口吻，横版。我已经提供了内容音频，你按这个音频时长来做。
```

## 2. Normalized intake

```yaml
input_intake:
  source_type: story
  production_mode: remotion-code
  style_family: vox-mixed-media
  content_shape: vo-sequence
  scene_statement: a Vox mixed-media explainer about a 1971 hijacker who vanished after a ransom jump
  reference_present: false
  aspect_ratio: 16:9
  orientation: horizontal
  audio_mode: use-source-audio
  total_duration_rule: follow-source-audio
  total_duration_seconds: 35
  scene_duration_policy: not-applicable
  video_model: doubao-seedance-1-5-pro-251215
  image_path: imagegen
```

## 3. Style thesis

```text
This video should feel like a calm but chromatic Vox mixed-media investigation built from rough fibrous white-bordered cutouts, broad sky-blue and deep-navy map fields, leaf-green supports, controlled marigold and coral focal accents, crisp halftone grain, marker routes, and short labels. Each scene changes its dominant color balance while keeping one bright tactile paper world; dense moments resolve as locked-camera tableaux that assemble and then hold.
```

## 4. Beat list

```yaml
- beat_slug: cold-open-date
  start_seconds: 0.0
  end_seconds: 3.0
  duration_seconds: 3.0
  narration: On November 24, 1971, a man boarded a Northwest Orient flight with a black briefcase.
  visual_goal: establish date, airline context, and the man's controlled arrival
  primary_subject: halftone cutout passenger at ticket or boarding context
  support_subjects:
    - date strip
    - airline tag
  route_hint: remotion

- beat_slug: ransom-demand
  start_seconds: 3.0
  end_seconds: 8.0
  duration_seconds: 5.0
  narration: By the time the plane landed in Seattle, he had demanded $200,000 and four parachutes.
  visual_goal: turn the demand into visible physical evidence
  primary_subject: typed ransom note pinned over cash
  support_subjects:
    - parachute card
    - airline paperwork
  route_hint: seedance

- beat_slug: night-jump
  start_seconds: 8.0
  end_seconds: 15.0
  duration_seconds: 7.0
  narration: That night, somewhere over the Pacific Northwest, he jumped into the dark and disappeared.
  visual_goal: show a jump into map-like darkness without losing editorial clarity
  primary_subject: aircraft door and falling silhouette
  support_subjects:
    - regional map
    - night paper clouds
  route_hint: remotion

- beat_slug: search-grid
  start_seconds: 15.0
  end_seconds: 24.0
  duration_seconds: 9.0
  narration: Search crews found scraps, rumors, and one small trail of cash.
  visual_goal: show an expanding search system with partial evidence
  primary_subject: search map with marked zones
  support_subjects:
    - cash fragments
    - evidence labels
    - line connectors
  route_hint: remotion

- beat_slug: missing-parachute
  start_seconds: 24.0
  end_seconds: 35.0
  duration_seconds: 11.0
  narration: They never found the parachute that should have told the whole story.
  visual_goal: end on one dense unresolved evidence tableau
  primary_subject: evidence board centered on the missing parachute clue
  support_subjects:
    - ransom note
    - regional map
    - red string network
  route_hint: seedance
```

## 5. Scene list

```yaml
- scene_slug: boarding-cold-open
  beat_slugs:
    - cold-open-date
  start_seconds: 0.0
  end_seconds: 3.0
  duration_seconds: 3.0
  route: remotion-cutout
  module_type: cutout-rise
  visual_metaphor: the passenger is swallowed by an oversized aircraft doorway
  layout_archetype: asymmetric-stage
  reading_path: left-to-right
  motion_rhythm: sequential-build
  scene_goal: establish the documentary setting and controlled entry

- scene_slug: ransom-evidence
  beat_slugs:
    - ransom-demand
  start_seconds: 3.0
  end_seconds: 8.0
  duration_seconds: 5.0
  route: seedance-first-last
  module_type: evidence-board
  visual_metaphor: a ransom note tears the calm timeline into two unequal halves
  layout_archetype: split-contrast
  reading_path: top-to-bottom
  motion_rhythm: cause-then-effect
  scene_goal: make the demand feel tangible as evidence

- scene_slug: jump-and-search
  beat_slugs:
    - night-jump
    - search-grid
  start_seconds: 8.0
  end_seconds: 24.0
  duration_seconds: 16.0
  route: remotion-cutout
  module_type: map-tracking
  visual_metaphor: a route draws across the map while the silhouette vanishes off that route
  layout_archetype: map-route
  reading_path: serpentine
  motion_rhythm: path-follow
  scene_goal: move from disappearance into structured search

- scene_slug: unanswered-clue
  beat_slugs:
    - missing-parachute
  start_seconds: 24.0
  end_seconds: 35.0
  duration_seconds: 11.0
  route: seedance-first-last
  module_type: final-evidence-wall
  visual_metaphor: evidence circles an empty center where the missing parachute should be
  layout_archetype: radial-cycle
  reading_path: radial-in
  motion_rhythm: radial-convergence
  scene_goal: resolve into a final unresolved poster tableau
```

## 5A. Color script example

Every Scene still needs its own manifest-level `color_script`. This is one valid
default entry; adjacent Scenes must change the dominant/accent pair or color-area
balance.

```yaml
color_script:
  style_reference: 0720-bright-paper
  dominant_field: sky blue fibrous paper
  support_colors:
    - deep ocean blue
    - leaf green
  focal_accent: marigold orange
  dark_anchor: deep navy
  paper_neutral: fibrous cream white
  area_budget:
    dominant_pct: 45
    support_pct: 28
    neutral_pct: 18
    accent_pct: 9
    archival_brown_gray_pct: 8
  hero_background_contrast: the warm marigold evidence cluster lands on a cool sky-blue reserve and is outlined by a fibrous cream edge, while deep navy supplies the darkest local value
  adjacent_scene_shift: the following Scene changes the dominant field to leaf green and moves sky blue into a supporting role
  prompt_palette_sentence: sky blue fibrous paper is the dominant field, deep ocean blue and leaf green are support colors, marigold orange is the focal accent, and deep navy is the dark anchor
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
    three_chromatic_hues_present: true
    hero_separates_at_thumbnail: true
    no_muddy_global_cast: true
    palette_match_across_assets: true
```

## 6. Route justification

```yaml
route_decision:
  ransom-evidence:
    visible_elements: 6
    independent_motions: 3
    integrated_tableau: true
    split_layers_would_break_look: true
    final_route: seedance-first-last
  unanswered-clue:
    visible_elements: 7
    independent_motions: 4
    integrated_tableau: true
    final_route: seedance-first-last
```

## 7. Storyboard panel example for one Seedance scene

```yaml
- panel_id: unanswered-clue-panel
  time_window: 24.0s-35.0s
  what_enters: note, map clue card, parachute evidence card, red string, brass pins
  what_changes: empty board becomes a fully assembled unresolved evidence wall
  focal_subject: missing parachute clue near center-right
  text_or_label: short date or evidence tag only
  sound_sync: pin click on final settle
  route: seedance
```

## 8. Motion intent example

```yaml
motion_intent:
  camera: locked
  start_state: quiet corkboard plate with archival map scraps and date strip already fixed
  assembly_order:
    - ransom note lands near center
    - map clue card slides in
    - parachute evidence card settles on the right
    - red string draws across the board
    - brass pins and one stamp accent settle last
  anchored_element: corkboard base and date strip
  micro_motion_on_hold:
    - slight paper-corner lift
    - soft shadow breathing
    - one tiny red-string quiver
```

## 9. Seedance image prompts

### `first-frame.png`

```text
Create a full-frame Vox-style editorial mixed-media collage still for a Seedance first+last scene.

Scene goal:
an unresolved documentary evidence board about a missing parachute clue

This specific still moment:
first-frame empty plate

Hero subject:
none yet; keep the center-right area open for the future clue assembly

Supporting subjects:
- corkboard background with archival map scraps already pinned down
- a small typewriter date strip
- two empty masking-tape corners

Background and surface logic:
a broad sky-blue fibrous paper field with one deep-navy map band; a limited warm-cork structural strip and sparse archival scraps remain below 20% of the frame

Composition rule:
preserve a readable central reserve and strong negative space for incoming evidence pieces

Style:
Vox-style editorial mixed-media collage, bright tactile paper, rough fibrous white-bordered cutouts, broad chromatic fields, crisp halftone and paper grain, matte lighting, soft layered shadows, non-photorealistic, no live-action

Palette lock:
sky blue fibrous paper is the dominant field, deep ocean blue and leaf green are support colors, marigold orange is the focal accent, and deep navy is the dark anchor

Negative palette:
no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look
```

### `last-frame.png`

```text
Edit the exact approved local first-frame image. Use it as the immutable edit target and sole `referenced_image_paths` input.

Scene goal:
resolve into a final unanswered-clue evidence tableau

This specific still moment:
last-frame final hold

Hero subject:
a parachute evidence card and ransom note forming the main unresolved clue cluster

Supporting subjects:
- regional map with a red string route
- one cash fragment evidence strip
- two brass pins and a red stamp accent

Change only:
- center evidence zone: add the ransom note and parachute evidence card
- lower-left evidence zone: add the cash fragment
- declared map-path zone: add the red string and pins

Background and surface logic:
preserve the exact first-frame canvas, crop, corkboard, map contours, date strip, paper tears, texture, grain, color, and lighting outside those change regions

Composition rule:
the clue cluster must dominate while the surrounding evidence remains readable and uncluttered

Style:
Vox-style editorial mixed-media collage, bright tactile halftone cutouts with rough fibrous white borders, broad chromatic color fields, restrained coral route lines and short labels, visible crisp paper grain, matte lighting, soft layered shadows, non-photorealistic, no live-action

Palette lock:
sky blue fibrous paper is the dominant field, deep ocean blue and leaf green are support colors, marigold orange is the focal accent, and deep navy is the dark anchor

Negative palette:
no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look

Hard invariant:
do not repaint, regenerate, restyle, recrop, move, extend, or simplify the background. Output the same first-frame canvas with only the approved additions.
```

## 10. Video prompt example

```text
Transform the provided first-frame and last-frame images into a premium Vox-style editorial mixed-media animation.

Preserve the final composition of the provided last frame exactly. The first frame is the quiet background plate. The last frame is the completed unresolved evidence tableau.

Style:
Vox-style editorial mixed-media collage in motion, flat map fields, halftone cutouts with rough white borders, restrained marker route lines and pins, rigid paper-piece motion, soft layered shadows, snappy editorial cadence, non-photorealistic, no live-action

Camera:
locked camera, no pan, no zoom, no tilt, no cuts, no morphing, no object replacement

Timing structure:
0-70 percent assemble the board from back to front
70-100 percent hold as a living poster

Assembly behavior:
the ransom note lands first, then the map clue card, then the parachute evidence card, then the red string draws across the board, then the brass pins settle and lock the final composition

Hold behavior:
all major objects stay fixed, with only slight paper-corner lift, soft shadow breathing, and one tiny string quiver

Audio:
no narration baked in, only subtle paper slide, pin click, tape press, and room tone
```

## 11. Example `SEEDANCE_SCENE.json`

```json
{
  "scene_slug": "unanswered-clue",
  "scene_index": 4,
  "scene_title": "Unanswered Clue",
  "route": "seedance-first-last",
  "video_model": "doubao-seedance-1-5-pro-251215",
  "prompt": "Transform the provided first-frame and last-frame images into a premium Vox-style editorial mixed-media animation. Preserve the final composition of the provided last frame exactly. The first frame is the quiet background plate. The last frame is the completed unresolved evidence tableau.",
  "motion_intent": "The camera remains locked. The scene begins on a quiet corkboard plate with archival map scraps and a date strip already fixed. The ransom note lands first, then the map clue card, then the parachute evidence card on the right. The red string is drawn across the board after that, and the brass pins settle last. The corkboard base and date strip stay anchored throughout. By the final third of the shot, the board is fully assembled and holds as a living poster with only slight paper-corner lift, soft shadow breathing, and one tiny string quiver.",
  "motion_contract": {
    "frame_state_audit_locked": true,
    "prompt_contract_consistency_locked": true,
    "fixed_objects": [
      {
        "id": "board_surface",
        "description": "the corkboard plate, archival map scraps, and date strip visible in both endpoint frames",
        "prompt_aliases": ["corkboard plate", "map scraps", "date strip"],
        "rule": "pixel-locked"
      }
    ],
    "entering_objects": [
      {
        "id": "ransom_note",
        "description": "one rigid ransom-note cutout",
        "motion_primitive": "page-place",
        "final_region": "center evidence zone"
      },
      {
        "id": "clue_cards",
        "description": "the exact two rigid clue cards from the last frame",
        "motion_primitive": "serial-placement",
        "final_region": "their separate final evidence zones"
      },
      {
        "id": "pins",
        "description": "the exact final brass pins",
        "motion_primitive": "pin-drop",
        "final_region": "their final string anchor points"
      }
    ],
    "draw_on_paths": [
      {
        "id": "evidence_string",
        "surface_id": "board_surface",
        "path_description": "the exact final red connection path across the board",
        "direction": "from the first final pin position to the last",
        "draw_mode": "segment-by-segment-reveal",
        "marker_rule": "no extra markers; pins arrive in their later timeline group"
      }
    ],
    "timeline": [
      {
        "start_pct": 0,
        "end_pct": 15,
        "behavior": "page-place",
        "object_ids": ["ransom_note"],
        "instruction": "place the note directly into its final center position"
      },
      {
        "start_pct": 15,
        "end_pct": 38,
        "behavior": "serial-placement",
        "object_ids": ["clue_cards"],
        "instruction": "place the two clue cards serially into their separate final zones"
      },
      {
        "start_pct": 38,
        "end_pct": 55,
        "behavior": "draw-path",
        "object_ids": ["evidence_string"],
        "instruction": "reveal the string only along its final path on the fixed board"
      },
      {
        "start_pct": 55,
        "end_pct": 70,
        "behavior": "pin-drop",
        "object_ids": ["pins"],
        "instruction": "drop each pin directly onto its final string anchor"
      },
      {
        "start_pct": 70,
        "end_pct": 100,
        "behavior": "hold",
        "object_ids": ["board_surface", "ransom_note", "clue_cards", "evidence_string", "pins"],
        "instruction": "hold the completed tableau with paper-edge and shadow micro-motion only"
      }
    ],
    "forbidden_events": [
      "object replacement",
      "object morphing",
      "duplicate surfaces",
      "cross-zone travel",
      "the fixed board or map layout moving, flipping, or being covered by a duplicate",
      "the string leaving the board or transforming into another object"
    ]
  },
  "keyframe_generation_contract": {
    "max_outside_region_mae": 0.06,
    "max_outside_significant_change_pct": 12,
    "first_frame": {
      "source": "imagegen",
      "mode": "generate",
      "execution_method": "built-in-image_gen-generate",
      "tool_called": true,
      "prompt_file": "02_assets/prompts/scene-04/first-frame.md",
      "result_receipt": "actual built-in imagegen result receipt",
      "output_sha256": "actual SHA-256 of first-frame.png"
    },
    "last_frame": {
      "source": "imagegen",
      "mode": "edit",
      "execution_method": "built-in-image_gen-edit",
      "tool_called": true,
      "prompt_file": "02_assets/prompts/scene-04/last-frame.md",
      "result_receipt": "actual built-in imagegen edit result receipt",
      "output_sha256": "actual SHA-256 of last-frame.png",
      "edit_target_role": "first_frame",
      "edit_target_path": "02_assets/keyframes/unanswered-clue/first-frame.png",
      "edit_target_sha256": "the same actual SHA-256 recorded for first_frame.output_sha256",
      "referenced_image_paths": [
        "02_assets/keyframes/unanswered-clue/first-frame.png"
      ],
      "preserve_outside_change_regions": true,
      "change_regions": [
        {
          "id": "center-evidence",
          "x_pct": 55,
          "y_pct": 48,
          "width_pct": 38,
          "height_pct": 48,
          "purpose": "add the ransom note and parachute clue cards"
        },
        {
          "id": "lower-left-cash",
          "x_pct": 25,
          "y_pct": 74,
          "width_pct": 24,
          "height_pct": 24,
          "purpose": "add the cash evidence fragment"
        },
        {
          "id": "map-path",
          "x_pct": 56,
          "y_pct": 50,
          "width_pct": 62,
          "height_pct": 18,
          "purpose": "add the red evidence string and brass pins"
        }
      ]
    },
    "continuity_review": {
      "same_canvas_and_crop": true,
      "background_geometry_match": true,
      "fixed_objects_match": true,
      "no_background_regeneration": true
    }
  },
  "resolution": {
    "aspect_ratio": "16:9",
    "resolution_tier": "720p"
  },
  "timing": {
    "duration_seconds": 11.0,
    "request_duration_seconds": 11,
    "frame_rate": 24
  },
  "seedance": {
    "generate_audio": false,
    "return_last_frame": false,
    "watermark": false,
    "input_mode": "first-last-frame",
    "base64_transport": true
  },
  "frames": [
    {
      "id": "first-frame",
      "role": "first_frame",
      "label": "empty or near-empty establishing plate",
      "path": "02_assets/keyframes/unanswered-clue/first-frame.png"
    },
    {
      "id": "last-frame",
      "role": "last_frame",
      "label": "final assembled tableau hold",
      "path": "02_assets/keyframes/unanswered-clue/last-frame.png"
    }
  ],
  "output": {
    "video_path": "05_render/seedance/unanswered-clue.mp4",
    "metadata_path": "05_render/seedance/unanswered-clue.json"
  }
}
```

## 12. Acceptance snapshot

This example passes because:

- production mode is explicit
- the last frame is an actual imagegen edit of the exact first-frame bytes, with edit provenance and protected-background continuity metrics
- content shape is explicit
- duration rule is explicit
- every beat has time, visual goal, and route
- every scene owns its beats
- both Seedance scenes justify their route
- the complex scene has exactly 2 stills
- the Seedance spec has no placeholder fields

## 13. Expected output tree

```text
[project-root]/
  00_brief/
    self-check.md
  01_storyboard/
    narration-timeline.md
    storyboard.md
  02_assets/
    keyframes/
      unanswered-clue/
        first-frame.png
        last-frame.png
  03_animation/
    seedance-runbook.md
  05_render/
    seedance/
      unanswered-clue.json
      unanswered-clue.mp4
  06_sequence/
    scene-plan.md
    scenes/
      unanswered-clue/
        SCENE.md
        SEEDANCE_SCENE.json
```
