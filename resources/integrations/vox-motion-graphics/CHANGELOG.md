# Changelog

Release history, newest first. Keep new entries in this file rather than creating version-specific changelog files. Corresponding publication notes are available on [GitHub Releases](https://github.com/sfsajid91/vox-motion-graphics/releases).

Historical entries describe the release at that time; the current `SKILL.md` and references remain the production instructions.

## Unreleased — Shot Vocabulary

- Expand motion guidance with purpose-led definitions, prerequisites, honest fallbacks and playback proof for push/zoom, pull-back reveal, orbit/object rotation, parallax, dolly zoom and locked/evidence holds.
- Add named transition guidance distinguishing whip-pan from directional slide, plus match cuts, J/L cuts and hard/hold-to-cuts.
- Resolve conflicting instructions before storyboard freeze; keep technique labels in shot scores rather than the subject/role vocabulary ledger. Preserve open-ended invention and purposeful stillness.
- Add paired behavioral probes for unsupported assets, camera/object distinctions, contradictory motion and audio-led handoffs. These are evaluation cases, not measured creative-quality or rendered-fidelity gains.
- Validation: 14 schema checks and 29 validator tests passed. A small-model planning smoke exercised ten feasible/unsupported shot and audio-handoff scenarios; no video was rendered and no creative-quality gain is claimed.

## 0.10.0 — Visual Invention & Long-Form Direction

Package version: `0.10.0`.

### Directing architecture

- Add Film → Chapter → Sequence → Scene → Beat ownership. Shorts collapse upper levels; long-form uses chapters/sequences for argument, evidence, emotional pacing, motifs, escalation, callbacks and payoffs. Scene-local grammar remains intact.
- Plan visual vocabulary before resolving assets. Distinguish recurring subject identity from repeated staging; useful viewpoints, details, environments, archives, process components and human context bind to the existing provenance ledger, not a second asset system.
- Require before → visible operation → after → viewer inference for explanatory/causal/process scenes. A label entrance alone does not prove the required relationship changed. Identity, chronology, evidence, atmosphere and emotional holds retain their own jobs.
- Compare 2–3 low-cost mechanisms across construction families for difficult or important explanatory beats, before expensive assets or implementation. Choose for comprehension, specificity, surprise, motion potential, truthfulness, feasibility, neighboring continuity and cost.
- Add a pre-implementation sequence pass across construction, scale, camera, primary object, visual/information density, color/value, motion energy, quiet/busy moments and archive/programmatic/metaphor balance. Repetition may establish comparison or a motif; no uniqueness quota.
- Direct important handoffs through focal exit/entry, direction, continuity object/path, shape, scale or semantic contrast. Hard resets, holds, archival cuts and sound-led transitions are intentional choices, not failed morphs.
- Prefer demonstrated thesis/payoffs before text/VO names the conclusion. Justified typography, evidence and emotional contributions remain valid.

### Production and review

- Add independent Scene, Sequence, Chapter (when declared) and Whole-Film critique before freeze and on the mastered draft. Individually approved scenes cannot self-certify the sequence or film.
- Whole-film review assesses progression, visual escalation, callbacks, repetition, style continuity, emotional rhythm, payoff and cumulative comprehension. Defining changes reopen affected scopes; implementation refinements do not trigger unrelated redesign.
- Make storyboard canvases target-ratio, with grouped long-form navigation/contact sheets. Remove vertical-only and fixed-seven-item assumptions while preserving overview-first inspection, the canonical shell and accessible controls.
- Require realistic consumption-size evidence: phone portrait for vertical shorts and desktop/mobile YouTube-scale landscape. Simplify or recompose illegible information instead of shrinking more text into the frame.
- Preserve purposeful stillness, silence, testimony, evidence holds and dramatic pauses. There is no constant-motion or fixed retention-event requirement.

### Contracts and transition

- Extend existing story/storyboard and editorial handoffs rather than replacing the pipeline. Hierarchy/vocabulary and scene contracts make relevant directing choices inspectable; scoped findings live inside the existing design/editorial reports and retain the board/master/report receipt triad.
- Include assets used only through scene vocabulary bindings in the publication readiness/rights/provenance gate. Asset and vocabulary role wording need not match; actual shot fitness remains an editorial judgment.
- Hash-bind local viewing-size proof files inside the board/master-bound review reports. Changing proof bytes invalidates release evidence; the critic still verifies that each proof depicts the reviewed artifact and is readable.
- Replace the universal scene QA check `stateChangeMeaningful` with `visualJobSatisfied`. Explanatory scenes still require a perceptible delta; exempt scenes no longer need a fictional state change to pass.
- Define bounded `ScenePacket` / `SequencePacket` contracts carrying frozen identity and only relevant direction, style, local evidence/assets, aligned timing, neighboring boundaries and proof requirements. No compiler, model router, SDK or new runtime dependency is introduced.
- Legacy manifests remain draft-valid. v0.10 publication requires current direction/scene contracts and independent scope/viewing-size reviews. Reconcile the preview and metadata, inspect real artifacts, then record review digests; never manufacture approval during migration.
- Preserve vague-brief autonomy, claim discipline, representation types, storyboard-first freeze, orthogonal asset lifecycle/provenance, final VO timing authority, semantic conformance, frame-driven Remotion, mastered QA and no generator self-certification.

### PR review fixes

- Publication now requires a populated `direction.vocabulary`; missing, empty, null, or non-array vocabulary cannot bypass the release gate by omitting scene vocabulary references. Provisional drafts remain accepted.
- Affirmative editorial reports (`approve` or `publish_candidate`) now require nonempty `scopeFindings` in the schema. Revision/redesign/unreviewed reports may remain incomplete; the project validator still enforces exact film/sequence/chapter coverage at publication.


### Verification

- All 14 JSON Schemas passed Draft 2020-12 checks and valid/invalid consumer cases. All 54 local Markdown links and schema reference targets resolved.
- All 29 Python validator tests passed, including hierarchy partitions/order, conditional delta exemptions, concept selection, malformed-input findings, populated vocabulary publication requirements, vocabulary-only asset gates, scoped review and changed proof/master evidence.
- Actual CLI publication smoke passed with FFmpeg-encoded 55-second portrait, 300-second multi-sequence landscape and 900-second chaptered landscape fixtures; FFprobe confirmed each encoded duration. Each scenario rejected missing deltas, unresolved rights on vocabulary-only assets, changed viewing proof and missing scoped review.
- Independent code and architecture review identified and repaired malformed/dangling schema definitions, input crash paths, vocabulary asset gate omissions, role-string overconstraint and optional/required rhythm wording drift. Final review found no remaining issues in the reviewed paths and passed all three requested duration envelopes.
- Packet validation is intentionally schema-only. Consumers verify scope membership/order, approval, file bytes and cross-field beat windows before use; no packet runtime validator or router is claimed.

CLI fixtures contain synthetic review metadata, not production approvals or proof of readable/inventive films. No real-video creative benchmark was run.


### Limits

Kodak and Concorde exposed general production weaknesses; neither supplies a mandatory visual template. Charts, reused assets, side profiles, locked cameras, static evidence and direct cuts remain valid when they serve the film. Deterministic validation checks metadata, references, scope coverage and artifact identity—not factual truth, legal clearance, perceptible causality, readability or creative quality. Updated behavioral evaluations are development material; this release does not claim measured improvement in rendered-video quality.

### Release packaging

- Consolidate all seven version-specific changelogs into this file, preserving the complete historical entries. Future versions add an entry here; GitHub Releases carry the corresponding version-specific publication notes.

### Known review notes

- Landscape storyboard authors should adapt the vertical-first focal-stage defaults to an appropriate player size.
- Long-form storyboard authors should adapt hierarchical navigation and sticky offsets to the actual rail height.
- The held-out evaluation procedure still names the older v0.8.1/v0.9.0 comparison; no v0.10 creative-quality benchmark has been run.


## v0.9.0 — Executable Direction and Publication Evidence

### Why this release exists

The independent Concorde and Kodak production postmortems found recurring gaps between sound directing principles, chosen visual mechanisms, and delivered output. Neither established that the written skill caused every failure. This release makes the existing principles easier to execute and their production gates harder to bypass; it does not turn either film's style into a template.

### Directing changes

- Make important concept decisions explicit: viewer inference, starting relationship, visible operation, resulting relationship, invariant, and factual limit. Compare two materially different concepts when a central explanatory beat merely reveals another noun.
- Use a compact joint shot score for composition/viewpoint, object action, camera information, attention, rhythm/payoff, sound or silence, and exit. Choose these autonomously rather than asking a non-designer user.
- Preserve valid identification, chronology, evidence inspection, emotional holds, direct cuts, bold captions, and silence. No required movement, variety quota, palette, caption shape, or fixed hold duration.
- Choose representation before concrete staging. Unsupported route geometry, materials, wear, device mechanics, or gestures must not acquire factual authority from cinematic treatment.
- Keep detailed approval-shell dimensions in the canonical layout reference rather than repeating them in the main directing entrypoint. The shell's tokens do not mandate the film's visual language.

### Production and critique changes

- Unify the stage graph: brief/evidence → concepts/shot scores → storyboard with caption/sound intent → independent design review → freeze → final VO/alignment → timing conformance → implementation → mastered draft → technical and independent editorial review → delivery.
- Preview realistic captions and disclosures before freeze. Review clean and captioned states at delivery size without shrinking accessibility text to rescue an overcrowded composition.
- Conform orientation, semantic trigger, action completion, readable payoff, and transition windows to final VO. Allow justified anticipation and J/L cuts; reading can overlap motion and transitions.
- Accept assets against their actual shot: deepest crop, complete-object payoff, animation requirements, evidence role, and rights. Inspect defining relationships in clips rather than treating asset/state presence as proof.
- Record planned sound as implemented, replaced, or intentionally omitted, with reasons for changes. Review the mastered mix, not just a cue list.
- Have the independent critic observe visual relationships before receiving the director's explanation, then compare with the assigned job and review the accessible master. Route concept failure, weak staging, implementation defect, and taste separately.
- Preserve the approved board snapshot separately from as-built notes. Bind review to the artifact actually inspected.

### Contracts and tooling

- `tools/validate_project.py --stage draft|publish` separates draft validation from publication eligibility; `draft` remains the default.
- Publication requires a populated frozen board, implementation metadata, accepted/verified used assets, resolved rights/provenance, and independently reviewed artifacts.
- New `review-receipt.schema.json` binds the frozen board, master, and design/editorial/technical report files by SHA-256. Reports name review contexts, verdicts, blockers, artifact digests, and review evidence. Missing, negative, self-awarded, or stale evidence fails the publication check.
- Evidence assets require honest origin, a source locator, and supported claim/source linkage. Generated/reconstructed material cannot masquerade as primary evidence; honest reconstructions, first-party records, and supported programmatic charts remain possible.
- Existing storyboard/frame/report schemas gain only the handoff fields used by this workflow: optional joint shot scores, observable relationship invariants/proof locations, semantic timing windows, cue disposition, and artifact-bound review metadata.
- Deterministic checks validate ranges, references, files, and digests—not visible causality, readability, audible sound, reviewer honesty, factual truth, or legal clearance. HTTP(S) source locators are not fetched; linked HTML dependencies are not recursively hashed. Use a self-contained or bundled frozen board.

### Existing-project transition

- Provisional projects may keep rendering and validating as drafts. A draft pass never implies publication approval.
- Before publishing, add `storyboard.preview.path`, `masterFile`, and `reviewReceipt` to the project manifest. Obtain real independent reviews before recording their digests; do not manufacture receipts to satisfy the gate.
- Existing evidence ledgers must provide `sourceUri` and `claimIds` linked through the manifest's `claimSet`. Used assets need traceable rights/creation evidence. Unused candidates may remain unresolved.
- All paths in the receipt and review references resolve from the project manifest directory. See `references/orchestration.md` and the validator help for the exact contract.
- Structured creative handoffs remain optional unless consumed. No new runtime dependency, orchestration service, or rendering wrapper was added.

### Verification and limits

- Schema suite: 12 schemas and behavioral guardrails passed.
- Validator suite: 21 tests passed, including draft/publication separation, changed artifact rejection, rights/evidence checks, review completeness, semantic timing, and readability overlapping action.
- Actual CLI smoke with a 12-second FFmpeg-encoded fixture: draft and valid artifact-bound release paths passed; unfrozen publication, unresolved used-asset rights, synthetic primary evidence, missing rendered-review references, and post-review master mutation were rejected. Fixture review metadata is test data, not approval of a production film.
- A text-only small-model planning smoke exercised autonomous mechanisms, chronology, emotional staging, caption planning, and provisional timing. It exposed unsupported staging specificity, prompting the explicit representation boundary above. This is not a rendered-video quality benchmark.
- Added paired behavioral prompts and a blinded held-out evaluation procedure. Improved small-model video quality remains unmeasured until that evaluation is run; deterministic passes and completed planning fields do not establish a creative gain.

## v0.8.1 — Storyboard Review Guardrails

### Why this patch exists

A real Kodak approval storyboard showed that v0.8 had the right architecture but agents could still over-document the approval page, lock frame precision before final VO, flood simple beats with research telemetry, and style reconstructed evidence too much like a primary artifact.

### Changes

- Added approval-surface ergonomics: visual preview first; long production prompts, frame tables, and implementation detail stay secondary until freeze.
- Split script lock, final voice-performance lock, and frame-timing lock.
- Strengthened the evidence-masquerade gate for newspapers, documents, screenshots, quotes, and retypeset excerpts.
- Added information-budget guidance so verified facts do not automatically become on-canvas telemetry.
- Added sound provenance guidance: device-specific effects are illustrative unless sourced as authentic.
- Added data/time-compression guidance for counters and per-unit SFX.
- Translate named creator references into observable production grammar after analysis.
- Added storyboard hard blockers and regression prompts for the new cases.

### No architecture change

The core pipeline remains:

`research/script -> narrative beats -> visual concepts -> HTML storyboard -> critique -> refinement -> freeze -> final VO/alignment -> Remotion -> audio/captions -> QA -> render`

## v0.8 — Storyboard-First Editorial Direction

### Major additions

- HTML/CSS/JS storyboard or motion preview as the primary visual decision surface and creative source of truth.
- Editorial critique, refinement, freeze, and post-freeze change control before Remotion implementation.
- Explicit process/system visualization guidance and stronger anti-slideshow checks.
- Separate editorial and technical QA references and schemas.
- Orthogonal asset lifecycle: origin, technical status, editorial status, rights status, and representation type.
- Deterministic project validator for timing, declared final holds, asset coherence, storyboard completeness, and implementation state drift.
- Positive and negative example sets that preserve both successful corrections and failed approaches.
- Autonomous orchestration guidance for bounded retries, approval gates, safe parallelism, resumable runs, and post-freeze change control.
- `ready_for_approval` storyboard state so an independent critic can finish review without bypassing a requested human approval gate.

### Removals and simplifications

- Reduced `SKILL.md` from a large rule catalog to workflow, decisions, gates, and reference routing.
- Replaced 19 overlapping numbered references with focused stage-based references.
- Removed eight redundant or weak contracts: separate asset plan/graph/approval/critic schemas, generic production state, monolithic QA, scene-concepts, and the oversized scene plan.
- Removed universal Studio/`Interactive.*` requirements, mandatory tune manifests, unsupported complexity counts, and repeated source-specific creative-DNA sections.
- Consolidated repeated mechanism, motion, style, truthfulness, and user-autonomy guidance into canonical homes.

### Behavioral changes

- Creative direction is resolved in the storyboard; the Remotion stage implements the frozen defining relationships. Machine metadata indexes the approved preview instead of duplicating it as a second creative spec.
- Narration, captions, scenes, transitions, final hold, and composition duration form one measured timing contract.
- Static slow zooms, long unchanged holds, and repeated process cards now trigger explicit editorial review when narration changes structure.
- Generated, technically verified, and editorially accepted assets are no longer conflated.
- A technical pass cannot produce editorial approval. Publish-candidate status requires independent editorial review.

### New workflow

`research/script -> narrative beats -> visual concepts -> HTML storyboard -> critique -> refinement -> freeze -> final VO/alignment -> Remotion -> SFX/music/captions -> editorial + technical QA -> render`

### Known limitations

- Aesthetic quality, stillness, “Vox-like” style, and storyboard/render visual similarity are not deterministically scored.
- The project validator checks declared metadata; it cannot prove the rendered focal hierarchy or motion relationship.
- PNG alpha inspection is supported; other alpha-bearing formats require an external check.
- No universal safe-zone, audio loudness, dead-tail, final-hold, object-count, or motion-density thresholds are imposed.
- The mined evidence is deep but largely from one documentary project; more genres are needed before promoting additional numeric or stylistic rules.

## v0.7 — Implementation Finish Contracts

### Why

v0.6 established the directing model. v0.7 closes the gap between a good
creative plan and a Remotion composition that is visually correct, deterministic,
and editable in Studio.

### Added

- Studio-first layer contract:
  - named `Interactive.*` elements for major editable layers;
  - typed props and inline `defaultProps`;
  - Studio layer-tree verification.
- Explicit repeated-motion entrance modes:
  - `synchronized`;
  - `staggered`;
  - `sequential`.
- Deterministic texture contract for paper, grain, halftone and registration:
  - frame plus stable layer seed for procedural samples;
  - spatially stable treatment unless motion is intentional;
  - text kept outside treatment filters;
  - bounded, editable treatment controls.
- Compositing geometry invariants for fills, tint, grain, outlines and masks.
- Data-graphic finish contract covering locked datasets, shared origins, scale,
  bar geometry, axis alignment and settled-frame legibility.
- Pixel-level diagnostics for entry, in-motion and settled renders.

### Corrected Failure Modes

- Plain `div` layers hidden under `AbsoluteFill` and unavailable in Studio.
- Chart scale and chart origin drifting away from the headline origin.
- Texture clips silently reducing the visible height of bars.
- Animated edge noise reading as fabric or wind instead of printed ink.
- Bar overlays using different bounds from their source bars.
- Staggered entrances appearing where the brief requires synchronized motion.
- Procedural noise implemented with uncontrolled randomness.

### Preserved

- v0.6 editorial physicalization and reference-learning model.
- Optional treatment selection; paper, halftone and grain remain story/style
  decisions, not defaults.
- External critique and no self-awarded production approval.

### Compatibility

No existing schema contract is removed. Existing tune manifests and parameter
patches remain valid; treatment controls should now include bounded density,
size, opacity and edge-variation fields when those treatments are selected.

## v0.6 — Creative Autopilot + Reference Grammar

### Merged
- v0.5 autonomous directing architecture, asset/evidence contracts, render critic and parameter repair loop.
- Editorial-instinct and physical-metaphor lessons from the modified MoSidd branch.
- MoSidd-derived motion rigs and reference-recreation methodology.
- Remotion property-control ideas, repurposed as an autonomous critic/tuning API.
- Optional halftone treatment tool.

### Added
- “Show the mechanism, not the noun” editorial-translation algorithm.
- `Anchor -> Action -> Consequence -> Launchpad` retained and expanded with many non-conflict scene grammars.
- Attention/gaze continuity planning across scene cuts.
- Construction-family library beyond four fixed archetypes.
- Structured reference deconstruction with classification:
  - creator_dna
  - surface_style
  - technique_recipe
  - benchmark_specific
- Optional treatment recipes rather than mandatory texture stack.
- Tunable parameter manifest and critic parameter-patch contracts.
- Contact-sheet helper for references/diagnostic frames.
- Behavioral regression prompts covering history, economics, UI, geography, premium product, data and reference-learning.

### Strengthened
- Generator cannot self-certify quality.
- Evidence specificity and representation safety.
- Asset graph/reuse and motion-aware raw asset rules.
- Narration-aligned semantic choreography.
- Remotion parameterization for autonomous art-direction repair.
- Gaze-continuity repair before scene redesign.

### Explicitly NOT universalized
- one narration sentence = one scene
- exactly six scenes
- fixed 65–85 word script budget
- fixed 3–5 second scene length
- mandatory Actor/Counter-force/Stakes conflict
- mandatory halftone / paper / grunge / vignette / 12fps boil
- fixed VO/BGM/SFX volume ratios
- fixed caption coordinates or universal safe-zone percentages
- exact benchmark frame counts
- self-awarded “9.9/10” quality audit

### Validation
16 JSON schemas pass Draft 2020-12 validation and behavioral guardrail tests.

## v0.5 — Creative Autopilot

Major change: move from a staged framework that still expects a knowledgeable operator to an autonomous directing system intended for vague briefs and non-motion-designers.

### Added
- Autopilot user-interaction policy: no motion-design questions by default.
- Director Brief normalization and material-world/contrast-pair inference.
- Creative Scene Engine with `Anchor -> Action -> Consequence -> Launchpad` visual grammar.
- Scene mechanism library and metaphor ladder.
- Internal concept search / cheap prototype selection for high-uncertainty scenes.
- Derived creator-DNA reference from the supplied MoSidd practice corpus.
- Asset graph + motion-aware routing as a first-class stage.
- Automated art-direction loop with diagnostic frames and targeted parameter search.
- Rig reuse / reskin rule.
- Current Remotion implementation guidance and no timed CSS animation.
- Claim-specificity invariant and generator QA guardrails.

### Removed as universal assumptions
- mandatory cream paper / halftone / marker strokes
- mandatory film grain / scan lines / gate weave
- exact word/line counts
- fixed scene length
- fixed caption position
- fixed audio volumes
- one narration line = one scene
- mandatory tension triangle in every scene
