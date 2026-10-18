#!/usr/bin/env bash
# Release encodes of a SOUND LAYER final, each one re-checked by qa.py (QA the file you deliver).
#   tools/encode_release.sh out/final.mp4 out/final        (run from the film folder, after qa.py passed on out/final.mp4)
#   → out/final_1080p.mp4 (crf 21, ≤3.4 Mbps)  out/final_720p.mp4 (crf 23, ≤1.7 Mbps)  audio/qa-final_*.json
# Audio is stream-copied (the mix.py master is not re-encoded or re-normalised). Video → TV range bt709.
# Why re-check: heavy compression changes qa.py's picture-motion curve. A gentle landing that passed on the
# master can fail on a CRF 26 copy. If a release file FAILs, lower its CRF, or fix the cue/picture, never the thresholds.
set -e; IN=${1:?usage: $0 out/final.mp4 OUTPREFIX}; O=${2:-out/final}
export PATH="$HOME/.local/bin:$PATH"; fail=0
enc() { ffmpeg -v error -y -i "$IN" -map 0:v -map 0:a -vf "scale=$1:in_range=pc:out_range=tv:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf "$2" -maxrate "$3" -bufsize "$4" -profile:v high -g 60 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart "$5"; }
# orientation-aware targets (reels are portrait, docs are landscape)
WH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN")
W0=${WH%,*}; H0=${WH#*,}
if [ "${H0:-0}" -gt "${W0:-0}" ]; then T1080="1080:-2"; T720="720:-2"; else T1080="1920:1080"; T720="1280:720"; fi
enc "$T1080" 21 3400k 6800k "${O}_1080p.mp4"
enc "$T720"  23 1700k 3400k "${O}_720p.mp4"
cp audio/qa-report.json /tmp/.qa_master.json 2>/dev/null || true; cp audio/qa.png /tmp/.qa_master.png 2>/dev/null || true
for f in "${O}_1080p.mp4" "${O}_720p.mp4"; do
  n=$(basename "$f" .mp4); r=$(uv run sound-layer/scripts/qa.py "$f" 2>&1) || true
  cp audio/qa-report.json "audio/qa-$n.json"
  echo "$r" | grep -v '^pass' | sed "s|^|[$n] |"
  echo "$r" | grep -q '^FAIL' && fail=1
  echo "[$n] $(du -h "$f" | cut -f1)"
done
cp /tmp/.qa_master.json audio/qa-report.json 2>/dev/null || true; cp /tmp/.qa_master.png audio/qa.png 2>/dev/null || true
[ $fail = 0 ] && echo "release encodes pass qa.py" || { echo "a release encode FAILED qa.py, so don't ship it"; exit 1; }
