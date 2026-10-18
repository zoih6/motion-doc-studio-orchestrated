// ════════════════════════════════════════════════════════════════════════════════════════════
//  KINETIC TYPE DEMO (10 s, 9:16, black stage) — template for lyric / quote / kinetic-text films.
//  Page: engine/kinetic.html   Doc: library/kinetic_type_motion.md   Engine: engine/type.js (KT)
//  Text (original): «الكلمة… حين تتحرّك، وتتنفّس، تسكن القلب… برفق، وتبقى»
//  Every beat = one MOTION PAIR (text + a partner shape) and the shape is always offset 2–6 frames.
// ════════════════════════════════════════════════════════════════════════════════════════════
(() => {
  const P = {}, F = KT.F, cx = W / 2;
  INITS.push(async () => {
    const hero = { font: 'Mirza', weight: 700, size: 230 }, sup = { font: 'Kufi', weight: 400, size: 82 };
    P.w1 = KT.word('الكلمة', hero);
    P.w2 = KT.word('حين', sup);
    P.w3 = KT.stretch('تتحرّك', Object.assign({}, hero, { size: 175 }), 3);                         // kashida variants → animated Arabic tracking
    P.w4 = KT.word('وتتنفّس', Object.assign({}, hero, { color: KT.ACC() }));
    P.w5 = KT.word('تسكن', Object.assign({}, hero, { size: 150 }));
    P.w6 = KT.word('القلب', Object.assign({}, hero, { size: 104, color: '#140a04' }));
    P.w7 = KT.word('برفق', Object.assign({}, hero, { size: 270 }));
    P.w8 = KT.word('وتبقى', Object.assign({}, sup, { size: 84, weight: 300 }));
  });

  SHOTS.push({ a: 0, b: 10, tin: 'cut', draw: (t) => {
    KT.stage();
    const push = 1 + .035 * KT.eInOut(t / 10);                   // slow camera breath on the whole stage
    KT.group(t, { x: cx, y: H / 2, sc: push }, () => { g.translate(-cx, -H / 2);

      // 1 · LEADER DOT → hero grows out of it (0.0 – 2.0)
      const y1 = 820, hand = KT.leader(t, .15, cx, y1, { r: 22, lead: .42 });
      // 2 · hanging word on a connector line, then the pair flips (rotateY) to the next word
      KT.group(t, { x: cx, y: y1, flip: { t0: 2.05, dur: .5 } }, (face) => {
        if (!face) {
          KT.show(P.w1, t, { x: 0, y: 0, t0: hand, in: 'grow', spring: 'pop', wiggle: { deg: 1.2, px: 1.5, f: .7 }, seed: 1 });
          KT.line(t, hand + .62, 0, 150, 0, 300, { width: 3, dur: .22 });                  // connector starts 4 f after the hero settles
          KT.show(P.w2, t, { x: 0, y: 372, t0: hand + .72, in: 'swing', angle: .55, fade: 6 });
        } else {
          // 3 · back face: the new word tracks in with kashida (Arabic letter-spacing done right)
          KT.show(P.w3, t, { x: 0, y: 40, t0: 2.3, in: 'none', keys: [[2.3, 0], [2.55, 3], [3.05, 1]], t1: 3.35, out: 'squash', outDur: .42 });
        }
      });

      // 4 · SQUASH → LINE → GROW: the old word collapses into a line, the new one grows out of it
      KT.line(t, 3.62, cx + 340, y1 + 40, cx - 340, y1 + 40, { width: 5, dur: .16, t1: 3.84, outDur: .14, color: KT.ACC() });
      const b4 = KT.show(P.w4, t, { x: cx, y: y1 + 40, t0: 3.72, in: 'unsquash', spring: 'pop', dimAt: 5.0, t1: 5.32, out: 'lift', outDur: .36 });
      // 5 · COMET: a dot lands above the accent word, then leads a trim-path arc around it
      const rx = P.w4.w / 2 + 70, ry = P.w4.size * .78;
      KT.dot(t, 4.0, cx, y1 + 40 - ry, 15, { t1: 4.16, outDur: .08 });
      KT.comet(t, 4.12, cx, y1 + 40, rx, ry, { a0: -Math.PI / 2, sweep: Math.PI * 1.55, dur: .78, tailLag: .3, width: 6, head: 15, dir: 1 });

      // 6 · HINGE: an accent line; a word slides out from behind it, the line tilts, a bubble answers
      const br = P.w6.w / 2 + 40, hx = 96 + br * 2 + 50, hy = 1060;      // row fits the 96 px safe margins
      KT.hinge(t, 5.28, hx, hy, 330, { keys: [[5.28, 0], [6.05, -.42]], width: 6, t1: 7.02, outDur: .22 });
      KT.show(P.w5, t, { x: hx + 26, y: hy - 10, ax: 0, t0: 5.42, in: 'fromLine', lineX: hx + 8, side: 'right', dur: .5, curve: 'expo', t1: 6.98, out: 'push', outDir: 'right', outDist: 180, outDur: .3 });
      KT.bubble(t, 6.1, hx - br - 60, hy + 40, br, { t1: 6.92, outDur: .28 });
      KT.show(P.w6, t, { x: hx - br - 60, y: hy + 40, t0: 6.18, in: 'pop', spring: 'pop', t1: 6.86, out: 'fade', outDur: .2 });

      // 7 · LIGHT STREAK carries us to the last line
      KT.streak(t, 6.92, { dur: .36, alpha: .5, width: 110, angle: .5, color: '255,214,170' });

      // 8 · BLUR-IN hero with echo ghosts, centre-out underline 4 f later, support rises, everything leaves offset
      const y8 = 880;
      KT.show(P.w7, t, { x: cx, y: y8, t0: 7.15, in: 'blur', dur: .55, curve: 'expo', echo: { n: 2, lag: 3, a: .28 }, drift: [0, -6], t1: 9.3, out: 'blur', outDur: .4 });
      KT.underline(t, 7.15 + F(14), cx, y8 + 225, P.w7.w * .8, { width: 6, dur: .4, t1: 9.18, outDur: .28 });
      KT.show(P.w8, t, { x: cx, y: y8 + 330, t0: 7.95, in: 'rise', dist: 40, fade: 12, drift: [0, -6], t1: 9.42, out: 'sink', outDur: .34 });
    });
  } });
})();
