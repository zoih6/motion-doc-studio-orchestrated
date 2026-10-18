// the hero word «الثُّلُث» writes itself stroke by stroke (order map baked offline)
let inkW, inkH, inkCan, inkCtx, inkData, inkAlpha, orderData, lastP = -1;
INITS.push(async () => {
  await Promise.all([loadImg('ink', 'assets/thuluth_ink.png'), loadImg('order', 'assets/thuluth_order.png'), loadImg('dot', 'assets/thuluth_dot.png')]);
  inkW = A.ink.width; inkH = A.ink.height; inkCan = mk(inkW, inkH); inkCtx = inkCan.getContext('2d');
  const tmp = mk(inkW, inkH), tx = tmp.getContext('2d');
  tx.drawImage(A.ink, 0, 0); inkAlpha = tx.getImageData(0, 0, inkW, inkH).data.slice();
  tx.clearRect(0, 0, inkW, inkH); tx.drawImage(A.order, 0, 0); orderData = tx.getImageData(0, 0, inkW, inkH).data.slice();
  inkData = inkCtx.createImageData(inkW, inkH);
});
function inkFrame(p) {
  if (p === lastP) return inkCan; lastP = p; const d = inkData.data, lim = p * 262;
  for (let i = 0; i < d.length; i += 4) { const a = inkAlpha[i + 3]; if (!a) { d[i + 3] = 0; continue; }
    const k = clamp((lim - orderData[i]) / 7); d[i] = 30; d[i + 1] = 20; d[i + 2] = 12; d[i + 3] = a * k; }
  inkCtx.putImageData(inkData, 0, 0); return inkCan;
}
// draw the word (width w, centred at x,y) at writing progress p; dot lands with spring at tDot
function heroWord(t, x, y, w, p, tDot) {
  const h = w * inkH / inkW, x0 = x - w / 2, y0 = y - h / 2;
  if (p > 0) g.drawImage(inkFrame(clamp(p)), x0, y0, w, h);
  const dk = sp(t, tDot, 'snap'); if (dk > 0) { const ex = x0 + 396 / inkW * w, ey = y0 + 301 / inkH * h, s = lerp(1.8, 1, dk);
    g.save(); g.globalAlpha = clamp(dk * 3); g.translate(ex, ey); g.scale(s, s); g.translate(-ex, -ey); g.drawImage(A.dot, x0, y0, w, h); g.restore(); }
  return { x0, y0, w, h };
}
