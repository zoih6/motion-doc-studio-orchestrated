# «الخط الواحد» — the ONE-LINE film grammar (engine: `engine/line.js`)

**One continuous line draws the entire film in a single unbroken take.** No cuts, no fades, no AI
images: a world laid out along a path; a keyed camera (LCAM) flies along it; the pen (LINE) keeps
drawing; fills bloom (BLOOM) where figures close; words are anchored in the world (wtext) so the
camera alone moves them. Pure function of `t` — build once in `WORLD.build`, read forever.

Reference production: `examples/one_line_reel/` (Lamset Shifa v3, 64.8 s vertical reel).

## When to use
Brand films, reels, "one-line art" requests — whenever the user wants something pure, premium and
handcrafted-feeling with NO photo assets. Vertical or square works best (the camera reads like a
helicopter over a map).

## The five-act grammar that worked (adapt, don't copy)
1. **Touch** (0–5 s, the hook): the line is born from one dot; small steps that GROW with «بداية لتغيير كبير» → hero word as a CUT.
2. **Identity** (5–16 s): the line circles the promise, climbs to a star, closes into the seal; subtitles written by the pen itself (wpen underlines); a fingerprint spiral = "every case is unique".
3. **Services** (seed → sprout → stations): the seed blooms, a sprout grows, and each service is a ring the pen draws + a Lucide icon it sketches (`LINE.icon`) + a two-line label (small mint over larger cream, alternating sides along the trail). End the act with a symbolic figure (infinity) that FILLS with meaning (spectrum bloom on the word).
4. **Care** (care = measured steps → heart → home around it → growth chart with arrow → sun of a new day) → **THE REVEAL**: camera pulls back until the whole film is one glowing path on screen; an editorial column speaks beside it; a light pulse runs the whole path; hero line lands as a CUT + FLASH.
5. **Contact & end card**: dive back to the pen; a pin for the address; the seal again; phone numbers written LTR (`wpenL`) with underlines; then a SEPARATE studio outro shot (cut to a new world, colour arcs sweep, badge springs in).

## Non-negotiable mechanics (each one cost us a failure)
- **Pen schedule is a choreography, not an afterthought**: draw the connector fast (5–8× figure speed), land at the figure, slow down. Pattern: `LINE.key(t0, markOfPreviousEnd)` then `key(t1, 'figA', 'io')`, `key(t2, 'figB', 'io')`.
- **In-world texts collide across scenes.** Keep ≥ ~300 world units between text blocks of adjacent scenes and scrub through the boundary. A text that appears before the camera arrives looks broken — set `t0` to the VO word AFTER arrival.
- **Heroes must register in ONE frame** (sound QA `appear` gate): use `in:'cut'` (or a hard BLOOM) + push the frame to `window.FLASH` + add `impact()` in the take's HITS. Eased rises FAIL the gate.
- **Fast pans ghost.** Distance-matched swoop keys (zoom out mid-move) + render with `--sub 6`. Never sub 2/3 for travelling shots.
- **Connectors never cross text.** Route around (far wall) or use `join:'lift'` with `liftWt:.02`.
- **Icons**: `LINE.icon(name, x, y, size, {c1,c2,dIn})` — the first element flows in from the connector, the rest are pen hops. Verify the icon name exists in the vendored Lucide set BEFORE using it.
- **Digits in RTL canvas reorder** → `ltrWord()` + `wpenL()` (left-to-right pen reveal).
- **The reveal camera** is a wide key far from the path axis (path becomes a spine on the left third, editorial column `ax:1` on the right). Hold with `hold:true`, then exit with `out:'lift'`.
- **`LINE.tf` maps POINTS, `LINE.sample` returns SUBS** — always `.map(sp => LINE.tf(sp, o))`. Feeding subs to tf injects NaN into the whole path (invisible world; `LINE.S` goes NaN).
- **End-card hygiene**: world text from previous scenes stays on screen unless the camera leaves it; give scene texts `t1/out:'sink'` before the card, or they hang half-cropped at the frame edge for the rest of the film.
- **Release encodes must match the film's orientation** (reels are portrait!) — `tools/encode_release.sh` decides by probing the master. A squished reel PASSES qa.py; check `ffprobe` dims yourself.

## API (module surface)
`LINE` — path: `start/add(subs,{join,c1,c2,dIn,k1,k2,liftWt})/fig/sample(d,step)/tf(pts,o)/mark/mark0/M/key(t,mark,ease)/head(t)/at(s)/stroke(s0,s1,{color,px,alpha,z,under,shadow,core})/bounds/icon(...)`.
`LCAM` — camera: `key(t,x,y,z,roll,hold)/at/set/apply/w2s/s2w/now` (Hermite, log-zoom; duplicate-t keys are forbidden — phase cuts by 1 frame).
`BLOOM.add({t0,dur,cx,cy,r,color,alpha,shape(c),t1,outDur})` — circular ink-spread clip over any shape.
Words: `wtext(W,t,{wx,wy,t0,in,…KT.show opts})`, `wpen/wpenL(W,t,s,k)` pen reveals driven by the line itself (`pk('ul1A','ul1B')` pattern).
Helpers: `SHAPES.circle/star`, `densify`, `leafD(L,w)`, `polyShape(subs)`.
Take shell (copy from the example): bg → blooms → under → dry line `#c7a75e` + gold trail + pen → over → screen → FLASH. `window.END_TAKE/FLASH/PEN_OFF/DRY/HITS`.

## Sound (works the same as any other film)
Cues export from the picture itself (`cue.appear/move/hero`). Heroes: thump+tap; support pops at drawn
elements, panned by side; camera flights: whoosh on `cue.move` spans; the reveal pulse: shimmer.
Keep music ≤ −28 dB under VO and let mix.py peak-align everything.
