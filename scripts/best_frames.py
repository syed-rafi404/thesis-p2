#!/usr/bin/env python
"""
=============================================================================
PICK THE FRAME THAT ACTUALLY SHOWS EACH PART OF THE BOARD
=============================================================================
The lecturer never leaves the shot. Measured over BanglaASR1, 79 frames: the
board is 23.5% covered in the median frame, 7.0% at best, and not one frame is
under 5%. So "wait for a clean frame" does not work.

What does work is that the lecturer only stands in one place at a time. When he
is writing on the right, the left half of the board is perfectly visible, and
ten seconds later the reverse is true. So rather than repair a bad frame, find,
for each region of the board separately, the frame in which that region is
actually legible.

This matters because the alternative was inpainting, and inpainting on this
material failed in two ways that are visible in
BanglaASR1/figures/fig_03_520.jpg: the lecturer survives as a grey silhouette
because a brightness threshold misses the light squares of his shirt, and board
text is lost because the donor frame was taken from a different moment. Worse,
the old metric counted how many masked pixels got *a* value rather than the
*right* value, so it reported 99.8% recovery for a figure with a ghost in it.

Selecting real frames avoids all of that. Every pixel in the output is a pixel a
camera recorded. Nothing is synthesised, so nothing can be silently wrong, and
the honest quality number is just how much of the region is still covered, which
this script reports per region.

Usage:
    python scripts/best_frames.py --frames <dir>
    python scripts/best_frames.py --frames <dir> --out-dir output/annotation_demo
    python scripts/best_frames.py --frames <dir> --json picks.json
=============================================================================
"""

import argparse
import glob
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from board_regions import (ink_mask, person_mask, find_regions,   # noqa: E402
                           temporal_person_masks)

SCAN_WIDTH = 640           # analyse at this width; cheap and plenty accurate
MAX_COVER = 0.25           # reject a frame if it hides this much of the region
MIN_GAIN = 1.04            # prefer a later frame only if it is this much better


def scan(frames, width=SCAN_WIDTH, temporal=True):
    """Per frame, the visible-ink mask and the occluder mask, at scan width.

    Temporal masking needs the whole stack in memory at scan width, which for a
    79-frame lecture at 640 px is well under 100 MB. It is much more reliable
    than the per-frame brightness rule, so it is the default; --brightness-mask
    exists to reproduce the old behaviour for comparison.
    """
    smalls, sizes = [], []
    for path in frames:
        image = Image.open(path).convert("RGB")
        w, h = image.size
        smalls.append(image.resize((width, max(1, int(h * width / w))), Image.BILINEAR))
        sizes.append(image.size)

    if temporal:
        masks, background = temporal_person_masks(np, smalls)
    else:
        masks, background = [person_mask(np, s) for s in smalls], None

    cache = []
    for path, small, person, size in zip(frames, smalls, masks, sizes):
        ink = ink_mask(np, small) & ~person
        cache.append({"path": path, "ink": ink, "person": person, "size": size})
    return cache, background


def reference_frame(cache):
    """The frame with the most visible ink: the board at its fullest."""
    return max(range(len(cache)), key=lambda i: int(cache[i]["ink"].sum()))


def score_region(entry, box, scale):
    """Visible ink inside the region, and how much of it the lecturer covers."""
    x1, y1, x2, y2 = [int(v * scale) for v in box]
    h, w = entry["ink"].shape
    x1, x2 = max(0, min(w, x1)), max(0, min(w, x2))
    y1, y2 = max(0, min(h, y1)), max(0, min(h, y2))
    if x2 <= x1 or y2 <= y1:
        return 0, 1.0
    ink = int(entry["ink"][y1:y2, x1:x2].sum())
    cover = float(entry["person"][y1:y2, x1:x2].mean())
    return ink, cover


def pick_for_regions(cache, regions, full_size, max_cover=MAX_COVER):
    """For each region, the frame where it is most legible."""
    scale = cache[0]["ink"].shape[1] / float(full_size[0])
    picks = []
    for region in regions:
        scored = []
        for i, entry in enumerate(cache):
            ink, cover = score_region(entry, region["bbox"], scale)
            scored.append((i, ink, cover))

        usable = [s for s in scored if s[2] <= max_cover]
        pool = usable or scored                     # fall back to least-covered
        if usable:
            best = max(pool, key=lambda s: s[1])
        else:
            best = min(pool, key=lambda s: s[2])

        index, ink, cover = best
        picks.append({
            "region_id": region["id"],
            "bbox": region["bbox"],
            "frame_index": index,
            "frame": Path(cache[index]["path"]).name,
            "visible_ink": ink,
            "covered_fraction": round(cover, 4),
            "usable_frames": len(usable),
            "clean": cover <= max_cover,
        })
    return picks


def main():
    ap = argparse.ArgumentParser(description="Choose the clearest frame for each board region")
    ap.add_argument("--frames", required=True, help="Directory of extracted frames")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--out-dir", default=None,
                    help="Also save each region cropped from its chosen frame")
    ap.add_argument("--max-cover", type=float, default=MAX_COVER)
    ap.add_argument("--brightness-mask", action="store_true",
                    help="Use the old per-frame brightness rule instead of temporal")
    ap.add_argument("--save-background", default=None,
                    help="Write the estimated clean board to this path")
    ap.add_argument("--interval", type=float, default=10.0,
                    help="Seconds between frames, for reporting timestamps")
    args = ap.parse_args()

    frames = sorted(glob.glob(str(Path(args.frames) / "*.jpg")))
    if not frames:
        sys.exit(f"no frames in {args.frames}")

    print(f"scanning {len(frames)} frames ...")
    cache, background = scan(frames, temporal=not args.brightness_mask)

    ref = reference_frame(cache)
    print(f"reference frame: {Path(cache[ref]['path']).name} "
          f"(most visible ink: {int(cache[ref]['ink'].sum())})")

    full = Image.open(cache[ref]["path"])
    regions = find_regions(full)
    print(f"regions on the reference: {len(regions)}\n")

    if args.save_background and background is not None:
        background.save(args.save_background, quality=93)
        print(f"wrote {args.save_background}  (estimated clean board)")

    picks = pick_for_regions(cache, regions, full.size, args.max_cover)

    print(f"{'region':>6} {'chosen frame':>28} {'t':>7} {'ink':>7} {'covered':>8}  usable")
    for pick in picks:
        stamp = f"{int(pick['frame_index'] * args.interval)//60}:" \
                f"{int(pick['frame_index'] * args.interval)%60:02d}"
        flag = "" if pick["clean"] else "  <- still covered"
        print(f"{pick['region_id']:>6} {pick['frame']:>28} {stamp:>7} "
              f"{pick['visible_ink']:>7} {pick['covered_fraction']*100:>7.1f}% "
              f"{pick['usable_frames']:>6}{flag}")

    clean = sum(1 for p in picks if p["clean"])
    print(f"\n{clean} of {len(picks)} regions have a frame that shows them clearly "
          f"(under {args.max_cover*100:.0f}% covered)")

    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        for pick in picks:
            image = Image.open(cache[pick["frame_index"]]["path"])
            pad = int(image.size[0] * 0.012)
            x1, y1, x2, y2 = pick["bbox"]
            crop = image.crop((max(0, x1 - pad), max(0, y1 - pad),
                               min(image.size[0], x2 + pad), min(image.size[1], y2 + pad)))
            path = out / f"region_{pick['region_id']:02d}.jpg"
            crop.save(path, quality=93)
            print(f"wrote {path}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(picks, indent=2), encoding="utf-8")
        print(f"wrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
