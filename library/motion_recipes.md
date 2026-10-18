# Motion recipes — قاموس الحركات (MOVES dictionary)

**Code:** [`engine/moves.js`](../engine/moves.js) · **Visual strips:** `specimens/moves_*.jpg` · **Related:** [easing_timing.md](easing_timing.md) (curves/springs) · [motion_vocabulary.md](motion_vocabulary.md) (camera & editorial words) · [glossary.md](glossary.md) (bilingual terms)

Every entry is a **named, reusable move** — a pure function of progress (no timers), so it works in the deterministic renderer.
The names are the industry vocabulary that designers, After Effects users and CSS libraries share (fadeInUp, popIn, rubberBand, hinge…),
so a brief, a storyboard or a user request can name a move and the agent can play it 1:1. All implementations are original.

## 1 · How to use

```js
// box = where the element lives: centre x,y + its size w,h (+ any move parameter: dist, k, d, period, amp, dir, clip…)
const box = { x: 960, y: 540, w: 700, h: 140 };
move('popIn', t, 2.0, box, () => drawTitle(0, 0));               // draw your element centred at (0,0)
move('rubberBand', t, 4.2, box, () => drawTitle(0, 0), { dur: 1.1 });
seqMove([['dropIn', 1.0], ['tada', 2.4], ['fadeOutUp', 5.6]], t, box, st => drawTitle(0, 0));
staggerMove('fadeInRight', t, 3.0, wordBoxes, (b, i) => drawWord(i), { gap: .06, order: 'rtl' });
// progress-only moves return values you apply yourself:
move('drawIn', t, 1, box, st => icon('landmark', 0, 0, 160, { k: st.reveal ?? 1 }));
move('typeIn', t, 1, box, st => drawText(line.slice(0, Math.ceil(line.length * (st.reveal ?? 1)))));
```
`st` (passed to your draw fn) also carries `shade` (flip darkness), `glow`, `shadow` (hover), `rgb` (glitch split) and `impactAt` (stampIn) for extra polish.

## 2 · Picking rules (house style)
1. **One persona per film** ([easing_timing.md §1](easing_timing.md)) → it decides the family: documentary = `fadeInUp/riseIn/blurIn/drawIn`; playful = `popIn/springIn/bounceIn/jello`; energetic = `whipIn/stampIn/punch/shakeX`; premium = `blurIn/unfoldIn/riseIn`.
2. **Never everything-fades-in.** At most 1 in 4 entrances may be a plain `fadeIn`; prefer a move with direction or mass.
3. **Arabic/RTL:** horizontal entrances come from the **right** (`fadeInRight`, `slideInRight`, `staggerMove(...,{order:'rtl'})`). Never animate Arabic letter by letter — move whole words (shaping breaks).
4. **Emphasis** is for something already visible that the VO is naming right now: `punch` on a beat, `pulse` for "look here", `shakeX` for refusal/error, `tada` for a win. Max one emphasis per 3 s.
5. **Exit faster than you enter** (≈ 0.7× duration); exits accelerate (`eI`), entrances decelerate.
6. **Loops** only on secondary elements (badges, icons, decor) — the hero must be still while read.
7. **Weight:** heavy things (stamps, books, stones) → `dropIn`, `stampIn`, `squash`; light things (paper, leaves, labels) → `swingIn`, `float`, `sway`.

## 3 · Named combos (recipes)

| recipe | sequence | use for |
|---|---|---|
| **Headline slam** | `stampIn` → camera `impact()` at u=.55 → `punch` on the key word | the hook line in the first 2 s |
| **Archive card** | `dropIn` (pivot feet) → `hover` loop → `flipOutX` | documents, photos, manuscripts |
| **Map pin** | `bounceInDown` → `pulse` ×2 → label `fadeInRight` | places, cities, battles |
| **Number reveal** | `zoomInUp` + counter tween → `heartBeat` at final value | statistics, dates |
| **Quote** | lines `staggerMove('riseIn', …, {order:'index', gap:.18})` (clip) → hold → `blurOut` | VO quotes, verses, poetry |
| **Correction** | old word `shakeX` → `wipeOut` → new word `popIn` | myths vs facts |
| **Character entrance** | portrait `swingIn` (top pivot, hanging frame) → nameplate `unfoldIn` | historical figures |
| **Icon list** | icons `staggerMove('drawIn')` + labels `fadeInRight` gap .08 | features, steps, causes |
| **Calm outro** | everything `fadeOutDown` staggered from the edges (`order:'center'` reversed) | endings |
| **Glitch fact** | `glitchIn` + rgbSplit → hold → `punch` | tech, modern contrasts |
| **Paper collage** | cut-outs `dropIn` + `jitter` loop at 12 fps | collage / stop-motion styles |
| **Seal / stamp** | `stampIn` + ink `luma` transition | approvals, firmans, dates |

<!-- AUTO -->
## Full MOVES dictionary (generated from engine/moves.js — 84 moves)
Visual strips: [moves_in](specimens/moves_in.jpg) · [moves_out](specimens/moves_out.jpg) · [moves_emph](specimens/moves_emph.jpg) · [moves_loop](specimens/moves_loop.jpg)

### Entrances — 34

