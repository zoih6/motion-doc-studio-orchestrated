# Seedance Motion Contract

## Purpose

Use this contract for every `seedance-first-last` scene. It prevents a video model from compressing several actions by replacing cards, morphing one red line into another, moving objects across semantic zones, or inventing transitional props.

The natural-language `prompt` explains the scene. `motion_contract` is the authoritative object and timing ledger. When the two conflict, revise the prose before submission; the compiled hard contract still overrides ambiguous prose.

Before setting `frame_state_audit_locked=true`, compare the actual first and last images and classify every meaningful object. Before setting `prompt_contract_consistency_locked=true`, remove any prose instruction that tells a fixed object to enter, disappear, flip, or be replaced. The submitter rejects either lock while false or missing.

## Keyframe creation contract

The paired frames are not two independent illustrations. They are two states of
one canvas.

1. Generate `first-frame.png` once with built-in `image_gen` generate mode.
2. Inspect that local file with `view_image`.
3. Call built-in `image_gen` again in edit mode with the exact first-frame path as
   the only `referenced_image_paths` input.
4. In the edit prompt, say `change only` and name every allowed addition region.
   Preserve all pixels, geometry, crop, paper tears, texture, color, and fixed
   objects outside those regions.
5. Save the edited result as `last-frame.png`; never issue an independent
   text-to-image request for the last frame.
6. Record the actual tool receipts, file hashes, edit target, and change regions
   under `keyframe_generation_contract`.
7. Run `validate_seedance_keyframes.py`. Seedance submission is forbidden until
   the protected background passes the continuity thresholds.

Text such as “same background,” “matching plate,” or “keep the layout” does not
prove continuity. Only edit provenance tied to the exact first-frame hash plus
the protected-area comparison satisfies this gate.

## Object classes

### Fixed objects

Anything already visible in the first frame and still present in the last frame must be listed under `fixed_objects`.

- `pixel-locked`: no entrance, exit, flip, replacement, duplicate, scale change, or position change
- `anchored-micro-motion`: same identity and position; only tiny paper-edge or shadow motion

Never tell the model to “place”, “drop in”, “replace”, or “reveal” a fixed object. If a panel, map, board, document, or other surface exists in the first frame, animate only content that is genuinely absent from that frame.

Every fixed object also lists `prompt_aliases`: the exact nouns used for it in `prompt` and `motion_intent`. At least one alias must actually appear in the prose. The submitter scans those sentences and rejects affirmative entrance/change verbs near a fixed alias. Negative constraints such as “never replace the board” remain valid.

### Entering objects

List exact object identities and counts. Group repeated identical objects only when they share one controlled serial behavior, such as “exactly N repeated cutouts placed in storyboard order.” Each group gets one final region and may not cross into another object's region.

Use one supported rigid-paper primitive: `slide-in`, `rise`, `stamp-in`, `page-place`, `pin-drop`, `serial-placement`, `direct-placement`, `unfold`, `wipe-reveal`, or `tape-press`. Do not write open-ended motion such as “moves dynamically” or “animates creatively.”

### Draw-on paths

Lines, curves, arrows, routes, underlines, and strings are paths, not flying objects.

Every draw path must specify:

- one fixed `surface_id`
- the exact path and direction
- `draw_mode=progressive-tip-growth` or `segment-by-segment-reveal`
- marker behavior

For progressive drawing, the stroke grows only at its leading tip. Previously drawn stroke remains visible. The whole finished path must not fade in, swap in, flip over, or arrive on a duplicate surface.

## Timing budget

- 5-second scene: no more than 4 non-hold action groups
- 10-second scene: no more than 7 non-hold action groups
- the timeline is serial and non-overlapping by default
- the final hold starts by 75% and ends at 100%

Repeated identical objects may be one action group when they use one serial rule. A repeated-subject sequence, a surface transition, a path draw, a foreground arrival, and a marker arrival are separate groups and must not be disguised as one vague “assembly” action.

## Required forbidden events

Every scene must explicitly forbid:

- object replacement
- object morphing
- duplicate surfaces
- cross-zone travel

Add scene-specific failures such as “the path leaving its declared surface,” “one accent transforming into another,” or “a duplicate panel covering the original.”

## Generic path-on-surface example

```json
{
  "motion_contract": {
    "frame_state_audit_locked": true,
    "prompt_contract_consistency_locked": true,
    "fixed_objects": [
      {
        "id": "data_surface",
        "description": "the information card, axes, grid, or map surface already visible in the first frame",
        "prompt_aliases": ["information card", "data surface"],
        "rule": "pixel-locked"
      }
    ],
    "entering_objects": [
      {
        "id": "subject_sequence",
        "description": "the exact repeated rigid subject cutouts named by the storyboard",
        "motion_primitive": "serial-placement",
        "final_region": "their storyboard-defined subject zone only"
      }
    ],
    "draw_on_paths": [
      {
        "id": "primary_path",
        "surface_id": "data_surface",
        "path_description": "the one final chart curve, route, connection, or underline defined by the last frame",
        "direction": "from the storyboard-defined start point to final endpoint",
        "draw_mode": "progressive-tip-growth",
        "marker_rule": "each marker appears only when the growing tip reaches its final coordinate"
      }
    ],
    "timeline": [
      {
        "start_pct": 0,
        "end_pct": 24,
        "behavior": "serial-placement",
        "object_ids": ["subject_sequence"],
        "instruction": "place the exact repeated subjects serially at near-final scale"
      },
      {
        "start_pct": 24,
        "end_pct": 46,
        "behavior": "draw-path",
        "object_ids": ["primary_path"],
        "instruction": "grow only the path tip inside its declared fixed surface"
      },
      {
        "start_pct": 70,
        "end_pct": 100,
        "behavior": "hold",
        "object_ids": ["data_surface", "subject_sequence", "primary_path"],
        "instruction": "hold all final objects; paper-edge and shadow micro-motion only"
      }
    ],
    "forbidden_events": [
      "object replacement",
      "object morphing",
      "duplicate surfaces",
      "cross-zone travel",
      "the fixed surface entering, flipping, moving, or being covered by a duplicate surface",
      "the primary path leaving its fixed surface or transforming into another accent"
    ]
  }
}
```

## Rejection conditions

Reject before submission when:

- `last-frame.png` has `mode=generate` instead of `mode=edit`
- the edit target or its SHA-256 does not match the exact first-frame file
- the imagegen edit call does not record the first-frame path as its sole `referenced_image_paths` input
- change regions cover more than 65% of the canvas
- background pixels outside change regions exceed the configured continuity thresholds
- the prompt gives an entrance instruction to an object already visible in the first frame
- a line is described as a generic accent instead of a path attached to a fixed surface
- two visually similar lines lack separate IDs and separate zones
- the timeline exceeds the duration action budget
- a timeline action references an undeclared object
- the final hold begins after 75%
- the prompt relies on “assemble everything” without object identities and serial timing
