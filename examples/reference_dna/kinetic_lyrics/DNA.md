# Reference DNA — 3 Arabic kinetic lyric videos (text motion only)

Source: `zoih6/motion-text-videos-20261013` (`1.mp4`, `2.mp4`, `3.mp4`), supplied by the user with the report
«تحليل موشن النصوص فقط — باعتبار الخلفية سوداء». Measured with `tools/video_dna.py` and read frame by frame at full fps
(strips in this folder). **Purpose:** learn the grammar and rebuild it for new words. Never copy (see
`library/kinetic_type_motion.md §9`). The videos themselves are not redistributed here.

## Measured
| | 1.mp4 | 2.mp4 | 3.mp4 |
|---|---|---|---|
| frame | 720×720 (1:1), 30 fps, 41.4 s | 360×640 (9:16), 25 fps, 40.1 s | 360×640 (9:16), ≈30.3 fps, 30.8 s |
| background | pure black (82 % of pixels), static white frame + corner ornaments + logo badge | photo of a silhouette + light leaks/flares | photo of a figure on a hill + grain, bokeh, streaks |
| cuts | **0** (one continuous shot; all change comes from type motion) | **0** | **0** |
| palette | #000100 · #f7f9f4 (ink) · #451901/#250e02 (badge browns) · greys #4f4e47 | teal-greys #73888a #819495 · near-black | greens/greys · white ink · **orange accent** |
| loudness | −8.9 LUFS (loud master) | −24.0 LUFS | −12.0 LUFS |

**Key finding:** in all three videos the background is static or near-static and there are **no cuts at all**.
Every bit of rhythm comes from how words enter, hold, hand off and leave. That's why the text motion must be fluid
and continuous, and choppy cuts kill it.

## 1.mp4 (black stage, 1:1): `strip_v1_a.jpg`, `strip_v1_b.jpg`
- **Leader dot → word:** a small white dot appears, swells, and the word appears at the dot's spot while the dot fades (≈10–14 f).
- **Spatial choreography:** each word lands somewhere new (top-right, centre, lower-left…). Never the same spot twice in a row.
- **Hold wobble:** the held word («ماغبت») rotates ±1–2° slowly (micro wiggle), so it never freezes.
- **Hanging word:** a supporting word hangs below its hero on a thin vertical line, swinging into place.
- **3D card flip** (rotateY) of the hero+hanger group to reveal the next word.
- **Squash → line → grow:** a word squashes vertically into a horizontal line; the next word grows out of it.
- **Kashida tracking:** «مـــن» is stretched with tatweel, then **spins out** (rotation ≈90° + shrink, ≈8 f) while
  the next word («اللهفه») **pops in growing** (≈6 f).
- **Dim to grey** before exit.
- Static frame/ornaments/logo badge: brand furniture that stays fixed while the words move.

## 2.mp4 (photo background, 9:16): `strip_v2_a.jpg`
- **Kashida-stretched light words** at the bottom-left («مــا انــام», «انــا طــامع») in a thin face.
- **Stand-up rotation:** a word lies vertical, then rotates to horizontal (hinged on one end).
- **Chroma split (RGB fringe)** on the stressed syllables, decaying in a few frames.
- **Translucent grey rectangles** flash as windows/masks (matte layer).
- Small two-line lyric at top-left inside a rounded outline with a highlight bar («انا ميت في…»), a quiet secondary block.
- Red/white **underline draw** under «ياحنين».

## 3.mp4 (photo background, 9:16, orange accent): `strip_v3_a.jpg`, `strip_v3_b.jpg`
- **Comet trim path:** a white dot sits above «اروح», then travels along an arc, *drawing* a stroke behind it
  around the word (≈0.5 s), then leaves as the tail catches up.
- The next word enters **rotated 90° (vertical)** and spins to horizontal.
- **Hinge line:** a vertical orange line; «فوادي» slides out from behind it (clipped at the line), then the
  line **tilts** and «فيه» answers on the other side.
- **Bubble:** a filled circle behind «مسكن» with an orange accent; **rotating orange strokes** orbit «مفتون».
- A dot follows «ومن» (punctuation as motion).
- Words are placed *around the subject* (the figure is never covered).

## Grammar extracted → engine (`engine/type.js`)
| grammar | KT call |
|---|---|
| leader dot hand-off | `KT.leader` + `in:'grow'` |
| hanging word | `KT.line` + `in:'swing'` |
| card flip of a unit | `KT.group({flip})` |
| squash → line → grow | `out:'squash'` → `KT.line` → `in:'unsquash'` |
| kashida tracking | `KT.stretch` + `keys` |
| spin-out / pop-in | `out:'spin'` / `in:'pop'` |
| dim before exit | `dimAt` |
| comet trim path | `KT.comet` |
| hinge line + emerge | `KT.hinge` + `in:'fromLine'` |
| bubble / orbit strokes | `KT.bubble` / `KT.orbit` |
| stand-up rotation | `in:'stand'` |
| chroma hit | `chroma: px` |
| translucent windows | `KT.panel` + `KT.clipTo` |

**Recombined, not copied:** `examples/kinetic_demo/` uses the same grammar on new words, with a new layout, palette
and order (9:16, ivory + one orange accent, 10 s).
