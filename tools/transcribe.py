#!/usr/bin/env python3
"""Word-level VO timings — the film's master clock.
usage: python3 tools/transcribe.py assets/vo.mp3 docs/vo_word_timings.json [lang=ar] [model=medium]
Needs: pip install faster-whisper  (CPU int8 is fine; ~1× realtime for 'small', slower for 'medium').
Output: [{s,e,text,words:[{w,s,e}]}] + a readable docs/vo_timeline.md with one line per segment.
Note: faster-whisper may fail on mp3 paths in some sandboxes → we decode with ffmpeg to float32 first."""
import argparse, json, subprocess, numpy as np
ap = argparse.ArgumentParser(description='Create word-level voice-over timings for Motion-Doc Studio.')
ap.add_argument('src', help='input audio/video file')
ap.add_argument('out', help='output JSON path')
ap.add_argument('lang', nargs='?', default='ar', help='Whisper language code (default: ar)')
ap.add_argument('model', nargs='?', default='medium', help='faster-whisper model size (default: medium)')
args = ap.parse_args()
src, out, lang, size = args.src, args.out, args.lang, args.model
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.float32)
from faster_whisper import WhisperModel
m = WhisperModel(size, device='cpu', compute_type='int8')
segs, info = m.transcribe(audio, language=lang, word_timestamps=True, vad_filter=True)
res = []
for s in segs:
    res.append(dict(s=round(s.start, 2), e=round(s.end, 2), text=s.text.strip(), words=[dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for w in (s.words or [])]))
    print(f"{s.start:7.2f}–{s.end:7.2f}  {s.text.strip()}", flush=True)
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
md = out.rsplit('.', 1)[0].replace('word_timings', 'timeline') + '.md'
with open(md, 'w') as f:
    f.write(f"# VO timeline ({len(audio)/16000:.2f} s)\n\n| start | end | text |\n|---|---|---|\n")
    for r in res: f.write(f"| {r['s']:.2f} | {r['e']:.2f} | {r['text']} |\n")
print('wrote', out, md, f'duration {len(audio)/16000:.2f}s')
