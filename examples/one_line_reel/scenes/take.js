// ═══ THE TAKE · one shot, one line · 0 → END_TAKE ═══════════════════════════════════════════════════
// bg → camera → blooms → world-under (images) → the line (dried ink + fresh trail + pen) → world words → screen words
const END_TAKE = window.END_TAKE || 61.30;
const LOOK = { px: 7, trail: 2600, dry: .92 };
function penHead(t) {
  const s = LINE.head(t), p = LINE.at(s), c = LCAM.now, z = c.z;
  const moving = Math.abs(LINE.head(t + 1 / 30) - s) > .5 || Math.abs(s - LINE.head(t - 1 / 30)) > .5;
  g.save(); g.fillStyle = LP.gold; g.globalAlpha = moving ? .28 : .16; g.beginPath(); g.arc(p.x, p.y, 20 / z, 0, 7); g.fill();
  g.globalAlpha = 1; g.fillStyle = '#fff6dc'; g.beginPath(); g.arc(p.x, p.y, 6.5 / z, 0, 7); g.fill(); g.restore();
}
SHOTS.push({ a: 0, b: END_TAKE, tin: 'cut', draw: (t) => {
  const hit = (typeof HITS !== 'undefined') ? HITS(t) : { x: 0, y: 0, r: 0 };
  const c = LCAM.set(t, hit);
  STAGE.bg(t, c);
  g.save(); LCAM.apply(c);
  BLOOM.draw(t);
  WORLD.under.forEach((f) => f(t));
  const s = LINE.head(t), dry = (typeof DRY !== 'undefined') ? DRY(t) : LOOK.dry;
  const px = LOOK.px * clamp(Math.pow(c.z, .3), .55, 1.15);
  LINE.stroke(0, s, { color: '#c7a75e', px, alpha: dry, z: c.z, shadow: .55 });
  LINE.stroke(Math.max(0, s - LOOK.trail), s, { color: LP.gold, px, alpha: 1, z: c.z, under: .09, core: .55 });
  WORLD.lineFx && WORLD.lineFx.forEach((f) => f(t, px, c));
  if (t < (window.PEN_OFF || END_TAKE)) penHead(t);
  g.restore();
  WORLD.over.forEach((f) => f(t));
  WORLD.screen.forEach((f) => f(t));
  // hit flashes (a breath of light on the hero frames)
  for (const t0 of (window.FLASH || [])) { const k = t - t0; if (k >= 0 && k < .25) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'screen'; g.fillStyle = `rgba(255,236,190,${.16 * Math.exp(-k * 14)})`; g.fillRect(0, 0, W, H); g.restore(); } }
} });
window.FLASH = (window.FLASH || []).concat([5.255, 10.525]);
// a small camera impact on hero landings
const HITS = (t) => { const hs = [[5.20, 10], [10.36, 6], [36.48, 6], [50.14, 8], [57.24, 7], [61.94, 9]]; let x = 0, y = 0, r = 0;
  for (const [t0, a] of hs) { const im = impact(t, t0, a); x += im.x; y += im.y; r += im.r; } return { x, y, r }; };
