# v0.9 Behavioral Regression Prompts

Run these across target coding agents without supplying the expectations as benchmark answers. Inspect decisions and artifacts, not exact wording or completed fields. These are proposed evaluation cases, not evidence of measured creative improvement; use the held-out procedure in [vague-autopilot-prompts.md](vague-autopilot-prompts.md).

## 1. Causal economics

“Create a 55-second vertical explainer about why high interest rates can hurt a government even when it never misses a payment.”

Expect: claims remain honest; a visible relationship explains the burden without prescribing one diagram; HTML storyboard precedes Remotion; final VO governs semantic timing and reading windows.

## 2. Technical process

“Explain how a heat pump moves heat for a general audience. Make the visuals do the explaining.”

Expect: connected state/flow visualization; no repeated specification cards; each narration turn changes the system or justifies a hold.

## 3. Archival history

“Create a 50-second short about the invention of the shipping container using supplied archival photos.”

Expect: photos provide identity/evidence; static inspection remains valid when that is the job; process claims get an explanatory relationship rather than wallpaper; reconstructions cannot masquerade as evidence; asset states remain explicit.

## 4. Product/UI

“Create a polished 40-second video showing how comments become assigned tasks in a fictional collaboration product.”

Expect: clean UI/process world rather than forced paper treatment; storyboard resolves state progression; implementation preserves those states.

## 5. Quiet product film

“Create a 30-second premium minimal film for a fictional mechanical pencil. No narration.”

Expect: the workflow allows deliberate stillness and a lightweight storyboard; no forced documentary grammar, captions, or constant structural changes.

## 6. Data evidence

“Create a 35-second video comparing electricity sources using the attached dataset without making it feel like a classroom chart.”

Expect: values remain truthful; hierarchy and object-as-data alternatives are explored; technical and editorial QA remain separate.

## 7. Reference learning

Provide a reference and ask: “Learn the creative grammar, then create an unrelated video.”

Expect: findings are classified per observation as creator DNA, technique, surface style, or benchmark-specific; exact layouts and assets are not copied.

## 8. Timing defect

“The VO ends at 41.2s, captions at 41.0s, and composition at 49s. The ending has no intended silence.”

Expect: deterministic QA reports a dead tail; the agent does not add a music fade or visual drift to conceal it.

## 9. Storyboard freeze drift

“The frozen storyboard shows one object passing through three stages. The Remotion version uses three independent cards because it was easier to build.”

Expect: implementation is rejected as design drift and returns to storyboard/change control rather than being called equivalent.

## 10. Asset lifecycle

“The generated hero PNG exists and has alpha, but nobody has reviewed its composition or provenance.”

Expect: origin is generated, technical status may be verified, editorial status remains pending, and the asset is not treated as accepted.

## Global checks

- The user is not asked to choose layout, easing, transition, or coordinates.
- Storyboard fidelity matches uncertainty: lightweight for simple scenes, playable for complex transitions/processes.
- Editorial QA reviews rendered/storyboard evidence; technical checks do not self-award creative approval.
- No Kodak/Concorde facts, palette, frame rate, timings, surface treatment, or mandatory hero continuity become defaults.

## 11. Conflicting creative metadata

“The approved HTML storyboard shows one continuous process, but an older JSON handoff describes three cards.”

Expect: HTML/review evidence is treated as the creative authority; the agent flags drift and reconciles metadata instead of silently implementing the stale JSON.

## 12. Human approval gate

“Run automatically, but show me the polished storyboard before you build Remotion.”

Expect: research, concepts, storyboard, and independent critique run automatically; the workflow stops at `ready_for_approval`; Remotion does not start until the user approves.

## 13. Long-form scene economy

“Create a five-minute explainer. One chapter explains the same mechanism for 35 seconds.”

Expect: the chapter may remain one coherent scene/world while using multiple semantic states or microbeats; the agent does not redesign the entire visual every few seconds or hold one unchanged frame for the whole chapter.


## 14. Fake newspaper temptation

“Make the 2012 bankruptcy beat feel historical. We know the filing date but do not have a newspaper scan. Invent a period newspaper page around the real event.”

Expect: refuses to masquerade invented layout/copy as primary evidence; uses a sourced artifact, a real-source retypeset excerpt, or a clearly editorial date/headline card.

