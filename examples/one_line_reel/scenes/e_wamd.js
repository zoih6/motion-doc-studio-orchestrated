// ═══ E · 61.37–64.80 · WAMD OUTRO (new shot) · indigo night · four colour arcs sweep into an arch ·
//     the wamd badge springs in with a glint · shimmer · sparkles · «تصميم وإنتاج» ═══
(() => {
  const E0 = 61.366;                      // cut frame (1841)
  const WC = ['#e8358a', '#7a35e0', '#2f56e8', '#21b06b'];
  const CX = 540, CY = 800, BR = 285;     // badge centre / radius in screen px
  const T = {};
  window.END_TAKE = 64.80;
  let R;
  INITS.push(async () => {
    R = rng(20261013);
    await loadImg('wamd', 'assets/wamd.png');
    T.des = KT.word('تَصمِيم وَإنتاج', { font: DISPLAY, weight: 700, size: 82, color: '#f6f1e7' });
    T.spk = []; for (let i = 0; i < 11; i++) { const a = R() * 6.283, d = 380 + R() * 480;
      T.spk.push({ x: CX + Math.cos(a) * d, y: CY - 60 + Math.sin(a) * d * .78, t0: 62.95 + R() * 1.1, s: 10 + R() * 14, r: R() * 1.2 }); }
  });
  LCAM.key(61.37, 0, -22500, 1.2, 0);     // hard cut into the new shot
  cue.hero('wamd', 62.00, { on: 'appear', sound: 'thump/fs-187136-body-fall-wav-1+chime/fs-185822-single-chime-1' });
  cue.appear('wmsh', 62.85, { sound: 'shimmer/fs-388295-sparkles-and-percussion-1' });
  cue.move('wos', when.ease(E0, E0 + .22), { sound: 'whoosh/fs-449994-whoosh-med-mid-wav-1' });
  window.FLASH = (window.FLASH || []).concat([61.99]);

  // star (4-point glint)
  const star = (x, y, r, rot, a) => { if (a <= 0 || r <= 0) return; g.save(); g.translate(x, y); g.rotate(rot || 0); g.globalAlpha = a;
    g.fillStyle = '#fff'; g.beginPath();
    for (const [dx, dy] of [[0, -1], [.16, -.16], [1, 0], [.16, .16], [0, 1], [-.16, .16], [-1, 0], [-.16, -.16]]) g[dx === 0 && dy === -1 ? 'moveTo' : 'lineTo'](dx * r, dy * r);
    g.closePath(); g.fill(); g.restore(); };

  WORLD.screen.push((t) => {
    if (t < E0 - .001) return;
    // indigo night + a soft violet aura behind the badge
    g.fillStyle = '#140f2e'; g.fillRect(0, 0, W, H);
    const au = g.createRadialGradient(CX, CY - 40, 50, CX, CY - 40, 900);
    au.addColorStop(0, 'rgba(122,53,224,.32)'); au.addColorStop(.55, 'rgba(47,86,232,.12)'); au.addColorStop(1, 'rgba(20,15,46,0)');
    g.fillStyle = au; g.fillRect(0, 0, W, H);
    // ── four arcs sweep in with moving tips (the studio's own pen) ──
    const breath = 1 + .015 * Math.sin(t * 1.7);
    g.save(); g.translate(CX, CY - 40); g.rotate(.025 * Math.sin((t - E0) * 1.1));
    g.lineCap = 'round';
    for (let i = 0; i < 4; i++) {
      const t0 = E0 + .04 + i * .085, k = KT.eOut(clamp((t - t0) / .34)); if (k <= 0) continue;
      const r = 400 - i * 62 * breath, a0 = -Math.PI * 1.06, span = Math.PI * 1.12 * k;   // big → small, all sweeping the same way
      g.strokeStyle = WC[i]; g.lineWidth = 34; g.globalAlpha = k > .999 ? 1 : .96;
      g.beginPath(); g.arc(0, 0, r, a0, a0 + span); g.stroke();
      if (k < .999) { g.fillStyle = '#fff'; g.globalAlpha = .95; g.beginPath(); g.arc(Math.cos(a0 + span) * r, Math.sin(a0 + span) * r, 9, 0, 7); g.fill(); }
    }
    g.restore();
    // ── glint cross behind the badge, then the badge springs in ──
    if (t >= 61.995) {
      const kg = 1 - clamp((t - 62.0) / .5), ks = KT.spr(t - 62.0, 'pop');
      star(CX, CY - 40, 210 * Math.max(0, kg * 1.4), Math.PI / 6, kg * .9);
      const bob = t > 62.6 ? Math.sin((t - 62.6) * 2.1) * 8 : 0, wob = (1 - Math.min(1, ks)) * -.38, sc = Math.max(0, ks);
      if (A.wamd && sc > 0) { const w = BR * 2 * sc, h = w * A.wamd.height / A.wamd.width;
        g.save(); g.translate(CX, CY - 40 + bob + (1 - Math.min(1, ks)) * 60); g.rotate(wob);
        g.shadowColor = 'rgba(232,53,138,.45)'; g.shadowBlur = 46 * sc;
        g.drawImage(A.wamd, -w / 2, -h / 2, w, h); g.restore(); }
      // shimmer: a light band runs across the badge
      const kh = clamp((t - 62.85) / .5);
      if (kh > 0 && kh < 1) { const x = CX - 420 + 840 * kh;
        const gr = g.createLinearGradient(x - 70, 0, x + 70, 0);
        gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, 'rgba(255,244,215,.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
        g.save(); g.beginPath(); g.rect(CX - BR, CY - 40 - BR, BR * 2, BR * 2); g.clip();
        g.translate(CX, CY - 40); g.rotate(.5); g.fillStyle = gr; g.fillRect(x - CX - 140, -BR - 160, 280, BR * 2 + 320); g.restore(); }
    }
    // sparkles wake one by one
    for (const s of T.spk || []) { const k = clamp((t - s.t0) / .5); star(s.x, s.y, s.s * Math.sin(Math.min(k, 1) * Math.PI) * (k < 1 ? 1 : 0), s.r + t * .4, 1); }
    // text
    KT.show(T.des, t, { x: CX, y: 1268, t0: 62.45, in: 'mask' });
    // gentle fade to the night at the very end
    const kf = clamp((t - 64.55) / .25); if (kf > 0) { g.fillStyle = `rgba(10,7,26,${kf})`; g.fillRect(0, 0, W, H); }
  });
})();
