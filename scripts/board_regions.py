#!/usr/bin/env python
"""
=============================================================================
FIND THE CONTENT REGIONS ON A LECTURE WHITEBOARD
=============================================================================
Given a video frame, locate the separate blocks of handwriting on the board:
the definition in one place, the truth table in another, the gate diagram on
the right. Each block comes back as a bounding box in reading order.

This is the grounding step for annotated figures. A vision-language model is
good at saying *what* something is and poor at saying *where* it is, especially
at lecture-board resolution where strokes are thin and the model has been
downscaled to a few hundred pixels. So geometry finds the regions, and the VLM
is asked only to label regions it is handed. That split is also why the
pipeline degrades gracefully: with no VLM weights present the boxes are still
correct, they just carry positional labels instead of semantic ones.

Detection works on ink, not on darkness. The board is unevenly lit, with glare
streaks and a gradient, so a global threshold either loses pale strokes or
swallows the shadows. Instead the image is compared against a heavily blurred
copy of itself: ink is whatever is markedly darker than its own neighbourhood,
plus anything strongly coloured, which catches the red title.

The lecturer is dark too. They are removed the same way illustrate_notes.py
removes them, by eroding away anything as thin as a pen stroke and keeping only
what survives as a large blob.

Usage:
    python scripts/board_regions.py --frame path/to/frame.jpg
    python scripts/board_regions.py --frame f.jpg --preview out.jpg --json out.json
    python scripts/board_regions.py --frame f.jpg --debug    # dump the masks
=============================================================================
"""

import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# Ink detection
WORK_WIDTH = 960           # detect at this width; boxes scale back to full size
INK_DELTA = 18             # how much darker than the local background counts as ink
INK_SAT = 34               # colourfulness that counts as coloured ink
BLUR_DIV = 24              # background blur radius = width / this

# Lecturer removal, same idea as illustrate_notes.py
PERSON_ERODE = 5
PERSON_DILATE = 13

# Grouping strokes into blocks
GAP_X_DIV = 42             # horizontal join distance = width / this
GAP_Y_DIV = 90             # vertical join distance = height / this
MIN_INK_PIXELS = 90        # a block with less ink than this is noise
MIN_SIDE_DIV = 60          # a block narrower or shorter than width/this is noise
MERGE_PAD_DIV = 70         # boxes closer than this are merged

# A board that has filled up over a whole lecture merges into one blob at the
# default join distance. Any region bigger than this share of the frame is
# re-examined with tighter joins, so a full board separates into its parts
# instead of coming back as a single box covering everything.
SPLIT_AREA = 0.22
SPLIT_SHRINK = 0.45        # join distances are scaled by this on each retry
SPLIT_DEPTH = 2


def _arrays():
    try:
        import numpy as np
    except ImportError:
        sys.exit("numpy is required: this script needs an interpreter that has numpy and Pillow")
    return np


def _dilate(np, mask, dx, dy):
    """Rectangular dilation by OR-ing shifted copies. Cheap and dependency-free."""
    out = mask.copy()
    for k in range(1, dx + 1):
        out[:, k:] |= mask[:, :-k]
        out[:, :-k] |= mask[:, k:]
    shifted = out.copy()
    for k in range(1, dy + 1):
        out[k:, :] |= shifted[:-k, :]
        out[:-k, :] |= shifted[k:, :]
    return out


def person_mask(np, image):
    """Large dark or colourful blobs, which is the lecturer and not the writing."""
    arr = np.asarray(image, dtype=np.int16)
    gray = arr.mean(axis=2)
    sat = arr.max(axis=2) - arr.min(axis=2)
    raw = ((gray < 118) | (sat > 42)).astype(np.uint8) * 255
    img = Image.fromarray(raw)
    img = img.filter(ImageFilter.MinFilter(PERSON_ERODE))    # erase stroke-thin things
    img = img.filter(ImageFilter.MaxFilter(PERSON_DILATE))   # regrow the blob
    return np.asarray(img, dtype=bool)


