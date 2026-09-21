"""Whiteboard clean-up for showing a reconstructed board in the notes (display only).

The mosaic leaves faint blocky ghosts where the lecturer stood for the whole era. This applies the
'whiteboard mode' of document-scanner apps: divide by a blurred copy of the board so the
background becomes flat, then fade everything that is not clearly darker than its surroundings
to white. Ink strokes keep their camera colour (slightly darkened); the background is replaced.
So the output is no longer unmodified camera pixels: say so wherever it is shown.

Optional --crop x0 y0 x1 y1 keeps only that box. --auto-crop tries to find the writing itself;
on the Speaker3 boards it was NOT reliable (leftover specks chain the box out to the whole
board), so crop by hand. Kept as the record of what was tried.

    python scripts/clean_board.py IN.jpg OUT.jpg [--crop 840 20 1920 740 | --auto-crop]
        [--mask board_eraN_*_occluder.png]
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def clean(img, lo=0.80, hi=0.93, blur=25, occluder=None):
    """Return (cleaned RGB image, ink weight array in 0..1).

    occluder: optional L image from board_mosaic.py --save-occluder. Pixels where the board still
    shows the lecturer are blanked, since whatever was written behind them was never seen.
    """
    gray_img = img.convert("L")
    gray = np.asarray(gray_img, dtype=np.float32)
    bg = np.asarray(gray_img.filter(ImageFilter.GaussianBlur(blur)), dtype=np.float32)
    norm = np.clip(gray / np.maximum(bg, 1.0), 0, 1)
    alpha = np.clip((hi - norm) / (hi - lo), 0, 1)
    if occluder is not None:
        person = np.asarray(occluder.filter(ImageFilter.MaxFilter(9)), dtype=np.float32) > 40
        alpha[person] = 0.0
    rgb = np.asarray(img, dtype=np.float32)
    out = alpha[..., None] * np.clip(rgb * 0.8, 0, 255) + (1 - alpha[..., None]) * 255.0
    return Image.fromarray(out.astype(np.uint8)), alpha


def components(mask):
    """4-connected components of a boolean mask: list of (pixel count, x0, y0, x1, y1)."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    found = []
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        if seen[y, x]:
            continue
        stack = [(y, x)]
        seen[y, x] = True
        n, x0, y0, x1, y1 = 0, x, y, x, y
        while stack:
            cy, cx = stack.pop()
            n += 1
            x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        found.append((n, x0, y0, x1 + 1, y1 + 1))
    return found


def auto_box(alpha, scale=4, gap=150, min_pixels=20, margin=24):
    """Bounding box of the writing.

    Leftover specks and the board's frame edge are about as large as single words, so size
    alone cannot tell them apart. Instead grow from the largest block of writing: add any blob
    within `gap` full-resolution pixels of the box so far, repeat until nothing more joins.
    Writing sits together on the board; specks and the frame edge sit apart from it.
    """
    h, w = alpha.shape
    small = Image.fromarray((alpha * 255).astype(np.uint8)).resize((w // scale, h // scale), Image.BOX)
    mask = np.asarray(small.filter(ImageFilter.MaxFilter(7))) > 60
    found = [c for c in components(mask) if c[0] >= min_pixels
             and not ((c[4] - c[2]) > 4 * (c[3] - c[1]))]       # tall thin strip: the frame edge
    if not found:
        return None
    found.sort(reverse=True)
    keep, rest = [found[0]], found[1:]
    g = gap / scale
    grew = True
    while grew:
        grew = False
        bx0, by0 = min(c[1] for c in keep), min(c[2] for c in keep)
        bx1, by1 = max(c[3] for c in keep), max(c[4] for c in keep)
        for c in list(rest):
            if c[1] <= bx1 + g and c[3] >= bx0 - g and c[2] <= by1 + g and c[4] >= by0 - g:
                keep.append(c)
                rest.remove(c)
                grew = True
    if not keep:
        return None
    x0 = min(c[1] for c in keep) * scale - margin
    y0 = min(c[2] for c in keep) * scale - margin
    x1 = max(c[3] for c in keep) * scale + margin
    y1 = max(c[4] for c in keep) * scale + margin
    return max(0, x0), max(0, y0), min(w, x1), min(h, y1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--crop", type=int, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    ap.add_argument("--auto-crop", action="store_true")
    ap.add_argument("--mask", help="Occluder PNG from board_mosaic.py --save-occluder")
    args = ap.parse_args()

    img = Image.open(args.src).convert("RGB")
    occ = Image.open(args.mask).convert("L") if args.mask else None
    if args.crop:
        img = img.crop(tuple(args.crop))
        occ = occ.crop(tuple(args.crop)) if occ else None
    out, alpha = clean(img, occluder=occ)
    if args.auto_crop and not args.crop:
        box = auto_box(alpha)
        if box:
            out = out.crop(box)
            print(f"auto crop: {box}")
    Path(args.dst).parent.mkdir(parents=True, exist_ok=True)
    out.save(args.dst, quality=92)
    print(f"wrote {args.dst}")


if __name__ == "__main__":
    main()
