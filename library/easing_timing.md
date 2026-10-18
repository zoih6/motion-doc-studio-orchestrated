# Easing, timing & motion personality

Code: `engine/fx.js` §1 (`E`, `bezier`, `CURVE`, `tw`, `kf`, `SPRINGS`, `spr`, `PERSONA`).
Sources distilled: LottieFiles motion-design skill, iart-ai motion-art-direction, Material 3, Apple HIG,
Penner equations (see `library/resources.md`).

## 0 · The motion-language spec (fill ONE value per row before animating)
| Property | Choose one | Documentary default | Sticker-pop default |
|---|---|---|---|
| Persona | documentary / premium / corporate / playful / energetic / stickerpop | documentary | stickerpop |
| Signature curve (≈80–90 % of moves) | one `CURVE.*` | `CURVE.signature` (.22,1,.36,1) | `CURVE.overshoot` (.34,1.56,.64,1) |
| Exit curve | one | `CURVE.md3Accel` | `CURVE.md3Accel` |
| Base unit | atomic duration; others ×½ ×2 | 0.6 s | 0.28 s |
| House springs | max 3 | card / snap / soft | snap / wobbly / pop |
| Transition family | 1 main + 1 accent | tear + push | cut + zoom/whip/flash |
| Stagger | one rhythm | 90 ms RTL | 70 ms RTL |
| Hold discipline | min stillness after a beat | 0.4 s | 0.3 s |
| Intensity budget | travel / scale / overshoot | ≤ ⅓ screen, 0.96→1, ≤3 % | ≤ ⅓ screen, 0.6→1, ≤10 % |

Mixing personas in one film is the #1 cause of "inconsistent" motion. A third curve must justify itself.

## 1 · Personalities (`PERSONA`)
| Persona | Duration | Curve | Overshoot | Reads as | Use for |
|---|---|---|---|---|---|
| documentary | 0.5–0.8 s | camera (.65,0,.35,1) / signature | ≤3 % | grave, cinematic | history, heritage, investigations |
| premium | 0.35–0.6 s | (.4,0,.2,1) | 0 % | elegant, luxury | brands, art, finance |
| corporate | 0.2–0.4 s | (.2,0,0,1) MD3 | 0–3 % | clean, trustworthy | product, UI, explainers |
| playful | 0.15–0.3 s | backOut / (.34,1.56,.64,1) | 10–20 % | fun, bouncy | kids, lifestyle, social |
| energetic | 0.1–0.25 s | expoOut | 15–30 % | hype, bold | sports, promos, trailers |
| stickerpop | 0.17–0.3 s | overshoot + snap spring | 5–10 % | witty, internet-native | dialect ads, social explainers |

## 2 · Duration table
| Element | Duration |
|---|---|
| micro (tick, dot, icon pop) | 0.1–0.2 s |
| word / caption entrance | 0.2–0.35 s |
| card / panel enter | 0.25–0.45 s |
| full-frame transition | 0.2–0.6 s (4–18 frames) |
| hero reveal / title | 0.6–1.2 s |
| camera push / drift | 1–4 s (whole shot) |
| ambient loop | 4–20 s period |
- **Distance scales duration:** 100 px = base, 200 px ×1.3, 400 px ×1.6.
- **Enter > exit:** entrances 30–50 % longer than exits. Exits accelerate away (ease-in family).
- **Weight:** heavy (modals, plates) 0.3–0.5 s, 0 % overshoot · medium (cards) 0.2–0.35 s, 3–5 % · light (icons, badges) 0.08–0.2 s, 5–15 %.

## 3 · Directional easing
Entrance → decelerate (ease-out family) · Exit → accelerate (ease-in) · On-screen move → in-out ·
Camera → `CURVE.camera` · Ambient loop → sine in-out · **Linear only** for continuous drifts, progress bars,
rotation loops. Never linear for spatial moves.