def temporal_person_masks(np, images, deviation=26, min_blob_side=None, percentile=78):
    """Occluder masks for a whole frame stack, by deviation from the board.

    person_mask() above thresholds on absolute brightness, and that fails
    whenever the lecturer is not dark. On BanglaASR1 the lecturer wears a light
    grey plaid shirt, so most of him sits above PERSON_DARK and is never masked;
    detection then puts boxes on his face and shirt pocket, and reconstruction
    leaves him behind as a grey ghost.

    The board itself is the thing that stays put. Taking a per-pixel median
    across the lecture gives the board with whoever was standing in front of it
    averaged away, and anything a frame differs from that median by is an
    occluder, whatever colour it happens to be.

    Handwriting also deviates from the median, since text written late in the
    lecture is absent from most frames. It is separated the same way as before:
    erode until anything as thin as a pen stroke disappears, then dilate, which
    keeps only blobs of body size.

    Returns (masks, background).

    A median assumes the lecturer is in front of any given pixel less than half
    the time, and on BanglaASR1 that is false: he stands left of centre for most
    of the lecture, so the median bakes his head into the board and the mask
    inverts there. The board is the bright thing and the lecturer is darker, so
    taking a high percentile instead of the middle one tolerates a pixel being
    covered most of the time. It stops short of the maximum because specular
    glare would then win, and it stays below the point where a pen stroke that
    is occasionally occluded would be replaced by bare board.
    """
    stack = np.stack([np.asarray(im, dtype=np.uint8) for im in images])
    background = np.percentile(stack, percentile, axis=0).astype(np.int16)
    bg_gray = background.mean(axis=2)

    erode = PERSON_ERODE
    dilate = PERSON_DILATE if min_blob_side is None else max(3, int(min_blob_side) | 1)

    masks = []
    for frame in stack:
        arr = frame.astype(np.int16)
        gray_diff = np.abs(arr.mean(axis=2) - bg_gray)
        colour_diff = np.abs(arr - background).max(axis=2)
        raw = ((gray_diff > deviation) | (colour_diff > deviation * 1.6))
        img = Image.fromarray((raw.astype(np.uint8) * 255))
        img = img.filter(ImageFilter.MinFilter(erode))
        img = img.filter(ImageFilter.MaxFilter(dilate))
        masks.append(np.asarray(img, dtype=bool))
    return masks, Image.fromarray(background.astype(np.uint8))


def ink_mask(np, image):
    """Pen strokes: markedly darker than the local background, or strongly coloured.

    Comparing against a blurred copy makes this immune to the glare streaks and
    the left-to-right brightness gradient that a global threshold trips over.
    """
    arr = np.asarray(image, dtype=np.int16)
    gray = arr.mean(axis=2)
    sat = arr.max(axis=2) - arr.min(axis=2)

    radius = max(4, image.size[0] // BLUR_DIV)
    background = np.asarray(
        image.convert("L").filter(ImageFilter.GaussianBlur(radius)), dtype=np.int16
    )
    darker = (background - gray) > INK_DELTA
    coloured = sat > INK_SAT
    return darker | coloured


def label_components(np, mask):
    """Connected components, 8-connected, by iterative flood fill.

    Written out rather than pulled from scipy because the environments that run
    this have numpy and Pillow but not scipy, and the mask is small enough that
    a plain stack-based fill is fast.
    """
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=np.int32)
    current = 0
    ys, xs = np.nonzero(mask)

    for start_y, start_x in zip(ys.tolist(), xs.tolist()):
        if labels[start_y, start_x]:
            continue
        current += 1
        stack = [(start_y, start_x)]
        labels[start_y, start_x] = current
        while stack:
            y, x = stack.pop()
            y0, y1 = max(0, y - 1), min(h, y + 2)
            x0, x1 = max(0, x - 1), min(w, x + 2)
            for ny in range(y0, y1):
                for nx in range(x0, x1):
                    if mask[ny, nx] and not labels[ny, nx]:
                        labels[ny, nx] = current
                        stack.append((ny, nx))
    return labels, current


def boxes_from_labels(np, labels, count, ink, min_ink, min_side):
    """One bounding box per component, keeping only blocks with real ink in them."""
    regions = []
    for label in range(1, count + 1):
        ys, xs = np.nonzero(labels == label)
        if ys.size == 0:
            continue
        x1, x2 = int(xs.min()), int(xs.max()) + 1
        y1, y2 = int(ys.min()), int(ys.max()) + 1
        ink_pixels = int(ink[y1:y2, x1:x2].sum())
        if ink_pixels < min_ink:
            continue
        if (x2 - x1) < min_side and (y2 - y1) < min_side:
            continue
        regions.append({"bbox": [x1, y1, x2, y2], "ink_pixels": ink_pixels})
    return regions


def merge_overlapping(regions, pad):
    """Join boxes that touch or nearly touch, repeatedly, until nothing changes."""
    boxes = [dict(r) for r in regions]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            if boxes[i] is None:
                continue
            for j in range(i + 1, len(boxes)):
                if boxes[j] is None:
                    continue
                a, b = boxes[i]["bbox"], boxes[j]["bbox"]
                if (a[0] - pad < b[2] and b[0] - pad < a[2]
                        and a[1] - pad < b[3] and b[1] - pad < a[3]):
                    boxes[i]["bbox"] = [min(a[0], b[0]), min(a[1], b[1]),
                                        max(a[2], b[2]), max(a[3], b[3])]
                    boxes[i]["ink_pixels"] += boxes[j]["ink_pixels"]
                    boxes[j] = None
                    changed = True
        boxes = [b for b in boxes if b is not None]
    return boxes


