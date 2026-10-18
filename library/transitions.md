# Transitions dictionary

Code: `engine/fx.js` §9 `TRANS` + core `tear`. Use per shot: `SHOTS.push({a, b, tin: 'whip', tdur: .3, focus: [x,y], accent, draw})`.
`FILM.tin` sets the default; `FILM.whipDir` (1 = content travels left→right, i.e. new shot enters from the
left — natural for RTL). The outgoing shot keeps animating during the transition (core passes its draw).

## Rules
- Pick **one transition family + one accent** per film (motion-language spec). Variety reads as noise.
- Every transition is **motivated**: by the VO (a turn, a "but…", a reveal), by the beat, or by a shape/motion
  that continues across the cut (match cut).
- Pro transitions are short: **4–10 frames** for cuts with energy, 12–18 frames for calm ones.
- A hard cut is fine when the *mood or register* changes (bright → dark) — and new content must still
  *arrive* after it (never land on a static frame).
- Don't transition the transition (no whip + spin + flash together).

## Catalogue
| key | dur | what | motivation / when | avoid |
|---|---|---|---|---|
| `cut` | 0 | hard cut | register/mood switch, hard beat, punchline | on calm continuous VO without new content arriving |
| `tear` | .62 | paper torn away RTL with fibre edge + shadow (core) | collage / manuscript styles | flat/digital styles |
| `whip` | .32 | both frames rush sideways with motion blur | energy, "meanwhile", topic jump | serious/grave beats |
| `whipUp` | .32 | vertical whip | lists, "next", feeds | — |
| `zoom` | .36 | punch-through into `focus`, incoming settles from .75 | "this one!", entering a detail/icon/map point | more than 2× per minute |
| `flash` | .24 | white (or `flashColor`) peak hides the cut, 2–3 frames full | impact, photo flash, reveal | epileptic strobe sequences (>3 flashes/s) |
| `dip` | .5 | dip to black (or `dipColor`) | time passing, chapter end | as a default |
| `iris` | .5 | circle opens from `focus`, accent ring | spotlight on a subject, old-film nod | — |
| `clock` | .55 | radial sweep (RTL = counter-clockwise) | time, cycles, "a year later" | — |
| `blinds` | .55 | 12 staggered vertical slices | lists, data, grids | organic topics |
| `push` | .5 | both frames move together, no blur | calm continuity, timeline travel | — |
| `slide` | .5 | incoming slides over, outgoing dims & recedes | layering, "zoom into a document" | — |
| `barn` | .55 | outgoing splits in two doors | reveal, opening, "behind the doors" | — |
| `luma` | .6 | organic noise burn-through | memory, dream, ink, smoke | fast-paced sections |
| `glitch` | .2 | slice offsets + RGB split | tech, error, hack, VHS | heritage/serious |
| `smear` | .3 | liquid stretch-blur morph | word → word morph, playful swap | — |
| `band` | .5 | diagonal accent band sweeps across | VOX-style graphic wipe, section change | more than one band colour |

## In-shot transitions (no shot change)
- **Match cut / shared element:** the same shape (circle, dot, frame, line) continues from shot A to B —
  draw it in both shots at the same place across the boundary.
- **Line carry:** a line exits shot A and becomes the frame/axis of shot B.
- **Letterform zoom:** push through the counter of a letter into the next scene (`zoom` with `focus` on it).
- **Colour strobe on the beat:** a card's fill alternates 2–4 colours every 3–4 frames for 0.5–1 s (DNA).
- **Blur swap:** change a word in place (`blurSwap`).
- **Panel build:** split-screen panels arrive one by one (`panel(... from)`) — a transition made of layout.
- **Stepped timing switch:** `E.steps(4)` motion that switches to smooth at the climax (sakuga feel).

## Rhythm recipes (from trailer/montage grammar)
- **Accelerando:** cuts with shrinking intervals (1.0 → 0.7 → 0.5 → 0.35 s) into a hold.
- **Blackout slam:** 4–8 black frames + silence, then a slam (`cut` + `impact()`).
- **Triple cut:** three quick detail shots (6–8 frames each) of the same subject.
- **Smash cut into stillness:** loud/fast → instant silence and a static frame (use rarely).
- **Card/footage cadence:** alternate title cards and images on the beat.

## SFX pairing (SOUND LAYER kit types, `workflow/10_sound_layer.md`)
| Transition | Cue | Kit sound (`sfx.py browse --type …`) |
|---|---|---|
| whip / push / slide | `cue.move(id, when.ease(a, a + dur))` | `whoosh` or `swish` |
| zoom / impact | `cue.move` + hero `cue.land` on the settle | `riser` peaking on `thump+tap` (punchy: `hit+boom`) |
| flash / hard cut | `cue.cut(id, a)` | `hit`, `click`, or a planned silence |
| tear (house RTL) | `cue.move(id, when.ease(a, a + TEAR))` | `paper` (LOOK: one event, no steady noise) |
| glitch / rgbSplit / band | `cue.cut` or `cue.move` | `glitch` / `zap` / `swish` |
| punchline cut | `cue.cut` + `stop_before` on the next hero | silence, then the hero |
Never synthesize these (no `tools/sfx.mjs` hits/whooshes). The VO ducks the music automatically (`duck_db`).

## GPU pack (v1.2): 125 more transitions
`engine/gl.js` + `engine/kit/data/gl_transitions.js` register every gl-transitions shader as `tin: 'gl:<Name>'` (e.g. `gl:Dreamy`, `gl:cube`, `gl:luma`, `gl:hexagonalize`).
Catalogue, curated picks by intent, and parameters: [gl_transitions.md](gl_transitions.md). Shot-level transition recipes (hidden cuts, line-carry, iris match…): [shot_cards_index.md](shot_cards_index.md) → `transition/`.
