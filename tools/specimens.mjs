// Regenerate the visual specimen sheets in library/specimens/ from engine/specimens.html.
//   node tools/specimens.mjs [fonts palettes icons patterns moves gl]     (run from repo root; default = all)
import { chromium } from 'playwright';
import { resolve } from 'node:path'; import { mkdirSync, writeFileSync } from 'node:fs'; import { pathToFileURL } from 'node:url';
const OUT = 'library/specimens'; mkdirSync(OUT, { recursive: true });
const want = new Set(process.argv.slice(2).length ? process.argv.slice(2) : ['fonts', 'palettes', 'icons', 'patterns', 'moves', 'gl']);
const b = await chromium.launch({ args: ['--allow-file-access-from-files', ...(process.env.RENDER_GL === 'swiftshader' ? ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] : [])] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', m => { if (/GLFAIL|Error/.test(m.text())) console.log('console:', m.text()); }); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto(pathToFileURL(resolve('engine/specimens.html')).href); await p.waitForFunction(() => window.ready === true);
const save = async (name, js, arg) => { const d = await p.evaluate(js, arg); writeFileSync(`${OUT}/${name}.jpg`, Buffer.from(d.split(',')[1], 'base64')); console.log('wrote', name); };
if (want.has('fonts')) await save('fonts', () => spec.fonts());
if (want.has('palettes')) await save('palettes', () => spec.palettes());
if (want.has('icons')) { await save('icons', () => spec.icons(0, 240)); await save('icons_drawon', () => spec.drawOn()); }
if (want.has('patterns')) await save('patterns', () => spec.patterns());
if (want.has('moves')) for (const t of ['in', 'out', 'emph', 'loop']) await save('moves_' + t, t2 => spec.moves(t2), t);
if (want.has('gl')) await save('gl_transitions', () => spec.gl(.5));
await b.close();
