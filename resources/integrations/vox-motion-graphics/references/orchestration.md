# Autonomous Orchestration

Use this reference when the workflow is expected to run with little supervision across research, storyboard, critique, Remotion, audio, QA, and render.

## Default ownership

The director should make ordinary creative decisions without asking the user to choose layouts, easing, transition types, scene count, or coordinates.

Pause only when:

- a factual uncertainty changes the claim;
- rights, brand, identity, or material cost needs user ownership;
- required credentials/assets/tools are unavailable;
- the user explicitly requested an approval gate;
- repeated repair no longer has a clear best next action.

## Stage graph

`brief/evidence -> concepts and shot scores -> storyboard with caption/sound intent -> independent design review -> freeze -> final VO/alignment -> timing conformance -> implementation -> mastered draft -> technical and independent editorial review -> delivery`

Keep stage outputs small. The HTML storyboard is the creative source of truth; freeze an immutable snapshot and keep as-built timing, cue decisions, and implementation notes separately. Never overwrite the approved board with a description of what happened to get implemented. Plan caption composition and sound intent before freeze; source/mix finishing audio and produce the accessible master before final review. Draft renders are permitted whenever inspection needs them; publication, not rendering, is gated.

## Bounded iteration

Avoid endless agent loops.

For a single editorial problem:

1. identify the symptom and responsible design layer;
2. make the smallest plausible repair;
3. review the changed evidence;
4. if the same problem survives two low-level repair attempts, stop patching and redesign the responsible storyboard decision;
5. if a redesign still cannot produce a clear improvement, escalate to the user with the smallest meaningful choice.

Do not generate many cosmetic variants after a concept is already clearly weaker.

## Approval gates

When the user wants approval before implementation:

- the critic may return `ready_for_approval`;
- show the browser preview plus a concise critic summary;
- do not start final Remotion implementation until approval;
- after approval, freeze the defining visual relationships and treat later redesign as change control.

Unless the user explicitly reserves an approval gate, the director continues autonomously and an independent critic may approve the freeze. Do not turn ordinary creative decisions into new user approval requests.

## Critic independence

A useful independent critic is a separate review pass that receives the artifact and evaluation criteria without being instructed to defend the generator's decisions. Prefer, in order:

1. human review;
2. separate model/agent context;
3. same model in a clean critic context with no hidden chain from generation.

A second message in the same implementation context that merely asks “is this good?” is not strong independence.

The critic first observes focal subjects, changes, stable references, and inferred relationships without the director's explanation; then compares with the intended job and reviews the accessible mastered output. Missing execution goes to implementation repair; an incorrect visual relationship returns to directing. An aesthetic preference without functional harm is not a blocker.

## Deterministic publish gate

Run from the skill directory:

```sh
python tools/validate_project.py /project/project-manifest.json --stage draft
python tools/validate_project.py /project/project-manifest.json --stage publish --json
```

`draft` is the default and preserves provisional manifests and preview rendering. A draft pass is not release approval. `publish` requires a populated frozen board, as-built scene/state metadata, accepted/verified used assets, resolved rights/provenance, and the receipt below. The validator's docstring describes the base manifest; add `storyboard.preview.path`, `masterFile`, and `reviewReceipt`:

```json
{
  "storyboard": {"preview": {"path": "frozen/board.html"}},
  "masterFile": "output/master.mp4",
  "reviewReceipt": "reviews/release.json"
}
```

These are additions to the complete manifest, not a standalone valid manifest. The receipt follows `schemas/review-receipt.schema.json`:

```json
{
  "producerContext": "director-and-implementation-session",
  "board": {"file": "frozen/board.html", "sha256": "<64 lowercase hex characters>"},
  "master": {"file": "output/master.mp4", "sha256": "<64 lowercase hex characters>"},
  "reviews": {
    "design": {"file": "reviews/design.json", "sha256": "<64 lowercase hex characters>"},
    "editorial": {"file": "reviews/editorial.json", "sha256": "<64 lowercase hex characters>"},
    "technical": {"file": "reviews/technical.json", "sha256": "<64 lowercase hex characters>"}
  }
}
```

**Every file path is relative to the project manifest directory, including paths inside the receipt and review references—not relative to the receipt directory.** Use a self-contained frozen HTML or a bundled board archive when linked files carry defining content. The validator hashes the listed file bytes only; it does not recursively collect HTML dependencies.

Design and final editorial files use `editorial-qa-report.schema.json`; technical uses `technical-qa-report.schema.json`. For publish, each report additionally requires `reviewContext`, `boardSha256`, and `blockers: []`. Final editorial and technical also require `masterSha256`. Design verdict is `overallStatus: "approve"`; final editorial is `"publish_candidate"`; technical is `"pass"`. Design and editorial require `critic`, `independent: true`, a `reviewContext` different from `producerContext`, and affirmative checks for every board scene. Technical checks must pass or explicitly be not applicable with evidence. Report hashes in the receipt bind the actual review files; report artifact hashes must match the receipt and actual frozen board/master. Missing reviews, negative scene verdicts/checks, blockers, or changed bytes fail.

Design/editorial `renderRefs` must identify at least one existing local review artifact or HTTP(S) locator. Local paths resolve from the manifest directory; remote locators are not fetched by the validator. A verdict without these evidence locations is incomplete.

Keep the existing board `freezeEvidence` as an index of the design review, not a substitute for it. Obtain the review before recording its digest. If board content changes, independently review the new board and resulting master; if only the master changes, refresh final reviews without repeating an unchanged design review. Never rewrite a digest to manufacture approval. Hash equality establishes identity, not quality, reviewer authenticity, or actual independence; independent artifact inspection remains mandatory.

