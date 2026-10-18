# Progress — <film>
## Resume from zero
```bash
printf '%s' '<PAT>' > /tmp/.ghtok           # never commit
cd /var/tmp && git clone https://github.com/<user>/<repo>.git film && cd film && ./tools/setup.sh
mkdir -p film/tmp && ffmpeg -v error -y -i assets/vo.mp3 -ar 48000 -ac 2 film/tmp/vo.wav
cd film && ../tools/sound_layer.sh setup . && ../tools/sound_layer.sh kit .    # sound-layer/ + CC0 kit (git-ignored, rebuild after resets)
PAGE=index.html node ../tools/export_cues.mjs && uv run sound-layer/scripts/mix.py audio/cues.json   # workflow/10_sound_layer.md
PAGE=index.html ../tools/cs.sh check 4 1 5 9 13
```
## Sections / parts
| part | frames | time | status | release asset |
|---|---|---|---|---|
## Critique log
## Open issues / next steps
## User's standing instructions
