// ════════════════════════════════════════════════════════════════════
//  motion-doc-studio · gl.js — GPU transition runner for the vendored gl-transitions pack
//  Load order: core.js → helpers.js → fx.js → kit/data/gl_transitions.js → gl.js
//  Every GLSL in window.GLT_SRC (125, MIT/BSD, authors kept) is registered as TRANS['gl:<Name>'], so a shot uses
//      { a, b, draw, tin: 'gl:Dreamy', tdur: .8, glParams: { amplitude: 30 } }
//  Pure function of progress k (no timers) → deterministic, frame-exact renders.
//  Catalogue + picking guide: ../library/gl_transitions.md · licence: ../resources/licenses/gl-transitions.txt
// ════════════════════════════════════════════════════════════════════
const GLT = (() => {
  let cv2 = null, gl = null, buf = null, texA = null, texB = null, texM = null; const progs = {};
  const VS = 'attribute vec2 p;varying vec2 uv;void main(){uv=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
  const HEAD = 'precision highp float;varying vec2 uv;uniform sampler2D from,to;uniform float progress,ratio;\n'
    + 'vec4 getFromColor(vec2 u){return texture2D(from,u);}vec4 getToColor(vec2 u){return texture2D(to,u);}\n';
  function ctx() { if (gl) return gl; cv2 = document.createElement('canvas'); cv2.width = W; cv2.height = H;
    gl = cv2.getContext('webgl', { preserveDrawingBuffer: true, premultipliedAlpha: false, antialias: false });
    if (!gl) throw new Error('gl.js: WebGL unavailable (headless chromium: launch with default GPU or --use-gl=swiftshader)');
    buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    const mkT = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v); return t; };
    texA = mkT(); texB = mkT(); texM = mkT();
    // procedural map for the two transitions that expect an image uniform (luma, displacement): seeded fbm, deterministic
    const mc = document.createElement('canvas'); mc.width = 512; mc.height = 288; const mx = mc.getContext('2d'), d = mx.createImageData(512, 288);
    for (let j = 0; j < 288; j++) for (let i = 0; i < 512; i++) { const v = (typeof fbm === 'function' ? .5 + .5 * fbm(i * .012, j * .012, 4) : ((i * 7 + j * 13) % 97) / 97) * 255; const o = (j * 512 + i) * 4; d.data[o] = d.data[o + 1] = d.data[o + 2] = v; d.data[o + 3] = 255; }
    mx.putImageData(d, 0, 0); gl.bindTexture(gl.TEXTURE_2D, texM); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, mc);
    return gl; }
  // parse "uniform <type> <name>; // = <default>"  (also /* = … */ before the semicolon)
  function uniforms(src) { const out = [];
    for (const m of src.matchAll(/uniform\s+(\w+)\s+(\w+)\s*(?:\/\*\s*=\s*([^*]+?)\s*\*\/)?\s*;\s*(?:\/\/\s*=\s*([^\n]+))?/g)) {
      const [, type, name, d1, d2] = m; let def = (d1 || d2 || '').trim().replace(/;$/, ''); out.push({ type, name, def }); }
    return out; }
  const parseVal = (type, s) => { if (type === 'bool') return /true/.test(s); s = String(s).split(';')[0].replace(/^\s*[a-z]+\d?\s*\(/i, '('); const n = (s.match(/-?\d*\.?\d+(?:e-?\d+)?/gi) || []).map(Number);
    if (type === 'float' || type === 'int') return n.length ? n[0] : 0; const k = +type.slice(-1); if (n.length === 1) return Array(k).fill(n[0]); return n.slice(0, k).concat(Array(Math.max(0, k - n.length)).fill(0)); };
  function prog(name) { if (progs[name]) return progs[name]; const S = window.GLT_SRC && GLT_SRC[name]; if (!S) throw new Error('gl.js: unknown transition ' + name);
    const g2 = ctx(), sh = (t, s) => { const o = g2.createShader(t); g2.shaderSource(o, s); g2.compileShader(o); if (!g2.getShaderParameter(o, g2.COMPILE_STATUS)) throw new Error('gl.js ' + name + ': ' + g2.getShaderInfoLog(o)); return o; };
    const P = g2.createProgram(); g2.attachShader(P, sh(g2.VERTEX_SHADER, VS)); g2.attachShader(P, sh(g2.FRAGMENT_SHADER, HEAD + S.glsl + '\nvoid main(){gl_FragColor=transition(uv);}')); g2.linkProgram(P);
    if (!g2.getProgramParameter(P, g2.LINK_STATUS)) throw new Error('gl.js link ' + name + ': ' + g2.getProgramInfoLog(P));
    return progs[name] = { P, U: uniforms(S.glsl) }; }
  function setU(g2, P, u, v) { const L = g2.getUniformLocation(P, u.name); if (!L) return; const t = u.type;
    if (t === 'float') g2.uniform1f(L, v); else if (t === 'int' || t === 'bool') g2.uniform1i(L, +v);
    else if (t === 'vec2') g2.uniform2fv(L, v); else if (t === 'vec3') g2.uniform3fv(L, v); else if (t === 'vec4') g2.uniform4fv(L, v);
    else if (t === 'ivec2') g2.uniform2iv(L, v.map(Math.round)); }
  // render transition `name` between two canvases at progress k into a canvas (returned)
  function frame(name, from, to, k, params = {}) { const { P, U } = prog(name), g2 = ctx(); g2.viewport(0, 0, W, H); g2.useProgram(P);
    g2.pixelStorei(g2.UNPACK_FLIP_Y_WEBGL, true);
    [[texA, from, 0, 'from'], [texB, to, 1, 'to']].forEach(([t, img, unit, nm]) => { g2.activeTexture(g2.TEXTURE0 + unit); g2.bindTexture(g2.TEXTURE_2D, t); g2.texImage2D(g2.TEXTURE_2D, 0, g2.RGBA, g2.RGBA, g2.UNSIGNED_BYTE, img); g2.uniform1i(g2.getUniformLocation(P, nm), unit); });
    g2.uniform1f(g2.getUniformLocation(P, 'progress'), k); g2.uniform1f(g2.getUniformLocation(P, 'ratio'), W / H);
    for (const u of U) { if (u.type === 'sampler2D') { g2.activeTexture(g2.TEXTURE2); g2.bindTexture(g2.TEXTURE_2D, texM); g2.uniform1i(g2.getUniformLocation(P, u.name), 2); continue; }
      const v = u.name in params ? (typeof params[u.name] === 'string' ? parseVal(u.type, params[u.name]) : params[u.name]) : parseVal(u.type, u.def); setU(g2, P, u, v); }
    const pos = g2.getAttribLocation(P, 'p'); g2.bindBuffer(g2.ARRAY_BUFFER, buf); g2.enableVertexAttribArray(pos); g2.vertexAttribPointer(pos, 2, g2.FLOAT, false, 0, 0);
    g2.drawArrays(g2.TRIANGLES, 0, 6); return cv2; }
  const list = () => Object.keys(window.GLT_SRC || {});
  const info = n => { const S = GLT_SRC[n]; return S && { name: n, author: S.author, license: S.license, desc: S.desc, uniforms: uniforms(S.glsl) }; };
  return { frame, list, info, uniforms };
})();

// register every pack transition in the engine's TRANS registry (fx.js) — key 'gl:<Name>'
// defaults: dur .8s, eased with CURVE.camera if present (shot.glEase:'linear' to disable), shot.glParams overrides uniforms
if (typeof TRANS !== 'undefined' && window.GLT_SRC) for (const n of GLT.list()) TRANS['gl:' + n] = { dur: .8, gl: true,
  draw(k, drawOut, o) { const IN = _inBuf(), OUT = renderOut(drawOut), ease = o.shot.glEase === 'linear' ? (x => x) : (typeof CURVE !== 'undefined' && CURVE.camera) || (x => x);
    const c = GLT.frame(n, OUT, IN, ease(k), o.shot.glParams || {}); g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(c, 0, 0); g.restore(); } };
