// ═══ Lamset Shifa v2 · «الخط الواحد» — ONE-LINE engine ══════════════════════════════════════════════
// One continuous gold line draws the whole film in a single take. Everything lives in ONE world:
//   LINE  — the path (points with a time-parameter s), pen keys (t → s), stroke/trace/highlight
//   LCAM   — a keyed camera (Hermite, log-zoom, roll) that films the world; w2s() maps world → screen
//   BLOOM — fills that "ink-spread" from a point once a figure is closed
//   wtext — kinetic words anchored in the world (they leave with the camera, no fades needed)
// Pure function of t: the path is built once in INITS; every frame only reads it.
const LP = { gold: '#e9c46b', goldD: '#b8913c', cream: '#f7f2e6', mint: '#8fd8c3', deep: '#04302b', bg: '#063c36', teal: '#0d6a5c' };

const LINE = (() => {
  const P = []; let S = 0; const M = {}; const KEYS = [];
  let svg = null;
  // sample an SVG path string → array of sub-polylines (split at pen jumps)
  function sample(d, step = 2.5) {
    if (!svg) { svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('style', 'position:absolute;left:-9999px;top:0;width:10px;height:10px'); document.body.appendChild(svg); }
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); svg.appendChild(p);
    const L = p.getTotalLength(), n = Math.max(2, Math.ceil(L / step)), out = []; let cur = [], prev = null;
    for (let i = 0; i <= n; i++) { const q = p.getPointAtLength(L * i / n), pt = [q.x, q.y];
      if (prev && Math.hypot(pt[0] - prev[0], pt[1] - prev[1]) > step * 3) { if (cur.length > 1) out.push(cur); cur = []; }
      cur.push(pt); prev = pt; }
    if (cur.length > 1) out.push(cur); p.remove(); return out;
  }
  // transform local figure coords → world  (o: {x,y,sc,rot,cx,cy,fx})
  const tf = (pts, o) => { const c = Math.cos(o.rot || 0), s = Math.sin(o.rot || 0), sc = o.sc || 1, fx = o.fx || 1;
    return pts.map(([x, y]) => { const u = (x - (o.cx || 0)) * sc * fx, v = (y - (o.cy || 0)) * sc; return [o.x + u * c - v * s, o.y + u * s + v * c]; }); };
  function pt(x, y, v, wt = 1) { if (P.length) { const q = P[P.length - 1]; S += Math.hypot(x - q.x, y - q.y) * (v ? 1 : wt); } P.push({ x, y, s: S, v }); }
  const last = () => P[P.length - 1];
  const dirEnd = () => { const n = P.length; if (n < 2) return [0, -1]; let j = n - 2; while (j > 0 && Math.hypot(P[n - 1].x - P[j].x, P[n - 1].y - P[j].y) < 12) j--;
    const dx = P[n - 1].x - P[j].x, dy = P[n - 1].y - P[j].y, l = Math.hypot(dx, dy) || 1; return [dx / l, dy / l]; };
  function bez(p0, c1, c2, p1, n) { const out = []; for (let i = 1; i <= n; i++) { const u = i / n, a = 1 - u;
    out.push([a * a * a * p0[0] + 3 * a * a * u * c1[0] + 3 * a * u * u * c2[0] + u * u * u * p1[0], a * a * a * p0[1] + 3 * a * a * u * c1[1] + 3 * a * u * u * c2[1] + u * u * u * p1[1]]); } return out; }
  // visible flowing connector from the pen to p (tangent-continuous); dIn = direction we want to arrive with
  function flow(p, { dIn = null, k1 = .45, k2 = .45, c1 = null, c2 = null } = {}) {
    const a = last(), d = Math.hypot(p[0] - a.x, p[1] - a.y), dOut = dirEnd();
    const C1 = c1 || [a.x + dOut[0] * d * k1, a.y + dOut[1] * d * k1];
    const din = dIn || [(p[0] - C1[0]), (p[1] - C1[1])]; const l = Math.hypot(din[0], din[1]) || 1;
    const C2 = c2 || [p[0] - din[0] / l * d * k2, p[1] - din[1] / l * d * k2];
    bez([a.x, a.y], C1, C2, p, Math.max(8, Math.ceil(d / 6))).forEach(([x, y]) => pt(x, y, true));
  }
  function start(x, y) { P.length = 0; S = 0; pt(x, y, true); }
  // add sub-polylines; first joined by `join` ('flow' | 'line' | 'lift'), the rest lifted (pen hops)
  let F0 = 0;
  function add(subs, { join = 'flow', liftWt = .08, dIn = null, k1, k2, c1, c2 } = {}) {
    subs.forEach((sp, j) => {
      const p0 = sp[0];
      if (!P.length) pt(p0[0], p0[1], true);
      else if (j === 0 && join === 'flow') { const d2 = sp[Math.min(3, sp.length - 1)]; flow(p0, { dIn: dIn || [d2[0] - p0[0], d2[1] - p0[1]], k1, k2, c1, c2 }); }
      else if (j === 0 && join === 'line') pt(p0[0], p0[1], true);
      else pt(p0[0], p0[1], false, liftWt);
      if (j === 0) F0 = S;
      for (let i = 1; i < sp.length; i++) pt(sp[i][0], sp[i][1], true);
    });
    return subs;
  }
  function fig(d, o, opt) { const subs = sample(d, o.step || 2.5).map((s) => tf(s, o)); return add(subs, opt); }
  const mark = (n) => (M[n] = S);
  const mark0 = (n) => (M[n] = F0);            // s where the last added figure itself starts (after its connector)
  const sOf = (m) => typeof m === 'number' ? m : M[m];
  // pen keys: at time t the pen is at s = mark (eased between keys)
  const key = (t, m, e = 'io') => KEYS.push([t, m, e]);
  const EZ = { io: (k) => .5 - .5 * Math.cos(Math.PI * k), lin: (k) => k, o: (k) => 1 - (1 - k) ** 3, i: (k) => k ** 2.2, oo: (k) => 1 - (1 - k) ** 2 };
  function head(t) {
    const K = KEYS; if (!K.length) return 0; if (t <= K[0][0]) return sOf(K[0][1]);
    for (let i = 0; i < K.length - 1; i++) if (t < K[i + 1][0]) { const [t0, m0] = K[i], [t1, m1, e] = K[i + 1];
      return lerp(sOf(m0), sOf(m1), (EZ[e] || EZ.io)(clamp((t - t0) / (t1 - t0)))); }
    return sOf(K[K.length - 1][1]);
  }
  function idx(s) { let lo = 0, hi = P.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (P[m].s <= s) lo = m; else hi = m - 1; } return lo; }
  function at(s) { const i = idx(s); if (i >= P.length - 1) { const q = P[P.length - 1]; return { x: q.x, y: q.y, v: true, i }; }
    const a = P[i], b = P[i + 1], k = b.s > a.s ? (s - a.s) / (b.s - a.s) : 0; return { x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k), v: b.v, i }; }
  function trace(s0, s1) {
    s0 = Math.max(0, s0); s1 = Math.min(S, s1); if (s1 <= s0) return;
    const i0 = idx(s0), i1 = idx(s1), p0 = at(s0); g.moveTo(p0.x, p0.y);
    for (let i = i0 + 1; i <= i1; i++) { const q = P[i]; q.v ? g.lineTo(q.x, q.y) : g.moveTo(q.x, q.y); }
    if (i1 < P.length - 1) { const p1 = at(s1); P[i1 + 1].v ? g.lineTo(p1.x, p1.y) : g.moveTo(p1.x, p1.y); }
  }
  // stroke a range in world space; width given in SCREEN px
  function stroke(s0, s1, { color = LP.gold, px = 7, alpha = 1, z = 1, under = 0, shadow = 0, core = 0 } = {}) {
    if (s1 <= s0 || alpha <= .003) return;
    g.save(); g.lineCap = 'round'; g.lineJoin = 'round';
    if (shadow) { g.shadowColor = `rgba(0,14,11,${shadow})`; g.shadowBlur = 12; g.shadowOffsetY = 7; }
    if (under) { g.globalAlpha = alpha * under; g.strokeStyle = color; g.lineWidth = px * 3.2 / z; g.beginPath(); trace(s0, s1); g.stroke(); }
    g.globalAlpha = alpha; g.strokeStyle = color; g.lineWidth = px / z; g.beginPath(); trace(s0, s1); g.stroke();
    if (core) { g.shadowColor = 'transparent'; g.globalAlpha = alpha * core; g.strokeStyle = '#fff4d2'; g.lineWidth = px * .32 / z; g.beginPath(); trace(s0, s1); g.stroke(); }
    g.restore();
  }
  const bounds = (s0 = 0, s1 = S) => { let a = [1e9, 1e9, -1e9, -1e9]; for (const q of P) if (q.s >= s0 && q.s <= s1) { a[0] = Math.min(a[0], q.x); a[1] = Math.min(a[1], q.y); a[2] = Math.max(a[2], q.x); a[3] = Math.max(a[3], q.y); } return a; };
  return { P, M, KEYS, mark0, sample, tf, pt, flow, start, add, fig, mark, sOf, key, head, at, trace, stroke, bounds, last, get S() { return S; } };
})();

