# Workflow

## Purpose

Use this workflow when building a short paper-collage animation from scratch or when reverse-engineering a reference piece into a reusable production system.

Choose the correct branch first:

- `single-scene`: one short handcrafted collage piece with a reveal and a living tableau
- `vo-sequence`: a narration-led editorial explainer made of multiple modular scenes

Before that branching step, the user-facing mode choice should be:

- `remotion-code`: build the video primarily with editable code animation
- `video-model`: build the video primarily with the video-model route

Across both branches, route each scene like this:

- `remotion-cutout`: use when the scene is layerable and editable as separable cutouts
- `seedance-first-last`: use when the scene is too dense for practical cutout animation and should behave like one integrated animated collage tableau

Default video model for the complex route: `doubao-seedance-1-5-pro-251215`. The model ID is case-sensitive; uppercase `Pro` is invalid.

If you need fixed field names, route thresholds, or pass/fail acceptance, normalize every output against `output-contract.md`.

## Core sequence

1. Pass `Gate 0`: environment and capability self-check.
2. Pass `Gate 1`: user-choice lock.
3. Decode the reference or brief.
4. Lock the beat board.
5. Route branch: build a layered asset pack for Remotion, or exactly two keyframes per Scene for Seedance.
6. Assemble the living scene.
7. Add sound and render.

Do not collapse these phases into one pass unless the user explicitly asks for speed over quality.

## Gate 0: Environment and capability self-check

