// ════════════════════════════════════════════════════════════════════
//  Thuluth film · v3 core — "Sepia Manuscript Cinema"
//  Pure function of time: window.seek(t) paints frame t. Seeded RNG only, no timers.
//  Design system → docs/STYLE_v3.md
// ════════════════════════════════════════════════════════════════════
const W = 1920, H = 1080;
const cv = document.getElementById('c');
let g = cv.getContext('2d');
const MAIN = g;

// ── math / motion ────────────────────────────────────────────────────
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const ease = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };   // in-out cubic
const easeOut = (a, b, x) => { const k = clamp((x - a) / (b - a)); return 1 - Math.pow(1 - k, 3); };
function spring(t, k = 170, d = 26) {
  if (t <= 0) return 0;
  const w0 = Math.sqrt(k), z = d / (2 * w0);
  if (z < 1) { const wd = w0 * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t)); }
  return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
}
// the ONLY three motion presets of the film
const SPR = { card: [150, 19], snap: [320, 28], soft: [60, 15] };
const sp = (t, t0, kind = 'card') => spring(t - t0, ...SPR[kind]);
function track(t, keys, k = 60, d = 15) { let v = keys[0][1]; for (let i = 1; i < keys.length; i++) v += (keys[i][1] - keys[i - 1][1]) * spring(t - keys[i][0], k, d); return v; }
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = (a, b = 0) => rng((a * 73856093) ^ (b * 19349663))();
const shake = (t, t0, amp, f = 60) => t < t0 ? 0 : amp * Math.exp(-(t - t0) * 9) * Math.sin((t - t0) * f);
const breathe = (id, t, amp = 1) => [Math.sin(t * .9 + id) * 1.6 * amp, Math.cos(t * .7 + id * 1.7) * 1.2 * amp, Math.sin(t * .5 + id * .3) * .0025 * amp];

// ── palette & type ───────────────────────────────────────────────────
const PAL = { bg: '#0c0906', ink: '#24180e', parch: '#e8d7b2', cream: '#f1e4c4', gold: '#c99a45', goldL: '#e9c77c', goldD: '#86520f', red: '#a8321f', shadow: 'rgba(0,0,0,.6)' };
const DISPLAY = 'Amiri', UI = 'Kufi';
const TYPE = { h1: 96, h2: 72, h3: 52, cap: 30, tag: 26 }, TS = 1.3;   // global type scale

// ── assets ───────────────────────────────────────────────────────────
const A = {};
const loadImg = (k, src) => new Promise(r => { const i = new Image(); i.onload = () => { A[k] = i; r(); }; i.onerror = () => { console.log('MISSING ' + src); r(); }; i.src = src; });
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = Math.max(1, Math.ceil(w)); c.height = Math.max(1, Math.ceil(h)); return c; };
function tornPoly(w, h, seed, rough = 6, step = 11) {
  const r = rng(seed), pts = [];
  const edge = (x0, y0, x1, y1, nx, ny) => { const len = Math.hypot(x1 - x0, y1 - y0), n = Math.max(2, Math.round(len / step)), ph = r() * 6.28, fr = 1 + r() * 2;
    for (let i = 0; i < n; i++) { const k = i / n, o = (r() - .5) * rough * 1.5 + Math.sin(k * 6.28 * fr + ph) * rough; pts.push([x0 + (x1 - x0) * k + nx * o, y0 + (y1 - y0) * k + ny * o]); } };
  edge(0, 0, w, 0, 0, -1); edge(w, 0, w, h, 1, 0); edge(w, h, 0, h, 0, 1); edge(0, h, 0, 0, -1, 0); return pts;
}
const pathPoly = (c, pts, ox = 0, oy = 0) => { c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x + ox, y + oy) : c.moveTo(x + ox, y + oy)); c.closePath(); };

