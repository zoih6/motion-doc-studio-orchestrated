# LISTEN: ear check for the demo (16 s, `../demo_16s.mp4`)

The agent cannot hear. Everything below comes from `qa.py` measurements, not from listening.
Please listen to these 5 moments (headphones, then a phone speaker) and answer yes/no.

| # | Timecode | Cue(s) | What the checks show | Ask the ear |
|---|---|---|---|---|
| 1 | 00:00.63 | hero `title` (thump+tap) | sync 0.12 frame · audible +15.1 dB · body +3.5 dB · picture: motion stops at frame 19 = cue | It sits 15 dB over a still-quiet music intro. Too loud for an opening? |
| 2 | 00:01.30 | `kicker` (tap) | **warn:** motion does not stop near the cue (the tag's text is still writing on) | Does the tap feel early against the tag? |
| 3 | 00:05.83 – 00:06.10 | `dot-0`, `dot-3` (pop, +0/+2 st) | **warn ×2:** dots too small for the picture check to see (change 0.55/0.70 vs local 0.51/0.53) | Do the two pops read as the dots appearing, or as random clicks? |
| 4 | 00:08.33 – 00:10.80 | `tear-list` + `fact-0/1/2` (swish) | densest stretch: 4 sounds in 2.5 s · audible +1.8…+4.4 dB · sync 0.00 frame | Can you tell all four apart? Is any swish harsh? |
| 5 | 00:12.33 – 00:12.80 | `tear-end` → dead stop → hero `end` + `end-rise` | dead stop ≈ 0.35 s before the hero · body +3.7 dB · audible +5.9 dB · picture: stops at frame 382 vs cue 384 | Does the silence feel intentional, not like a glitch? Does the ending land? |

QA summary (`qa-report.json`): **42 pass · 3 warn · 0 FAIL**, integrated −14.01 LUFS (target −14), true peak −3.18 dBTP,
offset 0 samples. Release encodes: `qa-final_1080p.json` and `qa-final_720p.json` → 0 FAIL, 2 warn each.
Fix rounds: 2 on the first cut + 1 after the picture change (see README). Sounds: `CREDITS.md`. Music: "oriental string ambient loop", Ehved, CC0.