def merge_text_lines(regions, frame_h, gap_ratio=1.3, max_line_frac=0.15):
    """Rejoin boxes that are parts of one written line.

    Splitting a dense board tightens the join distance globally, which is right
    for the crowded part and too aggressive elsewhere: on BanglaASR3 the line
    `else: print("Just Come")` came back as three boxes because that line is
    written with wider spacing than the code above it.

    Line structure is the cue. Two boxes belong together when they sit at the
    same height, overlapping vertically by most of the shorter one, and the gap
    between them is small next to the letter height. Using the height as the
    yardstick makes this work at any handwriting size without a fixed constant.
    """
    boxes = [dict(r) for r in regions]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            if boxes[i] is None:
                continue
            for j in range(i + 1, len(boxes)):
                if boxes[j] is None:
                    continue
                a, b = boxes[i]["bbox"], boxes[j]["bbox"]
                ha, hb = a[3] - a[1], b[3] - b[1]
                # Only single lines of writing take part. Without this the
                # allowed gap scales with the height of a tall block, and a
                # 446px truth table happily swallows a gate diagram half a
                # board away.
                if max(ha, hb) > max_line_frac * frame_h:
                    continue
                shorter = max(1, min(ha, hb))
                overlap = min(a[3], b[3]) - max(a[1], b[1])
                if overlap < 0.5 * shorter:
                    continue
                gap = max(b[0] - a[2], a[0] - b[2])
                if gap > gap_ratio * shorter:
                    continue
                boxes[i]["bbox"] = [min(a[0], b[0]), min(a[1], b[1]),
                                    max(a[2], b[2]), max(a[3], b[3])]
                boxes[i]["ink_pixels"] += boxes[j]["ink_pixels"]
                boxes[j] = None
                changed = True
        boxes = [b for b in boxes if b is not None]
    return boxes


def reading_order(regions, row_tolerance):
    """Top to bottom, left to right, with boxes on roughly the same line grouped."""
    ordered = sorted(regions, key=lambda r: (r["bbox"][1], r["bbox"][0]))
    rows, current = [], []
    for region in ordered:
        if not current:
            current = [region]
            continue
        if region["bbox"][1] - current[0]["bbox"][1] <= row_tolerance:
            current.append(region)
        else:
            rows.append(sorted(current, key=lambda r: r["bbox"][0]))
            current = [region]
    if current:
        rows.append(sorted(current, key=lambda r: r["bbox"][0]))
    return [r for row in rows for r in row]


def describe(region, width, height):
    """A positional label, used when no VLM is available to supply a real one."""
    x1, y1, x2, y2 = region["bbox"]
    cx, cy = (x1 + x2) / 2 / width, (y1 + y2) / 2 / height
    vertical = "top" if cy < 0.36 else ("middle" if cy < 0.7 else "lower")
    horizontal = "left" if cx < 0.36 else ("centre" if cx < 0.66 else "right")
    aspect = (x2 - x1) / max(1, y2 - y1)
    if aspect > 3.2:
        shape = "wide block"
    elif aspect < 0.5:
        shape = "tall block"
    else:
        shape = "block"
    return f"{vertical} {horizontal} {shape}"


def _blocks(np, ink, gap_x, gap_y, min_ink, min_side, merge_pad):
    """One pass of: join nearby strokes, label, box, merge."""
    grouped = _dilate(np, ink, max(1, int(gap_x)), max(1, int(gap_y)))
    labels, count = label_components(np, grouped)
    regions = boxes_from_labels(np, labels, count, ink, min_ink, min_side)
    return merge_overlapping(regions, pad=max(2, int(merge_pad)))


def _split_large(np, ink, regions, frame_area, gap_x, gap_y,
                 min_ink, min_side, merge_pad, depth):
    """Re-examine oversized regions with tighter joins until they separate.

    A region only survives whole if tightening fails to break it up, which is
    the right answer for a genuinely single object such as one large diagram.
    """
    if depth <= 0:
        return regions
    out = []
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        area = (x2 - x1) * (y2 - y1)
        if area / float(frame_area) <= SPLIT_AREA:
            out.append(region)
            continue
        sub_ink = ink[y1:y2, x1:x2]

        # One tighter pass is not always enough. Tightly spaced handwriting, such
        # as a block of code, stays joined at the first retry and only separates
        # when the vertical join shrinks below the line spacing. Keep shrinking
        # until it breaks up or the joins reach a single pixel, then give up and
        # keep the region whole, which is the right answer for one big diagram.
        parts, shrink = [region], 1.0
        for _ in range(4):
            shrink *= SPLIT_SHRINK
            gx, gy = gap_x * shrink, gap_y * shrink
            if gx < 1 and gy < 1:
                break
            candidate = _blocks(np, sub_ink, gx, gy,
                                min_ink, min_side, merge_pad * shrink)
            if len(candidate) > 1:
                parts = candidate
                break
        if len(parts) <= 1:
            out.append(region)
            continue
        gap_x, gap_y, merge_pad = gap_x * shrink, gap_y * shrink, merge_pad * shrink
        for part in parts:                     # back into frame coordinates
            px1, py1, px2, py2 = part["bbox"]
            part["bbox"] = [px1 + x1, py1 + y1, px2 + x1, py2 + y1]
        out.extend(_split_large(np, ink, parts, frame_area,
                                gap_x * SPLIT_SHRINK, gap_y * SPLIT_SHRINK,
                                min_ink, min_side, merge_pad * SPLIT_SHRINK, depth - 1))
    return out


