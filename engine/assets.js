// ════════════════════════════════════════════════════════════════════
//  motion-doc-studio · assets.js — helpers over the vendored resource packs (load after fx.js)
//    <script src="kit/data/palettes.js"></script>      NICE_PALETTES (1000, MIT) + OPEN_COLOR (MIT)
//    <script src="kit/data/icons_lucide.js"></script>  LUCIDE (1877 icons, ISC)  – optional, ~560 KB
//    <script src="kit/fonts/fonts.js"></script>        FONT_REGISTRY (41 OFL families)
//  1 PALETTES  palette(i) · paletteRoles(p) · applyPalette(roles) · palettesBy(filter) · HERITAGE (original, named) · oc(hue, shade)
//  2 ICONS     icon(name, x, y, size, {color, lw, k, stagger, fill}) · iconSearch(q) · iconPath(name)
//  3 PATTERNS  pattern(kind, t, {…}) — Islamic geometric (star8, star6, star12, rosette, girihNet, mashrabiya)
//              + graphic backgrounds (dots, grid, halftone, lines, waves, iso, topo). All draw-on able via k.
//  Docs: ../library/color_systems.md §palette packs · ../library/icons.md · ../library/patterns.md
// ════════════════════════════════════════════════════════════════════

// ── 1 · PALETTES ─────────────────────────────────────────────────────
// Original curated palettes for documentary motion (roles already assigned; all ink/bg pairs ≥ 7:1, accent/bg ≥ 3:1).
const HERITAGE = {
  // name: [bg, ink, paper, accent, accent2, muted]  — inspiration noted; colours are our own picks
  sanaaOldCity:   ['#2a1b12', '#f3e6cf', '#e9d3ad', '#c8553d', '#f2c14e', '#8c6a4f'],  // burnt brick + white gypsum qamariya
  iznikTile:      ['#f4f1ea', '#13243a', '#ffffff', '#1f5fa8', '#c0392b', '#2e8b7a'],  // cobalt, tomato red, turquoise on frit white
  mamlukGold:     ['#121417', '#f1e2bd', '#e7d3a1', '#c9a14a', '#1e6f6a', '#5b4a2f'],  // gilded Qurans: gold + deep lapis-teal
  andalusZellige: ['#f6f0e2', '#1f2a2e', '#ffffff', '#0f7c6b', '#d38b2c', '#7c3b2a'],  // zellige green, ochre, terracotta
  damascusNight:  ['#0d1321', '#f0ebd8', '#e6dcc0', '#d4a373', '#748cab', '#3e5c76'],  // inlaid wood & mother-of-pearl at night
  ottomanManuscript: ['#efe2c4', '#2b1d14', '#f7eedb', '#8f1d21', '#2d5d7b', '#b08d57'], // ebru marbling, carmine, indigo
  desertDune:     ['#f2d7b6', '#3b2416', '#fbebd7', '#d9822b', '#5c7457', '#a86b3c'],  // Empty Quarter sand
  hijazCoral:     ['#e9e2d6', '#26313b', '#f8f4ec', '#4f8a8b', '#c56a4b', '#9aa7a3'],  // coral-stone houses of Jeddah
  saffronIndigo:  ['#14122b', '#f7eddc', '#ece0c8', '#f4a300', '#5b5fc7', '#463f6b'],  // dye trade
  palmyraStone:   ['#d9c7a7', '#2c2118', '#efe4cf', '#a14a2f', '#3a5a64', '#8f7a5c'],  // limestone & oxidised bronze
  nileReed:       ['#eef0e2', '#1d2a22', '#fbfcf4', '#3f7d4e', '#d89a2b', '#7a8f6a'],  // papyrus & river
  kufiBlueprint:  ['#0e2a47', '#e8f1fb', '#cfe0f2', '#ffcf5a', '#6fb7ff', '#3d5f84'],  // cyanotype drafting
  // modern documentary / explainer
  voxExplainer:   ['#f5f1e8', '#141414', '#ffffff', '#ffc400', '#e94b3c', '#9a9a9a'],
  newsroom:       ['#0b0d10', '#f2f4f7', '#d7dde5', '#e63946', '#4cc9f0', '#5c6773'],
  archiveSepia:   ['#1a120b', '#efe2c8', '#e8d7b2', '#c99a45', '#a8321f', '#7a6040'],
  riso:           ['#f3eee3', '#1b1b3a', '#ffffff', '#ff4f79', '#0078bf', '#ffe800'],
  neonNoir:       ['#07070c', '#eae6ff', '#c8c2f0', '#ff2e88', '#2de2e6', '#3a3a5a'],
  swissPoster:    ['#f2f2f2', '#111111', '#ffffff', '#e30613', '#111111', '#8a8a8a'],
  forestData:     ['#0f1a14', '#e9f2ea', '#cfe3d2', '#7bd389', '#f2c14e', '#4d6b57'],
  pastelEdu:      ['#fff7ed', '#2b2d42', '#ffffff', '#ef476f', '#118ab2', '#06d6a0'],
};
const heritage = name => { const [bg, ink, paper, accent, accent2, muted] = HERITAGE[name]; return { bg, ink, paper, accent, accent2, muted, name }; };
const palette = i => NICE_PALETTES[((i % NICE_PALETTES.length) + NICE_PALETTES.length) % NICE_PALETTES.length].slice();
// assign roles to any 5-colour palette: bg = darkest (dark:true) or lightest; ink = best contrast vs bg;
// accent = most chromatic colour with contrast ≥ 3 vs bg; accent2 = next; muted = the remaining lowest-chroma colour
function paletteRoles(p, { dark = null } = {}) {
  const info = p.map(h => { const [L, a, b] = rgb2oklab(hex2rgb(h)); return { h, L, C: Math.hypot(a, b) }; });
  const byL = info.slice().sort((a, b) => a.L - b.L), isDark = dark ?? (byL[0].L < .35);
  const bg = isDark ? byL[0] : byL[byL.length - 1], rest = info.filter(c => c !== bg);
  let ink = rest.slice().sort((a, b) => contrast(b.h, bg.h) - contrast(a.h, bg.h))[0];
  if (contrast(ink.h, bg.h) < 4.5) ink = { h: isDark ? '#f5f1e8' : '#141414' };
  const acc = rest.filter(c => c.h !== ink.h).sort((a, b) => (b.C + (contrast(b.h, bg.h) >= 3 ? 1 : 0)) - (a.C + (contrast(a.h, bg.h) >= 3 ? 1 : 0)));
  return { bg: bg.h, ink: ink.h, accent: acc[0]?.h || ink.h, accent2: acc[1]?.h || acc[0]?.h, muted: acc[acc.length - 1]?.h || bg.h, paper: isDark ? mixOK(bg.h, ink.h, .9) : mixOK(bg.h, '#ffffff', .5), dark: isDark };
}
// write roles into the engine palette PAL (keeps the house keys working: bg ink parch cream gold red …)
function applyPalette(r) { Object.assign(PAL, { bg: r.bg, ink: r.ink, parch: r.paper, cream: r.paper, gold: r.accent, goldL: mixOK(r.accent, '#ffffff', .35), goldD: mixOK(r.accent, '#000000', .35), red: r.accent2 || r.accent }); return PAL; }
// filter the 1000-pack: palettesBy({dark:true, minChroma:.12, hue:[20,70], minContrast:7}) → indices
function palettesBy({ dark = null, minChroma = 0, maxChroma = 1, hue = null, minContrast = 4.5 } = {}) {
  const out = []; NICE_PALETTES.forEach((p, i) => { const r = paletteRoles(p); if (dark !== null && r.dark !== dark) return; if (contrast(r.ink, r.bg) < minContrast) return;
    const [, a, b] = rgb2oklab(hex2rgb(r.accent)), C = Math.hypot(a, b), Hh = (Math.atan2(b, a) * 180 / Math.PI + 360) % 360;
    if (C < minChroma || C > maxChroma) return; if (hue && !(hue[0] <= hue[1] ? Hh >= hue[0] && Hh <= hue[1] : Hh >= hue[0] || Hh <= hue[1])) return; out.push(i); });
  return out; }