## 15. Script locked, voice missing

“The script is approved, but VO will be recorded tomorrow. Build the storyboard now and give me exact final frame numbers.”

Expect: storyboard proceeds, but timing remains explicitly estimated; script lock, voice lock, and timing lock are kept separate; authoritative frame choreography waits for aligned final VO.

## 16. Research-rich hardware scene

“We have fifteen verified specifications for this machine. Put all of them around the product so it feels technical.”

Expect: selects only facts that orient/prove/pay off the beat; remaining specs stay in notes; the scene does not become a telemetry dashboard.

## 17. Compressed duration counter

“Show ‘23 seconds to record’ by counting 00→23 in 0.2 seconds and play a click for every number.”

Expect: preserves the 23-second fact but rejects imperceptible per-unit click spam and any false one-to-one time implication; uses grouped/rolling motion and a readable landing.

## 18. Named style shorthand

“Analyze Vox, Johnny Harris, and MoSidd, then write the production prompt.”

Expect: analysis may name references, but production direction translates them into concrete observable grammar instead of using creator names as the main style instruction.

## v0.9 matched probes

Run the failure and valid-counterexample variants; a critic that rejects both is not passing.

| Probe prompt / supplied artifact | Expected distinction |
|---|---|
| “Explain why printer cartridges generate repeat purchases.” Supply a concept that only pans to a second cartridge; contrast with a beat whose sole job is identifying cartridge types. | For recurrence, compare two materially different mechanisms and select autonomously using inference/before/operation/after/invariant/factual limit. Identification may correctly use discovery alone. |
| “Show how two pressures jointly constrain a housing project.” Supply a dates-only timeline; then assign the same timeline the job of showing event order. | Wrong relationship for combined constraint → concept redesign. Correct chronology → accept; no universal timeline ban. |
| “Stage artifact inspection, reservoir depletion, then an emotional aftermath.” | Joint score separates camera discovery from object action and supports film-level cadence. A locked view, hard cut, or silence may be chosen; generic push-ins are not sufficient explanation or a required repair. |
| Supply a correct reservoir mechanism with overlapping demand labels, long captions, and disclosure; also a sparse bold-caption-led warning scene. | First needs staging/composition repair in clean and captioned views, not a new concept or tiny captions. Bold prominence alone is not failure. |
| Supply two performances of identical words at different pacing, stale round-number scene windows, and an ending that becomes readable 0.08 seconds before the cut; include a purposeful L-cut. | Reconform semantic events and actual readable windows with speech. Flag stale timing/unreadable payoff; accept the purposeful overlap. A metadata duration alone cannot pass. |
| Supply one low-resolution archive used at an unreadable deep crop and at a readable wide view; a complete-object reveal that hides essential parts; a self-created fake primary document; a clearly disclosed reconstruction. | Accept by actual role, not source dimensions. Reject the failed crop/reveal and false evidence; permit the wider archive and honest reconstruction, subject to rights. |
| Against a frozen board, remove a relationship label, jump a match transform, and drop a planned sound bridge. Also supply reviewed hard-cut and silence replacements. | Route missing promises to implementation repair using boundary clips and mastered sound; accept reviewed replacements. Do not infer fidelity from asset/state inventory. |
| Give a critic clean pictures first, then the director's thesis and complete accessible master. Include a portrait whose name is supplied only in narration. | Critic records observed relationships before intent, compares assigned contribution, and does not require the portrait to visually encode the name. |
| Supply draft output with no independent review; then a reviewed master receipt followed by a changed master; then the unchanged reviewed artifact. | Draft rendering remains allowed. Missing/stale approval or unresolved delivery rights blocks publication; unchanged reviewed output does not trigger redundant review. |

For each critique record **wrong concept**, **weak staging**, **implementation defect**, or **taste**, plus observable evidence and the smallest responsible repair. Do not count a correct category label without artifact inspection as success. Technical/gate compliance and creative directing quality are separate outcomes.

## v0.10 direction probes

These are behavioral evaluation cases, not measured proof of creative improvement. Inspect the proposed direction and rendered/storyboard evidence; do not score source strings, field presence, or a checklist alone.

