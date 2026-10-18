// motion-doc-studio · render.mjs v2 — deterministic frame renderer (page must expose window.ready + window.seek(t))
//
//   PAGE=index.html node ../tools/render.mjs --from 0 --to 20.8 --out out/silent.mp4        (run from the film folder)
//   … --draft                 fast preview: 1 sub-frame, 960px wide, veryfast x264   (~6-10x faster than final)
//   … --workers 4|auto        split the range into parallel browser workers, then lossless concat (auto = by CPU + RAM)
//   env: RENDER_WORKERS=auto  RENDER_DRAFT=1  RENDER_GL=swiftshader  (also honoured through tools/render_seg.py)
//   … --sub 2                 sub-frames per output frame blended (tmix) → natural motion blur (final default 2)
//   … --gl auto|cpu|swiftshader   raster backend (auto = Chromium default; swiftshader = legacy, ~5x slower)
//   … --capture canvas|screenshot  canvas = read pixels straight from the page canvas (default, fastest)
//
// Why it used to be slow (measured, workflow/11_render_speed.md): the old launch flags forced *2D canvas* through
// SwiftShader (a software GPU emulator) → ~330 ms per sub-frame at 1080p. Chromium's normal CPU raster path draws
// the same frame in ~60 ms (PSNR 43-48 dB vs old = visually identical). Workers then scale with CPU cores.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname, basename, join } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { cpus, totalmem } from 'node:os';

const argv = process.argv;
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i > 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d; };
const flag = (k) => argv.includes('--' + k);
const DRAFT = flag('draft') || process.env.RENDER_DRAFT === '1';
const FPS = +arg('fps', 30), FROM = +arg('from', 0), TO = +arg('to', 20.8);
const SUB = +arg('sub', DRAFT ? 1 : 2);
const CRF = arg('crf', DRAFT ? '24' : '18');
const PRESET = arg('preset', DRAFT ? 'veryfast' : 'medium');
const WIDTH = +arg('width', DRAFT ? 960 : 0);            // 0 = native page size
const OUT = arg('out', DRAFT ? 'out/draft.mp4' : 'out/silent.mp4');
const GL = arg('gl', 'auto'), CAPTURE = arg('capture', 'canvas');
const QUALITY = +arg('jpeg', DRAFT ? 85 : 95);
const VW = +arg('vw', 1920), VH = +arg('vh', 1080);
// each worker ≈ 1 Chromium (~250 MB) + node (~100 MB) + x264 (~150-450 MB at 1080p) → budget ~0.7 GB per worker
const ramWorkers = Math.max(1, Math.floor((totalmem() / 2 ** 30 - 0.6) / 0.7));
const autoWorkers = Math.max(1, Math.min(6, cpus().length, ramWorkers));
const wArg = arg('workers', process.env.RENDER_WORKERS || '1');
const WORKERS = wArg === 'auto' ? autoWorkers : Math.max(1, +wArg || 1);
const THREADS = +arg('threads', process.env.RENDER_THREADS || 0);   // x264 threads (0 = ffmpeg auto); workers set it per child
const IS_CHILD = flag('child');
const PAGE = process.env.PAGE || 'index.html';

mkdirSync(dirname(resolve(OUT)), { recursive: true });
const frames0 = Math.round(FROM * FPS), frames1 = Math.round(TO * FPS), nFrames = frames1 - frames0;
if (nFrames <= 0) { console.error('render.mjs: empty range'); process.exit(2); }

