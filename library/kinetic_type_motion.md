# Kinetic Type Motion — Arabic lyric / quote / caption motion (v2.1)

> The grammar of **text-only motion on a black (or dark) stage**: Arabic Kinetic Typography + Lyric Motion
> Graphics. Engine: `engine/type.js` (`KT`). Page template: `engine/kinetic.html`. Demo: `examples/kinetic_demo/`
> (10 s, 9:16). Reference analysis: `examples/reference_dna/kinetic_lyrics/DNA.md`.
> Sources merged here: the user's analysis report «تحليل موشن النصوص فقط — باعتبار الخلفية سوداء», frame-by-frame
> analysis of 3 reference lyric videos, and the 2026 motion-design literature on secondary motion, overlap and timing.
> Older/basic layer: `library/kinetic_typography.md` (`layoutWords/drawWords` for VO captions in documentaries).

**Read §0 and §9 before designing. Never copy a reference shot; rebuild its *grammar* for the new words.**

---

## 0 · Ten laws (the difference between "pro" and "kids' stuff")
1. **Word-level only for Arabic.** Letters join, so per-letter animation breaks shaping. Animate whole words or
   phrases. For Arabic "tracking", use **kashida** (`KT.kashida`, `KT.stretch`). Never use letter-spacing.
2. **Hierarchy before motion.** Each beat has one **Hero** (big, strongest move), at most one **Supporting** word
   (small, quiet move) and at most one **Accent** (the accent colour or a shape). Only one thing is loud at a time.
3. **Motion pair.** Every important word travels with a partner shape (dot, line, circle, bar, bubble, hinge…).
   **Shape and text never start or end on the same frame**: offset them by 2–6 frames (`KT.F(n)`).
4. **Something always moves, nothing moves for no reason.** After landing, a word *holds* with micro-life
   (drift 6–20 px/s, wiggle 1–2° / 2–4 px, breathe 1–2 %). A hold is never a frozen frame and never a shake.
5. **Exits are 30–40 % shorter than entrances** and accelerate (ease-in). Entrances decelerate (ease-out / spring).
6. **Reading time is sacred:** at least 0.8 s of readable hold per word (1.0–1.5 s for heroes). `KT.timeline()`
   enforces `minHold`.
7. **Space is choreography.** Each new hero lands somewhere *new* (`KT.place(i)`), in negative space, never
   repeating the previous spot. Keep a 96 px safe margin (1080 px frames: about 8 %).
8. **One accent colour per film**, used *on meaning* (the emotional key word, its shape partner). White/ivory
   ink, grey for "past" words (dim before exit).
9. **Continuity between beats.** The exit of word A *becomes* the entrance of word B: squash→line→grow,
   flip, dot hand-off, wipe direction continued, a streak that carries the eye. Avoid hard cuts, and avoid crossfading everything.
10. **Sync to the audio.** Lyrics and VO words land on their syllable (±2 frames); hero landings on the beat/stress.
    Sound cues come from the same times (`engine/cues.js`, `workflow/10_sound_layer.md`).

---

## 1 · Roles (hierarchy)
| role | size (1080-wide frame) | weight / face | motion energy | typical moves |
|---|---|---|---|---|
| **Hero** | 55–75 % of frame width (≈200–300 px font) | display (Mirza, Lalezar, Rakkas, Aref Ruqaa, Katibeh) | strongest; spring `pop`/`card` | grow-from-dot, pop 80→108→100, flip, unsquash, blur-in, zoom-through |
| **Supporting** | 25–40 % of hero size (≈60–90 px) | light UI face (Kufi 300–400, Readex, Tajawal) | quiet: rise 30–60 px, fade 9–14 f | rise, swing on a hanger line, sequential vertical reveal |
| **Accent** | 1 word per line max | hero face in accent colour, or dark ink on an accent bubble | short & punchy | bubble pop, underline/bar, ring, comet, chroma hit |
| **Meta** | tiny | mono / UI | none | timestamps, artist tag, logo badge |

Composition on a 9:16 frame: heroes live between 30 % and 62 % of the height. Supporting text sits 1.2–1.6 × the
hero's height away. A logo badge or static frame ornament (when the brand has one) stays fixed and quiet in a corner.

---

