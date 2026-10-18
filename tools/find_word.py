#!/usr/bin/env python3
"""Find when words are spoken: python3 tools/find_word.py docs/vo_word_timings.json كلمة [كلمة2 ...]
Strips Arabic diacritics/tatweel for matching. Use the printed start times as shot/keyframe anchors."""
import sys, json, re
strip = lambda s: re.sub(r'[\u064B-\u0652\u0670\u0640\u060C\u061F.,!?«»"]', '', s).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
data = json.load(open(sys.argv[1]))
for q in sys.argv[2:]:
    for seg in data:
        for w in seg.get('words', []):
            ww = w.get('w', w.get('word', '')); st = w.get('s', w.get('start'))
            if strip(q) in strip(ww): print(f"{q}\t{st:.2f}\t{ww}\t| {seg['text'][:70]}")
