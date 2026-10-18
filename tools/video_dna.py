#!/usr/bin/env python3
"""Reference-video DNA extractor — measure a reference instead of guessing it.
   python3 tools/video_dna.py REF.mp4 OUTDIR [--fps-sheet 4] [--colors 10]
Writes OUTDIR/{report.md, metrics.json, contact_*.jpg, shots.jpg}. Never copies the video itself.
Measures: format + letterbox, hard cuts, animated transitions (multi-frame energy events),
flash / strobe frames, camera motion (median optical flow, needs opencv), shot lengths & rhythm,
palette (k-means, % coverage, OKLCH lightness), loudness (EBU R128), VO/music balance, audio onsets.
Then YOU watch the sheets and fill the qualitative half (type, layout, characters, graphic vocabulary)
using workflow/09_reference_dna.md."""
import sys, os, json, subprocess, argparse, math, shlex
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--fps-sheet', type=float, default=4); ap.add_argument('--colors', type=int, default=10)
ap.add_argument('--cut', type=float, default=60, help='mean abs diff (0-255) that counts as a hard cut')
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); O = lambda f: os.path.join(a.out, f)
sh = lambda c: subprocess.run(c, shell=True, capture_output=True, text=True)
SRC = shlex.quote(os.path.abspath(a.src))
Q = lambda p: shlex.quote(os.path.abspath(p))

# ── format ──
pr = json.loads(sh(f'ffprobe -v error -show_streams -show_format -of json {SRC}').stdout)
v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); has_audio = any(s['codec_type'] == 'audio' for s in pr['streams'])
Wv, Hv = int(v['width']), int(v['height']); num, den = map(int, v['r_frame_rate'].split('/')); FPS = num / den; DUR = float(pr['format']['duration'])

# ── decode all frames small (gray + colour) ──
SW = 240; SH = int(round(Hv * SW / Wv / 2)) * 2
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-vf', f'scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
F = np.frombuffer(p.stdout, np.uint8).reshape(-1, SH, SW, 3); N = len(F)