## 4 · Industry curves (`CURVE.*`)
| key | cubic-bezier | use |
|---|---|---|
| md3 | (.2,0,0,1) | default on-screen |
| md3Emph | (.05,.7,.1,1) | emphasized entrances |
| md3Accel | (.3,0,1,1) | exits |
| apple | (.25,.1,.25,1) | standard iOS |
| premium | (.4,0,.2,1) | calm, luxury |
| signature | (.22,1,.36,1) | soft-landing decelerate (great default) |
| expoOut | (.16,1,.3,1) | snappy reveals, colour changes |
| camera | (.65,0,.35,1) | camera moves, pushes, pans |
| overshoot | (.34,1.56,.64,1) | playful pop |
| bounceSettle | (.175,.885,.32,1.275) | settle with a kick |
| anticipate | (.36,0,.66,-.56) | wind-up before a move |
| whip | (.7,0,.2,1) | whip pans: slow-fast-slow |
Penner set in `E.*`: quad/cubic/quart/quint/sine/expo/circ/back/elastic/bounce × In/Out/InOut, plus
`E.steps(n)` for stepped "on twos" animation (sakuga-style timing switch: steps → smooth at the climax).

## 5 · Springs (`SPRINGS`, mass 1)
| name | k / d | feel |
|---|---|---|
| card | 150 / 19 | paper landing, slight overshoot (house) |
| snap | 320 / 28 | dots, ticks, stamps, captions (house) |
| soft | 60 / 15 | big heroes, crowns (house) |
| default | 170 / 26 | neutral |
| gentle | 120 / 14 | floaty |
| wobbly | 180 / 12 | stickers, jelly props |
| stiff | 210 / 20 | UI, decisive |
| slow | 280 / 60 | premium, no overshoot |
| molasses | 280 / 120 | heavy |
| pop | 400 / 22 | energetic hits |
| jelly | 260 / 10 | swinging signs |
Guard overshoot: `Math.max(0, r)` for radii/scales; alpha `clamp(k*3)`.

## 6 · Stagger budgets
| pattern | delay | total |
|---|---|---|
| micro cascade (grid cells) | 20–40 ms | < 200 ms |
| standard (cards, words) | 50–100 ms | < 400 ms |
| dramatic (hero lines) | 100–200 ms | < 600 ms |
| wave (data viz) | 30–60 ms | < 500 ms |
Arabic order = right→left, top→bottom. VO-synced captions ignore stagger and use word times.

## 7 · Choreography rules
- Lead with the hero; supports follow 50–150 ms later; texture is subliminal.
- Same entry direction for a group. Counter-motion: ambient layer drifts opposite at 20–30 % speed.
- **⅓ rule (distance):** nothing travels > ⅓ of the frame without a keyframe/scale change.
- **⅓ rule (elements):** with 3+ elements, ≤ ⅓ of them move at once.
- **Never scale from 0** — start at 0.6 (playful) … 0.9–0.97 (serious).
- Three motion layers always: primary (hero) · secondary (support) · ambient (breathing, drift, grain).
- One "wow" moment per piece.

## 8 · Emotion → motion
| emotion | path | curve | duration |
|---|---|---|---|
| joy | curved, upward | backOut | 0.2–0.4 s |
| calm | gentle curves | sine in-out | 0.5–1 s |
| urgency | straight | expoOut | 0.1–0.2 s |
| sadness | slow, downward | cubic in-out | 0.6–1.2 s |
| surprise | radial outward | expoOut | 0.15–0.3 s |
| elegance | long arcs | premium | 0.4–0.7 s |
| menace / suspense | slow push, low light | camera | 1.5–3 s |
Path language: angular = tense · curved = friendly · diagonal = purposeful · vertical = growth/weight ·
horizontal = progress (in RTL, "forward" is right→left).

## 9 · Material → motion
rigid ×1.2 dur, 0 % · elastic ×0.8, 15–25 % · fluid ×1.5, 5 % · paper ×1.0, 3–5 % · gas ×2.0, 0 % · glass ×0.9, 0 %.

## 10 · Keyframes in code
```js
const x = kf(t, [[2.0, 300], [2.6, 960, CURVE.expoOut], [4.0, 1000, CURVE.camera]]);   // ease applies INTO each key
const k = tw(t, 3.1, 3.4, CURVE.md3Emph);                                              // eased 0→1
const s = spr(t, 5.2, 'wobbly');                                                       // spring 0→1(+overshoot)
const P = PERSONA.stickerpop;  drawWords(L, t, 1.2, 1300, 400, { mode: 'pop', stagger: P.stagger, springName: P.spring });
```
