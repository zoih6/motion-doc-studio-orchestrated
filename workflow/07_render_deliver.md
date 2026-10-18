# 07 · Sample → full build → render → deliver

> Speed (v2.1): iterate with `render.mjs --draft` (≈1.6–2.6 s per film-second on a small sandbox), finals with
> `--workers auto`, part renders with `RENDER_WORKERS=auto python3 ../tools/render_seg.py …`. Details + honest
> estimates: `workflow/11_render_speed.md`.

## Sample (always first)
- 20–60 s covering the hook + one rich section, in the *final* style, with VO + SOUND LAYER (real SFX + music, qa.py run).
- Render: `PAGE=index.html VO=tmp/vo.wav SFX=tmp/sfx.wav python3 ../tools/render_seg.py sample 0 <F1>`
- Upload to the `segments` release (`tools/gh.sh release <owner/repo> segments segments/sample.mp4`),
  send the link + 3–5 lines on what to look at. Wait for approval/feedback.
- Feedback → update the style bible + rules for this film, then continue. If the user changes style,
  redo the sample (v2, v3…) — don't patch the old look.

## Full build
- Build sections **in order**, critique each, push each.
- Sound: register `cue.*` calls in each scene file as you build it (same t0/spring as the draw call).
  Previews: `PAGE=index.html node ../tools/export_cues.mjs && uv run sound-layer/scripts/mix.py audio/cues.json`.
  Full procedure: `workflow/10_sound_layer.md`. (Legacy synth path `cues_auto.py` + `sfx.mjs`: don't use it for hits/clicks/whooshes.)

## Part renders (crash-safe, workspace-friendly)
- Split into parts of 30–60 s at integer frames (e.g. 0–2020, 2020–3104 …). Run as a background job
  that renders → keeps the silent copy outside the workspace → uploads the preview part → deletes local files.
  ```bash
  for s in "p1 0 2020" "p2 2020 3104"; do set -- $s
    PAGE=index.html VO=tmp/vo.wav SFX=tmp/sfx.wav python3 ../tools/render_seg.py $1 $2 $3
    cp renders/silent_$1.mp4 /var/tmp/silent/ && ../tools/gh.sh release <owner/repo> segments segments/$1.mp4 && rm segments/$1.mp4
  done
  ```
- Speed reference: ~55 s wall time per 6 s chunk at 1080p with 2 sub-frames on 2 vCPU → a 4-min film ≈ 35–40 min.
- Re-using an approved, unchanged part: extract its video stream (`ffmpeg -i part.mp4 -map 0:v -c copy`).

## Final assembly
```bash
cd /var/tmp/silent && for f in p*.mp4; do echo "file '$f'"; done > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy master_silent.mp4      # check nb frames == round(dur*30)
# SOUND LAYER on the whole film (one mix; VO in audio/sound.json → voice), from film/:
cp /var/tmp/silent/master_silent.mp4 video.mp4
PAGE=index.html node ../tools/export_cues.mjs
uv run sound-layer/scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
uv run sound-layer/scripts/qa.py out/final.mp4            # 0 FAIL, ≤2 fix rounds (workflow/10_sound_layer.md §4)
../tools/encode_release.sh out/final.mp4 out/final         # final_1080p/720p + qa.py on each
```
Then: poster (`ffmpeg -ss <best moment> -frames:v 1 poster.jpg`), contact (`fps=1/10,scale=320:-1,tile=6x4`),
QA gates (rules/qa_checklist.md), release `vX.0` with final_1080p.mp4, final_720p.mp4, poster.jpg, contact.jpg;
commit `audio/cues.json`, `audio/sound.json`, `audio/qa-report.json`, `audio/qa.png`, `LISTEN.md`, credits.

## Report to the user (their language, short)
Links (1080p, 720p, release page) · what's in it (one line per section) · what was verified
(duration, qa.py pass/warn/FAIL + loudness, what qa.png shows at each hero, critique rounds, LISTEN.md timecodes; never "the sound is good") · housekeeping (pushed, cleaned) · next options / question.
Optionally drop the 720p file into the workspace and open it in the viewer so they can watch immediately.
