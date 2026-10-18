// ════════════════════════════════════════════════════════════════════
//  motion-doc-studio · helpers — reusable shot building blocks (load after core.js)
//  All are pure functions of t. Coordinates are 1920×1080 stage pixels.
// ════════════════════════════════════════════════════════════════════

// background plate (full-frame image) + god rays — the "set" of most shots
const set = (img, t, a, b, { dim = .62, s0 = 1.0, s1 = 1.05, fx0 = .5, fy0 = .5, fx1 = .5, fy1 = .5, ray = { x: 120, y: -320, ang: .92, int: .11 } } = {}) => {
  if (img) plate(img, t, a, b, { s0, s1, fx0, fy0, fx1, fy1, dim }); else { const k = ease(a, b, t), s = lerp(s0, s1, k); g.save(); g.translate(W / 2, H / 2); g.scale(s, s); g.drawImage(A.bg_dark, -W / 2, -H / 2, W, H); g.restore();
    g.fillStyle = `rgba(16,10,5,${.55 + dim * .35})`; g.fillRect(0, 0, W, H); }   // no plate → dark textured desk
  if (ray) rays(t, ray);
};

// plate + mapping plate pixels → stage pixels (pin overlays on a real photo while the camera moves)
function plateM(img, t, a, b, { s0 = 1, s1 = 1.06, fx0 = .5, fy0 = .5, fx1 = .5, fy1 = .5, dim = 0 } = {}) {
  plate(img, t, a, b, { s0, s1, fx0, fy0, fx1, fy1, dim });
  const k = ease(a, b, t), s = lerp(s0, s1, k), fx = lerp(fx0, fx1, k), fy = lerp(fy0, fy1, k);
  const base = Math.max(W / img.width, H / img.height), w = img.width * base * s, h = img.height * base * s;
  const x = clamp(W / 2 - fx * w, W - w, 0), y = clamp(H / 2 - fy * h, H - h, 0), K = base * s;
  return { K, map: (px, py) => [x + px * K, y + py * K] };
}

// a paper/photo piece drops in (or slides from the right = RTL), breathes, and can exit at t1
const dropP = (p, t, t0, x, y, rot = 0, id = 1, { from = 'drop', t1 = null } = {}) => {
  const k = sp(t, t0, 'card'); if (k <= .001) return null; const ko = t1 ? ease(t1, t1 + .45, t) : 0; if (ko >= 1) return null;
  const b = breathe(id, t, .5); let dx = 0, dy = -(1 - k) * 150; if (from === 'right') { dx = (1 - k) * 900; dy = 0; } else if (from === 'left') { dx = -(1 - k) * 900; dy = 0; }
  dx -= ko * 60; dy += ko * 80; const X = x + dx + b[0], Y = y + dy + b[1], R = rot + (1 - k) * .08 + b[2];
  drawP(p, X, Y, { rot: R, lift: 1 - k, alpha: clamp(k * 3) * (1 - ko) }); return { X, Y, R, k };
};
// draw in the local frame of a piece returned by dropP (origin = piece centre, units = piece px)
const onPiece = (p, r, fn) => { if (!r) return; g.save(); g.translate(r.X, r.Y); g.rotate(r.R); fn(p.w, p.h); g.restore(); };

// name typography (pre-rendered textImg) writes on RTL, exits upward at t1
const nameBlock = (img, t, t0, x, y, t1 = null) => { const k = easeOut(t0, t0 + .9, t), ko = t1 ? ease(t1, t1 + .4, t) : 0; if (ko < 1) writeOn(img, x, y - ko * 60, k, { alpha: 1 - ko }); };

// faint gold construction geometry (circles + axes + rhombus dots) — behind portraits / heroes
const geoHalo = (t, t0, cx, cy, R, color = PAL.gold) => { const k = ease(t0, t0 + 1.6, t); if (k <= 0) return;
  arc(cx, cy, R, k, { width: 1.4, alpha: .5, color }); arc(cx, cy, R * .62, k, { width: 1.2, alpha: .4, dir: 1, color });
  line([[cx - R * 1.25, cy], [cx + R * 1.25, cy]], k, { width: 1.2, alpha: .45, color }); line([[cx, cy - R * 1.2], [cx, cy + R * 1.2]], k, { width: 1.2, alpha: .45, color });
  for (const [dx, dy] of [[R, 0], [-R, 0], [0, R], [0, -R]]) if (k > .8) nuqta(g, cx + dx, cy + dy, 10, color); };

// ink blot / error stain (seeded)
const blob = (x, y, r, seed, color = PAL.ink) => { const R = rng(seed); g.save(); g.fillStyle = color; g.beginPath(); const n = 22;
  for (let i = 0; i <= n; i++) { const a = i / n * 6.283, rr = r * (.75 + R() * .45 + (i % 5 === 0 ? .35 : 0)); i ? g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr) : g.moveTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); }
  g.fill(); for (let i = 0; i < 9; i++) { const a = R() * 6.283, d = r * (1.3 + R() * 1.4), s = r * (.06 + R() * .14); g.beginPath(); g.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, s, 0, 6.283); g.fill(); } g.restore(); };

// recolour any canvas/image with a vertical gold gradient (for hero words in the finale)
function goldify(src, { top = '#f3d58e', mid = '#d4a04a', bot = '#a7742c' } = {}) {
  const c = mk(src.width, src.height), x = c.getContext('2d'); x.drawImage(src, 0, 0); x.globalCompositeOperation = 'source-in';
  const gr = x.createLinearGradient(0, 0, 0, c.height); gr.addColorStop(0, top); gr.addColorStop(.6, mid); gr.addColorStop(1, bot); x.fillStyle = gr; x.fillRect(0, 0, c.width, c.height); return c;
}

// animated counter (Arabic-Indic digits optional) — returns the string for time t
const counter = (t, t0, t1, from, to, { arabic = true, suffix = '' } = {}) => {
  const v = Math.round(lerp(from, to, easeOut(t0, t1, t))); const s = String(v);
  return (arabic ? s.replace(/\d/g, d => '٠١٢٣٤٥٦٧٨٩'[d]) : s) + suffix;
};
// live (non-cached) text, for counters: draws centred RTL text
const liveText = (s, x, y, size, { color = PAL.cream, font = DISPLAY, weight = 700, alpha = 1 } = {}) => {
  g.save(); g.globalAlpha = alpha; g.font = `${weight} ${size * TS}px ${font}`; g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = color; g.fillText(s, x, y); g.restore(); };

// a row/stack of items revealed RTL one after another (the "list" beat). items: [{p, x, y}]
const staggerIn = (items, t, t0, step = .22, from = 'right') => items.forEach((it, i) => dropP(it.p, t, t0 + i * step, it.x, it.y, it.rot || 0, 300 + i, { from }));

// pointer line from a feature to its label (draws on, ends in a rhombus dot)
const callout = (x0, y0, x1, y1, t, t0, color = PAL.goldL) => { const k = ease(t0, t0 + .5, t); if (k <= 0) return;
  line([[x0, y0], [x1, y1]], k, { color, width: 2.4 }); if (k > .95) nuqta(g, x0, y0, 12, color); };
