// ═══ B · 16.84–37.30 · every person has a seed → the seed sprouts → the services bloom along the stem
//     → «إضافة إلى برامج…» an infinity loop that fills with the SPECTRUM on «طيف التوحد» ═══
(() => {
  const T = {};
  const D7 = { font: DISPLAY, weight: 700 }, U7 = { font: UI, weight: 700 };
  const F = A_OPEN.F;                                        // fingerprint centre (A's world end)
  const SD = [0, -6500];                                     // the seed
  const ST = Array.from({ length: 7 }, (_, i) => [(i % 2 ? -1 : 1) * 280, -8420 - 430 * i]);
  const IC = ['hand', 'puzzle', 'baby', 'speech', 'book-open', 'brain', 'trending-up'];
  const LBL = [['العلاج', 'الوظيفي'], ['تنمية', 'المهارات'], ['التدخّل', 'المبكر'], ['علاج', 'النطق واللغة'],
    ['صعوبات', 'التعلّم'], ['العلاج', 'النفسي السلوكي'], ['التطوّر', 'الشامل السلوكي']];
  const TI = [24.08, 25.14, 26.38, 27.54, 29.14, 30.28, 32.06];
  const IN = [0, -11600], IA = 330;                          // the infinity of the spectrum
  INITS.push(async () => {
    T.lkl = KT.word('ولكِل شخص', { ...D7, size: 96, color: LP.cream });
    T.qdr = KT.word('قُدراته', { ...D7, size: 150, color: LP.gold });
    T.sth = KT.word('التي تستحق أن', { ...U7, size: 58, color: LP.mint });
    T.tkt = KT.word('تُكتشَف', { ...D7, size: 96, color: LP.cream });
    T.tnm = KT.word('وتُنمّى', { ...D7, size: 96, color: LP.gold });
    T.nqd = KT.word('نقدّم مجموعة من', { ...U7, size: 60, color: LP.mint });
    T.khd = KT.word('الخدمات المتخصّصة', { ...D7, size: 96, color: LP.cream });
    T.lbl = LBL.map(([a, b]) => [KT.word(a, { ...U7, size: 54, color: LP.mint }), KT.word(b, { ...D7, size: 88, color: LP.cream })]);
    T.prg = KT.word('برامج متخصّصة لإضطراب', { ...U7, size: 58, color: LP.mint });
    T.tyf = KT.word('طيف التوحّد', { ...D7, size: 150, color: LP.gold });
  });

  WORLD.build.push(() => {
    // from the fingerprint's core, the line runs down the left wall to a small ring: the SEED
    const aS = -Math.PI * .75;                                 // ring starts at −135°
    LINE.add([SHAPES.circle(SD[0], SD[1], 100, aS, 1, 130, -1)], { c1: [-540, F[1] - 380], c2: [-660, SD[1] + 480] });
    LINE.mark0('seedA'); LINE.mark('seedB');
    // the sprout: one stem + two leaves (pen hops)
    const stem = densify([[0, SD[1] - 100], [36, SD[1] - 240], [-22, SD[1] - 380], [6, SD[1] - 470]], 4);
    const l1 = LINE.sample(leafD(165, 30), 1.6).map((sp) => LINE.tf(sp, { x: 32, y: SD[1] - 246, rot: 2.35 }));
    const l2 = LINE.sample(leafD(180, 32), 1.6).map((sp) => LINE.tf(sp, { x: 2, y: SD[1] - 400, rot: -.95 }));
    LINE.add([stem, ...l1, ...l2], { dIn: [0, -1], k1: .3, k2: .35 });
    LINE.mark('stemB');
    // seven stations along the rising trail
    ST.forEach(([x, y], i) => {
      const prev = i === 0 ? [6, SD[1] - 470] : ST[i - 1];
      const a0 = Math.atan2(prev[1] - y, prev[0] - x);         // ring starts facing where we come from
      LINE.add([SHAPES.circle(x, y, 105, a0, 1, 110, -1)], i === 0 ? { c1: [-640, SD[1] - 900], c2: [-700, ST[0][1] + 420] } : { dIn: [Math.cos(a0 + 1), Math.sin(a0 + 1)] });
      LINE.mark0('r' + i + 'A'); LINE.mark('r' + i + 'B');
      LINE.icon(IC[i], x, y, 128); LINE.mark('i' + i + 'B');
    });
    // …then the line closes into an INFINITY: the spectrum has no end
    const inf = []; for (let q = 0; q <= 300; q++) { const u = Math.PI - q / 300 * Math.PI * 2, d = 1 + Math.sin(u) ** 2;
      inf.push([IN[0] + IA * Math.cos(u) / d, IN[1] + IA * 1.45 * Math.sin(u) * Math.cos(u) / d]); }
    LINE.add([inf], { dIn: [0, -1], c1: [IN[0] - 900, IN[1] + 700], c2: [IN[0] - IA - 140, IN[1] - 120] });
    LINE.mark0('infA'); LINE.mark('infB');
    T.inf = inf;
    // ── pen keys ──
    LINE.key(16.10, 'fpB');
    LINE.key(17.60, 'seedA', 'io'); LINE.key(18.10, 'seedB', 'io'); LINE.key(18.18, 'seedB');
    LINE.key(19.95, 'stemB', 'io');
    LINE.key(23.30, 'r0A', 'io');
    TI.forEach((ti, i) => {
      if (i) LINE.key(ti - .72, 'r' + i + 'A', 'io');
      LINE.key(ti - .28, 'r' + i + 'B', 'io'); LINE.key(ti + .40, 'i' + i + 'B', 'io');
    });
    LINE.key(33.05, 'i6B'); LINE.key(34.30, 'infA', 'io'); LINE.key(35.95, 'infB', 'io');
  });

  // ── camera: sink to the seed, breathe with the sprout, then climb station by station ──
  LCAM.key(16.84, 0, F[1] - 40, .99, .02);
  LCAM.key(18.20, 0, -6770, .95, 0);
  LCAM.key(20.30, 0, -6800, .965, 0, true);
  LCAM.key(21.60, 0, -7930, .90, -.008);
  LCAM.key(23.60, 50, -7950, .93, -.008, true);
  TI.forEach((ti, i) => { const [x, y] = ST[i];
    LCAM.key(ti - .55, x * .30, y + 520, .97, (i % 2 ? -.012 : .012));
    LCAM.key(ti + .30, x * .22, y + 465, .985, (i % 2 ? -.012 : .012), true); });
  LCAM.key(33.50, 0, -11420, .95, .008);
  LCAM.key(35.95, 0, -11680, .955, .008, true);
  LCAM.key(37.30, 0, -11710, .97, .008);

  // ── sound ──
  TI.forEach((ti, i) => { if (i === 0 || i === 2 || i === 6) cue.appear('svc' + i, ti - .26, { sound: i === 0 ? 'pop/fs-392624-champagne-cork-1' : 'tap/fs-339364-drop06-wav', pan: (i % 2 ? .3 : -.3) }); });
  cue.move('flyB', when.ease(21.00, 22.80), { sound: 'whoosh/fs-60002-swoosh-15-windy-1' });
  cue.appear('tawahhud', 36.52, { sound: 'thump/fs-133282-thump-on-carpet-2+chime/fs-127149-ding-wav-1' });

  INITS.push(async () => {
    BLOOM.add({ t0: 18.04, dur: .22, cx: SD[0], cy: SD[1], r: 34, color: LP.gold, alpha: 1, shape: (c) => c.arc(SD[0], SD[1], 26, 0, 7) });
    ST.forEach(([x, y], i) => BLOOM.add({ t0: TI[i] - .30, dur: .18, cx: x, cy: y, r: 24, color: LP.gold, alpha: 1, shape: (c) => c.arc(x, y, 14, 0, 7), t1: TI[i] + .15, outDur: .3 }));
  });
  WORLD.under.push((t) => {
    // «طيف التوحد»: the infinity fills with the spectrum — every colour belongs
    const k = KT.eOut((t - 36.52) / .55); if (k <= 0 || !T.inf) return;
    const gr = g.createLinearGradient(IN[0] - IA, 0, IN[0] + IA, 0);
    [[0, '#8fd8c3'], [.38, '#e9c46b'], [.7, '#e8935c'], [1, '#d97ba7']].forEach(([p, c]) => gr.addColorStop(p, c));
    g.save(); g.beginPath(); g.arc(IN[0], IN[1], 420 * k, 0, 7); g.clip();
    g.globalAlpha = .92; g.fillStyle = gr; g.beginPath(); polyShape([T.inf])(g); g.fill(); g.restore();
  });
  (WORLD.lineFx = WORLD.lineFx || []).push((t, px, c) => {
    // the spectrum's light runs into the next chapter
    const k = (t - 36.60) / .70; if (k <= 0 || k >= 1) return;
    const s = LINE.head(t);
    LINE.stroke(Math.max(0, s - 2200), s, { color: '#fff1c8', px: px * 1.5, alpha: Math.sin(Math.PI * k) * .9, z: c.z, under: .2, core: 1 });
  });
  window.FLASH = (window.FLASH || []).concat([36.52]);

  WORLD.over.push((t) => {
    wtext(T.lkl, t, { wx: 0, wy: -7480, t0: 17.40, in: 'mask' });
    wtext(T.qdr, t, { wx: 0, wy: -7340, t0: 17.86, in: 'mask' });
    wtext(T.sth, t, { wx: 170, wy: -7030, t0: 19.44, in: 'rise', dist: 24 });
    wtext(T.tkt, t, { wx: 150, wy: -6912, t0: 19.64, in: 'mask' });
    wtext(T.tnm, t, { wx: -256, wy: -6910, t0: 20.18, in: 'pop', spring: 'pop' });
    wtext(T.nqd, t, { wx: 0, wy: -8000, t0: 21.00, in: 'rise', dist: 26 });
    wtext(T.khd, t, { wx: 0, wy: -7875, t0: 22.32, in: 'mask' });
    T.lbl.forEach(([a, b], i) => { const [x, y] = ST[i], left = i % 2 === 0, lx = x + (left ? -146 : 146);
      wtext(a, t, { wx: lx, wy: y - 64, ax: left ? 1 : 0, t0: TI[i] - .10, in: 'rise', dist: 20 });
      wtext(b, t, { wx: lx, wy: y + 42, ax: left ? 1 : 0, t0: TI[i] + .06, in: 'mask' }); });
    wtext(T.prg, t, { wx: 0, wy: -12150, t0: 34.70, in: 'rise', dist: 24 });
    wtext(T.tyf, t, { wx: 0, wy: -12030, t0: 36.50, in: 'mask' });
  });
})();