// ── paper: aged parchment (or dark paper) clipped to a torn outline, burnt edge, baked shadow
function paper({ w, h, seed = 1, rough = 6, dark = false, content = null, burn = .55, res = 1 }) {
  const pad = 40, c = mk((w + pad * 2) * res, (h + pad * 2) * res), x = c.getContext('2d'); x.scale(res, res);
  const pts = tornPoly(w, h, seed, rough), r = rng(seed + 9);
  x.save(); pathPoly(x, pts, pad, pad); x.clip();
  const T = dark ? A.bg_dark : A.paper_cream, sc = Math.max((w + 80) / T.width, (h + 80) / T.height) * (1 + r() * .5);
  x.drawImage(T, pad - r() * (T.width * sc - w), pad - r() * (T.height * sc - h), T.width * sc, T.height * sc);
  x.fillStyle = dark ? 'rgba(20,14,9,.55)' : 'rgba(214,186,138,.38)'; x.globalCompositeOperation = dark ? 'source-over' : 'multiply'; x.fillRect(0, 0, w + pad * 2, h + pad * 2);
  x.globalCompositeOperation = 'source-over';
  if (!dark) { x.fillStyle = 'rgba(238,224,190,.42)'; x.fillRect(0, 0, w + pad * 2, h + pad * 2); }
  if (content) { x.save(); x.translate(pad, pad); content(x, w, h); x.restore(); }
  // burnt / aged inner edge
  if (burn > 0) { x.save(); pathPoly(x, pts, pad, pad); x.strokeStyle = dark ? 'rgba(0,0,0,.9)' : `rgba(92,58,24,${burn})`; x.lineWidth = 26; x.filter = 'blur(12px)'; x.stroke(); x.restore(); }
  x.restore();
  x.save(); pathPoly(x, pts, pad, pad); x.strokeStyle = dark ? 'rgba(210,190,150,.35)' : 'rgba(250,240,215,.75)'; x.lineWidth = 1.6; x.stroke(); x.restore();
  const s = mk(c.width, c.height), sx = s.getContext('2d'); sx.scale(res, res); sx.filter = `blur(${10 * res}px)`; sx.fillStyle = '#000'; pathPoly(sx, pts, pad, pad); sx.fill();
  return { c, s, w, h, pad, res };
}
function drawP(p, x, y, { rot = 0, sc = 1, alpha = 1, lift = 0, sx = 1 } = {}) {
  if (!p || alpha <= .002 || sc <= .001) return;
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(sc * sx / p.res, sc / p.res);
  const ox = -p.c.width / 2, oy = -p.c.height / 2;
  g.globalAlpha = alpha * (.7 - lift * .15); g.drawImage(p.s, ox + (6 + lift * 26) * p.res, oy + (10 + lift * 34) * p.res);
  g.globalAlpha = alpha; g.drawImage(p.c, ox, oy); g.restore();
}
// a photographic / scanned image printed on a torn paper piece
function photo(img, w, { crop = null, seed = 1, rough = 6, burn = .5, res = 1, mul = .14 } = {}) {
  const [sx, sy, sw, sh] = crop || [0, 0, img.width, img.height], h = Math.round(w * sh / sw);
  const p = paper({ w, h, seed, rough, burn, res, content: (x, w, h) => { x.drawImage(img, sx, sy, sw, sh, 0, 0, w, h);
    if (mul) { x.globalCompositeOperation = 'multiply'; x.globalAlpha = mul; x.drawImage(A.paper_cream, 0, 0, w, h); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; } } });
  p.img = img; p.crop = [sx, sy, sw, sh]; return p;
}
// cut-out object with its soft shadow
function cutout(img, blur = 14) { const c = mk(img.width + blur * 6, img.height + blur * 6), x = c.getContext('2d');
  x.filter = `blur(${blur}px) brightness(0)`; x.drawImage(img, blur * 3, blur * 3); return { img, sh: c, blur }; }
function drawCut(o, x, y, w, { rot = 0, alpha = 1, ax = .5, ay = .5, lift = 0, shA = .55 } = {}) {
  if (!o || alpha <= 0) return; const k = w / o.img.width, h = o.img.height * k, pad = o.blur * 3 * k;
  g.save(); g.translate(x, y); g.rotate(rot);
  g.globalAlpha = alpha * shA; g.drawImage(o.sh, -w * ax - pad + 10 + lift * 30, -h * ay - pad + 16 + lift * 40, o.sh.width * k, o.sh.height * k);
  g.globalAlpha = alpha; g.drawImage(o.img, -w * ax, -h * ay, w, h); g.restore();
}

