// LEGACY (pre-2.0). Do NOT use for hits, clicks or whooshes: the SOUND LAYER uses real CC0 recordings
// (workflow/10_sound_layer.md). Kept for old projects and for abstract drone beds only.
// node tools/sfx.mjs cues.json tmp/sfx.wav [duration]
// Synthesised SFX bed: click tick pop thump stamp whoosh paper snap scratch chime + 'swell' (drone swells) + low drone.
// cue = {t, type, gain?, pan?(-1..1), len?, pitch?}
// Pure synthesis, seeded noise -> identical output every run.
import { readFileSync, writeFileSync } from 'node:fs';
const SR = 48000;
const cues = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const DUR = Number(process.argv[4] || Math.max(...cues.map(c => c.t + (c.len || 1))) + 1.5);
const L = new Float32Array(Math.ceil(DUR * SR)), R = new Float32Array(L.length);
let s = 42; const noise = () => (s = (s * 1664525 + 1013904223) >>> 0) / 2147483648 - 1;

// one-pole filters
const lp = (a) => { let y = 0; return x => (y += a * (x - y)); };
const hp = (a) => { let y = 0, px = 0; return x => { y = a * (y + x - px); px = x; return y; }; };

const VOICES = {
  click: (n) => { const f = []; for (let i = 0; i < .05 * SR; i++) { const t = i / SR; f.push(Math.sin(2 * Math.PI * 2100 * t) * Math.exp(-t * 110) * .35); } return f; },
  tick: (n) => { const f = [], h = hp(.6); for (let i = 0; i < .06 * SR; i++) { const t = i / SR; f.push((h(noise()) * .6 + Math.sin(2 * Math.PI * 3200 * t) * .3) * Math.exp(-t * 140) * .5); } return f; },
  pop: (n, c) => { const f = [], p = c.pitch || 1; for (let i = 0; i < .14 * SR; i++) { const t = i / SR; f.push(Math.sin(2 * Math.PI * (520 + 800 * t) * p * t) * Math.exp(-t * 34) * .32); } return f; },
  thump: (n, c) => { const f = [], g = c.gain || 1; for (let i = 0; i < .7 * SR; i++) { const t = i / SR; f.push((Math.sin(2 * Math.PI * (75 - 40 * t) * t) * Math.exp(-t * 7) + Math.sin(2 * Math.PI * 150 * t) * Math.exp(-t * 30) * .3) * .8 * g); } return f; },
  stamp: (n, c) => { const f = [], l = lp(.25), g = c.gain || 1; for (let i = 0; i < .5 * SR; i++) { const t = i / SR;
      f.push((Math.sin(2 * Math.PI * (95 - 50 * t) * t) * Math.exp(-t * 11) * .9 + l(noise()) * Math.exp(-t * 45) * 1.2) * g); } return f; },
  whoosh: (n, c) => { const len = c.len || .45, f = [], l = lp(.06), h = hp(.95); for (let i = 0; i < len * SR; i++) { const t = i / SR, k = t / len;
      const env = Math.pow(Math.sin(Math.PI * Math.min(1, k)), 1.6); const cut = .02 + .12 * Math.sin(Math.PI * k);
      f.push(h(l(noise())) * env * .55 * (c.gain || 1) * (1 + cut * 3)); } return f; },
  paper: (n, c) => { const len = c.len || .22, f = [], h = hp(.7), l = lp(.5); for (let i = 0; i < len * SR; i++) { const t = i / SR;
      const crackle = (noise() > .93 ? 1 : .25); f.push(l(h(noise())) * crackle * Math.exp(-t * (8 / len)) * .7 * (c.gain || 1)); } return f; },
  snap: (n) => { const f = [], h = hp(.9); for (let i = 0; i < .12 * SR; i++) { const t = i / SR; f.push((h(noise()) * .7 + Math.sin(2 * Math.PI * 900 * t) * .2) * Math.exp(-t * 60) * .55); } return f; },
  scratch: (n, c) => { // reed pen on burnished paper: band-passed noise with stroke-rate amplitude modulation
      const len = c.len || 1.5, f = [], h = hp(.8), l = lp(.35); for (let i = 0; i < len * SR; i++) { const t = i / SR;
      const strokes = .55 + .45 * Math.sin(2 * Math.PI * 2.6 * t + Math.sin(t * 7) * 1.5);
      const grain = noise() > .97 ? 2.2 : 1; const env = Math.min(1, t / .05) * Math.min(1, (len - t) / .12);
      f.push(l(h(noise())) * strokes * grain * env * .32 * (c.gain || 1)); } return f; },
  chime: (n, c) => { const f = []; for (let i = 0; i < 1.6 * SR; i++) { const t = i / SR;
      f.push((Math.sin(2 * Math.PI * 1318 * t) * .5 + Math.sin(2 * Math.PI * 1975 * t) * .25 + Math.sin(2 * Math.PI * 2637 * t) * .12) * Math.exp(-t * 3.2) * .16 * (c.gain || 1)); } return f; },
};
for (const c of cues) {
  if (!VOICES[c.type]) continue;
  const f = VOICES[c.type](0, c), st = Math.floor(c.t * SR), pan = c.pan ?? 0;
  const gl = Math.cos((pan + 1) * Math.PI / 4), gr = Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < f.length && st + i < L.length; i++) { L[st + i] += f[i] * gl * 1.41; R[st + i] += f[i] * gr * 1.41; }
}
// drone bed: low fifth + breathing filtered noise, swells at given times
const swells = cues.filter(c => c.type === 'swell').map(c => c.t);
const dl = lp(.004), dr = lp(.004);
for (let i = 0; i < L.length; i++) {
  const t = i / SR;
  let sw = 0; for (const w of swells) if (t > w) sw += Math.exp(-(t - w) * .9) * Math.min(1, (t - w) * 8);
  const fade = Math.min(1, t / 1.5) * Math.min(1, (DUR - t) / 1.2);
  const tone = Math.sin(2 * Math.PI * 55 * t) * .5 + Math.sin(2 * Math.PI * 82.4 * t) * .3 + Math.sin(2 * Math.PI * 110 * t + Math.sin(t * .5)) * .12;
  const lfo = .75 + .25 * Math.sin(2 * Math.PI * .11 * t);
  const v = (tone * .06 * lfo + 0) * (1 + sw * .9) * fade;
  L[i] += v + dl(noise()) * .05 * fade; R[i] += v + dr(noise()) * .05 * fade;
}
const n = L.length, b = Buffer.alloc(44 + n * 4);
b.write('RIFF', 0); b.writeUInt32LE(36 + n * 4, 4); b.write('WAVEfmt ', 8);
b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(2, 22);
b.writeUInt32LE(SR, 24); b.writeUInt32LE(SR * 4, 28); b.writeUInt16LE(4, 32); b.writeUInt16LE(16, 34);
b.write('data', 36); b.writeUInt32LE(n * 4, 40);
for (let i = 0; i < n; i++) {
  b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i])) * 32767), 44 + i * 4);
  b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i])) * 32767), 46 + i * 4);
}
writeFileSync(process.argv[3], b);
console.log(`wrote ${process.argv[3]} (${cues.length} cues, ${DUR.toFixed(2)}s)`);