| Prompt / supplied context | Expected distinction |
|---|---|
| “Make a 55-second short about why a neighborhood grocery keeps running out of fresh food.” | Autonomously shape a compact film-level question, evidence progression, and demonstrated conclusion. Collapse chapter/sequence planning rather than inventing chapters or scene quotas; keep claims and any metaphor honest. |
| “Make a five-minute explainer about how a city gets drinking water during a drought.” | Plan explicit sequence turns and escalation appropriate to the evidence, with a local question/payoff and a full neighboring-scene rhythm scan. Do not make arbitrary scene or chapter counts. |
| “Make a 15-minute film about how public libraries changed as communities moved online.” | Consider chapters only where major argument/evidence turns justify them; plan callbacks and an earned visual conclusion. Do not treat the short-form structure as five-minute segments or fill time with repeated modules. |
| Supply neighboring scenes that all use the same diagram family: one pair compares genuinely equivalent systems; a later run repeats identical label cards for unrelated ideas. | Preserve the justified comparison; diagnose monotonous label modules by their actual sequence contribution, not a blanket family ban or uniqueness quota. |
| “Hold on an unchanging, legible archival ledger while the narrator reads the one entry that proves the disputed date.” | Accept purposeful evidence stillness and sufficient reading space; do not demand movement or a fictional state delta. |
| Supply a rising evidence sequence whose planned ending merely repeats a headline; ask for a dramatic conclusion. | Direct a payoff that visually demonstrates the established consequence or recontextualizes an earned motif; concise text may be a justified hero, not a substitute for available visual proof. |
| “Create an engaging short about a local flood-control system,” with only a few reliable facts and no usable local photography. | Broaden the vocabulary through truthful subject roles/viewpoints and honest programmatic or disclosed reconstructed imagery; do not invent local identity/evidence or pretend arbitrary composition changes create breadth. |
| Request a scene handoff followed by a sequence handoff for a long film, after direction is frozen. | Keep each packet bounded to its assigned scene/sequence, frozen revision, relevant evidence/assets/style/timing, and adjacent handoff context. Do not duplicate the full history or invent a router, compiler, or packet contract. |

## Shot vocabulary probes

Run both unsupported/conflicting and feasible variants. Inspect the chosen behavior, prerequisites, fallback and planned playback proof; identifying a technique name alone is not a pass. Planning-only responses do not establish rendered fidelity.

| Prompt / supplied context | Expected distinction |
|---|---|
| “Reveal the scale of this building with a pull-back.” Supply only a tightly cropped doorway photo; contrast with a supported wide photograph containing the same doorway and surrounding building. | Do not invent unseen architectural evidence or merely shrink the photo against empty space. Choose a supported wider reveal or an honest alternative; preserve the starting subject and make the added context legible. |
| “Orbit this product to show its back.” Supply one front-view PNG; contrast with a suitable 3D asset whose back is known. Also ask for a flat graphic spin. | Reject unsupported viewpoint claims for the PNG; distinguish camera orbit, fixed-camera object rotation and in-plane graphic rotation. Accept feasible geometry or honest graphic treatment without claiming unseen form. |
| “Keep the subject the same size while the warehouse stretches behind it.” Supply depth-aware scene geometry; contrast with one flat poster uniformly scaled. | Select coupled camera travel/focal-length change for a true dolly zoom; reject uniform scaling as equivalent. An explicit illustrative layered approximation or a simpler camera choice is valid when its limits are honest. |
| “Keep the camera locked and whip-pan on the same beat.” Contrast with a rapid camera-style sweep between supported views and a sliding UI panel. | Resolve the contradictory instructions instead of appending both. Distinguish whip-pan from panel translation; require edge coverage, a clear focal landing and readable states. A straight cut remains valid. |
| “Hold this ledger so the narrator can read the evidence, then let the outgoing sentence finish over the next picture.” Contrast with a new speaker's audio starting before their picture and with overlapping unintelligible dialogue. | Accept purposeful camera/evidence stillness and distinguish L-cut from J-cut by the actual audio/picture order. Preserve speech, captions and source identity; reject a confusing bridge, not sound overlap in general. |

No passing score on these prompts establishes improved model creativity; that requires the held-out evaluation procedure in [vague-autopilot-prompts.md](vague-autopilot-prompts.md).
