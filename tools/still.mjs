// PAGE=index.html node ../tools/still.mjs t1 t2 ...  -> tmp/still_<t>.png  (run from the film folder)
import { chromium } from 'playwright';
import { resolve } from 'node:path'; import { mkdirSync, writeFileSync } from 'node:fs'; import { pathToFileURL } from 'node:url';
mkdirSync('tmp', { recursive: true });
const ts = process.argv.slice(2).map(Number);
const b = await chromium.launch({ args: ['--allow-file-access-from-files', ...(process.env.RENDER_GL === 'swiftshader' ? ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] : [])] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', m => console.log('console:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto(pathToFileURL(resolve(process.env.PAGE || 'index.html')).href);
await p.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
for (const t of ts) { const t0 = Date.now(); await p.evaluate(t => window.seek(t), t);
  // read the canvas at its native size (works for 16:9, 9:16, 1:1 …) — no viewport scaling
  const b64 = await p.evaluate(() => document.querySelector('canvas').toDataURL('image/png').slice(22));
  writeFileSync(`tmp/still_${t.toFixed(2).padStart(7, "0")}.png`, Buffer.from(b64, 'base64')); console.log('t', t, Date.now() - t0, 'ms'); }
await b.close();