# letterbox / pillarbox: rows/cols that are ~black in 95 % of frames (memory-light: per-frame float32)
gray = lambda fr: fr.astype(np.float32) @ np.array([.299, .587, .114], np.float32)
smp = F[::max(1, N // 80)]; rl = np.stack([gray(f).mean(1) for f in smp]); cl = np.stack([gray(f).mean(0) for f in smp])
rows = np.where(np.percentile(rl, 95, axis=0) > 10)[0]; cols = np.where(np.percentile(cl, 95, axis=0) > 10)[0]
y0, y1, x0, x1 = rows.min(), rows.max() + 1, cols.min(), cols.max() + 1
F = F[:, y0:y1, x0:x1]; G = np.stack([gray(f) for f in F])
act_w, act_h = (x1 - x0) * Wv / SW, (y1 - y0) * Hv / SH; aspect = act_w / act_h
boxed = (y1 - y0) < SH * .95 or (x1 - x0) < SW * .95

# ── per-frame metrics ──
diff = np.zeros(N); diff[1:] = np.abs(G[1:] - G[:-1]).mean((1, 2)); lum = G.mean((1, 2))
flow = np.zeros((N, 2))
try:
    import cv2
    for i in range(1, N):
        fl = cv2.calcOpticalFlowFarneback(G[i - 1].astype(np.uint8), G[i].astype(np.uint8), None, .5, 3, 15, 3, 5, 1.2, 0)
        flow[i] = np.median(fl[..., 0]), np.median(fl[..., 1])
    has_flow = True
except Exception: has_flow = False

# hard cuts: single-frame spikes; transitions: runs of elevated diff ≥3 frames
cuts = [i for i in range(1, N) if diff[i] > a.cut and (i + 1 >= N or diff[i + 1] < a.cut * .6)]
ev, run = [], []
for i in range(1, N):
    if diff[i] > 8 and i not in cuts: run.append(i)
    elif run:
        if len(run) >= 3: ev.append(run)
        run = []
trans = [{'t0': r[0] / FPS, 't1': (r[-1] + 1) / FPS, 'frames': len(r), 'peak': float(diff[r].max()),
          'flow_x': float(flow[r, 0].mean()), 'flow_y': float(flow[r, 1].mean()), 'lum_delta': float(lum[r[-1]] - lum[r[0] - 1])} for r in ev]
flashes = [i / FPS for i in range(1, N - 1) if lum[i] - max(lum[i - 1], lum[i + 1]) > 30 or (i + 3 < N and lum[i] - lum[i - 1] > 30 and lum[i + 3] - lum[i] < -30 and abs(lum[i + 3] - lum[i - 1]) < 25)]
strobe = [i / FPS for i in range(2, N - 2) if (lum[i] - lum[i - 1]) * (lum[i + 1] - lum[i]) < -400]
bounds = [0] + [c / FPS for c in cuts] + [DUR]; shots = [round(bounds[i + 1] - bounds[i], 2) for i in range(len(bounds) - 1)]

# ── palette ──
px = F[::max(1, N // 60), ::3, ::3].reshape(-1, 3).astype(np.float32)
try:
    from sklearn.cluster import KMeans
    km = KMeans(a.colors, n_init=4, random_state=0).fit(px); C, lab = km.cluster_centers_, km.labels_
except Exception:
    q = Image.fromarray(px.reshape(-1, 1, 3).astype(np.uint8)).quantize(a.colors); C = np.array(q.getpalette()[:a.colors * 3]).reshape(-1, 3); lab = np.array(q).ravel()
cnt = np.bincount(lab, minlength=len(C))
def okL(c):
    r, g, b = [((x / 255) / 12.92 if x / 255 <= .04045 else (((x / 255) + .055) / 1.055) ** 2.4) for x in c]
    l, m, s = [v ** (1 / 3) for v in (.4122 * r + .5363 * g + .0514 * b, .2119 * r + .6807 * g + .1074 * b, .0883 * r + .2817 * g + .6300 * b)]
    L, A, B = .2105 * l + .7936 * m - .0041 * s, 1.978 * l - 2.4286 * m + .4506 * s, .0259 * l + .7828 * m - .8087 * s
    return round(float(L), 3), round(float(math.hypot(A, B)), 3), int(round(math.degrees(math.atan2(B, A)) % 360))
palette = [{'hex': '#%02x%02x%02x' % tuple(int(x) for x in c), 'pct': round(100 * n / cnt.sum(), 1), 'oklch': okL(c)} for n, c in sorted(zip(cnt, C), key=lambda z: -z[0])]

# ── audio ──
audio = {}
if has_audio:
    e = sh(f'ffmpeg -nostats -i {SRC} -af ebur128=peak=true -f null - 2>&1').stdout + sh(f'ffmpeg -nostats -i {SRC} -af ebur128=peak=true -f null - 2>&1').stderr
    import re
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', e); LRA = re.findall(r'LRA:\s+([\d.]+) LU', e); TP = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)
    audio = {'lufs': float(I[-1]) if I else None, 'lra': float(LRA[-1]) if LRA else None, 'true_peak': float(TP[-1]) if TP else None}
    w = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    hop = 160; en = np.array([np.sqrt((w[i:i + 400] ** 2).mean() + 1e-12) for i in range(0, len(w) - 400, hop)]); db = 20 * np.log10(en + 1e-6)
    fl = np.maximum(0, np.diff(db)); on = [i * .01 for i in range(2, len(fl) - 2) if fl[i] > 6 and fl[i] == fl[i - 2:i + 3].max()]
    bands = []
    for s0 in range(0, int(len(w) / 16000), 2):
        seg = w[s0 * 16000:(s0 + 2) * 16000]
        if len(seg) < 1600: break
        S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))); f = np.fft.rfftfreq(len(seg), 1 / 16000); tot = S.sum() + 1e-9
        bands.append({'t': s0, 'bass': round(float(S[f < 150].sum() / tot), 2), 'voice': round(float(S[(f > 300) & (f < 3000)].sum() / tot), 2), 'rms_db': round(float(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)), 1)})
    audio.update({'onsets': [round(x, 2) for x in on], 'onsets_per_s': round(len(on) / DUR, 2), 'bands_2s': bands})

