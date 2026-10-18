// ════════════════════════════════════════════════════════════════════════════════════════════
//  motion-doc-studio · type.js — KINETIC TYPOGRAPHY LAYER (Arabic-first, word-level, motion pairs)
//  Load order: core.js → helpers.js → fx.js → type.js        Doc: library/kinetic_type_motion.md
//
//  KT.word(text, style)              pre-render ONE word/phrase (INITS only)          → W (word object)
//  KT.kashida(text, n, where)        Arabic tracking = tatweel insertion (never letter-spacing)
//  KT.stretch(text, style, maxN)     kashida variants for animated tracking (show({kashida}))
//  KT.show(W, t, spec)               draw a word with entrance / hold behaviour / exit → live box
//  KT.group(t, spec, fn)             parent transform (null object): flip, swing, drift a whole unit
//  Partners (motion pairs)           dot leader comet ring underline bar line hinge bubble window
//                                    orbit streak bokeh — each is a pure function of t
//  KT.F(n)                           n frames → seconds (offset shapes 2–6 frames from text)
//  KT.spots(aspect) / KT.place(i)    spatial choreography: each new word lands somewhere new
//  KT.post(t, o)                     clean black-stage finish (grain + soft vignette, no sepia)
//
//  RULES baked in (library/kinetic_type_motion.md): word-level only (Arabic shaping), exits faster than
//  entrances, shape & text never start/end on the same frame, one accent colour, hold ≥ 0.8 s for reading.
// ════════════════════════════════════════════════════════════════════════════════════════════
const KT = (() => {
  const FPS = (window.FILM && FILM.fps) || 30;
  const F = (n) => n / FPS;
  const INK = () => (FILM.kt && FILM.kt.ink) || '#f5f1ea';
  const ACC = () => (FILM.kt && FILM.kt.accent) || PAL.gold;
  const DIM = () => (FILM.kt && FILM.kt.dim) || '#6b6762';

  // ── springs & curves (tuned for type; values in library/kinetic_type_motion.md §4) ──────────────
  const SP = { card: [150, 19], snap: [320, 28], pop: [260, 15], soft: [60, 15], swing: [170, 9], glide: [90, 19] };
  const spr = (t, kind = 'card') => spring(t, ...(SP[kind] || SP.card));
  const eOut = (k) => 1 - Math.pow(1 - clamp(k), 3);
  const eIn = (k) => Math.pow(clamp(k), 3);
  const eExpo = (k) => (k = clamp(k), k >= 1 ? 1 : 1 - Math.pow(2, -10 * k));
  const eInOut = (k) => (k = clamp(k), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  const easeK = (t, t0, dur, curve = 'out') => ({ out: eOut, in: eIn, expo: eExpo, inout: eInOut, lin: clamp }[curve] || eOut)((t - t0) / dur);

  // ── Arabic kashida (tatweel) — the ONLY correct Arabic tracking ───────────────────────────────
  const DUAL = 'بتثجحخسشصضطظعغفقكلمنهيئیکگپچـ';                     // letters that join to the NEXT letter
  const AR = /[\u0621-\u064A\u066E-\u06D3\u06FA-\u06FF]/;
  const HAR = /[\u064B-\u065F\u0670\u06D6-\u06ED]/;                      // harakat / Quranic marks
  function joints(word) {                                                // legal tatweel positions (index after char i)
    const ch = [...word], out = [];
    for (let i = 0; i < ch.length; i++) {
      if (!DUAL.includes(ch[i])) continue;
      let j = i + 1; while (j < ch.length && HAR.test(ch[j])) j++;      // skip the letter's own harakat
      if (j >= ch.length || !AR.test(ch[j]) || HAR.test(ch[j])) continue;
      if (ch[i] === 'ل' && 'اأإآ'.includes(ch[j])) continue;            // never break the lam-alef ligature
      out.push(j);
    }
    return out;
  }
  function kashida(text, n = 2, where = 'last') {
    if (n <= 0) return text;
    return text.split(' ').map((w) => {
      const J = joints(w); if (!J.length) return w;
      const ch = [...w], add = {};
      if (where === 'all') J.forEach((j) => add[j] = n);
      else if (where === 'spread') for (let k = 0; k < n; k++) { const j = J[J.length - 1 - (k % J.length)]; add[j] = (add[j] || 0) + 1; }
      else add[J[J.length - 1]] = n;                                       // classic: before the final letter
      let s = ''; ch.forEach((c, i) => { if (add[i]) s += 'ـ'.repeat(add[i]); s += c; }); return s;
    }).join(' ');
  }

  // ── word objects (pre-rendered once; cached) ────────────────────────────────────────────────
  const cache = {};
  function word(text, o = {}) {
    const size = (o.size || 120) * (o.noScale ? 1 : TS), font = o.font || DISPLAY, weight = o.weight || 700, color = o.color || INK();
    const key = [text, size, font, weight, color, o.stroke || '', o.shadow || ''].join('|'); if (cache[key]) return cache[key];
    const m = mk(8, 8).getContext('2d'); m.font = `${weight} ${size}px ${font}`; m.direction = 'rtl';
    const mt = m.measureText(text), pad = Math.ceil(size * .45) + 24;
    const w = Math.ceil(mt.width), h = Math.ceil(size * (o.lh || 1.5));
    const c = mk(w + pad * 2, h + pad * 2), x = c.getContext('2d');
    x.font = m.font; x.direction = 'rtl'; x.textAlign = 'center'; x.textBaseline = 'middle';
    if (o.shadow) { x.shadowColor = o.shadow; x.shadowBlur = size * .25; }
    if (o.stroke) { x.lineJoin = 'round'; x.lineWidth = o.strokeW || size * .06; x.strokeStyle = o.stroke; x.strokeText(text, c.width / 2, c.height / 2 + (o.dy || 0) * size); }
    x.fillStyle = color; x.fillText(text, c.width / 2, c.height / 2 + (o.dy || 0) * size);
    return cache[key] = { img: c, text, w, h, pad, size, style: o };
  }
  const stretch = (text, o = {}, maxN = 4, where = 'last') => Array.from({ length: maxN + 1 }, (_, n) => word(kashida(text, n, where), o));
  const tinted = {};
  function tint(Wd, color) { const k = Wd.text + Wd.size + color + (Wd.style.font || ''); if (tinted[k]) return tinted[k];
    const c = mk(Wd.img.width, Wd.img.height), x = c.getContext('2d'); x.drawImage(Wd.img, 0, 0); x.globalCompositeOperation = 'source-in';
    x.fillStyle = color; x.fillRect(0, 0, c.width, c.height); return tinted[k] = Object.assign({}, Wd, { img: c }); }

  // ── entrances: k = spring/ease progress 0→1(+overshoot); S = mutable draw state ────────────
  // every entrance also gets an opacity ramp of `fade` frames (6–14) unless it is a mask/cut
  const IN = {
    rise:    (k, S, o) => { S.dy += (1 - k) * (o.dist ?? 60); },
    fall:    (k, S, o) => { S.dy -= (1 - k) * (o.dist ?? 60); },
    slide:   (k, S, o) => { const d = o.dist ?? 110, a = { right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1] }[o.dir || 'right']; S.dx += a[0] * (1 - k) * d; S.dy += a[1] * (1 - k) * d; },
    pop:     (k, S, o) => { const s = lerp(o.from ?? .8, 1, k); S.sx *= s; S.sy *= s; },        // spring 'pop' → 80→108→100
    grow:    (k, S, o) => { const s = Math.max(0, k); S.sx *= s; S.sy *= s; S.blur += (1 - clamp(k)) * 10; },   // from a point (leader dot)
    blur:    (k, S, o) => { S.blur += (1 - clamp(k)) * (o.blurPx ?? 16); const s = lerp(1.08, 1, k); S.sx *= s; S.sy *= s; },
    zoom:    (k, S, o) => { const s = lerp(o.from ?? 2.2, 1, k); S.sx *= s; S.sy *= s; S.blur += (1 - clamp(k)) * 8; },       // camera-through
    mask:    (k, S, o) => { S.clip = 'line'; S.dy += (1 - clamp(k)) * S.h * .9; S.noFade = true; },  // rises out of its own baseline
    drop:    (k, S, o) => { S.clip = 'line'; S.dy -= (1 - clamp(k)) * S.h * .9; S.noFade = true; },
    wipe:    (k, S, o) => { S.clip = 'wipe'; S.wipe = clamp(k); S.wdir = o.dir || 'rtl'; S.noFade = true; },  // RTL soft-edge reveal
    vwipe:   (k, S, o) => { S.clip = 'vwipe'; S.wipe = clamp(k); S.wdir = o.dir || 'down'; S.noFade = true; },
    flip:    (k, S, o) => { const a = (1 - clamp(k)) * Math.PI / 2; S.sx *= Math.max(.001, Math.cos(a)); S.skewY += Math.sin(a) * .18 * (o.side || 1); },  // 3D card (rotateY)
    flipX:   (k, S, o) => { const a = (1 - clamp(k)) * Math.PI / 2; S.sy *= Math.max(.001, Math.cos(a)); S.skewX += Math.sin(a) * .18; },              // rotateX
    spin:    (k, S, o) => { S.rot += (1 - k) * (o.angle ?? -Math.PI / 2); const s = lerp(.55, 1, k); S.sx *= s; S.sy *= s; },
    stand:   (k, S, o) => { S.rot += (1 - k) * (o.angle ?? -Math.PI / 2); S.pivot = o.pivot || 'right'; },      // lies down from vertical, hinged on its first letter
    swing:   (k, S, o) => { S.rot += (1 - k) * (o.angle ?? .5); S.pivot = 'top'; },                              // hangs on a line, damped (spring 'swing')
    unsquash:(k, S, o) => { S.sy *= Math.max(.02, k); S.sx *= lerp(1.5, 1, clamp(k)); S.noFade = true; },       // grows out of a horizontal line
    fromLine:(k, S, o) => { S.clip = 'half'; S.lineX = o.lineX ?? 0; S.dx += (1 - clamp(k)) * (o.side === 'left' ? 1 : -1) * (S.w + 30); S.noFade = true; },  // emerges from behind a line
    track:   (k, S, o) => { S.kashida = (o.kFrom ?? 4) + ((o.kTo ?? 0) - (o.kFrom ?? 4)) * clamp(k); },          // tracking-in via kashida
    cut:     (k, S, o) => { S.noFade = true; if (k > 0 && k < .25) { S.sx *= 1.1; S.sy *= 1.1; } },              // hard appear + 2-frame punch
  };
  // ── exits: k = 0→1 (accelerating); exits are 30–40 % shorter than entrances ────────────────
  const OUT = {
    fade:    (k, S) => { S.alpha *= 1 - k; },
    dim:     (k, S) => { S.dimK = Math.max(S.dimK, k); },                                                    // to grey, stays (then fade by caller)
    sink:    (k, S, o) => { S.dy += k * (o.outDist ?? 40); S.alpha *= 1 - k; },
    lift:    (k, S, o) => { S.dy -= k * (o.outDist ?? 50); S.alpha *= 1 - k; S.blur += k * 6; },
    push:    (k, S, o) => { const a = { right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1] }[o.outDir || 'left']; S.dx += a[0] * k * (o.outDist ?? 260); S.dy += a[1] * k * (o.outDist ?? 260); S.alpha *= 1 - eIn(k); S.blur += k * 10; },
    spin:    (k, S, o) => { S.rot += k * (o.outAngle ?? Math.PI * .55); const s = 1 - k * .7; S.sx *= s; S.sy *= s; S.alpha *= 1 - eIn(k); },
    squash:  (k, S) => { const a = clamp(k / .7), b = clamp((k - .7) / .3); S.sy *= Math.max(.015, 1 - a); S.sx *= lerp(1, 1.45, a) * (1 - b); S.alpha *= 1 - b * .5; },   // → a line
    flip:    (k, S, o) => { const a = clamp(k) * Math.PI / 2; S.sx *= Math.max(.001, Math.cos(a)); S.skewY -= Math.sin(a) * .18 * (o.side || 1); },
    wipe:    (k, S, o) => { S.clip = 'wipe'; S.wipe = 1 - clamp(k); S.wdir = (o.dir || 'rtl') === 'rtl' ? 'ltr-out' : 'rtl-out'; },
    mask:    (k, S) => { S.clip = 'line'; S.dy -= clamp(k) * S.h * .9; },
    blur:    (k, S) => { S.blur += k * 18; S.alpha *= 1 - k; const s = 1 + k * .08; S.sx *= s; S.sy *= s; },
    zoom:    (k, S) => { const s = 1 + eIn(k) * 2.5; S.sx *= s; S.sy *= s; S.alpha *= 1 - k; S.blur += k * 10; },
  };

  // ── show(): the one call per word ───────────────────────────────────────────────────────────
  // spec: {x, y, t0, t1?, in, out, spring, dur, fade, ax, ay, rot, sc, alpha, dist, dir, from, angle, side,
  //        echo:{n, lag, a}, drift:[px/s, px/s], wiggle:{deg, px, f}, breathe, dimAt, dimDur, chroma, glow,
  //        kashida: array-of-variants + {kFrom,kTo} via in:'track' or keys:[[t,n],…], color (tint), outDur}
  function state(Wd) { return { dx: 0, dy: 0, sx: 1, sy: 1, rot: 0, skewX: 0, skewY: 0, alpha: 1, blur: 0, clip: null, pivot: 'center', w: Wd.w, h: Wd.h, dimK: 0, kashida: null }; }
  function progressIn(t, s) {
    const lt = t - s.t0; if (lt < 0) return -1;
    if (s.dur) return easeK(t, s.t0, s.dur, s.curve || 'expo');
    return spr(lt, s.spring || ({ pop: 'pop', swing: 'swing', grow: 'pop', mask: 'card', cut: 'snap', stand: 'card', spin: 'card' }[s.in] || 'card'));
  }
  function compute(Wd, t, s, lagT = 0) {
    const S = state(Wd), tt = t - lagT;
    const kin = progressIn(tt, s); if (kin < 0 && s.in !== 'none') return null;
    if (s.in && s.in !== 'none') { (Array.isArray(s.in) ? s.in : [s.in]).forEach((n) => IN[n] && IN[n](Math.max(kin, 0), S, s)); }
    if (!S.noFade && s.in !== 'none') S.alpha *= clamp((tt - s.t0) / F(s.fade ?? 9));
    // hold behaviours
    const ht = tt - s.t0;
    if (s.drift) { S.dx += s.drift[0] * ht; S.dy += s.drift[1] * ht; }
    if (s.wiggle && typeof wiggle === 'function') { const w = s.wiggle; S.rot += wiggle(tt, w.f ?? .8, (w.deg ?? 1.5) * Math.PI / 180, (s.seed || 1) + 3); S.dx += wiggle(tt, w.f ?? .8, w.px ?? 2, (s.seed || 1) + 7); S.dy += wiggle(tt, (w.f ?? .8) * .9, w.px ?? 2, (s.seed || 1) + 11); }
    if (s.breathe) { const b = 1 + Math.sin(ht * 1.4 + (s.seed || 0)) * s.breathe; S.sx *= b; S.sy *= b; }
    if (s.keys) S.kashida = track(tt, s.keys, 90, 19);                       // animated kashida tracking (spring between variant indices)
    if (s.dimAt != null) S.dimK = Math.max(S.dimK, easeK(tt, s.dimAt, s.dimDur ?? .35, 'out'));
    if (s.t1 != null && tt > s.t1) {
      const ko = clamp((tt - s.t1) / (s.outDur ?? .32)); if (ko >= 1 && s.out !== 'dim') return null;
      const ke = (s.out === 'squash' || s.out === 'dim') ? eInOut(ko) : eIn(ko);
      (Array.isArray(s.out) ? s.out : [s.out || 'fade']).forEach((n) => OUT[n] && OUT[n](ke, S, s));
    }
    return S;
  }
  function pick(Wd, S) {                                                    // kashida variant + dim tint
    let W2 = Wd;
    if (Array.isArray(Wd)) { const n = clamp(Math.round(S.kashida ?? 0), 0, Wd.length - 1); W2 = Wd[n]; }
    return W2;
  }
  function paint(W2, S, s, alphaMul = 1, color = null) {
    const A = S.alpha * (s.alpha ?? 1) * alphaMul; if (A <= .003 || Math.abs(S.sx) < .002 || Math.abs(S.sy) < .002) return;
    const img = color ? tint(W2, color).img : W2.img, iw = img.width, ih = img.height;
    const ax = s.ax ?? .5, ay = s.ay ?? .5, cx = -iw * ax, cy = -ih * ay;
    g.save(); g.translate(s.x, s.y); if (s.rot) g.rotate(s.rot);
    if (S.clip) {                                                            // masks live in the word's final frame
      g.beginPath(); const L = -W2.w * ax - 10, T = -W2.h * ay - W2.h * .1, Wc = W2.w + 20, Hc = W2.h * 1.2;
      if (S.clip === 'line') g.rect(-iw * ax - 40, T - W2.h * .2, iw + 80, Hc + W2.h * .2);
      else if (S.clip === 'half') { const lx = S.lineX - s.x; if ((s.side || 'right') === 'left') g.rect(lx - 4000, -4000, 4000, 8000); else g.rect(lx, -4000, 4000, 8000); }
      else if (S.clip === 'wipe' || S.clip === 'vwipe') {
        const k = S.wipe, d = S.wdir;
        if (d === 'rtl') g.rect(L + Wc * (1 - k) - 40, -ih, Wc * k + 80, ih * 2);
        else if (d === 'ltr') g.rect(L - 40, -ih, Wc * k + 40, ih * 2);
        else if (d === 'ltr-out') g.rect(L - 40, -ih, Wc * k + 40, ih * 2);   // continue RTL travel: the right side leaves first
        else if (d === 'rtl-out') g.rect(L + Wc * (1 - k), -ih, Wc * k + 80, ih * 2);
        else if (d === 'down') g.rect(-iw, T, iw * 2, Hc * k);
        else g.rect(-iw, T + Hc * (1 - k), iw * 2, Hc * k);
      }
      g.clip();
    }
    g.translate(S.dx, S.dy);
    let px = 0, py = 0;                                                      // pivots for hinge moves
    if (S.pivot === 'right') px = W2.w / 2; else if (S.pivot === 'left') px = -W2.w / 2; else if (S.pivot === 'top') py = -W2.h * .55;
    g.translate(px, py); g.rotate(S.rot); g.transform(1, S.skewY, S.skewX, 1, 0, 0); g.scale(S.sx * (s.sc ?? 1), S.sy * (s.sc ?? 1)); g.translate(-px, -py);
    g.globalAlpha = clamp(A);
    if (S.blur > .4) g.filter = `blur(${S.blur.toFixed(1)}px)`;
    if (s.glow) { g.shadowColor = s.glowColor || INK(); g.shadowBlur = s.glow; }
    if (s.chroma && s.chromaK > 0) {                                         // RGB split hit that decays after landing
      const d = s.chroma * s.chromaK; g.globalCompositeOperation = 'lighter';
      g.drawImage(tint(W2, '#ff2a4a').img, cx - d, cy); g.drawImage(tint(W2, '#29e0ff').img, cx + d, cy); g.globalCompositeOperation = 'source-over';
    }
    g.drawImage(img, cx, cy);
    if (S.dimK > 0) { g.globalAlpha = clamp(A * S.dimK); g.drawImage(tint(W2, s.dimColor || DIM()).img, cx, cy); }
    g.restore();
  }
  function show(Wd, t, s) {
    const S = compute(Array.isArray(Wd) ? Wd[0] : Wd, t, s); if (!S) return null;
    const W2 = pick(Wd, S);
    if (s.chroma) s.chromaK = clamp(1 - (t - s.t0 - .05) / .25) * (t >= s.t0 ? 1 : 0);
    if (s.echo) {                                                            // ghosts trail the hero by lag frames
      const e = Object.assign({ n: 2, lag: 3, a: .35 }, s.echo);
      for (let i = e.n; i >= 1; i--) { const Se = compute(Array.isArray(Wd) ? Wd[0] : Wd, t, s, F(e.lag * i)); if (Se) paint(pick(Wd, Se), Se, s, e.a * Math.pow(.7, i - 1), e.color || null); }
    }
    paint(W2, S, s, 1, s.color || null);
    const sc = (s.sc ?? 1) * Math.abs(S.sx);
    return { x: s.x + S.dx, y: s.y + S.dy, w: W2.w * sc, h: W2.h * (s.sc ?? 1) * Math.abs(S.sy), alpha: S.alpha, rot: S.rot + (s.rot || 0),
      left: s.x + S.dx - W2.w * sc * (s.ax ?? .5), right: s.x + S.dx + W2.w * sc * (1 - (s.ax ?? .5)), top: s.y + S.dy - W2.h * .5, bottom: s.y + S.dy + W2.h * .5 };
  }

  // ── parent / null object: everything drawn in fn() moves as one unit ───────────────────────────
  // spec: {x, y, rot, sc, flip:{t0, t1, dur} (3D card flip between two states), swing:{t0, amp}, drift:[vx,vy], t0}
  function group(t, s, fn) {
    g.save(); g.translate(s.x || 0, s.y || 0);
    if (s.drift) g.translate(s.drift[0] * (t - (s.t0 || 0)), s.drift[1] * (t - (s.t0 || 0)));
    if (s.rot) g.rotate(s.rot);
    if (s.swing) { const lt = t - s.swing.t0; if (lt > 0) g.rotate(s.swing.amp * Math.exp(-lt * 3.2) * Math.sin(lt * 7.5)); }
    let face = 0;
    if (s.flip) { const k = eInOut((t - s.flip.t0) / (s.flip.dur || .5)); const a = k * Math.PI; face = k >= .5 ? 1 : 0;
      g.transform(1, Math.sin(a) * .12 * (k < .5 ? 1 : -1), 0, 1, 0, 0); g.scale(Math.max(.002, Math.abs(Math.cos(a))), 1); }
    if (s.sc) g.scale(s.sc, s.sc);
    try { fn(face); } finally { g.restore(); }
  }

  // ── motion-pair partners ───────────────────────────────────────────────────────────────────
  function dot(t, t0, x, y, r = 14, o = {}) {                               // pops on snap, optional exit shrink
    const k = spr(t - t0, o.spring || 'pop'); if (k <= 0) return 0;
    let s = k; if (o.t1 != null && t > o.t1) s *= 1 - eIn((t - o.t1) / (o.outDur || .22)); if (s <= .002) return 0;
    g.save(); g.globalAlpha = o.alpha ?? 1; g.fillStyle = o.color || INK(); g.beginPath(); g.arc(x, y, Math.max(0, r * s), 0, Math.PI * 2); g.fill(); g.restore(); return s;
  }
  // leader dot: appears → swells → collapses exactly while the word grows from its spot (hand-off)
  function leader(t, t0, x, y, o = {}) {
    const r = o.r || 16, hand = t0 + (o.lead ?? .4);                       // word should start at `hand` (returned)
    if (t < t0) return hand;
    const kin = spr(t - t0, 'pop'), sw = 1 + .5 * eOut((t - t0) / (o.lead ?? .4)), kout = eIn((t - hand) / .18);
    const s = Math.max(0, kin * sw * (1 - clamp(kout)));
    if (s > .002) { g.save(); g.fillStyle = o.color || INK(); g.beginPath(); g.arc(x, y, r * s, 0, Math.PI * 2); g.fill(); g.restore(); }
    return hand;
  }
  // comet: a dot leads a trim-path stroke along an ellipse arc; the tail catches up (V3 grammar)
  function comet(t, t0, cx, cy, rx, ry, o = {}) {
    const dur = o.dur || .7, a0 = o.a0 ?? -Math.PI / 2, sw = o.sweep ?? Math.PI * 1.25, dir = o.dir ?? -1;
    const head = eInOut((t - t0) / dur), tail = eInOut((t - t0 - (o.tailLag ?? dur * .45)) / dur);
    if (head <= 0 || tail >= 1) return;
    const A = (k) => a0 + dir * sw * k, P = (a) => [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry];
    g.save(); g.strokeStyle = o.color || INK(); g.lineWidth = o.width || 6; g.lineCap = 'round'; g.globalAlpha = o.alpha ?? 1; g.beginPath();
    const n = 48; for (let i = 0; i <= n; i++) { const a = A(lerp(tail, head, i / n)), p = P(a); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); } g.stroke();
    const hp = P(A(head)); g.fillStyle = o.color || INK(); g.beginPath(); g.arc(hp[0], hp[1], (o.head || 12) * (1 - tail * .6), 0, Math.PI * 2); g.fill(); g.restore();
  }
  // ring: circle draw-on (trim start) + optional draw-off continuing in the same direction (trim end)
  function ring(t, t0, cx, cy, r, o = {}) {
    const k = eInOut((t - t0) / (o.dur || .55)); if (k <= 0) return; const ko = o.t1 != null ? eInOut((t - o.t1) / (o.outDur || .4)) : 0; if (ko >= 1) return;
    const a0 = o.a0 ?? -Math.PI / 2, dir = o.dir ?? -1;
    g.save(); g.strokeStyle = o.color || ACC(); g.lineWidth = o.width || 5; g.lineCap = 'round'; g.beginPath();
    if (dir < 0) g.arc(cx, cy, r, a0 - Math.PI * 2 * k, a0 - Math.PI * 2 * ko, false); else g.arc(cx, cy, r, a0 + Math.PI * 2 * ko, a0 + Math.PI * 2 * k, false);
    g.stroke(); g.restore();
  }
  // underline: grows from the centre outwards; exits shrinking to one side (never the same frame as the word)
  function underline(t, t0, x, y, w, o = {}) {
    const k = easeK(t, t0, o.dur || .35, 'expo'); if (k <= 0) return; const ko = o.t1 != null ? easeK(t, o.t1, o.outDur || .3, 'in') : 0; if (ko >= 1) return;
    let a, b; if (o.from === 'right') { a = x + w / 2 - w * k; b = x + w / 2; } else if (o.from === 'left') { a = x - w / 2; b = x - w / 2 + w * k; } else { a = x - w / 2 * k; b = x + w / 2 * k; }
    if (ko > 0) a = lerp(a, b, ko);                                          // exits towards the reading end (left in RTL)
    g.save(); g.strokeStyle = o.color || ACC(); g.lineWidth = o.width || 6; g.lineCap = 'round'; g.beginPath(); g.moveTo(b, y); g.lineTo(a, y); g.stroke(); g.restore();
  }
  // highlight bar: wipes in behind the word, then wipes OUT in the same travel direction (bar passing behind)
  function bar(t, t0, x, y, w, h, o = {}) {
    const k = easeK(t, t0, o.dur || .3, 'expo'); if (k <= 0) return; const ko = o.t1 != null ? easeK(t, o.t1, o.outDur || .28, 'in') : 0; if (ko >= 1) return;
    const L = x - w / 2, R = x + w / 2; let a, b;
    if ((o.dir || 'rtl') === 'rtl') { b = R - w * ko; a = R - w * k; } else { a = L + w * ko; b = L + w * k; }
    g.save(); g.fillStyle = o.color || ACC(); g.globalAlpha = o.alpha ?? 1; g.beginPath();
    if (g.roundRect) g.roundRect(Math.min(a, b), y - h / 2, Math.abs(b - a), h, o.r ?? h * .12); else g.rect(Math.min(a, b), y - h / 2, Math.abs(b - a), h);
    g.fill(); g.restore();
  }
  // straight line draw-on (connector, hanger, divider) with optional retract
  function line2(t, t0, x1, y1, x2, y2, o = {}) {
    const k = easeK(t, t0, o.dur || .3, 'expo'); if (k <= 0) return; const ko = o.t1 != null ? easeK(t, o.t1, o.outDur || .25, 'in') : 0; if (ko >= 1) return;
    g.save(); g.strokeStyle = o.color || INK(); g.lineWidth = o.width || 3; g.lineCap = 'round'; g.globalAlpha = o.alpha ?? 1; g.beginPath();
    g.moveTo(lerp(x1, x2, ko), lerp(y1, y2, ko)); g.lineTo(lerp(x1, x2, k), lerp(y1, y2, k)); g.stroke(); g.restore();
  }
  // hinge: an accent line that pivots (track keys of [time, angleRad]) — words slide out from behind it
  function hinge(t, t0, x, y, len, o = {}) {
    const k = easeK(t, t0, o.dur || .3, 'expo'); if (k <= 0) return; const ko = o.t1 != null ? easeK(t, o.t1, o.outDur || .3, 'in') : 0; if (ko >= 1) return;
    const a = o.keys ? track(t, o.keys, 120, 16) : (o.angle || 0);
    g.save(); g.translate(x, y); g.rotate(a); g.strokeStyle = o.color || ACC(); g.lineWidth = o.width || 5; g.lineCap = 'round';
    g.beginPath(); g.moveTo(0, -len / 2 * k * (1 - ko)); g.lineTo(0, len / 2 * k * (1 - ko)); g.stroke(); g.restore(); return a;
  }
  // bubble: filled disc behind an accent word (scale pop → hold → shrink/drift away)
  function bubble(t, t0, x, y, r, o = {}) {
    const k = spr(t - t0, o.spring || 'pop'); if (k <= 0) return; let s = k, dx = 0;
    if (o.t1 != null && t > o.t1) { const ko = eIn((t - o.t1) / (o.outDur || .3)); s *= 1 - ko; dx = (o.exitDx ?? -60) * ko; }
    if (s <= .002) return; g.save(); g.globalAlpha = o.alpha ?? 1; g.fillStyle = o.color || ACC(); g.beginPath(); g.arc(x + dx, y, Math.max(0, r * s), 0, Math.PI * 2); g.fill(); g.restore();
  }
  // window: translucent panel; words drawn inside clip(win) pass "through" it
  function panel(t, t0, x, y, w, h, o = {}) {
    const k = easeK(t, t0, o.dur || .35, 'expo'); if (k <= 0) return null; const ko = o.t1 != null ? easeK(t, o.t1, o.outDur || .3, 'in') : 0; if (ko >= 1) return null;
    const hh = h * k * (1 - ko);
    g.save(); g.fillStyle = o.color || 'rgba(255,255,255,.14)'; g.fillRect(x - w / 2, y - hh / 2, w, hh);
    if (o.stroke) { g.strokeStyle = o.stroke; g.lineWidth = 2; g.strokeRect(x - w / 2, y - hh / 2, w, hh); } g.restore();
    return { x, y, w, h: hh };
  }
  function clipTo(box, fn) { if (!box) return; g.save(); g.beginPath(); g.rect(box.x - box.w / 2, box.y - box.h / 2, box.w, box.h); g.clip(); try { fn(); } finally { g.restore(); } }
  // orbit: n short accent strokes rotating around a word (keeps a held word alive)
  function orbit(t, t0, cx, cy, r, o = {}) {
    const k = easeK(t, t0, o.dur || .4, 'out'); if (k <= 0) return; const ko = o.t1 != null ? easeK(t, o.t1, .3, 'in') : 0; if (ko >= 1) return;
    const n = o.n || 3, len = o.len || .55, sp = o.speed || 1.4;
    g.save(); g.strokeStyle = o.color || ACC(); g.lineWidth = o.width || 4; g.lineCap = 'round'; g.globalAlpha = (o.alpha ?? 1) * (1 - ko);
    for (let i = 0; i < n; i++) { const a = (t - t0) * sp + i * Math.PI * 2 / n; g.beginPath(); g.ellipse(cx, cy, r * (1 + .08 * i), r * (o.squash || .62), o.tilt || -.25, a, a + len * k); g.stroke(); }
    g.restore();
  }
  // light streak wipe: a hot diagonal band crossing the frame (additive) — use as a transition accent
  function streak(t, t0, o = {}) {
    const k = (t - t0) / (o.dur || .35); if (k <= 0 || k >= 1) return; const x = lerp(-W * .3, W * 1.3, eInOut(k)), wd = o.width || W * .12;
    g.save(); g.globalCompositeOperation = 'lighter'; g.translate(x, H / 2); g.rotate(o.angle ?? .35);
    const gr = g.createLinearGradient(-wd, 0, wd, 0); const c = o.color || '255,236,210';
    gr.addColorStop(0, `rgba(${c},0)`); gr.addColorStop(.5, `rgba(${c},${o.alpha ?? .55})`); gr.addColorStop(1, `rgba(${c},0)`);
    g.fillStyle = gr; g.fillRect(-wd, -H, wd * 2, H * 2); g.restore();
  }
  // foreground bokeh: soft discs drifting slowly (seeded, deterministic)
  function bokeh(t, o = {}) {
    const r = rng(o.seed || 77), n = o.n || 7;
    g.save(); g.globalCompositeOperation = 'lighter';
    for (let i = 0; i < n; i++) {
      const bx = r() * W, by = r() * H, rad = (o.size || 60) * (.5 + r()), vx = (r() - .5) * 18, vy = -6 - r() * 10, ph = r() * 6;
      const x = ((bx + vx * t) % (W + 200) + W + 200) % (W + 200) - 100, y = ((by + vy * t) % (H + 200) + H + 200) % (H + 200) - 100;
      const a = (o.alpha ?? .12) * (.6 + .4 * Math.sin(t * .8 + ph));
      const gr = g.createRadialGradient(x, y, 0, x, y, rad); gr.addColorStop(0, `rgba(${o.color || '255,220,190'},${a})`); gr.addColorStop(.7, `rgba(${o.color || '255,220,190'},${a * .6})`); gr.addColorStop(1, `rgba(${o.color || '255,220,190'},0)`);
      g.fillStyle = gr; g.beginPath(); g.arc(x, y, rad, 0, Math.PI * 2); g.fill();
    }
    g.restore();
  }

  // ── spatial choreography: anchor spots per aspect; never land twice in a row on the same spot ──────
  function spots(aspect) {
    const a = aspect || (W > H * 1.2 ? '16:9' : H > W * 1.2 ? '9:16' : '1:1');
    const P = { '16:9': [[.62, .36], [.38, .58], [.66, .66], [.32, .34], [.5, .5], [.72, .5], [.28, .66]],
      '9:16': [[.5, .3], [.42, .46], [.58, .6], [.5, .72], [.36, .38], [.62, .42], [.5, .55]],
      '1:1': [[.6, .3], [.4, .5], [.62, .66], [.36, .32], [.5, .5], [.66, .48], [.34, .68]] }[a] || [[.5, .5]];
    return P.map(([x, y]) => [x * W, y * H]);
  }
  const place = (i, aspect) => { const P = spots(aspect); return P[i % P.length]; };

  // ── finishing for black-stage kinetic films (no sepia) ────────────────────────────────────────
  function post(t, o = {}) {
    if (typeof fxGrain === 'function') fxGrain(t, o.grain ?? .045, 'overlay');
    if (typeof fxVignette === 'function') fxVignette(o.vignette ?? .35, { inner: .5 });
  }
  function stage(color) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = color || (FILM.kt && FILM.kt.bg) || '#050505'; g.fillRect(0, 0, W, H); g.restore(); }

  // ── timing helpers ─────────────────────────────────────────────────────────────────────────
  // lyric/VO words [{w,s,e}] → per-word {t0, t1} with reading-time floor and exit overlap
  function timeline(words, o = {}) {
    const minHold = o.minHold ?? .8, overlap = o.overlap ?? F(4);
    return words.map((wd, i) => { const nx = words[i + 1]; const t1 = nx ? Math.max(wd.s + minHold, nx.s - overlap) : wd.e + (o.tail ?? .6); return Object.assign({}, wd, { t0: wd.s, t1 }); });
  }

  return { F, SP, spr, eOut, eIn, eExpo, eInOut, easeK, joints, kashida, word, stretch, tint, IN, OUT, show, group,
    dot, leader, comet, ring, underline, bar, line: line2, hinge, bubble, panel, clipTo, orbit, streak, bokeh,
    spots, place, post, stage, timeline, INK, ACC, DIM };
})();
window.KT = KT;