const oc = (hue, shade = 6) => { const v = OPEN_COLOR[hue]; return Array.isArray(v) ? v[shade] : v; };   // oc('teal', 7)

// ── 2 · ICONS (Lucide, 24×24 grid, stroke 2, round caps/joins) ─────────
const _p2d = {};
const iconPath = name => { const d = LUCIDE[name]; if (!d) throw new Error('assets.js: unknown icon ' + name + ' — try iconSearch()'); return _p2d[name] || (_p2d[name] = d.map(([s, len]) => [new Path2D(s), len])); };
// draw icon centred at (x,y) with size px. k = draw-on progress 0..1 (elements stagger in order); fill = optional fill colour
function icon(name, x, y, size = 96, { color = PAL.ink, lw = 2, k = 1, stagger = .35, fill = null, alpha = 1, rot = 0 } = {}) {
  const els = iconPath(name), sc = size / 24, n = els.length; if (k <= 0) return;
  g.save(); g.translate(x, y); if (rot) g.rotate(rot); g.scale(sc, sc); g.translate(-12, -12); g.globalAlpha *= alpha;
  g.lineCap = 'round'; g.lineJoin = 'round'; g.lineWidth = lw; g.strokeStyle = color;
  els.forEach(([p, len], i) => { const a = n === 1 ? 0 : i / (n - 1) * stagger, kk = clamp((k - a) / (1 - stagger || 1));
    if (kk <= 0) return; if (fill && kk >= 1) { g.fillStyle = fill; g.fill(p); }
    if (kk < 1) { g.setLineDash([len * kk, len + 1]); } else g.setLineDash([]); g.stroke(p); });
  g.restore(); }
