# Kinetic typography (Arabic-first)

> **v2.1:** for lyric videos, quotes, text-only films and any expressive text motion use the pro system
> `library/kinetic_type_motion.md` + `engine/type.js` (motion pairs, kashida tracking, 20 entrances / 12 exits).
> This file stays the reference for VO captions inside documentaries (`layoutWords/drawWords`).

Code: `engine/fx.js` §7 — `layoutWords`, `drawWords`, `voTimes`, `letters`, `maskReveal`, `marker`,
`blurSwap`, `weightText`; §5 `extrude`, `echo`, `rgbSplit`, `outline`; core `textImg`, `writeOn`, `card`.

## 0 · The Arabic rule
Arabic letters **join**. Splitting a word into letters breaks shaping (isolated forms, broken ligatures).
- Animate **per word** (`layoutWords` keeps each word whole) or reveal whole lines with masks/write-on.
- Per-letter stagger is for Latin only (`letters()`).
- Canvas: `direction = 'rtl'`, an Arabic font loaded from a local file, wait for `document.fonts.load`.
- Diacritics (tashkeel) need extra line height (×1.45 box in `layoutWords`); never clip them in masks.
- Numerals: choose Arabic-Indic (٠١٢) or Western (012) once per film (`counter(..., {arabic})`).

## 1 · Roles (max 3 faces + 1 meta)
| role | job | example fonts (library/fonts.md) |
|---|---|---|
| caption | carries the VO words, highly legible, heavy | Noto Kufi 800, Readex Pro 700, Changa 700 |
| emphasis | the ONE key word of the line, in the accent colour | Aref Ruqaa Bold, Marhey 700, Rakkas |
| display | titles, coined words, logos | Lalezar, Amiri Bold (heritage), El Messiri 700 |
| meta | tiny tags, glosses, code comments (`// …`), sources | IBM Plex Mono |
Markup: `layoutWords('عارف *البرنامج* ده؟', { font: UI, weight: 800, accent: { font: 'Ruqaa', color: PAL.teal, size: 110 } })`.

## 2 · Entrance modes (`drawWords(L, t, t0, x, y, {mode})`)
| mode | motion | persona |
|---|---|---|
| `pop` | scale .6→1 + tiny alternating rotation, snap spring | playful, sticker-pop |
| `rise` | +60 px → 0, fade | corporate, clean |
| `mask` | each word rises out of its own clip line (expoOut) | premium, cinematic titles |
| `blur` | blur 14→0 + scale 1.08→1 | premium, dreamy |
| `slam` | scale 2.4→1 in 0.22 s | energetic, punchlines (add `impact()`) |
| `type` | instant appear with 1.12 punch for 2 frames | dialect/comedy captions, quotes |
| `drop` | falls from above with wobbly spring | kids, playful |
| `swing` | hinged swing settle (jelly) | signs, labels |
Exit: `t1` + `exit: 'fade' | 'up'` (exits are faster than entrances).

## 3 · Sync to the voice
```js
// WORDS = [{w, s, e}] from tools/transcribe.py (docs/vo_word_timings.json)
const L = layoutWords('تعال يا *ولدي*', { size: 84, accent: { font: 'Ruqaa', color: PAL.teal } });
drawWords(L, t, 0, 1320, 420, { mode: 'pop', times: voTimes(WORDS, 0.25, 3), hiColor: PAL.teal });
```
Word appears when it is spoken (±0.15 s). `hiColor` = karaoke highlight of the current word.

## 4 · Technique dictionary
| technique | how | when |
|---|---|---|
| write-on RTL | `writeOn(img, x, y, k)` soft edge | documentary captions, names |
| mask reveal | `maskReveal(img, x, y, k, {dir:'up'})` | titles, lines of a quote |
| word-by-word pop | `drawWords(mode:'pop')` | dialect ads, social |
| karaoke highlight | `times` + `hiColor` | lyrics, emphasis on spoken word |
| emphasis swap face | `*word*` accent style | the joke/feeling word |
| highlighter sweep | `marker(x, y, w, h, k)` behind text | VOX explainer key facts |
| underline draw | `line()` / `pathDraw()` under the word | definitions |
| offset extrude | `extrude(img, 12, .8, teal)` | coined words, sticker titles |
| echo / RGB split | `echo()`, `rgbSplit()` | glitchy emphasis, "?!" moments |
| sticker outline | `outline(img, 10, '#fff')` | type as a sticker on photos |
| blur swap | `blurSwap(a, b, t, t0, x, y)` | change one word in place |
| smear morph | shot `tin:'smear'` | word → new word |
| weight morph | `weightText(s, lerp(300, 900, k))` (variable fonts) | emphasis growth, breathing titles |
| rebus | small icon/sprite placed after a word | ☀/☾, objects, emojis-as-glyphs |
| dictionary gloss | mono line under a word (`in·spi·ra·tion`) | coined / foreign words |
| meta tag | `// tag` in mono above the caption | witty narrator voice |
| counter / digit roll | `counter()`, `liveText()` | numbers |
| typewriter | words with `type` mode at speech rate | quotes, chat |
| type as frame | huge word fills frame, image inside the letters (clip to text) | chapter openers |

## 5 · Legibility rules
- Min caption 34 px @1080p (TS 1.3), contrast ≥ 4.5:1 (≥ 3:1 for display ≥ 60 px). Check with `contrast(a, b)`.
- Max ~7 words on screen per caption; 1–2 lines; never over a face.
- Don't loop-animate text while it is being read; animate in, hold, animate out.
- One emphasis word per line; one display moment per shot.
- Thin scripts and decorative faces only at display sizes; never for running captions.