## 2 · Move dictionary → engine call
`KT.show(word, t, {x, y, t0, t1, in, out, …})` returns the live box `{x, y, w, h, left, right, top, bottom}`, so
partner shapes can attach to the word as a parented unit.

### 2.1 Entrances (`in:`)
| move (EN / AR) | what it looks like | `in` | default timing |
|---|---|---|---|
| Opacity-Position combo / ظهور مع إزاحة | rises 30–120 px while fading in | `rise` / `fall` / `slide` (+`dir`, `dist`) | spring card, fade 9 f |
| Scale pop with overshoot / نبضة | 80 % → 108 % → 100 % | `pop` (spring `pop`) | settles ≈ 0.35 s |
| Leader dot → word / النقطة القائدة | a dot appears, swells, the word grows from its spot as the dot collapses | `KT.leader()` + `in:'grow'` | dot 0.4 s, hand-off 6 f |
| Blur-in / ظهور من الضبابية | defocus 16 px → sharp, 108 % → 100 % | `blur` | 0.45–0.6 s expo |
| Zoom-through / الاقتحام | 220 % + blur → 100 % (camera passes through) | `zoom` | 0.35 s |
| Mask reveal (baseline) / كشف بالقناع | rises out of its own line, clipped | `mask` / `drop` | spring card |
| Horizontal wipe RTL / مسح أفقي | soft-edge reveal right→left (reading direction) | `wipe` (`dir:'rtl'`) | 0.3–0.5 s |
| Vertical mask reveal / كشف عمودي | reveal top→down / bottom→up | `vwipe` (`dir`) | 0.3–0.5 s |
| 3D card flip / قلب البطاقة | rotateY with a slight perspective skew | `flip` (single word) / `KT.group({flip})` (a unit) | 0.4–0.55 s in-out |
| Spin-in / دوران دخول | from −90° and 55 % scale | `spin` | spring card |
| Stand-up hinge / الوقوف | lies down from vertical, hinged on its first letter | `stand` (`pivot`) | spring card |
| Hanging swing / الكلمة المعلّقة | hangs on a thin connector line and swings to rest | `swing` + `KT.line` | spring `swing` (k170 d9) |
| Grow from a line / النمو من الخط | a line opens into a word (sy 0→1, sx 150→100 %) | `unsquash` | spring pop |
| Emerge from behind a line / الخروج من خلف الخط | the word slides out of a hinge line (clipped at the line) | `fromLine` (`lineX`, `side`) | 0.5 s expo |
| Kashida tracking-in / تمطيط الكشيدة | the word arrives stretched and tightens (or opens up) | `track` or `keys:[[t,n],…]` with `KT.stretch` | 0.25–0.6 s |
| Echo / ghost stagger / الصدى | 2–3 ghosts trail the hero by 2–4 frames at 20–60 % opacity | option `echo:{n, lag, a}` on any entrance | — |
| Hard appear + punch / قطع مع نبضة | instant, 110 % for 2 frames (comedy, dialect, impact) | `cut` | 2 f |

### 2.2 Holds (options on `KT.show`)
| behaviour | option | values |
|---|---|---|
| Soft drift / انجراف ناعم | `drift:[vx, vy]` px/s | 6–20 px/s, opposite to the next word's arrival |
| Alternating vertical drift | `drift:[0, ±8]` alternating word to word | — |
| Micro wiggle / اهتزاز دقيق | `wiggle:{deg, px, f}` | 1–2°, 2–4 px, 0.6–1 Hz (never > 2 Hz) |
| Breathe | `breathe: .015` | 1–2 % |
| Dim to grey before exit / الخفوت | `dimAt, dimDur` (colour `FILM.kt.dim`) | 0.3–0.4 s, 0.2–0.5 s before the exit |
| Chroma hit / انقسام لوني | `chroma: px` (decays 0.25 s after landing) | 3–8 px; percussive words only |
| Glow | `glow, glowColor` | rarely; never on UI |

### 2.3 Exits (`out:` with `t1`, `outDur`)
| move | `out` | notes |
|---|---|---|
| Fade / dim | `fade`, `dim` | dim keeps the word as a grey "memory" |
| Sink / lift (trailing exit) | `sink`, `lift` | follow-through: the word leaves after its shape |
| Directional push | `push` (`outDir`, `outDist`) | continues the eye path into the next word |
| Spin-out | `spin` | rotate + shrink (as in the reference «مـــن» → next word) |
| Squash to line / الانضغاط إلى خط | `squash` | then a line or the next word `unsquash`es from it |
| Flip, wipe (continues the reveal direction), mask, blur, zoom | `flip`, `wipe`, `mask`, `blur`, `zoom` | — |

