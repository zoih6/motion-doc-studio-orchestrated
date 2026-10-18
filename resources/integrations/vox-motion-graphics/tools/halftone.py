#!/usr/bin/env python3
"""Optional newsprint halftone treatment for transparent cutouts.

Produces a white fill inside the silhouette with black round dots on a
45-degree screen while preserving source alpha. Use only when the selected
visual language benefits from a print treatment.

Usage:
  python3 halftone.py IN.png [IN2.png ...] --out OUT_DIR [--pitch 5] [--long-edge 1100]

Every input is trimmed to its alpha bounding box, resized so its long edge is
LONG_EDGE (up or down - this keeps the apparent dot pitch identical across a
whole set, which is what makes mismatched sources read as one publication),
screened, and written to OUT_DIR under the same filename with a .png extension.
"""

import argparse
import math
import os

from PIL import Image, ImageDraw, ImageOps

ANGLE = 45          # classic single-ink screen angle
SUPERSAMPLE = 3     # dots drawn at 3x then Lanczos-downsampled
RMAX_FACTOR = 0.68  # max dot radius as a fraction of the cell; shadows fuse solid
CONTRAST_CUTOFF = 2 # autocontrast percentile clip - the "high contrast" in the look
MIN_DARKNESS = 0.03 # cells lighter than this stay clean paper


def halftone_gray(gray, pitch):
    rot = gray.rotate(ANGLE, expand=True, fillcolor=255, resample=Image.BICUBIC)
    sw, sh = max(1, rot.width // pitch), max(1, rot.height // pitch)
    small = rot.resize((sw, sh), Image.LANCZOS)
    cell = pitch * SUPERSAMPLE
    canvas = Image.new("L", (sw * cell, sh * cell), 255)
    draw = ImageDraw.Draw(canvas)
    px = small.load()
    rmax = cell * RMAX_FACTOR
    for y in range(sh):
        for x in range(sw):
            dark = (255 - px[x, y]) / 255.0
            if dark <= MIN_DARKNESS:
                continue
            r = rmax * math.sqrt(dark)  # area-linear growth, like real print
            cx, cy = x * cell + cell / 2, y * cell + cell / 2
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    canvas = canvas.resize(rot.size, Image.LANCZOS)
    back = canvas.rotate(-ANGLE, expand=True, fillcolor=255, resample=Image.BICUBIC)
    left = (back.width - gray.width) // 2
    top = (back.height - gray.height) // 2
    return back.crop((left, top, left + gray.width, top + gray.height))


def process(path, out_dir, pitch, long_edge):
    im = Image.open(path).convert("RGBA")
    bbox = im.split()[3].getbbox()
    if bbox:
        im = im.crop(bbox)
    r = long_edge / max(im.size)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    alpha = im.split()[3]
    gray = ImageOps.autocontrast(im.convert("L"), cutoff=CONTRAST_CUTOFF)
    dots = halftone_gray(gray, pitch)
    out = Image.merge("RGBA", (dots, dots, dots, alpha))  # white fill, black dots
    name = os.path.splitext(os.path.basename(path))[0] + ".png"
    dest = os.path.join(out_dir, name)
    out.save(dest)
    print(f"{name}  {out.size[0]}x{out.size[1]}  pitch={pitch}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pitch", type=int, default=5)
    ap.add_argument("--long-edge", type=int, default=1100)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for p in args.inputs:
        process(p, args.out, args.pitch, args.long_edge)


if __name__ == "__main__":
    main()
