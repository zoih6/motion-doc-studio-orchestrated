// ═══ D · 52.56–61.30 · the camera dives back to the pen → a pin (address) → the seal again (END CARD) + numbers ═══
(() => {
  const T = {};
  const D7 = { font: DISPLAY, weight: 700 }, U7 = { font: UI, weight: 700 };
  const SUN = [0, -16250];
  const PIN = [0, -17350], PS = 230;
  const EC = { y: -18750, seal: -19100, R: 200 };
  const N1 = EC.seal + 530, N2 = N1 + 130;                                    // number baselines
  INITS.push(async () => {
    T.zur = KT.word('زورونا في', { ...U7, size: 64, color: LP.mint });
    T.san = KT.word('صنعاء', { ...D7, size: 170, color: LP.gold });
    T.shr = KT.word('شارع الزبيري', { ...D7, size: 78, color: LP.cream });
    T.jwr = KT.word('جوار مستشفى سيبلاس', { ...U7, size: 60, color: LP.mint });
    T.tws = KT.word('تواصلوا معنا', { ...U7, size: 58, color: LP.mint });
    T.n1 = ltrWord('775 591 666', { size: 98, color: LP.cream });
    T.n2 = ltrWord('775 581 666', { size: 98, color: LP.cream });
    T.adr = KT.word('صنعاء · شارع الزبيري · جوار مستشفى سيبلاس', { ...U7, size: 38, color: LP.mint });
  });

  WORLD.build.push(() => {
    // pin (Lucide map-pin, drawn by the pen)
    LINE.icon('map-pin', PIN[0], PIN[1], PS, { dIn: [0, -1], c1: [SUN[0] + 420, SUN[1] - 300], c2: [PIN[0] + 380, PIN[1] + 260] }); LINE.mark('pinB');
    LINE.M.pinA = LINE.M.rayB + 1;                                               // approximate start for keys (connector included)
    LINE.key(52.30, 'rayB'); LINE.key(53.50, 'pinB', 'io');
    // the seal again — the end card
    const ring = SHAPES.circle(0, EC.seal, EC.R, 0, 1, 200, -1);
    LINE.add([ring], { dIn: [0, -1], c1: [PIN[0] + 420, PIN[1] - 240], c2: [EC.R + 240, EC.seal + 420] }); LINE.mark0('ecA'); LINE.mark('ecB');
    LINE.key(56.00, 'pinB'); LINE.key(56.45, 'ecA', 'io'); LINE.key(57.12, 'ecB', 'io');
    // the pen writes under each number (LTR)
    const w1 = 330;
    LINE.add([densify([[-w1, N1 + 62], [w1, N1 + 62]], 4)], { join: 'lift', liftWt: .02 }); LINE.M.u1A = LINE.S - w1 * 2; LINE.mark('u1B');
    LINE.add([densify([[-w1, N2 + 62], [w1, N2 + 62]], 4)], { join: 'lift', liftWt: .02 }); LINE.M.u2A = LINE.S - w1 * 2; LINE.mark('u2B');
    LINE.key(57.78, 'ecB'); LINE.key(57.86, 'u1A', 'io'); LINE.key(58.36, 'u1B', 'lin'); LINE.key(58.42, 'u2A', 'io'); LINE.key(58.92, 'u2B', 'lin');
  });
  window.PEN_OFF = 59.30;

  // ── camera: dive from the whole journey back to the pen ──
  LCAM.key(53.05, 0, -17500, .95, 0, true);
  LCAM.key(55.95, 0, -17525, .975, 0, true);
  LCAM.key(56.60, 0, EC.y, .95, 0);
  LCAM.key(61.30, 0, EC.y - 15, 1.0, 0);

  // ── sound ──
  cue.move('dive', when.ease(52.05, 53.05), { sound: 'whoosh/fs-449992-whoosh-short-low-wav-1' });
  cue.appear('pin', 53.50, { sound: 'pop/fs-253956-bubble-pop-1' });
  cue.hero('endcard', 57.30, { on: 'appear', sound: 'thump/fs-187136-body-fall-wav-1+chime/fs-185822-single-chime-1' });
  window.FLASH = (window.FLASH || []).concat([57.29]);

  INITS.push(async () => {
    const s = PS / 24, ox = PIN[0] - 12 * s, oy = PIN[1] - 12 * s;
    BLOOM.add({ t0: 53.48, dur: .3, cx: PIN[0], cy: PIN[1], r: PS, color: LP.gold, alpha: .95,
      shape: (c) => { c.moveTo(ox + 20 * s, oy + 10 * s); c.bezierCurveTo(ox + 20 * s, oy + 15 * s, ox + 14.5 * s, oy + 20.2 * s, ox + 12 * s, oy + 22 * s);
        c.bezierCurveTo(ox + 9.5 * s, oy + 20.2 * s, ox + 4 * s, oy + 15 * s, ox + 4 * s, oy + 10 * s); c.arc(ox + 12 * s, oy + 10 * s, 8 * s, Math.PI, 0); c.closePath(); } });
    BLOOM.add({ t0: 53.52, dur: .2, cx: PIN[0], cy: PIN[1] - 2 * s, r: 4 * s, color: '#063c36', alpha: 1, shape: (c) => c.arc(PIN[0], PIN[1] - 2 * s, 3.4 * s, 0, 7) });
    BLOOM.add({ t0: 56.95, dur: .45, cx: 0, cy: EC.seal, r: EC.R, color: LP.cream, alpha: 1, shape: (c) => c.arc(0, EC.seal, EC.R - 16, 0, 7) });
  });
  WORLD.under.push((t) => {
    // pin lands: a ripple under its tip
    const k = clamp((t - 53.55) / .8); if (k > 0 && k < 1) { const s = PS / 24; g.save(); g.strokeStyle = LP.gold; g.globalAlpha = (1 - k) * .7; g.lineWidth = 4 / LCAM.now.z;
      g.beginPath(); g.ellipse(PIN[0], PIN[1] + 10 * s, 20 + 160 * KT.eOut(k), (20 + 160 * KT.eOut(k)) * .32, 0, 0, 7); g.stroke(); g.restore(); }
    const ke = KT.spr(t - 57.10, 'pop'); if (ke > 0 && A.emblem) { const w = (EC.R - 16) * 2 * .8 * Math.max(0, ke), h = w * A.emblem.height / A.emblem.width;
      g.save(); g.translate(0, EC.seal + 3); g.rotate((1 - Math.min(1, ke)) * .25); g.drawImage(A.emblem, -w / 2, -h / 2, w, h); g.restore(); }
  });
  WORLD.over.push((t) => {
    wtext(T.zur, t, { wx: 0, wy: -17860, t0: 52.70, in: 'rise', dist: 26, t1: 56.15, out: 'sink', outDur: .3 });
    wtext(T.san, t, { wx: 0, wy: -17730, t0: 53.50, in: 'mask', t1: 56.18, out: 'sink', outDur: .3 });
    wtext(T.shr, t, { wx: 0, wy: -17135, t0: 54.04, in: 'mask', t1: 56.21, out: 'sink', outDur: .3 });
    wtext(T.jwr, t, { wx: 0, wy: -17035, t0: 54.96, in: 'rise', dist: 24, t1: 56.24, out: 'sink', outDur: .3 });
    if (A.wmark && t >= 57.29) { const k = KT.eOut((t - 57.29) / .3), c = LCAM.now, ww = 560 * c.z * lerp(1.08, 1, k), hh = ww * A.wmark.height / A.wmark.width, [x, y] = LCAM.w2s(0, EC.seal + EC.R + 88);
      g.save(); g.translate(x, y); g.rotate(c.r); g.drawImage(A.wmark, -ww / 2, -hh / 2, ww, hh); g.restore(); }
    wtext(T.tws, t, { wx: 0, wy: N1 - 112, t0: 56.80, in: 'rise', dist: 24 });
    const pk = (a, b) => clamp((LINE.head(t) - LINE.M[a]) / (LINE.M[b] - LINE.M[a]));
    wpenL(T.n1, t, { wx: 0, wy: N1 }, pk('u1A', 'u1B'));
    wpenL(T.n2, t, { wx: 0, wy: N2 }, pk('u2A', 'u2B'));
    wtext(T.adr, t, { wx: 0, wy: N2 + 150, t0: 59.05, in: 'rise', dist: 20 });
  });
})();