// ── typography: text drawn live so it can "write on" (RTL wipe) ───────
function textImg(lines, { align = 'center', lh = 1.35, gap = 0 } = {}) {
  // lines: [{t, size, font, weight, color}] → canvas
  const m = mk(10, 10).getContext('2d'); let wmax = 0, hs = [];
  for (const L of lines) { m.font = `${L.weight || 700} ${L.size * TS}px ${L.font || DISPLAY}`; m.direction = 'rtl'; wmax = Math.max(wmax, m.measureText(L.t).width); hs.push(L.size * TS * (L.lh || lh)); }
  const pad = 20, Wd = wmax + pad * 2, Hd = hs.reduce((a, b) => a + b, 0) + pad * 2 + gap * (lines.length - 1);
  const c = mk(Wd, Hd), x = c.getContext('2d'); let y = pad;
  lines.forEach((L, i) => { x.font = `${L.weight || 700} ${L.size * TS}px ${L.font || DISPLAY}`; x.direction = 'rtl'; x.textBaseline = 'middle'; x.fillStyle = L.color || PAL.ink;
    x.textAlign = align === 'center' ? 'center' : align === 'right' ? 'right' : 'left';
    const xx = align === 'center' ? Wd / 2 : align === 'right' ? Wd - pad : pad;
    if (L.divider) { x.strokeStyle = L.color || PAL.gold; x.lineWidth = 2; const yy = y + hs[i] / 2, half = L.divider / 2;
      x.beginPath(); x.moveTo(Wd / 2 - half, yy); x.lineTo(Wd / 2 - 18, yy); x.moveTo(Wd / 2 + 18, yy); x.lineTo(Wd / 2 + half, yy); x.stroke(); nuqta(x, Wd / 2, yy, 13, L.color || PAL.gold); }
    else x.fillText(L.t, xx, y + hs[i] / 2 + (L.dy || 0));
    y += hs[i] + gap; });
  return c;
}
// write-on: reveal a text canvas right→left with a soft edge
function writeOn(img, x, y, k, { sc = 1, alpha = 1, ax = .5, ay = .5 } = {}) {
  if (k <= 0 || alpha <= 0) return; const w = img.width * sc, h = img.height * sc, x0 = x - w * ax, y0 = y - h * ay;
  g.save(); g.globalAlpha = alpha;
  if (k < 1) { const edge = 60 * sc, cut = x0 + w - (w + edge) * k;
    g.beginPath(); g.rect(cut + edge, y0 - 5, w + 10, h + 10); g.clip(); }
  g.drawImage(img, x0, y0, w, h); g.restore();
}
// a text card = torn parchment piece + live text
function card(lines, { seed = 1, dark = false, padX = 70, padY = 40, minW = 0, rough = 6, opts = {} } = {}) {
  const ti = textImg(lines, opts), w = Math.max(minW, ti.width + padX * 2 - 40), h = ti.height + padY * 2 - 40;
  return { p: paper({ w, h, seed, rough, dark, burn: dark ? .9 : .5 }), ti, w, h };
}
// card lands like a sheet dropped on the table, then its text writes on
function drawCard(cd, t, t0, x, y, { rot = 0, t1 = null, sc = 1, wdur = .55, from = 'drop' } = {}) {
  const k = sp(t, t0, 'card'); if (k <= .001) return;
  const ko = t1 ? ease(t1, t1 + .45, t) : 0; if (ko >= 1) return;
  const b = breathe(seed2(cd), t, .6);
  let dx = 0, dy = 0, r = rot + (1 - k) * .1, s = sc * lerp(1.06, 1, k), lift = (1 - k) * .9;
  if (from === 'drop') dy = -(1 - k) * 120; else if (from === 'right') dx = (1 - k) * 700; else if (from === 'left') dx = -(1 - k) * 700;
  dx += ko * -40; dy += ko * 60; const al = clamp(k * 3) * (1 - ko);
  drawP(cd.p, x + dx + b[0], y + dy + b[1], { rot: r + b[2], sc: s, alpha: al, lift });
  g.save(); g.translate(x + dx + b[0], y + dy + b[1]); g.rotate(r + b[2]); writeOn(cd.ti, 0, 0, easeOut(t0 + .12, t0 + .12 + wdur, t), { sc: s, alpha: al }); g.restore();
}
const seed2 = (o) => (o.w * 7 + o.h * 13) % 97;
function nuqta(c, x, y, s, color = PAL.ink, rot = 0) {
  c.save(); c.translate(x, y); c.rotate(Math.PI / 4 + rot); c.fillStyle = color; const a = s / 2, k = a * .12;
  c.beginPath(); c.moveTo(-a, -a + k); c.quadraticCurveTo(-a, -a, -a + k, -a); c.lineTo(a - k, -a); c.quadraticCurveTo(a, -a, a, -a + k);
  c.lineTo(a, a - k); c.quadraticCurveTo(a, a, a - k, a); c.lineTo(-a + k, a); c.quadraticCurveTo(-a, a, -a, a - k); c.closePath(); c.fill(); c.restore();
}
// gold hairline reveal along a polyline
function line(pts, p, { color = PAL.gold, width = 2.2, dash = null, closed = false, alpha = 1 } = {}) {
  if (p <= 0) return; const P = closed ? [...pts, pts[0]] : pts; let L = 0; const seg = [];
  for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); seg.push(l); L += l; }
  let rem = L * clamp(p); g.save(); g.globalAlpha = alpha; g.strokeStyle = color; g.lineWidth = width; g.lineCap = 'round'; g.lineJoin = 'round'; if (dash) g.setLineDash(dash);
  g.beginPath(); g.moveTo(P[0][0], P[0][1]);
  for (let i = 1; i < P.length && rem > 0; i++) { const l = seg[i - 1], k = Math.min(1, rem / l); g.lineTo(lerp(P[i - 1][0], P[i][0], k), lerp(P[i - 1][1], P[i][1], k)); rem -= l; }
  g.stroke(); g.restore();
}
function arc(cx, cy, r, p, { color = PAL.gold, width = 2.2, a0 = -Math.PI / 2, dir = -1, dash = null, alpha = 1 } = {}) {
  if (p <= 0) return; g.save(); g.globalAlpha = alpha; g.strokeStyle = color; g.lineWidth = width; if (dash) g.setLineDash(dash);
  g.beginPath(); g.arc(cx, cy, r, a0, a0 + dir * p * Math.PI * 2, dir < 0); g.stroke(); g.restore();
}

