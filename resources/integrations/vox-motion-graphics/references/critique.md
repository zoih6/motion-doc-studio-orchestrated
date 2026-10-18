# Editorial and Technical Critique

## Two Independent Questions

A video may render perfectly and still be visually weak. It may also have a strong storyboard and fail technically.

Keep two explicit verdicts:

- **editorial verdict**: does the visual storytelling work?
- **technical verdict**: is the implementation correct, complete, and safe to render?

Neither verdict substitutes for the other. A publish candidate requires both to pass.

## Verdict Ownership

The agent that creates or implements an artifact may identify risks and request review, but it must not approve its own work or assign itself a production-ready status.

Use an independent critic, reviewer agent, or explicit human review. Independence means a separate review pass that receives the artifact and criteria without being asked to defend the generator's prior choices. Prefer a human or separate agent/model context; a clean critic context on the same model is acceptable when stronger separation is unavailable.

The critic must inspect the artifact itself:

- storyboard review uses the HTML preview and representative states;
- render review uses actual frames and motion previews;
- technical review uses the implementation, timing data, asset ledger, and validation output.

If no independent reviewer is available, mark the relevant verdict `unreviewed`. Continue only as a draft; do not claim approval or production readiness. If the user explicitly owns the approval gate, the critic may mark work `ready_for_approval` but only the user's approval freezes it.

Bind each stage verdict to the artifact revision/digest actually inspected, reviewer/context, unresolved blockers, and evidence locations. Preserve the frozen board separately from as-built notes. A defining change invalidates affected approval; an unchanged artifact does not need redundant review. Fingerprints prove identity, not quality. Draft rendering is allowed to obtain evidence; publish-candidate promotion requires current independent approval and resolved delivery blockers.

## Editorial QA

Editorial QA asks whether the film communicates with clarity, specificity, and deliberate visual direction.

### Observe first, then compare

1. **Without the director's thesis or rationale**, inspect the artifact and describe focal subjects, visible changes, stable references, and inferred relationships. When isolating a visual mechanism, begin without narration/accessibility captions; retain meaningful on-canvas evidence and labels. Record what is actually observable, not the most charitable explanation.
2. **Then receive the intended contribution** and compare it with those observations. Review the complete accessible master with narration, captions, disclosures, and mixed sound. Judge the assigned job—not whether pictures encode every word, proper name, or historical fact.

A timeline may correctly show order but fail a claim about cumulative pressure. A portrait may establish identity while narration supplies the name. Static evidence, testimony, atmosphere, symbolism, and purposeful silence remain valid contributions.

### Multilevel scope review

Before freeze, obtain independent Scene and Sequence critiques, plus Chapter critique where chapters exist, and a Film-level critique. Keep findings in the existing design/editorial report: its existing scene findings retain per-scene verdicts and viewing-size evidence; add `scopeFindings` for the film and each declared sequence/chapter, preserving the receipt triad. Each scope finding records `{scopeType, scopeId, status, finding}`; scope type is `film`, `sequence`, or `chapter`, and status is `approve`, `revise`, or `redesign`.

- Scene findings cover each scene's contribution and perceptible relationship.
- Sequence findings cover local rhythm, construction, repetition, handoffs, and payoff.
- Chapter findings cover argument turn, evidence burden, and payoff.
- Film findings cover narrative progression, escalation, callbacks/repetition, style and emotional rhythm, payoff, and cumulative comprehension.

Each scene finding includes `viewingSizeEvidence: [{widthPx, heightPx, distance, observation, proofRef, proofSha256}]`, with positive pixel dimensions for the actual video/player window, not the device display. For example, inspect a portrait short at 360×640; landscape work may include phone-player 390×219 and desktop-player 960×540 views. Record every relevant view. `proofRef` names a local file relative to the project manifest; `proofSha256` binds its inspected bytes inside the artifact-bound report. The critic must confirm the proof shows that report's frozen board or current master; a hash cannot infer this relationship or prove readability. Preserve the proof with the release, and independently refresh affected review if it changes. Simplify or recompose unreadable content rather than shrinking it.

Reopen the changed scope and affected neighbors after a defining change. A harmless easing adjustment does not trigger whole-film redesign.

### Review dimensions

- **Visual contribution:** can the assigned relationship, identification, evidence, or emotional job be described from observed image rather than director explanation?
- **Focal hierarchy:** is one element dominant in each meaningful state, and does attention move intentionally?
- **Contribution clarity:** does the visual perform its assigned explanatory, identification, emotional, chronological, or evidence job rather than merely naming related objects?
- **State progression:** when the intended contribution changes, does the visual respond or sustain a justified useful hold? Stillness is valid when it satisfies the assigned job; do not require a fictional state change.
- **Payoff:** does the scene land on a readable consequence, often with a simpler composition than the buildup?
- **Pacing:** are holds purposeful, actions readable, and transitions timed around semantic resolution?
- **Continuity:** does attention hand off through position, direction, object, line, color, or scale?
- **Asset fitness:** do selected assets support required crop, motion, identity, and tone?
- **Text hierarchy:** do labels, evidence, disclosures, payoff text, and accessibility captions remain useful and readable together in clean/captioned reviews?
- **Style cohesion:** do continuity tokens create one film without forcing every scene into the same layout?
- **Evidence honesty:** are literal, evidence, reconstruction, metaphor, and abstract treatments unmistakable and claim-safe?
- **Review ergonomics:** can the user judge the scene without implementation prompts, dense telemetry, or long frame tables?
- **Status coherence:** are script lock, final voice status, and timing precision described consistently?
- **Information budget:** does every on-canvas fact/label advance orientation, proof, or payoff?
- **Film progression:** do escalation, callbacks and repetition, style/emotional rhythm, payoff, and cumulative comprehension work across the film?

