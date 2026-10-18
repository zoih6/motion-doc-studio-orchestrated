# 11 · Render speed: why it was slow, what is normal, how to go fast

## Is slow rendering normal?
Partly. Every frame is computed exactly (`render(t)`), drawn by a headless browser and encoded. A 4-minute
film is 7,200 frames, and with 2 motion-blur sub-frames that's 14,400 drawings. Like an After Effects render, this
is never real-time on a CPU. **But up to v2.0 it was ~5× slower than necessary.**

## The cause (measured, v2.1)
The old launch flags (`--use-angle=swiftshader --enable-unsafe-swiftshader`) forced the **2D canvas through
SwiftShader**, a software emulation of a GPU. Chromium's normal CPU raster path draws the same frame much faster:

| per sub-frame, 1920×1080 demo page, 2 vCPU sandbox | time |
|---|---|
| SwiftShader 2D (old) | **329 ms** |
| default Chromium raster (new) | **60 ms** |
| SwiftShader for WebGL + CPU 2D (`--disable-accelerated-2d-canvas`) | 79 ms |
| extra cost of `page.screenshot` JPEG | ≈ +50 ms |
| extra cost of reading the canvas directly (`toDataURL`) | ≈ 0–5 ms |

Output is visually identical: PSNR 45 dB between old and new renders (≥ 40 dB is indistinguishable). WebGL
transitions (`gl.js`) still work, because headless Chromium provides WebGL by default.

## Measured end-to-end (same 2 vCPU / 2 GB sandbox, no GPU)
| job | old v2.0 | new v2.1 | speed-up |
|---|---|---|---|
| 1080p 16:9 demo, final (2 sub-frames) | 29.0 s per film-second | **6.1 s** | **4.8×** |
| same, `--draft` (1 sub-frame, 960 px, veryfast) | — | **2.6 s** | **11×** |
| 1080×1920 kinetic demo, 10 s, final | ≈ 290 s (est.) | **43 s** (4.3 s/s) | ≈ 6.7× |
| same, `--draft` | — | **16 s** (1.6 s/s) | ≈ 18× |

**Parallel workers** (`--workers N|auto`) split the range into N browser processes and join the parts losslessly
(`-c copy`). They scale with CPU cores. Each worker needs about 0.6–0.9 GB RAM (Chromium + x264), so `auto` picks
`min(cores, (RAM−0.6 GB)/0.7 GB, 6)`. On a 2 GB machine that's 1: two workers ran out of memory in our test, which
is why the script warns. *Estimate, not measured here:* an 8-core / 16 GB laptop with `--workers auto` (6) should
land around 1–1.5 s per film-second for 1080p finals. A 4-minute film then renders in roughly 4–6 minutes,
versus ~2 hours on v2.0 in a small sandbox.

## How to work fast (the rule: draft often, final once)
| stage | command | why |
|---|---|---|
| design / critique | `PAGE=… ../tools/cs.sh name 6 t1 t2 …` (stills only) | seconds; judge composition |
| motion check | `node ../tools/render.mjs --from A --to B --draft` | 1.6–2.6 s per film-second |
| full-fps strip of a transition | `ffmpeg -ss A -t .7 -i draft.mp4 -vf fps=30,scale=180:-1,tile=7x3 strip.jpg` | catch pops/jumps |
| final | `node ../tools/render.mjs --from 0 --to D --workers auto` | motion blur, CRF 18 |
| long films (crash-safe parts) | `RENDER_WORKERS=auto python3 ../tools/render_seg.py name F1 F2` | resumable chunks |

Options: `--sub 1|2|3` motion-blur sub-frames · `--crf` · `--preset` · `--width 1280` (downscale on encode) ·
`--gl auto|cpu|swiftshader` · `--capture canvas|screenshot` (screenshot only if your page draws HTML over the canvas).
Env equivalents: `RENDER_WORKERS`, `RENDER_DRAFT=1`, `RENDER_GL`.

## What makes a scene slow (fix these before blaming the renderer)
- `ctx.filter = 'blur()'` on big images every frame. Blur small, pre-rendered word canvases (as `KT` does), or pre-blur in `INITS`.
- `shadowBlur` on large paths. Bake shadows into cached canvases.
- Full-frame post FX stacks (`fxBloom`, `fxHalation`, `fxLeak`): use one look, not three.
- Creating canvases, text or gradients inside `draw()`: build them once in `INITS` (cache by key).
- Huge source images: downscale to ≤ 2× their on-screen size once.
- Drawing hundreds of off-screen objects: cull by time and frame bounds.

## Telling the user
Give an honest estimate before a long render: *frames × sub-frames × measured ms ÷ workers*. Measure with a
2-second draft first. Say when the machine is the limit (no GPU, 2 cores, 2 GB) and what the same film costs on a
normal laptop.
