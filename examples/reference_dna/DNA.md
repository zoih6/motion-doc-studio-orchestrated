# Reference DNA — "Sticker-Pop Dialect Ad" (source: zoih6/1000757841-video)

> **What this is:** a forensic breakdown of a 20-second Arabic (Egyptian dialect) app commercial.
> It records the *grammar* (rhythm, layout, type system, motion, transitions, palette roles, sound) so you
> can reuse it on **new** content. It is **not** a template to copy: do not reuse the character, the
> brand, the jokes, the script or the exact layouts. The original video is not stored in this repo.
>
> Measured with `tools/video_dna.py` → `measured_report.md`, `metrics.json`. Visual evidence:
> `contact_0-10s.jpg`, `contact_10-20s.jpg` (4 fps), `keyframes.jpg`, `shots.jpg`.
> Ready-to-use preset built from it: `library/style_presets.md` → **F · Sticker-Pop Dialect Ad**.

---

## 1 · Format
- Delivered as 720×1280 (9:16) but the picture is a **16:9 frame letterboxed** inside it (active ≈720×406).
  Lesson: master in 16:9 and re-stack for 9:16 instead of shipping black bars (see `library/camera_language.md §7`).
- 30 fps, 20.4 s, **8 shots, mean 2.55 s**, but on-screen text changes every **≈0.5 s**
  (2.16 audio onsets/s). Shots are long-ish; *inside* each shot something new happens every beat.

## 2 · Beat map (measured times)
| t (s) | shot / register | what happens | transition in |
|---|---|---|---|
| 0.00–0.20 | dark → cream | 3-frame light/dark flicker + tiny "psst" bubble = **hook in 0.2 s** | strobe |
| 0.20–1.47 | **cream**, character bottom-left (medium) | character pops in (≈0.3 s, motion-blurred, overshoot); caption word-by-word; emphasis word in teal hand-lettering + sparkle; mono "// code-comment" tag above the caption | cut |
| 1.47–2.57 | **dark, warm under-light**, extreme close-up | mood switch for the set-up line; "…" grows on the caption | hard cut |
| 2.57–4.03 | cream, character small corner | phone rises from below (0.3 s); caption + emphasis question word; hand-drawn circle starts on one icon | hard cut |
| 4.03–4.33 | → macro | **punch-in zoom** (9 frames, heavy motion blur) into the circled icon | zoom-through |
| 4.33–5.33 | cream macro | big exclamation word with **teal offset extrude**; hand circle finished around a blurred red dot | — |
| 5.33–9.73 | **split screen** (3 rounded panels) | teal panel = character, dark panel = phone feed scrolling, caption card = words; card **colour-strobes** cream→yellow→ink on the beat (6.6–7.6 s, every 3–4 frames); props fall onto the phone; thought bubble "…?" | cut + panels build (8 f) |
| 9.73–9.93 | → cream | 6-frame slide/whip | whip |
| 9.93–12.23 | cream type shot | word with RGB-style echo → **smear-morph (6 f)** into the coined word: big teal hand-lettered + extruded, **mono dictionary gloss** (`in·spi·ra·tion`) under it; polaroid stickers pop around in a stagger; character slides in bottom-**right** (the only side switch) | smear |
| 12.23–14.90 | **teal** full-bleed | character + phone slide in with blur (5 f); caption word-by-word; icon flies in; **3-frame white flash** on the punch word; orbit ring + sparkles + flying object | cut, flash |
| 14.90–16.80 | **dark under-light**, extreme close-up, slow push | menacing grin + hand-lettered question = the emotional peak | hard cut |
| 16.80–20.40 | cream **end card** | logo word builds, app icon with pin drops, tagline, CTA pill with outer ring, bubble from character, stickers scatter, **cursor glides in and clicks** (ripple) — builds in ≈1 s then holds 3 s alive | cut |

## 3 · Palette (k-means, 10 clusters) and roles
| role | hex | coverage | OKLCH |
|---|---|---|---|
| light neutral (60 %) | `#f8f4e9` cream + `#e5e4d5` panel grey | 46 % | L .97 / .92, C ≈ .02, warm hue |
| dark neutral (30 %) | `#1c1917` ink + `#080706` night | 31 % | L .22 / .13 |
| **accent (10 %)** | `#05a1a2` teal | 11.6 % | L .64 C .11 H 196 |
| pop accent (≤1 %) | `#f8bb3e` yellow | ≈1 % | used once, on the beat strobe |
| skin / character | `#cc8b47`, `#684832`, `#c6b2a2` | 8 % | warm hues 56–65 |

Lessons: one cool accent against warm neutrals (complementary temperature); neutrals are **tinted** (warm
cream, warm black) — never pure #fff/#000; the second accent is rationed to a single moment.

