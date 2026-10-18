// ═══ stage: deep-teal room the line lives in · WORLD registries ═══════════════════════════════════════
// background = calm radial teal + two soft light pools with slow parallax (depth without particles) + fine grain
const WORLD = { build: [], under: [], over: [], screen: [] };   // build order = path order (one line!)
const STAGE = (() => {
  let bgC = null, poolC = null, vigC = null;
  INITS.push(async () => {
    bgC = mk(W, H); { const x = bgC.getContext('2d'), gr = x.createRadialGradient(W * .5, H * .45, 60, W * .5, H * .5, H * .8);
      gr.addColorStop(0, '#0a4d45'); gr.addColorStop(.55, '#063c36'); gr.addColorStop(1, '#03261f'); x.fillStyle = gr; x.fillRect(0, 0, W, H); }
    poolC = mk(900, 900); { const x = poolC.getContext('2d'), gr = x.createRadialGradient(450, 450, 0, 450, 450, 450);
      gr.addColorStop(0, 'rgba(120,210,180,.10)'); gr.addColorStop(.5, 'rgba(90,190,160,.04)'); gr.addColorStop(1, 'rgba(90,190,160,0)'); x.fillStyle = gr; x.fillRect(0, 0, 900, 900); }
    vigC = mk(W, H); { const x = vigC.getContext('2d'), gr = x.createRadialGradient(W / 2, H * .48, H * .38, W / 2, H / 2, H * .9);
      gr.addColorStop(0, 'rgba(0,10,8,0)'); gr.addColorStop(1, 'rgba(0,10,8,.42)'); x.fillStyle = gr; x.fillRect(0, 0, W, H); }
  });
  function bg(t, c) {
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(bgC, 0, 0);
    // light pools drift with 12 % parallax of the camera → the room feels deep while the camera travels
    const P = [[260, 520, 1.5, 0], [820, 1460, 1.9, 2.1]];
    P.forEach(([x, y, s, ph]) => { const px = x - c.x * .12 + Math.sin(t * .25 + ph) * 40, py = ((y - c.y * .12) % 2400 + 2400) % 2400 - 240, d = 900 * s * Math.sqrt(c.z);
      g.drawImage(poolC, px - d / 2, py - d / 2, d, d); });
    g.restore();
  }
  function post(t) { g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(vigC, 0, 0); fxGrain(t, .045, 'overlay'); }
  return { bg, post };
})();
// build the one line (all scene builders, in file order) before any scene INIT reads it
INITS.push(async () => { WORLD.build.forEach((f) => f()); });
