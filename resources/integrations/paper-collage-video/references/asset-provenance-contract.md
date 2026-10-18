# Image Asset Provenance Contract

Use this contract for every visible asset in `remotion-code` mode.

## Non-negotiable rule

A `.png` extension is not proof that an asset came from imagegen. New visible art must be created by an actual `image_gen` tool call, unless the user supplied the source image.

If the built-in image generation tool is unavailable or fails, stop and report the blocker. Do not silently replace it with Pillow, ImageDraw, Canvas, SVG, CSS drawing, OpenCV, Cairo, Matplotlib, Sharp, or ImageMagick drawing commands.

Local processing is limited to non-creative transformations of an existing imagegen or user-supplied raster: chroma-key removal, crop, matte cleanup, or color correction. It must not introduce new characters, shapes, text, maps, cards, arrows, or composition.

## Required imagegen sequence

1. Write one concrete prompt file for one asset under `02_assets/prompts/scene-xx/`.
2. Call the built-in `image_gen` tool once for that distinct asset. Do not generate several independently moving assets on one sheet.
3. Preserve the selected unmodified output under `02_assets/imagegen-originals/scene-xx/`.
4. For transparent cutouts, use the imagegen skill's installed `remove_chroma_key.py` helper only after generating a flat chroma-key source.
5. Alpha-trim every final non-background PNG to 3-5% transparent padding. Keep the original untouched; record `crop` or `remove-chroma-key+crop` as `postprocess`.
6. Copy the final raster into `07_remotion/public/scenes/scene-xx/`.
7. Record the prompt, original, and final SHA-256 hashes plus the tool result receipt in `ASSETS.json`.
8. Set `approved: true` only after visual inspection and provenance validation.

## Imagegen provenance schema

```json
{
  "source": "imagegen",
  "provenance": {
    "method": "built-in-image_gen",
    "tool_called": true,
    "result_receipt": "generated image output hint or concrete tool result identifier",
    "prompt_file": "02_assets/prompts/scene-01/hero-cutout.md",
    "prompt_sha256": "64 lowercase hex characters",
    "original_path": "02_assets/imagegen-originals/scene-01/hero-cutout.png",
    "original_sha256": "64 lowercase hex characters",
    "final_sha256": "64 lowercase hex characters",
    "postprocess": "remove-chroma-key",
    "fallback_user_approved": false
  }
}
```

`method=imagegen-cli` is allowed only after the user explicitly approves the imagegen skill's CLI fallback; then set `fallback_user_approved: true`.

## User-supplied assets

Use `source=user-supplied`, preserve the original under `02_assets/supplied-originals/`, set `provenance.method=user-supplied`, and record the original and final hashes. Do not relabel locally drawn art as user-supplied.

## Rejection conditions

Reject the Asset Gate when:

- a project-local script contains a procedural drawing API
- `source=imagegen` has no concrete prompt, original output, result receipt, or matching hashes
- `tool_called` is false
- a CLI fallback lacks explicit user approval
- an asset was changed while `postprocess=none`
- post-processing creates new visible content instead of extracting or cleaning an existing generated image
- a final non-background PNG retains enough transparent padding to make its visible alpha bounds cover less than 72% of either source-canvas axis
