// ════════════════════════════════════════════════════════════════════
//  motion-doc-studio · fx.js — the "pro" layer (load after core.js + helpers.js)
//  Everything is a pure function of t (seeded noise, no timers). Sections:
//   1 easing (Penner + cubic-bezier + named industry curves) · keyframes · springs · personalities
//   2 noise (seeded simplex) · wiggle · handheld
//   3 colour science (OKLab/OKLCH mix, WCAG contrast)
//   4 2.5D camera rig (dolly/truck/pedestal/roll/orbit/vertigo/rack-focus/handheld) + depth layers
//   5 image ops (tint, outline-sticker, extrude, offset echo / RGB split, pixelate, polaroid)
//   6 post FX (grain, vignette, bloom, halation, chromatic aberration, light leak, LGG grade, looks)
//   7 kinetic typography (RTL word layout, 8 entrance modes, VO-synced karaoke, mask reveal,
//     marker sweep, blur swap, variable-weight morph)
//   8 graphics (rounded panels, hand-drawn circle, SVG path draw-on, burst, sparkles, ring,
//     speech bubble, pill button, cursor + ripple, pixel sprites, phone mock)
//   9 transitions registry TRANS (whip, whipUp, zoom, flash, dip, iris, clock, blinds, push,
//     slide, barn, luma, glitch, smear, band) — used by core render via shot.tin
//  Docs: ../library/easing_timing.md, camera_language.md, transitions.md, kinetic_typography.md,
//        color_systems.md, compositing_fx.md
// ════════════════════════════════════════════════════════════════════

// ── 1 · EASING ───────────────────────────────────────────────────────
const E = (() => {
  const P = Math.PI, c1 = 1.70158, c2 = c1 * 1.525, c3 = c1 + 1, c4 = 2 * P / 3, c5 = 2 * P / 4.5;
  const bOut = x => { const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75; if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; };
  return {
    linear: x => x,
    quadIn: x => x * x, quadOut: x => 1 - (1 - x) * (1 - x), quadInOut: x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2,
    cubicIn: x => x ** 3, cubicOut: x => 1 - Math.pow(1 - x, 3), cubicInOut: x => x < .5 ? 4 * x ** 3 : 1 - Math.pow(-2 * x + 2, 3) / 2,
    quartIn: x => x ** 4, quartOut: x => 1 - Math.pow(1 - x, 4), quartInOut: x => x < .5 ? 8 * x ** 4 : 1 - Math.pow(-2 * x + 2, 4) / 2,
    quintIn: x => x ** 5, quintOut: x => 1 - Math.pow(1 - x, 5), quintInOut: x => x < .5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2,
    sineIn: x => 1 - Math.cos(x * P / 2), sineOut: x => Math.sin(x * P / 2), sineInOut: x => -(Math.cos(P * x) - 1) / 2,
    expoIn: x => x === 0 ? 0 : Math.pow(2, 10 * x - 10), expoOut: x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
    expoInOut: x => x === 0 ? 0 : x === 1 ? 1 : x < .5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2,
    circIn: x => 1 - Math.sqrt(1 - x * x), circOut: x => Math.sqrt(1 - Math.pow(x - 1, 2)),
    circInOut: x => x < .5 ? (1 - Math.sqrt(1 - Math.pow(2 * x, 2))) / 2 : (Math.sqrt(1 - Math.pow(-2 * x + 2, 2)) + 1) / 2,
    backIn: x => c3 * x ** 3 - c1 * x * x, backOut: x => 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2),
    backInOut: x => x < .5 ? (Math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2 : (Math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2,
    elasticIn: x => x === 0 ? 0 : x === 1 ? 1 : -Math.pow(2, 10 * x - 10) * Math.sin((x * 10 - 10.75) * c4),
    elasticOut: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * c4) + 1,
    elasticInOut: x => x === 0 ? 0 : x === 1 ? 1 : x < .5 ? -(Math.pow(2, 20 * x - 10) * Math.sin((20 * x - 11.125) * c5)) / 2 : (Math.pow(2, -20 * x + 10) * Math.sin((20 * x - 11.125) * c5)) / 2 + 1,
    bounceOut: bOut, bounceIn: x => 1 - bOut(1 - x), bounceInOut: x => x < .5 ? (1 - bOut(1 - 2 * x)) / 2 : (1 + bOut(2 * x - 1)) / 2,
    steps: n => x => Math.floor(x * n) / n,                      // "on twos/threes" stepped motion
  };
})();
// CSS-style cubic-bezier(x1,y1,x2,y2) → easing function (Newton + bisection, like browsers)
function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const X = s => ((ax * s + bx) * s + cx) * s, Y = s => ((ay * s + by) * s + cy) * s, dX = s => (3 * ax * s + 2 * bx) * s + cx;
  return x => { if (x <= 0) return 0; if (x >= 1) return 1; let s = x;
    for (let i = 0; i < 8; i++) { const e = X(s) - x; if (Math.abs(e) < 1e-6) return Y(s); const d = dX(s); if (Math.abs(d) < 1e-6) break; s -= e / d; }
    let lo = 0, hi = 1; s = x; for (let i = 0; i < 30; i++) { const v = X(s); if (Math.abs(v - x) < 1e-6) break; if (x > v) lo = s; else hi = s; s = (lo + hi) / 2; } return Y(s); };
}
// named industry curves (see library/easing_timing.md)
const CURVE = {
  md3: bezier(.2, 0, 0, 1), md3Emph: bezier(.05, .7, .1, 1), md3Accel: bezier(.3, 0, 1, 1),
  apple: bezier(.25, .1, .25, 1), premium: bezier(.4, 0, .2, 1), signature: bezier(.22, 1, .36, 1),
  expoOut: bezier(.16, 1, .3, 1), camera: bezier(.65, 0, .35, 1), overshoot: bezier(.34, 1.56, .64, 1),
  bounceSettle: bezier(.175, .885, .32, 1.275), anticipate: bezier(.36, 0, .66, -.56), whip: bezier(.7, 0, .2, 1),
};
const tw = (t, a, b, fn = CURVE.signature) => fn(clamp((t - a) / (b - a)));          // eased progress 0→1
// keyframes: kf(t, [[t0,v0],[t1,v1,ease?],…]) — v may be a number or an array; ease applies to the segment INTO that key
function kf(t, keys) {
  if (t <= keys[0][0]) return keys[0][1]; const L = keys[keys.length - 1]; if (t >= L[0]) return L[1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [ta, va] = keys[i - 1], [tb, vb, fn] = keys[i], k = (fn || CURVE.camera)((t - ta) / (tb - ta));
    return Array.isArray(va) ? va.map((v, j) => lerp(v, vb[j], k)) : lerp(va, vb, k); }
}
// spring library (stiffness, damping; mass 1). Use spr(t, t0, 'wobbly'). core SPR presets stay the film's 3 house springs.
const SPRINGS = { default: [170, 26], gentle: [120, 14], wobbly: [180, 12], stiff: [210, 20], slow: [280, 60], molasses: [280, 120],
  card: [150, 19], snap: [320, 28], soft: [60, 15], pop: [400, 22], jelly: [260, 10] };