# ── sheets ──
crop = f'crop={act_w:.0f}:{act_h:.0f}:{x0 * Wv / SW:.0f}:{y0 * Hv / SH:.0f}'
n_sheet = int(DUR * a.fps_sheet); per = 42
for k in range(0, n_sheet, per):
    t0 = k / a.fps_sheet; t1 = min(DUR, (k + per) / a.fps_sheet)
    sh(f'ffmpeg -v error -y -ss {t0} -t {t1 - t0} -i {SRC} -vf "{crop},fps={a.fps_sheet},scale=320:-2,drawtext=text=\'%{{pts\\:flt}}\':x=4:y=4:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x7:padding=3" -frames:v 1 -q:v 4 {Q(O(f"contact_{t0:05.1f}s.jpg"))}')
mids = [(bounds[i] + bounds[i + 1]) / 2 for i in range(len(bounds) - 1)]
tmp = O('_k'); os.makedirs(tmp, exist_ok=True)
for j, t in enumerate(mids): sh(f'ffmpeg -v error -y -ss {t:.3f} -i {SRC} -frames:v 1 -vf "{crop},scale=480:-2" {Q(os.path.join(tmp, f"k{j:03d}.png"))}')
cols_ = min(4, max(1, len(mids))); sh(f'ffmpeg -v error -y -pattern_type glob -i {Q(tmp)}/k*.png -vf "tile={cols_}x{math.ceil(len(mids) / cols_)}:padding=4" -frames:v 1 -q:v 3 {Q(O("shots.jpg"))}')
for f_ in os.listdir(tmp): os.remove(os.path.join(tmp, f_))
os.rmdir(tmp)

M = {'src': os.path.basename(a.src), 'size': [Wv, Hv], 'fps': FPS, 'duration': DUR, 'active_area': [round(act_w), round(act_h)], 'aspect_active': round(aspect, 3), 'boxed': bool(boxed),
     'cuts': [round(c / FPS, 3) for c in cuts], 'shot_lengths': shots, 'mean_shot': round(float(np.mean(shots)), 2), 'transitions': trans, 'flash_frames': flashes, 'strobe_frames': strobe,
     'palette': palette, 'audio': audio, 'optical_flow': has_flow}
json.dump(M, open(O('metrics.json'), 'w'), indent=1, default=float)
L = [f"# DNA report — {M['src']}", '', '## Measured (tools/video_dna.py)', f"- {Wv}×{Hv} @ {FPS:g} fps, {DUR:.2f} s" + (f"; active picture {M['active_area'][0]}×{M['active_area'][1]} (aspect {aspect:.2f}) — letter/pillar-boxed" if boxed else ''),
     f"- {len(shots)} shots, mean {M['mean_shot']} s (min {min(shots)}, max {max(shots)}); hard cuts at {', '.join(f'{c:.2f}' for c in M['cuts'])}",
     f"- {len(trans)} animated transitions/moves: " + '; '.join(f"{t['t0']:.2f}–{t['t1']:.2f}s ({t['frames']}f, Δlum {t['lum_delta']:+.0f}{', flow %.1f,%.1f' % (t['flow_x'], t['flow_y']) if has_flow else ''})" for t in trans),
     f"- flash frames: {', '.join(f'{x:.2f}' for x in flashes) or 'none'}; strobe frames: {len(strobe)}", '', '| colour | coverage | OKLCH (L C H) |', '|---|---|---|']
L += [f"| `{c['hex']}` | {c['pct']} % | {c['oklch']} |" for c in palette]
if audio: L += ['', f"- loudness {audio['lufs']} LUFS, LRA {audio['lra']} LU, true peak {audio['true_peak']} dBFS; {audio['onsets_per_s']} audio onsets/s",
                '- 2 s bands (bass<150 Hz / voice 300–3k / RMS): ' + ' · '.join(f"{b['t']}s {b['bass']}/{b['voice']}/{b['rms_db']}" for b in audio['bands_2s'])]
L += ['', '## Observed (fill in by watching the sheets — see workflow/09_reference_dna.md)', '- Format & framing:', '- Typography (faces, roles, emphasis system):', '- Colour roles (60/30/10):',
      '- Character / subject treatment:', '- Layout grid & recurring compositions:', '- Motion grammar (entrances, springs, camera):', '- Transition toolbox:', '- Graphic vocabulary:', '- Sound design:',
      '- What to ADOPT (grammar) / what NOT to copy (content, characters, brand, jokes):']
open(O('report.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:8])); print('→', a.out)