// ── camera: keys {t,x,y,z,r,hold}; Hermite per channel (zoom in log space) ─────────────────────────
const LCAM = (() => {
  const K = [];
  const key = (t, x, y, z = 1, r = 0, hold = false) => { K.push({ t, x, y, z: Math.log(z), r, hold }); K.sort((a, b) => a.t - b.t); };
  function ch(t, c) {
    if (t <= K[0].t) return K[0][c]; const n = K.length; if (t >= K[n - 1].t) return K[n - 1][c];
    let i = 0; while (t >= K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], h = b.t - a.t, u = (t - a.t) / h;
    const m = (j) => { const q = K[j]; if (q.hold || j === 0 || j === n - 1) return 0; return (K[j + 1][c] - K[j - 1][c]) / (K[j + 1].t - K[j - 1].t); };
    const h00 = 2 * u ** 3 - 3 * u * u + 1, h10 = u ** 3 - 2 * u * u + u, h01 = -2 * u ** 3 + 3 * u * u, h11 = u ** 3 - u * u;
    return h00 * a[c] + h10 * h * m(i) + h01 * b[c] + h11 * h * m(i + 1);
  }
  let now = { x: 0, y: 0, z: 1, r: 0 };
  function at(t) { return { x: ch(t, 'x'), y: ch(t, 'y'), z: Math.exp(ch(t, 'z')), r: ch(t, 'r') }; }
  function set(t, extra = null) { now = at(t); if (extra) { now.x += extra.x || 0; now.y += extra.y || 0; now.r += extra.r || 0; } return now; }
  function apply(c = now) { g.translate(W / 2, H / 2); g.rotate(c.r); g.scale(c.z, c.z); g.translate(-c.x, -c.y); }
  function w2s(x, y, c = now) { const dx = (x - c.x) * c.z, dy = (y - c.y) * c.z, cs = Math.cos(c.r), sn = Math.sin(c.r); return [W / 2 + dx * cs - dy * sn, H / 2 + dx * sn + dy * cs]; }
  // world point that appears at screen (sx,sy) for a given camera
  function s2w(sx, sy, c) { const dx = sx - W / 2, dy = sy - H / 2, cs = Math.cos(-c.r), sn = Math.sin(-c.r); return [c.x + (dx * cs - dy * sn) / c.z, c.y + (dx * sn + dy * cs) / c.z]; }
  return { K, key, at, set, apply, w2s, s2w, get now() { return now; } };
})();

