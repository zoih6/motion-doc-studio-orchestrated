# Patterns & backgrounds — النقوش والخلفيات (Islamic geometry + graphic textures)

**Code:** [`engine/assets.js`](../engine/assets.js) §3 `pattern(kind, t, opts)` · **Sheet:** [specimens/patterns.jpg](specimens/patterns.jpg)
All kinds are procedural (no image files), deterministic, resolution-independent, and **draw-on able** (`k` 0→1 with seeded stagger).

| kind | العربية | geometry | use for |
|---|---|---|---|
| `star8` | الخاتم الثماني | {8/2} stars (two squares) on a square lattice + tip-to-tip bands | general Islamic ground, Rub el Hizb motif |
| `rosette` | الشمسة | star8 + inner {8/3} rosette + node circles | illumination, title cards, medallions |
| `star6` | النجمة السداسية | hexagram + hexagon on a triangular lattice with links | Levantine/Andalusian woodwork |
| `star12` | الاثنا عشرية | {12/5} stars on a hex lattice + inner dodecagon | Mamluk/Seljuk monuments |
| `girihNet` | شبكة الكريه | {10/3} decagonal stars on an offset lattice | Persian/Timurid girih strapwork |
| `mashrabiya` | المشربية | rotated squares + turned-wood rings | windows, screens, Hijazi/Egyptian houses |
| `dots` | نقاط | regular dot grid (pops in with back-ease) | VOX paper grounds |
| `halftone` | نقاط طباعية | dot size = tone (gradient, noise, or `tone(x,y)`) | riso, comics, print |
| `grid` / `lines` | شبكة / خطوط | ruled grid / parallel lines | blueprint, notebooks, scanlines |
| `waves` | أمواج | animated sine bands (`speed`, `amp`) | water, sound, desert wind |
| `iso` | شبكة متساوية القياس | 30° isometric lattice | isometric cities, data floors |
| `topo` | خطوط كنتور | marching-squares contours of animated fbm | maps, terrain, data landscapes |

```js
// gold 8-fold lattice drawing itself behind a title, at 10% strength
pattern('star8', t, { cell: 140, color: PAL.gold, lw: 1.4, alpha: .12, k: tw(t, 0.5, 3.5, CURVE.camera), stagger: .7 });
// a rotating rosette medallion clipped to a circle
g.save(); g.beginPath(); g.arc(960, 540, 300, 0, 6.283); g.clip();
pattern('rosette', t, { x: 660, y: 240, w: 600, h: 600, cell: 120, rot: t * .05, color: PAL.goldD }); g.restore();
// halftone shading driven by a radial tone
pattern('halftone', t, { cell: 22, color: PAL.ink, tone: (x, y) => 1 - Math.hypot(x - 960, y - 540) / 900 });
```
Rules: patterns are **ground, not subject**. Use alpha 0.06–0.18 behind content and full strength only as a dedicated "geometry" beat. Use one pattern family per film (it's part of the style bible).
Construction beats (a compass drawing a star, lines extending into a lattice) are a strong documentary hook: draw-on `k` with `CURVE.camera`, then hold.
