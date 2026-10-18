# Arabic / RTL rules

## Canvas text
- Always set `ctx.direction = 'rtl'` **and** an Arabic-capable font; otherwise punctuation and numbers jump
  to the wrong side.
- Fonts must be local files declared with `@font-face` and pre-loaded (`document.fonts.load(...)`) before
  `window.ready = true`, or the first frames render in a fallback font.
- Good open fonts (OFL): Amiri (naskh display), Noto Kufi Arabic (UI), Noto Naskh Arabic, Reem Kufi,
  El Messiri, Aref Ruqaa, Rakkas, Katibeh, Marhey, Lemonada, Scheherazade New. Avoid using a calligraphic
  font for long UI text.
- Never letter-space Arabic. Never stretch with `scale(x)` — use kashida (ـ) only if typographically right.
- Diacritics (تشكيل) are welcome on display words (more beautiful, disambiguates) but increase line
  height; allow ≥1.35.
- Arabic-Indic digits for Arabic films: `s.replace(/\d/g, d => '٠١٢٣٤٥٦٧٨٩'[d])`. Hijri dates as "ت ٣٢٨ هـ".

## Layout & motion
- Reading starts top-right. First element enters from the right; lists flow right→left; write-on reveals
  right→left; transitions tear right→left; timelines run right→left (past on the right).
- Mirror any western template before use (arrows, progress bars, callout directions).

## Content accuracy
- Never trust AI images for Arabic letters — generate artefacts without text, then use real manuscripts
  or typeset text. If a generated calligraphy hero word is used, verify every letter and dot with a
  native reader's eye (dots missing is the typical failure; draw a separate dot layer).
- Calligraphy terms: keep the style names exact (ثلث، نسخ، محقق، ريحاني، توقيع، رقاع، كوفي، طومار).
- Check names and dates against at least one reliable source; show death dates as the VO says them.

## Transcription
- Whisper on Arabic: use `medium`+ for accuracy; keep diacritics stripped when searching words
  (`tools/find_word.py` normalises أ/إ/آ→ا, ة→ه, ى→ي).
