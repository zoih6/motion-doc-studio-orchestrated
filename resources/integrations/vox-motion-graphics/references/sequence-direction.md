# Film and Sequence Direction

Use this reference after the brief and evidence are understood, before scene-level design. It owns the film/chapter/sequence arc and the full sequence scan; scene construction, asset lifecycle, staging, transitions, timing, sound, and critique remain in their specialized references.

## Plan at the right scale

Think in nested contributions, not a scene quota:

- **Film:** what the viewer is promised, the argument, emotional progression, callbacks, and a conclusion demonstrated by the visuals.
- **Chapter (when useful):** a major argument turn, its evidence burden, and its payoff.
- **Sequence:** a local question/answer progression, escalation, recurring motif, neighboring-scene rhythm, and local payoff.
- **Scene:** one visual contribution; a scene may contain several semantic beats or hold a coherent world across them.
- **Beat:** a semantic event or useful hold; final aligned VO governs its timing.

Shorts collapse chapter and sequence planning into the film. A machine handoff may use one compact sequence, but do not invent chapter breaks or approval pages. A five-minute film usually needs explicit sequence turns within the film; a 10–20-minute film may benefit from chapters that own major argument turns and evidence burdens. These are planning aids, not durations, minimum counts, or scene quotas. Let subject complexity and evidence determine the divisions.

## Direct the progression

Before scenes, state the viewer promise and argument, then write the emotional progression in plain language. For each sequence, decide:

1. What question or uncertainty does the viewer enter with?
2. What evidence or mechanism answers it—and what new question or consequence follows?
3. What changes in the viewer's understanding, stakes, or expectation by the exit?
4. What should be remembered, anticipated, or reinterpreted later?

Escalate by strengthening evidence, consequence, constraint, scale, or emotional meaning—not by increasing visual busyness. Respect evidence boundaries: distinguish what sources establish from inference, reconstruction, and metaphor; never let a callback imply proof the referenced image or sound does not contain.

Let important motifs recur with a changing role or meaning. A callback earns its return by recognizing, contrasting, completing, or recontextualizing an earlier motif; it need not appear in every sequence. Reserve space for the film's conclusion to show the argument's consequence or resolution, not merely restate it. A justified text hero may state a concise thesis, date, number, or final phrase, but it should not replace a visual demonstration when one is possible. Keep the provenance ledger and claim boundaries with their existing evidence/asset owners.

## Establish vocabulary before acquisition

Plan a broad enough visual vocabulary to avoid defaulting to the first familiar stock image or diagram. Name concepts, processes, people, places, and evidence that are actually relevant; allow distinct visual roles or viewpoints where they clarify a subject. Keep **subject identity** (what the thing is) distinct from **composition** (how a shot frames or arranges it), and distinguish both from representation (literal, evidence, reconstruction, metaphor, or abstract). Repeated identity may be right; changing composition alone is not a new subject or mechanism.

For structured handoffs, use `storyboard.direction.vocabulary` entries shaped as `{id, subjectIdentity, visualRole, viewpoint, representation, assetIds: []}`; scenes bind roles with `vocabularyIds`. Plan roles before sourcing; `assetIds` may remain empty until binding. The existing asset ledger alone owns source/acquisition, technical and editorial status, rights, derivation, and provenance. Do not duplicate that ledger here.

## Scan every neighboring scene

Review the sequence in order as a film, not as isolated scene prompts. Compare neighboring scenes across:

- construction family and explanatory mechanism;
- shot composition, scale, viewpoint, and camera behavior;
- focal object or subject;
- visual density and information density;
- color and value;
- motion energy, including deliberate stillness;
- archival, programmatic, and metaphorical representation.

Ask whether a repeated family is doing useful work—comparison, ritual, accumulation, contrast, or payoff—or has become a label-module reflex. Change only what weakens clarity, progression, or attention. No category needs to vary just for variety; there is no diversity quota or ban on repeated construction, locked camera, charts, side profiles, or morphs.

In `storyboard.direction`, `film` carries `viewerPromise`, `argument`, `emotionalProgression`, optional `callbacks`, and `conclusion`. Ordered `sequences` partition the scene order; each carries `id`, `sceneIds`, `purpose`, `payoffTrajectory`, `repetitionAssessment`, and `rhythmIntent`. Rhythm intent may be one line defending a stable scale or evidence hold; it does not mandate variation. Optional chapters partition sequence order and carry `id`, `sequenceIds`, `argumentTurn`, `evidenceBurden`, and `payoff`. Keep scene contributions and beat timing in their existing owners.

## Close the loop

The sequence should leave the viewer with a resolved local answer, a deliberately sharpened question, or a clear launch into the next turn. Across chapters and the film, check that evidence accumulates toward the promised conclusion, callbacks pay off, and quieter evidence or emotional pauses have room to register. A still or quiet scene may be the right contribution; do not manufacture escalation when evidence, tone, or meaning calls for restraint.
