// ═══════════════════════════════════════════════════════════════════════════
//  engine/cues.js — SOUND LAYER cue registry (load after core.js / fx.js).
//
//  The picture already knows when every action happens: it is all springs and
//  easings. This file turns that same math into sound cues, so cue frames are
//  never typed by hand and never drift after a re-time.
//
//    when.spring(t0, 'card')      → motion driven by sp(t, t0, 'card')
//    when.ease(a, b, ease)        → motion driven by ease/easeOut/smooth(a, b, t)
//    when.path(t => pos, t0, t1)  → any position function (number or [x, y, …])
//      each returns { start, peak, land } in FRAMES, measured exactly the way
//      sound-layer/scripts/qa.py measures the video: frame-to-frame change,
//      peak = frame of largest change (= peak speed), land = first frame after
//      the peak where change ≤ 5 % of the peak (= motion has stopped).
//
//    cue.land('id', when.spring(4.1), { sound: 'paper', pan: .3 })
//    cue.move('id', when.ease(4, 8.2), { sound: 'whoosh' })
//    cue.cut('id', 4.0, { sound: 'transition' })     // t of the full-frame change
//    cue.appear('id', when.spring(5.8, 'snap'), { sound: 'pop' })   // or a time in s
//    cue.hero('id', when.spring(12.4, 'soft'), { on: 'land' })     // thump+tap, stop_before, build
//
//  Call these at scene load (top of the scene IIFE), never inside draw().
//  tools/export_cues.mjs reads window.CUES and writes audio/cues.json in the
//  `uv run sound-layer/scripts/mix.py --schema` format.
// ═══════════════════════════════════════════════════════════════════════════
window.CUES = window.CUES || [];
(() => {
  const FPS = () => (window.FILM && FILM.fps) || 30;
  const springOf = (kind) => Array.isArray(kind) ? kind
    : (typeof SPR !== 'undefined' && SPR[kind]) || (typeof SPRINGS !== 'undefined' && SPRINGS[kind]) || null;
  const mag = (a, b) => Array.isArray(a) ? Math.hypot(...a.map((v, i) => v - b[i])) : Math.abs(a - b);

  // sample pos(t) at frame times f/fps; change[f] = |pos(f) - pos(f-1)| (qa.py's motion curve)
  function path(pos, t0, t1, { stop = 0.05 } = {}) {
    const fps = FPS(), f0 = Math.max(0, Math.floor(t0 * fps) - 1), f1 = Math.ceil(t1 * fps) + 1, d = [];
    let prev = pos(f0 / fps);
    for (let f = f0 + 1; f <= f1; f++) { const x = pos(f / fps); d.push([f, mag(x, prev)]); prev = x; }
    let pi = 0; d.forEach(([, v], i) => { if (v > d[pi][1]) pi = i; });
    const max = d[pi][1]; if (!(max > 0)) throw new Error(`when.path: no motion between ${t0}s and ${t1}s`);
    const si = d.findIndex(([, v]) => v > 0.02 * max);
    let li = d.length - 1; for (let i = pi + 1; i < d.length; i++) if (d[i][1] <= stop * max) { li = i; break; }
    return { start: d[si][0], peak: d[pi][0], land: d[li][0], src: '' };
  }
  const spring_ = (t0, kind = 'card', o = {}) => {
    const p = springOf(kind); if (!p) throw new Error(`when.spring: unknown spring '${kind}'`);
    const r = path((t) => spring(t - t0, p[0], p[1]), t0, t0 + (o.max || 4), o);
    r.src = `spring ${Array.isArray(kind) ? p.join('/') : kind} @${+t0.toFixed(3)}s`; return r;
  };
  const ease_ = (a, b, fn = ease, o = {}) => {
    const r = path((t) => fn(a, b, t), a, b, o); r.src = `${fn.name || 'ease'} ${a}–${b}s`; return r;
  };
  window.when = { spring: spring_, ease: ease_, path: (pos, t0, t1, o) => Object.assign(path(pos, t0, t1, o), { src: `path ${t0}–${t1}s` }) };

  const KEYS = ['sound', 'weight', 'align', 'pan', 'stop_before', 'build', 'pitch', 'note'];
  function add(id, frame, visual, o = {}, src = '') {
    if (!id || typeof id !== 'string') throw new Error('cue: id (string) required');
    if (!o.sound) throw new Error(`cue ${id}: sound required (type | type/id | path | "a+b")`);
    const c = { id, frame: Math.round(frame), visual };
    for (const k of KEYS) if (o[k] !== undefined) c[k] = o[k];
    if (src || o.src) c.src = o.src || src;
    CUES.push(c); return c;
  }
  const at = (w, key) => typeof w === 'number' ? { f: Math.round(w * FPS()), src: `t ${w}s` } : { f: w[key], src: `${w.src} → ${key}` };
  window.cue = {
    // element stops moving (frame motion settles)
    land: (id, w, o) => { const p = at(w, 'land'); return add(id, p.f, 'land', o, p.src); },
    // frame of peak speed (whooshes, swishes)
    move: (id, w, o) => { const p = at(w, 'peak'); return add(id, p.f, 'move', o, p.src); },
    // full-frame change at time t (s): first frame at or after t
    cut: (id, t, o) => add(id, Math.ceil(t * FPS() - 1e-6), 'cut', o, `cut @${t}s`),
    // element pops in: first visible frame
    appear: (id, w, o) => { const p = typeof w === 'number' ? { f: Math.floor(w * FPS()) + 1, src: `appear @${w}s` } : at(w, 'start'); return add(id, p.f, 'appear', o, p.src); },
    // one hero per ~4 s: soft hero = thump+tap with a dead stop before and a music build into it
    hero: (id, w, o = {}) => {
      const on = o.on || 'land', key = on === 'move' ? 'peak' : on === 'appear' ? 'start' : 'land';
      const p = at(w, key);
      return add(id, p.f, on, { sound: 'thump+tap', stop_before: true, build: true, ...o, weight: 'hero' }, p.src);
    },
    // raw cue (no picture check) — e.g. a riser that peaks on the hero frame: cue.raw('rise', heroCue.frame, {sound:'riser'})
    raw: (id, frame, o) => add(id, frame, undefined, o, `frame ${frame}`),
  };
})();
