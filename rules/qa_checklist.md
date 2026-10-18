# QA gates (copy into the progress doc and tick them)

## Per shot (check on the contact sheet, at 3 moments: entry · mid · just before exit)
- [ ] Starts on its VO word (±0.15 s); on-screen words appear when spoken.
- [ ] One focal point; ≤ 1 hero + 1 card + 2 supports; ≥ 35 % quiet space.
- [ ] All text ≥ 34 px, inside 96 px margins, contrast OK (no gold-on-parchment hairlines, no dark-on-dark).
- [ ] Card is in the third opposite the subject; nothing overlaps a face or the artefact's key detail.
- [ ] Every element has an entrance motion (spring) and a motivated exit; nothing just fades.
- [ ] Real artefact is cropped to its meaningful part; overlays are pinned in image pixels.
- [ ] No spelling mistakes (Arabic: dots, hamzas, diacritics, Arabic-Indic numerals).
- [ ] An empty card at a sampled time is only acceptable if its text is about to write on — re-sample 0.8 s later to confirm.

## Per section
- [ ] ≥ 3 critique rounds (contact sheet → list problems → fix → re-render) — note them in PROGRESS.md.
- [ ] Rhythm: a new idea every 2–4 s; the section has a build and a climax.
- [ ] Transition into the next section is motivated and RTL/LTR-correct.
- [ ] Style matches the style bible (palette, faces, surfaces, light, grade).

## Final
- [ ] **Arabic/RTL gate:** if Arabic text exists, `python3 tools/validate_arabic_project.py <project>` passes; inspect direction, dots, shaping, numerals, and font loading in a rendered still.
- [ ] Frame count = round(VO duration × fps); duration matches the VO to the frame.
- [ ] Sound layer (`workflow/10_sound_layer.md`): `tools/sound_layer.sh verify` OK (scripts unmodified); cues exported by
      `tools/export_cues.mjs` (no hand-typed frames); no synthesized hits/clicks/whooshes.
- [ ] `qa.py out/final.mp4` → 0 FAIL (loudness −14 ±1 LUFS or −18 calm, TP ≤ −1 dBTP, sync, audible, voice, music, silence,
      picture); ≤ 2 fix rounds, cues/sounds only; warnings listed in LISTEN.md.
- [ ] `tools/encode_release.sh` → every release encode also 0 FAIL.
- [ ] Described `audio/qa.png` at each hero cue in words; LISTEN.md has 5 timecodes; credits list every sound + music file used.
- [ ] Spot-check sync at 5 key words across the film (scrub the final file, not the stills).
- [ ] 1080p ≈ 3.4 Mbps (≈100 MB per 4 min) + 720p version; `+faststart`; plays in a browser.
- [ ] **Orientation gate**: `ffprobe` every deliverable — reels are 1080×1920, docs are 1920×1080. A squished file can pass qa.py.
- [ ] Hero-appear gate: every hero cue is a single-frame event (cut/hard bloom + FLASH + impact). Eased heroes fail sound QA.
- [ ] One-line films: ≥300 world units between scenes' text blocks; pan-sweeps rendered with `--sub 6`; world counters of text (`LINE.S` finite).
- [ ] Release created with final_1080p.mp4, final_720p.mp4, poster.jpg, contact.jpg; links tested (HTTP 200).
- [ ] Code/assets/docs pushed; PROGRESS.md has resume instructions; workspace cleaned; tokens deleted.
