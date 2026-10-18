# Bounded Implementation Packets

Use a `ScenePacket` or `SequencePacket` after the storyboard is frozen and final timing is aligned. A packet narrows implementation context to one scene or one ordered sequence; it is not a router, compiler, alternate source of truth, or publication approval. The frozen board remains authoritative. Do not send the entire skill as mandatory context for every scene: include relevant reference excerpts and local evidence only.

## Packet bounds

Both packet kinds carry the same bounded fields:

- `projectId`, `packetType`, and `frozenBoard: {file, sha256}` identify the project and exact frozen revision.
- `scope: {id, sceneIds}` bounds ownership. A `ScenePacket` contains exactly one scene ID; a `SequencePacket` contains one or more ordered scene IDs. A legitimate one-scene sequence needs no artificial second scene.
- `context: {objective, constraints?}` states the assigned outcome and limited constraints, not a duplicate creative brief.
- `artifacts` and `evidence` are required arrays of relevant project-manifest-relative `{file, sha256, purpose}` references. Include local claim/rights sources and expected proof for defining relationships/payoffs only when relevant to this scope; use `[]` when none apply.
- `assets` is a required array of relevant `{id, role, file, purpose}` bindings from the existing asset ledger. Do not create a parallel asset catalog; use `[]` when no asset binding applies, but every supplied binding has all four fields. An empty array does not waive evidence or accepted assets needed for the assigned scene/sequence.
- `style: {visualLanguage, palette?, typography?}` provides the applicable style boundary.
- `timing: {startSec, durationSec, beats?}` uses the agreed aligned timing convention; each beat has `{id, startSec, endSec}` and, when present, stays within `durationSec`. Do not rewrite timing around provisional estimates.
- `neighbors` is required and provides optional `previous` and `next` objects `{sceneId, handoff}` when adjacent handoff boundaries matter.

Use the packet to select relevant references and excerpts plus local claims, rights/assets, approved implementation decisions, frozen revision/hash, and style/timing/neighbor boundaries. Keep each excerpt relevant; do not copy the entire reference catalog into every packet.

## Example

This illustrative SequencePacket shows the bounded payload. Replace symbolic hash notes with digests computed from the actual frozen/referenced file bytes before validation; placeholders below are not valid approval evidence.

```json
{
  "projectId": "film-example",
  "packetType": "SequencePacket",
  "frozenBoard": {
    "file": "frozen/storyboard.html",
    "sha256": "<digest of actual frozen board bytes>"
  },
  "scope": {
    "id": "seq-pressure",
    "sceneIds": ["scene-03", "scene-04"]
  },
  "context": {
    "objective": "Show how the local constraint compounds, then hand attention to the consequence.",
    "constraints": ["Keep the established visual vocabulary", "Preserve the approved payoff and handoff"]
  },
  "artifacts": [
    {
      "file": "frozen/sequence-direction.json",
      "sha256": "<digest of actual direction bytes>",
      "purpose": "Sequence intent and selected mechanism"
    },
    {
      "file": "references/sequence-direction.md",
      "sha256": "<digest of actual reference bytes>",
      "purpose": "Relevant excerpt: sequence rhythm scan"
    }
  ],
  "evidence": [
    {
      "file": "evidence/claim-support.pdf",
      "sha256": "<digest of actual evidence bytes>",
      "purpose": "Supports the factual limit used in this sequence"
    }
  ],
  "assets": [
    {
      "id": "asset-ledger-17",
      "role": "constraint marker",
      "file": "public/assets/marker.png",
      "purpose": "Accepted asset for the scene's mechanism"
    }
  ],
  "style": {
    "visualLanguage": "Layered editorial paper with one restrained signal accent",
    "palette": "Use the frozen sequence palette",
    "typography": "Use the frozen editorial type roles"
  },
  "timing": {
    "startSec": 18.4,
    "durationSec": 7.2,
    "beats": [
      {"id": "compound", "startSec": 0.0, "endSec": 4.6},
      {"id": "handoff", "startSec": 4.6, "endSec": 7.2}
    ]
  },
  "neighbors": {
    "previous": {
      "sceneId": "scene-02",
      "handoff": "Continue the left-to-right attention path established by the prior scene."
    },
    "next": {
      "sceneId": "scene-05",
      "handoff": "Resolve on the constrained marker so the next scene can inherit it."
    }
  }
}
```

For a `ScenePacket`, retain the same bounded fields and set `packetType` to `ScenePacket` with exactly one `sceneIds` entry. Include only applicable neighbor boundaries. Timing and beat windows follow the packet's declared aligned timing convention and must not be mistaken for new timing authority over the frozen direction.

## Schema validation and consumer obligations

Validate packet structure against `schemas/implementation-packet.schema.json`. It checks the discriminator, required fields, nonempty unique scene IDs, one-scene bounds for `ScenePacket`, hash syntax and nonnegative timing values. Register the local schema bundle when resolving relative references; no network schema fetch is needed.

Before consuming a packet, inspect the referenced frozen board and confirm its approval, scope IDs/order, artifact/evidence bytes against their digests, asset acceptance/provenance in the existing ledger, and relevant neighbor boundaries. Packet `startSec` is composition-global; beat `startSec`/`endSec` are packet-local. Check `0 <= startSec < endSec <= durationSec` for every beat against final alignment. JSON Schema cannot compare these fields or prove file identity; those are consumer obligations, not checks currently performed by `tools/validate_project.py`. Reject stale/dangling references or invalid beat windows rather than guessing.

A schema pass proves structure only. This release defines future routing contracts, not a packet compiler or runtime validator. It does not prove frozen-board approval, rights clearance, factual truth, perceptible meaning, readable payoff, audible sound, implementation quality, critic independence or publication readiness. Keep those obligations with the consuming implementer and independent review; never manufacture hashes or receipts.