| move | default dur | what it does / when |
|---|---|---|
| `fadeIn` | 0.45s | plain opacity. Use sparingly (banned as the ONLY entrance in a film) |
| `fadeInUp` | 0.55s | rise a little while fading — calm default for captions |
| `fadeInDown` | 0.55s | drop a little while fading — labels from above |
| `fadeInLeft` | 0.55s | enters from the left (LTR reading) |
| `fadeInRight` | 0.55s | enters from the right (RTL reading — default for Arabic) |
| `slideInUp` | 0.6s | travels in from below the frame, no fade |
| `slideInDown` | 0.6s | travels in from above the frame |
| `slideInLeft` | 0.6s | travels in from off-screen left |
| `slideInRight` | 0.6s | travels in from off-screen right (RTL) |
| `zoomIn` | 0.5s | grows from small |
| `zoomInUp` | 0.7s | grows while rising, slight overshoot |
| `popIn` | 0.45s | scale with overshoot — the signature "sticker" entrance |
| `springIn` | 0.9s | physical spring scale-in (stiffness el.k, damping el.d) |
| `bounceIn` | 0.75s | staircase of scale overshoots — cartoony |
| `bounceInDown` | 0.9s | falls from above and bounces on its baseline |
| `backInUp` | 0.8s | arrives small from below, then scales to full size |
| `backInDown` | 0.8s | arrives small from above, then scales to full size |
| `flipInX` | 0.7s | card flips toward camera around the horizontal axis |
| `flipInY` | 0.7s | card flips around the vertical axis |
| `rotateIn` | 0.6s | spins into place |
| `rollIn` | 0.75s | rolls in from the side like a coin |
| `lightSpeedIn` | 0.55s | races in with a forward shear, settles with a counter-lean |
| `jackInTheBox` | 0.8s | springs out of the bottom pivot with a wobble |
| `blurIn` | 0.6s | focus pull from soft to sharp — premium/editorial |
| `dropIn` | 0.7s | gravity fall + squash on landing (pivot at feet) |
| `stampIn` | 0.45s | slams from huge onto the page; pair with impact()/shake at u=.55 |
| `swingIn` | 0.9s | swings down from a top pivot, like a hanging sign |
| `riseIn` | 0.65s | rises out of an invisible baseline mask (set el.clip=true) |
| `whipIn` | 0.35s | very fast horizontal arrival with smear |
| `elasticIn` | 1s | rubbery overshoot scale |
| `unfoldIn` | 0.7s | opens as a line, then unfolds vertically (screens, panels) |
| `glitchIn` | 0.4s | stuttering digital arrival (set rgb split on draw) |
| `typeIn` | 1s | progress only: use reveal for text.slice(0, n*reveal) or a mask |
| `drawIn` | 1s | progress only: stroke draw-on for paths/icons (icon(..,{k:reveal})) |

### Exits — 18

| move | default dur | what it does / when |
|---|---|---|
| `fadeOut` | 0.35s | plain opacity out |
| `fadeOutUp` | 0.45s | lifts away |
| `fadeOutDown` | 0.45s | sinks away |
| `slideOutLeft` | 0.5s | pushed off left |
| `slideOutRight` | 0.5s | pushed off right |
| `zoomOut` | 0.4s | shrinks away |
| `popOut` | 0.35s | small anticipation swell, then collapses |
| `backOutDown` | 0.8s | shrinks, then drops out |
| `flipOutX` | 0.5s | flips away around horizontal axis |
| `rotateOut` | 0.5s | spins away |
| `rollOut` | 0.7s | rolls off to the side |
| `lightSpeedOut` | 0.45s | races out with a backward shear |
| `hinge` | 1.6s | a bolt breaks: swings from the top-left corner, then falls |
| `blurOut` | 0.45s | defocuses away |
| `dropOut` | 0.6s | gravity takes it |
| `shrinkOut` | 0.3s | quick collapse to a point |
| `whipOut` | 0.3s | very fast exit with smear |
| `wipeOut` | 0.5s | progress only: hard wipe mask from the reading edge (set el.clip=true) |

### Emphasis (element already on screen) — 21

| move | default dur | what it does / when |
|---|---|---|
| `pulse` | 0.6s | gentle swell — "look here" |
| `heartBeat` | 1.1s | two quick beats (lub-dub) |
| `rubberBand` | 0.9s | stretches and snaps back like elastic |
| `shakeX` | 0.6s | horizontal shake — denial/error/impact |
| `shakeY` | 0.6s | vertical shake — rumble |
| `headShake` | 0.9s | a "no" shake with tilt |
| `nod` | 0.7s | a "yes" nod |
| `swing` | 1s | pendulum from the top edge |
| `tada` | 1s | crouch, then wiggle big — celebration |
| `wobble` | 1s | side-to-side lurch with rotation |
| `jello` | 0.9s | shear wobble like gelatin |
| `bounce` | 0.9s | hops in place twice, squashes at the bottom |
| `flash` | 0.8s | blinks twice |
| `punch` | 0.35s | instant scale punch that decays — beat hits |
| `squash` | 0.5s | squash on the baseline (weight) |
| `stretch` | 0.5s | stretch upward (anticipation before a jump) |
| `tilt` | 0.6s | curious tilt and back |
| `nudge` | 0.45s | small push toward el.dir, returns |
| `glow` | 0.8s | progress only: drive a highlight/halo (use on highlights, NOT on UI) |
| `spinOnce` | 0.7s | one full turn |
| `flipCoin` | 0.8s | one full Y-flip (coin) |

### Loops (ambient, u = seconds) — 11

| move | default dur | what it does / when |
|---|---|---|
| `float` | ∞ | slow vertical float (period el.period) |
| `bob` | ∞ | repeated small hops |
| `sway` | ∞ | plant/flag sway from the base |
| `spin` | ∞ | continuous rotation |
| `orbit` | ∞ | elliptical orbit with fake depth |
| `pendulum` | ∞ | clock pendulum from the top |
| `breathe` | ∞ | living idle — subtle scale |
| `blink` | ∞ | on/off (cursors, REC lights) |
| `drift` | ∞ | organic noise drift (seeded) |
| `hover` | ∞ | hover with shadow cue (use shadow to scale a contact shadow) |
| `jitter` | ∞ | stop-motion boil on twos/threes (el.fps 8–12) |
