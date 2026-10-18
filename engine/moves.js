// ════════════════════════════════════════════════════════════════════
//  motion-doc-studio · moves.js — MOVES: a dictionary of named motion moves (original implementations)
//  Load after core.js + fx.js. Each move is a pure function of normalised progress u∈[0,1] (loops: of seconds).
//  Names follow the common industry vocabulary (fadeInUp, popIn, rubberBand, hinge…) so prompts, briefs and
//  storyboards can say the move by name. Docs + picking guide: ../library/motion_recipes.md
//
//  USE
//    move('popIn', t, 2.0, { x: 960, y: 540, w: 400, h: 120 }, () => drawThing(0, 0));   // draw centred at (0,0)
//    move('rubberBand', t, 4.1, box, fn, { dur: .9 })      // override duration
//    moveOut('hinge', t, 7.0, box, fn)                     // alias of move() – exits leave alpha 0 after the end
//    seqMove([['dropIn', 1.0], ['tada', 2.2], ['zoomOut', 5.0]], t, box, fn)   // one element, many moves
//    staggerMove('fadeInUp', t, t0, boxes, (b, i) => draw(b), { gap: .07 })    // cascade over many items
//  STATE returned by MOVES[name].f(u, el): { x, y (px offset), s, sx, sy (scale), r (rad), skx (shear), a (alpha), blur (px), px, py (pivot 0..1) }
// ════════════════════════════════════════════════════════════════════
const MOVES = (() => {
  const P = Math.PI, C = typeof clamp === 'function' ? clamp : (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), L = (a, b, k) => a + (b - a) * k;
  const eO = x => 1 - Math.pow(1 - x, 3), eI = x => x * x * x, eIO = x => x < .5 ? 4 * x ** 3 : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const expO = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x), expI = x => x <= 0 ? 0 : Math.pow(2, 10 * x - 10);
  const back = (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2), backI = (x, s = 1.70158) => (s + 1) * x ** 3 - s * x * x;
  const bounce = x => { const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75; if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; };
  const springU = (u, dur, k = 170, d = 18) => { const t = u * dur; if (t <= 0) return 0; const w0 = Math.sqrt(k), z = d / (2 * w0); if (z >= 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t); const wd = w0 * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t)); };
  const decay = (u, f = 3, k = 4) => Math.sin(u * f * 2 * P) * Math.exp(-u * k);       // damped oscillation −1…1
  const D = (el, k = 1) => (el.dist ?? Math.max(160, (el.h || 120) * 1.4)) * k;         // default travel distance
  const M = {};
  const def = (name, type, dur, f, note) => M[name] = { type, dur, f, note };
  // ── ENTRANCES ──────────────────────────────────────────────────────
  def('fadeIn', 'in', .45, u => ({ a: eO(u) }), 'plain opacity. Use sparingly (banned as the ONLY entrance in a film)');
  def('fadeInUp', 'in', .55, (u, el) => ({ a: C(u * 2), y: (1 - eO(u)) * D(el, .35) }), 'rise a little while fading — calm default for captions');
  def('fadeInDown', 'in', .55, (u, el) => ({ a: C(u * 2), y: -(1 - eO(u)) * D(el, .35) }), 'drop a little while fading — labels from above');
  def('fadeInLeft', 'in', .55, (u, el) => ({ a: C(u * 2), x: -(1 - eO(u)) * D(el, .4) }), 'enters from the left (LTR reading)');
  def('fadeInRight', 'in', .55, (u, el) => ({ a: C(u * 2), x: (1 - eO(u)) * D(el, .4) }), 'enters from the right (RTL reading — default for Arabic)');
  def('slideInUp', 'in', .6, (u, el) => ({ y: (1 - expO(u)) * (el.H || 1080) * .7 }), 'travels in from below the frame, no fade');
  def('slideInDown', 'in', .6, (u, el) => ({ y: -(1 - expO(u)) * (el.H || 1080) * .7 }), 'travels in from above the frame');
  def('slideInLeft', 'in', .6, (u, el) => ({ x: -(1 - expO(u)) * (el.W || 1920) * .7 }), 'travels in from off-screen left');
  def('slideInRight', 'in', .6, (u, el) => ({ x: (1 - expO(u)) * (el.W || 1920) * .7 }), 'travels in from off-screen right (RTL)');
  def('zoomIn', 'in', .5, u => ({ s: L(.3, 1, eO(u)), a: C(u * 2.5) }), 'grows from small');
  def('zoomInUp', 'in', .7, (u, el) => ({ s: L(.25, 1, eO(u)), y: (1 - back(u, 1.2)) * D(el, .8), a: C(u * 2.5) }), 'grows while rising, slight overshoot');
  def('popIn', 'in', .45, u => ({ s: u <= 0 ? 0 : back(u, 2.2), a: C(u * 5) }), 'scale with overshoot — the signature "sticker" entrance');
  def('springIn', 'in', .9, (u, el) => ({ s: springU(u, .9, el.k || 180, el.d || 12), a: C(u * 6) }), 'physical spring scale-in (stiffness el.k, damping el.d)');
  def('bounceIn', 'in', .75, u => { const k = u < .2 ? L(.3, 1.1, u / .2) : u < .4 ? L(1.1, .9, (u - .2) / .2) : u < .6 ? L(.9, 1.03, (u - .4) / .2) : u < .8 ? L(1.03, .97, (u - .6) / .2) : L(.97, 1, (u - .8) / .2); return { s: k, a: C(u * 4) }; }, 'staircase of scale overshoots — cartoony');
  def('bounceInDown', 'in', .9, (u, el) => ({ y: -(1 - bounce(u)) * (el.H || 1080) * .6, a: C(u * 6) }), 'falls from above and bounces on its baseline');
  def('backInUp', 'in', .8, (u, el) => { const a = C(u / .7), b = C((u - .7) / .3); return { y: (1 - eO(a)) * D(el, 2), s: L(.7, 1, eO(b)), a: .7 + .3 * eO(a) }; }, 'arrives small from below, then scales to full size');
  def('backInDown', 'in', .8, (u, el) => { const a = C(u / .7), b = C((u - .7) / .3); return { y: -(1 - eO(a)) * D(el, 2), s: L(.7, 1, eO(b)), a: .7 + .3 * eO(a) }; }, 'arrives small from above, then scales to full size');
  def('flipInX', 'in', .7, u => { const k = back(u, 1.6); return { sy: Math.max(.001, Math.sin(k * P / 2)), skx: 0, a: C(u * 3), shade: 1 - C(u * 1.5) }; }, 'card flips toward camera around the horizontal axis');
  def('flipInY', 'in', .7, u => { const k = back(u, 1.6); return { sx: Math.max(.001, Math.sin(k * P / 2)), a: C(u * 3), shade: 1 - C(u * 1.5) }; }, 'card flips around the vertical axis');
  def('rotateIn', 'in', .6, u => ({ r: -(1 - eO(u)) * P * .9, s: L(.6, 1, eO(u)), a: C(u * 2.5) }), 'spins into place');
  def('rollIn', 'in', .75, (u, el) => ({ x: -(1 - eO(u)) * D(el, 2.2), r: -(1 - eO(u)) * P * .7, a: C(u * 2) }), 'rolls in from the side like a coin');
  def('lightSpeedIn', 'in', .55, (u, el) => { const k = expO(u); return { x: (1 - k) * D(el, 3), skx: u < .6 ? -.5 * (1 - u / .6) : .15 * Math.sin((u - .6) / .4 * P) , a: C(u * 3) }; }, 'races in with a forward shear, settles with a counter-lean');
  def('jackInTheBox', 'in', .8, u => ({ s: L(.1, 1, eO(u)), r: decay(u, 1.5, 4) * .3, py: 1, a: C(u * 3) }), 'springs out of the bottom pivot with a wobble');
  def('blurIn', 'in', .6, u => ({ blur: (1 - eO(u)) * 24, s: L(1.15, 1, eO(u)), a: C(u * 2) }), 'focus pull from soft to sharp — premium/editorial');
  def('dropIn', 'in', .7, (u, el) => { const fall = C(u / .55), land = C((u - .55) / .45); return { y: -(1 - eI(fall)) * D(el, 3), sy: u < .55 ? 1.08 : 1 - .18 * decay(land, 1, 6), sx: u < .55 ? .95 : 1 + .14 * decay(land, 1, 6), py: 1, a: C(u * 5) }; }, 'gravity fall + squash on landing (pivot at feet)');
  def('stampIn', 'in', .45, u => ({ s: L(2.6, 1, eI(C(u / .55))) + .05 * decay(C((u - .55) / .45), 1.5, 6), a: C(u * 4), impactAt: .55 }), 'slams from huge onto the page; pair with impact()/shake at u=.55');
  def('swingIn', 'in', .9, u => ({ r: (1 - eO(u)) * -1.2 + decay(u, 1.2, 3.5) * .25 * (1 - u), py: 0, a: C(u * 4) }), 'swings down from a top pivot, like a hanging sign');
  def('riseIn', 'in', .65, (u, el) => ({ y: (1 - expO(u)) * (el.h || 120) * 1.1, clipY: 1 - expO(u), a: 1 }), 'rises out of an invisible baseline mask (set el.clip=true)');
  def('whipIn', 'in', .35, (u, el) => ({ x: (1 - expO(u)) * D(el, 4), sx: 1 + (1 - u) * .6, blur: (1 - u) * 14, a: C(u * 6) }), 'very fast horizontal arrival with smear');
  def('elasticIn', 'in', 1.0, u => ({ s: u <= 0 ? 0 : u >= 1 ? 1 : Math.pow(2, -10 * u) * Math.sin((u * 10 - .75) * 2 * P / 3) + 1 }), 'rubbery overshoot scale');
  def('unfoldIn', 'in', .7, u => ({ sx: Math.max(.002, eO(C(u / .5))), sy: u < .5 ? .04 : Math.max(.04, eO(C((u - .5) / .5))) }), 'opens as a line, then unfolds vertically (screens, panels)');
  def('glitchIn', 'in', .4, (u, el) => { const r = Math.sin(Math.floor(u * 14) * 91.7) * 43758.5 % 1; return { x: u < .8 ? (r - .5) * 40 : 0, a: u < .8 ? (r > .3 ? 1 : .2) : 1, rgb: u < .8 ? 8 : 0 }; }, 'stuttering digital arrival (set rgb split on draw)');
  def('typeIn', 'in', 1.0, u => ({ reveal: u }), 'progress only: use reveal for text.slice(0, n*reveal) or a mask');
  def('drawIn', 'in', 1.0, u => ({ reveal: eIO(u) }), 'progress only: stroke draw-on for paths/icons (icon(..,{k:reveal}))');
  // ── EXITS ──────────────────────────────────────────────────────────
  def('fadeOut', 'out', .35, u => ({ a: 1 - eI(u) }), 'plain opacity out');
  def('fadeOutUp', 'out', .45, (u, el) => ({ a: 1 - C(u * 1.4), y: -eI(u) * D(el, .35) }), 'lifts away');
  def('fadeOutDown', 'out', .45, (u, el) => ({ a: 1 - C(u * 1.4), y: eI(u) * D(el, .35) }), 'sinks away');
  def('slideOutLeft', 'out', .5, (u, el) => ({ x: -expI(u) * (el.W || 1920) * .8 }), 'pushed off left');
  def('slideOutRight', 'out', .5, (u, el) => ({ x: expI(u) * (el.W || 1920) * .8 }), 'pushed off right');
  def('zoomOut', 'out', .4, u => ({ s: L(1, .3, eI(u)), a: 1 - C(u * 1.3) }), 'shrinks away');
  def('popOut', 'out', .35, u => ({ s: u < .3 ? L(1, 1.12, eO(u / .3)) : L(1.12, 0, eI((u - .3) / .7)), a: 1 - C((u - .5) * 2) }), 'small anticipation swell, then collapses');
  def('backOutDown', 'out', .8, (u, el) => { const a = C(u / .3), b = C((u - .3) / .7); return { s: L(1, .7, eO(a)), y: eI(b) * D(el, 2.5), a: 1 - .3 * a - .7 * b }; }, 'shrinks, then drops out');
  def('flipOutX', 'out', .5, u => ({ sy: Math.max(.001, Math.cos(eI(u) * P / 2)), a: 1 - C((u - .6) * 2.5), shade: u }), 'flips away around horizontal axis');
  def('rotateOut', 'out', .5, u => ({ r: eI(u) * P * .9, s: L(1, .6, eI(u)), a: 1 - C(u * 1.2) }), 'spins away');
  def('rollOut', 'out', .7, (u, el) => ({ x: eI(u) * D(el, 2.2), r: eI(u) * P * .7, a: 1 - C(u * 1.3) }), 'rolls off to the side');
  def('lightSpeedOut', 'out', .45, (u, el) => ({ x: expI(u) * D(el, 3), skx: .5 * eI(u), a: 1 - C((u - .4) * 1.7) }), 'races out with a backward shear');
  def('hinge', 'out', 1.6, (u, el) => { const sw = C(u / .65), fall = C((u - .65) / .35); return { r: 1.25 * eO(sw) + .25 * Math.sin(sw * P * 4) * (1 - sw), px: 0, py: 0, y: eI(fall) * (el.H || 1080), a: 1 - C((fall - .6) * 2.5) }; }, 'a bolt breaks: swings from the top-left corner, then falls');
  def('blurOut', 'out', .45, u => ({ blur: eI(u) * 24, s: L(1, 1.12, eI(u)), a: 1 - C(u * 1.2) }), 'defocuses away');
  def('dropOut', 'out', .6, (u, el) => ({ y: eI(u) * (el.H || 1080) * .9, r: eI(u) * .25, a: 1 - C((u - .7) * 3.3) }), 'gravity takes it');
  def('shrinkOut', 'out', .3, u => ({ s: 1 - eI(u), a: 1 - C((u - .7) * 3.3) }), 'quick collapse to a point');
  def('whipOut', 'out', .3, (u, el) => ({ x: -expI(u) * D(el, 4), sx: 1 + u * .6, blur: u * 14, a: 1 - C((u - .5) * 2) }), 'very fast exit with smear');
  def('wipeOut', 'out', .5, u => ({ clipX: eIO(u) }), 'progress only: hard wipe mask from the reading edge (set el.clip=true)');
  // ── EMPHASIS (play on an element that is already on screen) ─────────
  def('pulse', 'emph', .6, u => ({ s: 1 + .06 * Math.sin(u * P) }), 'gentle swell — "look here"');
  def('heartBeat', 'emph', 1.1, u => ({ s: 1 + .14 * (Math.exp(-Math.pow((u - .14) / .06, 2)) + .8 * Math.exp(-Math.pow((u - .42) / .06, 2))) }), 'two quick beats (lub-dub)');
  def('rubberBand', 'emph', .9, u => { const k = decay(u, 2, 4.5); return { sx: 1 + .25 * k, sy: 1 - .2 * k }; }, 'stretches and snaps back like elastic');
  def('shakeX', 'emph', .6, u => ({ x: decay(u, 5, 3) * 14 }), 'horizontal shake — denial/error/impact');
  def('shakeY', 'emph', .6, u => ({ y: decay(u, 5, 3) * 12 }), 'vertical shake — rumble');
  def('headShake', 'emph', .9, u => ({ x: decay(u, 2.5, 4) * 10, r: decay(u, 2.5, 4) * .06 }), 'a "no" shake with tilt');
  def('nod', 'emph', .7, u => ({ y: Math.abs(decay(u, 2, 4)) * 10, r: -Math.abs(decay(u, 2, 4)) * .03 }), 'a "yes" nod');
  def('swing', 'emph', 1.0, u => ({ r: decay(u, 2, 3) * .25, py: 0 }), 'pendulum from the top edge');
  def('tada', 'emph', 1.0, u => ({ s: u < .2 ? 1 - .1 * Math.sin(u / .2 * P / 2) : u < .9 ? 1.1 : L(1.1, 1, (u - .9) / .1), r: u > .2 && u < .9 ? Math.sin((u - .2) / .7 * P * 6) * .05 : 0 }), 'crouch, then wiggle big — celebration');
  def('wobble', 'emph', 1.0, (u, el) => ({ x: decay(u, 2.5, 3.5) * D(el, .15), r: decay(u, 2.5, 3.5) * .08 }), 'side-to-side lurch with rotation');
  def('jello', 'emph', .9, u => ({ skx: decay(u, 3, 4) * .25 }), 'shear wobble like gelatin');
  def('bounce', 'emph', .9, (u, el) => { const h = Math.abs(Math.sin(u * P * 2)) * Math.exp(-u * 3); return { y: -h * D(el, .3), sy: 1 + (u > .45 && u < .55 ? -.08 : .03 * h), py: 1 }; }, 'hops in place twice, squashes at the bottom');
  def('flash', 'emph', .8, u => ({ a: .5 + .5 * Math.cos(u * P * 4) }), 'blinks twice');
  def('punch', 'emph', .35, u => ({ s: 1 + .18 * Math.exp(-u * 8) * (u > 0 ? 1 : 0) }), 'instant scale punch that decays — beat hits');
  def('squash', 'emph', .5, u => { const k = Math.sin(u * P); return { sx: 1 + .2 * k, sy: 1 - .2 * k, py: 1 }; }, 'squash on the baseline (weight)');
  def('stretch', 'emph', .5, u => { const k = Math.sin(u * P); return { sx: 1 - .15 * k, sy: 1 + .25 * k, py: 1 }; }, 'stretch upward (anticipation before a jump)');
  def('tilt', 'emph', .6, u => ({ r: Math.sin(u * P) * .12 }), 'curious tilt and back');
  def('nudge', 'emph', .45, (u, el) => ({ x: Math.sin(u * P) * D(el, .12) * (el.dir || 1) }), 'small push toward el.dir, returns');
  def('glow', 'emph', .8, u => ({ glow: Math.sin(u * P) }), 'progress only: drive a highlight/halo (use on highlights, NOT on UI)');
  def('spinOnce', 'emph', .7, u => ({ r: eIO(u) * 2 * P }), 'one full turn');
  def('flipCoin', 'emph', .8, u => ({ sx: Math.cos(eIO(u) * 2 * P), shade: Math.abs(Math.sin(eIO(u) * 2 * P)) }), 'one full Y-flip (coin)');
  // ── LOOPS (ambient; u = seconds since t0, not 0..1) ──────────────────
  def('float', 'loop', 0, (s, el) => ({ y: Math.sin(s * 2 * P / (el.period || 3.2) + (el.phase || 0)) * (el.amp || 10) }), 'slow vertical float (period el.period)');
  def('bob', 'loop', 0, (s, el) => ({ y: -Math.abs(Math.sin(s * P / (el.period || .8))) * (el.amp || 14) }), 'repeated small hops');
  def('sway', 'loop', 0, (s, el) => ({ r: Math.sin(s * 2 * P / (el.period || 3) + (el.phase || 0)) * (el.amp || .05), py: el.py ?? 1 }), 'plant/flag sway from the base');
  def('spin', 'loop', 0, (s, el) => ({ r: s * 2 * P / (el.period || 6) }), 'continuous rotation');
  def('orbit', 'loop', 0, (s, el) => { const a = s * 2 * P / (el.period || 5) + (el.phase || 0); return { x: Math.cos(a) * (el.rx || 120), y: Math.sin(a) * (el.ry || 40), s: 1 + Math.sin(a) * (el.depth || .1) }; }, 'elliptical orbit with fake depth');
  def('pendulum', 'loop', 0, (s, el) => ({ r: Math.sin(s * 2 * P / (el.period || 2)) * (el.amp || .35), py: 0 }), 'clock pendulum from the top');
  def('breathe', 'loop', 0, (s, el) => ({ s: 1 + Math.sin(s * 2 * P / (el.period || 4)) * (el.amp || .025) }), 'living idle — subtle scale');
  def('blink', 'loop', 0, (s, el) => ({ a: (s % (el.period || 1)) < (el.period || 1) / 2 ? 1 : 0 }), 'on/off (cursors, REC lights)');
  def('drift', 'loop', 0, (s, el) => ({ x: (typeof wiggle === 'function' ? wiggle(s, .3, el.amp || 18, el.seed || 1) : Math.sin(s * .7) * 18), y: (typeof wiggle === 'function' ? wiggle(s, .25, (el.amp || 18) * .7, (el.seed || 1) + 4) : Math.cos(s * .5) * 12) }), 'organic noise drift (seeded)');
  def('hover', 'loop', 0, (s, el) => ({ y: Math.sin(s * 2 * P / (el.period || 2.4)) * (el.amp || 8), shadow: .5 + .5 * Math.sin(s * 2 * P / (el.period || 2.4)) }), 'hover with shadow cue (use shadow to scale a contact shadow)');
  def('jitter', 'loop', 0, (s, el) => { const f = Math.floor(s * (el.fps || 12)); return { x: (Math.sin(f * 12.9898) * 43758.5453 % 1) * (el.amp || 2), y: (Math.sin(f * 78.233) * 43758.5453 % 1) * (el.amp || 2) }; }, 'stop-motion boil on twos/threes (el.fps 8–12)');
  return M;
})();