## 4 · Typography system
- **Caption face:** heavy geometric Arabic sans, black on cream / white on dark, word-by-word.
- **Emphasis face:** hand-lettered brush/ruq'ah style in the accent colour for the *one* key word of each line
  (the word that carries the joke or the feeling). Sometimes with a sparkle or a hard extrude.
- **Display/coined words:** hand-lettered + flat teal **offset extrude** (sticker-3D), very large.
- **Meta layer:** small monospace Latin/Arabic "code comment" tags (`// …`) and dictionary glosses — adds a
  nerdy, internet-native voice for almost no space.
- **Rebus:** tiny icons replace or follow words (moon/sun pictograms in rounded squares inside the caption).
- Captions sit in the empty side opposite the character; text never overlaps the face.

## 5 · Character treatment
- One pixel-art character (crisp nearest-neighbour edges) on flat vector UI → texture contrast that reads instantly.
- Anchored to the **bottom-left corner** in almost every shot; its **shot size** changes instead
  (corner-small → medium → extreme close-up) — "one actor, many shot sizes" gives cinematic variety cheaply.
- Expressions/poses change per line (smile, wink, closed eyes, grin) — the character *acts* the VO.
- Two lighting registers: flat bright (info/comedy) vs dark warm under-light (suspense/punchline).

## 6 · Motion grammar
- Entrances 0.17–0.30 s with motion blur and small overshoot (≈5–10 %) → **snap** spring family.
- After a hard cut the new content still *arrives* (character/phone slide-up) — cuts never land on a static frame.
- Camera: mostly locked; one **punch-in zoom** and one **slow push** on the dark beat. Movement is in the
  elements, not the camera.
- Hold discipline: each line lands, holds ≈0.3–0.5 s, next word arrives — speech rhythm drives everything.
- Ambient life during holds: sparkle twinkle, cursor drift, sticker settle.

## 7 · Transition toolbox (all motivated, all ≤10 frames)
hard cut on a mood switch · 3-frame strobe (hook) · punch-in zoom-through with motion blur · whip/slide
(6 f) · smear-morph between two words (6 f) · 3-frame white flash on impact · colour strobe of a caption
card on the beat · panel build (8 f).

## 8 · Graphic vocabulary
hand-drawn circle around the target · offset/extruded words · speech & thought bubbles with hard shadow ·
polaroid stickers scattered with seeded rotation · pixel icons · rounded split-screen panels (r≈20 px,
even gutters) · orbit ring + 4-point sparkles · pill CTA with an outer ring · cursor + click ripple ·
phone mock with a scrolling feed.

## 9 · Sound
VO-led (voice band 50–80 % of energy) with a light bed; bed swells at the end card (bass share 0.17→0.26).
Integrated −14.6 LUFS (good), but true peak −0.3 dBFS (too hot — we keep ≤ −1.5). One audible breath/
silence (2.40–2.61 s) right before the first reveal = tension gap.

## 10 · Adopt vs. don't copy
| ADOPT (grammar) | DON'T COPY (content) |
|---|---|
| hook ≤0.3 s; text beat every ≈0.5 s; shots 2–3 s | the grandmother character, her look/tattoo |
| bright ↔ dark-under-light register switch for punchlines | the brand, logo, app name, UI |
| one character, many shot sizes, fixed anchor corner | script, jokes, dialect lines, coined word |
| caption face + hand-lettered accent word + mono meta tag | exact layouts/frames |
| 60/30/10 tinted neutrals + one cool accent + rationed pop colour | |
| ≤10-frame motivated transitions (zoom, whip, smear, flash, strobe) | |
| end card that builds in 1 s and stays alive (cursor/click) | |

## 11 · Engine mapping (engine/fx.js)
| DNA element | call |
|---|---|
| word-by-word captions, VO-synced | `layoutWords()` + `drawWords(…, {mode:'pop'|'type', times: voTimes(…)})` |
| hand-lettered accent word | `layoutWords('… *word* …', {accent:{font:'Ruqaa', color:PAL.teal}})` |
| offset extrude / echo | `extrude(img, 12, .8, PAL.teal)`, `echo()`, `rgbSplit()` |
| hand circle | `handCircle(cx, cy, rx, ry, k)` |
| punch-in / whip / smear / flash / strobe | shot `tin: 'zoom'` (+`focus`) / `'whip'` / `'smear'` / `'flash'`; strobe = alternate fills on beat frames |
| split screen | `panel(x, y, w, h, t, t0, {fill, from, content})` |
| bubbles, CTA, cursor | `bubble()`, `pill()`, `cursor()`, `ripple()` |
| stickers | `polaroid()`/`outline()` + `scatter()` + `sticker()` |
| pixel character crispness | `pixelate()`, `drawCrisp()`, `sprite()` |
| dark under-light beat | radial warm gradient + `LOOKS.film`, `cam({z})` slow push + `handheld()` |
| impact | `burst()`, `impact()` added into `cam()`, `sparkles()`, `ring()` |
