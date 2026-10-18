# Camera language for motion graphics (2D / 2.5D)

Code: `engine/fx.js` §4 — `cam()`, `camKeys()`, `layer(depth, fn)`, `handheld()`, `impact()`;
core: `camOn()/camOff()` (simple scale-around-point). Sources: iart-ai shot-composition, video-shotcraft
shot library, video-talkcraft "anti-slideshow" camera system, classic cinematography.

## 1 · Rules
- **One shot, one camera intent.** Push OR pan OR orbit — combined moves read as chaos.
- Camera moves use `CURVE.camera` (in-out) over the whole shot; never linear, never fast zooms unless it is a
  deliberate punch-in.
- The camera is never perfectly dead: at least a 1–3 % drift or a breathing layer (anti-slideshow).
- Motivation: the camera moves *towards what the VO names*, or reveals what the VO introduces.
- Split every scene into depth planes: background (ambient) · midground (subject) · foreground (props).

## 2 · Depth planes & parallax (`layer(depth, fn)`)
| plane | depth | parallax speed | contrast / focus | contents |
|---|---|---|---|---|
| far background | 3–5 | 0.2–0.33× | low, desaturated, blurred | sky, gradient, texture |
| background | 1.6–2.5 | 0.4–0.6× | medium | set, map, room |
| subject | 1 | 1× | sharp | hero, text card |
| foreground | 0.5–0.8 | 1.25–2× | may blur as it crosses | props, particles of the *content*, frames |
```js
cam(camKeys(t, { z: [[a, 1], [b, 1.12]], x: [[a, 0], [b, -60]] }), t, 2);   // push + truck, 2 px handheld
layer(3, () => drawBg());  layer(1, () => drawHero());  layer(.6, () => drawProps());
```

## 3 · Move vocabulary
| move | how (cam fields) | intent | typical |
|---|---|---|---|
| **push-in / dolly in** | z 1 → 1.05–1.2 | intimacy, importance, tension | whole shot, camera curve |
| **pull-back / reveal** | z 1.3 → 1 | context, isolation, "the bigger picture" | 1.5–3 s |
| **slow pressure push** | z 1 → 1.08 + handheld 2–3 px, dark grade | suspense, menace | 2–4 s |
| **punch-in (snap zoom)** | z 1 → 2.5+ in 6–10 frames, motion blur, or `tin:'zoom'` | comic emphasis, "this one!" | 0.2–0.35 s |
| **truck / pan** | x keyframes | follow, survey, timeline travel | 1–3 s |
| **pedestal / tilt** | y keyframes | reveal height, top→bottom reading | 1–2 s |
| **crane rise** | y + z out together | from detail to overview (dashboards, maps) | 1.5–3 s |
| **orbit / arc** | ox = R·sin(θ) (subject stays, fg/bg slide opposite) | 3-D feel on flat art, hero moment | 2–4 s |
| **dolly zoom (vertigo)** | vz 0 → .25 (bg scales, subject constant) | unease, realisation | 1–2 s |
| **rack focus** | fd from 1 → 3 with ap 6–10 | shift attention between planes | 0.4–0.8 s |
| **dutch roll → level** | r .06 → 0 | instability resolved | 0.6–1 s |
| **handheld** | `cam(st, t, amp)` amp 2–6 px | documentary realism, nervousness | continuous |
| **impact shake** | add `impact(t, t0)` to cam | hits, stamps, slams | 0.3–0.5 s decay |
| **drone dive** | z 1 → 1.6 + y down, ease-in then settle | landing on a point of a map | 1–1.5 s |
| **bullet-time freeze orbit** | freeze element time, orbit camera | dramatic pause | 1–2 s |
| **exploded view** | layers separate in z (scale offsets) | how something is built | 1–2 s |

## 4 · Shot sizes (works for characters AND objects)
extreme wide (context) · wide · medium (character bust, info) · close-up (emotion) · extreme close-up
(eyes/detail, punchline) · macro (an icon, a letter's nuqta). Changing shot size on ONE subject is the
cheapest way to get cinematic variety (see the reference DNA: one character, many sizes).

## 5 · Composition
- 12-column grid, 96 px safe margins @1080p (title-safe ~5 %), 8 px spacing unit.
- One focal point on a thirds power point (33 % / 67 %); text in the empty third opposite the subject.
- Hierarchy order: size > contrast > colour > position. Negative space is active, not leftover.
- RTL: text reads right→left, so the caption block is right-aligned and the hero usually sits left;
  "forward" motion and timelines travel right→left, list items enter in RTL order; "back/undo" reverses it.

## 6 · Entrances/exits by edge
Enter from the nearest edge, ease-out; exit through an edge, ease-in, 30–50 % faster. Drilling deeper =
push in / scale up. Returning = reverse the entrance.

## 7 · Multi-aspect (16:9 master → 9:16 / 1:1)
| aspect | title-safe |
|---|---|
| 16:9 | ~5 % all sides |
| 9:16 | top 12–14 %, bottom 18–20 %, sides 6 % |
| 1:1 | 6–8 % |
| 4:5 | 6 % sides, 8 % top/bottom |
Keep the focal point in the centre band; for 9:16 **re-stack** (caption above, subject below) instead of
cropping or letterboxing. To render 9:16 set the canvas to 1080×1920 in the film page (core uses W,H) and
the viewport in still.mjs/render.mjs.

## 8 · Anti-slideshow checklist (per shot)
- [ ] continuous camera curve or breathing layer
- [ ] ≥2 depth planes with different parallax
- [ ] a primary action verb (enter / build / transform / measure / collide / write)
- [ ] something new every 2–4 s (text beats can be faster)
- [ ] idle life during holds (breathe, twinkle, drift), then *yield* (exit) before the next shot
