// Regenerate the auto-generated dictionary sections from the code/data (run from repo root):
//   node tools/build_docs.mjs   →  library/motion_recipes.md (table part) · library/gl_transitions.md (catalogue part) · library/icons.md (category index)
// Hand-written parts live above the "<!-- AUTO -->" marker in each file and are preserved.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import vm from 'node:vm';
const ctx = { clamp: (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), rng: s => () => ((s = s * 16807 % 2147483647) / 2147483647), window: {}, console };
vm.createContext(ctx);
vm.runInContext(readFileSync('engine/moves.js', 'utf8') + '\n;this.MOVES = MOVES;', ctx);
vm.runInContext(readFileSync('engine/kit/data/gl_transitions.js', 'utf8'), ctx);
vm.runInContext(readFileSync('engine/kit/data/icons_lucide.js', 'utf8'), ctx);
const keep = (file, auto) => { const head = existsSync(file) ? readFileSync(file, 'utf8').split('<!-- AUTO -->')[0] : `# ${file}\n\n`; writeFileSync(file, head + '<!-- AUTO -->\n' + auto); console.log('wrote', file); };

// 1 · MOVES table
{ const T = { in: 'Entrances', out: 'Exits', emph: 'Emphasis (element already on screen)', loop: 'Loops (ambient, u = seconds)' }; let s = '';
  for (const [type, title] of Object.entries(T)) { const rows = Object.entries(ctx.MOVES).filter(([, m]) => m.type === type);
    s += `\n### ${title} — ${rows.length}\n\n| move | default dur | what it does / when |\n|---|---|---|\n` + rows.map(([n, m]) => `| \`${n}\` | ${m.dur ? m.dur + 's' : '∞'} | ${m.note} |`).join('\n') + '\n'; }
  keep('library/motion_recipes.md', `## Full MOVES dictionary (generated from engine/moves.js — ${Object.keys(ctx.MOVES).length} moves)\nVisual strips: [moves_in](specimens/moves_in.jpg) · [moves_out](specimens/moves_out.jpg) · [moves_emph](specimens/moves_emph.jpg) · [moves_loop](specimens/moves_loop.jpg)\n` + s); }

// 2 · gl-transitions catalogue
{ const S = ctx.window.GLT_SRC, uni = src => [...src.matchAll(/uniform\s+(\w+)\s+(\w+)\s*(?:\/\*\s*=\s*([^*]+?)\s*\*\/)?\s*;\s*(?:\/\/\s*=\s*([^\n;]+))?/g)].map(m => `${m[2]}${(m[3] || m[4]) ? '=' + (m[3] || m[4]).trim() : ''}`);
  const rows = Object.entries(S).map(([n, o]) => `| \`gl:${n}\` | ${o.desc.replace(/\|/g, '/') || '—'} | ${o.author.replace(/\|/g, '/')} | ${o.license} | ${uni(o.glsl).join(', ').replace(/\|/g, '/') || '—'} |`);
  keep('library/gl_transitions.md', `## Catalogue (generated from engine/kit/data/gl_transitions.js — ${rows.length} transitions)\nContact sheet at progress .5: [specimens/gl_transitions.jpg](specimens/gl_transitions.jpg)\n\n| shot.tin | description | author | licence | uniforms (= default) → shot.glParams |\n|---|---|---|---|---|\n` + rows.join('\n') + '\n'); }

// 3 · icon index by category
{ const T = ctx.window.LUCIDE_TAGS, cats = {};
  for (const [n, t] of Object.entries(T)) { const words = t.split(' '); const known = ['accessibility','account','animals','arrows','brands','buildings','charts','communication','connectivity','cursors','design','development','devices','emoji','files','finance','food-beverage','gaming','home','layout','mail','math','medical','multimedia','nature','navigation','notifications','people','photography','science','seasons','security','shapes','shopping','social','sports','sustainability','text','time','tools','transportation','travel','weather'];
    for (const w of words) if (known.includes(w)) (cats[w] = cats[w] || []).push(n); }
  const s = Object.keys(cats).sort().map(c => `<details><summary><b>${c}</b> (${cats[c].length})</summary>\n\n${[...new Set(cats[c])].map(n => '`' + n + '`').join(' ')}\n\n</details>`).join('\n');
  keep('library/icons.md', `## Index by category (generated — ${Object.keys(ctx.window.LUCIDE).length} icons; an icon can be in several categories)\n\n` + s + '\n'); }