// ── blooms: fills that spread from a point (drawn in world space, under the line) ─────────────────────
const BLOOM = (() => {
  const L = [];
  const add = (o) => L.push(Object.assign({ dur: .5, alpha: 1, color: LP.gold, t1: null, outDur: .4 }, o));
  function draw(t) {
    for (const b of L) { const k = KT.eOut((t - b.t0) / b.dur); if (k <= 0) continue;
      const ko = b.t1 != null ? clamp((t - b.t1) / b.outDur) : 0; if (ko >= 1) continue;
      g.save(); g.beginPath(); g.arc(b.cx, b.cy, b.r * k, 0, 7); g.clip(); g.globalAlpha = b.alpha * (1 - ko);
      g.fillStyle = b.color; g.beginPath(); b.shape(g); g.fill(b.rule || 'nonzero'); g.restore(); }
  }
  return { L, add, draw };
})();
const polyShape = (subs) => (c) => subs.forEach((sp) => { sp.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.closePath(); });

// ── words anchored in the world ────────────────────────────────────────────────────────────────────
function wtext(Wd, t, s) {
  const c = LCAM.now, [x, y] = LCAM.w2s(s.wx, s.wy);
  return KT.show(Wd, t, Object.assign({}, s, { x, y, sc: (s.sc ?? 1) * c.z, rot: (s.rot || 0) + c.r }));
}
// RTL "pen reveal" for a word in world space: wipe edge follows a given progress fn
function wpen(Wd, t, s, k) {
  if (k <= 0) return; const c = LCAM.now, [x, y] = LCAM.w2s(s.wx, s.wy), sc = (s.sc ?? 1) * c.z;
  g.save(); g.translate(x, y); g.rotate(c.r); g.scale(sc, sc);
  const w = Wd.img.width, h = Wd.img.height;
  if (k < 1) { const right = Wd.w / 2 + 30, edge = right - (Wd.w + 60) * k; g.beginPath(); g.rect(edge, -h, right - edge + w, h * 2); g.clip(); }
  g.globalAlpha = s.alpha ?? 1; g.drawImage(Wd.img, -w / 2, -h / 2); g.restore();
}
// shared shapes (local coords, then LINE.tf)
const SHAPES = {
  // left footprint in a 100×160 box (sole, then toes big→little)
  foot: 'M52 158 C34 158 26 146 27 126 C28 106 21 92 21 70 C21 48 37 36 56 37 C75 38 82 53 80 72 C78 92 71 104 73 124 C75 146 68 158 52 158 Z' +
    ['69 15 12', '51 11 8.5', '38 16 7', '28 24 6', '20 34 5'].map((q) => { const [x, y, r] = q.split(' ').map(Number); return `M${x + r} ${y} A${r} ${r} 0 1 0 ${x - r} ${y} A${r} ${r} 0 1 0 ${x + r} ${y}`; }).join(''),
  circle: (cx, cy, r, a0 = 0, turns = 1, n = 160, dir = -1) => { const o = []; for (let i = 0; i <= n; i++) { const a = a0 + dir * turns * Math.PI * 2 * i / n; o.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } return o; },
  star: (cx, cy, R, r, rot = -Math.PI / 2) => { const o = []; for (let i = 0; i <= 10; i++) { const a = rot + i * Math.PI / 5, q = i % 2 ? r : R; o.push([cx + Math.cos(a) * q, cy + Math.sin(a) * q]); } return o; },
};
const densify = (pts, step = 4) => { const o = [pts[0]]; for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / step)); for (let j = 1; j <= n; j++) o.push([lerp(x0, x1, j / n), lerp(y0, y1, j / n)]); } return o; };

