# HTML Storyboard & Design Freeze

## Purpose

The storyboard is the film's primary **visual decision surface**. Build it after the narrative beats and scene concepts are credible, and before production Remotion work begins.

Use ordinary HTML, CSS, and minimal JavaScript to resolve the decisions that are expensive to discover after implementation:

- composition and focal hierarchy;
- asset choice and crop;
- scene structure and meaningful visual states;
- motion and transition intent;
- pacing and intentional holds;
- caption mode, realistic text/disclosure loads, and sound intent;
- continuity between neighboring scenes.

The storyboard is not a second renderer. It should communicate the intended experience without reproducing Remotion's frame math, media pipeline, effects stack, or component architecture.

Treat the browser preview itself as the creative source of truth. JSON/Markdown may index scene IDs, review state, or machine-checkable metadata, but should not restate the whole storyboard in a second format. If two representations drift, stop and reconcile them instead of letting an agent guess which one is current.

## Place in the Workflow

`brief/evidence -> concepts and shot scores -> storyboard with caption/sound intent -> independent design review -> freeze -> final VO/alignment -> timing conformance -> implementation -> mastered draft -> technical and independent editorial review -> delivery`

Do not begin detailed scene implementation while important composition, asset, or mechanism decisions remain unresolved in the storyboard. Cheap draft previews remain permitted to answer those questions; a draft render is not publication approval.

## Storyboard Architecture

The storyboard is the visual decision surface for both short and long work: scan the larger structure, then inspect the relevant scene without losing navigation or neighboring context.

Before building the shell:

- Always load [storyboard-layout.md](storyboard-layout.md), the canonical layout contract.
- A project `DESIGN.md` may override tokens and named rules. Preserve shell anatomy unless its `Layout` section explicitly changes it.
- Treat the shell as layout grammar, not a template for topic, assets, copy, scene count, or animation.
- Keep frame art, scene-specific visual systems, and motion studies inside the shell.

### Navigation and inspection

Expose Film → Chapter → Sequence → Scene → Beat navigation where those levels exist. Shorts may collapse to one film/sequence overview and need no artificial chapter or extra approval page. Long-form work should remain browsable by chapter and sequence, with grouped contact sheets for the relevant scene ranges rather than one unwieldy wall of thumbnails.

Start at an overview that communicates progression and lets the reviewer jump to a scene. The scene inspection view should retain breadcrumbs and nearby sequence context, and provide a clear route back to the overview. Beats are inspectable within a scene when their timing or visual change needs review. Navigation and controls retain minimum 44px targets.

The overview and inspection canvas use the project's target aspect ratio, not a fixed vertical format. Grouped contact sheets may adjust card density to the number of scenes while preserving the shell's scanning hierarchy and usable controls.

### Layout shell

Use a centered editorial frame, masthead, sticky director rail, overview/grouped contact sheets, repeated scene inspection units, and concise director notes. Each scene inspection presents context and focal visual beside supporting sequence/beat views when useful. The canonical layout reference gives responsive behavior and visual tokens; these may be adapted for target ratio and long-form browsing without reintroducing fixed seven-scene or vertical-only constraints.

The shell is the approval surface. It must make hierarchy obvious without requiring the reviewer to read implementation notes.

### Scene construction and direction

Before asset acquisition, define vocabulary as subject identity, visual role/viewpoint, and representation—not as a predetermined composition. Bind selected assets later through the existing asset ledger. Reuse is intentional when an asset, motif, or visual role recurs with a clear narrative purpose; record that purpose rather than forcing novelty.

Describe each scene's visual contribution, construction family, staging, density, and rhythm profile. For difficult or important explanatory beats, including unresolved label-only mechanisms, compare 2–3 materially different low-cost concepts across construction families before expensive sourcing or coding. Select one and state why; do not create variants for low-stakes or non-explanatory scenes.

Explanatory scenes that claim a relationship change require a conditional `stateDelta` with `before`, `operation`, `after`, and `viewerInference`. Identification, evidence, chronology, atmosphere, or emotion may use another suitable job; a justified hold is valid and need not invent a delta. The universal editorial check is `visualJobSatisfied`: judge whether the assigned contribution is perceptible, not whether four fields exist or every scene changes state.

For each sequence, state its `purpose`, `payoffTrajectory`, `repetitionAssessment`, and `rhythmIntent`; one line may justify a quiet or uniform passage. Chapters, when present, state their `argumentTurn`, `evidenceBurden`, and `payoff`. For important neighboring relationships, record an observable handoff/payoff intent and proof location. Hard cuts, contrast, sound-led transitions, typography, and stillness are valid. Scan construction, scale, camera, object, visual/information density, value/color, motion energy, and media mode; explain intentional repetition without quotas or family bans.

