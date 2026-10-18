#!/usr/bin/env python3
"""LEGACY (pre-2.0): use engine/cues.js + tools/export_cues.mjs (workflow/10_sound_layer.md).
Auto-derive an SFX cue sheet from scene code, then merge hand-placed cues.
usage: python3 tools/cues_auto.py "scenes/*.js" extra_cues.json out_cues.json
Detects: SHOTS a: (transition → paper tear + whoosh + thump), drawCard(..., t, T0 (paper + thump + pen scratch),
dropP(..., t, T0 (paper + soft thump), nameBlock(..., t, T0 (pen scratch + chime).
Add signature moments by hand in extra_cues.json: [{"t":12.9,"type":"stamp","gain":0.6}, ...]."""
import sys, re, json, glob
src = ''.join(open(f).read() for f in sorted(glob.glob(sys.argv[1])))
extra = json.load(open(sys.argv[2])) if len(sys.argv) > 3 else []
out = sys.argv[-1]; N = []
a = lambda t, ty, **k: N.append(dict(t=round(t, 3), type=ty, **k))
shots = sorted(set(float(x) for x in re.findall(r'a:\s*([\d.]+),\s*b:', src)))
for s in shots[1:]: a(s, 'paper', len=.6, gain=.8); a(s, 'whoosh', len=.6, gain=.4); a(s + .25, 'thump', gain=.3)
for i, t0 in enumerate(sorted(set(float(x) for x in re.findall(r'drawCard\([^,]+,\s*t,\s*([\d.]+)', src)))):
    pan = .4 if i % 2 else -.2; a(t0 + .05, 'paper', len=.22, gain=.6, pan=pan); a(t0 + .2, 'thump', gain=.25, pan=pan); a(t0 + .15, 'scratch', len=.5, gain=.25, pan=pan)
for t0 in sorted(set(float(x) for x in re.findall(r'dropP\([^,]+,\s*t,\s*([\d.]+)', src))): a(t0 + .05, 'paper', len=.3, gain=.5); a(t0 + .25, 'thump', gain=.3)
for t0 in sorted(set(float(x) for x in re.findall(r'nameBlock\([^,]+,\s*t,\s*([\d.]+)', src))): a(t0, 'scratch', len=1.0, gain=.4); a(t0 + .1, 'chime', gain=.3)
cues = sorted(N + extra, key=lambda c: c['t'])
json.dump(cues, open(out, 'w'), indent=0); print(f'{len(N)} auto + {len(extra)} manual cues → {out}')
