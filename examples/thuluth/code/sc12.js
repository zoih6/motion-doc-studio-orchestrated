// ════════════════════════════════════════════════════════════════════
//  v3 · S1 (0 – 20.14) hook · S2 (20.14 – 32.64) the laws
// ════════════════════════════════════════════════════════════════════
(() => {
  const P = {};
  const STRIPS = [   // real manuscripts → the "hundreds of scripts"
    { k: 'v2_folio', f: 'assets/v2/birmingham.jpg', crop: [1080, 420, 880, 128], label: 'الحجازي' },
    { k: 'v2_kufic', f: 'assets/v2/kufic.jpg', crop: [120, 360, 2200, 320], label: 'الكوفي' },
    { k: 'v2_giant', f: 'assets/v2/giant.jpg', crop: [30, 560, 1700, 300], label: 'المحقَّق' },
    { k: 'v2_bawwab', f: 'assets/v2/bawwab.jpg', crop: [380, 1045, 1560, 227], label: 'النَّسخ' },
    { k: 'v3_prayer', f: 'assets/v3/prayer.jpg', crop: [420, 690, 1620, 236], label: 'الثُّلُث', hero: true },
  ];
  // the prayer line (real Ottoman thuluth) used as the "laws" blueprint; alif measured in crop px
  const PL = { w: 1900, h: 600, alif: { x: 1285, top: 100, bot: 480 }, base: 470, top: 104 };

  INITS.push(async () => {
    const L = (k, f) => loadImg(k, f);
    await Promise.all([L('pl_hand', 'assets/v3/plate_hand.jpg'), L('pl_desk', 'assets/v3/plate_desk.jpg'), L('pl_master', 'assets/v3/plate_master.jpg'),
      L('crown3', 'assets/v3/crown.png'), L('prayer_line', 'assets/v3/prayer_line.jpg'), ...STRIPS.map(s => L(s.k, s.f))]);
    P.crown = cutout(A.crown3, 18);
    const H1 = TYPE.h1;
    P.c1 = card([{ t: 'في عالَمِ', size: 76 }, { t: 'الحرفِ العربيّ', size: 104 }, { divider: 300, size: 30, color: PAL.gold }], { seed: 11, padX: 90 });
    P.strips = STRIPS.map((s, i) => ({ ...s, p: photo(A[s.k], 960, { crop: s.crop, seed: 40 + i, rough: 4, burn: .35 }),
      tag: card([{ t: s.label, size: 30, font: UI, weight: 700, color: s.hero ? PAL.ink : PAL.cream }], { seed: 60 + i, dark: !s.hero, padX: 44, padY: 26, rough: 3 }) }));
    P.c2 = card([{ t: 'عرفتِ البشريّةُ', size: 70, color: PAL.cream }, { t: 'مئاتِ الخطوط', size: 92, color: PAL.goldL }, { divider: 280, size: 26, color: PAL.gold }], { seed: 12, dark: true, padX: 80, padY: 50 });
    P.tLakin = textImg([{ t: 'لكنَّ', size: 110, color: PAL.goldL }, { t: 'التاجَ…', size: 130, color: PAL.cream }], { lh: 1.25 });
    P.tLam = [textImg([{ t: 'لم يُوضَعْ إلّا', size: 96, color: PAL.cream }]), textImg([{ t: 'على رأسِ خطٍّ', size: 96, color: PAL.cream }]), textImg([{ t: 'واحِد!', size: 150, color: PAL.goldL }])];
    P.sheet = paper({ w: 1180, h: 660, seed: 13, rough: 8, burn: .55 });
    P.sup = [card([{ t: 'أعظمُ', size: 88 }], { seed: 14, padX: 60, padY: 26 }), card([{ t: 'وأجملُ', size: 88 }], { seed: 15, padX: 60, padY: 26 }),
      card([{ t: 'وأصعبُ', size: 100, color: PAL.cream }], { seed: 16, dark: true, padX: 66, padY: 30 })];
    P.tYad = textImg([{ t: 'ما أبدعَتْه يدُ خطّاط', size: 50, color: PAL.cream, weight: 400 }]);
    P.prayer = photo(A.v3_prayer, 1640, { crop: [230, 470, 1940, 680], seed: 17, rough: 6, burn: .4, mul: .08 });
    P.c6 = card([{ t: 'ليسَ مجرّدَ', size: 70 }, { t: 'حروفٍ تُرسَم', size: 96 }], { seed: 18, padX: 80 });
    P.bp = photo(A.prayer_line, 1500, { seed: 19, rough: 7, burn: .45, res: 1.4 });
    P.c7 = card([{ t: 'بل هو دولةٌ', size: 74 }, { t: 'لها قوانينُها الصارمة', size: 74, color: PAL.ink }, { divider: 300, size: 26, color: PAL.gold }], { seed: 20, padX: 70 });
    P.c8 = card([{ t: 'ومَن لم يُطِقْ موازينَه…', size: 70, color: PAL.cream }], { seed: 21, dark: true, padX: 70 });
    P.c9 = card([{ t: 'فليسَ في عُرفِ أهلِ الصنعةِ', size: 62 }, { t: 'بخطّاط', size: 104, color: PAL.red }], { seed: 22, padX: 80 });
  });

  // 1 · hook: the hand and the reed (0 – 2.52)
  SHOTS.push({ a: 0, b: 2.52, tin: 'cut', draw: (t) => {
    plate(A.pl_hand, t, -0.3, 3.0, { s0: 1.16, s1: 1.04, fx0: .34, fy0: .62, fx1: .42, fy1: .52 });
    rays(t, { x: 120, y: -260, ang: .9, int: .15 });
    drawCard(P.c1, t, .3, 1340, 520, { rot: -.02 });
  } });

  // 2 · the hundreds of scripts (2.52 – 6.50): real manuscripts slide in like specimen strips
  SHOTS.push({ a: 2.52, b: 6.5, draw: (t) => {
    plate(A.pl_desk, t, 2.52, 6.6, { s0: 1.0, s1: 1.07, fx0: .5, fy0: .5, fx1: .46, fy1: .5, dim: .45 });
    rays(t, { x: 0, y: -300, ang: .85, int: .1 });
    const X = 660, Y0 = 190, DY = 172;
    P.strips.forEach((s, i) => { const k = sp(t, 2.62 + i * .32, 'card'); if (k <= 0) return; const y = Y0 + i * DY, b = breathe(i, t, .6);
      const x = X - (1 - k) * 900, r = (i % 2 ? .012 : -.01) + (1 - k) * -.06, hero = s.hero ? sp(t, 5.7, 'snap') : 0;
      drawP(s.p, x + b[0], y + b[1], { rot: r, sc: (s.p.w ? 1 : 1) * (1 + .05 * hero), lift: (1 - k) * .8 + hero * .5 });
      drawCard(s.tag, t, 2.85 + i * .32, x + 430 + b[0], y - 40 + b[1], { rot: .03, sc: 1, wdur: .3 }); });
    drawCard(P.c2, t, 3.2, 1530, 540, { rot: .015, from: 'drop' });
  } });

  // 3 · «لكنّ التاج» (6.50 – 12.96): dark paper splits open on the crown; then «لم يوضع إلا على رأس خط واحد»
  SHOTS.push({ a: 6.5, b: 12.96, draw: (t) => {
    g.fillStyle = '#120d08'; g.fillRect(0, 0, W, H);
    // the stage behind the paper: a warm pool of light
    const gr = g.createRadialGradient(1180, 560, 40, 1180, 560, 760); gr.addColorStop(0, 'rgba(120,82,40,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    rays(t, { x: 900, y: -320, ang: 1.45, n: 4, int: .14, spread: .6 });
    const move = ease(8.55, 9.6, t), cx = lerp(1010, 1260, move), cy = lerp(590, 560, move) + Math.sin(t * 1.2) * 6, cw = lerp(640, 820, move) * lerp(.92, 1, easeOut(6.6, 8.2, t));
    drawCut(P.crown, cx, cy, cw, { rot: Math.sin(t * .8) * .01 });
    // shine sweep across the crown
    { const k = ((t - 7.4) % 3.2) / 1.1; if (k > 0 && k < 1) { const kk = cw / P.crown.img.width, ch = P.crown.img.height * kk;
      const c = mk(cw, ch), x = c.getContext('2d'); x.drawImage(P.crown.img, 0, 0, cw, ch); x.globalCompositeOperation = 'source-in';
      const sg = x.createLinearGradient(lerp(-cw * .5, cw * 1.3, k), 0, lerp(-cw * .5, cw * 1.3, k) + cw * .25, ch * .4); sg.addColorStop(0, 'rgba(255,240,200,0)'); sg.addColorStop(.5, 'rgba(255,240,200,.55)'); sg.addColorStop(1, 'rgba(255,240,200,0)');
      x.fillStyle = sg; x.fillRect(0, 0, cw, ch); g.save(); g.globalCompositeOperation = 'screen'; g.drawImage(c, cx - cw / 2, cy - ch / 2); g.restore(); } }
    // the dark paper cracks open (two torn halves)
    const op = ease(6.62, 7.5, t);
    if (op < 1) { const r = rng(5); const edge = []; for (let y = -40; y <= H + 40; y += 24) edge.push([1010 + (r() - .5) * 70 + Math.sin(y * .01) * 40, y]);
      const half = (dir) => { g.save(); g.translate(dir * op * 1100, 0); g.rotate(dir * op * .05);
        g.beginPath(); if (dir < 0) { g.moveTo(-300, -60); edge.forEach(([x, y]) => g.lineTo(x, y)); g.lineTo(-300, H + 60); } else { g.moveTo(W + 300, -60); edge.forEach(([x, y]) => g.lineTo(x, y)); g.lineTo(W + 300, H + 60); }
        g.closePath(); g.save(); g.shadowColor = 'rgba(0,0,0,.8)'; g.shadowBlur = 40; g.fillStyle = '#17110b'; g.fill(); g.restore(); g.save(); g.clip(); g.globalAlpha = .55; g.drawImage(A.bg_dark, -200, -100, W + 400, H + 200); g.restore();
        g.strokeStyle = 'rgba(225,205,165,.5)'; g.lineWidth = 3; g.beginPath(); edge.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); g.restore(); };
      half(-1); half(1); }
    // text, left third
    const o1 = ease(8.45, 8.85, t);
    if (o1 < 1) writeOn(P.tLakin, 470 - o1 * 60, 540, easeOut(6.75, 7.9, t), { alpha: 1 - o1 });
    const xs = 520; [[8.97, 330], [10.78, 500], [12.0, 710]].forEach(([t0, y], i) => writeOn(P.tLam[i], xs + (i === 2 ? 30 : 0), y, easeOut(t0, t0 + .6, t)));
    if (t > 12.1) { const k = easeOut(12.2, 12.7, t); line([[xs - 230, 850], [xs + 230, 850]], k, { color: PAL.gold, width: 3 }); }
  } });

  // 4 · the hero word writes itself, the crown lands on it (12.96 – 20.14)
  SHOTS.push({ a: 12.96, b: 20.14, draw: (t) => {
    plate(A.pl_desk, t, 12.96, 20.2, { s0: 1.08, s1: 1.0, dim: .62 });
    rays(t, { x: 200, y: -300, ang: .9, int: .12 });
    const shift = ease(15.0, 15.9, t), sx = lerp(960, 700, shift), ss = lerp(1, .82, shift), b = breathe(3, t, .5);
    drawP(P.sheet, sx + b[0], 560 + b[1], { rot: -.01, sc: ss });
    g.save(); g.translate(sx + b[0], 560 + b[1]); g.rotate(-.01); g.scale(ss, ss);
    const hw = heroWord(t, 0, 40, 900, (t - 13.0) / 1.6, 14.75);
    g.restore();
    // crown descends onto the word
    const ck = sp(t, 14.3, 'card'), cw = 300 * ss;
    if (ck > 0) drawCut(P.crown, sx + 290 * ss, lerp(-300, 560 - 250 * ss, ck), cw, { rot: (1 - ck) * .3 - .06, lift: (1 - ck) });
    // superlatives stack in the right third
    const xr = 1500; [[15.7, 300], [16.3, 510], [16.98, 730]].forEach(([t0, y], i) => drawCard(P.sup[i], t, t0, xr, y, { rot: [-.02, .015, -.025][i], from: 'right' }));
    if (t > 17.0) { const k = easeOut(17.25, 17.7, t); line([[xr - 170, 835], [xr + 170, 835]], k, { color: PAL.red, width: 5 }); }
    writeOn(P.tYad, xr, 920, easeOut(18.1, 19.2, t));
  } });

  // 5 · «ليس مجرد حروف ترسم» (20.14 – 22.92): a real Ottoman thuluth panel glides past
  SHOTS.push({ a: 20.14, b: 22.92, draw: (t) => {
    plate(A.pl_desk, t, 20.1, 23, { s0: 1.0, s1: 1.04, dim: .7 });
    const k = ease(20.0, 23.2, t), b = breathe(5, t, .5);
    drawP(P.prayer, lerp(1060, 860, k) + b[0], 470 + b[1], { rot: -.015, sc: lerp(1.0, 1.06, k) });
    rays(t, { x: 300, y: -300, ang: .95, int: .1 });
    drawCard(P.c6, t, 20.35, 1420, 860, { rot: .02 });
  } });

  // 6 · the laws (22.92 – 28.94): construction lines on a real thuluth line, then the error
  SHOTS.push({ a: 22.92, b: 28.94, draw: (t) => {
    plate(A.pl_desk, t, 22.9, 29, { s0: 1.04, s1: 1.0, dim: .72 });
    const push = ease(26.3, 27.3, t), cs = lerp(1, 1.55, push);
    const bx = 860, by = 430, k = P.bp.w / PL.w, b = breathe(6, t, .4);
    const toS = (px, py) => [bx - P.bp.w / 2 + px * k, by - P.bp.h / 2 + py * k];
    const [afx, afy] = toS(PL.alif.x, (PL.alif.top + PL.alif.bot) / 2);
    camOn(cs, lerp(960, afx + 80, push), lerp(540, afy, push));
    drawP(P.bp, bx + b[0], by + b[1], { rot: 0 });
    // horizontal rules: baseline and the alif height
    const [x0, yb] = toS(0, PL.base), [x1] = toS(PL.w, 0), [, yt] = toS(0, PL.top);
    line([[x1 - 20, yb], [x0 + 20, yb]], ease(23.0, 23.8, t), { width: 3.2, color: PAL.goldD });
    line([[x1 - 20, yt], [x0 + 20, yt]], ease(23.3, 24.1, t), { width: 2.6, dash: [12, 8], color: PAL.goldD });
    // vertical guides at three alifs + the nuqta ladder on the hero alif
    [PL.alif.x, 862 + 28, 470].forEach((ax, i) => { const [gx] = toS(ax, 0); line([[gx, yt - 30], [gx, yb + 30]], ease(23.8 + i * .2, 24.4 + i * .2, t), { width: 2.4, dash: [8, 6], color: PAL.goldD }); });
    const n = 7, [lx] = toS(PL.alif.x - 48, 0), step = (yb - yt) / n;
    for (let i = 0; i < n; i++) { const kk = sp(t, 24.6 + i * .09, 'snap'); if (kk > 0) nuqta(g, lx, yb - step * (i + .5), step * .62 * kk, PAL.goldD, 0); }
    // angle arc at the bowl
    const [ax0, ay0] = toS(PL.alif.x - 420, PL.base - 60); arc(ax0, ay0, 70, ease(25.3, 26.0, t), { width: 3, dash: [6, 5], color: PAL.goldD });
    // error: a ghost alif, too short and tilted — red ring and cross
    const ek = sp(t, 27.45, 'snap');
    if (ek > 0) { const [ex, ey] = toS(PL.alif.x + 130, PL.top + 70); g.save(); g.globalAlpha = clamp(ek * 2) * .85; g.translate(ex, ey + 160); g.rotate(.22);
      g.fillStyle = 'rgba(168,50,31,.75)'; g.beginPath(); g.moveTo(-9, -230); g.lineTo(11, -230); g.lineTo(13, 120); g.lineTo(-13, 120); g.closePath(); g.fill(); g.restore();
      arc(ex + 20, ey + 140, 150, ease(27.6, 28.2, t), { color: PAL.red, width: 4 });
      if (t > 28.15) { const q = easeOut(28.15, 28.45, t); line([[ex - 70, ey + 70], [ex + 110, ey + 210]], q, { color: PAL.red, width: 6 }); line([[ex + 110, ey + 70], [ex - 70, ey + 210]], easeOut(28.3, 28.6, t), { color: PAL.red, width: 6 }); }
      // the correct alif gets a gold check
      const [cx2, cy2] = toS(PL.alif.x, PL.top - 40); line([[cx2 - 26, cy2], [cx2 - 6, cy2 + 22], [cx2 + 30, cy2 - 26]], easeOut(28.3, 28.7, t), { color: PAL.goldD, width: 6 }); }
    camOff();
    drawCard(P.c7, t, 23.1, 1420, 850, { rot: -.015, t1: 26.25 });
    drawCard(P.c8, t, 26.6, 1380, 900, { rot: .02 });
  } });

  // 7 · the master and the student (28.94 – 32.64)
  SHOTS.push({ a: 28.94, b: 32.64, draw: (t) => {
    plate(A.pl_master, t, 28.9, 32.8, { s0: 1.02, s1: 1.12, fx0: .5, fy0: .5, fx1: .4, fy1: .45 });
    rays(t, { x: 1200, y: -300, ang: 1.9, n: 4, int: .1 });
    drawCard(P.c9, t, 29.1, 1440, 840, { rot: -.015 });
  } });
})();