def find_regions(image, work_width=WORK_WIDTH, remove_person=True):
    """Content blocks on the board, in reading order, in full-resolution pixels."""
    np = _arrays()
    full_w, full_h = image.size
    scale = work_width / float(full_w)
    small = image.convert("RGB").resize(
        (work_width, max(1, int(full_h * scale))), Image.BILINEAR
    )
    h, w = small.size[1], small.size[0]

    ink = ink_mask(np, small)
    if remove_person:
        ink = ink & ~person_mask(np, small)

    gap_x, gap_y = max(2, w // GAP_X_DIV), max(1, h // GAP_Y_DIV)
    min_side = max(6, w // MIN_SIDE_DIV)
    merge_pad = max(2, w // MERGE_PAD_DIV)

    regions = _blocks(np, ink, gap_x, gap_y, MIN_INK_PIXELS, min_side, merge_pad)
    regions = _split_large(np, ink, regions, w * h, gap_x, gap_y,
                           MIN_INK_PIXELS, min_side, merge_pad, SPLIT_DEPTH)
    regions = merge_overlapping(regions, pad=max(2, merge_pad // 2))
    regions = merge_text_lines(regions, h)
    regions = reading_order(regions, row_tolerance=max(8, h // 14))

    inv = 1.0 / scale
    out = []
    for i, region in enumerate(regions):
        x1, y1, x2, y2 = region["bbox"]
        box = [int(x1 * inv), int(y1 * inv), int(x2 * inv), int(y2 * inv)]
        out.append({
            "id": i + 1,
            "bbox": box,
            "ink_pixels": region["ink_pixels"],
            "area_fraction": round((box[2] - box[0]) * (box[3] - box[1])
                                   / float(full_w * full_h), 4),
            "position": describe({"bbox": box}, full_w, full_h),
            "label": "",
        })
    return out


def draw_preview(image, regions, out_path):
    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    w = canvas.size[0]
    line = max(2, w // 500)
    colours = ["#e63946", "#2a9d8f", "#e9c46a", "#4361ee", "#b5179e", "#f77f00"]
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        colour = colours[(region["id"] - 1) % len(colours)]
        draw.rectangle([x1, y1, x2, y2], outline=colour, width=line)
        tag = str(region["id"])
        draw.rectangle([x1, max(0, y1 - 26), x1 + 26, y1], fill=colour)
        draw.text((x1 + 8, max(0, y1 - 22)), tag, fill="white")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=92)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Locate content blocks on a whiteboard frame")
    ap.add_argument("--frame", required=True)
    ap.add_argument("--preview", default=None, help="Write a copy with the boxes drawn")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--work-width", type=int, default=WORK_WIDTH)
    ap.add_argument("--keep-person", action="store_true",
                    help="Do not mask the lecturer, for debugging")
    ap.add_argument("--debug", action="store_true", help="Also write the ink and person masks")
    args = ap.parse_args()

    path = Path(args.frame)
    if not path.exists():
        sys.exit(f"no such frame: {path}")
    image = Image.open(path)

    regions = find_regions(image, args.work_width, remove_person=not args.keep_person)

    print(f"frame   : {path.name}  ({image.size[0]}x{image.size[1]})")
    print(f"regions : {len(regions)}")
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        print(f"  {region['id']:>2}. {str(region['position']):<22} "
              f"{x2 - x1:>4}x{y2 - y1:<4} at ({x1},{y1})  ink={region['ink_pixels']}")

    if args.preview:
        print(f"wrote {draw_preview(image, regions, Path(args.preview))}")
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(regions, indent=2), encoding="utf-8")
        print(f"wrote {args.json_out}")

    if args.debug:
        np = _arrays()
        small = image.convert("RGB").resize(
            (args.work_width, int(image.size[1] * args.work_width / image.size[0]))
        )
        stem = Path(args.preview or "debug").with_suffix("")
        Image.fromarray((ink_mask(np, small) * 255).astype("uint8")).save(f"{stem}_ink.png")
        Image.fromarray((person_mask(np, small) * 255).astype("uint8")).save(f"{stem}_person.png")
        print(f"wrote {stem}_ink.png and {stem}_person.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
