# 06 · Critique loop — the difference between "ok" and "a million views"

## The loop (≥3 rounds per section, more for the hook and the finale)
1. Render a contact sheet: 3 stills per shot (entry +0.4 s, middle, exit −0.3 s), 4 columns.
   `PAGE=index.html ../tools/cs.sh s05a 4 67.8 70.2 73.0 …`
2. Look at it **as a viewer on a phone**: can I read every word? Where does my eye go first? Is anything
   crowded, tiny, cut off, overlapping, low-contrast, or empty for no reason?
3. Write the problems as a numbered list (in PROGRESS.md), each with the fix:
   "s05 74.5: three panels + label → crowded; drop the label, enlarge panels 1.2×".
4. Fix, re-render only the affected times at full size (`still.mjs`) to verify details.
5. Repeat until a round finds nothing important.

## Critique lenses (run all)
- **Composition:** thirds, margins, opposite-third card, quiet space ≥35 %.
- **Hierarchy:** one focal point; key noun biggest; motion leads the eye.
- **Legibility:** ≥34 px, contrast, Arabic dots/diacritics intact, no text over busy texture.
- **Truth:** asset matches the sentence (right era, right person, right script); dates/names correct.
- **Rhythm:** something new every 2–4 s; holds are intentional.
- **Consistency:** palette, faces, surfaces, motion presets, grade — same film everywhere.
- **Wow:** does the section have a memorable beat? If not, design one.

## Sanity checks that catch most bugs
- An empty card at a sampled time — re-sample +0.8 s (it may just be before its write-on).
- Black frame / missing image → `MISSING` in the console (cs.sh prints it).
- Last frame of a shot equals the first of the next? (transition missing) → check `tin`.
- Compare a still to the reference images side by side for style drift.