---

## Storyboard Content Contract

For each scene, make the following visible or inspectable:

- semantic job and compact concept decision: inference → before → operation → after → invariant → factual limit, when a state delta applies;
- focal subject, construction/staging, meaningful entry/change/payoff/exit states, and rhythm profile;
- joint shot score from [motion-patterns.md](motion-patterns.md): composition, object action, camera/revealed information, attention, rhythm, sound, exit;
- selected construction family and, for difficult or important explanatory beats, materially different mechanism alternatives considered;
- pre-asset vocabulary identity, visual role/viewpoint, representation, and later asset bindings;
- asset roles, acceptance evidence, and current status;
- caption mode, realistic clean/captioned previews, and editorial text/disclosure roles;
- provisional semantic anchors and actual readable payoff intent;
- important handoff/payoff promises with observable invariants and proof locations;
- known uncertainty or representation risk.

The storyboard should answer: where does the eye go first; what does the visual contribute; what changes or usefully holds; can the reviewer perceive the intended relationship and payoff; how does attention hand to the next scene; and are the assets fit for their roles?

### Sequence scan

Across each sequence, inspect changes in construction, scale, camera, object, visual and information density, value/color, motion energy, and media mode. Explain meaningful repetition and variation in service of escalation, callbacks, stillness, or payoff. These dimensions prompt editorial judgment; they are not automated diversity quotas.

## Approval-Surface Ergonomics

The user should be able to judge the direction by watching and scanning, not by reading a production document. Default each scene to the target-ratio visual, playback/scrub controls when motion matters, a one-sentence visual thesis, and only the notes required to approve the idea.

Keep these secondary, collapsed, or in separate files until freeze:

- long research/source discussions;
- full Remotion or coding prompts;
- exact easing/transform values;
- dense frame tables;
- exhaustive SFX cue sheets;
- internal implementation parameters;
- provenance/legal notes that do not change the immediate visual decision.

A storyboard may contain deep documentation, but the approval path must remain visually obvious. Do not let planning text, telemetry, or UI chrome compete with the scene itself.

## Status and Precision Discipline

Use separate status concepts:

- **script status**: draft / approved / locked words;
- **voice-performance status**: missing / scratch / final;
- **timing status**: estimated / aligned / frame-locked.

Do not use a single ambiguous label such as `narration locked` to cover all three. If final VO is not aligned, scene times are editorial estimates. Exact frame numbers may be shown only as explicitly provisional blocking aids; do not present them as the production timing contract.

A scene can be design-ready before final VO, but frame-accurate choreography waits for the final performance.

## Evidence-Looking Objects

A newspaper, document, screenshot, memo, archival card, quotation panel, or chart can visually imply primary evidence even when the text is invented. Before approval, classify it.

- **real evidence**: use the sourced artifact or a faithful crop/retypeset with source identity preserved;
- **retypeset excerpt**: clearly identify it as a retypeset/editorial excerpt and do not add a fake masthead, invented article body, quotation, stamp, or date that makes it look recovered;
- **reconstruction/metaphor**: make the reconstruction visibly editorial rather than counterfeit archival evidence.

If the viewer could reasonably mistake a fabricated document for a historical source, the storyboard is not ready for approval.

## Information Budget

Source notes may be rich; the frame should not be. Assign visible text a role: orientation, evidence, relationship label, disclosure, or payoff; accessibility captions remain a distinct function. Preview realistic long caption loads before freeze, including necessary disclosures, at intended viewing size. Repair composition before shrinking readable text. Move unused specifications and supporting provenance out of the canvas, but retain visible disclosures needed for honest representation. Dense technical displays and bold caption-led scenes remain valid when they serve the story.

## Asset Status in Storyboards

Never compress acquisition, usability, taste, and rights into one status. Show the asset ledger's independent fields:

- `origin`: `reused`, `programmatic`, `sourced`, `reconstructed`, or `generated`;
- `technicalStatus`: `candidate`, `available`, or `verified`;
- `editorialStatus`: `pending`, `accepted`, or `rejected`;
- `rightsStatus`: `unresolved`, `needs_review`, `verified`, or `self_created`;
- representation type and claim references where factual meaning is involved.

`generated` describes origin only. It does not imply that the asset is technically verified, editorially accepted, rights-cleared, or suitable as evidence. Likewise, a technically verified asset may still be editorially rejected.

Placeholders are allowed during concept work and review. Resolve identity-critical, evidence-critical, and composition-defining assets early because replacing them can invalidate the design. Before final freeze, every referenced production asset must be technically verified and editorially accepted; otherwise keep the storyboard in review. Rights and representation requirements remain separate gates.

## Motion and Timing Fidelity