### Hard blockers at the storyboard gate

Do not mark `ready_for_approval` while any of these remain:

- a fabricated or generated evidence-looking document could be mistaken for an authentic source;
- an identity/evidence-critical asset is presented more confidently than its provenance or representation allows;
- the board claims final/frame-locked timing while final VO alignment is still provisional;
- contradictory stage/status labels make it unclear what is actually approved;
- a production prompt or implementation detail is carrying the design because the visual preview itself is not understandable.

### Editorial verdicts

- `approve`: visual decisions are ready to freeze or publish at this stage;
- `revise`: the concept works but named issues require repair;
- `redesign`: the mechanism, hierarchy, or representation is fundamentally weak;
- `unreviewed`: no independent editorial review occurred.

Route issues by cause, naming symptom, scene/state, observed evidence, and smallest useful repair:

| Finding | Route |
|---|---|
| Wrong inferred relationship for the assigned job | `redesign`: concept/storyboard |
| Correct relationship, weak visibility or staging | `revise`: composition/choreography |
| Correct frozen plan, missing label/action/cue or broken crop/timing | Implementation repair; redesign only if the plan itself changes |
| Aesthetic disagreement without functional harm | Taste note, not blocker |

Restore missing execution before judging whether it fixes the idea; restoring labels cannot rescue an unrelated mechanism. Do not reject cards, timelines, bold captions, static evidence, hard cuts, or silence on style preference alone.

## Technical QA

Technical QA asks whether the accepted design has been implemented deterministically and without delivery defects.

### Review dimensions

- composition renders at the declared size, frame rate, and duration;
- scene, narration, caption, transition, and final-hold timing reconcile;
- no dead tail or early cut remains unexplained;
- render-visible motion is frame-driven and deterministic;
- assets load reliably and use supported formats/paths;
- required provenance, rights, and claim references exist;
- text and critical subjects remain inside the named platform safe area;
- captions fit, remain legible, and do not collide with critical art;
- masks, overlays, textures, and transforms preserve intended geometry;
- all expected data, labels, and final values remain visible at settle;
- audio files, channels, sync points, and final mix are present and valid;
- no runtime, typecheck, lint, schema, or render errors remain;
- representative output matches the frozen storyboard or records an approved deviation.

### Technical verdicts

- `pass`: delivery checks are satisfied;
- `fail`: a blocking defect exists;
- `blocked`: required input, tool, credential, or evidence is unavailable;
- `unreviewed`: no independent technical review occurred.

Do not convert technical success into an editorial approval. “It renders” is not evidence that the film communicates well.

## Stage-Specific Review

### Storyboard gate

Run editorial QA only. Technical notes may flag feasibility, but they should not overrule a strong concept until the implementation risk is real and specific.

### Implementation gate

Run technical QA first so broken output does not waste editorial review. Then compare representative renders with the frozen storyboard.

### Final gate

Run both verdicts on the mastered output, using the issue-routing table above. Reopen only the responsible layer and its affected approval; do not rerun unrelated design decisions to repair a missing implementation detail.

## Critique Evidence

Use the smallest evidence set that proves the verdict:

- entry, meaningful action, payoff, and exit frames at actual small consumption size;
- boundary/action clips for camera, transition, timing, and audible cue promises;
- clean and realistically captioned views, including disclosures, at target ratio and viewing size;
- final alignment plus orientation/trigger/completion/readable-payoff/transition windows, checked with speech;
- deepest asset crop and complete-reveal payoff where those roles are promised;
- frozen revision comparison and observable invariant/proof location for defining relationships;
- before/after comparison for repairs, tied to the mastered output actually reviewed.

Deterministic fields and hashes establish contract coverage or artifact identity; neither proves perception, independence, quality, readability, factual truth, or sound. A final frame cannot prove motion quality, and source code cannot prove rendered composition. Final multi-level editorial and technical review uses the actual mastered, captioned/audio artifact; preserve the inspected hashes and never change them to simulate review.

## Repair Discipline

Repair the responsible layer; do not march through unrelated polish. Resolve truthfulness and wrong concepts first, then staging/readability, then surface treatment. An implementation omission in an accepted design goes directly to implementation repair. Verify the repaired artifact rather than relying on updated notes.

After two failed low-level repairs to the same editorial problem, return to the storyboard and redesign. If one redesign still cannot produce a clearly better direction, escalate the smallest meaningful choice instead of looping. Do not stack effects or parameters around a weak concept.

