# vendor/ — third-party code shipped unmodified

## opus-sound-layer
upstream: https://github.com/Bodila51/opus-sound-layer
pinned_commit: 52ac266a24b7dfd3cd06a28c34d5af360a8d7586
pinned_date: 2026-10-10 (Merge pull request #4 — hero defaults)
license: MIT © 2026 Bodila51 — `opus-sound-layer/LICENSE`
checksums: `opus-sound-layer.sha256` (sha256 of every file at the pinned commit)

**What it is:** the sound engine behind the SOUND LAYER step (`skills/sound-layer/`, `workflow/10_sound_layer.md`):
- `scripts/sfx.py` builds a CC0 library (`kit`: Kenney packs + hand-checked Freesound recordings →
  measured at the pin: **1,139 sounds in 19 types**, ≈3.5 min, ≈220 MB in `audio/kit/`, never committed), browses it with
  waveform/spectrogram sheets, searches Openverse for missing sounds, and judges every file;
- `scripts/mix.py` places each sound by its peak on the cue frame, builds music/voice/SFX stems and
  masters to −14 LUFS (punchy) or −18 (calm), −2 dBTP limiter;
- `scripts/qa.py` measures the finished MP4 (picture match, offset, loudness, sync, audibility, voice
  clearance, music dips, silence) and draws `audio/qa.png`. Exit code 1 on any FAIL.

**Rules:** the files in `opus-sound-layer/` are byte-identical to the pinned commit. Never edit them and
never loosen a threshold to make a check pass. `tools/sound_layer.sh verify DIR` proves it.

**How a film gets it:** `tools/sound_layer.sh setup film/` → `film/sound-layer/`: it runs the upstream
`git clone` (as the SOUND LAYER prompt says) and checks out the pinned commit; offline it copies this
vendored folder. `LATEST=1` stays on upstream HEAD (then re-run `tools/selftest.mjs` and the demo QA).

**Updating the pin:** clone upstream, check the new `mix.py --schema` against `tools/export_cues.mjs`,
replace `opus-sound-layer/` with `git archive <sha> | tar -x`, regenerate the checksums
(`cd vendor/opus-sound-layer && find . -type f ! -name .gitignore | sort | xargs sha256sum > ../opus-sound-layer.sha256`),
update `pinned_commit` above, re-run the demo (`examples/demo/sound/`) and note it in CHANGELOG.md.
