# Reference: Lamset Shifa v3 «الخط الواحد» — a 64.8 s one-line Reels ad (2026-10)

One continuous gold line draws the whole ad in a single take: a healthcare centre's 61-second
voice-over turned into a hand-drawn world the camera flies through. **Watch it first:**
<https://github.com/zoih6/lamset-shifa/releases/tag/v3.0>.

- Source project (full film): `zoih6/lamset-shifa/film2/` — the files under `scenes/` here are the
  CANONICAL copies for study (same content, kept frozen at v3.0).
- Engine: `../../engine/line.js` · Style grammar: `../../library/one_line_engine.md` (read it BEFORE
  writing a one-line film; every rule there paid for a real failure).
- Full concept/storyboard: `zoih6/lamset-shifa/docs/v2/brief.md`.

## Acts (time, design move, sound beat)
| s | Act | Move | Sound |
|---|---|---|---|
| 0–16.8 | Touch → steps that grow → seal → fingerprint | pen born from a dot; underlines write the subtitles; a wave of light leaves the fingerprint on «احتياجاتها» | pop, thump+tap heroes, whooshes on flights, chime |
| 16.8–37.3 | Seed sprouts → 7 service stations → spectrum infinity | rings + Lucide icons sketched by the pen; two-line labels alternating sides; infinity fills with the spectrum on «طيف التوحد» (cut+FLASH) | pops panned by side, hero thump+chime |
| 37.3–52.6 | Measured steps → heart → home → chart → sun → REVEAL | camera pulls back: the whole film = one path; editorial column on the right; strike-through «مجرد علاج»; «بل رحلة» as a cut hero; light pulse runs the entire path | chime, reveal whoosh, hero thump+tap |
| 52.6–61.3 | Address pin → end card | dives back to the pen; seal again; numbers written LTR with pen underlines | whoosh, pin pop, hero |
| 61.4–64.8 | Studio outro (separate shot) | cut to indigo night; 4 colour arcs sweep into an arch; the badge springs in with a glint + shimmer + sparkles | whoosh, hero, shimmer |

## What to study in the source
- `scenes/stage.js` — the take shell (bg pools, grain, world registries, build INIT order).
- `scenes/b_services.js` — connector choreography, `LINE.icon`, alternating label layout, spectrum
  bloom with gradient + circular spread clip.
- `scenes/c_care.js` — parametric heart, house-in-one-stroke, the REVEAL (wide camera key +
  screen-space editorial column + path-wide light pulse in `lineFx`).
- `scenes/d_contact.js` — end-card hygiene (text exits), LTR digits (`ltrWord`/`wpenL`).
- `scenes/e_wamd.js` — how to make a second "shot": new camera key (hard cut), full-screen layer,
  studio-grade logo moment (arcs, spring, glint, shimmer sweep, sparkles).

## QA artefacts
- `poster.png` · `contact.png` · `sound_qa.png` — what "done" looks like.
- Sound QA: 0 FAIL, master ≈ −14 LUFS, TP ≤ −2 dBTP.
