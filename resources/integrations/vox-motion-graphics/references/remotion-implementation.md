# Remotion Implementation

Use this reference after storyboard freeze.

## Implement the frozen decision

Preserve:

- scene and state order;
- visual thesis and focal hierarchy;
- defining object/causal relationship;
- accepted asset identity;
- transition job and focal handoff;
- readable payoff windows, caption/disclosure hierarchy, and planned sound decisions.

Implementation may refine interpolation, easing, overlap, compositing, and performance. If it changes the thesis, focal owner, defining relationship, accepted hero asset, or transition logic, return to storyboard review.

Keep the frozen snapshot distinct from as-built notes. For each defining promise, carry its observable invariant and proof location, not just object/state IDs. Inspect boundary/action clips for handoffs, complete-reveal frames, deepest planned crops, and mastered sound. A present asset or cue filename does not prove it was visible or audible.

Use a bounded [implementation packet](implementation-packets.md) for the assigned scene or sequence: cite the frozen board revision/hash, relevant claims/rights/assets, approved implementation decisions, style and aligned timing, and applicable neighbor boundaries. Include only relevant reference excerpts, not the whole skill as a per-scene prerequisite. The packet helps bound context; it never supersedes the frozen storyboard, ledger, evidence, or review gates.

## Deterministic frame-driven motion

Use current official patterns from the installed Remotion version, such as frame/config hooks, interpolation, springs/easing, sequences/series, and Remotion media primitives.

- Write scene motion against local frame zero.
- Convert aligned seconds to frames at the implementation boundary.
- Clamp interpolation where overshoot would break composition.
- Conform orientation, semantic trigger, action completion, readable payoff, and transition windows to final alignment; nominal scene durations are not enough.
- Permit reviewed anticipation and J/L cuts. Count payoff reading time only after essential content becomes legible, accounting for competing action.
- Use stable seeds for render-visible procedural variation.
- Do not use timed CSS transitions, CSS keyframes, or browser-time animation for render-visible motion.

Current installed documentation overrides remembered APIs.

## Component boundaries

Keep the composition registry thin. Place scene-specific components, props, and data under the project/scene boundary. Name layers and parameters by semantic owner so local asset transforms cannot silently collide with camera transforms.

Property controls and interactive Studio layers are optional. Use them when manual editability or bounded critic repair is valuable, not as a universal finish requirement.

## Small tune surface

Expose only high-leverage repair decisions, for example:

- focal x/y and scale;
- crop/object position;
- headline position/size;
- camera origin/depth;
- action/settle/transition offsets;
- chosen treatment strength;
- relevant SFX offset/level.

Use typed bounds. Avoid exposing arbitrary CSS. Emit a tune manifest/parameter patch only when the workflow will consume it.

## Geometry and compositing

- Compose cutouts using visible/alpha bounds and important features.
- Account for the complete transform chain, including asset, entrance, camera, and overscan scale.
- Preserve faces, logos, dates, and evidence details from accidental occlusion.
- Keep fills, tint, grain, outlines, masks, and clip paths on consistent source bounds.
- Keep text outside image filters unless occlusion is intentional.
- Preserve the owning scene's background across nested panels and embedded playback.
- Check clean and captioned compositions with disclosures at intended viewing size; preserve the accepted hierarchy rather than shrinking captions to fit.
- Match crop behavior to the promised role: a complete-object reveal must expose essential components at payoff, even if a cover crop looks attractive.

## Charts and evidence graphics

- Lock values, units, date range, source, order, and label copy before choreography.
- Use one explicit origin for axes, marks, and labels.
- Scale the complete chart group rather than only its fill.
- Keep overlays and masks on the source geometry.
- Render entry, in-motion, and settled states; verify all data and labels remain legible and in frame.

## Media and reliability

Use current Remotion guidance for media loading, premounting, asset readiness, and fonts. When rendering many stills locally, avoid concurrent bundlers fighting over the same cache; reuse one bundle or render sequentially.

Prefer HTML/CSS/SVG/2.5D compositing before true 3D unless the story geometry requires depth that simpler methods cannot express.

## Mastered review

Resolve each planned sound cue as implemented, replaced, or omitted with a reason for changes. Produce a mastered draft with narration, captions/disclosures, SFX, and music as applicable, then run technical and independent editorial review on that artifact. Draft previews may render throughout; they must not inherit publication approval from an earlier board or master revision.

For a v0.10 publish candidate, retain independent pre-freeze Scene and Sequence reviews, Chapter review where applicable, and Film review. After implementation, reopen the changed scope and affected neighbors when a defining deviation changes their promise. Run final multi-level editorial review on the actual mastered output with captions, disclosures, narration, and mixed sound; keep its inspected board/master hashes unchanged. Small viewing-size evidence must show actual consumption-size readability. Neither a packet validator nor artifact digest proves perception or approval.