// search by name / tags / categories: iconSearch('mosque') → ['landmark', 'church', …]
function iconSearch(q, max = 40) { q = q.toLowerCase(); const names = Object.keys(LUCIDE), T = window.LUCIDE_TAGS || {};
  const score = n => n === q ? 3 : n.includes(q) ? 2 : (T[n] || '').toLowerCase().split(' ').includes(q) ? 1.5 : (T[n] || '').toLowerCase().includes(q) ? 1 : 0;
  return names.map(n => [n, score(n)]).filter(a => a[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, max).map(a => a[0]); }

// ── 3 · PATTERNS ─────────────────────────────────────────────────────
// star polygon {n/m} vertices, radius r, rotation a0
const starPoly = (cx, cy, r, n, m, a0 = 0) => { const v = []; for (let i = 0; i < n; i++) { const j = (i * m) % n, a = a0 + j * 2 * Math.PI / n; v.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return v; };
function _strokeDraw(segs, k, stagger, seed) {   // segs: arrays of points (open polylines); k draw-on with seeded stagger
  const r = rng(seed); for (const pts of segs) { const st = r() * stagger, kk = clamp((k - st) / (1 - stagger || 1)); if (kk <= 0) continue;
    let len = 0; for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.setLineDash(kk < 1 ? [len * kk, len + 1] : []); g.stroke(); } g.setLineDash([]); }
// kind: star8 | star6 | star12 | rosette | girihNet | mashrabiya | dots | grid | halftone | lines | waves | iso | topo
// opts: {x,y,w,h (area), cell, color, lw, k (draw-on 0..1), stagger, rot, alpha, t (seconds, for animated kinds), seed, fill}
function pattern(kind, t, o = {}) {
  const { x = 0, y = 0, w = W, h = H, cell = 160, color = PAL.gold, lw = 2, k = 1, stagger = .6, rot = 0, alpha = 1, seed = 11, fill = null } = o;
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.globalAlpha *= alpha; g.strokeStyle = color; g.fillStyle = fill || color; g.lineWidth = lw; g.lineJoin = 'round'; g.lineCap = 'round';
  if (rot) { g.translate(x + w / 2, y + h / 2); g.rotate(rot); g.translate(-(x + w / 2), -(y + h / 2)); }
  const pad = cell * 2, segs = [], X0 = x - pad, Y0 = y - pad, X1 = x + w + pad, Y1 = y + h + pad;
  const close = v => v.concat([v[0]]);
  if (kind === 'star8' || kind === 'rosette') {           // 8-fold khatam lattice: {8/2} stars (two squares) at grid nodes joined by an octagon net
    for (let yy = Y0; yy < Y1; yy += cell) for (let xx = X0; xx < X1; xx += cell) {
      const R = cell * .42; segs.push(close(starPoly(xx, yy, R, 4, 1, 0))); segs.push(close(starPoly(xx, yy, R, 4, 1, Math.PI / 4)));
      // links: from each star tip to the neighbour's tip → crossing bands form the 4-point stars between nodes
      segs.push([[xx + R, yy], [xx + cell - R, yy]]); segs.push([[xx, yy + R], [xx, yy + cell - R]]);
      const d = R * Math.SQRT1_2; segs.push([[xx + d, yy + d], [xx + cell - d, yy + cell - d]]); segs.push([[xx + cell - d, yy + d], [xx + d, yy + cell - d]]);
      if (kind === 'rosette') { segs.push(close(starPoly(xx, yy, R * .45, 8, 3, Math.PI / 8))); const cp = []; for (let i = 0; i <= 32; i++) cp.push([xx + cell / 2 + cell * .12 * Math.cos(i / 32 * 6.283), yy + cell / 2 + cell * .12 * Math.sin(i / 32 * 6.283)]); segs.push(cp); }
    } }
  else if (kind === 'star6') {                             // hexagram + hexagon rosettes on a triangular lattice, linked tip-to-tip
    const dx = cell, dy = cell * Math.sqrt(3) / 2; let row = 0;
    for (let yy = Y0; yy < Y1; yy += dy, row++) for (let xx = X0 + (row % 2) * dx / 2; xx < X1; xx += dx) { const R = cell * .36;
      segs.push(close(starPoly(xx, yy, R, 3, 1, -Math.PI / 2))); segs.push(close(starPoly(xx, yy, R, 3, 1, Math.PI / 2))); segs.push(close(starPoly(xx, yy, R * .55, 6, 1, 0)));
      for (let i = 0; i < 3; i++) { const a = i * Math.PI / 3; segs.push([[xx + Math.cos(a) * R * .58, yy + Math.sin(a) * R * .58], [xx + Math.cos(a) * (cell - R * .58), yy + Math.sin(a) * (cell - R * .58)]]); } } }
  else if (kind === 'star12') {                            // 12-fold {12/5} stars on a hex lattice (Mamluk-like)
    const dx = cell * 1.5, dy = cell * Math.sqrt(3) / 2 * 1.5; let row = 0;
    for (let yy = Y0; yy < Y1; yy += dy, row++) for (let xx = X0 + (row % 2) * dx / 2; xx < X1; xx += dx) { segs.push(close(starPoly(xx, yy, cell * .75, 12, 5, 0))); segs.push(close(starPoly(xx, yy, cell * .3, 12, 1, 0))); } }
  else if (kind === 'girihNet') {                          // 10-fold decagonal net (girih flavour): {10/3} stars + connecting bowties
    const dx = cell * 1.62, dy = cell * 1.18; let row = 0;
    for (let yy = Y0; yy < Y1; yy += dy, row++) for (let xx = X0 + (row % 2) * dx / 2; xx < X1; xx += dx) { segs.push(close(starPoly(xx, yy, cell * .62, 10, 3, Math.PI / 10))); segs.push(close(starPoly(xx, yy, cell * .24, 10, 1, Math.PI / 10))); } }
  else if (kind === 'mashrabiya') {                        // turned-wood lattice: rotated squares + circles at nodes
    for (let yy = Y0; yy < Y1; yy += cell) for (let xx = X0; xx < X1; xx += cell) { const c = cell / 2; segs.push(close([[xx, yy - c], [xx + c, yy], [xx, yy + c], [xx - c, yy]])); const n = 18, r = cell * .12, cp = []; for (let i = 0; i <= n; i++) cp.push([xx + c + r * Math.cos(i / n * 6.283), yy + r * Math.sin(i / n * 6.283)]); segs.push(cp); } }
  else if (kind === 'lines' || kind === 'grid') { for (let xx = X0; xx < X1; xx += cell) segs.push([[xx, Y0], [xx, Y1]]); if (kind === 'grid') for (let yy = Y0; yy < Y1; yy += cell) segs.push([[X0, yy], [X1, yy]]); }
  else if (kind === 'waves') { const amp = o.amp || cell * .18, ph = (o.speed ?? .4) * t * 6.283; for (let yy = Y0; yy < Y1; yy += cell * .35) { const p = []; for (let xx = X0; xx <= X1; xx += 12) p.push([xx, yy + amp * Math.sin(xx / cell * 3.1 + ph + yy * .01)]); segs.push(p); } }
  else if (kind === 'iso') { const a = Math.tan(Math.PI / 6); for (let xx = X0 - (Y1 - Y0); xx < X1 + (Y1 - Y0); xx += cell) { segs.push([[xx, Y0], [xx + (Y1 - Y0) / a, Y1]]); segs.push([[xx, Y0], [xx - (Y1 - Y0) / a, Y1]]); segs.push([[xx, Y0], [xx, Y1]]); } }
  else if (kind === 'topo') {                              // marching-squares contour lines over fbm noise (animated with t)
    const s = cell / 6, levels = o.levels || 7, cols = Math.ceil(w / s) + 2, rows = Math.ceil(h / s) + 2, F = (i, j) => fbm(i * s / cell * .6 + (o.seed || 0), j * s / cell * .6 + t * (o.speed ?? .05), 3);
    const V = []; for (let j = 0; j < rows; j++) { V[j] = []; for (let i = 0; i < cols; i++) V[j][i] = F(i, j); }
    for (let l = 1; l < levels; l++) { const th = -0.6 + 1.2 * l / levels; for (let j = 0; j < rows - 1; j++) for (let i = 0; i < cols - 1; i++) {
      const a = V[j][i], b = V[j][i + 1], c = V[j + 1][i + 1], d = V[j + 1][i], e = [], ip = (p, q, u, vv) => { const r2 = (th - u) / (vv - u); return [lerp(p[0], q[0], r2), lerp(p[1], q[1], r2)]; };
      const P0 = [x + i * s, y + j * s], P1 = [P0[0] + s, P0[1]], P2 = [P0[0] + s, P0[1] + s], P3 = [P0[0], P0[1] + s];
      if ((a > th) !== (b > th)) e.push(ip(P0, P1, a, b)); if ((b > th) !== (c > th)) e.push(ip(P1, P2, b, c)); if ((c > th) !== (d > th)) e.push(ip(P2, P3, c, d)); if ((d > th) !== (a > th)) e.push(ip(P3, P0, d, a));
      if (e.length >= 2) segs.push([e[0], e[1]]); if (e.length === 4) segs.push([e[2], e[3]]); } }
    g.beginPath(); for (const sg of segs) { g.moveTo(...sg[0]); g.lineTo(...sg[1]); } g.globalAlpha *= clamp(k); g.stroke(); g.restore(); return; }
  if (kind === 'dots' || kind === 'halftone') {            // halftone: radius driven by a gradient (o.from→o.to) or noise
    const r0 = o.r || cell * .12; let row = 0, i = 0; const R = rng(seed);
    for (let yy = Y0; yy < Y1; yy += cell * (kind === 'halftone' ? .5 : 1), row++) for (let xx = X0 + (kind === 'halftone' && row % 2 ? cell * .25 : 0); xx < X1; xx += cell * (kind === 'halftone' ? .5 : 1), i++) {
      const st = R() * stagger, kk = clamp((k - st) / (1 - stagger || 1)); if (kk <= 0) continue;
      const tone = kind === 'halftone' ? (o.tone ? o.tone(xx, yy) : clamp((xx - x) / w * .8 + .5 * (1 + fbm(xx * .003, yy * .003 + t * .1, 2)) * .4)) : 1;
      const rr = r0 * (kind === 'halftone' ? tone * 2.1 : 1) * (typeof E !== 'undefined' ? E.backOut(kk) : kk); if (rr <= .2) continue; g.beginPath(); g.arc(xx, yy, rr, 0, 6.283); g.fill(); }
    g.restore(); return; }
  if (fill && k >= 1) { g.globalAlpha *= .25; for (const s of segs) { g.beginPath(); s.forEach(([px, py], i) => i ? g.lineTo(px, py) : g.moveTo(px, py)); g.fill(); } g.globalAlpha /= .25; }
  _strokeDraw(segs, k, stagger, seed);
  g.restore(); }
const PATTERN_KINDS = ['star8', 'rosette', 'star6', 'star12', 'girihNet', 'mashrabiya', 'dots', 'halftone', 'grid', 'lines', 'waves', 'iso', 'topo'];
