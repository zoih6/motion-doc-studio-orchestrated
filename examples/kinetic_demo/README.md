# Kinetic type demo: 10 s, 9:16, black stage

`kinetic_demo_9x16.mp4` (1080×1920, 30 fps, silent) · `contact.jpg` · `poster.jpg`
Source: `engine/kinetic.html` + `engine/scenes/kt_demo.js` (engine `engine/type.js`, grammar `library/kinetic_type_motion.md`).

Text (original): «الكلمة… حين تتحرّك، وتتنفّس، تسكن القلب… برفق، وتبقى»

| time | beat | grammar |
|---|---|---|
| 0.0–2.0 | a leader dot swells, «الكلمة» grows out of it and holds with a micro wiggle; a connector line drops and «حين» swings in, hanging | leader dot · grow · hanging word |
| 2.05–3.3 | the pair **flips** (rotateY) → «تتحرّك» arrives *stretched with kashida* and tightens (Arabic tracking) | group flip · kashida keys |
| 3.35–4.0 | «تتحرّك» **squashes into a line**, and the accent word «وتتنفّس» grows out of that line | squash → line → unsquash |
| 4.0–5.6 | a dot lands above it, then **leads a trim path** (comet) around the word; the word dims to grey and lifts away | comet · dim · lift |
| 5.3–7.0 | an orange **hinge line** draws; «تسكن» slides out from behind it; the line tilts and «القلب» pops inside an accent **bubble** | hinge · fromLine · bubble |
| 6.9 | a thin **light streak** carries the eye | streak |
| 7.15–9.7 | «برفق» **blurs in** with echo ghosts and a slow drift, a centre-out underline follows 14 f later, «وتبقى» rises; everything leaves offset by 2–4 f | blur + echo · underline · rise · offset exits |

Rules visible here: one hero per moment, one accent colour (#ff7a2f), shapes offset 2–6 frames from text, no cuts,
holds ≥ 0.8 s, safe margins, exits shorter than entrances. Grammar learned from
`examples/reference_dna/kinetic_lyrics/DNA.md`, **recombined, not copied**.

Render time (2 vCPU / 2 GB sandbox, no GPU): final 43 s (4.3 s per film-second), draft 16 s.
```bash
cd engine && PAGE=kinetic.html node ../tools/render.mjs --from 0 --to 10 --out out/kinetic.mp4            # final
cd engine && PAGE=kinetic.html node ../tools/render.mjs --from 0 --to 10 --draft                          # preview
```
Sound: run `skills/motion-sound-layer` on it (add `cue.appear/land/hero` calls at the beat times listed above).