// ── plates: full-frame cinematic backgrounds with eased camera moves ──
function plate(img, t, a, b, { s0 = 1.0, s1 = 1.06, fx0 = .5, fy0 = .5, fx1 = .5, fy1 = .5, dim = 0 } = {}) {
  const k = ease(a, b, t), s = lerp(s0, s1, k), fx = lerp(fx0, fx1, k), fy = lerp(fy0, fy1, k);
  const base = Math.max(W / img.width, H / img.height), w = img.width * base * s, h = img.height * base * s;
  const x = clamp(W / 2 - fx * w, W - w, 0), y = clamp(H / 2 - fy * h, H - h, 0);
  g.drawImage(img, x, y, w, h);
  if (dim) { g.fillStyle = `rgba(8,6,4,${dim})`; g.fillRect(0, 0, W, H); }
}
// shot camera: scale s around focus (fx,fy) in a 1920×1080 "stage"
function camOn(s, fx, fy, rot = 0) { g.save(); g.translate(W / 2, H / 2); g.scale(s, s); g.rotate(rot); g.translate(-fx, -fy); }
const camOff = () => g.restore();

// ── light: soft volumetric rays drifting slowly (screen blend) ───────
function rays(t, { x = 260, y = -200, ang = .62, n = 5, int = .16, spread = .5 } = {}) {
  g.save(); g.globalCompositeOperation = 'screen';
  for (let i = 0; i < n; i++) { const a = ang + (i - n / 2) * spread / n + Math.sin(t * .25 + i * 1.7) * .02, wdt = 60 + 120 * hash(i, 77), L = 2600;
    g.save(); g.translate(x, y); g.rotate(a);
    const gr = g.createLinearGradient(0, -wdt, 0, wdt); const al = int * (.55 + .45 * Math.sin(t * .6 + i * 2.1));
    gr.addColorStop(0, 'rgba(255,214,150,0)'); gr.addColorStop(.5, `rgba(255,214,150,${al})`); gr.addColorStop(1, 'rgba(255,214,150,0)');
    g.fillStyle = gr; g.fillRect(0, -wdt, L, wdt * 2); g.restore(); }
  g.restore();
}
let grain = [], vign, buf, bufCtx;
function grade(t) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.save(); g.globalCompositeOperation = 'soft-light'; g.fillStyle = 'rgba(214,150,70,.22)'; g.fillRect(0, 0, W, H); g.restore();
  g.save(); g.globalCompositeOperation = 'overlay'; g.globalAlpha = .09; g.drawImage(grain[Math.floor(t * 12) % 4], 0, 0, W, H); g.restore();
  g.drawImage(vign, 0, 0);
}