Storyboard timing is for editorial judgment. Use semantic anchors and approximate durations until final narration alignment exists.

Preview:

- orientation, semantic trigger, action completion, readable payoff, and transition interval;
- whether the held image still performs its assigned job as narration develops;
- whether essential payoff content is readable before the next competing action;
- whether speech/captions intentionally bridge a cut or instead create an unexplained mismatch;
- whether planned sound or silence supports the attention path;
- whether an unexplained dead tail follows the final meaningful event.

Intentional anticipation and J/L cuts are valid; scene endpoints need not coincide with sentence boundaries. After final VO, conform these semantic windows before frame-accurate implementation. Exact alignment, frame rounding, audio trimming, and render-safe media handling belong to that conformance/implementation handoff, not provisional board estimates.

## Critique and Refinement

Run independent editorial critique before freeze. The critic observes subjects, changes, invariants, and inferred relationships before receiving the director's thesis, then compares them with the assigned contribution. Review clean and realistically captioned versions at the target aspect ratio and actual small consumption size.

Review Scene scope independently using the existing scene findings; add `scopeFindings` for the Film and each declared Sequence and optional Chapter in the existing design/editorial report. Preserve the receipt triad. Reopen affected neighboring scopes after defining changes; harmless easing does not require whole-film redesign.

Resolve, in this order:

1. truthfulness and representation risk;
2. visual thesis and process/mechanism clarity;
3. focal hierarchy and composition;
4. meaningful state progression and pacing;
5. asset fitness and readability;
6. continuity and transition intent;
7. surface treatment.

Repair the responsible decision. Do not conceal a weak mechanism with more text, texture, camera drift, or decorative motion.

Use [critique.md](critique.md) for verdict ownership and [anti-patterns.md](anti-patterns.md) for common failure recovery.

## Freeze Gate

Independent Scene, Sequence, optional Chapter, and Film critics must pass their relevant scopes before freeze. Each scope review records evidence and findings, including actual small-size viewing—not just metadata or deterministic field checks. Freeze only when:

- every scene performs its assigned contribution with readable hierarchy;
- explanatory beats show a perceptible relationship; identification, chronology, evidence, atmosphere, emotion, and purposeful holds are judged by their own jobs;
- identity/evidence-critical assets are accepted for their actual crop/reveal and honestly represented;
- captions and disclosures coexist legibly in realistic preview states at intended viewing size;
- shot score, transition promises, sound intent, and readable payoff windows are resolved;
- progression, escalation, callbacks/repetition, style/emotional rhythm, payoff, and cumulative comprehension work across sequences, chapters, and the whole film;
- unresolved issues are implementation details rather than design questions.

If the user asked to approve the preview, stop at `ready_for_approval` and show it with concise review notes. Freeze only after that approval. Otherwise, continue autonomously through independent review; do not invent a human gate for ordinary directing choices.

Preserve the approved board snapshot separately from as-built notes. Keep the existing compact receipt linking revision/digest, reviewer/context, verdict, blockers, and evidence locations. Put scoped findings in the existing design/editorial reports; do not create a parallel receipt. The generating agent may request review but may not self-award approval.

## Handoff to Remotion

After freeze, the Remotion agent is primarily an implementer. It should preserve:

- scene order and semantic jobs;
- accepted composition and focal hierarchy;
- meaningful visual states;
- asset selection and representation type;
- motion and transition intent;
- readable payoff and handoff states.

It may refine deterministic timing, responsive geometry, easing, compositing, accessibility, and render reliability without reopening design. Reopen only the affected scene and neighboring scopes when a defining change alters their promise; harmless easing does not call for whole-film redesign.

## Change Control After Freeze

Classify proposed changes before editing:

### Implementation refinement

May proceed without returning to storyboard when it preserves the accepted visual meaning. Examples: frame rounding, safer crop bounds, deterministic easing, caption layout, media loading, or small position adjustments.

### Design deviation

Return to the storyboard and re-run editorial critique when a change alters:

- the focal subject or hierarchy;
- the scene mechanism or construction family;
- an accepted hero/evidence asset;
- the number or order of meaningful states;
- the visual meaning of a transition;
- the payoff composition;
- factual or representational interpretation.

Do not let implementation convenience silently redesign a frozen scene.

## Storyboard-to-Render Check

Compare actual output with the frozen revision, not a board rewritten to match implementation. Verify defining relationships through their observable invariants and proof locations; object/state presence alone is insufficient. Use boundary/action clips for transitions and sound, deepest-crop/full-reveal views for assets, and actual readable payoff windows with speech. Record reviewed deviations and route defining changes back through storyboard critique. Final editorial review inspects the mastered draft with captions, disclosures, and mixed sound.