### 2.4 Partner shapes (the motion pair)
| partner | call | grammar |
|---|---|---|
| Dot | `KT.dot(t, t0, x, y, r, {t1})` | lead-in, punctuation, a "period" that lands after the word |
| Leader | `KT.leader(t, t0, x, y)` → returns hand-off time | dot → word hand-off |
| Comet (dot leading a trim path) | `KT.comet(t, t0, cx, cy, rx, ry, {sweep, dir, tailLag})` | a dot draws an arc around a word, the tail catches up and vanishes |
| Ring / circle draw-on | `KT.ring(t, t0, cx, cy, r, {t1})` | Trim Paths start 0→100 in 0.3–0.8 s, draw-off continues the same way |
| Underline centre-out | `KT.underline(t, t0, x, y, w, {from, t1})` | grows from the centre; exits towards the reading end |
| Highlight bar passing behind | `KT.bar(t, t0, x, y, w, h, {dir, t1})` | wipes in behind the word, then wipes OUT in the same direction |
| Connector / hanger line | `KT.line(t, t0, x1, y1, x2, y2)` | links a supporting word to its hero |
| Hinge line | `KT.hinge(t, t0, x, y, len, {keys})` | an accent line that pivots; words emerge from behind it |
| Bubble | `KT.bubble(t, t0, x, y, r, {t1})` | filled accent disc behind a key word (dark ink on top) |
| Window panel | `KT.panel()` + `KT.clipTo(box, fn)` | a translucent rectangle; words pass *through* it (visible only inside) |
| Orbit strokes | `KT.orbit(t, t0, cx, cy, r)` | rotating accent strokes keep a long hold alive |
| Light streak wipe | `KT.streak(t, t0, {angle, width})` | 0.2–0.5 s additive band, a transition accent |
| Foreground bokeh | `KT.bokeh(t, {n, alpha})` | only over photo/footage backgrounds; on pure black it reads as dirt (banned) |
| Parent / null object | `KT.group(t, {x, y, rot, sc, flip, swing, drift}, fn)` | the whole pair moves as one unit |

---

## 3 · Transitions between words/lines (black stage)
| transition | use | engine |
|---|---|---|
| Cut on the beat | rap and fast lines; only when the new word has a strong entrance | `in:'cut'` |
| Crossfade | slow ballads, at most 0.3 s, never as the default | `out:'fade'` + `rise` |
| Directional push | the next word continues the exit vector | `out:'push'` + `in:'slide'` (same dir) |
| Mask wipe | premium, editorial | `out:'wipe'` → `in:'wipe'` |
| Light wipe | emotional peak, chorus entry | `KT.streak` over the swap frame |
| Echo transition | the old word leaves ghosts that become the new word | `echo` + overlap 4–6 f |
| Card flip | binary pairs (question/answer, before/after) | `KT.group({flip})` with `face` |
| Squash → line → grow | a word "collapses" into the next | `out:'squash'` → `KT.line` → `in:'unsquash'` |
| Dot hand-off | quiet intimacy | `KT.dot` exit → `KT.leader` |

---

## 4 · Timing table (30 fps; from the report, verified on the references)
| parameter | value | note |
|---|---|---|
| fade in | 6–14 f (0.2–0.45 s) | the shorter the word, the shorter the fade |
| slide distance | 30–120 px | supporting 30–60, hero 60–120 |
| scale pop | 80 → 108 → 100 % | spring `pop` = k260 d15 |
| hold | 0.8–1.5 s | up to 2 s on the song's title word |
| echo | 2–3 copies, 20–60 % opacity, lag 2–4 f | fade the trail fast |
| wiggle | 1–2° or 2–4 px | 0.6–1 Hz |
| light streak | 0.2–0.5 s | once per section, not per word |
| trim path (ring/comet) | 0.3–0.8 s | in-out cubic |
| shape ↔ text offset | 2–6 f | shape first on entrances, text first on exits |
| underline after word | 4–8 f | centre-out expo |
| exit | 0.2–0.4 s | ease-in |
| word-to-word overlap | 2–6 f | `KT.timeline({overlap})` |
| card flip | 0.4–0.55 s | in-out cubic, back face swaps at 50 % |