// ── transitions: the outgoing shot is TORN away right→left (RTL) ──────
const TEAR = .62;
function tearPoly(xl, seed) { const r = rng(seed), pts = [[-200, -50]]; let x = xl;
  for (let y = -50; y <= H + 50; y += 22) { x = xl + (r() - .5) * 46 + Math.sin(y * .013 + seed) * 30; pts.push([x, y]); } pts.push([-200, H + 50]); return pts; }
function drawTear(t, t0, drawOut, seed) {
  const k = ease(t0, t0 + TEAR, t); if (k >= 1) return; const xl = lerp(W + 140, -140, k);
  const prev = g; g = bufCtx; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H); drawOut(); g.setTransform(1, 0, 0, 1, 0, 0); g = prev;
  const pts = tearPoly(xl, seed);
  // shadow cast by the torn sheet on the incoming shot
  g.save(); g.filter = 'blur(18px)'; g.fillStyle = 'rgba(0,0,0,.7)'; pathPoly(g, pts.map(([x, y]) => [x + 22, y])); g.fill(); g.restore();
  g.save(); pathPoly(g, pts); g.clip(); g.drawImage(buf, 0, 0); g.restore();
  // fibrous white paper edge
  g.save(); g.strokeStyle = 'rgba(240,228,200,.85)'; g.lineWidth = 7; g.beginPath(); pts.slice(1, -1).forEach(([x, y], i) => i ? g.lineTo(x + 3, y) : g.moveTo(x + 3, y)); g.stroke();
  g.strokeStyle = 'rgba(160,130,90,.6)'; g.lineWidth = 2; g.stroke(); g.restore();
}

// ── shots ─────────────────────────────────────────────────────────────
const SHOTS = [], INITS = [];
// shot: {a, b, draw(t), tin: 'tear'|'cut'}
function render(t) {
  g = MAIN; g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = PAL.bg; g.fillRect(0, 0, W, H);
  let i = SHOTS.findIndex(s => t >= s.a && t < s.b); if (i < 0) i = t < SHOTS[0].a ? 0 : SHOTS.length - 1;
  const s = SHOTS[i]; s.draw(t); g.setTransform(1, 0, 0, 1, 0, 0);
  if (i > 0 && (s.tin || 'tear') === 'tear' && t < s.a + TEAR) drawTear(t, s.a, () => SHOTS[i - 1].draw(t), 31 + i * 7);
  grade(t);
}
async function init() {
  for (const [k, f] of [['paper_cream', 'assets/paper_cream.jpg'], ['bg_dark', 'assets/bg_dark.jpg']]) await loadImg(k, f);
  for (const f of ['700 60px Amiri', '400 60px Amiri', '800 60px Kufi', '600 60px Kufi', '60px Tholoth']) { try { await document.fonts.load(f, 'خط الثلث'); } catch (e) {} }
  await document.fonts.ready;
  for (let k = 0; k < 4; k++) { const c = mk(640, 360), x = c.getContext('2d'), d = x.createImageData(640, 360), r = rng(900 + k);
    for (let i = 0; i < d.data.length; i += 4) { const v = r() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); grain.push(c); }
  vign = mk(W, H); { const x = vign.getContext('2d'), gr = x.createRadialGradient(W / 2, H * .48, H * .32, W / 2, H / 2, H * 1.0);
    gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,.66)'); x.fillStyle = gr; x.fillRect(0, 0, W, H); }
  buf = mk(W, H); bufCtx = buf.getContext('2d');
  for (const f of INITS) await f();
  SHOTS.sort((a, b) => a.a - b.a);
  window.ready = true;
}
window.seek = (t) => { if (window.ready) render(t); return true; };
