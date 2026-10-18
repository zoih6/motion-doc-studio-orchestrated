# 0720 Bright Tactile Paper Style

## Purpose

This is the default color and material direction for `vox-mixed-media`. It is
derived from the successful visual language in the user's `0720-remake`
project, but the rules are content-independent. Do not copy its tropical
subjects into unrelated stories; copy its color hierarchy, paper depth, and
clarity.

## Style thesis

Build a sunlit editorial paper world from broad chromatic fields, tactile
cut-paper layers, and a small number of richly colored hero objects. The image
should feel handmade and premium, not faded, sepia, dusty, or generically
vintage. Quiet means low detail, not low saturation.

## Color DNA

The reference succeeds because it uses color by role:

- a large cool field such as sky blue, ocean blue, turquoise, or leaf green
- a darker cool anchor such as deep navy or forest green for depth
- a warm focal color such as marigold, cacao orange, coral, or warm red
- a tactile structural color such as corrugated-cardboard brown in a limited area
- cream or fibrous white only for torn edges, clouds, foam, labels, and breathing room

Do not force every scene to use blue. Preserve the relationship: one chromatic
dominant field, two supporting chromatic hues, one warm/cool counterpoint, one
dark anchor, and one paper neutral.

### Default area budget

- dominant chromatic field: 35-60%
- supporting chromatic colors combined: 20-40%
- paper neutral: 5-25%
- focal accent: 3-15%
- brown, gray, tan, and archival desk tones combined: no more than 20%

The values are planning targets, not pixel-perfect measurements. A user-supplied
palette may override them only when `user_palette_override=true` and a concrete
reason is recorded.

## Contrast hierarchy

- Background: medium saturation, broad shapes, low edge density.
- Midground: one darker or lighter structural band that creates depth.
- Hero: clearer local contrast and higher chroma than its landing zone.
- Accent: the warmest or most saturated color, used once or in one linked family.
- White edge: bright separator around important cutouts, not a full beige wash.

At thumbnail size, the hero silhouette must separate from the background without
depending on a drop shadow. Do not place a muted green hero on a muted green-gray
background or a tan object on a cream-tan field.

## Material hierarchy

Use at least three visibly different paper treatments across the frame:

1. broad fibrous or watercolor paper for the background field
2. corrugated, printed, halftone, or botanical paper for structural and hero layers
3. torn white fibers or a thin cream sticker keyline for separation

Keep texture crisp. Avoid global blur, heavy yellow aging, muddy overlays, and a
single uniform paper texture pasted over every object.

## Sequence color script

Before image generation, assign every Scene a `color_script`.

- Keep one sequence-level palette family and material grammar.
- Change the dominant hue, dominant/support ratio, or warm/cool direction between adjacent Scenes.
- Adjacent Scenes may not use the same dominant field and focal accent combination.
- Reserve the sequence accent for narrative emphasis; do not scatter it as decoration.
- A quiet background may still be blue, turquoise, green, coral, or marigold. Reduce detail and edge contrast, not color life.

## Prompt contract

Every background and foreground prompt must copy the Scene's approved
`prompt_palette_sentence` verbatim. It must also repeat all
`negative_palette_terms` verbatim.

Recommended negative palette terms:

```text
no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look
```

### Background prompt example

```text
Create a quiet stage-only paper collage background for an editorial explainer.
Use a broad sky-blue fibrous paper field, a deep ocean-blue structural band,
small leaf-green side masses, and no more than a narrow warm-cardboard ground
edge. Keep the hero landing zones low-detail and free of subject-shaped objects.
Medium color saturation, broad matte paper shapes, crisp visible fibers, clean
light-dark separation, no focal object.

Palette lock: sky blue is the dominant field, deep navy and leaf green are the
support colors, marigold is reserved for the future hero accent, fibrous white is
only a separator.

No sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated
vintage filter, no monochrome kraft-paper scene, no faded low-contrast look.
```

### Transparent hero prompt example

```text
Create one isolated premium cut-paper hero object on a flat chroma-key
background. Use warm marigold and cacao orange for the focal surfaces, deep navy
for the darkest printed details, leaf green only as a small support color, and a
thin fibrous cream-white cut edge. Crisp silhouette, visible paper fibers,
corrugated and halftone material contrast, clear local contrast at thumbnail
size, no extra props, no environment, no text.

Palette lock: sky blue is reserved for the scene background; this hero must be
warmer and more saturated than its landing zone.

No sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated
vintage filter, no monochrome kraft-paper scene, no faded low-contrast look.
```

## Reject conditions

Reject and regenerate when any of these are true:

- beige, tan, brown, gray, and cream visually dominate without user authorization
- the frame contains fewer than three meaningful chromatic hues
- every layer has similar saturation or similar lightness
- the hero merges into the background at thumbnail size
- the same faded paper overlay muddies all assets
- the accent color appears everywhere and no longer identifies the focal action
- adjacent Scenes repeat the same dominant/support/accent balance
- quiet background instructions have been interpreted as washed-out color
