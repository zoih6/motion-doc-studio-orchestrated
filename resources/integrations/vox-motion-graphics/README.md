# v0.10 — Visual Invention & Long-Form Direction

`vox-motion-graphics` directs and implements editorial motion-graphics videos without requiring the user to storyboard or speak motion-design jargon.

v0.10 adds film/chapter/sequence direction above the existing storyboard-first scene workflow. Conditional visual state deltas, pre-acquisition asset vocabulary, mechanism concept search and independent multi-level critique address inventive storytelling and cumulative rhythm—not just polished frames. Shorts collapse the hierarchy; longer explainers/documentaries use it for evidence, motifs, escalation, callbacks and payoff.

Read [the upgrade architecture and audit](V0.10-DESIGN-NOTES.md) and [the changelog](CHANGELOG.md). Production lessons motivate general contracts, not a Concorde template or bans on charts, asset reuse, side profiles, stillness or hard cuts. Measured creative improvement remains unproven; [behavioral evaluations](tests/vague-autopilot-prompts.md) distinguish that question from deterministic validation.

Start with `SKILL.md`. Load only the references linked for the current production stage.

## Package shape

- `SKILL.md` — workflow, routing, gates, and non-negotiables
- `CHANGELOG.md` — complete release history; version-specific publication notes live on [GitHub Releases](https://github.com/sfsajid91/vox-motion-graphics/releases)
- `references/` — focused directing, reference-analysis, orchestration, and implementation guidance
- `references/sequence-direction.md` — hierarchy, visual vocabulary, neighboring-scene rhythm and cumulative payoff
- `references/implementation-packets.md` — bounded future ScenePacket/SequencePacket handoffs; no model router
- `examples/positive/` and `examples/negative/` — corrected outcomes and instructive failures
- `schemas/` — core handoff contracts plus optional tuning/reference contracts
- `tools/validate_project.py` — deterministic timing, asset, storyboard, implementation, and publication-evidence checks
- `tools/make_contact_sheet.py` — representative-frame contact sheets
- `tools/halftone.py` — optional image treatment, not a default style

## Validation

From this directory:

```bash
python tests/test_schemas.py
python -m unittest discover -s tests -p 'test_*.py'
python tools/validate_project.py --help
python tools/validate_project.py path/to/project-manifest.json --stage draft
python tools/validate_project.py path/to/project-manifest.json --stage publish
```

The first two commands run the repository tests. The manifest commands operate on a production's real artifacts; use `--help` and [orchestration](references/orchestration.md) for the publication receipt contract. Draft is the default and does not confer publication approval.

Legacy manifests remain usable for drafts. Publication under v0.10 requires the new direction/scene contracts and independent scene, sequence, chapter (when declared) and whole-film review with realistic viewing-size evidence. The existing board/master/report receipt remains the release binding. Migrate and review the actual artifacts; never refresh digests to fabricate approval.

The validator checks metadata, references, and artifact identity, not visual relationships, audible cues, source truth, reviewer honesty, or aesthetic quality. Independent review must inspect the actual mastered output. Behavioral prompts are development evaluations, not deterministic proof that a model follows the skill.
