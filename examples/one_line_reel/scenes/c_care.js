// ═══ C · 37.30–52.56 · measured steps → a heart → a home around it → growth you can touch → a new day ═══
// → THE REVEAL: the camera pulls all the way back — the whole film was one path. A light runs along it (HERO «بل رحلة»).
(() => {
  const T = {};
  const D7 = { font: DISPLAY, weight: 700 }, U7 = { font: UI, weight: 700 };
  const IN = [0, -11600];
  const NODES = Array.from({ length: 5 }, (_, i) => [lerp(-320, 320, i / 4), lerp(-12560, -12940, i / 4) + Math.sin(i * 1.3) * 10]), NT = [37.78, 38.18, 38.58, 38.98, 39.30];
  const HT = [0, -14000], HS = 8.2;                                            // heart centre / scale
  const HO = { l: -250, r: 250, b: -13830, w: -14160, p: -14400 };              // house
  const CB = -15100, CH = [[-300, -15100], [-175, -15215], [-60, -15160], [70, -15335], [180, -15270], [320, -15475]];
  const SUN = [0, -16250], SR = 150;
  const REV = { x: 2362, y: -8110, z: .1016 };
  INITS.push(async () => {
    T.nml = KT.word('نعمل', { ...U7, size: 62, color: LP.mint });
    T.khw = KT.word('بخطوات مدروسة', { ...D7, size: 118, color: LP.cream });
    T.aht = KT.word('واهتمام', { ...U7, size: 62, color: LP.mint });
    T.hqq = KT.word('حقيقي', { ...D7, size: 150, color: LP.gold });
    T.msn = KT.word('لمساندة', { ...U7, size: 62, color: LP.mint });
    T.atf = KT.word('الأطفال والأسر', { ...D7, size: 112, color: LP.cream });
    T.thq = KT.word('وتحقيق', { ...U7, size: 62, color: LP.mint });
    T.ttw = KT.word('تطور ملموس', { ...D7, size: 124, color: LP.cream });
    T.ynk = KT.word('ينعكس على', { ...U7, size: 62, color: LP.mint });
    T.hyt = KT.word('حياتهم اليومية', { ...D7, size: 128, color: LP.gold });
    T.lsh = KT.word('لأن الشفاء', { ...U7, size: 62, color: LP.mint });
    T.lys = KT.word('ليس مجرد علاج', { ...D7, size: 86, color: LP.cream });
    T.bal = KT.word('بل رحلة', { ...D7, size: 196, color: LP.gold });
    T.nhw = KT.word('نحو حياة أفضل', { ...D7, size: 86, color: LP.cream });
  });

  WORLD.build.push(() => {
    // measured steps: equal intervals, a small loop at every node
    NODES.forEach(([x, y], i) => {
      const loop = SHAPES.circle(x, y, 17, Math.PI, 1, 40, -1);
      LINE.add([loop], i === 0 ? { c1: [IN[0] - 520, IN[1] - 200], c2: [x - 160, y + 120], dIn: [0, -1] } : { join: 'line' }); LINE.mark('n' + i);
      if (i === 0) LINE.M.n0A = LINE.S - 107;
    });
    LINE.key(35.95, 'infB'); LINE.key(37.66, 'n0A', 'io');
    NT.forEach((t, i) => LINE.key(t, 'n' + i, i ? 'io' : 'o'));
    // heart (one stroke from its tip) — then a home is drawn around it
    const heart = []; for (let i = 0; i <= 260; i++) { const u = Math.PI + i / 260 * Math.PI * 2;
      heart.push([HT[0] + HS * 16 * Math.sin(u) ** 3, HT[1] - HS * (13 * Math.cos(u) - 5 * Math.cos(2 * u) - 2 * Math.cos(3 * u) - Math.cos(4 * u)) - 20]); }
    LINE.add([heart], { dIn: [-.6, -1], c1: [520, -13100], c2: [HT[0] + 200, HT[1] + 330] }); LINE.mark0('hA'); LINE.mark('hB');
    LINE.key(39.40, 'hA', 'io'); LINE.key(40.02, 'hB', 'io');
    const house = densify([[HO.l, HO.b], [HO.l, HO.w], [0, HO.p], [HO.r, HO.w], [HO.r, HO.b], [HO.l, HO.b]], 4);
    LINE.add([house], { dIn: [0, -1], c1: [HT[0] - 240, HT[1] + 300], c2: [HO.l - 60, HO.b + 160] }); LINE.mark0('hoA'); LINE.mark('hoB');
    LINE.key(40.80, 'hB'); LINE.key(41.05, 'hoA', 'io'); LINE.key(42.00, 'hoB', 'io');
    T.heart = heart;
    // growth you can touch: a base line, then a rising line with an arrow
    LINE.add([densify([[-340, CB], [340, CB]], 4)], { dIn: [1, 0], c1: [HO.l - 300, HO.b - 400], c2: [-560, CB + 40] }); LINE.mark0('cbA'); LINE.mark('cbB');
    LINE.add([densify(CH, 4)], { join: 'lift' }); LINE.mark('chB');
    const e = CH[CH.length - 1];
    LINE.add([densify([e, [e[0] - 78, e[1] + 14]], 3), densify([e, [e[0] - 22, e[1] + 76]], 3)], { join: 'line' }); LINE.mark('arB');
    LINE.key(42.10, 'hoB'); LINE.key(42.70, 'cbA', 'io'); LINE.key(42.98, 'cbB', 'io'); LINE.key(43.85, 'chB', 'io'); LINE.key(44.05, 'arB', 'o');
    // a new day: horizon (R→L), the sun's arc, its rays
    LINE.add([densify([[380, SUN[1]], [-380, SUN[1]]], 4)], { dIn: [-1, 0], c1: [e[0] + 140, e[1] - 160], c2: [560, SUN[1] + 60] }); LINE.mark0('hzA'); LINE.mark('hzB');
    const arc = SHAPES.circle(SUN[0], SUN[1], SR, Math.PI, .5, 90, 1);
    LINE.add([arc], { join: 'lift' }); LINE.mark('arcB');
    const rays = []; for (let k = 0; k < 7; k++) { const a = Math.PI + .28 + k * (Math.PI - .56) / 6; rays.push(densify([[SUN[0] + Math.cos(a) * (SR + 38), SUN[1] + Math.sin(a) * (SR + 38)], [SUN[0] + Math.cos(a) * (SR + 98), SUN[1] + Math.sin(a) * (SR + 98)]], 3)); }
    LINE.add(rays, { join: 'lift' }); LINE.mark('rayB');
    LINE.key(44.10, 'arB'); LINE.key(44.45, 'hzA', 'io'); LINE.key(44.78, 'hzB', 'io'); LINE.key(45.30, 'arcB', 'io'); LINE.key(45.80, 'rayB', 'io');
    T.arc = arc;
  });

  // ── camera ──
  LCAM.key(37.75, 0, -12780, .95, .01);
  LCAM.key(39.25, 0, -12800, .975, .01, true);
  LCAM.key(39.78, 0, -14125, .95, -.01);
  LCAM.key(42.20, 0, -14145, .975, -.01, true);
  LCAM.key(42.75, 0, -15400, .95, .01);
  LCAM.key(44.20, 0, -15415, .975, .01, true);
  LCAM.key(44.72, 0, -16400, .95, 0);
  LCAM.key(46.30, 0, -16420, .985, 0, true);
  LCAM.key(47.70, REV.x, REV.y, REV.z, 0);
  LCAM.key(52.05, REV.x - 60, REV.y - 120, REV.z * 1.04, 0, true);

  // ── sound ──
  cue.appear('heart', 40.04, { sound: 'chime/fs-185822-single-chime-1' });
  cue.move('reveal', when.ease(46.30, 47.70), { sound: 'whoosh/fs-60002-swoosh-15-windy-1' });
  cue.hero('rihla', 50.20, { on: 'appear', sound: 'thump/fs-133282-thump-on-carpet-2+tap/fs-369710-wood-knock' });

  INITS.push(async () => {
    NODES.forEach(([x, y], i) => BLOOM.add({ t0: NT[i] - .04, dur: .2, cx: x, cy: y, r: 22, color: LP.gold, alpha: 1, shape: (c) => c.arc(x, y, 15, 0, 7) }));
    BLOOM.add({ t0: 40.04, dur: .32, cx: HT[0], cy: HT[1] + 60, r: 260, color: LP.gold, alpha: .95, shape: polyShape([T.heart]) });
    BLOOM.add({ t0: 43.84, dur: .4, cx: -300, cy: CB, r: 760, color: LP.mint, alpha: .2, shape: polyShape([[...CH, [320, CB], [-300, CB]]]) });
    BLOOM.add({ t0: 45.82, dur: .4, cx: SUN[0], cy: SUN[1], r: SR, color: LP.gold, alpha: .95, shape: polyShape([[...T.arc, [SUN[0] - SR, SUN[1]]]]) });
  });
  window.FLASH = (window.FLASH || []).concat([50.19]);
  // the journey lights up end to end while «بل رحلة نحو حياة أفضل»
  (WORLD.lineFx = WORLD.lineFx || []).push((t, px, c) => {
    const k = (t - 49.95) / 2.25; if (k <= 0 || k >= 1.08) return; const end = LINE.M.rayB, hd = end * KT.eInOut(Math.min(1, k)), band = end * .16;
    LINE.stroke(Math.max(0, hd - band), hd, { color: '#fff1c8', px: px * 1.6, alpha: k > 1 ? 1 - (k - 1) / .08 : 1, z: c.z, under: .2, core: 1 });
    if (k < 1) { const p = LINE.at(hd); g.save(); g.fillStyle = '#fff8e4'; g.beginPath(); g.arc(p.x, p.y, 13 / c.z, 0, 7); g.fill(); g.globalAlpha = .3; g.beginPath(); g.arc(p.x, p.y, 40 / c.z, 0, 7); g.fill(); g.restore(); }
  });
  window.DRY = (t) => lerp(.92, 1, clamp((t - 46.6) / .8) * (1 - clamp((t - 52.2) / .5)));

  WORLD.over.push((t) => {
    wtext(T.nml, t, { wx: 0, wy: -13180, t0: 37.40, in: 'rise', dist: 26 });
    wtext(T.khw, t, { wx: 0, wy: -13060, t0: 38.14, in: 'mask' });
    wtext(T.aht, t, { wx: 0, wy: -14650, t0: 39.50, in: 'rise', dist: 26 });
    wtext(T.hqq, t, { wx: 0, wy: -14525, t0: 40.04, in: 'mask' });
    wtext(T.msn, t, { wx: 0, wy: -13715, t0: 40.84, in: 'rise', dist: 26 });
    wtext(T.atf, t, { wx: 0, wy: -13600, t0: 41.60, in: 'mask' });
    wtext(T.thq, t, { wx: 0, wy: -15735, t0: 42.68, in: 'rise', dist: 26 });
    wtext(T.ttw, t, { wx: 0, wy: -15615, t0: 43.36, in: 'mask' });
    wtext(T.ynk, t, { wx: 0, wy: -16765, t0: 44.42, in: 'rise', dist: 26 });
    wtext(T.hyt, t, { wx: 0, wy: -16645, t0: 45.24, in: 'mask' });
  });
  // the reveal: an editorial column on the right, the whole path on the left
  WORLD.screen.push((t) => {
    if (t < 46.4 || t > 52.6) return;
    const X = 1000, out = { t1: 52.08, out: 'lift', outDur: .26 };
    if (A.wmark && t >= 46.75) { const k = KT.spr(t - 46.75, 'card'), ko = clamp((t - 52.08) / .26), ww = 520, hh = ww * A.wmark.height / A.wmark.width;
      g.save(); g.globalAlpha = clamp(k * 2) * (1 - ko); g.drawImage(A.wmark, X - ww, 470 - hh / 2 + (1 - Math.min(1, k)) * 40 - ko * 50, ww, hh); g.restore(); }
    KT.show(T.lsh, t, { x: X, y: 660, ax: 1, t0: 47.78, in: 'rise', dist: 26, ...out });
    const r = KT.show(T.lys, t, { x: X, y: 790, ax: 1, t0: 48.84, in: 'mask', dimAt: 50.05, dimDur: .3, ...out });
    // strike through «مجرد علاج»: it is more than a treatment
    if (r && t > 49.92) { const k = KT.eOut((t - 49.92) / .3), x1 = r.right - T.lys.w * .36, x0 = r.left;
      g.save(); g.strokeStyle = LP.gold; g.lineWidth = 7; g.lineCap = 'round'; g.globalAlpha = r.alpha; g.beginPath(); g.moveTo(x1, r.y + 4); g.lineTo(lerp(x1, x0, k), r.y + 4); g.stroke(); g.restore(); }
    KT.show(T.bal, t, { x: X, y: 1000, ax: 1, t0: 50.19, in: 'cut', ...out });
    KT.show(T.nhw, t, { x: X, y: 1190, ax: 1, t0: 51.04, in: 'mask', ...out });
  });
})();