const spr = (t, t0, name = 'default') => spring(t - t0, ...(SPRINGS[name] || SPRINGS.default));
// motion personalities: pick ONE per film (library/easing_timing.md §1)
const PERSONA = {
  documentary: { dur: .6, ease: CURVE.camera, enter: CURVE.signature, exit: CURVE.md3Accel, spring: 'card', stagger: .09, overshoot: .03 },
  premium:     { dur: .5, ease: CURVE.premium, enter: CURVE.premium, exit: CURVE.md3Accel, spring: 'slow', stagger: .1, overshoot: 0 },
  corporate:   { dur: .3, ease: CURVE.md3, enter: CURVE.md3Emph, exit: CURVE.md3Accel, spring: 'stiff', stagger: .06, overshoot: .02 },
  playful:     { dur: .25, ease: E.backOut, enter: CURVE.overshoot, exit: E.backIn, spring: 'wobbly', stagger: .05, overshoot: .15 },
  energetic:   { dur: .18, ease: E.expoOut, enter: CURVE.expoOut, exit: E.expoIn, spring: 'pop', stagger: .035, overshoot: .2 },
  stickerpop:  { dur: .28, ease: CURVE.overshoot, enter: CURVE.overshoot, exit: CURVE.md3Accel, spring: 'snap', stagger: .07, overshoot: .1 },
};

// ── 2 · NOISE (seeded 2D simplex) ────────────────────────────────────
const NOISE = (() => {
  const perm = new Uint8Array(512), r = rng(1337), p = [...Array(256).keys()];
  for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; }
  for (let i = 0; i < 512; i++) perm[i] = p[i & 255];
  const G = [[1, 1], [-1, 1], [1, -1], [-1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]], F2 = .5 * (Math.sqrt(3) - 1), G2 = (3 - Math.sqrt(3)) / 6;
  return (x, y) => { const s = (x + y) * F2, i = Math.floor(x + s), j = Math.floor(y + s), t0 = (i + j) * G2, x0 = x - (i - t0), y0 = y - (j - t0);
    const i1 = x0 > y0 ? 1 : 0, j1 = 1 - i1, x1 = x0 - i1 + G2, y1 = y0 - j1 + G2, x2 = x0 - 1 + 2 * G2, y2 = y0 - 1 + 2 * G2, ii = i & 255, jj = j & 255;
    const c = (gx, gy, xx, yy) => { let tt = .5 - xx * xx - yy * yy; if (tt < 0) return 0; const g8 = G[gx % 8]; tt *= tt; return tt * tt * (g8[0] * xx + g8[1] * yy); };
    return 70 * (c(perm[ii + perm[jj]], 0, x0, y0) + c(perm[ii + i1 + perm[jj + j1]], 0, x1, y1) + c(perm[ii + 1 + perm[jj + 1]], 0, x2, y2)); };
})();
const noise2 = NOISE;                                                                   // −1…1
const fbm = (x, y, oct = 4) => { let v = 0, a = .5, f = 1; for (let i = 0; i < oct; i++) { v += a * noise2(x * f, y * f); a *= .5; f *= 2; } return v; };
const wiggle = (t, freq = 1, amp = 1, seed = 1) => amp * fbm(t * freq, seed * 17.31, 2);   // After-Effects style wiggle()
const handheld = (t, amp = 6, freq = .55, seed = 3) => ({ x: wiggle(t, freq, amp, seed), y: wiggle(t, freq * .9, amp * .7, seed + 5), r: wiggle(t, freq * .6, amp * .0009, seed + 9) });

// ── 3 · COLOUR SCIENCE ───────────────────────────────────────────────
const hex2rgb = h => { h = h.replace('#', ''); if (h.length === 3) h = h.split('').map(c => c + c).join(''); const n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; };
const rgb2hex = c => '#' + c.map(v => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join('');
const s2l = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
const l2s = v => 255 * (v <= .0031308 ? 12.92 * v : 1.055 * Math.pow(Math.max(0, v), 1 / 2.4) - .055);
function rgb2oklab([R, G, B]) { const r = s2l(R), g2 = s2l(G), b = s2l(B);
  const l = Math.cbrt(.4122214708 * r + .5363325363 * g2 + .0514459929 * b), m = Math.cbrt(.2119034982 * r + .6806995451 * g2 + .1073969566 * b), s = Math.cbrt(.0883024619 * r + .2817188376 * g2 + .6299787005 * b);
  return [.2104542553 * l + .793617785 * m - .0040720468 * s, 1.9779984951 * l - 2.428592205 * m + .4505937099 * s, .0259040371 * l + .7827717662 * m - .808675766 * s]; }
function oklab2rgb([L, a, b]) { const l = (L + .3963377774 * a + .2158037573 * b) ** 3, m = (L - .1055613458 * a - .0638541728 * b) ** 3, s = (L - .0894841775 * a - 1.291485548 * b) ** 3;
  return [l2s(4.0767416621 * l - 3.3077115913 * m + .2309699292 * s), l2s(-1.2684380046 * l + 2.6097574011 * m - .3413193965 * s), l2s(-.0041960863 * l - .7034186147 * m + 1.707614701 * s)]; }
const oklch = (L, C, H) => rgb2hex(oklab2rgb([L, C * Math.cos(H * Math.PI / 180), C * Math.sin(H * Math.PI / 180)]));   // oklch(.78,.17,50) → hex
const mixOK = (a, b, k) => { const A = rgb2oklab(hex2rgb(a)), B = rgb2oklab(hex2rgb(b)); return rgb2hex(oklab2rgb(A.map((v, i) => lerp(v, B[i], k)))); };   // perceptual mix, never muddy
const lum = h => { const [r, g2, b] = hex2rgb(h).map(s2l); return .2126 * r + .7152 * g2 + .0722 * b; };
const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };    // WCAG ratio (≥4.5 body, ≥3 display)
const rgba = (h, a) => { const [r, g2, b] = hex2rgb(h); return `rgba(${r},${g2},${b},${a})`; };

// ── 4 · 2.5D CAMERA RIG ──────────────────────────────────────────────
// Set the camera once per frame with cam({...}); then draw scene planes with layer(depth, fn).
// depth 1 = subject plane, 2 = twice as far (moves half as much), .5 = foreground (moves 2×).
//  x,y  truck/pedestal (px at subject plane)   z  dolly/zoom (1 = none)   r roll (rad)
//  ox   orbit offset: subject stays, fg/bg slide opposite (fake orbit/arc shot)
//  vz   vertigo (dolly-zoom): background scales, subject size constant
//  fd   focus depth, ap aperture (px of blur per unit of defocus) → rack focus
let CAM = { x: 0, y: 0, z: 1, r: 0, ox: 0, vz: 0, fd: 1, ap: 0 };
function cam(st = {}, t = null, shakeAmp = 0) {
  CAM = Object.assign({ x: 0, y: 0, z: 1, r: 0, ox: 0, vz: 0, fd: 1, ap: 0 }, st);
  if (shakeAmp && t !== null) { const h = handheld(t, shakeAmp); CAM.x += h.x; CAM.y += h.y; CAM.r += h.r; }
  return CAM;
}
// camera move from keyframes: camKeys(t, {z:[[2,1],[5,1.15]], x:[[2,0],[5,-80]]}, base)
function camKeys(t, keys, base = {}) { const st = Object.assign({}, base); for (const [k, v] of Object.entries(keys)) st[k] = kf(t, v); return st; }
function layer(depth, fn, { blurMax = 14 } = {}) {
  const p = 1 / depth, s = (1 + (CAM.z - 1) * p) * (1 + CAM.vz * (1 - p));
  const tx = CAM.x * p + CAM.ox * (p - 1), ty = CAM.y * p;
  g.save(); g.translate(W / 2, H / 2); g.rotate(CAM.r * p); g.scale(s, s); g.translate(-W / 2 - tx, -H / 2 - ty);
  const bl = Math.min(blurMax, CAM.ap * Math.abs(p - 1 / CAM.fd)); if (bl > .4) g.filter = `blur(${bl.toFixed(1)}px)`;
  fn(); g.filter = 'none'; g.restore();
}
// shake on impact (decaying), returns {x,y,r} to add into cam()
const impact = (t, t0, amp = 18, f = 38) => { if (t < t0) return { x: 0, y: 0, r: 0 }; const d = Math.exp(-(t - t0) * 7); return { x: amp * d * Math.sin((t - t0) * f), y: amp * .6 * d * Math.cos((t - t0) * f * 1.3), r: amp * .0006 * d * Math.sin((t - t0) * f * .7) }; };