// combine a state into the current canvas transform and draw. box = {x,y (centre), w,h, W,H, ...extra el params}
function applyMoveState(st, box, drawFn) {
  if (st.a !== undefined && st.a <= 0.001) return st;
  const w = box.w || 200, h = box.h || 100, px = st.px ?? box.px ?? .5, py = st.py ?? box.py ?? .5, ox = (px - .5) * w, oy = (py - .5) * h;
  g.save(); g.translate(box.x + (st.x || 0) + ox, box.y + (st.y || 0) + oy);
  if (st.r) g.rotate(st.r); if (st.skx) g.transform(1, 0, st.skx, 1, 0, 0);
  const s = st.s ?? 1, sx = s * (st.sx ?? 1), sy = s * (st.sy ?? 1); if (sx !== 1 || sy !== 1) g.scale(sx, sy);
  g.translate(-ox, -oy);
  if (st.a !== undefined && st.a < 1) g.globalAlpha *= Math.max(0, st.a);
  if (st.blur > .3) g.filter = `blur(${st.blur.toFixed(1)}px)`;
  if (box.clip && (st.clipY !== undefined || st.clipX !== undefined)) { g.beginPath(); if (st.clipY !== undefined) g.rect(-w / 2 - 40, -h / 2 - 40 - (st.y || 0), w + 80, h + 80); else { const cx = st.clipX * w; (FILM.rtl === false) ? g.rect(-w / 2 - 40 + cx, -h / 2 - 40, w + 80, h + 80) : g.rect(-w / 2 - 40, -h / 2 - 40, w + 80 - cx, h + 80); } g.clip(); }
  drawFn(st); g.restore(); return st;
}
// play a named move: before t0 → entrances hidden / others at rest; after the end → entrances at rest, exits gone.
function move(name, t, t0, box, drawFn, o = {}) {
  const M = MOVES[name]; if (!M) throw new Error('moves.js: unknown move ' + name);
  const el = Object.assign({ W: typeof W !== 'undefined' ? W : 1920, H: typeof H !== 'undefined' ? H : 1080 }, box, o);
  if (M.type === 'loop') return applyMoveState(t < t0 ? {} : M.f(t - t0, el), box, drawFn);
  const dur = o.dur || M.dur, u = (t - t0) / dur;
  if (u < 0) { if (M.type === 'in') return null; return applyMoveState({}, box, drawFn); }
  if (u >= 1) { if (M.type === 'out') return null; return applyMoveState(M.type === 'in' || M.type === 'emph' ? (M.f(1, el).reveal !== undefined ? { reveal: 1 } : {}) : {}, box, drawFn); }
  return applyMoveState(M.f(u, el), box, drawFn);
}
const moveOut = move;
// sequence of moves on one element: [[name, t0, {dur}], …] sorted by t0. The active move is the latest started one.
function seqMove(list, t, box, drawFn) {
  const first = list[0]; if (t < first[1] && MOVES[first[0]].type === 'in') return null;
  let cur = first; for (const m of list) if (t >= m[1]) cur = m;
  const M = MOVES[cur[0]], end = cur[1] + ((cur[2] && cur[2].dur) || M.dur);
  if (M.type === 'out' && t >= end) return null;
  return move(cur[0], t, cur[1], box, drawFn, cur[2] || {});
}
// cascade: same move across many boxes, offset by gap (seconds). order: 'rtl' | 'ltr' | 'center' | 'random' | 'index'
function staggerMove(name, t, t0, boxes, drawFn, { gap = .07, order = 'index', seed = 7, dur } = {}) {
  const idx = boxes.map((b, i) => i); let rank = idx.slice();
  if (order === 'rtl') rank = idx.slice().sort((a, b) => boxes[b].x - boxes[a].x);
  if (order === 'ltr') rank = idx.slice().sort((a, b) => boxes[a].x - boxes[b].x);
  if (order === 'center') { const cx = boxes.reduce((s, b) => s + b.x, 0) / boxes.length, cy = boxes.reduce((s, b) => s + b.y, 0) / boxes.length; rank = idx.slice().sort((a, b) => Math.hypot(boxes[a].x - cx, boxes[a].y - cy) - Math.hypot(boxes[b].x - cx, boxes[b].y - cy)); }
  if (order === 'random') { const r = rng(seed); rank = idx.map(i => [i, r()]).sort((a, b) => a[1] - b[1]).map(a => a[0]); }
  const pos = []; rank.forEach((bi, k) => pos[bi] = k);
  boxes.forEach((b, i) => move(name, t, t0 + pos[i] * gap, b, st => drawFn(b, i, st), dur ? { dur } : {}));
}
// list moves by type for docs/specimens: movesBy('in') …
const movesBy = type => Object.entries(MOVES).filter(([, m]) => !type || m.type === type).map(([n]) => n);