**Springs** (`KT.SP`): `card` k150 d19 (default land) · `snap` k320 d28 (fast, tiny overshoot) · `pop` k260 d15
(≈8 % overshoot) · `soft` k60 d15 (slow, avoid for heroes) · `swing` k170 d9 (hanging/pendulum) · `glide` k90 d19.

**Easing rules** (from the report): entrances use ease-out or spring; exits use ease-in; never use linear for position.
Lines and trim paths use in-out. Holds use only noise and sine (no keyframe jitter). Overshoot is for scale, not for position on long distances.

---

## 5 · Motion Pair: text + its shape (core of the report)
**Principle:** the text is the *primary motion*, the shape is the *secondary motion* (it reacts, leads or trails),
and a *matte* (mask/window) can be a third layer that only reveals.

| pattern | how | rule |
|---|---|---|
| Dot/circle behind the word | the dot pops 2–4 f **before** the word, holds behind/beside it, exits **after** the word | lead in, trail out |
| Bar passing behind | the bar wipes in, the word appears over it, the bar continues out in the same direction | direction never reverses |
| Shape wipe-out | the shape sweeps across and takes the word with it (mask exit) | the word's exit = the shape's pass |
| Follow-through | the shape trails the word by 2–6 f, and lands with a softer spring | offset + softer spring |
| Parented unit | text + shape inside one `KT.group`; the group moves, the children keep micro-offsets | the group carries the big move |

**Recipes (from the report, generalised):**
- **A · Circle exit:** the word holds, a ring draws around it (0.5 s), then the word shrinks into the ring's centre
  (out `spin`/`zoom`) and the ring draws off 3 f later.
- **B · Bar reveal + wipe:** `bar` wipes in RTL (0.3 s), the word `wipe`s in 3 f later; on exit the bar continues
  left and the word `wipe`s out in the same direction 2 f before the bar finishes.
- **C · Word through a window:** a `panel` opens, the word `slide`s across *inside* `KT.clipTo(panel)`, and the
  panel closes after the word has left.
- **D · Circle draw-on:** a `comet` dot lands, then leads a trim path around the word. The tail catches up and the
  head dot vanishes as the word starts dimming.

**Motion-pair timing:** shape in −2…−4 f · text in 0 · text settled +8…12 f · shape settled +10…16 f · text out at T ·
shape out at T+2…6 f. **Never the same frame.**

---

## 6 · Kashida: Arabic tracking done right
- `KT.kashida('ما انام', 3)` → `مـــا انـــام` inserts tatweel only at **legal joints**: after a dual-joining
  letter, before a following Arabic letter, skipping harakat, and **never inside lam-alef** (لا).
- `where:'last'` (classic, before the final letter) · `'spread'` · `'all'`.
- Animated tracking: `const V = KT.stretch('تتحرّك', style, 4)` then `KT.show(V, t, {keys: [[t0, 0], [t0+.25, 4], [t0+.7, 1]]})`.
  It springs between variants. The steps blend under the 2-sub-frame motion blur.
- Use it on **long vowels and emotional words** (the singer stretches them). It's the Arabic equivalent of a
  tracking animation. Never apply it to every word.

---

## 7 · Reference grammar (what the 3 analysed videos actually do)
Detailed in `examples/reference_dna/kinetic_lyrics/DNA.md`. Grammar worth keeping, as moves to *recombine*, not shots to copy:
- **Leader dot → word.** The dot grows and the word replaces it on the same spot (intimate opening).
- **Spatial choreography.** Every word lands in a new place in the frame; nothing repeats the centre.
- **Hanging word** on a thin vertical line, swinging into place under its hero.
- **3D card flip** of the hero+hanger unit to the next word.
- **Squash to a line → the next word grows from the line.**
- **Kashida stretch** (`مـــن`), then a **spin-out** while the next word pops in growing.
- **Dim to grey** before exit (the word becomes a memory).
- **Comet:** a dot leads a trim path around the word (half-circle), then leaves.
- **Hinge line:** an accent line; a word slides out from behind it, the line tilts, the next word answers on the other side.
- **Bubble** behind the key word; **accent strokes orbiting** a held word; **vertical stand-up** of a word lying on its side.
- **Chroma split** on percussive syllables; **translucent panels** flashing as windows; light streaks and bokeh *over footage*.