Run this gate on every invocation, before reading the brief into beats:

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/preflight.py
```

The command must exit successfully. A Markdown report or a `needs-action` field is not a pass.

Confirm:

- `~/.codex/skills/paper-collage-video/.env` exists
- that exact skill-local `.env` contains a non-empty `ARK_API_KEY`; a process environment value is not a substitute
- the `imagegen` skill is installed and readable
- the Remotion skill/plugin is installed and readable
- local `node` and `npm` are available
- popup support state is known from the current tool inventory: function-calling popup available or unavailable
- the chosen aspect ratio is one of `16:9`, `9:16`
- every Seedance complex scene has exactly 2 local stills
- every Seedance complex scene stays inside the 4-12 second model window

If the preflight exits non-zero, stop. Do not create a project directory, storyboard, asset list, or animation code.

## Gate 1: User-choice lock

Before decoding the brief into beats or scenes, lock these user-facing decisions:

- `mode`
- `aspect_ratio`
- `audio_mode`

Automatically lock `style_family=vox-mixed-media`. It is no longer a user-facing choice.
Automatically lock `total_duration_rule` from source audio, generated voiceover, an explicit duration already present in the brief, or an estimate from content, in that priority order. Never show a duration-choice popup.
Automatically lock `scene_duration_policy=auto-by-content` for `video-model` and `not-applicable` for `remotion-code`. Never show a per-scene duration popup.

If the host supports Tool Call / Function Calling popups, this gate must be satisfied through the popup contract in `popup-tool-contract.md`.
If popup support is unavailable, ask the same choices as a short text list and wait for the user's reply.
Popup unavailability never authorizes defaults. If this gate is incomplete, do not continue into planning.

For `video-model`, duration planning is always hierarchical:

1. Lock or estimate the whole-video timeline.
2. Split the source into semantic scenes; one scene should express one visual proposition or causal step.
3. Assign each scene its narration/content window.
4. Choose an integer Seedance request duration from `4-12s` for that scene.
5. Split again when one scene needs more than `12s`, more than 4 non-hold action groups in a 5-second request, or more than 7 in a longer request.

The user never chooses individual scene duration. `auto-by-content` is mandatory for `video-model`; the agent calculates each request duration from the Scene's semantic content window and motion budget.

## Phase 1: Decode the reference

Produce these outputs first:

- A one-paragraph style thesis
- A master asset sheet with every visible cutout or derived layer
- A beat list with timings, entrances, reveals, and loop behavior
- A route hint per beat or scene: `remotion` or `seedance`
- A `motion_intent` paragraph for any scene likely to go to Seedance

Capture these facts:

- Background texture and palette
- Number of depth planes
- Which assets are generated, supplied, or derived from another asset
- Which motions are smooth versus stepped
- Which reveal device starts the scene
- Where sound should enter and leave

If the project is `vo-sequence`, also capture:

- final narration lines
- word or line timing windows
- which beats can share one scene
- the repeated visual system across the whole sequence
- which scenes are simple enough for Remotion-built motion versus which need Seedance

If the user provides only a concept and no reference clip, infer a beat list that uses the same grammar as the source kit:

- Beat 1: closed or hidden state
- Beat 2: reveal mechanic
- Beat 3: scene fully open
- Beat 4: hero element arrives
- Beat 5: living loop or held tableau

If the project is `vo-sequence` and the user provides narration lines, treat each non-empty line as a candidate beat before merging them into scenes.

When the user provides only a story, a narration draft, or a loose brief, confirm these production choices before moving on:

- production mode: `remotion-code` or `video-model`
- aspect ratio: `16:9` or `9:16`
- content shape: `single-scene` or `vo-sequence`
- audio handling first:
  source audio exists -> use source audio
  no source audio -> ask `generate Mandarin male voiceover` or `no audio`
- automatic total-duration handling after the audio choice:
  source audio exists -> lock the whole-video runtime to the audio duration
  generated voiceover selected -> skip the duration question and use the measured MP3 duration
  no audio selected and the brief contains an explicit total runtime -> honor it
  no audio selected without an explicit runtime -> estimate the whole-video runtime from content
- automatic scene-duration policy:
  `video-model` -> `auto-by-content`
  `remotion-code` -> `not-applicable`
If generated voiceover is selected, stop before beat planning and run the Voiceover Gate:

1. Lock the final narration text.
2. Run `preflight.py --require-edge-tts`.
3. Generate `voiceover.mp3`, `voiceover.srt`, and metadata with `generate_edge_voiceover.py` using `zh-CN-YunjianNeural`.
4. Replace the whole-video duration with the measured MP3 duration.
5. Build beats from SRT cue windows and only then group beats into semantic scenes.

Never estimate duration or evenly distribute narration lines after a generated SRT exists. Multiple adjacent SRT cues may be merged into one scene, but cue timing remains authoritative.

Preferred behavior:

- if the host supports Tool Call / Function Calling popups, emit a popup tool request instead of plain text
- if popup UI is unavailable, ask with a short text option list
- do not silently choose production mode, aspect ratio, or no-source-audio handling when the user has not provided them; runtime rules are derived automatically

When popup tool support exists, use the host popup contract defined in `popup-tool-contract.md`.

Only if the user explicitly delegates the choice, apply these defaults:

- production mode: `remotion-code`
- content shape: infer from request shape
- aspect ratio: `16:9`
- orientation: infer from aspect ratio
- audio mode: use source audio when present; otherwise `no-audio` only when the user explicitly delegates defaults
- total duration: follow source or generated voiceover when present; otherwise estimate from content
- video-model scene duration: `auto-by-content`; assign each semantic scene an integer `4-12s` request duration and split again if it needs more than 12s
- route default: `remotion-cutout` unless the scene meets the Seedance route matrix

Before invoking the scaffold, record the decision origin as `user-selection` or `user-authorized-defaults`. Never label an inferred model choice as user-selected.

## Phase 2: Lock the beat board

Create a storyboard using the actual or planned assets whenever possible. Add timing and motion notes under each panel.

The board must answer:

- What appears in each beat
- What changes between beats
- Which layer each prop belongs to
- Which motions loop after the reveal
- Which moments need sound sync

For `vo-sequence`, also answer:

- which beats belong to which scene
- which scene module type each beat wants
- which scene route each scene wants
- where a foreground anchor or label appears
- which spoken words trigger counters, highlight sweeps, or typewriter reveals

Use a stop gate here:

- If the board looks wrong, revise now.
- Do not generate a full asset pack or write the animation build yet.

## Phase 3: Build or collect the asset pack

This phase has a hard route split:

- `remotion-cutout`: follow the layered asset-pack, Composition Blueprint, background, cutout, collision, and provenance rules below.
- `seedance-first-last`: skip the layered asset pack completely. Do not create `ASSETS.json`, background/hero/support cutouts, a contact sheet, Composition Blueprint, `07_remotion`, or a Remotion template. Generate exactly `first-frame.png` and `last-frame.png` for the Scene and continue at the Seedance rules below.

Never execute the Remotion branch first as a style test or preparation step for Seedance. Route selection happens before the first image call.

Separate assets into two origin buckets:

- Supplied: files already provided by the user or kit
- Generated: new transparent PNGs or textures

Record crops, masks, matte cleanup, and color correction as `provenance.postprocess` on the originating generated or supplied asset. Do not treat local drawing as a third origin bucket.

For `vo-sequence`, allow a fourth bucket:

- Motion-built: animation containers, transitions, timing rigs, masks, camera moves, and layer choreography built in Remotion while all visible image content still comes from `imagegen` or supplied files

For generated assets:

- Use the `imagegen` skill as the default generation path for all new image assets
- An instruction to use imagegen is not sufficient: make an actual `image_gen` tool call for every distinct asset
- Preserve the unmodified selected result, per-asset prompt, tool receipt, and hashes according to `asset-provenance-contract.md`
- If image generation is unavailable or fails, stop; never substitute a project-local raster drawing script
- Bake the collage treatment into the prompt
- Keep each asset regenerable as a single prompt or command
- Favor transparent PNG output
- Preserve the original imagegen result, then alpha-trim each final non-background PNG to 3-5% transparent padding; record the crop in provenance
- Classify each final asset as `portrait-subject`, `wide-group`, `object-prop`, `editorial-card`, `foreground-strip`, or `accent-mark` before choosing its size
- Match new line-art assets to an existing reference cutout when style continuity matters
- In `remotion-code` mode, treat Remotion as the animation engine only. Do not draw charts, newspapers, speech bubbles, counters, quote cards, or other scene-defining visible art directly in SVG or React code. Those surfaces must exist first as approved image assets unless the user explicitly asks for code-drawn graphics.

Generation order for `remotion-code` scenes:

1. Lock the visual metaphor, layout archetype, reading path, and motion rhythm.
2. Lock `color_script` from `0720-bright-paper-style.md`: chromatic dominant/support/accent roles, area budget, hero/background separation, adjacent-Scene shift, exact prompt palette sentence, and negative palette terms.
3. Write final element boxes, action-end boxes, z-order, motion corridors, safe gaps, and intentional overlap pairs.
4. Build `background_contract`: allowed fixed stage elements, forbidden moving-subject aliases, saliency budget, and one low-detail reserved zone covering every moving asset.
5. Check pairwise final overlap and motion-path collisions before any image call.
6. Set `composition_blueprint_locked=true` and run `python3 tools/validate_composition_blueprint.py --project .`; stop if it fails.
7. Generate exactly the approved minimum pack first: one Scene-specific background plus three independently timed narrative assets. The scaffold provides `background.md`, `hero-cutout.md`, `support-cutout-01.md`, and `metaphor-driver.md`; rename roles in the Manifest when content needs a more precise asset, but do not skip the four-asset minimum or generate optional decoration before the minimum pack is approved.
8. Every background prompt must repeat the Gate 1 orientation, aspect ratio, and target canvas dynamically. Never hardcode `16:9`; isolated-asset prompts must also state the locked delivery frame and forbid full-scene or multi-option outputs.
7. Generate the colorful-but-quiet `background plate` only.
8. Inspect the background alone. Reject duplicate subject classes, high-detail objects in reserved zones, muddy neutral casts, or any background focal point that competes with the metaphor.
9. Lock the background review fields.
10. Generate hero and content-specific moving assets separately, copying the exact palette contract into every prompt.
11. Generate optional environment, editorial, foreground, and accent assets last.
12. Inspect the assembled asset set at thumbnail size and lock the color review fields.
13. Only after that, assemble the scene in Remotion.

For `vox-mixed-media`, apply `vox-motion-contract.md` before generation:

- generate a different background plate for each scene by default
- treat each background as a low-saliency stage, not a completed scene illustration
- use the `0720-bright-paper` hierarchy by default; low saliency means broad low-detail chromatic fields, not beige or desaturated color
- prohibit the background from containing detailed duplicates of any moving subject or metaphor object
- reserve every moving asset's landing box and motion corridor before background generation
- reject unapproved pairwise overlap above 8% of the smaller final alpha-visible box
- require 4-8 approved raster assets per scene
- require at least 3 independently timed moving assets excluding the background
- record each asset's frame occupancy, anchor, appearance order, appearance reason, entrance, settle, hold, and exit
- calculate visible occupancy from the final PNG's non-transparent alpha bounds rather than trusting its CSS container dimensions
- set `sizing_mode=height-driven` for portrait subjects, `width-driven` for wide groups/cards/strips/marks, and `box-contain` for isolated props
- separate entrance `motion` from semantic `action_motion`; retreat, chase, convergence, replacement, defeat, rise, and fall require a concrete action phase
- derive `appearance_order` from the content sequence before writing Remotion code
- set the three content/composition/motion locks only after checking every asset against its source phrase
- never generate one cross-scene hero sheet or combine independently moving story elements into one hero image

Background plate rules:

- one stable environment only
- broad, quiet shape language
- no extra decorative sticker scraps
- no surprise labels or graphic marks
- no extra people, props, or symbols beyond the approved background plan
- preserve negative space for incoming subjects and overlays
- express negative space as numeric reserved zones tied to asset IDs, not only as prose
- keep strongest contrast, edge density, texture, and accent color outside reserved zones
- when a building, vehicle, person, chart, machine, or document is a moving asset, use abstract side masses, terrain, wall, floor, horizon, or broad geometry instead of another detailed object of that class

Hard gate for `remotion-code` scenes:

- if a scene-defining visible asset is still missing, stop and generate or request that asset
- do not substitute missing primary art with code-drawn SVG, CSS geometry, or live typography
- placeholder boxes are acceptable only inside an unfinished scaffold, never as the intended final visual language
- if the background plate already contains the hero subject, support props, or decorative clutter that should live in separate layers, reject it and regenerate
- reject any scene missing `background_contract`, `collision_plan`, cleared reserved zones, duplicate-subject review, or motion-path review
- reject non-allowlisted element overlap above the Scene's default limit
- run `python3 tools/validate_collage_project.py --project .` before Studio or render
- reject every `.svg` file, inline `<svg>`, SVG data URI, or code-generated substitute for a missing raster asset
- reject Pillow, ImageDraw, Canvas, OpenCV, Cairo, Matplotlib, Sharp, ImageMagick drawing, or any other project-local procedural visible-asset generator, even when its output extension is PNG
- reject `source=imagegen` unless its prompt, original imagegen output, result receipt, and prompt/original/final hashes validate
- require each scene's `ASSETS.json` to be approved and to resolve separate raster `background_plate`, `hero_cutout`, and at least two content-specific moving assets derived from the visual metaphor
- reject reused background paths unless `background_policy=shared-continuity` and user authorization is recorded
- reject a scene with fewer than 4 approved assets or fewer than 3 independently timed non-background assets
- reject missing, duplicate, or non-contiguous `appearance_order` values
- reject missing subject size or per-element motion fields
- reject non-background assets with large transparent margins, mismatched content kind/sizing mode, or projected visible occupancy below the Vox minimum
- reject narrated actions represented only by entrance motion or passive drift
- reject any scene whose `content_order_locked`, `composition_locked`, or `motion_plan_locked` value is not `true`

For `seedance-first-last` scenes:

- Generate exactly 2 stills, not one
- Read the Scene canvas from the Gate 1 `aspect_ratio`; never hardcode `16:9`. The scaffold maps `16:9` to `1536x864 horizontal` and `9:16` to `864x1536 vertical` and writes that contract into both the prompt and `SEEDANCE_SCENE.json`
- Generate `first-frame.png` once with the `imagegen` skill; it is the empty or near-empty plate containing all fixed scene scaffolding
- Immediately run `python3 tools/validate_seedance_first_frame.py --project . --scene-spec ...`; do not generate the last frame until the first frame matches the Gate 1 canvas
- If imagegen returns another ratio, preserve its receipt and original hash, normalize or regenerate it before the last-frame call, record the postprocess, and use the normalized file as the actual edit target
- Inspect the local first frame with `view_image`, then create `last-frame.png` only through built-in `image_gen` edit mode with the exact first-frame path as the sole `referenced_image_paths` entry
- Treat `last-frame.png` as an additive edit state of the first-frame canvas, never as an independent text-to-image generation
- Limit edits to declared `change_regions`; preserve canvas, crop, camera, background geometry, fixed objects, paper tears, texture, and color outside those regions
- Keep one prompt per still so the scene is regenerable
- Fill `SEEDANCE_SCENE.json` before submission
- Fill `keyframe_generation_contract` with actual imagegen receipts, hashes, edit target, change regions, and continuity review
- Run `python3 ~/.codex/skills/paper-collage-video/scripts/validate_seedance_keyframes.py --project [project-root] --scene-spec ...` before submission
- Fill and validate its structured `motion_contract` before submission; prose alone is not an acceptable motion specification
- compare the actual first and last images, then lock `frame_state_audit_locked` and `prompt_contract_consistency_locked`; never infer persistence from an outdated image prompt
- classify first-frame persistent surfaces as fixed objects, arrivals as entering objects, and curves/routes/underlines as draw-on paths attached to a fixed surface
- keep 5-second scenes to 4 non-hold action groups and 10-second scenes to 7
- Run `python3 ~/.codex/skills/paper-collage-video/scripts/run_seedance_scene.py --project [project-root] --scene-spec ...` or `--scene-slug ...`
- Never crop or resize either keyframe after the last-frame edit; post-edit canvas changes invalidate the recorded edit target and hashes

When `first-frame.png` is intentionally empty or near-empty, also require:

- an explicit `allowed objects` list in the video prompt
- an explicit `forbidden objects` list in the video prompt
- each key foreground prop described as one rigid flat paper cutout
- a serial enough assembly order to follow visually
- no broad semantic categories like `grocery elements` when one exact object identity is intended

Before submission, reject the scene if any of these are still true:

- any required field still contains placeholder text such as `[fill ...]`
- the first and last still do not share one aspect ratio
- the last frame was independently generated instead of edited from the exact first-frame bytes
- `last_frame.referenced_image_paths` does not contain only the first-frame path
- the protected area outside `change_regions` exceeds the allowed pixel-difference thresholds
- the prompt does not describe the final tableau
- `motion_intent` does not state camera rule, assembly order, anchored element, and hold behavior
- a first-frame object is instructed to enter, drop in, flip, or be replaced
- a chart line, route, string, or underline lacks a fixed surface and progressive draw rule
- visually similar lines are not assigned separate identities and zones
- the structured timeline exceeds the scene's action budget or delays the hold past 75%
- an empty-first-frame scene still leaves object identity open to interpretation

Review the pack on a contact sheet or quick layout before animating.

Use a stop gate here:

- Regenerate weak assets now.
- Do not compensate for weak art with motion tricks.

## Phase 4: Assemble the living scene

Treat the animation as a system of layers plus motion rules.

Define:

- Layer order
- Entry and exit timing
- Loop rates per depth plane
- Pivot points for rocking or hinge motion
- Which elements use smooth interpolation
- Which elements use stepped holds
- Which props expose user controls

If the project is `vo-sequence`, also define:

- per-scene duration in frames
- the shared palette contract and each scene's independent background concept
- per-scene prop presets
- the assembly order inside the master sequence

Default motion recipe:

- Background: smooth drift
- Midground: gentle parallax and reveal transitions
- Characters or hero prop: stepped holds with uneven durations
- Scene-ending tableau: looping micro-motion only

Default editorial sequence recipe:

- background: shared and visually locked across scenes
- cut-outs: spring into place with silhouette strokes
- charts and counters: animate approved image assets on cue
- alpha plates: run as transparent video layers
- text systems: animate approved text-image assets, or keep them out of the generated imagery entirely when subtitles/final assembly will handle them

Default Seedance recipe for complex scenes:

- first frame: empty or near-empty plate
- last frame: final assembled tableau hold
- motion intent: describe assembly order, secondary motion, what remains anchored, and where the shot settles

For empty-first-frame scenes with a small number of critical props, prefer this tighter recipe:

- first frame: keep it empty, but keep the fixed background highly stable
- objects: define a strict whitelist of the only props allowed to appear
- substitutes: explicitly forbid likely semantic substitutions
- motion: chart or background logic first, hero object second, support props third, labels last
- hold: no new prop creation after the frame reaches the approved tableau

Use a stop gate here:

- Review at normal speed.
- Fix timing and pose-hold rhythm before touching audio.

## Phase 5: Add sound and render

Pitch music direction options before generation. Let the user select a direction. Then add a restrained set of cues.

Default sound structure for a ten-second piece:

- One music bed
- One reveal foley cue
- One continuous ambience or bed
- One accent cue tied to an on-screen moment

For `vo-sequence`, default sound structure becomes:

- one voiceover stem
- use source audio only when the user has provided source audio
- otherwise keep the render silent
- optional sparse effects only if the user explicitly asks for them

Review once without watching the video:

- If a cue calls attention to itself, lower it or remove it.

## Deliverables checklist

Use this checklist at the end of the task:

- Storyboard approved
- Remotion asset sheet complete, or Seedance two-keyframe contract complete
- Narration timeline approved
- Beat-to-scene mapping approved
- Prompt pack saved
- Scene structure documented
- Seedance first-frame and last-frame paths documented
- Motion intent documented for Seedance scenes
- Sequence assembly documented
- Prop controls exposed
- Sound timings documented
- Render settings chosen
- Final review notes captured

## Pass/Fail gates

Treat these as acceptance rules, not suggestions.

### Intake gate

Pass only if:

- one canonical `scene` statement exists
- one canonical production mode is chosen
- one canonical duration rule is chosen
- aspect ratio and audio mode are known or defaulted
- the project is clearly marked `single-scene` or `vo-sequence`

### Beat gate

Pass only if every beat has:

- an id or slug
- start and end time
- one narration line or one visual statement
- one visual idea
- one route hint

### Scene gate

Pass only if:

- every beat belongs to exactly one scene
- scenes cover the full runtime with no gaps or overlaps
- each scene has one route
- each complex scene has one `motion_intent`

### Seedance gate

Pass only if:

- there are exactly 2 stills
- the first-frame canvas matches the Gate 1 aspect ratio, orientation, and canonical dimensions before the last-frame call
- `first-frame.png` exists
- `last-frame.png` exists
- `SEEDANCE_SCENE.json` contains no placeholder markers
- requested duration is between `4-12s`
- no `ASSETS.json`, cutout pack, contact sheet, Composition Blueprint, or Remotion project was generated for a `video-model` Scene
- neither keyframe was cropped or resized after the last-frame edit
- output paths are defined

### Final review gate

For `remotion-code`, the scaffold always creates `07_remotion/`; it must not create Seedance specs or keyframe folders. Run `npm run studio` and `npm run render` from `07_remotion/`. These commands reuse the fingerprinted runtime under `~/.codex/cache/paper-collage-video/remotion-runtime/` and enforce blueprint, asset/provenance, and TypeScript gates. Do not run `npm install` or browser installation per project.

`npm run render` produces only `07_remotion/out/rough.mp4`, semantic review frames, and a pending hash-bound `05_render/layout-audit/review.json`. View the contact sheet and approve all checks, then run `npm run finalize` to create `05_render/final.mp4`.

Legacy Remotion manifests without `manifest_version=2` must be migrated with `migrate_asset_manifests.py`, visually reviewed, and relocked before they enter the current gates.

Pass only if:

- all deliverables listed for the chosen mode exist
- no unresolved `[fill ...]` markers remain
- route choices are documented
- review notes say either `approved` or `revise`