// ───────────────────────────── parallel orchestrator ─────────────────────────────
if (WORKERS > 1 && !IS_CHILD) {
  const n = Math.min(WORKERS, Math.max(1, Math.floor(nFrames / 15)));
  const tmp = resolve(dirname(resolve(OUT)), `.parts_${basename(OUT, '.mp4')}`);
  rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp, { recursive: true });
  const self = fileURLToPath(import.meta.url), t0 = Date.now();
  const drop = ['--from', '--to', '--out', '--workers', '--threads'];
  const pass = argv.slice(2).filter((a, i, A) => !drop.includes(a) && !drop.includes(A[i - 1]));
  const thr = String(Math.max(1, Math.floor(cpus().length / n)));
  if (n > ramWorkers) console.log(`render.mjs: warning — ${n} workers may exceed RAM (${(totalmem() / 2 ** 30).toFixed(1)} GB); safe max ≈ ${ramWorkers}`);
  const jobs = [];
  for (let k = 0; k < n; k++) {
    const a = frames0 + Math.floor(nFrames * k / n), b = frames0 + Math.floor(nFrames * (k + 1) / n);
    const part = join(tmp, `p${String(k).padStart(2, '0')}.mp4`);
    jobs.push({ part, p: new Promise((ok, bad) => {
      const c = spawn(process.execPath, [self, ...pass, '--child', '--from', String(a / FPS), '--to', String(b / FPS), '--out', part, '--threads', thr, '--quiet'], { stdio: ['ignore', 'pipe', 'inherit'], env: process.env });
      c.stdout.on('data', (d) => { const s = String(d).trim(); if (s) console.log(`[w${k}] ${s}`); });
      c.on('close', (code) => code === 0 ? ok() : bad(new Error(`worker ${k} exited ${code}`)));
    }) });
  }
  console.log(`render.mjs: ${nFrames} frames × ${SUB} sub → ${n} workers (${cpus().length} CPUs)`);
  await Promise.all(jobs.map((j) => j.p));
  writeFileSync(join(tmp, 'list.txt'), jobs.map((j) => `file '${j.part}'`).join('\n'));
  await new Promise((ok, bad) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', join(tmp, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', resolve(OUT)], { stdio: 'inherit' })
    .on('close', (c) => c === 0 ? ok() : bad(new Error('concat failed'))));
  rmSync(tmp, { recursive: true, force: true });
  const secs = (Date.now() - t0) / 1000;
  console.log(`done -> ${OUT}  ${secs.toFixed(0)}s  (${(secs / (nFrames / FPS)).toFixed(1)}s per film-second, ${n} workers)`);
  process.exit(0);
}

// ───────────────────────────── single worker ─────────────────────────────
const glArgs = { auto: [], cpu: ['--disable-gpu', '--disable-accelerated-2d-canvas'],
  swiftshader: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] }[GL] || [];
const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--disable-dev-shm-usage', ...glArgs] });
const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.log('ERR', e.message));
await page.goto(pathToFileURL(resolve(PAGE)).href);
await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
const cvs = await page.evaluate(() => { const c = document.querySelector('canvas'); return c ? [c.width, c.height] : null; });
let useCanvas = CAPTURE === 'canvas' && !!cvs && cvs[0] > 0;
if (!useCanvas && cvs && (cvs[0] !== VW || cvs[1] !== VH)) await page.setViewportSize({ width: cvs[0], height: cvs[1] });   // screenshot mode: match the canvas (9:16, 1:1 …)
const filters = [];
if (SUB > 1) filters.push(`tmix=frames=${SUB}`, `select='eq(mod(n\\,${SUB})\\,${SUB - 1})'`, `setpts=N/${FPS}/TB`);
if (WIDTH > 0) filters.push(`scale=${WIDTH}:-2:flags=lanczos`);
filters.push('scale=in_range=pc:out_range=tv', 'format=yuv420p');
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS * SUB), '-i', '-',
  '-vf', filters.join(','), '-r', String(FPS), '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-color_range', 'tv',
  ...(THREADS ? ['-threads', String(THREADS), '-filter_threads', '1', '-x264-params', 'rc-lookahead=15'] : []), '-movflags', '+faststart', resolve(OUT)],
  { stdio: ['pipe', 'inherit', 'inherit'] });
const grab = async (t) => {
  if (useCanvas) {
    const b64 = await page.evaluate(([t, q]) => { window.seek(t); return document.querySelector('canvas').toDataURL('image/jpeg', q).slice(23); }, [t, QUALITY / 100]);
    return Buffer.from(b64, 'base64');
  }
  await page.evaluate((t) => window.seek(t), t);
  return page.screenshot({ type: 'jpeg', quality: QUALITY });
};
const total = nFrames * SUB, t0 = Date.now(), quiet = flag('quiet');
for (let i = 0; i < total; i++) {
  // sub-frames are centred inside each output frame → symmetric motion blur
  const t = frames0 / FPS + (i + 0.5) / (FPS * SUB) - 0.5 / FPS;
  const jpg = await grab(Math.max(0, t));
  if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once('drain', r));
  if (i % (FPS * SUB * 2) === 0 && i > 0) {
    const el = (Date.now() - t0) / 1000, eta = el / i * (total - i);
    console.log(`${quiet ? '' : OUT + ': '}${(frames0 / FPS + i / (FPS * SUB)).toFixed(1)}s  ${(100 * i / total).toFixed(0)}%  elapsed ${el.toFixed(0)}s  eta ${eta.toFixed(0)}s`);
  }
}
ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await browser.close();
const secs = (Date.now() - t0) / 1000;
if (!quiet) console.log(`done -> ${OUT}  ${secs.toFixed(0)}s  (${(secs / (nFrames / FPS)).toFixed(1)}s per film-second)`);
if (!existsSync(resolve(OUT))) process.exit(1);
