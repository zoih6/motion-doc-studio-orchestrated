# Fonts — 41 bundled OFL families, chosen by role · دليل الخطوط

**Bundled:** [`engine/kit/fonts/`](../engine/kit/fonts/) — 48 files, all **SIL OFL 1.1** (free for video, embedding and redistribution).
**Full table (file, weights, copyright):** [`engine/kit/fonts/README.md`](../engine/kit/fonts/README.md) · **Visual specimen:** [specimens/fonts.jpg](specimens/fonts.jpg)
**Registry in code:** `kit/fonts/fonts.js` → `FONT_REGISTRY`, `fontsBy('kufi')`, `fontLoads(['Cairo','Amiri'])` · **CSS:** `kit/fonts/fonts.css` (all `@font-face`, local files, no network).
Rebuild after adding a font: drop the `.ttf` in `engine/kit/fonts/`, add a row in `tools/build_fonts.py`, run `python3 tools/build_fonts.py`.

## 1 · Wiring into a film
```html
<link rel="stylesheet" href="kit/fonts/fonts.css">
<script src="kit/fonts/fonts.js"></script>          <!-- before core.js if you use fontLoads() in FILM -->
<script>window.FILM = { display: 'Qahiri', ui: 'Cairo', fonts: fontLoads(['Qahiri', 'Cairo']) };</script>
```
Canvas: `g.font = '800 72px "Cairo"'; g.direction = 'rtl';` — variable weights work directly in the font string (any value inside the axis range, e.g. `640`), which is how weight-pump / weight-morph effects work ([kinetic_typography.md](kinetic_typography.md)).
Colour fonts (`RuqaaInk`, `ReemKufiInk`) render their own built-in colours in Chromium (COLR), and `fillStyle` is ignored for those glyphs. Use them for one hero word only.

## 2 · The rule: one display face + one UI face (+ an optional emphasis face)
Pick by **genre of the subject**, then by **energy**. Never mix two display faces of different genres (e.g. Qahiri + Lemonada).

| role | what it does | best families |
|---|---|---|
| **Display: heritage** | titles for history, religion, manuscripts | `Amiri`, `Mirza`, `Scheherazade`, `ReemKufi`, `Qahiri`, `Ruqaa` |
| **Display: poetry/Persianate** | verses, Sufi, Persian/Urdu culture | `Nastaliq`, `Gulzar`, `Lateef` |
| **Display: monumental/architecture** | inscriptions, mosques, Mamluk/Fatimid topics | `Qahiri` (square kufi), `ReemKufi`, `Kufam` |
| **Display: modern explainer** | VOX-like, data, news | `Cairo` 800–1000, `Alexandria` 700–900, `Kufi` 900, `Changa` 700 |
| **Display: loud/poster** | hooks, slogans, sports | `Lalezar`, `Jomhuria`, `Changa` 800, `Blaka` (dramatic) |
| **Display: playful/kids/edu** | children, food, light topics | `Lemonada`, `Baloo`, `ReemKufiFun`, `Marhey` |
| **Display: retro/cinema** | old posters, nostalgia | `Rakkas`, `Katibeh`, `Vibes` (festive) |
| **Display: tech/LED** | scoreboards, digital, retro computing | `Handjet` (dot-matrix), `JetBrains` |
| **UI / captions** | labels, lower-thirds, subtitles | `Cairo`, `Tajawal`, `Almarai`, `Kufi`, `Readex`, `PlexArabic`, `Mada` |
| **Body / long quotes** | multi-line quotes, documents | `Naskh`, `Markazi`, `Scheherazade`, `Amiri` 400 |
| **Data / meta** | numbers, years, coordinates, sources | `PlexArabic`, `Mono`, `JetBrains`, `Inter` (Latin) |
| **Emphasis (one word)** | the word the VO stresses | `Ruqaa`/`RuqaaInk`, `Marhey`, accent colour of the display face |

## 3 · Tested pairings (display / UI / emphasis / meta)
| style (see [style_catalog.md](style_catalog.md)) | display | UI | emphasis | meta |
|---|---|---|---|---|
| Sepia manuscript | Amiri 700 | Kufi 600 | Amiri gold | Mono |
| Mamluk monument | Qahiri | Naskh 500 | ReemKufi gold | PlexArabic |
| Andalusian/Maghrebi | ReemKufi 700 | Harmattan 700 | Ruqaa | Mono |
| Persian poetry | Nastaliq 700 | Naskh 400 | Gulzar | — |
| Ottoman archive | Mirza 700 | Markazi 500 | RuqaaInk | Mono |
| Clean VOX explainer | Cairo 900 | Readex 500 | marker sweep | PlexArabic |
| Newsroom/data | Alexandria 800 | PlexArabic 400 | accent colour | JetBrains |
| Sticker-pop | Lalezar | Kufi 800 | Ruqaa accent | Mono |
| Kids/edu | Lemonada 700 | Almarai 700 | ReemKufiFun | — |
| Cartoon/edu | Baloo 800 | Tajawal 700 | Marhey | — |
| Retro cinema | Rakkas | Changa 600 | Katibeh | Mono |
| Dramatic/thriller | Blaka | Mada 500 | Jomhuria | JetBrains |
| Tech/LED | Handjet 700 | Cairo 500 | Handjet accent | JetBrains |
| Editorial essay | Markazi 700 | Mada 400 | Amiri | Inter |
| Luxury/premium | ElMessiri 700 | Readex 300 | Amiri 400 | — |
| Bilingual (AR+EN) | Alexandria / Cairo | Cairo + Inter | — | SpaceGrotesk |
| Latin-only promos | Fraunces / SpaceGrotesk | Inter | Fraunces italic-ish (WONK) | JetBrains |

## 4 · Arabic typography rules for motion
- **Never split Arabic into letters** for animation; shaping (joining forms) breaks. Animate **words** or use masks/clips ([kinetic_typography.md](kinetic_typography.md)).
- Set `g.direction = 'rtl'` and `textAlign: 'right'` (the start edge). Measure with `measureText` *after* setting font + direction.
- Diacritics (tashkeel) need extra line height: ×1.5 for Naskh/Amiri, ×1.8 for Nastaliq (it hangs diagonally).
- Minimum caption size at 1080p: 34 px (Kufi/Cairo) and 40 px for Naskh (thin strokes).
- Kashida/tatweel (ـ) stretching is a valid kinetic move for Naskh/Kufi words. Don't use it on Nastaliq.
- Numerals: Arabic-Indic (١٢٣) for heritage pieces, Western (123) for data/news. Be consistent per film.
- Colour fonts and Nastaliq are slow to rasterise: cache them as images (`textImg()` in core) if drawn every frame.
