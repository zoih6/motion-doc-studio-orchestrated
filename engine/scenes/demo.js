// ════════════════════════════════════════════════════════════════════
//  DEMO film (16 s) — proves the pipeline end-to-end with zero external assets.
//  Copy this file as the template for every scene file: one IIFE, private P{},
//  INITS.push(async loader), SHOTS.push({a,b,draw}). Times = VO seconds.
// ════════════════════════════════════════════════════════════════════
(() => {
  const P = {};
  INITS.push(async () => {
    // pre-render every card/text ONCE here (never inside draw → speed + determinism)
    P.title = card([{ t: 'كيف تصنع', size: 78 }, { t: 'فيلمًا وثائقيًا', size: 124 }, { divider: 300, size: 26, color: PAL.gold }], { seed: 1, padX: 90 });
    P.kicker = card([{ t: 'الحلقة الأولى', size: 30, font: UI, color: PAL.cream }], { seed: 2, dark: true, padX: 44, padY: 26, rough: 3 });
    P.sheet = paper({ w: 1180, h: 620, seed: 3, rough: 8 });
    P.word = textImg([{ t: 'القاعدة', size: 200, color: PAL.ink }]);
    P.wordCap = card([{ t: 'كل شيء يُقاس', size: 56, color: PAL.cream }], { seed: 4, dark: true, padX: 60 });
    P.facts = ['الصوت أولًا', 'فكرة كل ٣ ثوانٍ', 'عنصر بطل واحد'].map((s, i) => card([{ t: s, size: 58 }], { seed: 10 + i, padX: 60, padY: 30 }));
        P.end = textImg([{ t: 'ابدأ الآن', size: 210, color: '#fff' }]);
    P.endGold = goldify(P.end);
  });

  // 1 · hook (0 – 4): card lands on a lit desk, kicker tag, gold construction halo
  SHOTS.push({ a: 0, b: 4, tin: 'cut', draw: (t) => {
    set(null, t, 0, 4.2, { dim: .3 });
    geoHalo(t, .2, 1340, 520, 330);
    drawCard(P.title, t, .25, 1340, 520, { rot: -.02 });
    drawCard(P.kicker, t, .9, 1340, 240, { rot: .03, wdur: .3 });
  } });

  // 2 · the rule (4 – 8): torn-in parchment, the word writes on RTL, a dot ruler measures it
  SHOTS.push({ a: 4, b: 8, draw: (t) => {
    set(null, t, 4, 8.2, { dim: .5 });
    const push = ease(4, 8.2, t); camOn(lerp(1, 1.06, push), 960, 520);
    const r = dropP(P.sheet, t, 4.1, 960, 500, -.01, 5);
    if (r) { g.save(); g.translate(r.X, r.Y); g.rotate(r.R); writeOn(P.word, 80, 0, easeOut(4.5, 5.6, t)); g.restore();
      for (let i = 0; i < 7; i++) { const s = sp(t, 5.8 + i * .09, 'snap'); if (s > 0) nuqta(g, r.X - 450, r.Y - 150 + i * 48, 34 * s, PAL.red); }
      line([[r.X - 380, r.Y + 175], [r.X + 470, r.Y + 175]], ease(6.4, 7.0, t), { color: PAL.goldD, width: 3.5 }); }
    camOff();
    drawCard(P.wordCap, t, 6.6, 960, 920, { rot: .01 });
  } });

  // 3 · the list (8 – 12): three facts stagger in from the right (RTL), one per beat
  SHOTS.push({ a: 8, b: 12, draw: (t) => {
    set(null, t, 8, 12.2, { dim: .55 });
        P.facts.forEach((f, i) => drawCard(f, t, 8.9 + i * .9, 1480 - i * 520, 620 + (i % 2) * 50, { rot: (i - 1) * .02, from: 'right' }));
    liveText(counter(t, 8.3, 10.7, 0, 3) + ' قواعد', 960, 300, 96, { color: PAL.goldL, alpha: clamp((t - 8.2) * 4) });
  } });

  // 4 · end card (12 – 16): gold word, rays, slow push
  SHOTS.push({ a: 12, b: 16, draw: (t) => {
    set(null, t, 12, 16.2, { dim: .7, ray: { x: 960, y: -300, ang: 1.57, n: 6, int: .16, spread: .8 } });
    const k = sp(t, 12.4, 'card'), s = lerp(1.15, 1, k);   // hero = decisive stop (a 'soft' settle is too gradual to land a sound on: QA r2)
    g.save(); g.globalAlpha = clamp(k * 2); g.translate(960, 540); g.scale(s, s); g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 24; g.shadowOffsetY = 10;
    g.drawImage(P.endGold, -P.endGold.width / 2, -P.endGold.height / 2); g.restore();
    geoHalo(t, 12.8, 960, 540, 380);
  } });
})();

// ── SOUND LAYER cues (engine/cues.js) ─────────────────────────────────────────
// Same t0 values and springs/easings as the draw() calls above, so the cue frames are computed,
// never typed. Export: PAGE=index.html node ../tools/export_cues.mjs  → audio/cues.json
// Real actions only. Tags: cut · move (peak speed) · land (motion stops) · appear (pops in).
if (typeof cue !== 'undefined') {
  const pan = (x) => +(x / 960 - 1).toFixed(2);                       // screen x → stereo position
  cue.hero('title', when.spring(.25, 'card'), { stop_before: false, build: false, pan: pan(1340) }); // hook: no music to stop yet
  cue.land('kicker', when.spring(.9, 'card'), { sound: 'tap', pan: pan(1340) });
  cue.move('tear-rule', when.ease(4, 4 + TEAR), { sound: 'paper/fs-140463-packaging-paper-rub-sliding-1' }); // QA r1: page-turn masked here (1.1 dB)                   // RTL paper tear = the transition
  [0, 3].forEach((i, n) => cue.appear('dot-' + i, when.spring(5.8 + i * .09, 'snap'), { sound: 'pop', pitch: n * 2, pan: pan(960 - 450) })); // QA r1: 3rd pop masked → 2 pops
  cue.appear('caption', when.spring(6.6, 'card'), { sound: 'tap/fs-369710-wood-knock' }); // camera push never 'stops' in shot 2 → appear
  cue.move('tear-list', when.ease(8, 8 + TEAR), { sound: 'paper/fs-397550-page-turn-03-wav-2' });
  [0, 1, 2].forEach((i) => cue.move('fact-' + i, when.spring(8.9 + i * .9, 'card'), { sound: 'swish', pan: pan(1480 - i * 520) }));
  cue.move('tear-end', when.ease(12, 12 + TEAR), { sound: 'paper/fs-397550-page-turn-03-wav-2' });
  const end = cue.hero('end', when.spring(12.4, 'card'), { sound: 'thump/fs-133282-thump-on-carpet-2+tap' }); // thump+tap; deeper thump (QA: body 2.7 → 3.0 dB with thump-close), stop_before, build
  cue.raw('end-rise', end.frame, { sound: 'riser', align: 'peak' });                  // a riser peaking on the hero frame
}