Design and final editorial reports retain their verdicts and scene findings, add `scopeFindings` for Film and each declared Sequence/Chapter, and carry each scene's viewing-size proof as `{widthPx, heightPx, distance, observation, proofRef, proofSha256}`. Local proof files resolve from the manifest directory and their inspected bytes are hash-bound inside the report. Critics must confirm they depict the reviewed board/master; hashes cannot infer that relationship. Scoped review passes before freeze and again on the mastered, captioned/audio output. Defining changes reopen affected scopes; never rewrite digests to simulate approval.

Draft migration may retain legacy storyboard metadata. v0.10 publication requires the new direction hierarchy and complete scoped review evidence, including real independent re-review of the actual artifact. Updating fields or regenerating hashes cannot stand in for review.

Used assets are the union of board/state/implementation `assetIds`, assets bound to vocabulary roles referenced by scene `vocabularyIds`, and ledger entries with nonempty `sceneIds`. Unused candidates may retain unresolved rights. Used assets must be accepted/verified, have resolved `rightsStatus`, a `sourceUri` (HTTP(S) locator or existing local source/creation record), and `rightsEvidence`; verified rights also require `license`. Role descriptions need not be identical strings; editorial review verifies fit against the actual shot. Rights text is a traceable research record, not machine legal clearance.

For `representationType: "evidence"`, require `sourceUri` and `claimIds`. Include the existing claim-set shape as manifest `claimSet`; each referenced claim needs verified claim text and `sourceRefs` resolving to source records with an HTTP(S) `url` or existing local file. The validator checks linkage/local existence, not remote retrieval or factual truth. Generated/reconstructed assets cannot claim `evidence`; honest reconstructions remain valid as `reconstruction`, and sourced/first-party documentary evidence and supported programmatic charts remain valid.

## Compact conformance handoff

- Optional storyboard scene `shotScore` records `composition`, `objectAction`, `camera`, `attention`, `rhythm`, `sound`, and `exit`. It hands staging to the implementer; locked camera and deliberate silence are valid values.
- Optional `relationshipInvariants` records only defining promises as `{id, observable, proofRef}`. The critic consumes `proofRef` (frame, boundary clip, or timecode location), comparing the observable against the frozen promise. These fields do not assert that matching IDs prove visible continuity.
- After final alignment, optional frame-spec microbeat `semanticTiming` carries `phrase`, `orientationStartSec`, `triggerSec`, `actionCompleteSec`, `readableStartSec`, `readableEndSec`, `transitionStartSec`, and `transitionEndSec`. Copy the same microbeats into validator manifest `scenes` for checking; all times are scene-local seconds. Orientation ≤ trigger ≤ action completion ≤ transition end; readable start < readable end ≤ transition end; transition start ≤ transition end; all times stay inside the scene. Readability may overlap action and transition: do not wait for every easing curve to finish before counting actual reading time. The trigger is the intended visual semantic event, not necessarily the first spoken word; justify anticipation/J/L-cuts during review. No fixed hold length is imposed.
- Frame-spec/manifest scene `sfxEvents` may record `disposition: implemented|replaced|omitted`; replacements/omissions require `decisionReason`. Retain the planned cue in the frozen board, record the as-built choice separately, and review intentional silence or replacement rather than silently dropping sound.

The validator checks timing ranges/order and cue-decision completeness only. It cannot infer actual readability, a perceptible relationship, factual honesty, or audible sound from fields. Review boundary clips, clean and captioned compositions at viewing size, and the mastered sound/VO together.

The universal editorial job check is `visualJobSatisfied`: judge the assigned job, not a mandatory state change. Stillness is explicitly valid when it performs its intended job; explanatory relationship changes require perceptible evidence, while identification, evidence, chronology, atmosphere, and emotion are judged on their own terms. Schema or manifest fields cannot establish perception.


## Safe parallelism

Parallelize work only after shared decisions are stable.

Good candidates:

- independent research/evidence collection;
- asset sourcing/generation for already-defined roles;
- reusable primitive implementation;
- diagnostic frame extraction;
- independent QA dimensions.

Do not parallelize several agents that can silently redefine the same scene thesis, storyboard, or timing contract. Conflicting proposals remain candidates until one is explicitly retained.

## Resume and interruption safety

Long workflows should be restartable after an interrupted agent session.

Persist only durable stage state, for example:

- current stage;
- approved/frozen storyboard path and revision;
- unresolved blockers;
- accepted asset identities;
- final VO/alignment path;
- last QA verdicts;
- requested next action.

Do not serialize the entire reasoning transcript as production state. On resume, reconstruct context from approved artifacts and concise stage metadata.

## Change control after freeze

Changes that alter the thesis, focal hierarchy, defining relationship, hero/evidence asset identity, or transition logic return to storyboard review.

Changes limited to easing, interpolation, micro-timing, compositing, performance, or bounded layout repair may remain in implementation if they preserve the approved visual argument.

## Completion

A run is complete when:

- requested approval gates have been satisfied;
- factual/rights blockers are resolved for publication (otherwise deliver only a clearly labeled review draft);
- implementation matches frozen direction, with reviewed as-built deviations recorded separately;
- technical QA passes on the actual master;
- independent editorial review approves that same master, or the output remains `needs_review`;
- requested render/output exists.

Do not continue polishing merely because another effect or variant is possible.
