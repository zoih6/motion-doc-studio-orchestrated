# Pitfalls — real failures from production and their fixes

## Environment & ops
- **Sandbox resets wipe everything not pushed** (.git, node_modules, /tmp, untracked files). → Push after
  every step; keep a `docs/PROGRESS.md` with resume commands; `tools/setup.sh` is idempotent.
- `/tmp` may be RAM-backed; ~2 GB RAM total. → Work in `/var/tmp/<project>`; never run stills while a
  render runs (OOM); render in 6 s chunks in fresh browsers (`render_seg.py`).
- User workspace fills up during renders. → Never render inside the user's visible workspace; delete
  chunks/silent files after upload; final cleanup at the end.
- GitHub rejects files > 100 MB and warns > 50 MB. → Videos go to **Release assets**; don't `git add -A`
  render folders; keep `.gitignore` strict.
- Wrong repo/URL guesses waste time. → Copy exact names from the user/API.
- Background processes: logs piped through `grep` are block-buffered → check the files on disk / chunk
  folder to see progress, or use `python -u`.
- Long jobs: start them as background processes and poll with waits; never block a single shell call
  beyond its timeout.

## Rendering & engine
- `fetch()` of local JSON fails under `file://`. → Embed data as `.js` globals (`window.DATA = …`).
- Editing scene files while a render runs corrupts later chunks (each chunk reloads the page). → Freeze
  code during renders; `node --check` every file before rendering.
- Segment boundaries must be integer frames (`F0`, `F1` at fps), or audio drifts on concat.
- Playwright `locator.screenshot` PNG was ~20× slower than `page.screenshot({type:'jpeg'})`. → render.mjs
- v2.0 launched Chromium with SwiftShader flags → the *2D canvas* was emulated on a software GPU: 329 ms vs 60 ms per frame.
  v2.1 uses default raster + reads the canvas directly (`toDataURL`). Don't re-add `--use-angle=swiftshader` (use `--gl swiftshader` only if WebGL is missing).
- Two render workers + x264 at 1080p on a 2 GB machine → out of memory (each x264 ≈ 450 MB with default lookahead). `--workers auto` sizes by RAM.
- Arabic tracking with `letterSpacing` or per-letter offsets breaks joining → use `KT.kashida()` (tatweel at legal joints, never inside لا).
- Bokeh/particles over a pure black stage read as dust → only over footage/photos.
- Word canvases sized from `measureText` can be wider than the frame at hero sizes with kashida → check `W.w` against the safe area.
  uses JPEG q95 piped to ffmpeg.
- Screenshots are full-range (yuvj420p). → Convert to TV range in the final encode (`scale=in_range=pc:out_range=tv`).
- Spring overshoot makes radii negative → `Math.max(0, r)`.
- A transform reset inside a helper breaks the camera. → Helpers must `save()/restore()`, never `setTransform` (only `render`/`grade` do).
- Labels drawn before later layers get covered. → Draw labels/overlays in a final pass of the shot.
- Contact sheets ordered alphabetically put 100.0 before 68.0. → Zero-pad times (cs.sh does).
- `track()` keys must be cumulative absolute values, not deltas.

## Visual
- Gold hairlines on light parchment are invisible; black on dark is invisible. → Context colours (goldD on
  light, cream on dark) and ≥3 px lines.
- Small text on contact sheets = small text on phones. → TS=1.3, min 34 px.
- Too many strips/cards in one shot ("crowded") was the top complaint. → Density rule; stagger; remove.
- Dirty-looking paper (texture too dark). → Cream veil over light paper (rgba(238,224,190,.42)).
- AI-generated calligraphy drops dots/letters. → Verify; add a separate dot layer; prefer real artefacts.
- Low-res sources look cheap when pushed in. → Need ≥2× the on-screen size; use the original file
  (e.g. 4000 px) for close-ups, not a downscaled copy.
- Connected-component detection fails on connected scripts. → Measure positions on a grid overlay by eye
  and store them as constants in image pixels.

## Assets & tools
- Wikimedia thumb URLs with arbitrary widths (e.g. /2400px-) return 2 KB error files. → `Special:FilePath/<name>?width=2560` or original URL; check size > 50 KB.
- rembg on several images in one process gets OOM-killed. → One process per image (`tools/cutout.sh`).
- faster-whisper can fail on mp3 paths. → Decode with ffmpeg to float32 numpy first (`tools/transcribe.py`).
- NumPy 2 removed `ndarray.ptp()` → use `np.ptp(a)`.
- Image generation tools may cap calls per turn (e.g. 10). → Plan assets in batches of ≤10, most important first, and tell the user about the limit.
- `read_file`/viewers may cache an image path → write new filenames for each iteration.
- `sed` with `#` delimiter breaks on colour codes → edit with python or a proper editor tool.
- JSON doesn't accept `.5` → write `0.5`.

## «الخط الواحد» one-line films (lamset v3, v3.0)
- `LINE.tf` expects flat points; `LINE.sample` returns SUB-polylines. `tf(sample(d))` injects NaN → the
  whole world disappears (`LINE.S` NaN). → `.map(sp => LINE.tf(sp, o))`.
- In one-take worlds, neighbouring scenes' texts collide: keep ≥300 world units between text blocks;
  text must appear only after the camera has arrived (t0 = the VO word AFTER arrival).
- Sound-QA `appear` gate needs a ≥3× change in ONE frame: eased hero entrances FAIL. → `in:'cut'`,
  `window.FLASH` at the frame, `impact()` in HITS, then find the exact frame by frame-diffing (t = f/30).
- Hermite cameras overshoot between distant keys (text slides sideways). → `hold:true` on arrival keys.
- Release encodes squished a 9:16 reel into 1920×1080 and STILL passed qa.py. → encode_release.sh now
  probes orientation; for reels verify `ffprobe` yourself (1080×1920) before shipping.
- World-anchored texts never leave by themselves: give them `t1` + `out:'sink'` before the end card.
- Duplicate-t camera keys divide by zero; LC keys sort themselves but LINE.KEYS must stay chronological.
- A mid-turn sandbox reset wiped an uncommitted film branch: COMMIT+push after every working step; keep
  only reproducible-from-repo state uncommitted (kit/stems cache is regenerable via sound_layer.sh kit).

## Sound layer (v3 additions)
- The SFX kit is regenerated by `sound_layer.sh kit` and is NOT committed (audio/kit is gitignored) —
  kit rebuilds may pick different files. → After any rebuild, grep every `sound:` in scenes against
  `audio/kit/**.wav` before mixing; a wrong id means a silent cue that qa.py will flag as inaudible.
- `sfx.py kit` takes 3–10 min and downloads ~220 MB — start it as a background process first thing.
- Bare kit types ('chime', 'tap') resolve to different picks between kits → always pin the file id.
