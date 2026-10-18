// ════════════════════════════════════════════════════════════════════
//  v3 · S3 (32.64 – 48.64) Umayyad origin · S4 (48.64 – 67.34) Ibn Muqla & Ibn al-Bawwab
// ════════════════════════════════════════════════════════════════════
(() => {
  const P = {};
  const ALIF = { x: 689, top: 186, bot: 662 }, RDOT = { x: 644, y: 488, w: 57, h: 53 };   // baysunghur.jpg px
  const PCROP = [620, 0, 880, 1152];   // portrait crop
  INITS.push(async () => {
    const L = (k, f) => A[k] ? Promise.resolve() : loadImg(k, f);
    await Promise.all([L('pl_desk', 'assets/v3/plate_desk.jpg'), L('v2_folio', 'assets/v2/birmingham.jpg'), L('v2_giant', 'assets/v2/giant.jpg'), L('v2_kufic', 'assets/v2/kufic.jpg'),
      L('v2_bays', 'assets/v2/baysunghur.jpg'), L('v2_bawwab', 'assets/v2/bawwab.jpg'), L('v2_reed', 'assets/v2/qalam_side.png'), L('v2_dot', 'assets/v2/real_dot.png'), L('knife', 'assets/knife.png'),
      L('por_qutba', 'assets/v3/por_qutba.jpg'), L('por_muqla', 'assets/v3/por_muqla.jpg'), L('por_bawwab', 'assets/v3/por_bawwab.jpg'), L('compass3', 'assets/v3/compass.png'), L('crown3', 'assets/v3/crown.png')]);
    P.folio = photo(A.v2_folio, 1040, { seed: 301, rough: 7 });
    P.cEra = card([{ t: 'بدأتِ الحكايةُ', size: 52 }, { t: 'في العصرِ الأمويّ', size: 82 }, { divider: 280, size: 24, color: PAL.gold }, { t: '٤١ – ١٣٢ هـ', size: 30, font: UI, color: PAL.ink }], { seed: 302, padX: 70 });
    P.tagFolio = card([{ t: 'مصحف بالخط الحجازي · القرن الأول الهجري', size: 22, font: UI, weight: 600, color: PAL.cream }], { seed: 303, dark: true, padX: 36, padY: 22, rough: 3 });
    P.qutba = photo(A.por_qutba, 600, { crop: PCROP, seed: 304, rough: 9, burn: .7, mul: 0 });
    P.nQutba = textImg([{ t: 'قُطبةُ المحرِّر', size: 104, color: PAL.cream }, { divider: 300, size: 30, color: PAL.gold }, { t: 'خطّاطٌ أمويّ', size: 40, font: UI, weight: 600, color: PAL.goldL }]);
    P.giant = photo(A.v2_giant, 1000, { seed: 305, rough: 6 });
    P.tagTumar = card([{ t: 'خطُّ الطومار الكبير', size: 48, color: PAL.cream }], { seed: 306, dark: true, padX: 50, padY: 26 });
    P.mat = paper({ w: 1700, h: 520, seed: 307, rough: 8, burn: .6 });
    P.reed = cutout(A.v2_reed, 12); P.knife = cutout(A.knife, 8);
    P.tThird = card([{ t: 'ثُلُث', size: 84, color: PAL.cream }], { seed: 308, dark: true, padX: 50, padY: 22 });
    P.slip = paper({ w: 980, h: 470, seed: 309, rough: 8 });
    P.tName = textImg([{ t: 'ومن هنا جاء الاسم', size: 56, color: PAL.cream }]);
    P.kufic = photo(A.v2_kufic, 900, { seed: 310, rough: 6 });
    P.cAbb = card([{ t: 'وفي القرنِ الرابعِ', size: 70 }, { t: 'الهجريّ', size: 104 }, { divider: 260, size: 24, color: PAL.gold }, { t: 'العصر العباسي', size: 32, font: UI, color: PAL.ink }], { seed: 311, padX: 80 });
    P.tagKufic = card([{ t: 'مصحف بالخط الكوفي · القرن الثالث الهجري', size: 22, font: UI, weight: 600, color: PAL.cream }], { seed: 312, dark: true, padX: 36, padY: 22, rough: 3 });
    P.muqla = photo(A.por_muqla, 700, { crop: PCROP, seed: 313, rough: 10, burn: .7, mul: 0 });
    P.nMuqla = textImg([{ t: 'ابنُ مُقلة', size: 120, color: PAL.cream }, { divider: 320, size: 30, color: PAL.gold }, { t: 'وزيرُ الخلافةِ العباسية', size: 42, font: UI, weight: 600, color: PAL.goldL }, { t: '(ت ٣٢٨ هـ)', size: 34, font: UI, weight: 500, color: 'rgba(241,228,196,.75)' }]);
    P.tGenius = card([{ t: 'العبقريّ', size: 50, color: PAL.ink }], { seed: 314, padX: 46, padY: 20 });
    P.bays = photo(A.v2_bays, 1400, { seed: 315, rough: 6, res: 1.6 });
    P.ruler = paper({ w: 46, h: 300, seed: 316, rough: 2, burn: 0 });
    P.compass = cutout(A.compass3, 10);
    P.cGeo = card([{ t: 'أعظمُ منظومةٍ', size: 66 }, { t: 'للنِّسَبِ الهندسيّة', size: 66, color: PAL.ink }], { seed: 317, padX: 70 });
    P.tagUnit = card([{ t: 'النقطة = وحدة القياس', size: 28, font: UI, weight: 700, color: PAL.cream }], { seed: 318, dark: true, padX: 40, padY: 22, rough: 3 });
    P.bawwab = photo(A.por_bawwab, 660, { crop: PCROP, seed: 319, rough: 10, burn: .7, mul: 0 });
    P.nBaw = textImg([{ t: 'ثمّ جاءَ', size: 50, color: PAL.goldL, weight: 400 }, { t: 'ابنُ البوّاب', size: 116, color: PAL.cream }, { divider: 300, size: 30, color: PAL.gold }, { t: '(ت ٤١٣ هـ)', size: 34, font: UI, weight: 500, color: 'rgba(241,228,196,.75)' }]);
    P.page = photo(A.v2_bawwab, 560, { seed: 320, rough: 5 });
    P.cRef = card([{ t: 'ليُهذِّبَ هذا البناء', size: 64 }], { seed: 321, padX: 66 });
    P.tagPage = card([{ t: 'مصحف ابن البواب · ٣٩١ هـ', size: 22, font: UI, weight: 600, color: PAL.cream }], { seed: 322, dark: true, padX: 36, padY: 22, rough: 3 });
    P.slabs = ['النقطة', 'الألف', 'الدائرة', 'النِّسبة'].map((s, i) => ({ p: paper({ w: 900 - i * 150, h: 120, seed: 330 + i, rough: 5, burn: .6 }), t: textImg([{ t: s, size: 60, color: PAL.ink }]) }));
    P.cFound = card([{ t: 'ويُرسي قواعدَه', size: 70, color: PAL.cream }, { t: 'بعمقٍ أكبر', size: 92, color: PAL.goldL }], { seed: 323, dark: true, padX: 70 });
  });

  const desk = (t, a, b, dim = .62, s0 = 1.0, s1 = 1.05) => { plate(A.pl_desk, t, a, b, { s0, s1, dim }); rays(t, { x: 120, y: -320, ang: .92, int: .11 }); };
  const nameBlock = (img, t, t0, x, y, t1 = null) => { const k = easeOut(t0, t0 + .9, t), ko = t1 ? ease(t1, t1 + .4, t) : 0; if (ko < 1) writeOn(img, x, y - ko * 60, k, { alpha: 1 - ko }); };
  // faint gold construction behind portraits (the attachment's look)
  const geoHalo = (t, t0, cx, cy, R) => { const k = ease(t0, t0 + 1.6, t); if (k <= 0) return;
    arc(cx, cy, R, k, { width: 1.4, alpha: .5 }); arc(cx, cy, R * .62, k, { width: 1.2, alpha: .4, dir: 1 });
    line([[cx - R * 1.25, cy], [cx + R * 1.25, cy]], k, { width: 1.2, alpha: .45 }); line([[cx, cy - R * 1.2], [cx, cy + R * 1.2]], k, { width: 1.2, alpha: .45 });
    for (const [dx, dy] of [[R, 0], [-R, 0], [0, R], [0, -R]]) if (k > .8) nuqta(g, cx + dx, cy + dy, 10, PAL.gold); };

  // 8 · Umayyad era (32.64 – 36.78)
  SHOTS.push({ a: 32.64, b: 36.78, draw: (t) => {
    desk(t, 32.6, 36.9);
    const k = sp(t, 32.9, 'card'), b = breathe(8, t, .5);
    drawP(P.folio, 690 + b[0], 500 - (1 - k) * 140 + b[1], { rot: -.02 + (1 - k) * .08, lift: (1 - k), alpha: clamp(k * 3) });
    drawCard(P.tagFolio, t, 34.3, 760, 870, { rot: .015, wdur: .4 });
    drawCard(P.cEra, t, 33.3, 1520, 520, { rot: .02 });
  } });

  // 9 · Qutba al-Muharrir and the great Tumar (36.78 – 42.08)
  SHOTS.push({ a: 36.78, b: 42.08, draw: (t) => {
    desk(t, 36.7, 42.2, .72);
    geoHalo(t, 37.0, 1420, 520, 330);
    const k = sp(t, 36.9, 'card'), b = breathe(9, t, .5);
    drawP(P.qutba, 1420 + b[0], 540 - (1 - k) * 120 + b[1], { rot: .02 + (1 - k) * .06, lift: (1 - k), alpha: clamp(k * 3) });
    nameBlock(P.nQutba, t, 38.42, 600, 520, 40.05);
    // the Tumar unrolls right → left into the left two-thirds
    const u = ease(40.3, 41.3, t);
    if (u > 0) { const x0 = 600, hw = P.giant.w / 2 + 40, xr = x0 + hw, xl = lerp(xr, x0 - hw, u);
      g.save(); g.beginPath(); g.rect(xl, 0, xr - xl + 60, H); g.clip(); drawP(P.giant, x0, 470, { rot: -.012 }); g.restore();
      if (u < 1) { g.save(); g.fillStyle = '#6b4a2a'; g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 20; g.fillRect(xl - 18, 470 - P.giant.h / 2 - 20, 36, P.giant.h + 40); g.restore(); }
      drawCard(P.tagTumar, t, 40.8, 600, 830, { rot: -.02 });
      // derivation: Tumar → Qutba
      const ap = ease(41.25, 41.85, t); if (ap > 0) { const pts = []; for (let i = 0; i <= 30; i++) { const v = i / 30; pts.push([lerp(900, 1220, v), lerp(250, 300, v) - Math.sin(v * Math.PI) * 120]); }
        line(pts, ap, { color: PAL.goldL, width: 4 }); if (ap > .97) nuqta(g, 1222, 300, 22, PAL.goldL); }
    }
  } });

  // 10 · the reed is cut — a third of its width (42.08 – 48.64)
  SHOTS.push({ a: 42.08, b: 48.64, draw: (t) => {
    desk(t, 42.0, 48.7, .66, 1.04, 1.0);
    const push = ease(44.2, 45.2, t) * (1 - ease(46.3, 47.0, t)), cs = lerp(1, 1.28, push);
    camOn(cs, lerp(960, 900, push), lerp(540, 470, push));
    const b = breathe(10, t, .4); drawP(P.mat, 960 + b[0], 520 + b[1], { rot: .008 });
    // reed: horizontal, nib to the left
    const RL = 1400, k = RL / A.v2_reed.height, RX = 1000, RY = 470, tipX = RX - RL / 2, SL = 34, thick = A.v2_reed.width * k;
    const kin = sp(t, 42.15, 'card'), out = ease(46.4, 47.0, t);
    const drawReed = (r0, r1, dx = 0, dy = 0, rot = 0) => { g.save(); g.translate(RX + dx + out * 1500, RY + dy - (1 - kin) * 200); g.rotate(-Math.PI / 2 + rot + (1 - kin) * .08);
      g.globalAlpha = .45; g.drawImage(P.reed.sh, 0, r0, P.reed.sh.width, r1 - r0, -thick / 2 - 36 * k - 14, -RL / 2 + r0 * k - 8, P.reed.sh.width * k, (r1 - r0) * k);
      g.globalAlpha = 1; g.drawImage(A.v2_reed, 0, r0, A.v2_reed.width, r1 - r0, -thick / 2, -RL / 2 + r0 * k, thick, (r1 - r0) * k); g.restore(); };
    const N = A.v2_reed.height, CUT = 43.10;
    if (t < CUT) drawReed(0, N); else { drawReed(SL, N); const dt = t - CUT; if (dt < 1.2) { g.save(); const px = tipX + SL * k / 2;
      g.translate(px - 120 * dt, RY + 1000 * dt * dt + 40 * dt); g.rotate(-2.2 * dt); g.translate(-px, -RY); drawReed(0, SL); g.restore(); } }
    // knife slices the nib
    if (t > 42.3 && t < CUT + .8) { const kx = tipX + SL * k, u = (t - 42.35) / (CUT - 42.35);
      const y = u < 1 ? lerp(RY - 900, RY + 30, 1 - Math.pow(1 - clamp(u), 2.4)) : RY + 30 - (t - CUT) * 1500 * spring(t - CUT - .12, 200, 26);
      g.save(); g.translate(kx + (RY - y) * .5, y); g.rotate(-Math.PI / 2 + .45); drawCut(P.knife, 0, 0, 600, { ax: 0, ay: .5 }); g.restore(); }
    // thirds of the width, projected to the nib
    const mp = ease(44.45, 44.95, t), mo = ease(46.3, 46.6, t);
    if (mp > 0 && mo < 1) { g.save(); g.globalAlpha = 1 - mo; const bx = tipX + 980, y0 = RY - thick / 2 + 8, y1 = RY + thick / 2 - 8, Lh = y1 - y0;
      line([[bx, y0], [bx, y1]], mp, { color: PAL.ink, width: 3.4 }); for (const yy of [y0, y1]) line([[bx - 14, yy], [bx + 14, yy]], mp, { color: PAL.ink, width: 3.4 });
      for (let i = 1; i <= 2; i++) { const s = sp(t, 44.75 + i * .14, 'snap'); if (s > 0) nuqta(g, bx, y0 + Lh * i / 3, 18 * s, PAL.goldD); }
      const th = sp(t, 45.42, 'snap'); if (th > 0) { line([[bx, y0 + Lh / 3], [bx, y0 + 2 * Lh / 3]], 1, { color: PAL.goldD, width: 12 * th });
        const gp = ease(45.5, 46.0, t); line([[bx, y0 + Lh / 3], [tipX + SL * k + 6, RY - Lh / 6]], gp, { color: PAL.goldD, width: 2.4, dash: [9, 8] });
        line([[bx, y0 + 2 * Lh / 3], [tipX + SL * k + 6, RY + Lh / 6]], gp, { color: PAL.goldD, width: 2.4, dash: [9, 8] }); }
      g.restore(); drawCard(P.tThird, t, 45.45, bx - 260, RY - 170, { rot: -.04, t1: 46.3 }); }
    camOff();
    // the name: a slip drops, the word writes itself
    const ks = sp(t, 46.6, 'card');
    if (ks > 0) { const b2 = breathe(11, t, .5), sy = 560 - (1 - ks) * 160; drawP(P.slip, 960 + b2[0], sy + b2[1], { rot: -.01 + (1 - ks) * .06, lift: 1 - ks, alpha: clamp(ks * 3) });
      g.save(); g.translate(960 + b2[0], sy + b2[1]); g.rotate(-.01); heroWord(t, 0, 10, 780, (t - 46.95) / 1.3, 48.3); g.restore();
      writeOn(P.tName, 960, 170, easeOut(46.8, 47.6, t)); }
  } });

  // 11 · the 4th century AH (48.64 – 51.08)
  SHOTS.push({ a: 48.64, b: 51.08, draw: (t) => {
    desk(t, 48.6, 51.2);
    const k = sp(t, 48.85, 'card'), b = breathe(12, t, .5);
    drawP(P.kufic, 660 + b[0], 500 - (1 - k) * 140 + b[1], { rot: .02 - (1 - k) * .08, lift: 1 - k, alpha: clamp(k * 3) });
    drawCard(P.tagKufic, t, 49.9, 700, 860, { rot: -.015, wdur: .4 });
    drawCard(P.cAbb, t, 49.2, 1500, 520, { rot: -.02 });
  } });

  // 12 · Ibn Muqla (51.08 – 55.34)
  SHOTS.push({ a: 51.08, b: 55.34, draw: (t) => {
    desk(t, 51.0, 55.5, .76, 1.06, 1.0);
    geoHalo(t, 51.3, 1380, 520, 380);
    const k = sp(t, 51.2, 'card'), b = breathe(13, t, .5), push = ease(51.1, 55.4, t);
    drawP(P.muqla, 1380 + b[0], 540 - (1 - k) * 120 + b[1], { rot: -.015 + (1 - k) * .05, sc: lerp(1, 1.04, push), lift: 1 - k, alpha: clamp(k * 3) });
    nameBlock(P.nMuqla, t, 52.16, 560, 520);
    drawCard(P.tGenius, t, 53.52, 1660, 210, { rot: .08, from: 'drop' });
  } });

  // 13 · the geometric system on a real alif (55.34 – 60.12)
  SHOTS.push({ a: 55.34, b: 60.12, draw: (t) => {
    desk(t, 55.3, 60.2, .74);
    const CX = 820, CY = 470, KC = P.bays.w / 2000, imL = (ix, iy) => [CX - P.bays.w / 2 + ix * KC, CY - P.bays.h / 2 + iy * KC];
    const [ax, ay] = imL(ALIF.x, (ALIF.top + ALIF.bot) / 2), R = (ALIF.bot - ALIF.top) / 2 * KC;
    const push = ease(56.1, 57.0, t) * (1 - ease(58.9, 59.7, t) * .6), cs = lerp(1, 1.7, push);
    camOn(cs, lerp(960, ax + 60, push), lerp(540, ay, push));
    const k = sp(t, 55.4, 'card'), b = breathe(14, t, .3);
    drawP(P.bays, CX + b[0], CY - (1 - k) * 140 + b[1], { lift: 1 - k, alpha: clamp(k * 3) });
    // 1) the manuscript's own nuqta lifts off …
    const [dx, dy] = imL(RDOT.x, RDOT.y), dw = RDOT.w * KC, dh = RDOT.h * KC, lift = sp(t, 55.9, 'snap'), fly = sp(t, 56.5, 'card');
    const [rx, ry0] = imL(ALIF.x - 64, ALIF.top), [, ry1] = imL(ALIF.x - 64, ALIF.bot), rh = ry1 - ry0;
    if (lift > 0) { arc(dx, dy, 34, ease(55.95, 56.35, t) * (1 - ease(56.5, 56.8, t)), { color: PAL.goldD, width: 2.5 });
      const kr = sp(t, 56.35, 'snap'); if (kr > 0) { g.save(); g.translate(rx, ry0 + rh / 2); g.scale(1, (rh + 24) / P.ruler.h * kr); drawP(P.ruler, 0, 0); g.restore(); }
      const n = 11, step = rh / n;   // 2) … its copies stack up the alif: the unit of measure
      for (let i = 0; i < n; i++) { const q = spring(t - (56.62 + i * .085), 300, 20); if (q <= 0) continue; const ty = ry1 - step * (i + .5), sc = lerp(1.25, step / dh * 1.02, q);
        g.drawImage(A.v2_dot, lerp(dx, rx, q) - dw * sc / 2, lerp(dy - 30 * lift, ty, q) - dh * sc / 2, dw * sc, dh * sc); }
      if (fly < .98) { g.globalAlpha = 1 - fly; const sc = 1 + .25 * lift; g.drawImage(A.v2_dot, dx - dw * sc / 2, dy - 30 * lift - dh * sc / 2, dw * sc, dh * sc); g.globalAlpha = 1; } }
    // 3) the circle whose diameter is the alif — drawn by a brass compass
    const cp = ease(57.1, 58.1, t);
    if (cp > 0) { arc(ax, ay, R, cp, { color: PAL.goldD, width: 4.5 });
      if (cp < 1) { const a1 = -Math.PI / 2 - cp * Math.PI * 2, px = ax + Math.cos(a1) * R, py = ay + Math.sin(a1) * R;
        g.save(); g.translate(ax, ay); g.rotate(Math.atan2(py - ay, px - ax)); drawCut(P.compass, 0, 0, R * 1.18 / .9, { ax: .06, ay: .5, shA: .4 }); g.restore(); } }
    // 4) construction: diameter, inscribed rhombus (the nuqta again), half circles
    const gp = (i) => ease(58.38 + i * .2, 58.88 + i * .2, t);
    line([[ax - R, ay], [ax + R, ay]], gp(0), { color: PAL.goldD, width: 3, dash: [10, 7] });
    line([[ax, ay - R], [ax + R, ay], [ax, ay + R], [ax - R, ay]], gp(1), { color: PAL.goldD, width: 3.6, closed: true });
    for (const oy of [-R / 2, R / 2]) arc(ax, ay + oy, R / 2, gp(2), { color: PAL.goldD, width: 2.6, dash: [7, 6] });
    camOff();
    drawCard(P.tagUnit, t, 57.4, 420, 880, { rot: -.02 });
    drawCard(P.cGeo, t, 58.4, 1460, 860, { rot: .015 });
  } });

  // 14 · Ibn al-Bawwab refines the building (60.12 – 64.22)
  SHOTS.push({ a: 60.12, b: 64.22, draw: (t) => {
    desk(t, 60.1, 64.3, .76);
    geoHalo(t, 60.3, 1400, 520, 360);
    const k = sp(t, 60.25, 'card'), b = breathe(15, t, .5);
    drawP(P.bawwab, 1400 + b[0], 540 - (1 - k) * 120 + b[1], { rot: .015 + (1 - k) * .05, lift: 1 - k, alpha: clamp(k * 3) });
    nameBlock(P.nBaw, t, 60.5, 580, 500, 62.2);
    // his own Qur'an page, read through a loupe
    const kp = sp(t, 62.3, 'card');
    if (kp > 0) { const x = 600, y = 500 - (1 - kp) * 140, rot = -.03 + (1 - kp) * .07; drawP(P.page, x, y, { rot, lift: 1 - kp, alpha: clamp(kp * 3) });
      const lp = ease(62.7, 64.3, t), w = P.page.w, h = P.page.h, lx = lerp(w * .25, -w * .22, lp), ly = lerp(-h * .02, h * .08, lp) + Math.sin(lp * 6) * 6, r = 120, Z = 2.4, sc = sp(t, 62.6, 'snap');
      if (sc > 0) { g.save(); g.translate(x, y); g.rotate(rot); g.translate(lx, ly); g.scale(sc, sc);
        g.save(); g.globalAlpha = .5; g.filter = 'blur(10px)'; g.fillStyle = '#000'; g.beginPath(); g.arc(14, 20, r + 14, 0, 6.283); g.fill(); g.restore();
        g.save(); g.beginPath(); g.arc(0, 0, r, 0, 6.283); g.clip(); g.scale(Z, Z); g.translate(-lx, -ly); g.drawImage(A.v2_bawwab, -w / 2, -h / 2, w, h); g.restore();
        g.lineWidth = 13; g.strokeStyle = '#a8823c'; g.beginPath(); g.arc(0, 0, r + 5, 0, 6.283); g.stroke(); g.lineWidth = 2; g.strokeStyle = 'rgba(255,240,200,.7)'; g.beginPath(); g.arc(0, 0, r - 3, -2.6, -1.3); g.stroke();
        g.save(); g.rotate(.8); g.fillStyle = '#3b2716'; g.fillRect(r + 10, -12, 140, 24); g.fillStyle = '#a8823c'; g.fillRect(r + 5, -15, 18, 30); g.restore(); g.restore(); }
      drawCard(P.tagPage, t, 62.9, x + 20, y + h / 2 + 40, { rot: .02, wdur: .4 }); }
    drawCard(P.cRef, t, 62.5, 1420, 900, { rot: -.015 });
  } });

  // 15 · foundations laid deeper (64.22 – 67.34)
  SHOTS.push({ a: 64.22, b: 67.34, draw: (t) => {
    desk(t, 64.2, 67.5, .78);
    const sink = ease(64.4, 67.4, t); camOn(lerp(1.0, 1.06, sink), 760, lerp(520, 600, sink));
    const base = 900;
    P.slabs.forEach((s, i) => { const k = sp(t, 64.35 + i * .45, 'card'); if (k <= 0) return; const y = base - i * 122, b = breathe(20 + i, t, .4);
      drawP(s.p, 700 + b[0], y - (1 - k) * 260 + b[1], { rot: (i % 2 ? .01 : -.01) + (1 - k) * .06, lift: 1 - k, alpha: clamp(k * 3) });
      g.save(); g.translate(700 + b[0], y - (1 - k) * 260 + b[1]); writeOn(s.t, 60, 0, easeOut(64.5 + i * .45, 64.9 + i * .45, t)); g.restore();
      // icon of each rule
      const ix = 700 - (s.p.w / 2) + 90, iy = y - (1 - k) * 260;
      if (i === 0) nuqta(g, ix, iy, 34 * k, PAL.ink); else if (i === 1) { g.fillStyle = PAL.ink; g.fillRect(ix - 6, iy - 38 * k, 12, 76 * k); }
      else if (i === 2) arc(ix, iy, 34 * k, 1, { color: PAL.ink, width: 4 }); else { line([[ix - 40, iy + 30], [ix + 40, iy - 30]], k, { color: PAL.ink, width: 4 }); nuqta(g, ix - 40, iy + 30, 14, PAL.ink); nuqta(g, ix + 40, iy - 30, 14, PAL.ink); } });
    // gold plumb line binding the layers
    line([[700, base + 90], [700, base - 3 * 122 - 100]], ease(66.0, 66.8, t), { color: PAL.goldL, width: 2.5, dash: [10, 8] });
    camOff();
    drawCard(P.cFound, t, 64.6, 1480, 540, { rot: .02 });
  } });
})();
