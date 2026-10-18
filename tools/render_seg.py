#!/usr/bin/env python3
"""Crash-safe chunked render of one film part (run from the film folder):
   PAGE=index.html VO=tmp/vo.wav SFX=tmp/sfx.wav python3 ../tools/render_seg.py NAME F0 F1
F0/F1 are frame numbers at FPS (default 30). Renders 6 s chunks in fresh browsers (retry ×4),
skips chunks already done (resume after crash/reset), concatenates by stream copy →
renders/silent_NAME.mp4, then muxes a preview mix (VO + SFX ducked, -14 LUFS) → segments/NAME.mp4"""
import sys, subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
name, f0, f1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
FPS = int(os.environ.get('FPS', 30)); CH = FPS * 6
VO, SFX = os.environ.get('VO', 'tmp/vo.wav'), os.environ.get('SFX', 'tmp/sfx.wav')
for d in ('tmp/chunks', 'segments', 'renders'): os.makedirs(d, exist_ok=True)
parts = []
for a in range(f0, f1, CH):
    b = min(a + CH, f1); out = f'tmp/chunks/{name}_{a:05d}.mp4'; parts.append(out)
    if os.path.exists(out) and os.path.getsize(out) > 1000: continue
    for attempt in range(4):
        r = subprocess.run(['node', f'{here}/render.mjs', '--fps', str(FPS), '--from', f'{a/FPS:.6f}', '--to', f'{b/FPS:.6f}', '--sub', '2', '--crf', '20', '--out', out + '.part.mp4'])
        if r.returncode == 0: os.rename(out + '.part.mp4', out); break
        print('retry', out, attempt, flush=True)
    else: sys.exit('chunk failed ' + out)
with open(f'tmp/chunks/{name}.txt', 'w') as f: f.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
sil = f'renders/silent_{name}.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'tmp/chunks/{name}.txt', '-c', 'copy', sil], check=True)
A, D = f0 / FPS, (f1 - f0) / FPS
if os.path.exists(VO):
    ins = ['-i', sil, '-ss', f'{A}', '-t', f'{D}', '-i', VO]
    if os.path.exists(SFX):
        ins += ['-ss', f'{A}', '-t', f'{D}', '-i', SFX]
        fc = '[2:a]volume=0.5[s];[s][1:a]sidechaincompress=threshold=0.05:ratio=3[sc];[1:a][sc]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]'
    else: fc = '[1:a]loudnorm=I=-14:TP=-1.5[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', f'segments/{name}.mp4'], check=True)
else:
    subprocess.run(['cp', sil, f'segments/{name}.mp4'], check=True)
for p in parts: os.remove(p)
os.remove(f'tmp/chunks/{name}.txt')
print('DONE', name, f'segments/{name}.mp4', flush=True)
