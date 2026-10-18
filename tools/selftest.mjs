// Smoke-test the engine + every resource pack inside the real film page (no rendering to video).
//   node tools/selftest.mjs        (run from repo root)  → exit 1 on any failure
import { chromium } from 'playwright';
import { resolve } from 'node:path'; import { pathToFileURL } from 'node:url';
const b = await chromium.launch({ args: ['--allow-file-access-from-files', ...(process.env.RENDER_GL === 'swiftshader' ? ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] : [])] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
p.on('pageerror', e => errs.push('pageerror ' + e.message));
await p.goto(pathToFileURL(resolve('engine/index.html')).href);
await p.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
const r = await p.evaluate(async () => {
  const out = { fail: [] }, F = (k, e) => out.fail.push(k + ': ' + (e && e.message || e));
  out.counts = { fonts: FONT_REGISTRY.length, palettes: NICE_PALETTES.length, icons: Object.keys(LUCIDE).length, gl: GLT.list().length, moves: Object.keys(MOVES).length, trans: Object.keys(TRANS).length, patterns: PATTERN_KINDS.length, heritage: Object.keys(HERITAGE).length };
  // fonts actually load
  for (const f of FONT_REGISTRY) { const w = f.weights[0].split(' ').pop(); try { await document.fonts.load(`${w} 40px "${f.family}"`, 'أب'); if (!document.fonts.check(`${w} 40px "${f.family}"`, 'أب')) F('font ' + f.family, 'not loaded'); } catch (e) { F('font ' + f.family, e); } }
  // every move at several progress values
  const box = { x: 960, y: 540, w: 300, h: 120 };
  for (const n of Object.keys(MOVES)) for (const t of [0, .1, .4, .8, 1.2, 3]) { try { move(n, t, 0, box, () => { g.fillRect(-150, -60, 300, 120); }); } catch (e) { F('move ' + n, e); } }
  try { seqMove([['dropIn', 0], ['tada', 1], ['fadeOutUp', 2.5]], 1.5, box, () => {}); staggerMove('fadeInRight', 1, 0, [box, { ...box, x: 500 }], () => {}, { order: 'rtl' }); } catch (e) { F('seq/stagger', e); }
  // icons, patterns, palettes
  for (const n of Object.keys(LUCIDE)) { try { iconPath(n); } catch (e) { F('icon ' + n, e); } }
  try { icon('landmark', 960, 540, 200, { k: .5 }); if (!iconSearch('time').length) F('iconSearch', 'empty'); } catch (e) { F('icon draw', e); }
  for (const k of PATTERN_KINDS) { try { pattern(k, 1.3, { x: 0, y: 0, w: 400, h: 300, k: .7 }); } catch (e) { F('pattern ' + k, e); } }
  try { const roles = paletteRoles(palette(7)); if (!roles.bg || !roles.accent) F('paletteRoles', JSON.stringify(roles)); out.darkPalettes = palettesBy({ dark: true }).length; heritage('mamlukGold'); oc('teal', 6); } catch (e) { F('palettes', e); }
  // every TRANS key (canvas + GL) at mid progress, inside a real render
  const s1 = SHOTS[1], keep = [s1.tin, s1.tdur];
  for (const k of Object.keys(TRANS)) { try { s1.tin = k; s1.tdur = 1; render(s1.a + .5); } catch (e) { F('trans ' + k, e); } }
  [s1.tin, s1.tdur] = keep; render(1.5);
  const d = g.getImageData(960, 540, 1, 1).data; out.pixel = [...d];
  // SOUND LAYER cue registry (engine/cues.js): demo cues + timing math
  try {
    out.counts.cues = CUES.length; if (!CUES.length) F('cues', 'demo registered no cues');
    const ids = new Set(); for (const c of CUES) { if (ids.has(c.id)) F('cue id', c.id); ids.add(c.id); if (!c.sound) F('cue sound', c.id); }
    for (const k of ['card', 'snap', 'soft']) { const w = when.spring(2, k); if (!(w.start <= w.peak && w.peak < w.land)) F('when.spring ' + k, JSON.stringify(w)); }
    const e = when.ease(1, 2); if (e.peak !== 45) F('when.ease peak', e.peak + ' != 45 (mid of 30..60)');
    const pth = when.path((t) => [t * 100, 0], 0, 1); if (!(pth.peak >= 0)) F('when.path', JSON.stringify(pth));
    if (!CUES.some((c) => c.weight === 'hero')) F('cues', 'no hero in demo');
  } catch (e) { F('cues.js', e); }
  return out; });
// KINETIC TYPE layer (engine/type.js) inside the 9:16 kinetic page: every entrance/exit/partner + kashida rules
const p2 = await b.newPage(); p2.on('pageerror', e => errs.push('kinetic pageerror ' + e.message));
await p2.goto(pathToFileURL(resolve('engine/kinetic.html')).href);
await p2.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
const k = await p2.evaluate(() => {
  const fail = [], F = (k, e) => fail.push(k + ': ' + (e && e.message || e));
  const Wd = KT.word('تجربة', { size: 120 }), V = KT.stretch('تتحرّك', { size: 100 }, 3);
  for (const n of Object.keys(KT.IN)) for (const t of [0, .05, .2, .5, 1, 2]) { try { KT.show(Wd, t, { x: 540, y: 900, t0: .1, in: n, t1: 1.5, out: 'fade' }); } catch (e) { F('in ' + n, e); } }
  for (const n of Object.keys(KT.OUT)) for (const t of [1.4, 1.55, 1.7, 2.5]) { try { KT.show(Wd, t, { x: 540, y: 900, t0: 0, in: 'rise', t1: 1.5, out: n }); } catch (e) { F('out ' + n, e); } }
  try { KT.show(V, 1, { x: 540, y: 900, t0: 0, in: 'none', keys: [[0, 0], [.5, 3]], echo: { n: 2 }, wiggle: {}, drift: [0, -5], chroma: 4, dimAt: .5 }); } catch (e) { F('show options', e); }
  try { const t = .5; KT.leader(t, 0, 540, 900); KT.dot(t, 0, 1, 1); KT.comet(t, 0, 540, 900, 300, 150); KT.ring(t, 0, 540, 900, 100); KT.underline(t, 0, 540, 900, 300); KT.bar(t, 0, 540, 900, 300, 60);
    KT.line(t, 0, 0, 0, 100, 100); KT.hinge(t, 0, 540, 900, 200, { keys: [[0, 0], [.3, .4]] }); KT.bubble(t, 0, 540, 900, 80); KT.clipTo(KT.panel(t, 0, 540, 900, 400, 200), () => {});
    KT.orbit(t, 0, 540, 900, 200); KT.streak(.1, 0); KT.bokeh(t); KT.group(t, { x: 1, flip: { t0: 0, dur: 1 }, swing: { t0: 0, amp: .2 } }, () => {}); KT.post(t); } catch (e) { F('partners', e); }
  const kc = [['تتحرّك', 2, 'تتحــرّك'], ['السلام', 2, 'الســلام'], ['ما انام', 3, 'مـــا انـــام'], ['دار', 2, 'دار']];
  for (const [w, n, want] of kc) { const got = KT.kashida(w, n); if (got !== want) F('kashida ' + w, got + ' != ' + want); }
  if (KT.kashida('الله', 2).includes('لـا')) F('kashida', 'broke lam-alef');
  if (KT.timeline([{ w: 'a', s: 0, e: .2 }, { w: 'b', s: .3, e: .9 }])[0].t1 < .8) F('timeline', 'minHold not applied');
  return { fail, ins: Object.keys(KT.IN).length, outs: Object.keys(KT.OUT).length, size: [W, H] };
});
await b.close();
r.fail.push(...k.fail); r.counts.ktIn = k.ins; r.counts.ktOut = k.outs; r.counts.ktCanvas = k.size.join('x');
console.log(JSON.stringify(r.counts), 'darkPalettes', r.darkPalettes);
const fails = [...errs, ...r.fail];
if (fails.length) { console.log('FAIL', fails.length); console.log(fails.slice(0, 40).join('\n')); process.exit(1); }
console.log('selftest OK');
