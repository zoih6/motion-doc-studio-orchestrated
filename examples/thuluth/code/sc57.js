// ════════════════════════════════════════════════════════════════════
//  v3 · S5 (67.34 – 81.76) Ottoman peak · S6 (81.76 – 103.44) why hardest
//       S7 (103.44 – 131.46) the harakat pen & al‑haml
// ════════════════════════════════════════════════════════════════════
(() => {
  const P = {};
  const PCROP = [620, 0, 880, 1152];
  const tint = (img, color) => { const c = mk(img.width, img.height), x = c.getContext('2d'); x.drawImage(img, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = color; x.fillRect(0, 0, c.width, c.height); return c; };
  INITS.push(async () => {
    const L = (k, f) => A[k] ? Promise.resolve() : loadImg(k, f);
    await Promise.all([L('pl_desk', 'assets/v3/plate_desk.jpg'), L('pl_ist', 'assets/v3/plate_istanbul.jpg'), L('pl_hand', 'assets/v3/plate_hand.jpg'),
      L('r_hilye', 'assets/v3/real/hilye.jpg'), L('r_dense', 'assets/v3/real/lv_dense.jpg'), L('r_round', 'assets/v3/real/round_lv.jpg'), L('r_sevki', 'assets/v3/real/sevki_murakka.jpg'),
      L('r_jali', 'assets/v3/real/jali_lv.jpg'), L('por_hafiz', 'assets/v3/por_hafiz.jpg'), L('por_sevki', 'assets/v3/por_sevki.jpg'),
      L('pline', 'assets/v3/prayer_line.jpg'), L('pmarks', 'assets/v3/prayer_marks.png'), L('v2_reed', 'assets/v2/qalam_side.png')]);
    // S5
    P.cPeak = card([{ t: 'حتى بلغَ الثُّلُثُ', size: 54, color: PAL.cream }, { t: 'ذروةَ مجدِه', size: 96, color: PAL.goldL }], { seed: 501, dark: true, padX: 70 });
    P.cGold = card([{ t: 'عصرُه الذهبيّ', size: 92 }, { t: 'في العهد العثمانيّ', size: 56 }, { divider: 280, size: 24, color: PAL.gold }, { t: '٦٩٩ – ١٣٤٢ هـ', size: 30, font: UI, color: PAL.ink }], { seed: 502, padX: 80 });
    P.hilye = photo(A.r_hilye, 470, { seed: 503, rough: 6, mul: .08 });
    P.dense = photo(A.r_dense, 500, { seed: 504, rough: 6, mul: .08 });
    P.round = photo(A.r_round, 520, { seed: 505, rough: 6, mul: .08 });
    P.cGiants = card([{ t: 'عمالقةٌ خلّدوا أسماءَهم', size: 60, color: PAL.cream }], { seed: 506, dark: true, padX: 60, padY: 30 });
    P.hafiz = photo(A.por_hafiz, 660, { crop: PCROP, seed: 507, rough: 10, burn: .7, mul: 0 });
    P.nHafiz = textImg([{ t: 'الحافظ عثمان', size: 116, color: PAL.cream }, { divider: 300, size: 30, color: PAL.gold }, { t: 'إمامُ الخطّاطين العثمانيين', size: 40, font: UI, weight: 600, color: PAL.goldL }, { t: '(ت ١١١٠ هـ)', size: 34, font: UI, weight: 500, color: 'rgba(241,228,196,.75)' }]);
    P.sevki = photo(A.por_sevki, 660, { crop: [600, 0, 880, 1152], seed: 508, rough: 10, burn: .7, mul: 0 });
    P.nSevki = textImg([{ t: 'سلطانُ الحرف', size: 52, color: PAL.goldL, weight: 400 }, { t: 'محمد شوقي', size: 120, color: PAL.cream }, { divider: 300, size: 30, color: PAL.gold }, { t: '(ت ١٣٠٤ هـ)', size: 34, font: UI, weight: 500, color: 'rgba(241,228,196,.75)' }]);
    P.sevkiWork = photo(A.r_sevki, 760, { crop: [330, 110, 1980, 440], seed: 509, rough: 5, mul: .06 });
    P.tagSevki = card([{ t: 'من خطّ محمد شوقي · مَشق', size: 22, font: UI, weight: 600, color: PAL.cream }], { seed: 510, dark: true, padX: 36, padY: 22, rough: 3 });
    // S6
    P.cWhy = textImg([{ t: 'لماذا هو', size: 70, color: PAL.cream, weight: 400 }, { t: 'الأصعب', size: 170, color: PAL.cream }]);
    P.qm = textImg([{ t: '؟', size: 230, color: PAL.red }]);
    P.pline = photo(A.pline, 1640, { seed: 601, rough: 7, mul: .05, res: 1.2 });
    P.cErr = card([{ t: 'الخطأُ فيه', size: 50, color: PAL.cream }, { t: 'لا يُغتفَر', size: 92, color: '#e0563c' }], { seed: 602, dark: true, padX: 70 });
    P.cRuin = card([{ t: 'يُشوِّهُ لوحةً', size: 60 }, { t: 'بأكملِها', size: 86, color: PAL.red }], { seed: 603, padX: 70 });
    P.marksRed = tint(A.pmarks, '#c0391f'); P.marksGold = tint(A.pmarks, '#d9a440'); P.marksInk = tint(A.pmarks, '#2a1b10');
    P.jali = photo(A.r_jali, 1680, { seed: 604, rough: 6, mul: 0, res: 1.15 });
    P.cTall = card([{ t: 'حروفٌ طويلةٌ', size: 64 }, { t: 'ممشوقة', size: 96, color: PAL.goldD }], { seed: 605, padX: 70 });
    P.cCurve = card([{ t: 'وانحناءاتٌ', size: 64 }, { t: 'واسعة', size: 96, color: PAL.goldD }], { seed: 606, padX: 70 });
    P.compLine = photo(A.r_jali, 720, { crop: [120, 120, 2060, 640], seed: 607, rough: 5, mul: 0 });
    P.compRound = photo(A.r_round, 470, { seed: 608, rough: 5, mul: 0 });
    P.compDense = photo(A.r_dense, 450, { crop: [0, 90, 2204, 2204], seed: 609, rough: 5, mul: 0 });
    P.cPliant = card([{ t: 'طواعيةٌ هائلة في التركيب', size: 62, color: PAL.cream }], { seed: 610, dark: true, padX: 60, padY: 30 });
    // S7
    P.cBut = textImg([{ t: 'ولكن…', size: 64, color: PAL.goldL, weight: 400 }]);
    P.cKnow = card([{ t: 'هل تعلم', size: 104, color: PAL.cream }, { t: 'كيف تُشكَّلُ الحروف؟', size: 52, color: PAL.goldL }], { seed: 701, dark: true, padX: 80 });
    P.pline2 = photo(A.pline, 1700, { seed: 702, rough: 7, mul: .05, res: 1.2 });
    P.cHarakat = card([{ t: 'الحركاتُ الإعرابيّة', size: 58 }, { t: 'والتزيينيّة', size: 58, color: PAL.goldD }], { seed: 703, padX: 66 });
    P.mat = paper({ w: 1760, h: 860, seed: 704, rough: 8, burn: .6 });
    P.reed = cutout(A.v2_reed, 12);
    P.tBig = card([{ t: 'قلمُ الحروف', size: 40, color: PAL.cream }], { seed: 705, dark: true, padX: 40, padY: 20, rough: 3 });
    P.tSmall = card([{ t: 'قلمُ الحركات', size: 40, color: PAL.cream }], { seed: 706, dark: true, padX: 40, padY: 20, rough: 3 });
    P.cNotSame = card([{ t: 'لا تُكتَبُ بالقلمِ نفسِه', size: 56 }, { t: 'بل بقلمٍ آخرَ مخصّص', size: 56, color: PAL.goldD }], { seed: 707, padX: 60 });
    P.cQuarter = card([{ t: '¼', size: 130, font: UI, weight: 800, color: PAL.goldL }, { t: 'ربعُ عرضِ القلم', size: 54, color: PAL.cream }], { seed: 708, dark: true, padX: 70 });
    P.pline3 = photo(A.pline, 1780, { seed: 709, rough: 7, mul: .05, res: 1.2 });
    P.cWeave = card([{ t: 'تداخلٌ وتشابُك', size: 66, color: PAL.cream }], { seed: 710, dark: true, padX: 60, padY: 28 });
    P.cBal = card([{ t: 'وتوازنٌ بصريٌّ دقيق', size: 66, color: PAL.cream }], { seed: 711, dark: true, padX: 60, padY: 28 });
    P.cVoid = card([{ t: 'بين الفراغ', size: 66 }, { t: 'والامتلاء', size: 66, color: PAL.goldD }], { seed: 712, padX: 60, padY: 28 });
    P.cHaml = card([{ t: 'يُسمّيه الخطّاطون', size: 46, color: PAL.goldL, weight: 400, lh: 1.5 }, { t: 'الحَمْل', size: 170, color: PAL.cream, lh: 1.25, dy: 30 }], { seed: 713, dark: true, padX: 110, padY: 60, opts: { gap: 30 } });
  });

  const desk = (t, a, b, dim = .62, s0 = 1.0, s1 = 1.05) => { plate(A.pl_desk, t, a, b, { s0, s1, dim }); rays(t, { x: 120, y: -320, ang: .92, int: .11 }); };
  const nameBlock = (img, t, t0, x, y, t1 = null) => { const k = easeOut(t0, t0 + .9, t), ko = t1 ? ease(t1, t1 + .4, t) : 0; if (ko < 1) writeOn(img, x, y - ko * 60, k, { alpha: 1 - ko }); };
  const geoHalo = (t, t0, cx, cy, R) => { const k = ease(t0, t0 + 1.6, t); if (k <= 0) return;
    arc(cx, cy, R, k, { width: 1.4, alpha: .5 }); arc(cx, cy, R * .62, k, { width: 1.2, alpha: .4, dir: 1 });
    line([[cx - R * 1.25, cy], [cx + R * 1.25, cy]], k, { width: 1.2, alpha: .45 }); line([[cx, cy - R * 1.2], [cx, cy + R * 1.2]], k, { width: 1.2, alpha: .45 });
    for (const [dx, dy] of [[R, 0], [-R, 0], [0, R], [0, -R]]) if (k > .8) nuqta(g, cx + dx, cy + dy, 10, PAL.gold); };
  // drop-in for photos: from above with tilt
  const dropP = (p, t, t0, x, y, rot = 0, id = 1, from = 'drop', t1 = null) => { const k = sp(t, t0, 'card'); if (k <= .001) return null; const ko = t1 ? ease(t1, t1 + .45, t) : 0; if (ko >= 1) return null;
    const b = breathe(id, t, .5); let dx = 0, dy = -(1 - k) * 150; if (from === 'right') { dx = (1 - k) * 900; dy = 0; }
    dx -= ko * 60; dy += ko * 80; const X = x + dx + b[0], Y = y + dy + b[1], R = rot + (1 - k) * .08 + b[2];
    drawP(p, X, Y, { rot: R, lift: 1 - k, alpha: clamp(k * 3) * (1 - ko) }); return { X, Y, R }; };
  // map image px of a photo piece drawn at (X,Y,rot) → stage
  const onPiece = (p, X, Y, R, fn) => { g.save(); g.translate(X, Y); g.rotate(R); const [sx, sy, sw, sh] = p.crop, k = p.w / sw; g.translate(-p.w / 2 - sx * k, -p.h / 2 - sy * k); g.scale(k, k); fn(); g.restore(); };
  const blob = (x, y, r, seed, color) => { const R = rng(seed); g.save(); g.fillStyle = color; g.beginPath(); const n = 22;
    for (let i = 0; i <= n; i++) { const a = i / n * 6.283, rr = r * (.75 + R() * .45 + (i % 5 === 0 ? .35 : 0)); i ? g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr) : g.moveTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); }
    g.fill(); for (let i = 0; i < 9; i++) { const a = R() * 6.283, d = r * (1.3 + R() * 1.4), s = r * (.06 + R() * .14); g.beginPath(); g.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, s, 0, 6.283); g.fill(); } g.restore(); };

  // 16 · the Ottoman peak (67.34 – 73.52)
  SHOTS.push({ a: 67.34, b: 73.52, draw: (t) => {
    plate(A.pl_ist, t, 67.3, 73.6, { s0: 1.12, s1: 1.0, fx0: .62, fy0: .5, fx1: .5, fy1: .5, dim: .18 });
    rays(t, { x: 1500, y: 300, ang: 2.9, n: 6, int: .14, spread: .9 });
    drawCard(P.cPeak, t, 68.7, 560, 300, { rot: -.02, t1: 70.45 });
    drawCard(P.cGold, t, 70.75, 560, 330, { rot: .015 });
  } });

  // 17 · the giants: their real works (73.52 – 76.82)
  SHOTS.push({ a: 73.52, b: 76.82, draw: (t) => {
    desk(t, 73.5, 76.9, .7);
    const pan = ease(73.5, 77.0, t); camOn(1.0, lerp(1000, 920, pan), 520);
    dropP(P.round, t, 73.6, 1430, 470, .03, 31);
    dropP(P.hilye, t, 73.95, 960, 500, -.02, 32);
    dropP(P.dense, t, 74.3, 490, 470, .025, 33);
    camOff();
    drawCard(P.cGiants, t, 74.7, 960, 950, { rot: -.01 });
  } });

  // 18 · Hafiz Osman (76.82 – 78.78)
  SHOTS.push({ a: 76.82, b: 78.78, draw: (t) => {
    desk(t, 76.8, 78.9, .76, 1.05, 1.0);
    geoHalo(t, 76.95, 1400, 520, 360);
    const k = sp(t, 76.9, 'card'), b = breathe(18, t, .5);
    drawP(P.hafiz, 1400 + b[0], 540 - (1 - k) * 120 + b[1], { rot: -.015 + (1 - k) * .05, lift: 1 - k, alpha: clamp(k * 3) });
    nameBlock(P.nHafiz, t, 77.45, 580, 520);
  } });

  // 19 · Mehmed Şevki, sultan of the letter (78.78 – 81.76)
  SHOTS.push({ a: 78.78, b: 81.76, draw: (t) => {
    desk(t, 78.7, 81.9, .76);
    geoHalo(t, 78.9, 1400, 500, 360);
    const k = sp(t, 78.85, 'card'), b = breathe(19, t, .5);
    drawP(P.sevki, 1400 + b[0], 500 - (1 - k) * 120 + b[1], { rot: .015 + (1 - k) * .05, lift: 1 - k, alpha: clamp(k * 3) });
    nameBlock(P.nSevki, t, 79.0, 580, 440);
    const r = dropP(P.sevkiWork, t, 80.7, 600, 860, -.015, 34, 'right');
    if (r) drawCard(P.tagSevki, t, 81.0, 800, 960, { rot: .02, wdur: .35 });
  } });

  // 20 · why is it the hardest? (81.76 – 83.76)
  SHOTS.push({ a: 81.76, b: 83.76, draw: (t) => {
    desk(t, 81.7, 83.9, .84, 1.08, 1.02);
    const k = sp(t, 81.85, 'soft');
    writeOn(P.cWhy, 1040, 540 + (1 - k) * 30, easeOut(81.85, 82.9, t));
    const q = sp(t, 83.0, 'snap'); if (q > 0) { g.save(); g.translate(520, 560); g.rotate(-.12 * (1 - q) + Math.sin(t * 2) * .02); g.scale(lerp(1.6, 1, q), lerp(1.6, 1, q)); g.globalAlpha = clamp(q * 3); g.drawImage(P.qm, -P.qm.width / 2, -P.qm.height / 2); g.restore(); }
  } });

  // 21 · one slip ruins the whole panel (83.76 – 93.76)
  SHOTS.push({ a: 83.76, b: 93.76, draw: (t) => {
    desk(t, 83.7, 93.9, .74);
    const p = P.pline, X = 960, Y = 560, KX = p.w / 1900;
    const SX = 905, SY = 300;                                     // splat point (image px)
    const sx = X - p.w / 2 + SX * KX, sy = Y - p.h / 2 + SY * KX;
    const push = ease(86.8, 87.8, t) * (1 - ease(91.3, 92.1, t)), cs = lerp(1, 1.75, push);
    camOn(cs, lerp(960, sx + 40, push), lerp(540, sy + 20, push));
    const k = sp(t, 83.85, 'card'), b = breathe(21, t, .3);
    drawP(p, X + b[0], Y - (1 - k) * 140 + b[1], { lift: 1 - k, alpha: clamp(k * 3) });
    // the falling drop
    const T0 = 87.0, T1 = 87.62;
    if (t > T0 && t < T1) { const u = (t - T0) / (T1 - T0), dy = (1 - u * u) * 520; g.save(); g.globalAlpha = .35; g.fillStyle = '#000'; g.beginPath(); g.ellipse(sx + 6, sy + 8, 14 * u, 6 * u, 0, 0, 6.283); g.fill(); g.restore();
      g.fillStyle = '#140b05'; g.beginPath(); g.ellipse(sx, sy - dy, 9, 14, 0, 0, 6.283); g.fill(); }
    if (t >= T1) { const s = spring(t - T1, 260, 18), grow = 1 + ease(91.4, 93.0, t) * 1.2; blob(sx, sy, 30 * KX * 1.6 * Math.max(0, s) * grow, 77, 'rgba(20,11,5,.94)'); }
    // a misplaced haraka: correct place (gold ring) vs. where it fell (red)
    const M = PRAYER_MARKS.filter(m => m[2] > 18).sort((a, c) => Math.hypot(a[0] - 1000, a[1] - 190) - Math.hypot(c[0] - 1000, c[1] - 190))[0];
    const ep = ease(89.2, 89.9, t);
    if (ep > 0) { const mx = X - p.w / 2 + (M[0] + M[2] / 2) * KX, my = Y - p.h / 2 + (M[1] + M[3] / 2) * KX, r = Math.max(M[2], M[3]) * KX * .9;
      arc(mx, my, r, ease(89.6, 90.1, t), { color: PAL.goldD, width: 3, dash: [6, 5] });
      g.save(); g.translate(mx + 46 * ep, my - 34 * ep); g.rotate(.5 * ep); g.drawImage(P.marksRed, M[0], M[1], M[2], M[3], -M[2] * KX / 2, -M[3] * KX / 2, M[2] * KX, M[3] * KX); g.restore();
      const xp = ease(90.4, 90.8, t); if (xp > 0) { const cx = mx + 46, cy = my - 34, a = 16; line([[cx - a, cy - a], [cx + a, cy + a]], xp, { color: PAL.red, width: 4 }); line([[cx + a, cy - a], [cx - a, cy + a]], ease(90.6, 91.0, t), { color: PAL.red, width: 4 }); } }
    // … and the stain takes over the whole page
    const ru = ease(91.4, 93.4, t);
    if (ru > 0) { g.save(); g.globalCompositeOperation = 'multiply'; const gr = g.createRadialGradient(sx, sy, 10, sx, sy, 60 + ru * 1500);
      gr.addColorStop(0, 'rgba(90,40,20,.85)'); gr.addColorStop(.5, `rgba(150,80,50,${.55 * ru})`); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr;
      g.fillRect(X - p.w / 2, Y - p.h / 2, p.w, p.h); g.restore(); }
    camOff();
    drawCard(P.cErr, t, 84.85, 1500, 200, { rot: .02, t1: 91.2 });
    drawCard(P.cRuin, t, 91.6, 1480, 880, { rot: -.02 });
  } });

  // 22 · tall slender letters, wide curves (93.76 – 100.16) — real celî panel
  SHOTS.push({ a: 93.76, b: 100.16, draw: (t) => {
    desk(t, 93.7, 100.3, .78);
    const p = P.jali, X = 960, Y = 420, K = p.w / 2302, im = (ix, iy) => [X - p.w / 2 + ix * K, Y - p.h / 2 + iy * K];
    const push = ease(94.0, 100.3, t); camOn(lerp(1.0, 1.08, push), lerp(960, 1040, push), 500);
    const k = sp(t, 93.85, 'card'), b = breathe(22, t, .3);
    drawP(p, X + b[0], Y - (1 - k) * 140 + b[1], { lift: 1 - k, alpha: clamp(k * 3) });
    // light sweep right → left across the gilded letters
    const sw = ease(94.5, 96.0, t); if (sw > 0 && sw < 1) { const lx = lerp(X + p.w / 2, X - p.w / 2, sw); g.save(); g.globalCompositeOperation = 'screen';
      const gr = g.createLinearGradient(lx - 160, 0, lx + 160, 0); gr.addColorStop(0, 'rgba(255,220,150,0)'); gr.addColorStop(.5, 'rgba(255,220,150,.35)'); gr.addColorStop(1, 'rgba(255,220,150,0)');
      g.fillStyle = gr; g.fillRect(X - p.w / 2, Y - p.h / 2, p.w, p.h); g.restore(); }
    // height brackets beside three alifs
    [[2215, 205, 640], [1945, 215, 610], [1190, 215, 640]].forEach(([ix, top, bot], i) => { const q = ease(96.3 + i * .25, 96.9 + i * .25, t); if (q <= 0) return;
      const [x0, y0] = im(ix - 34, top), [, y1] = im(ix, bot), ym = (y0 + y1) / 2, hh = (y1 - y0) / 2 * q;
      line([[x0, ym - hh], [x0, ym + hh]], 1, { color: PAL.cream, width: 4 }); for (const yy of [ym - hh, ym + hh]) line([[x0 - 11, yy], [x0 + 11, yy]], 1, { color: PAL.cream, width: 4 });
      if (q > .95) { nuqta(g, x0, ym - hh, 12, PAL.cream); nuqta(g, x0, ym + hh, 12, PAL.cream); } });
    // the wide bowls traced
    [[2010, 545, 150, 85], [1500, 560, 170, 70], [720, 545, 190, 80]].forEach(([cx, cy, rx, ry], i) => { const q = ease(98.2 + i * .3, 99.0 + i * .3, t); if (q <= 0) return; const [x, y] = im(cx, cy);
      g.save(); g.strokeStyle = PAL.cream; g.lineWidth = 4.5; g.setLineDash([12, 8]); g.beginPath(); g.ellipse(x, y, rx * K * 1.1, ry * K * 1.25, 0, 0, Math.PI * q); g.stroke(); g.restore(); });
    camOff();
    drawCard(P.cTall, t, 96.4, 1560, 900, { rot: .015, t1: 97.95 });
    drawCard(P.cCurve, t, 98.15, 1560, 900, { rot: -.015 });
  } });

  // 23 · pliant composition: line · circle · square (100.16 – 103.44)
  SHOTS.push({ a: 100.16, b: 103.44, draw: (t) => {
    desk(t, 100.1, 103.6, .74);
    const items = [[P.compLine, 1420, 440, 100.3, 'line'], [P.compRound, 860, 440, 100.75, 'circle'], [P.compDense, 380, 440, 101.2, 'square']];
    items.forEach(([p, x, y, t0, sh], i) => { const r = dropP(p, t, t0, x, y, (i - 1) * .025, 40 + i); if (!r) return;
      const q = ease(t0 + .4, t0 + 1.0, t), iy = 740, ix = x, s = 40;
      if (sh === 'line') line([[ix + 90, iy], [ix - 90, iy]], q, { color: PAL.goldL, width: 6 });
      else if (sh === 'circle') arc(ix, iy, s, q, { color: PAL.goldL, width: 6 });
      else line([[ix - s, iy - s], [ix + s, iy - s], [ix + s, iy + s], [ix - s, iy + s]], q, { color: PAL.goldL, width: 6, closed: true }); });
    drawCard(P.cPliant, t, 101.4, 960, 890, { rot: .01 });
  } });

  // 24 · "but… do you know?" (103.44 – 107.16)
  SHOTS.push({ a: 103.44, b: 107.16, draw: (t) => {
    plate(A.pl_hand, t, 103.4, 107.3, { s0: 1.0, s1: 1.1, fx1: .58, fy1: .62, dim: .45 });
    rays(t, { x: 160, y: -300, ang: .95, int: .12 });
    nameBlock(P.cBut, t, 103.5, 1500, 260, 104.9);
    drawCard(P.cKnow, t, 104.95, 1420, 560, { rot: -.02 });
  } });

  // 25 · the harakat light up on a real panel (107.16 – 110.52)
  SHOTS.push({ a: 107.16, b: 110.52, draw: (t) => {
    desk(t, 107.1, 110.6, .72);
    const p = P.pline2, X = 960, Y = 450, K = p.w / 1900;
    const push = ease(107.2, 110.6, t); camOn(lerp(1.0, 1.1, push), lerp(960, 1080, push), lerp(540, 470, push));
    const k = sp(t, 107.25, 'card'), b = breathe(25, t, .3), x0 = X + b[0] - p.w / 2, y0 = Y - (1 - k) * 140 + b[1] - p.h / 2;
    drawP(p, X + b[0], Y - (1 - k) * 140 + b[1], { lift: 1 - k, alpha: clamp(k * 3) });
    if (t > 107.7) { const dim = ease(107.7, 108.2, t); g.save(); g.globalAlpha = .38 * dim; g.fillStyle = '#efe0bd'; g.fillRect(x0 + 20, y0 + 20, p.w - 40, p.h - 40); g.restore();
      PRAYER_MARKS.forEach((m, i) => { const q = spring(t - (107.8 + i * .055), 260, 16); if (q <= 0) return; const cx = x0 + (m[0] + m[2] / 2) * K, cy = y0 + (m[1] + m[3] / 2) * K, s = Math.max(0, lerp(1.8, 1, q));
        g.save(); g.translate(cx, cy); g.scale(s, s); g.drawImage(P.marksGold, m[0], m[1], m[2], m[3], -m[2] * K / 2, -m[3] * K / 2, m[2] * K, m[3] * K); g.restore(); }); }
    camOff();
    drawCard(P.cHarakat, t, 108.0, 520, 870, { rot: -.015 });
  } });

  // 26 · a different, smaller pen — a quarter of the width (110.52 – 119.52)
  SHOTS.push({ a: 110.52, b: 119.52, draw: (t) => {
    desk(t, 110.5, 119.6, .7);
    const b = breathe(26, t, .3); drawP(P.mat, 960 + b[0], 540 + b[1], { rot: -.006 });
    const N = A.v2_reed.height, Wd = A.v2_reed.width;
    const reed = (y, len, thick, t0, xr) => { const k = sp(t, t0, 'card'); if (k <= 0) return; const kk = len / N;
      g.save(); g.translate(xr + (1 - k) * 900, y); g.rotate(-Math.PI / 2 + (1 - k) * .05);
      g.globalAlpha = .4; g.drawImage(P.reed.sh, -thick / 2 - 30, -len / 2 + 12, P.reed.sh.width * thick / Wd, P.reed.sh.height * kk); g.globalAlpha = 1;
      g.drawImage(A.v2_reed, -thick / 2, -len / 2, thick, len); g.restore(); };
    // big reed (letters) and small reed (harakat); nib points left
    const bigT = Wd * 1300 / N * 1.0, smT = bigT * .42;
    const shift = ease(114.9, 115.6, t);                           // reeds move up to make room for the width diagram
    const yB = lerp(380, 260, shift), yS = lerp(600, 410, shift);
    reed(yB, 1300, bigT, 110.6, 1060); drawCard(P.tBig, t, 111.0, 1560, yB - 95, { rot: .02, t1: 115.0 });
    reed(yS, 900, smT, 112.5, 1260); drawCard(P.tSmall, t, 113.2, 1560, yS + 85, { rot: -.02, t1: 115.0 });
    drawCard(P.cNotSame, t, 110.9, 600, 820, { rot: -.015, t1: 114.9 });
    // nib-width diagram: one big square = four small ones
    const d = ease(115.1, 115.6, t);
    if (d > 0) { const U = 64, bx = 1080, by = 720;
      g.save(); g.globalAlpha = d; nuqta(g, bx, by, U * 4 * .72 * sp(t, 115.15, 'snap'), PAL.ink); g.restore();
      for (let i = 0; i < 4; i++) { const q = sp(t, 116.7 + i * .16, 'snap'); if (q > 0) nuqta(g, bx - 260, by - U * 1.5 + i * U, U * .72 * q, PAL.goldD); }
      const lq = ease(117.3, 117.9, t); const xL = bx - 330, xR = bx + U * 2.05;
      line([[xL, by - U * 2], [xL, by + U * 2]], lq, { color: PAL.goldD, width: 3 }); line([[xR, by - U * 2], [xR, by + U * 2]], lq, { color: PAL.goldD, width: 3 });
      line([[xL, by - U * 2], [xR, by - U * 2]], ease(117.6, 118.2, t), { color: PAL.goldD, width: 2.4, dash: [8, 6] });
      line([[xL, by + U * 2], [xR, by + U * 2]], ease(117.6, 118.2, t), { color: PAL.goldD, width: 2.4, dash: [8, 6] }); }
    drawCard(P.cQuarter, t, 116.75, 500, 730, { rot: .02 });
  } });

  // 27 · weave, balance, void & fill → al‑haml (119.52 – 131.46)
  SHOTS.push({ a: 119.52, b: 131.46, draw: (t) => {
    desk(t, 119.5, 131.6, .72);
    const p = P.pline3, X = 960, Y = 540, K = p.w / 1900;
    const push = ease(129.2, 130.4, t); camOn(lerp(1.0, 1.06, push), 960, 520);
    const k = sp(t, 119.6, 'card'), b = breathe(27, t, .3), x0 = X + b[0] - p.w / 2, y0 = Y - (1 - k) * 140 + b[1] - p.h / 2;
    drawP(p, X + b[0], Y - (1 - k) * 140 + b[1], { lift: 1 - k, alpha: clamp(k * 3) });
    const im = (ix, iy) => [x0 + ix * K, y0 + iy * K];
    // weave: gold threads linking each haraka to its neighbour
    const wv = ease(120.8, 122.0, t), wo = ease(125.2, 125.7, t);
    if (wv > 0 && wo < 1) { g.save(); g.globalAlpha = 1 - wo; for (let i = 1; i < PRAYER_MARKS.length; i++) { const a = PRAYER_MARKS[i - 1], c = PRAYER_MARKS[i], q = clamp(wv * PRAYER_MARKS.length - i + 1);
        if (q <= 0) continue; const [ax, ay] = im(a[0] + a[2] / 2, a[1] + a[3] / 2), [cx, cy] = im(c[0] + c[2] / 2, c[1] + c[3] / 2); if (Math.hypot(cx - ax, cy - ay) > 260) continue;
        line([[ax, ay], [lerp(ax, cx, .5), Math.min(ay, cy) - 18], [cx, cy]], q, { color: PAL.goldD, width: 3.2, alpha: .9 }); }
      PRAYER_MARKS.forEach(m => g.drawImage(P.marksGold, m[0], m[1], m[2], m[3], x0 + m[0] * K, y0 + m[1] * K, m[2] * K, m[3] * K)); g.restore(); }
    // balance: a gold scale settles above the panel
    const bs = sp(t, 122.85, 'card'), bo = ease(125.1, 125.5, t);
    if (bs > 0 && bo < 1) { g.save(); g.globalAlpha = clamp(bs * 2) * (1 - bo); const cx = 960, cy = 120, ang = .35 * Math.exp(-(t - 122.85) * 1.6) * Math.cos((t - 122.85) * 7);
      line([[cx, cy - 10], [cx - 30, cy + 50], [cx + 30, cy + 50]], 1, { color: PAL.cream, width: 4, closed: true });
      g.translate(cx, cy - 10); g.rotate(ang); line([[-300, 0], [300, 0]], 1, { color: PAL.cream, width: 5 });
      for (const sx of [-300, 300]) { g.save(); g.translate(sx, 0); g.rotate(-ang); line([[0, 0], [-44, 64]], 1, { color: PAL.cream, width: 3 }); line([[0, 0], [44, 64]], 1, { color: PAL.cream, width: 3 });
        g.strokeStyle = PAL.cream; g.lineWidth = 4; g.beginPath(); g.arc(0, 64, 48, 0, Math.PI); g.stroke(); nuqta(g, 0, 84, 22, PAL.goldL); g.restore(); }
      g.restore(); }
    // void & fill: grid; empty cells glow, then the harakat fill them
    const gq = ease(125.4, 126.2, t);
    if (gq > 0) { const cols = 12, rows = 3, gx0 = x0 + 60, gy0 = y0 + 50, cw = (p.w - 120) / cols, ch = (p.h - 100) / rows;
      g.save(); g.globalAlpha = .7 * (1 - ease(129.1, 129.6, t));
      for (let c = 0; c <= cols; c++) line([[gx0 + c * cw, gy0], [gx0 + c * cw, gy0 + rows * ch]], gq, { color: PAL.goldD, width: 2.4 });
      for (let r = 0; r <= rows; r++) line([[gx0, gy0 + r * ch], [gx0 + cols * cw, gy0 + r * ch]], gq, { color: PAL.goldD, width: 2.4 });
      const R = rng(55); for (let c = 0; c < cols; c++) for (let r = 0; r < 2; r++) { if (R() < .55) continue; const q = ease(126.4 + R() * .8, 126.9 + R() * .8, t) * (1 - ease(127.6, 128.2, t));
        if (q > 0) { g.fillStyle = `rgba(255,236,190,${.55 * q})`; g.fillRect(gx0 + c * cw + 3, gy0 + r * ch + 3, cw - 6, ch - 6); } }
      g.restore();
      const fq = ease(127.6, 128.9, t); if (fq > 0) PRAYER_MARKS.forEach((m, i) => { const q = spring(t - (127.6 + i * .04), 240, 16); if (q <= 0) return; const s = Math.max(0, lerp(1.6, 1, q));
        const cx = x0 + (m[0] + m[2] / 2) * K, cy = y0 + (m[1] + m[3] / 2) * K; g.save(); g.translate(cx, cy); g.scale(s, s); g.drawImage(P.marksGold, m[0], m[1], m[2], m[3], -m[2] * K / 2, -m[3] * K / 2, m[2] * K, m[3] * K); g.restore(); }); }
    camOff();
    if (t > 128.8) { g.save(); g.fillStyle = `rgba(10,7,4,${.55 * ease(128.8, 129.4, t)})`; g.fillRect(0, 0, W, H); g.restore(); }
    drawCard(P.cWeave, t, 120.9, 960, 900, { rot: -.01, t1: 122.6 });
    drawCard(P.cBal, t, 122.85, 960, 900, { rot: .01, t1: 125.15 });
    drawCard(P.cVoid, t, 125.4, 960, 900, { rot: -.01, t1: 129.1 });
    drawCard(P.cHaml, t, 128.95, 960, 540, { rot: -.015 });
  } });
})();
