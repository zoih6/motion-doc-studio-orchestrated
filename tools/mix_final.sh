#!/usr/bin/env bash
# Final master: ONE global audio mix over the concatenated silent video.
# usage: tools/mix_final.sh master_silent.mp4 vo.wav sfx.wav DURATION OUTPREFIX
#   → OUTPREFIX_1080p.mp4 (~3.4 Mbps, fits GitHub/WhatsApp) + OUTPREFIX_720p.mp4 + OUTPREFIX_mix.wav
set -e; V=$1; VO=$2; SFX=$3; DUR=$4; O=$5
ffmpeg -v error -y -i "$VO" -i "$SFX" -filter_complex "[1:a]volume=0.5[s];[s][0:a]sidechaincompress=threshold=0.05:ratio=3[sc];[0:a][sc]amix=inputs=2:normalize=0,atrim=0:$DUR,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[a]" -ar 48000 -c:a pcm_s16le "${O}_mix.wav"
VF="scale=in_range=pc:out_range=tv:flags=lanczos,format=yuv420p"   # screenshots are full-range JPEG → convert to TV range
ffmpeg -v error -y -i "$V" -i "${O}_mix.wav" -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset medium -crf 23 -maxrate 3400k -bufsize 6800k -profile:v high -level 4.1 -g 60 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 160k -t "$DUR" -movflags +faststart "${O}_1080p.mp4"
ffmpeg -v error -y -i "$V" -i "${O}_mix.wav" -map 0:v -map 1:a -vf "scale=1280:720:in_range=pc:out_range=tv:flags=lanczos,format=yuv420p" -c:v libx264 -preset medium -crf 24 -maxrate 1700k -bufsize 3400k -profile:v high -g 60 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 128k -t "$DUR" -movflags +faststart "${O}_720p.mp4"
ffmpeg -i "${O}_1080p.mp4" -af ebur128 -f null - 2>&1 | grep -A1 "Integrated" | tail -1
ls -la "${O}"_*.mp4
