# Image-generation prompt templates

Rules: one shared **style suffix** per film; never ask for text/letters in the image; 16:9 for plates,
4:5 for portraits; plain background for cut-outs; generate in batches (≤10 per turn on capped tools);
review every result for anatomy, anachronism and fake text.

## Style suffixes
- **Sepia Manuscript Cinema:** `cinematic sepia painting, warm candle and window light, volumetric god rays,
  aged parchment tones, painterly realism, fine detail, shallow depth of field, muted browns and gold, no text, no letters, no watermark`
- **Clean VOX:** `flat editorial illustration, off-white paper texture, limited palette (ink black, mustard yellow, blue), subtle grain, no text`
- **Dark Archive:** `grainy black-and-white archival photograph look, harsh flashlight, film burn edges, documentary realism, no text`
- **Blueprint:** `technical blueprint drawing, white hairlines on deep blue grid, isometric, precise, no text`

## Plates (backgrounds, 16:9)
- Desk: `top-down view of an old calligrapher's wooden desk, scattered reed pens, ink pots, a brass compass, parchment sheets with NO writing, empty space in the centre and right third for overlays, {suffix}`
- Hand: `close-up of an elderly hand holding a reed pen writing on burnished paper, ink stroke visible but no readable letters, {suffix}`
- Master & student: `an old master calligrapher teaching a young student in a sunlit Ottoman workshop, shelves of manuscripts, {suffix}`
- City: `Istanbul skyline at golden hour seen from the Bosphorus, silhouettes of domes and minarets, boats, {suffix}`
- Interior: `grand Ottoman mosque interior with mihrab, shafts of light from high windows, large empty plain wall area above the mihrab for overlay text, {suffix}`
- Library/archive: `ancient library corridor with tall wooden shelves of manuscripts, ladder, dust in light beams, {suffix}`
- Modern bridge: `a calligrapher's desk with a modern flatbed scanner / drawing tablet / laser engraver, warm workshop light, {suffix}`
Leave **empty space** where the cards will go (say which third).

## Portraits (4:5, historical persons without photos)
`portrait of {name}, {century} {region} {profession}, {age} years old, {clothing: turban/robe details accurate to era}, {pose: holding a reed pen / scroll}, chest-up, looking slightly to the {left|right} (towards frame centre), plain warm parchment background, painterly sepia realism like an old master oil sketch, {suffix}`
- Keep the same lighting direction for all portraits in the film.
- Mention era-correct details; avoid modern items; avoid glasses unless documented.
- Present as "artistic reconstruction" where relevant.

## Objects for cut-out (plain background)
`a {golden ornate crown with gems | brass drafting compass | reed pen and penknife | ink pot}, isolated on a plain light grey background, soft studio light, high detail, photorealistic, no text`
→ `tools/cutout.sh in.png cut_crown.png`

## Textures
`seamless aged parchment texture, subtle fibres and stains, even lighting, no text` · `dark walnut wood desk texture, top-down, even light`

## Negative checklist (append if the tool supports negatives)
`text, letters, calligraphy, watermark, signature, logo, extra fingers, deformed hands, modern objects, blurry, oversaturated`
