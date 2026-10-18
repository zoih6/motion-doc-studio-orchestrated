# Motion rules

## 0. Direction first (before any keyframe)
- Fill the **motion-language spec** (library/easing_timing.md §0): ONE persona, ONE signature curve + one exit
  curve, base unit, ≤3 house springs, ONE transition family (+1 accent), stagger rhythm, hold discipline.
- Rank every element: hero (primary) / support (secondary) / texture (ambient). Exactly one hero per frame.
- Restraint pass: list what stays still. One "wow" moment per film.

## 1. Physics, not tweens
- Use **damped springs** for every entrance (`sp(t, t0, preset)`), cubic in-out (`ease`) for camera
  moves, `easeOut` for write-ons. Linear only for continuous drifts (rays, breathing).
- Exactly **three presets** per film so the motion feels designed, e.g.
  `card: [150, 19]` (paper landing, slight overshoot) · `snap: [320, 28]` (dots, ticks, stamps) ·
  `soft: [60, 15]` (big reveals, crowns, heroes).
- Guard against overshoot artefacts: radii/scales → `Math.max(0, …)`; alpha → `clamp(k*3)`.
- Everything alive "breathes" a little (±1.6 px, ±0.15°) so the frame never freezes — including holds.

## 2. Pacing
- **Hook in the first 2 s** (an action, not a logo).
- **New idea every 2–4 s.** A shot may last longer only if something keeps evolving inside it.
- Enter on the word: element reaches 90 % of its spring 0.1–0.2 s *before* the word ends.
- Stagger lists at 0.18–0.35 s per item (RTL order for Arabic).
- Holds before big statements (0.3–0.6 s of stillness) make them land; follow with a "snap".

## 3. Camera  (full vocabulary: library/camera_language.md)
- Build shots in depth planes with `layer(depth, fn)` (bg 0.2–0.5× parallax, subject 1×, fg 1.25–2×).
- Every shot has a slow drift (scale 1.00 → 1.03–1.08) or a motivated push towards the subject named in
  the VO. Never static, never fast zooms.
- `camOn(scale, focusX, focusY)` around a stage point; ease over the whole shot.
- Max one camera idea per shot (push OR pan OR tilt).

## 4. Transitions  (catalogue: library/transitions.md, code: TRANS in engine/fx.js)
- Pro transitions are 4–10 frames (energetic) or 12–18 frames (calm). After a hard cut, content must still arrive.
- Between shots: a motivated physical transition — **paper tear RTL** (default in collage/manuscript
  styles), slide, push-through, match on shape. Hard cut only on a hard beat (stamp, "But…").
- The outgoing shot keeps animating during the transition (render both: `drawTear(..., () => prev.draw(t))`).
- Exits: elements leave in the reading direction (to the left in RTL) or fall down; never just vanish.

## 5. Write-on & reveal
- Text writes on RTL with a soft edge (`writeOn`), 0.4–0.9 s depending on length.
- Calligraphy/ink: reveal along a stroke-order map (geodesic distance from stroke start), not a wipe.
- Lines/geometry draw on along their path (`line`, `arc`), dots land with `snap` and a 1.8→1 scale.

## 6. Banned
- Everything fading in. Centered title on a gradient. Corner labels / lower-third bars. Frame borders.
  Glow/drop-shadow on UI text. Generic particles/bokeh. Lens flares. Spinning 3D text. Bounce on serious
  topics. Slideshow (photo + Ken Burns + crossfade). Random stock that doesn't match the sentence.
  Transitions from editing-software presets.

## 7. Determinism (render = f(t))
- Seeded RNG (`rng(seed)`, `hash(a,b)`); no `Math.random`, `Date.now`, `requestAnimationFrame`, CSS
  animation, `<video>`.
- Shot functions must not keep state between frames (except pure caches keyed by t/progress).
- Any frame can be rendered alone (chunked renders start mid-film).

## 8. Motion blur
- Render 2 sub-frames per frame and blend (`render.mjs --sub 2`) — cheap, removes strobing on fast springs.

## 9. Craft rules distilled from 2026 open-source motion skills
- **Never linear** for spatial movement (only drifts, loops, progress). Entrance = ease-out, exit = ease-in,
  on-screen = in-out, camera = `CURVE.camera`.
- **Never opacity-only** for an important change — combine with position/scale/blur/mask.
- **Never scale from 0** — start at 0.6 (playful) to 0.9–0.97 (serious).
- **Enter > exit:** exits 30–50 % shorter. Distance scales duration (200 px ×1.3, 400 px ×1.6).
- **⅓ rule:** nothing travels more than ⅓ of the frame without a keyframe; with 3+ elements ≤ ⅓ move at once.
- **Three motion layers** always: primary + secondary + ambient (breathing, drift, grain).
- **Stagger budget** ≤ 400–600 ms total per group (per-word VO sync is the exception).
- **Hold discipline:** ≥ 0.3 s of stillness after each beat before the next move.
- **Arabic kinetic type:** animate per word, never per letter (shaping breaks) — library/kinetic_typography.md.
- **Anti-slideshow:** continuous camera curve or breathing on every shot, ≥2 parallax planes, idle → yield.
- **Personality is global:** do not mix playful overshoot into serious/financial/grief content.