---

## 8 · Workflows mapped (for users coming from After Effects / CapCut)
| After Effects | CapCut | Motion-Doc Studio |
|---|---|---|
| Text animator (Opacity + Position, Range Selector by words) | "Text → Animation → In: Fade/Rise" | `KT.show(word, t, {in:'rise'})`, one word object per word |
| Scale keyframes 80/108/100 with Easy Ease | "Pop" / "Bounce" in | `in:'pop'` (spring `pop`) |
| Track matte (alpha) on a rectangle | Mask → Linear | `in:'wipe'`/`'mask'`, `KT.clipTo(panel)` |
| Trim Paths on an ellipse | Shape + "Draw" | `KT.ring`, `KT.comet` |
| Echo effect / duplicated layers with offset | Duplicate + delay | `echo:{n, lag, a}` |
| Wiggle expression `wiggle(1, 3)` | "Shake" (too strong) | `wiggle:{deg, px, f}` (simplex) |
| Parent to Null | Group / compound clip | `KT.group()` |
| Motion blur switch | — | `render.mjs --sub 2` (default) |
| Light Leak / Optical Flares | overlay stock | `KT.streak`, `fxLeak`, `fxBloom` |

---

## 9 · Creative adaptation, not copying (for any agent)
1. **Derive the moves from the words' meaning.** A word for *falling* falls (`fall`, `drop`); *breathing* grows from
   a line; *returning* comes back through a flip; *distance* travels across the frame with a hinge between; *memory*
   dims; *heart* sits inside a bubble. Write a one-line verb for every hero *before* choosing a move.
2. **Pick a motion persona per film** (`library/easing_timing.md §0`): *intimate* (leader dots, blur, swing,
   slow drift), *punchy* (cut+punch, chroma, pop, push), *editorial* (wipes, bars, hinges, grid placement) or
   *dreamy* (blur, echo, glow, orbit). Use only 6–9 moves per film. Repetition with variation builds a style; 20
   different moves look like a demo reel.
3. **Recombine.** Each beat = (entrance) × (partner) × (hold) × (exit → next entrance). Change at least two of the
   four from the reference you were given. Never re-create a reference frame's layout, colours and words together.
4. **Escalate.** Verses quieter (rise, fade, small partners); chorus bigger (pop, flip, streak, accent bubble);
   last line the strongest (or the quietest, by contrast). Optionally make each repeated word slightly bigger.
5. **Anticipation and overlap.** For big moves, add a 2–3 f counter-move (scale 97 %, or 6 px the other way)
   before the action. Let partner shapes overlap the word's motion by a few frames instead of waiting.
6. **Arcs.** Long translations travel on a slight curve (combine `slide` with a `drift` on the other axis or a group rotation).
7. **Critique like a director:** contact sheet every 0.3–0.5 s, plus a full-fps strip over every transition. Check:
   is anything frozen? Is anything moving without a reason? Is there one hero per moment? Do shape and text share a start frame?
   Is everything inside the safe margins? Is every word legible for ≥ 0.8 s?

## 10 · Banned in kinetic films
Per-letter Arabic animation · letter-spacing on Arabic · everything fading in the same way · centred title on a gradient ·
generic particles/bokeh on pure black · glow on UI · bouncing at > 2 Hz · random rotation · words smaller than
34 px · two accent colours fighting · shape and text starting on the same frame · holds shorter than 0.8 s ·
crossfade as the only transition · copying a reference's layout + words + colours.

## 11 · Quick start (kinetic film)
```bash
tools/new_film.sh /var/tmp/my-lyric --kinetic --aspect 9:16    # engine + kinetic.html + scenes/kt_demo.js as template
cd /var/tmp/my-lyric/film && PAGE=kinetic.html ../tools/cs.sh look 6 0.5 1.5 3 4.5 6 7.5   # contact sheet
PAGE=kinetic.html node ../tools/render.mjs --from 0 --to 10 --draft     # 1.6 s per film-second preview
PAGE=kinetic.html node ../tools/render.mjs --from 0 --to 10 --workers auto   # final, motion-blurred
```
Lyrics or VO with timings → `KT.timeline(words)` → one `KT.show` per word inside a few `SHOTS` (one per line or section).
