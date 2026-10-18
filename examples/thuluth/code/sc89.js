// ════════════════════════════════════════════════════════════════════
//  v3 · S8 (131.46 – 188.92) nine worlds · S9 (188.92 – 236.1) today → forever
// ════════════════════════════════════════════════════════════════════
(() => {
  const P = {};
  const NUM = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  const NAMES = ['المفرَّق', 'الوسط', 'المشبَّك', 'الجليّ', 'المحبوك', 'الزخرفيّ', 'المختزَل', 'المتناظر', 'المسلسَل'];
  const VB = { w: 1243, h: 576 };
  INITS.push(async () => {
    const L = (k, f) => A[k] ? Promise.resolve() : loadImg(k, f);
    await Promise.all([L('pl_desk', 'assets/v3/plate_desk.jpg'), L('pl_hand', 'assets/v3/plate_hand.jpg'), L('pl_archive', 'assets/v3/plate_archive.jpg'), L('pl_scan', 'assets/v3/plate_scan.jpg'),
      L('pl_tablet', 'assets/v3/plate_tablet.jpg'), L('pl_laser', 'assets/v3/plate_laser.jpg'), L('pl_mat', 'assets/v3/plate_materials.jpg'), L('pl_mihrab', 'assets/v3/plate_mihrab.jpg'),
      L('r_sevki', 'assets/v3/real/sevki_murakka.jpg'), L('yaqut3', 'assets/v3/yaqut.jpg'), L('r_dense', 'assets/v3/real/lv_dense.jpg'), L('r_bursa', 'assets/v3/real/bursa_wall.jpg'),
      L('r_hagia', 'assets/v3/real/hagia_med.jpg'), L('r_knot', 'assets/v3/real/bursa_knot.jpg'), L('r_round', 'assets/v3/real/round_lv.jpg'), L('r_lion', 'assets/v3/real/lion.jpg'),
      L('r_mirror', 'assets/v3/real/mirror.jpg'), L('crown3', 'assets/v3/crown.png')]);
    P.c1 = card([{ t: 'وليس الثُّلُثُ', size: 52, color: PAL.cream }, { t: 'شكلاً واحداً', size: 84, color: PAL.cream }], { seed: 801, dark: true, padX: 70 });
    P.c9 = card([{ t: 'بل هو', size: 46, color: PAL.cream, weight: 400 }, { t: 'تسعةُ عوالم', size: 96, color: PAL.goldL }], { seed: 802, dark: true, padX: 70 });
    P.tiles = NAMES.map((n, i) => ({ p: paper({ w: 300, h: 150, seed: 810 + i, rough: 5, burn: .55 }), t: textImg([{ t: NUM[i], size: 30, font: UI, weight: 800, color: PAL.goldD, lh: 1.1 }, { t: n, size: 50, color: PAL.ink, lh: 1.15 }]) }));
    P.ch = NAMES.map((n, i) => card([{ t: NUM[i] + ' / ٩', size: 30, font: UI, weight: 700, color: PAL.goldL }, { t: 'الثلث ' + n, size: 74, color: PAL.cream }], { seed: 830 + i, dark: true, padX: 60, padY: 30 }));
    const cap = (s, i, s2 = null) => card(s2 ? [{ t: s, size: 46 }, { t: s2, size: 46, color: PAL.goldD }] : [{ t: s, size: 46 }], { seed: 850 + i, padX: 56, padY: 28 });
    P.cap = [cap('تتباعدُ الحروفُ بوضوح', 0, 'دون تشابُك'), cap('معتدلٌ بين', 1, 'الترابطِ والتباعُد'), cap('يكتنزُ بالحروف', 2, 'فوق بعضِها'), cap('بأقلامٍ عريضةٍ جدّاً', 3),
      cap('كضفيرةٍ معقّدة', 4), cap('ممزوجٌ بالزخارفِ', 5, 'النباتيّةِ والهندسيّة'), cap('تُصوََّرُ فيه الحروف', 6, 'لتَقهرَ المساحة'), cap('انعكاسٌ مرآويٌّ', 7, 'مُعجِز'),
      cap('تتّصلُ نهاياتُ الحروف', 8, 'ببداياتِها'), cap('كسلسلةٍ لا تنقطع', 9)];
    P.capMosque = cap('ليُخلَّدَ على جدرانِ', 10, 'المساجدِ والقباب');
    P.s1 = photo(A.r_sevki, 1160, { crop: [300, 990, 2000, 420], seed: 861, rough: 6, mul: 0 });
    P.s2 = photo(A.yaqut3, 1080, { crop: [106, 345, 1330, 350], seed: 862, rough: 6, mul: 0 });
    P.s3 = photo(A.r_dense, 700, { seed: 863, rough: 6, mul: 0 });
    P.s5 = photo(A.r_knot, 980, { crop: [1880, 500, 1260, 900], seed: 865, rough: 7, mul: 0 });
    P.s6 = photo(A.r_round, 760, { seed: 866, rough: 6, mul: 0 });
    P.s7 = photo(A.r_lion, 1020, { seed: 867, rough: 6, mul: 0 });
    P.s8 = photo(A.r_mirror, 1020, { seed: 868, rough: 6, mul: 0 });
    P.disc = paper({ w: 900, h: 900, seed: 869, rough: 8, burn: .6 });
    // S9
    P.tToday = textImg([{ t: 'واليوم…', size: 64, color: PAL.goldL, weight: 400 }]);
    P.cOld = card([{ t: 'لم يبقَ الثُّلُثُ', size: 56, color: PAL.cream }, { t: 'حبيسَ الأوراقِ القديمة', size: 72, color: PAL.goldL }], { seed: 901, dark: true, padX: 70 });
    P.cReed = card([{ t: 'يبدأُ من قصبةِ الخطّاط', size: 56, color: PAL.cream }], { seed: 902, dark: true, padX: 60, padY: 28 });
    P.scanSheet = photo(A.r_sevki, 700, { crop: [300, 990, 2000, 420], seed: 903, rough: 5, mul: 0 });
    P.cScan = card([{ t: 'مسحٌ ضوئيٌّ عالي الدقّة', size: 50, color: PAL.cream }, { t: '1200 dpi', size: 30, font: UI, weight: 700, color: PAL.goldL }], { seed: 904, dark: true, padX: 56, padY: 26 });
    P.vecSheet = paper({ w: 1300, h: 640, seed: 905, rough: 7, burn: .5 });
    P.tVec = card([{ t: 'الفكتور · إليستريتور', size: 40, font: UI, weight: 700, color: PAL.cream }], { seed: 906, dark: true, padX: 44, padY: 22, rough: 3 });
    P.cCurves = card([{ t: 'منحنياتٌ صافية', size: 72 }], { seed: 907, padX: 66, padY: 30 });
    P.cNoBreak = card([{ t: 'تُكبَّرُ لعمائرِ المساجد', size: 50, color: PAL.cream }, { t: 'دون أن تتكسّر', size: 74, color: PAL.goldL }], { seed: 908, dark: true, padX: 66 });
    P.tRaster = card([{ t: 'صورة نقطيّة', size: 30, font: UI, weight: 700, color: PAL.cream }], { seed: 909, dark: true, padX: 30, padY: 16, rough: 3 });
    P.tVector = card([{ t: 'مسار متّجه', size: 30, font: UI, weight: 700, color: PAL.cream }], { seed: 910, dark: true, padX: 30, padY: 16, rough: 3 });
    P.cAI = card([{ t: 'الذكاءُ الاصطناعيّ', size: 62, color: PAL.cream }, { t: 'وبروكريت', size: 52, color: PAL.goldL }], { seed: 911, dark: true, padX: 66 });
    P.cLaser = card([{ t: 'مكائنُ الليزر', size: 64, color: PAL.cream }, { t: 'تنحتُه', size: 52, color: PAL.goldL }], { seed: 912, dark: true, padX: 66 });
    P.tMat = ['الخشب', 'المعدن', 'الرخام'].map((s, i) => card([{ t: s, size: 44, color: PAL.cream }], { seed: 913 + i, dark: true, padX: 44, padY: 20, rough: 3 }));
    P.cWitness = card([{ t: 'سيبقى خطُّ الثُّلُث', size: 52, color: PAL.cream }, { t: 'شاهداً خالداً', size: 84, color: PAL.goldL }], { seed: 920, dark: true, padX: 70 });
    P.tEnd = textImg([{ t: 'سلطانٌ يتربّعُ على عرشِ الجمال', size: 58, color: PAL.cream }, { divider: 360, size: 30, color: PAL.gold }, { t: 'إلى الأبد', size: 44, color: PAL.goldL, weight: 400 }]);
    // vector path of the hero word
    P.vec = new Path2D(); THULUTH_VEC.forEach(poly => { poly.forEach(([x, y], i) => i ? P.vec.lineTo(x, y) : P.vec.moveTo(x, y)); P.vec.closePath(); });
    P.wordGold = mk(VB.w, VB.h); { const x = P.wordGold.getContext('2d'); x.fillStyle = '#d9a440'; x.fill(P.vec, 'evenodd'); x.drawImage(A.dot, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = '#d9a440'; x.fillRect(0, 0, VB.w, VB.h); }
    P.wordInk = mk(VB.w, VB.h); { const x = P.wordInk.getContext('2d'); x.drawImage(A.ink, 0, 0); x.drawImage(A.dot, 0, 0); }
    P.tiny = mk(62, 29); { const x = P.tiny.getContext('2d'); x.drawImage(P.wordInk, 0, 0, 62, 29); }
    P.goldBuf = mk(VB.w, VB.h);
  });

  const desk = (t, a, b, dim = .62, s0 = 1.0, s1 = 1.05) => { plate(A.pl_desk, t, a, b, { s0, s1, dim }); rays(t, { x: 120, y: -320, ang: .92, int: .11 }); };
  // plate + mapping from plate pixels to stage
  function plateM(img, t, a, b, { s0 = 1, s1 = 1.06, fx0 = .5, fy0 = .5, fx1 = .5, fy1 = .5, dim = 0 } = {}) {
    plate(img, t, a, b, { s0, s1, fx0, fy0, fx1, fy1, dim });
    const k = ease(a, b, t), s = lerp(s0, s1, k), fx = lerp(fx0, fx1, k), fy = lerp(fy0, fy1, k);
    const base = Math.max(W / img.width, H / img.height), w = img.width * base * s, h = img.height * base * s;
    const x = clamp(W / 2 - fx * w, W - w, 0), y = clamp(H / 2 - fy * h, H - h, 0), K = base * s;
    return { K, map: (px, py) => [x + px * K, y + py * K] };
  }
  const dropP = (p, t, t0, x, y, rot = 0, id = 1, t1 = null) => { const k = sp(t, t0, 'card'); if (k <= .001) return null; const ko = t1 ? ease(t1, t1 + .45, t) : 0; if (ko >= 1) return null;
    const b = breathe(id, t, .5), X = x + b[0] - ko * 60, Y = y - (1 - k) * 150 + b[1] + ko * 80, R = rot + (1 - k) * .08 + b[2];
    drawP(p, X, Y, { rot: R, lift: 1 - k, alpha: clamp(k * 3) * (1 - ko) }); return { X, Y, R, k }; };
  // the word in gold, written at progress p
  function goldWord(p, x, y, w, alpha = 1) { const h = w * VB.h / VB.w, c = P.goldBuf.getContext('2d'); c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, VB.w, VB.h);
    c.drawImage(inkFrame(clamp(p)), 0, 0); if (p >= 1) c.drawImage(A.dot, 0, 0); c.globalCompositeOperation = 'source-in';
    const gr = c.createLinearGradient(0, 0, 0, VB.h); gr.addColorStop(0, '#f3d58e'); gr.addColorStop(.6, '#d4a04a'); gr.addColorStop(1, '#a7742c'); c.fillStyle = gr; c.fillRect(0, 0, VB.w, VB.h);
    g.save(); g.globalAlpha = alpha; g.shadowColor = 'rgba(0,0,0,.65)'; g.shadowBlur = 24; g.shadowOffsetY = 10; g.drawImage(P.goldBuf, x - w / 2, y - h / 2, w, h); g.restore(); return { x0: x - w / 2, y0: y - h / 2, w, h }; }

  // 28 · not one shape — nine worlds (131.46 – 135.68)
  SHOTS.push({ a: 131.46, b: 135.68, draw: (t) => {
    desk(t, 131.4, 135.8, .7, 1.0, 1.04);
    P.tiles.forEach((tl, i) => { const c = i % 3, r = Math.floor(i / 3), x = 1560 - c * 340, y = 300 + r * 200, t0 = 133.55 + i * .11, k = sp(t, t0, 'card'); if (k <= 0) return;
      const b = breathe(60 + i, t, .4), rot = (hash(i, 3) - .5) * .06 + (1 - k) * .1;
      drawP(tl.p, x + b[0], y - (1 - k) * 120 + b[1], { rot, lift: 1 - k, alpha: clamp(k * 3) });
      g.save(); g.translate(x + b[0], y - (1 - k) * 120 + b[1]); g.rotate(rot); writeOn(tl.t, 0, 0, easeOut(t0 + .1, t0 + .5, t)); g.restore(); });
    drawCard(P.c1, t, 131.6, 430, 520, { rot: -.02, t1: 133.4 });
    drawCard(P.c9, t, 134.4, 430, 540, { rot: .02 });
  } });

  // template for the nine styles: real specimen left, chapter card + caption right
  function style(i, a, b, piece, { x = 720, y = 520, rot = -.012, capT, cap2 = null, cap2T = null, chT = null, over = null, push = 1.05 } = {}) {
    SHOTS.push({ a, b, draw: (t) => {
      desk(t, a, b + .1, .74);
      const pz = ease(a, b + .2, t); camOn(lerp(1, push, pz), lerp(960, 900, pz), 540);
      const pc = P[piece], r = dropP(pc, t, a + .1, x, y, rot, 70 + i);
      if (r && over) over(t, r, pc);
      camOff();
      drawCard(P.ch[i], t, chT || a + .35, 1530, 320, { rot: .02 });
      drawCard(P.cap[i], t, capT, 1530, 700, { rot: -.015, t1: cap2T ? cap2T - .2 : null });
      if (cap2) drawCard(cap2, t, cap2T, 1530, 700, { rot: .015 });
    } });
  }
  const onPiece = (p, r, fn) => { p = P[p] || p; g.save(); g.translate(r.X, r.Y); g.rotate(r.R); fn(p.w, p.h); g.restore(); };

  // 1 · mufarraq — the master's separated letters
  style(0, 135.68, 141.72, 's1', { capT: 138.6, over: (t, r) => onPiece('s1', r, (w, h) => {
    const q = ease(138.7, 140.6, t); for (let j = 0; j < 7; j++) { const gx = w / 2 - w * (.12 + j * .125), s = sp(t, 138.7 + j * .18, 'snap'); if (s <= 0) continue;
      line([[gx, h * .18], [gx, h * .82]], s, { color: PAL.red, width: 3.4, dash: [8, 6], alpha: .9 * (1 - ease(140.8, 141.4, t)) }); } }) });
  // 2 · wasat — balanced
  style(1, 141.72, 146.58, 's2', { capT: 143.6, over: (t, r) => onPiece('s2', r, (w, h) => {
    const q = ease(144.6, 145.8, t); if (q <= 0) return; const y0 = h / 2 + 150, L = w * .7;
    line([[-L / 2, y0], [L / 2, y0]], ease(144.4, 144.9, t), { color: PAL.goldL, width: 4 });
    const mx = lerp(L / 2, 0, spring(t - 144.8, 60, 9)); nuqta(g, mx, y0, 30, PAL.goldL);
    nuqta(g, L / 2, y0, 14, PAL.goldL); nuqta(g, -L / 2, y0, 14, PAL.goldL); }) });
  // 3 · mushabbak — stacked tiers
  style(2, 146.58, 152.2, 's3', { x: 700, capT: 149.1, over: (t, r) => onPiece('s3', r, (w, h) => {
    for (let j = 0; j < 4; j++) { const yy = -h * .3 + j * h * .2, q = ease(150.5 + j * .2, 151.1 + j * .2, t); if (q <= 0) continue;
      line([[w * .42, yy], [-w * .42, yy]], q, { color: PAL.cream, width: 2.6, dash: [10, 7] }); nuqta(g, w * .42 + 18, yy, 16, PAL.goldL); } }) });

  // 4a · jali on the walls of Bursa Ulu Camii (real photo)
  SHOTS.push({ a: 152.2, b: 157.1, draw: (t) => {
    plate(A.r_bursa, t, 152.1, 157.2, { s0: 1.0, s1: 1.14, fx0: .45, fy0: .42, fx1: .38, fy1: .35, dim: .12 });
    rays(t, { x: 600, y: -300, ang: 1.2, int: .1 });
    drawCard(P.ch[3], t, 153.3, 1540, 300, { rot: .02 });
    drawCard(P.cap[3], t, 155.1, 1540, 820, { rot: -.015 });
  } });
  // 4b · the domes: Hagia Sophia roundel
  SHOTS.push({ a: 157.1, b: 160.42, draw: (t) => {
    plate(A.r_hagia, t, 157.0, 160.5, { s0: 1.0, s1: 1.1, fx0: .5, fy0: .36, fx1: .48, fy1: .33, dim: .1 });
    rays(t, { x: 1500, y: -200, ang: 2.3, int: .1 });
    drawCard(P.ch[3], t, 157.0, 1540, 300, { rot: .02 });
    drawCard(P.capMosque, t, 157.6, 1540, 820, { rot: -.015 });
  } });

  // 5 · mahbuk — the braid (real knot from Bursa) + a gold three‑strand plait
  style(4, 160.42, 165.86, 's5', { capT: 163.5, over: (t, r) => onPiece('s5', r, (w, h) => {
    const q = ease(163.4, 165.0, t); if (q <= 0) return; const y0 = h / 2 + 70, L = w * .9;
    for (let s = 0; s < 3; s++) { const pts = []; for (let j = 0; j <= 120; j++) { const u = j / 120; pts.push([L / 2 - u * L, y0 + Math.sin(u * Math.PI * 8 + s * 2.094) * 18]); }
      line(pts, q, { color: [PAL.goldL, PAL.cream, PAL.gold][s], width: 4 }); } }) });
  // 6 · zukhrufi — gold rosette over illuminated panel
  style(5, 165.86, 168.92, 's6', { x: 700, capT: 166.9, over: (t, r) => onPiece('s6', r, (w, h) => {
    const q = ease(166.4, 168.0, t); if (q <= 0) return; const R = w * .56;
    for (let j = 0; j < 2; j++) { const pts = []; for (let k = 0; k < 4; k++) { const a = j * Math.PI / 4 + k * Math.PI / 2; pts.push([Math.cos(a) * R, Math.sin(a) * R]); } line(pts, q, { color: PAL.goldL, width: 2.4, closed: true }); }
    arc(0, 0, R * 1.02, q, { color: PAL.goldL, width: 2 }); }) });
  // 7 · mukhtazal — the lion made of letters
  style(6, 168.92, 174.36, 's7', { capT: 170.9, push: 1.12, over: (t, r) => onPiece('s7', r, (w, h) => {
    const q = ease(171.9, 172.6, t) * (1 - ease(173.6, 174.2, t)); if (q <= 0) return;
    g.save(); g.globalAlpha = q; g.strokeStyle = PAL.goldL; g.lineWidth = 3; g.setLineDash([10, 8]); g.strokeRect(-w * .44, -h * .4, w * .88, h * .8); g.restore(); }) });
  // 8 · mutanazir — mirror axis
  style(7, 174.36, 178.66, 's8', { capT: 176.3, over: (t, r) => onPiece('s8', r, (w, h) => {
    const ax = -w / 2 + 1208 / 2400 * w, q = ease(175.8, 176.6, t); if (q <= 0) return;
    line([[ax, -h * .46], [ax, h * .46]], q, { color: PAL.red, width: 5, dash: [14, 9] });
    const s = ease(176.6, 177.4, t); for (const d of [-1, 1]) { const x0 = ax + d * 60, x1 = ax + d * (60 + 120 * s);
      line([[x0, h * .5 + 26], [x1, h * .5 + 26]], 1, { color: PAL.goldL, width: 3.5 }); if (s > .1) line([[x1 - d * 14, h * .5 + 14], [x1, h * .5 + 26], [x1 - d * 14, h * .5 + 38]], 1, { color: PAL.goldL, width: 3.5 }); } }) });

  // 9 · musalsal — the word as an unbroken chain
  SHOTS.push({ a: 178.66, b: 188.92, draw: (t) => {
    desk(t, 178.6, 189.0, .76);
    const CX = 730, CY = 540, k = sp(t, 178.75, 'card'), b = breathe(79, t, .4);
    drawP(P.disc, CX + b[0], CY - (1 - k) * 140 + b[1], { rot: -.02, lift: 1 - k, alpha: clamp(k * 3) });
    const n = 6, R = 270, spin = (t - 178.7) * .09 + spring(t - 184.42, 200, 14) * .0, close = sp(t, 184.42, 'snap');
    g.save(); g.translate(CX + b[0] + shake(t, 184.42, 4), CY + b[1]); g.rotate(-spin);
    for (let i = 0; i < n; i++) { const a = -Math.PI / 2 - i * 2 * Math.PI / n, q = sp(t, 179.9 + i * .22, 'snap'); if (q <= 0) continue;
      g.save(); g.rotate(a + Math.PI / 2); g.translate(0, -R); const w = 250 * q; g.drawImage(P.wordInk, -w / 2, -w * VB.h / VB.w / 2, w, w * VB.h / VB.w); g.restore(); }
    // links between consecutive words; the last one closes the loop
    for (let i = 0; i < n; i++) { const a = -Math.PI / 2 - (i + .5) * 2 * Math.PI / n, last = i === n - 1, q = last ? close : ease(182.3 + i * .35, 182.7 + i * .35, t); if (q <= 0) continue;
      g.save(); g.rotate(a + Math.PI / 2); g.translate(0, -R); g.strokeStyle = last ? PAL.red : PAL.goldD; g.lineWidth = 6; g.beginPath(); g.ellipse(0, 0, 30 * Math.max(.01, q), 16, 0, 0, Math.PI * 2 * Math.min(1, q)); g.stroke(); g.restore(); }
    g.restore();
    drawCard(P.ch[8], t, 179.9, 1530, 320, { rot: .02 });
    drawCard(P.cap[8], t, 182.3, 1530, 700, { rot: -.015, t1: 185.2 });
    drawCard(P.cap[9], t, 185.45, 1530, 700, { rot: .015 });
  } });

  // 37 · today — no longer locked in old papers (188.92 – 193.6)
  SHOTS.push({ a: 188.92, b: 193.6, draw: (t) => {
    plate(A.pl_archive, t, 188.9, 193.7, { s0: 1.0, s1: 1.1, fx0: .4, fx1: .3, dim: .1 });
    rays(t, { x: 100, y: -100, ang: .7, int: .12 });
    const ko = ease(190.4, 190.7, t); if (ko < 1) writeOn(P.tToday, 1460, 330 - ko * 40, easeOut(189.0, 189.7, t), { alpha: 1 - ko });
    drawCard(P.cOld, t, 190.6, 1460, 520, { rot: -.02 });
  } });
  // 38 · it starts from the calligrapher's reed (193.6 – 196.06)
  SHOTS.push({ a: 193.6, b: 196.06, draw: (t) => {
    plate(A.pl_hand, t, 193.5, 196.2, { s0: 1.1, s1: 1.2, fx0: .55, fy0: .55, fx1: .6, fy1: .62, dim: .25 });
    rays(t, { x: 160, y: -300, ang: .95, int: .12 });
    drawCard(P.cReed, t, 194.6, 1400, 900, { rot: .015 });
  } });
  // 39 · high‑resolution scan (196.06 – 199.18)
  SHOTS.push({ a: 196.06, b: 199.18, draw: (t) => {
    plate(A.pl_scan, t, 196.0, 199.3, { s0: 1.0, s1: 1.06, fx1: .55, dim: .2 });
    const r = dropP(P.scanSheet, t, 196.15, 1380, 250, .02, 91);
    if (r) { const sw = ease(196.6, 198.2, t), w = P.scanSheet.w, h = P.scanSheet.h; g.save(); g.translate(r.X, r.Y); g.rotate(r.R);
      // not yet scanned: dimmed
      g.fillStyle = 'rgba(20,14,8,.5)'; g.fillRect(-w / 2, -h / 2 + h * sw, w, h * (1 - sw));
      if (sw > 0 && sw < 1) { const yy = -h / 2 + h * sw; g.save(); g.globalCompositeOperation = 'screen'; const gr = g.createLinearGradient(0, yy - 30, 0, yy + 30);
        gr.addColorStop(0, 'rgba(180,220,255,0)'); gr.addColorStop(.5, 'rgba(200,235,255,.9)'); gr.addColorStop(1, 'rgba(180,220,255,0)'); g.fillStyle = gr; g.fillRect(-w / 2 - 20, yy - 30, w + 40, 60); g.restore(); }
      g.restore(); }
    drawCard(P.cScan, t, 197.1, 1380, 470, { rot: -.015 });
  } });
  // 40 · the vector (199.18 – 204.38)
  SHOTS.push({ a: 199.18, b: 204.38, draw: (t) => {
    desk(t, 199.1, 204.5, .82);
    const k = sp(t, 199.25, 'card'), b = breathe(92, t, .3), X = 900 + b[0], Y = 520 - (1 - k) * 140 + b[1];
    drawP(P.vecSheet, X, Y, { rot: -.01, lift: 1 - k, alpha: clamp(k * 3) });
    const S = 1000 / VB.w; g.save(); g.translate(X, Y); g.rotate(-.01); g.translate(-VB.w * S / 2, -VB.h * S / 2); g.scale(S, S);
    // outline draws on, polygon by polygon
    const op = ease(199.5, 201.2, t), fill = ease(202.3, 203.1, t);
    if (fill > 0) { g.save(); g.beginPath(); g.rect(VB.w * (1 - fill), -20, VB.w * fill + 20, VB.h + 40); g.clip(); g.fillStyle = PAL.ink; g.fill(P.vec, 'evenodd'); g.drawImage(A.dot, 0, 0); g.restore(); }
    THULUTH_VEC.forEach((poly, i) => { const q = clamp(op * THULUTH_VEC.length - i); if (q > 0) line(poly, q, { color: PAL.goldD, width: 2.4 / S * .9, closed: true, alpha: 1 - fill * .6 }); });
    // anchors + handles
    const an = ease(200.4, 201.6, t), ao = ease(203.0, 203.6, t);
    if (an > 0 && ao < 1) { g.globalAlpha = 1 - ao; let c = 0; THULUTH_VEC.forEach(poly => poly.forEach(([x, y], j) => { if (j % 3) return; c++; if (c / 70 > an) return; const s = 9 / S;
      g.fillStyle = '#fff8e8'; g.strokeStyle = '#2c6fd6'; g.lineWidth = 1.6 / S; g.fillRect(x - s / 2, y - s / 2, s, s); g.strokeRect(x - s / 2, y - s / 2, s, s);
      if (j % 9 === 0) { const nx = poly[(j + 1) % poly.length], px = poly[(j - 1 + poly.length) % poly.length], dx = (nx[0] - px[0]) * 1.2, dy = (nx[1] - px[1]) * 1.2;
        g.strokeStyle = '#2c6fd6'; g.beginPath(); g.moveTo(x - dx, y - dy); g.lineTo(x + dx, y + dy); g.stroke(); g.fillStyle = '#2c6fd6'; g.beginPath(); g.arc(x + dx, y + dy, 4 / S, 0, 6.283); g.arc(x - dx, y - dy, 4 / S, 0, 6.283); g.fill(); } })); g.globalAlpha = 1; }
    g.restore();
    drawCard(P.tVec, t, 199.4, 520, 150, { rot: -.02, wdur: .4 });
    drawCard(P.cCurves, t, 202.4, 1500, 900, { rot: .015 });
  } });
  // 41 · scaled to mosque architecture without breaking (204.38 – 209.98)
  SHOTS.push({ a: 204.38, b: 209.98, draw: (t) => {
    const M = plateM(A.pl_mihrab, t, 204.3, 210.1, { s0: 1.0, s1: 1.16, fx0: .5, fy0: .45, fx1: .49, fy1: .4, dim: .15 });
    rays(t, { x: 300, y: -200, ang: 1.0, int: .12 });
    const gk = sp(t, 204.6, 'soft'), [cx, cy] = M.map(1000, 330), w = lerp(120, 560, ease(204.6, 206.6, t)) * M.K;
    if (gk > 0) { g.save(); g.globalAlpha = clamp(gk * 2); g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 20; g.drawImage(P.wordGold, cx - w / 2, cy - w * VB.h / VB.w / 2, w, w * VB.h / VB.w); g.restore(); }
    // two loupes: raster breaks, vector stays crisp
    const lq = sp(t, 207.35, 'card');
    if (lq > 0) [[470, P.tiny, true, P.tRaster], [1450, P.wordGold, false, P.tVector]].forEach(([x, src, pix, tag], i) => { const y = 760 - (1 - lq) * 80, r = 150;
      g.save(); g.globalAlpha = clamp(lq * 3); g.save(); g.filter = 'blur(14px)'; g.fillStyle = 'rgba(0,0,0,.6)'; g.beginPath(); g.arc(x + 12, y + 18, r + 10, 0, 6.283); g.fill(); g.restore();
      g.beginPath(); g.arc(x, y, r, 0, 6.283); g.save(); g.clip(); g.fillStyle = '#efe2c4'; g.fillRect(x - r, y - r, 2 * r, 2 * r);
      const FX = 1000, FY = 330, Z = 1.25; g.translate(x - FX * Z, y - FY * Z); g.scale(Z, Z);
      if (pix) { g.imageSmoothingEnabled = false; g.drawImage(P.tiny, 0, 0, VB.w, VB.h); g.imageSmoothingEnabled = true; } else { g.fillStyle = PAL.ink; g.fill(P.vec, 'evenodd'); }
      g.restore(); g.lineWidth = 12; g.strokeStyle = '#a8823c'; g.beginPath(); g.arc(x, y, r + 5, 0, 6.283); g.stroke(); g.restore();
      drawCard(tag, t, 207.6 + i * .15, x, y + r + 50, { rot: (i ? -1 : 1) * .02, wdur: .3 }); });
    drawCard(P.cNoBreak, t, 205.9, 960, 930, { rot: -.01, t1: 207.2 });
  } });
  // 42 · AI & Procreate (209.98 – 214.26)
  SHOTS.push({ a: 209.98, b: 214.26, draw: (t) => {
    const M = plateM(A.pl_tablet, t, 209.9, 214.4, { s0: 1.0, s1: 1.0, dim: .1 });
    // screen affine: TL, TR, BL in plate px
    const [ox, oy] = M.map(621, 508), [ux, uy] = M.map(1240, 360), [vx, vy] = M.map(913, 833);
    g.save(); g.setTransform((ux - ox), (uy - oy), (vx - ox), (vy - oy), ox, oy);
    const p = (t - 210.3) / 2.4; if (p > 0) { g.drawImage(inkFrame(clamp(p)), .1, .22, .66, .66 * (VB.h / VB.w) * ((Math.hypot(ux - ox, uy - oy)) / Math.hypot(vx - ox, vy - oy))); }
    if (t > 212.75) { const s = sp(t, 212.75, 'snap'); g.globalAlpha = clamp(s * 3); g.drawImage(A.dot, .1, .22, .66, .66 * (VB.h / VB.w) * ((Math.hypot(ux - ox, uy - oy)) / Math.hypot(vx - ox, vy - oy))); }
    g.restore();
    drawCard(P.cAI, t, 210.9, 470, 880, { rot: -.02 });
  } });
  // 43 · laser engraving (214.26 – 216.88)
  SHOTS.push({ a: 214.26, b: 216.88, draw: (t) => {
    const M = plateM(A.pl_laser, t, 214.2, 217.0, { s0: 1.0, s1: 1.18, fx0: .5, fy0: .6, fx1: .45, fy1: .66, dim: .05 });
    const [bx, by] = M.map(1016, 791);
    // engraved word trails out of the beam as the slab travels
    const u = ease(214.4, 216.8, t), w = 520 * M.K * 1.4, h = w * VB.h / VB.w;
    g.save(); g.translate(bx - 10, by + 60 * M.K); g.scale(1, .42); const x0 = -w * u;
    g.beginPath(); g.rect(x0, -h, w * u + 2, h * 2); g.clip(); g.globalAlpha = .8; g.drawImage(P.wordInk, x0, -h / 2, w, h); g.restore();
    // sparks (deterministic)
    g.save(); g.globalCompositeOperation = 'screen';
    for (let i = 0; i < 40; i++) { const life = .5, ph = (t * 1.7 + hash(i, 5)) % 1, age = ph * life, a = -Math.PI / 2 + (hash(i, 9) - .5) * 2.6, v = 300 + 500 * hash(i, 11);
      const x = bx + Math.cos(a) * v * age, y = by + Math.sin(a) * v * age + 900 * age * age; g.fillStyle = `rgba(255,${170 + 60 * hash(i, 2) | 0},90,${1 - ph})`; g.beginPath(); g.arc(x, y, 2.4 * (1 - ph) + .6, 0, 6.283); g.fill(); }
    const gl = g.createRadialGradient(bx, by, 0, bx, by, 90); gl.addColorStop(0, 'rgba(255,200,120,.8)'); gl.addColorStop(1, 'rgba(255,160,60,0)'); g.fillStyle = gl; g.fillRect(bx - 90, by - 90, 180, 180); g.restore();
    drawCard(P.cLaser, t, 214.9, 1520, 270, { rot: .02 });
  } });
  // 44 · marble · metal · wood (216.88 – 220.06)
  SHOTS.push({ a: 216.88, b: 220.06, draw: (t) => {
    const M = plateM(A.pl_mat, t, 216.8, 220.2, { s0: 1.0, s1: 1.04, dim: .08 });
    [[1293, 217.1, 'rgba(70,70,74,.85)', 2], [831, 217.62, 'rgba(60,38,10,.85)', 1], [368, 218.36, 'rgba(25,12,4,.9)', 0]].forEach(([px, t0, col, ti]) => {
      const [x, y] = M.map(px, 470), w = 330 * M.K, h = w * VB.h / VB.w, q = ease(t0, t0 + .7, t); if (q <= 0) return;
      const c = P.goldBuf.getContext('2d'); c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, VB.w, VB.h); c.drawImage(P.wordInk, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = col; c.fillRect(0, 0, VB.w, VB.h);
      g.save(); g.beginPath(); g.rect(x + w / 2 - w * q, y - h, w * q + 4, h * 2); g.clip(); g.globalCompositeOperation = 'multiply'; g.drawImage(P.goldBuf, x - w / 2, y - h / 2, w, h); g.restore();
      if (q < 1) { const ex = x + w / 2 - w * q; g.save(); g.globalCompositeOperation = 'screen'; const gr = g.createRadialGradient(ex, y, 0, ex, y, 40); gr.addColorStop(0, 'rgba(255,190,110,.9)'); gr.addColorStop(1, 'rgba(255,120,40,0)'); g.fillStyle = gr; g.fillRect(ex - 40, y - 40, 80, 80); g.restore(); }
      drawCard(P.tMat[ti], t, t0 + .1, x, M.map(px, 860)[1], { rot: (ti - 1) * .02, wdur: .3 }); });
  } });
  // 45 · finale — forever (220.06 – 236.1)
  SHOTS.push({ a: 220.06, b: 236.2, draw: (t) => {
    const M = plateM(A.pl_mihrab, t, 220.0, 236.2, { s0: 1.0, s1: 1.12, fx0: .5, fy0: .5, fx1: .5, fy1: .42, dim: .5 });
    rays(t, { x: 300, y: -200, ang: 1.0, int: .12 + .14 * ease(230.4, 232.0, t) });
    rays(t, { x: 1620, y: -200, ang: 2.14, int: .1 * ease(230.4, 232.0, t) });
    const CX = 960, CY = 520, WW = 980, up = ease(232.6, 233.6, t), y = CY - up * 40;
    const r = goldWord((t - 220.2) / 1.7, CX, y, WW);
    // engineered: circle, alif axis, baseline, nuqta rhombus
    const gp = (i) => ease(225.1 + i * .35, 225.8 + i * .35, t), go = 1 - ease(232.7, 233.6, t) * .75;
    if (t > 225) { g.save(); g.globalAlpha = go;
      arc(CX, y, WW * .56, gp(0), { color: PAL.goldL, width: 2.2 });
      line([[CX - WW * .62, y + r.h * .3], [CX + WW * .62, y + r.h * .3]], gp(1), { color: PAL.goldL, width: 2, dash: [10, 8] });
      const ax = r.x0 + 1175 / VB.w * WW; line([[ax, y - WW * .5], [ax, y + WW * .4]], gp(2), { color: PAL.goldL, width: 2, dash: [10, 8] });
      const RR = WW * .56; line([[CX, y - RR], [CX + RR, y], [CX, y + RR], [CX - RR, y]], gp(3), { color: PAL.goldL, width: 1.6, closed: true, alpha: .7 });
      for (const [dx, dy] of [[RR, 0], [-RR, 0], [0, RR], [0, -RR]]) { const s = sp(t, 227.0, 'snap'); if (s > 0) nuqta(g, CX + dx, y + dy, 16 * s, PAL.goldL); }
      g.restore(); }
    // the crown returns: a sultan
    const ck = spring(t - 228.0, 70, 11);
    if (ck > 0) { const cw = 330, ch = cw * A.crown3.height / A.crown3.width, yy = lerp(-300, y - r.h * .5 - ch * .4, ck);
      g.save(); g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 30; g.shadowOffsetY = 14; g.drawImage(A.crown3, CX - cw / 2 + 60, yy - ch / 2 + shake(t, 229.7, 3), cw, ch); g.restore(); }
    drawCard(P.cWitness, t, 222.1, 960, 920, { rot: -.01, t1: 224.9 });
    writeOn(P.tEnd, 960, 900, easeOut(230.6, 231.9, t));
    if (t > 235.2) { g.fillStyle = `rgba(0,0,0,${ease(235.2, 236.1, t)})`; g.fillRect(0, 0, W, H); }
  } });
})();