// ── 5 · IMAGE OPS (pre-render in INITS where possible) ───────────────
const _tintC = new Map();
function tint(img, color) { const key = img; let m = _tintC.get(key); if (!m) _tintC.set(key, m = {}); if (m[color]) return m[color];
  const c = mk(img.width, img.height), x = c.getContext('2d'); x.drawImage(img, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = color; x.fillRect(0, 0, c.width, c.height); return m[color] = c; }
// sticker outline (die-cut border) around any alpha image
function outline(img, px = 10, color = '#fff', { shadow = 'rgba(0,0,0,.25)', sh = 8 } = {}) {
  const pad = px + sh + 4, c = mk(img.width + pad * 2, img.height + pad * 2), x = c.getContext('2d'), T = tint(img, color);
  if (shadow) { const S = tint(img, '#000'); x.globalAlpha = 1; x.filter = `blur(${sh}px)`; x.globalAlpha = .5; for (let a = 0; a < 16; a++) x.drawImage(S, pad + Math.cos(a / 16 * 6.283) * px, pad + sh * .7 + Math.sin(a / 16 * 6.283) * px); x.filter = 'none'; x.globalAlpha = 1; }
  for (let a = 0; a < 24; a++) x.drawImage(T, pad + Math.cos(a / 24 * 6.283) * px, pad + Math.sin(a / 24 * 6.283) * px);
  x.drawImage(img, pad, pad); return c;
}
// hard 3D extrude (flat "sticker type"): depth px along angle, solid colour
function extrude(img, depth = 10, ang = Math.PI * .25, color = '#05a0a2') {
  const dx = Math.cos(ang), dy = Math.sin(ang), c = mk(img.width + depth + 4, img.height + depth + 4), x = c.getContext('2d'), T = tint(img, color);
  const ox = dx < 0 ? depth : 0, oy = dy < 0 ? depth : 0; for (let i = depth; i >= 1; i--) x.drawImage(T, ox + dx * i, oy + dy * i); x.drawImage(img, ox, oy); return c;
}
// offset echo / RGB split: draw coloured copies behind (light bg: multiply; dark bg: screen)
function echo(img, x, y, layers = [{ dx: 6, dy: 4, color: '#05a0a2' }], { sc = 1, alpha = 1, ax = .5, ay = .5, rot = 0, blend = 'source-over' } = {}) {
  const w = img.width * sc, h = img.height * sc; g.save(); g.translate(x, y); g.rotate(rot); g.globalAlpha = alpha;
  g.globalCompositeOperation = blend; for (const L of layers) g.drawImage(tint(img, L.color), -w * ax + L.dx, -h * ay + L.dy, w, h);
  g.globalCompositeOperation = 'source-over'; g.drawImage(img, -w * ax, -h * ay, w, h); g.restore();
}
const rgbSplit = (img, x, y, amt = 6, o = {}) => echo(img, x, y, [{ dx: -amt, dy: 0, color: '#ff2a4d' }, { dx: amt, dy: 0, color: '#00d9ff' }], o);
// pixelate any image (pixel-art look); draw result with imageSmoothingEnabled = false
function pixelate(img, block = 6) { const w = Math.ceil(img.width / block), h = Math.ceil(img.height / block), s = mk(w, h), sx = s.getContext('2d');
  sx.imageSmoothingEnabled = true; sx.drawImage(img, 0, 0, w, h); const c = mk(w * block, h * block), x = c.getContext('2d'); x.imageSmoothingEnabled = false; x.drawImage(s, 0, 0, c.width, c.height); return c; }
// polaroid / instant-photo frame for any image
function polaroid(img, { w = 220, pad = 14, bottom = 46, bg = '#fbf8f1', seed = 1 } = {}) {
  const k = (w - pad * 2) / img.width, ih = img.height * k, c = mk(w + 24, ih + pad + bottom + 24), x = c.getContext('2d');
  x.shadowColor = 'rgba(0,0,0,.22)'; x.shadowBlur = 14; x.shadowOffsetY = 6; x.fillStyle = bg; x.fillRect(12, 8, w, ih + pad + bottom); x.shadowColor = 'transparent';
  x.drawImage(img, 12 + pad, 8 + pad, w - pad * 2, ih); return c;
}

// ── 6 · POST FX (call in FILM.post, after the frame is drawn) ────────
const _fx = {}; const fxBuf = (k, w = W, h = H) => { if (!_fx[k] || _fx[k].width !== w) { _fx[k] = mk(w, h); } return _fx[k]; };
function fxGrain(t, amt = .06, blend = 'overlay', fps = 12) { if (!grain.length) return; g.save(); g.globalCompositeOperation = blend; g.globalAlpha = amt; g.drawImage(grain[Math.floor(t * fps) % grain.length], 0, 0, W, H); g.restore(); }
function fxVignette(amt = .5, { color = '0,0,0', inner = .35, cx = .5, cy = .5 } = {}) {
  const key = `v${amt}${color}${inner}${cx}${cy}`; let c = _fx[key];
  if (!c) { c = _fx[key] = mk(W, H); const x = c.getContext('2d'), gr = x.createRadialGradient(W * cx, H * cy, H * inner, W * cx, H * cy, H * 1.05);
    gr.addColorStop(0, `rgba(${color},0)`); gr.addColorStop(1, `rgba(${color},${amt})`); x.fillStyle = gr; x.fillRect(0, 0, W, H); }
  g.drawImage(c, 0, 0);
}
// bloom: isolate highlights (x³ via self-multiply on a ¼-res copy), blur, screen back
function fxBloom(strength = .45, radius = 18, { tintColor = null, power = 2 } = {}) {
  const s = fxBuf('bloom', W / 4, H / 4), x = s.getContext('2d'); x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1; x.drawImage(cv, 0, 0, s.width, s.height);
  x.globalCompositeOperation = 'multiply'; for (let i = 0; i < power; i++) x.drawImage(s, 0, 0);
  if (tintColor) { x.fillStyle = tintColor; x.fillRect(0, 0, s.width, s.height); }
  g.save(); g.globalCompositeOperation = 'screen'; g.globalAlpha = strength; g.filter = `blur(${radius}px)`; g.drawImage(s, 0, 0, W, H); g.restore();
}
const fxHalation = (strength = .35, radius = 10) => fxBloom(strength, radius, { tintColor: '#ff6a3a', power: 3 });   // film halation: red glow on highlights
// chromatic aberration: 'lens' (radial, grows to edges) or 'shift'
function fxChroma(amt = 2.5, mode = 'lens') {
  const src = fxBuf('caS'); src.getContext('2d').drawImage(cv, 0, 0);
  const ch = (key, col) => { const c = fxBuf(key), x = c.getContext('2d'); x.globalCompositeOperation = 'source-over'; x.drawImage(src, 0, 0); x.globalCompositeOperation = 'multiply'; x.fillStyle = col; x.fillRect(0, 0, W, H); return c; };
  const R = ch('caR', '#f00'), G = ch('caG', '#0f0'), B = ch('caB', '#00f');
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.fillStyle = '#000'; g.fillRect(0, 0, W, H); g.globalCompositeOperation = 'lighter';
  const put = (c, k) => { if (mode === 'lens') { const s = 1 + k * amt / W * 2; g.drawImage(c, W / 2 - W * s / 2, H / 2 - H * s / 2, W * s, H * s); } else g.drawImage(c, k * amt, 0); };
  put(R, 1); put(G, 0); put(B, -1); g.restore();
}
// light leak: big warm blobs drifting on noise (screen)
function fxLeak(t, { int = .35, seed = 1, colors = ['255,140,60', '255,60,90', '255,210,120'], speed = .08 } = {}) {
  g.save(); g.globalCompositeOperation = 'screen';
  colors.forEach((c, i) => { const x = W * (.5 + .7 * noise2(t * speed, seed + i * 3.1)), y = H * (.5 + .6 * noise2(seed + i * 7.7, t * speed)), r = H * (.5 + .25 * noise2(t * speed * .7, i + seed * 2));
    const a = int * (.55 + .45 * noise2(t * .3, i * 9 + seed)); const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(${c},${Math.max(0, a)})`); gr.addColorStop(1, `rgba(${c},0)`); g.fillStyle = gr; g.fillRect(0, 0, W, H); });
  g.restore();
}
// lift / gamma / gain + saturation + split-tone (per-pixel, ~25 ms @1080p). Order: LGG → contrast → sat → split-tone.
// opts: {lift:[r,g,b] (−.1….1), gamma:[…] (.8…1.2), gain:[…] (.8…1.2), contrast:1, sat:1, shadows:'#1d4a5a', highlights:'#ffb070', split:.12}
const _lut = {};
function fxGrade(o = {}) {
  const key = JSON.stringify(o); let L = _lut[key];
  if (!L) { L = _lut[key] = [0, 1, 2].map(ch => { const a = new Uint8ClampedArray(256), lf = (o.lift || [0, 0, 0])[ch], gm = (o.gamma || [1, 1, 1])[ch], gn = (o.gain || [1, 1, 1])[ch], ct = o.contrast || 1;
    for (let i = 0; i < 256; i++) { let v = i / 255; v = v * gn + lf * (1 - v); v = Math.pow(clamp(v), 1 / gm); v = (v - .5) * ct + .5; a[i] = clamp(v) * 255; } return a; }); }
  const img = g.getImageData(0, 0, W, H), d = img.data, sat = o.sat ?? 1, sp = o.split || 0, S = o.shadows ? hex2rgb(o.shadows) : null, Hh = o.highlights ? hex2rgb(o.highlights) : null;
  for (let i = 0; i < d.length; i += 4) { let r = L[0][d[i]], gg = L[1][d[i + 1]], b = L[2][d[i + 2]];
    if (sat !== 1 || sp) { const y = .2126 * r + .7152 * gg + .0722 * b; r = y + (r - y) * sat; gg = y + (gg - y) * sat; b = y + (b - y) * sat;
      if (sp) { const l = y / 255, ws = sp * (1 - l) * (1 - l), wh = sp * l * l; if (S) { r += (S[0] - r) * ws; gg += (S[1] - gg) * ws; b += (S[2] - b) * ws; } if (Hh) { r += (Hh[0] - r) * wh; gg += (Hh[1] - gg) * wh; b += (Hh[2] - b) * wh; } } }
    d[i] = r; d[i + 1] = gg; d[i + 2] = b; }
  g.putImageData(img, 0, 0);
}
// LOOKS = finished post chains. FILM.post = t => fxLook(t, 'pop')
const LOOKS = {
  sepia: t => grade(t),                                                                         // the house documentary grade (core.js)
  clean: t => { fxGrain(t, .035); },
  pop: t => { fxGrain(t, .045, 'overlay'); fxVignette(.18, { inner: .55 }); },                  // flat sticker/explainer: almost no grade
  film: t => { fxHalation(.22, 10); fxGrain(t, .08, 'overlay', 24); fxVignette(.45); },
  tealOrange: t => { fxGrade({ contrast: 1.08, sat: 1.05, shadows: '#0f4c5c', highlights: '#ffb36b', split: .16 }); fxGrain(t, .05); fxVignette(.4); },
  noir: t => { fxGrade({ contrast: 1.25, sat: 0, lift: [.02, .02, .02] }); fxGrain(t, .1, 'overlay', 24); fxVignette(.6); },
  dream: t => { fxBloom(.4, 26); fxLeak(t, { int: .22 }); fxGrain(t, .04); },
  vhs: t => { fxChroma(3, 'shift'); fxGrain(t, .09, 'overlay', 30); fxVignette(.35); },
};
const fxLook = (t, name) => (LOOKS[name] || LOOKS.clean)(t);

// ── 7 · KINETIC TYPOGRAPHY ───────────────────────────────────────────
// Arabic letters JOIN: never split Arabic per letter (it breaks shaping). Animate per WORD, or reveal
// whole lines with masks. Per-letter stagger is for Latin only (letters(…)).
// layoutWords('تعال يا *ابني*', {size:96, font:UI, weight:800, color, accent:{font:'Ruqaa', color:'#05a0a2'}, maxW:900})
//  → {words:[{img,x,y,w,h,acc}], w, h}  positions are relative to the block centre; RTL line order.
function layoutWords(text, { size = 80, font = UI, weight = 800, color = PAL.ink, accent = null, maxW = 1100, lh = 1.25, gap = .28, align = 'right', dir = 'rtl' } = {}) {
  const m = mk(8, 8).getContext('2d'), toks = text.split(/\s+/).filter(Boolean).map(w => { const acc = /^\*.*\*$/.test(w); return { s: acc ? w.slice(1, -1) : w, acc }; });
  const words = toks.map(tk => { const st = tk.acc && accent ? Object.assign({ size, font, weight, color }, accent) : { size, font, weight, color };
    const px = st.size * TS; m.font = `${st.weight} ${px}px ${st.font}`; m.direction = dir; const wd = m.measureText(tk.s).width, hh = px * 1.45;
    const c = mk(wd + px * .3, hh), x = c.getContext('2d'); x.font = m.font; x.direction = dir; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = st.color; x.fillText(tk.s, c.width / 2, hh / 2 + (st.dy || 0) * px);
    return { img: c, w: c.width, h: hh, acc: tk.acc, s: tk.s }; });
  const sp = size * TS * gap, lines = [[]]; let cur = 0;
  for (const w of words) { if (cur && cur + sp + w.w > maxW) { lines.push([]); cur = 0; } lines[lines.length - 1].push(w); cur += (cur ? sp : 0) + w.w; }
  const lineH = size * TS * lh * 1.1, bw = Math.max(...lines.map(L => L.reduce((a, w) => a + w.w, 0) + sp * (L.length - 1))), bh = lineH * lines.length;
  lines.forEach((L, li) => { const lw = L.reduce((a, w) => a + w.w, 0) + sp * (L.length - 1); let x = align === 'center' ? lw / 2 : align === 'left' ? -bw / 2 + lw : bw / 2;
    if (dir === 'ltr') x = align === 'center' ? -lw / 2 : align === 'right' ? bw / 2 - lw : -bw / 2;
    for (const w of L) { if (dir === 'rtl') { w.x = x - w.w / 2; x -= w.w + sp; } else { w.x = x + w.w / 2; x += w.w + sp; } w.y = -bh / 2 + lineH * (li + .5); } });
  return { words, w: bw, h: bh };
}
// draw a word layout with an entrance mode. times: optional per-word absolute start times (VO sync).
// modes: pop | rise | mask | blur | slam | type | drop | swing
function drawWords(Lw, t, t0, x, y, { mode = 'pop', stagger = .08, times = null, sc = 1, alpha = 1, t1 = null, exit = 'fade', springName = 'snap', hiColor = null, rot = 0 } = {}) {
  const ko = t1 ? tw(t, t1, t1 + .3, CURVE.md3Accel) : 0; if (ko >= 1) return;
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(sc, sc);
  Lw.words.forEach((w, i) => { const ts = times ? times[i] : t0 + i * stagger; if (t < ts) return; const dt = t - ts;
    let k = spr(t, ts, springName), dx = 0, dy = 0, s = 1, r = 0, a = clamp(dt * 8), bl = 0, clipY = null;
    if (mode === 'pop') { s = lerp(.6, 1, k); r = (1 - k) * .12 * (i % 2 ? 1 : -1); }
    else if (mode === 'rise') { dy = (1 - k) * 60; a = clamp(dt * 6); }
    else if (mode === 'mask') { dy = (1 - tw(t, ts, ts + .45, CURVE.expoOut)) * w.h; clipY = true; a = 1; }
    else if (mode === 'blur') { const e = tw(t, ts, ts + .4, CURVE.signature); bl = (1 - e) * 14; s = lerp(1.08, 1, e); a = e; }
    else if (mode === 'slam') { const e = tw(t, ts, ts + .22, E.expoOut); s = lerp(2.4, 1, e); a = clamp(dt * 12); }
    else if (mode === 'type') { s = dt < .07 ? 1.12 : 1; a = 1; }
    else if (mode === 'drop') { dy = -(1 - spr(t, ts, 'wobbly')) * 120; r = (1 - spr(t, ts, 'wobbly')) * .2; }
    else if (mode === 'swing') { r = (1 - spr(t, ts, 'jelly')) * .5; a = clamp(dt * 6); }
    if (ko) { if (exit === 'fade') a *= 1 - ko; else { dy -= ko * 50; a *= 1 - ko; } }
    g.save(); g.globalAlpha = a * alpha;
    if (clipY) { g.beginPath(); g.rect(w.x - w.w / 2 - 4, w.y - w.h / 2, w.w + 8, w.h); g.clip(); }
    g.translate(w.x + dx, w.y + dy); g.rotate(r); g.scale(s, s); if (bl > .3) g.filter = `blur(${bl.toFixed(1)}px)`;
    const im = hiColor && times && i === activeIndex(times, t) ? tint(w.img, hiColor) : w.img;
    g.drawImage(im, -w.w / 2, -w.h / 2); g.restore(); });
  g.restore();
}
const activeIndex = (times, t) => { let a = -1; for (let i = 0; i < times.length; i++) if (t >= times[i]) a = i; return a; };
// VO word timings → per-word start times for a caption: voTimes(WORDS, 3.2, 4) (WORDS = [{w,s,e}] from tools/transcribe.py)
const voTimes = (WORDS, from, n) => { const i0 = WORDS.findIndex(w => (w.s ?? w.start) >= from - .05); return WORDS.slice(i0, i0 + n).map(w => w.s ?? w.start); };
// Latin per-letter stagger (Arabic: use layoutWords)
function letters(s, x, y, t, t0, { size = 80, font = UI, weight = 800, color = PAL.ink, stagger = .03, mode = 'rise' } = {}) {
  g.save(); g.font = `${weight} ${size * TS}px ${font}`; g.textBaseline = 'middle'; g.fillStyle = color; let cx = x - g.measureText(s).width / 2;
  for (let i = 0; i < s.length; i++) { const ch = s[i], w = g.measureText(ch).width, k = spr(t, t0 + i * stagger, 'snap'); if (k > 0) { g.save(); g.globalAlpha = clamp(k * 2);
    g.translate(cx + w / 2, y + (mode === 'rise' ? (1 - k) * 40 : 0)); if (mode === 'pop') g.scale(k, k); g.fillText(ch, -w / 2, 0); g.restore(); } cx += w; }
  g.restore();
}
// directional mask reveal of any image: dir 'rtl' | 'ltr' | 'up' | 'down', soft edge in px
function maskReveal(img, x, y, k, { dir = 'rtl', sc = 1, ax = .5, ay = .5, alpha = 1, soft = 0 } = {}) {
  if (k <= 0) return; const w = img.width * sc, h = img.height * sc, x0 = x - w * ax, y0 = y - h * ay; k = clamp(k);
  g.save(); g.globalAlpha = alpha; g.beginPath();
  if (dir === 'rtl') g.rect(x0 + w * (1 - k) - soft, y0 - 4, w * k + soft + 4, h + 8); else if (dir === 'ltr') g.rect(x0 - 4, y0 - 4, w * k + 4, h + 8);
  else if (dir === 'up') g.rect(x0 - 4, y0 + h * (1 - k), w + 8, h * k + 4); else g.rect(x0 - 4, y0 - 4, w + 8, h * k + 4);
  g.clip(); g.drawImage(img, x0, y0, w, h); g.restore();
}
// highlighter marker sweeping behind a word (RTL by default)
function marker(x, y, w, h, k, { color = '#f8bb3e', dir = 'rtl', skew = -.06, r = 6 } = {}) { if (k <= 0) return; k = clamp(k);
  g.save(); g.fillStyle = color; g.transform(1, 0, skew, 1, 0, 0); const ww = w * k, xx = dir === 'rtl' ? x + w / 2 - ww : x - w / 2; rrect(xx, y - h / 2, ww, h, r); g.fill(); g.restore(); }
// swap one word image for another with a blur cross (copy change)
function blurSwap(a, b, t, t0, x, y, { dur = .35, sc = 1 } = {}) { const k = tw(t, t0, t0 + dur, CURVE.md3);
  const one = (im, al, bl, s) => { if (al <= 0) return; g.save(); g.globalAlpha = al; if (bl > .3) g.filter = `blur(${bl}px)`; g.translate(x, y); g.scale(s * sc, s * sc); g.drawImage(im, -im.width / 2, -im.height / 2); g.restore(); };
  one(a, 1 - k, k * 16, 1 + k * .06); one(b, k, (1 - k) * 16, 1.06 - k * .06); }
// variable-font weight morph (fonts with a wght axis: Kufi, Readex, Changa, Marhey, ElMessiri) — cached per 20 units
const _wm = {}; function weightText(s, wt, { size = 90, font = UI, color = PAL.ink } = {}) { const q = Math.round(wt / 20) * 20, key = s + '|' + q + '|' + size + font + color;
  return _wm[key] || (_wm[key] = textImg([{ t: s, size, font, weight: q, color }])); }

// ── 8 · GRAPHICS ─────────────────────────────────────────────────────
function rrect(x, y, w, h, r = 18, c = g) { r = Math.max(0, Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2)); c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
// rounded panel that slides/scales in (split-screen layouts). from: 'left'|'right'|'up'|'down'|'scale'
function panel(x, y, w, h, t, t0, { fill = '#05a0a2', r = 22, from = 'scale', springName = 'snap', shadow = true, t1 = null, content = null } = {}) {
  const k = spr(t, t0, springName); if (k <= .001) return null; const ko = t1 ? tw(t, t1, t1 + .3, CURVE.md3Accel) : 0; if (ko >= 1) return null;
  let dx = 0, dy = 0, s = 1; if (from === 'left') dx = -(1 - k) * (w + 200); else if (from === 'right') dx = (1 - k) * (w + 200); else if (from === 'up') dy = -(1 - k) * (h + 200); else if (from === 'down') dy = (1 - k) * (h + 200); else s = lerp(.9, 1, k);
  dy += ko * 40; g.save(); g.globalAlpha = (from === 'scale' ? clamp(k * 3) : 1) * (1 - ko); g.translate(x + w / 2 + dx, y + h / 2 + dy); g.scale(s, s);
  if (shadow) { g.shadowColor = 'rgba(0,0,0,.18)'; g.shadowBlur = 30; g.shadowOffsetY = 12; } g.fillStyle = fill; rrect(-w / 2, -h / 2, w, h, r); g.fill(); g.shadowColor = 'transparent';
  if (content) { g.save(); rrect(-w / 2, -h / 2, w, h, r); g.clip(); content(w, h); g.restore(); }
  g.restore(); return { X: x + dx, Y: y + dy, k };
}
// hand-drawn wobbly ellipse that draws itself (circle-the-target)
function handCircle(cx, cy, rx, ry, k, { color = '#05a0a2', width = 9, seed = 2, turns = 1.12, a0 = -2.2 } = {}) {
  if (k <= 0) return; const r = rng(seed), wob = [r(), r(), r()], n = 90, end = Math.floor(n * clamp(k)); g.save(); g.strokeStyle = color; g.lineWidth = width; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath();
  for (let i = 0; i <= end; i++) { const u = i / n, a = a0 - u * turns * 6.283, j = 1 + .05 * Math.sin(u * 9 + wob[0] * 6) + .04 * u + .02 * Math.sin(u * 23 + wob[1] * 6);
    const px = cx + Math.cos(a) * rx * j, py = cy + Math.sin(a) * ry * j; i ? g.lineTo(px, py) : g.moveTo(px, py); } g.stroke(); g.restore();
}
// SVG path draw-on: pathDraw('M10 10 C …', k, {x,y,sc,color,width}) — length measured once via an SVG element
const _plen = {}; function pathLen(d) { if (_plen[d]) return _plen[d]; const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); return _plen[d] = p.getTotalLength(); }
function pathDraw(d, k, { x = 0, y = 0, sc = 1, color = PAL.ink, width = 6, fill = null, fillK = 0 } = {}) {
  if (k <= 0) return; const L = pathLen(d), P = new Path2D(d); g.save(); g.translate(x, y); g.scale(sc, sc); g.lineCap = 'round'; g.lineJoin = 'round';
  if (fill && fillK > 0) { g.globalAlpha = clamp(fillK); g.fillStyle = fill; g.fill(P); g.globalAlpha = 1; }
  g.strokeStyle = color; g.lineWidth = width / sc; g.setLineDash([L * clamp(k), L + 1]); g.stroke(P); g.restore();
}
// impact burst lines (comic "pow")
function burst(cx, cy, t, t0, { n = 10, r0 = 60, r1 = 150, color = PAL.ink, width = 7, seed = 4, dur = .35 } = {}) {
  const k = tw(t, t0, t0 + dur, E.expoOut); if (k <= 0 || k >= 1) return; const r = rng(seed), out = tw(t, t0 + dur * .35, t0 + dur, E.quadIn);
  g.save(); g.strokeStyle = color; g.lineWidth = width; g.lineCap = 'round'; for (let i = 0; i < n; i++) { const a = i / n * 6.283 + r() * .3, a1 = lerp(r0, r1, k), a0 = lerp(r0, r1, out) * (.9 + r() * .1);
    g.beginPath(); g.moveTo(cx + Math.cos(a) * a0, cy + Math.sin(a) * a0); g.lineTo(cx + Math.cos(a) * a1, cy + Math.sin(a) * a1); g.stroke(); } g.restore();
}
// 4-point twinkle stars around a point
function sparkles(cx, cy, R, t, t0, { n = 6, color = '#fff', size = 12, seed = 7 } = {}) { const r = rng(seed); if (t < t0) return;
  for (let i = 0; i < n; i++) { const a = r() * 6.283, d = R * (.6 + r() * .5), ph = r() * 6, s = size * (.5 + r() * .7) * clamp((t - t0 - i * .05) * 5) * (.6 + .4 * Math.sin(t * 7 + ph)); if (s <= 0) continue;
    const x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d; g.save(); g.fillStyle = color; g.translate(x, y); g.beginPath(); g.moveTo(0, -s); g.quadraticCurveTo(0, 0, s, 0); g.quadraticCurveTo(0, 0, 0, s); g.quadraticCurveTo(0, 0, -s, 0); g.quadraticCurveTo(0, 0, 0, -s); g.fill(); g.restore(); } }
const ring = (cx, cy, r, k, { color = '#fff', width = 3, dash = [2, 10], rot = 0, alpha = 1 } = {}) => arc(cx, cy, r, k, { color, width, dash, a0: -Math.PI / 2 + rot, alpha });
// speech bubble canvas (hard offset shadow, tail at bottom-left/right)
function bubble(text, { size = 34, font = UI, weight = 700, color = PAL.ink, bg = '#fff', border = PAL.ink, tail = 'left', pad = 26, shadow = 6, r = 16 } = {}) {
  const L = layoutWords(text, { size, font, weight, color, maxW: 9999 }), w = L.w + pad * 2, h = L.h + pad * 1.2, c = mk(w + shadow + 40, h + shadow + 40), x = c.getContext('2d'), ox = 6, oy = 6;
  const shape = (dx, dy) => { rrect(ox + dx, oy + dy, w, h, r, x); const tx = tail === 'left' ? ox + dx + 30 : ox + dx + w - 30; x.moveTo(tx, oy + dy + h - 2); x.lineTo(tx + (tail === 'left' ? -14 : 14), oy + dy + h + 26); x.lineTo(tx + (tail === 'left' ? 18 : -18), oy + dy + h - 2); };
  x.fillStyle = border; shape(shadow, shadow); x.fill(); x.fillStyle = bg; x.strokeStyle = border; x.lineWidth = 3.5; shape(0, 0); x.fill(); x.stroke();
  for (const wd of L.words) x.drawImage(wd.img, ox + w / 2 + wd.x - wd.w / 2, oy + h / 2 + wd.y - wd.h / 2); return c;
}
// pill button canvas (CTA)
function pill(text, { size = 34, font = UI, weight = 800, color = '#fff', bg = '#05a0a2', ring = true, padX = 48, padY = 18 } = {}) {
  const L = layoutWords(text, { size, font, weight, color, maxW: 9999 }), w = L.w + padX * 2, h = L.h + padY * 2 - size * TS * .5, c = mk(w + 30, h + 30), x = c.getContext('2d');
  if (ring) { x.strokeStyle = bg; x.lineWidth = 3; rrect(3, 3, w + 24, h + 24, (h + 24) / 2, x); x.stroke(); } x.fillStyle = bg; rrect(15, 15, w, h, h / 2, x); x.fill();
  for (const wd of L.words) x.drawImage(wd.img, 15 + w / 2 + wd.x - wd.w / 2, 15 + h / 2 + wd.y - wd.h / 2); return c;
}
// arrow cursor (press 0…1 squashes it) + click ripple
function cursor(x, y, press = 0, { sc = 1.6, fill = '#fff', stroke = PAL.ink } = {}) { const s = sc * (1 - press * .15); g.save(); g.translate(x, y); g.scale(s, s); g.fillStyle = fill; g.strokeStyle = stroke; g.lineWidth = 2.2 / s * sc; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 30); g.lineTo(7, 23); g.lineTo(12, 34); g.lineTo(17, 32); g.lineTo(12, 21); g.lineTo(22, 21); g.closePath(); g.fill(); g.stroke(); g.restore(); }
function ripple(x, y, t, t0, { color = '#05a0a2', r1 = 70, dur = .5, width = 5 } = {}) { const k = tw(t, t0, t0 + dur, E.expoOut); if (k <= 0 || k >= 1) return; g.save(); g.globalAlpha = 1 - k; g.strokeStyle = color; g.lineWidth = width * (1 - k) + 1; g.beginPath(); g.arc(x, y, r1 * k, 0, 6.283); g.stroke(); g.restore(); }
// pixel sprite from string rows: sprite(['..aa..','.abba.'], {a:'#222', b:'#f8bb3e'}, 8)
function sprite(rows, pal, px = 8) { const c = mk(rows[0].length * px, rows.length * px), x = c.getContext('2d');
  rows.forEach((row, j) => [...row].forEach((ch, i) => { if (pal[ch]) { x.fillStyle = pal[ch]; x.fillRect(i * px, j * px, px, px); } })); return c; }
// phone mock canvas: content(x, w, h) draws the screen (in screen coords)
function phone(w = 360, h = 740, content = null, { body = '#111', bezel = 14, r = 54, screen = '#fff' } = {}) { const c = mk(w + 40, h + 40), x = c.getContext('2d');
  x.shadowColor = 'rgba(0,0,0,.25)'; x.shadowBlur = 30; x.shadowOffsetY = 14; x.fillStyle = body; rrect(20, 14, w, h, r, x); x.fill(); x.shadowColor = 'transparent';
  x.save(); rrect(20 + bezel, 14 + bezel, w - bezel * 2, h - bezel * 2, r - bezel, x); x.clip(); x.fillStyle = screen; x.fillRect(20, 14, w, h); x.translate(20 + bezel, 14 + bezel); if (content) content(x, w - bezel * 2, h - bezel * 2); x.restore();
  x.fillStyle = body; rrect(20 + w / 2 - 55, 14 + bezel + 10, 110, 30, 15, x); x.fill(); return c; }
// draw an image (cutout, sprite…) with crisp pixels
function drawCrisp(img, x, y, w, h) { const s = g.imageSmoothingEnabled; g.imageSmoothingEnabled = false; g.drawImage(img, x, y, w, h); g.imageSmoothingEnabled = s; }
// sticker drop: lands with spring + rotation settle, baked shadow (img should already be outline()/polaroid())
function sticker(img, x, y, t, t0, { rot = 0, sc = 1, springName = 'wobbly', from = -160, alpha = 1, t1 = null } = {}) {
  const k = spr(t, t0, springName); if (k <= .001) return; const ko = t1 ? tw(t, t1, t1 + .25, CURVE.md3Accel) : 0; if (ko >= 1) return;
  const s = sc * lerp(1.25, 1, k) * (1 - ko * .4), r = rot + (1 - k) * .35, yy = y + (1 - k) * from; g.save(); g.globalAlpha = clamp(k * 4) * alpha * (1 - ko); g.translate(x, yy); g.rotate(r); g.scale(s, s); g.drawImage(img, -img.width / 2, -img.height / 2); g.restore(); }
// seeded scatter of n points inside rect, keeping out of `avoid` rects ({x,y,w,h}) and apart by minD
function scatter(n, seed, { x = 60, y = 60, w = W - 120, h = H - 120, avoid = [], minD = 150 } = {}) { const r = rng(seed), pts = []; let guard = 0;
  while (pts.length < n && guard++ < 4000) { const p = [x + r() * w, y + r() * h]; if (avoid.some(a => p[0] > a.x && p[0] < a.x + a.w && p[1] > a.y && p[1] < a.y + a.h)) continue; if (pts.some(q => Math.hypot(q[0] - p[0], q[1] - p[1]) < minD)) continue; pts.push([...p, (r() - .5) * .5, r()]); }
  return pts; }

// ── 9 · TRANSITIONS (shot.tin = key; shot.tdur overrides duration) ───
// The incoming shot is already painted on the main canvas when draw() runs; drawOut() paints the outgoing shot.
const _inBuf = () => { const c = fxBuf('trIn'); const x = c.getContext('2d'); x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, W, H); x.drawImage(cv, 0, 0); return c; };
function renderOut(drawOut) { const c = fxBuf('trOut'), prev = g; g = c.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.filter = 'none'; g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, W, H); g.fillStyle = PAL.bg; g.fillRect(0, 0, W, H); drawOut(); g.setTransform(1, 0, 0, 1, 0, 0); g = prev; return c; }
// motion-blurred draw of a full frame: N equal-weight taps between offsets (dx0,dy0)→(dx1,dy1)
function smearDraw(img, dx0, dy0, dx1, dy1, n = 10, { sc = 1 } = {}) { g.save(); for (let i = 0; i < n; i++) { const u = n === 1 ? 0 : i / (n - 1); g.globalAlpha = 1 / (i + 1);
  const s = sc, w = W * s, h = H * s; g.drawImage(img, W / 2 - w / 2 + lerp(dx0, dx1, u), H / 2 - h / 2 + lerp(dy0, dy1, u), w, h); } g.restore(); }
const TRANS = {
  // whip pan: both frames rush sideways with heavy motion blur (RTL: content travels left→right, new shot enters from the left)
  whip: { dur: .32, draw(k, drawOut, o) { const dir = (o.shot.whipDir ?? FILM.whipDir ?? 1), IN = _inBuf(), OUT = renderOut(drawOut), e = CURVE.whip(k), v = Math.sin(k * Math.PI) * 260;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); const xo = dir * e * W, xi = xo - dir * W; smearDraw(OUT, xo - dir * v, 0, xo, 0, 9); smearDraw(IN, xi - dir * v, 0, xi, 0, 9); g.restore(); } },
  whipUp: { dur: .32, draw(k, drawOut) { const IN = _inBuf(), OUT = renderOut(drawOut), e = CURVE.whip(k), v = Math.sin(k * Math.PI) * 220;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); const yo = -e * H, yi = yo + H; smearDraw(OUT, 0, yo + v, 0, yo, 9); smearDraw(IN, 0, yi + v, 0, yi, 9); g.restore(); } },
  // zoom-through punch-in: outgoing scales up into a focus point with radial-ish blur; incoming settles from 0.8
  zoom: { dur: .36, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), [fx, fy] = o.shot.focus || [W / 2, H / 2];
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = PAL.bg; g.fillRect(0, 0, W, H);
    const eo = E.expoIn(clamp(k / .55)), so = 1 + eo * 3.5; if (k < .62) { g.save(); g.globalAlpha = 1 - clamp((k - .4) / .22); g.translate(fx, fy); g.scale(so, so); g.translate(-fx, -fy); g.filter = `blur(${(eo * 18).toFixed(1)}px)`; g.drawImage(OUT, 0, 0); g.restore(); }
    const ei = E.expoOut(clamp((k - .4) / .6)); if (k > .4) { const si = lerp(.75, 1, ei); g.save(); g.globalAlpha = clamp((k - .4) * 5); g.translate(W / 2, H / 2); g.scale(si, si); g.translate(-W / 2, -H / 2); g.filter = `blur(${((1 - ei) * 12).toFixed(1)}px)`; g.drawImage(IN, 0, 0); g.restore(); }
    g.restore(); } },
  // white (or colour) flash that hides a hard cut — 2–3 frames at peak (impacts, reveals)
  flash: { dur: .24, draw(k, drawOut, o) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); if (k < .3) { const OUT = renderOut(drawOut); g.drawImage(OUT, 0, 0); }
    const a = k < .3 ? k / .3 : 1 - (k - .3) / .7; g.fillStyle = o.shot.flashColor || '#fff'; g.globalAlpha = clamp(a); g.fillRect(0, 0, W, H); g.restore(); } },
  dip: { dur: .5, draw(k, drawOut, o) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); if (k < .5) { g.drawImage(renderOut(drawOut), 0, 0); } g.fillStyle = o.shot.dipColor || '#000'; g.globalAlpha = k < .5 ? E.cubicIn(k * 2) : 1 - E.cubicOut((k - .5) * 2); g.fillRect(0, 0, W, H); g.restore(); } },
  // iris: incoming opens in a circle from shot.focus with an accent ring
  iris: { dur: .5, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), [fx, fy] = o.shot.focus || [W / 2, H / 2], R = E.cubicInOut(k) * Math.hypot(W, H);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, 0, 0); g.beginPath(); g.arc(fx, fy, R, 0, 6.283); g.save(); g.clip(); g.drawImage(IN, 0, 0); g.restore();
    g.strokeStyle = o.shot.accent || PAL.gold; g.lineWidth = 14 * (1 - k) + 2; g.stroke(); g.restore(); } },
  // clock wipe: radial sweep (RTL = counter-clockwise)
  clock: { dur: .55, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), [fx, fy] = o.shot.focus || [W / 2, H / 2], e = E.cubicInOut(k), dir = FILM.rtl === false ? 1 : -1;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, 0, 0); g.beginPath(); g.moveTo(fx, fy); g.arc(fx, fy, 3000, -Math.PI / 2, -Math.PI / 2 + dir * e * 6.2832, dir < 0); g.closePath(); g.clip(); g.drawImage(IN, 0, 0); g.restore(); } },
  // blinds: n vertical slices close staggered (RTL order)
  blinds: { dur: .55, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), n = o.shot.slices || 12, sw = W / n;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, 0, 0); for (let i = 0; i < n; i++) { const j = n - 1 - i, e = E.cubicInOut(clamp((k - j / n * .45) / .55)); if (e <= 0) continue; const x = i * sw, w = sw * e;
      g.save(); g.beginPath(); g.rect(x + (sw - w) / 2, 0, w + .5, H); g.clip(); g.drawImage(IN, 0, 0); g.restore(); } g.restore(); } },
  // push: both frames move together (no blur) — calm sibling of whip
  push: { dur: .5, draw(k, drawOut, o) { const dir = (o.shot.whipDir ?? FILM.whipDir ?? 1), IN = _inBuf(), OUT = renderOut(drawOut), e = CURVE.camera(k);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, dir * e * W, 0); g.drawImage(IN, dir * e * W - dir * W, 0); g.restore(); } },
  // slide: incoming frame slides over the outgoing, which dims and recedes
  slide: { dur: .5, draw(k, drawOut, o) { const dir = (o.shot.whipDir ?? FILM.whipDir ?? 1), IN = _inBuf(), OUT = renderOut(drawOut), e = CURVE.md3Emph(k);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#000'; g.fillRect(0, 0, W, H); const s = 1 - e * .06; g.globalAlpha = 1 - e * .5; g.drawImage(OUT, W * (1 - s) / 2, H * (1 - s) / 2, W * s, H * s); g.globalAlpha = 1;
    g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 40; g.drawImage(IN, -dir * (1 - e) * W, 0); g.restore(); } },
  // barn doors: outgoing splits in half and opens
  barn: { dur: .55, draw(k, drawOut) { const OUT = renderOut(drawOut), e = E.cubicInOut(k) * W / 2; g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
    g.save(); g.beginPath(); g.rect(-e, 0, W / 2, H); g.clip(); g.drawImage(OUT, -e, 0); g.restore(); g.save(); g.beginPath(); g.rect(W / 2 + e, 0, W / 2, H); g.clip(); g.drawImage(OUT, e, 0); g.restore(); g.restore(); } },
  // luma/noise dissolve: organic burn-through using a seeded noise mask
  luma: { dur: .6, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), mw = 240, mh = 135, m = fxBuf('lumaM', mw, mh), mx = m.getContext('2d'), d = mx.createImageData(mw, mh);
    for (let j = 0; j < mh; j++) for (let i = 0; i < mw; i++) { const n = .5 + .5 * fbm(i * .03, j * .03 + (o.i || 0) * 7, 3), a = clamp((k * 1.4 - n) * 6 + .2); d.data[(j * mw + i) * 4 + 3] = a * 255; } mx.putImageData(d, 0, 0);
    const c = fxBuf('lumaC'), x = c.getContext('2d'); x.globalCompositeOperation = 'source-over'; x.clearRect(0, 0, W, H); x.drawImage(m, 0, 0, W, H); x.globalCompositeOperation = 'source-in'; x.drawImage(IN, 0, 0);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, 0, 0); g.drawImage(c, 0, 0); g.restore(); } },
  // glitch cut: 4–6 frames of slice offsets + RGB split, deterministic per frame
  glitch: { dur: .2, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), src = k < .5 ? OUT : IN, r = rng(Math.floor(k * 12) + 17 * (o.i || 1));
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(src, 0, 0); for (let s = 0; s < 9; s++) { const y = r() * H, h = 20 + r() * 120, dx = (r() - .5) * 180; g.drawImage(r() < .5 ? OUT : IN, 0, y, W, h, dx, y, W, h); }
    g.globalCompositeOperation = 'screen'; g.globalAlpha = .5; g.drawImage(tint(src, '#ff0040'), -14, 0); g.drawImage(tint(src, '#00e5ff'), 14, 0); g.restore(); } },
  // smear: outgoing stretches horizontally & blurs out, incoming un-stretches (liquid word morph feel)
  smear: { dur: .3, draw(k, drawOut) { const IN = _inBuf(), OUT = renderOut(drawOut); g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = PAL.bg; g.fillRect(0, 0, W, H);
    const a = E.quadIn(clamp(k / .6)), b = E.quadOut(clamp((k - .4) / .6));
    if (k < .6) { g.save(); g.globalAlpha = 1 - a; g.filter = `blur(${(a * 10).toFixed(1)}px)`; g.translate(W / 2, H / 2); g.scale(1 + a * 1.2, 1 - a * .2); g.drawImage(OUT, -W / 2 - a * 120, -H / 2); g.restore(); }
    if (k > .4) { g.save(); g.globalAlpha = b; g.filter = `blur(${((1 - b) * 10).toFixed(1)}px)`; g.translate(W / 2, H / 2); g.scale(1 + (1 - b) * 1.2, 1 - (1 - b) * .2); g.drawImage(IN, -W / 2 + (1 - b) * 120, -H / 2); g.restore(); }
    g.restore(); } },
  // graphic band: a diagonal accent-colour band sweeps across and carries the cut (VOX-style wipe)
  band: { dur: .5, draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), e = CURVE.camera(k), col = o.shot.accent || PAL.gold, sk = 260, x = lerp(W + sk + 200, -sk - 400, e), bw = 380;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(OUT, 0, 0); g.save(); g.beginPath(); g.moveTo(x + bw, 0); g.lineTo(W + 600, 0); g.lineTo(W + 600, H); g.lineTo(x + bw - sk, H); g.closePath(); g.clip(); g.drawImage(IN, 0, 0); g.restore();
    g.fillStyle = col; g.beginPath(); g.moveTo(x, 0); g.lineTo(x + bw, 0); g.lineTo(x + bw - sk, H); g.lineTo(x - sk, H); g.closePath(); g.fill(); g.restore(); } },
};
