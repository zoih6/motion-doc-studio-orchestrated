// Export audio/cues.json from the picture's own timing (engine/cues.js → window.CUES).
// Run from the film folder (the one with index.html):
//   PAGE=index.html node ../tools/export_cues.mjs [--config audio/sound.json] [--out audio/cues.json]
// audio/sound.json (optional) holds the non-cue fields of the mix.py schema:
//   { "energy": "punchy"|"calm", "music": {...}, "voice": [...], "duck_db": 10, "room": {...},
//     "silence_ok": [[a,b]], "lufs": -14, "kit": "audio/kit", "cues_extra": [ ...cues with "t" or "frame"... ] }
// fps = FILM.fps (default 30); duration_s = FILM.duration or the end of the last shot.
// Validates: unique ids, sound present, visual ∈ cut|move|land|appear, inside the film,
// and warns when heroes are closer than ~4 s. Output format: `uv run sound-layer/scripts/mix.py --schema`.
import { chromium } from 'playwright';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const PAGE = process.env.PAGE || 'index.html', OUT = arg('out', 'audio/cues.json'), CFG = arg('config', 'audio/sound.json');

const browser = await chromium.launch({ args: ['--allow-file-access-from-files', ...(process.env.RENDER_GL === 'swiftshader' ? ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] : [])] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = []; page.on('pageerror', (e) => errs.push(e.message));
await page.goto(pathToFileURL(resolve(PAGE)).href);
await page.waitForFunction(() => window.ready === true || window.__err, null, { timeout: 120000 }).catch(() => {});
const film = await page.evaluate(() => ({
  hasCues: Array.isArray(window.CUES), cues: window.CUES || [],
  fps: (window.FILM && FILM.fps) || 30,
  duration: (window.FILM && FILM.duration) || (typeof SHOTS !== 'undefined' && SHOTS.length ? Math.max(...SHOTS.map((s) => s.b)) : 0),
}));
await browser.close();
if (errs.length) { console.error('page errors:\n  ' + errs.join('\n  ')); process.exit(1); }
if (!film.hasCues) { console.error('window.CUES missing — add <script src="cues.js"></script> after core.js/fx.js in ' + PAGE); process.exit(1); }

const cfg = existsSync(CFG) ? JSON.parse(readFileSync(CFG, 'utf8')) : {};
const extra = (cfg.cues_extra || []).map((c) => ({ ...c, src: c.src || 'audio/sound.json cues_extra' }));
delete cfg.cues_extra;
const fps = film.fps, T = +(cfg.duration_s || film.duration).toFixed(3);
const frameOf = (c) => (c.frame !== undefined ? c.frame : Math.round(c.t * fps));
const cues = [...film.cues, ...extra].sort((a, b) => frameOf(a) - frameOf(b));

// validation
const bad = [], warn = [], ids = new Set(), V = new Set(['cut', 'move', 'land', 'appear']);
for (const c of cues) {
  if (ids.has(c.id)) bad.push(`duplicate id '${c.id}'`); ids.add(c.id);
  if (!c.sound) bad.push(`${c.id}: no sound`);
  if (c.visual !== undefined && !V.has(c.visual)) bad.push(`${c.id}: visual '${c.visual}' not in cut|move|land|appear`);
  const f = frameOf(c); if (!(f >= 1 && f < Math.round(T * fps))) bad.push(`${c.id}: frame ${f} outside the film (1…${Math.round(T * fps) - 1})`);
  if (/^synth:(?!pluck|bell)/.test(c.sound || '')) bad.push(`${c.id}: only synth:pluck / synth:bell exist — never synthesize hits, clicks or whooshes`);
}
const heroes = cues.filter((c) => c.weight === 'hero');
for (let i = 1; i < heroes.length; i++) {
  const gap = (frameOf(heroes[i]) - frameOf(heroes[i - 1])) / fps;
  if (gap < 3.5) warn.push(`heroes '${heroes[i - 1].id}' and '${heroes[i].id}' are ${gap.toFixed(2)} s apart (aim for one hero per ~4 s)`);
}
if (!heroes.length) warn.push('no hero cue (logo / reveal): add cue.hero(...)');
const untagged = cues.filter((c) => !c.visual && c.weight !== 'hero').length;

const out = { fps, duration_s: T, energy: 'punchy', kit: 'audio/kit', ...cfg, cues };
mkdirSync(dirname(resolve(OUT)), { recursive: true });
writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
console.log(`${cues.length} cues (${heroes.length} hero, ${untagged} without a visual tag) · ${fps} fps · ${T} s → ${OUT}`);
for (const c of cues) console.log(`  f${String(frameOf(c)).padStart(5)}  ${(frameOf(c) / fps).toFixed(3).padStart(7)}s  ${(c.visual || '-').padEnd(6)} ${(c.weight || 'support').padEnd(7)} ${String(c.sound).padEnd(22)} ${c.id}${c.src ? '   ← ' + c.src : ''}`);
for (const w of warn) console.log('WARN ' + w);
if (bad.length) { console.error('FAIL\n  ' + bad.join('\n  ')); process.exit(1); }