// ── v2.1 additions ──
// Lucide icon (24×24) drawn by the same pen: ring-part flows in from the connector, the rest are pen hops
LINE.icon = (name, x, y, size, opt = {}) => {
  const parts = (window.LUCIDE || {})[name]; if (!parts) return [];
  const subs = [];
  for (const [d] of parts) LINE.sample(d, opt.step || 2).forEach((sp) => subs.push(LINE.tf(sp, { x, y, cx: 12, cy: 12, sc: size / 24 })));
  return LINE.add(subs.filter((s) => s.length > 1), opt);
};
// LTR "pen reveal" (numbers): wipe edge travels left → right
function wpenL(Wd, t, s, k) {
  if (k <= 0) return; const c = LCAM.now, [x, y] = LCAM.w2s(s.wx, s.wy), sc = (s.sc ?? 1) * c.z;
  const w = Wd.img.width, h = Wd.img.height;
  g.save(); g.translate(x, y); g.rotate(c.r); g.scale(sc, sc);
  if (k < 1) { g.beginPath(); g.rect(-w / 2, -h / 2, w * k, h); g.clip(); }
  g.globalAlpha = s.alpha ?? 1; g.drawImage(Wd.img, -w / 2, -h / 2); g.restore();
}
// LTR word (digits reorder in an rtl canvas)
function ltrWord(text, o = {}) {
  const size = (o.size || 120) * TS, font = o.font || UI, weight = o.weight || 700, color = o.color || LP.cream;
  const m = mk(8, 8).getContext('2d'); m.font = `${weight} ${size}px ${font}`; m.direction = 'ltr';
  const mt = m.measureText(text), pad = Math.ceil(size * .45) + 24;
  const w = Math.ceil(mt.width), h = Math.ceil(size * (o.lh || 1.5));
  const c = mk(w + pad * 2, h + pad * 2), x = c.getContext('2d');
  x.font = m.font; x.direction = 'ltr'; x.textAlign = 'center'; x.textBaseline = 'middle';
  x.fillStyle = color; x.fillText(text, c.width / 2, c.height / 2);
  return { img: c, text, w, h, pad, size, style: o };
}
const leafD = (L, w) => `M0 0 C ${w} ${-L * .28} ${w * .92} ${-L * .72} 0 ${-L} C ${-w * .92} ${-L * .72} ${-w} ${-L * .28} 0 0 Z`;
