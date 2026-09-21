#!/usr/bin/env python
"""
=============================================================================
BUILD A CLEAN BOARD BY TILING SNAPSHOTS TAKEN WHEN NOBODY IS IN THE WAY
=============================================================================
Cut the frame into a grid of small tiles. For each tile independently, find a
moment when the lecturer was not standing in front of that tile, and take the
tile from there. Assemble the tiles. The lecturer is never in any of them, so
they are absent from the result, and every pixel is still something the camera
actually recorded.

This beats both alternatives tried before it. Inpainting invents pixels and was
visibly wrong. Picking one good frame per content region cannot help when the
lecturer stands in front of a region for the whole lecture. Tiles are small
enough that he steps off each one many times.

THE TRAP, AND WHY ERAS EXIST
----------------------------
The lecturer erases the board and starts again. Measured on BanglaASR1: at
6:20 the board reads "Data Type: i) String ii) Integer iii) Float iv) Bool",
and at 13:00 it reads "pi = ...", "age = 10", "agE = 10", with erase smudges
still visible. Different content entirely.

So "take the latest clean view of every tile" is wrong. Tiles the lecturer
happened to leave early would show pre-erase writing, tiles he left late would
show post-erase writing, and the assembled board would be a collage of two
different lessons that never coexisted. It would look plausible and be a lie.

The fix is to cut the lecture into eras at the erase points and mosaic inside
each era only. Each output board is then a real, coherent state of the board.
An erase is detected as a large set of pixels that held ink and then stopped
holding it, counted only over pixels that were unoccluded both before and after,
so the lecturer walking past is not mistaken for an erasure.

SEAMS
-----
Neighbouring tiles come from different moments, so exposure and glare differ
slightly and hard tile edges would show. Tiles are therefore overlapped and
blended with a raised-cosine weight, which spreads any difference across the
overlap instead of leaving a line.

Usage:
    python scripts/board_mosaic.py --frames <dir>
    python scripts/board_mosaic.py --frames <dir> --out-dir output/boards
    python scripts/board_mosaic.py --frames <dir> --tile 48 --no-eras
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
from board_regions import ink_mask, temporal_person_masks   # noqa: E402

SCAN_WIDTH = 640           # masks and decisions are computed at this width
TILE = 32                  # tile size in scan pixels
OVERLAP = 0.5              # fraction of a tile that overlaps its neighbour
CLEAN_TOL = 0.02           # a tile counts as clean below this occluded fraction
ERASE_DROP = 0.30          # this share of ink vanishing marks an erase
MIN_ERA_FRAMES = 4         # ignore eras shorter than this


def load_small(frames, width=SCAN_WIDTH):
    smalls, sizes = [], []
    for path in frames:
        image = Image.open(path).convert("RGB")
        w, h = image.size
        smalls.append(image.resize((width, max(1, int(h * width / w))), Image.BILINEAR))
        sizes.append(image.size)
    return smalls, sizes


def detect_erases(inks, masks, persist=3):
    """Frame indices where a lot of ink disappeared and stayed gone.

    Only pixels visible in both frames are compared, so the lecturer moving
    across the board cannot be mistaken for an erasure.

    Persistence is what makes this usable. Ink "vanishes" for a frame or two
    constantly, from glare, autofocus and compression noise, and without the
    check a 13 minute lecture splits into eight eras and each one has too few
    frames to fill every tile. A real erasure is still gone several frames
    later, so the lost pixels are re-checked against the next few frames and the
    event is kept only if they stay blank.
    """
    events = []
    for i in range(1, len(inks)):
        visible = ~masks[i - 1] & ~masks[i]
        before = inks[i - 1] & visible
        total = int(before.sum())
        if total < 200:                       # too little visible to judge
            continue
        lost = before & ~inks[i]
        if int(lost.sum()) / float(total) < ERASE_DROP:
            continue

        still_gone, checked = 0, 0
        for j in range(i, min(len(inks), i + persist + 1)):
            seen = lost & ~masks[j]
            if int(seen.sum()) < 50:
                continue
            checked += 1
            if int((seen & ~inks[j]).sum()) / float(int(seen.sum())) > 0.6:
                still_gone += 1
        if checked == 0 or still_gone / float(checked) >= 0.6:
            events.append(i)
    return events


def to_eras(events, count):
    """Turn erase points into [start, end) spans, dropping very short ones."""
    bounds = [0] + [e for e in events] + [count]
    spans = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a >= MIN_ERA_FRAMES:
            spans.append((a, b))
    if not spans:
        spans = [(0, count)]
    # merge a stray short tail into the previous era
    merged = [spans[0]]
    for a, b in spans[1:]:
        if a - merged[-1][1] <= 1 and (b - a) < MIN_ERA_FRAMES:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def tile_origins(extent, tile, step):
    """Tile start positions that always reach the far edge.

    A plain range leaves a strip at the right and bottom uncovered, which came
    out as black bars across the assembled board, so the last position is
    pinned to the edge.
    """
    last = max(0, extent - tile)
    spots = list(range(0, last + 1, step))
    if not spots or spots[-1] != last:
        spots.append(last)
    return spots


def tile_sources(masks, era, xs, ys, tile):
    """For each tile, the latest frame inside the era where the tile is clear.

    Latest rather than earliest because the board accumulates writing within an
    era, so the last clean look at a tile is the most complete one.
    """
    start, end = era
    sources = np.full((len(ys), len(xs)), -1, dtype=np.int32)
    cover = np.ones((len(ys), len(xs)), dtype=np.float32)
    for gy, y0 in enumerate(ys):
        for gx, x0 in enumerate(xs):
            # Starts above any possible coverage so that the first frame
            # examined always wins. Starting at 1.0 meant a tile the lecturer
            # covered completely in every frame of the era never beat its own
            # initial value, kept a source of -1, and was then skipped during
            # assembly, leaving a black rectangle in the output.
            best_frac = float("inf")
            best_idx = -1
            for i in range(end - 1, start - 1, -1):
                frac = float(masks[i][y0:y0 + tile, x0:x0 + tile].mean())
                if frac <= CLEAN_TOL:
                    best_idx, best_frac = i, frac
                    break
                if frac < best_frac:
                    best_idx, best_frac = i, frac
            sources[gy, gx] = best_idx
            cover[gy, gx] = best_frac
    return sources, cover


def cosine_window(tile):
    ramp = np.hanning(tile * 2)[:tile] if tile > 1 else np.ones(1)
    win = np.minimum(ramp, ramp[::-1])
    win = np.maximum(win, 1e-3)
    return np.outer(win, win).astype(np.float32)


def assemble(frames, sizes, sources, xs, ys, tile, scale):
    """Paste each tile from its chosen frame at full resolution, with blending."""
    full_w, full_h = sizes[0]
    acc = np.zeros((full_h, full_w, 3), dtype=np.float32)
    wsum = np.zeros((full_h, full_w, 1), dtype=np.float32)

    needed = sorted({int(v) for v in np.unique(sources) if v >= 0})
    cache = {i: np.asarray(Image.open(frames[i]).convert("RGB"), dtype=np.float32)
             for i in needed}

    ftile = max(2, int(round(tile / scale)))
    window = cosine_window(ftile)[:, :, None]

    for gy, sy in enumerate(ys):
        for gx, sx in enumerate(xs):
            idx = int(sources[gy, gx])
            if idx < 0:
                continue
            y0 = min(int(round(sy / scale)), max(0, full_h - ftile))
            x0 = min(int(round(sx / scale)), max(0, full_w - ftile))
            patch = cache[idx][y0:y0 + ftile, x0:x0 + ftile]
            if patch.shape[:2] != (ftile, ftile):
                continue
            acc[y0:y0 + ftile, x0:x0 + ftile] += patch * window
            wsum[y0:y0 + ftile, x0:x0 + ftile] += window

    uncovered = int((wsum == 0).sum())
    if uncovered:
        print(f"    warning: {uncovered} pixels had no tile and are left black")
    wsum[wsum == 0] = 1.0
    return Image.fromarray(np.clip(acc / wsum, 0, 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser(description="Assemble a lecturer-free board from tiles")
    ap.add_argument("--frames", required=True)
    ap.add_argument("--out-dir", default="output/annotation_demo/boards")
    ap.add_argument("--tile", type=int, default=TILE)
    ap.add_argument("--interval", type=float, default=10.0)
    ap.add_argument("--no-eras", action="store_true",
                    help="Treat the whole lecture as one era (will mix pre/post erase)")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--eras-from", default=None,
                    help="Reuse the eras (time ranges) of an earlier mosaic.json instead of "
                         "detecting erases here. For denser frames: at 2 s spacing the erase "
                         "detector mistakes the lecturer's movement for erasing and splits the "
                         "lecture into many short eras")
    ap.add_argument("--extend-to-erase", action="store_true",
                    help="With --eras-from: end each era at the first erase detected in THESE "
                         "frames after the earlier era's end, never before it. The earlier run "
                         "says roughly when the board was wiped; the denser frames say exactly "
                         "when, so the clean moments just after the old end are not cut off")
    args = ap.parse_args()

    frames = sorted(glob.glob(str(Path(args.frames) / "*.jpg")))
    if not frames:
        sys.exit(f"no frames in {args.frames}")
    print(f"loading {len(frames)} frames ...")
    smalls, sizes = load_small(frames)
    masks, _ = temporal_person_masks(np, smalls)
    inks = [ink_mask(np, s) & ~m for s, m in zip(smalls, masks)]

    if args.eras_from:
        def secs(stamp_text):
            m_, s_ = stamp_text.split(":")
            return int(m_) * 60 + int(s_)
        dt = int(args.interval)
        old = json.loads(Path(args.eras_from).read_text(encoding="utf-8"))
        dense = detect_erases(inks, masks) if args.extend_to_erase else []
        events, eras = [], []
        for k, e in enumerate(old):
            a = -(-secs(e["from"]) // dt)                            # ceiling division
            b = min(len(frames), secs(e["to"]) // dt + 1)            # the old end
            if args.extend_to_erase:
                gap_end = (-(-secs(old[k + 1]["from"]) // dt)) if k + 1 < len(old) else len(frames)
                later = [ev for ev in dense if b <= ev <= gap_end]
                b = min(later) if later else (gap_end if k + 1 == len(old) else b)
            if a < b:
                eras.append((a, b))
    else:
        events = [] if args.no_eras else detect_erases(inks, masks)
        eras = to_eras(events, len(frames))
    stamp = lambda i: f"{int(i*args.interval)//60}:{int(i*args.interval)%60:02d}"
    print(f"erase points : {[stamp(e) for e in events] or 'none detected'}")
    print(f"eras         : {[(stamp(a), stamp(b-1)) for a, b in eras]}\n")

    h, w = masks[0].shape
    scale = w / float(sizes[0][0])
    tile = args.tile
    step = max(1, int(tile * (1 - OVERLAP)))
    xs = tile_origins(w, tile, step)
    ys = tile_origins(h, tile, step)
    print(f"grid: {len(xs)} x {len(ys)} tiles of {tile}px, step {step}px "
          f"({len(xs)*len(ys)} tiles)\n")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = []

    for n, era in enumerate(eras, 1):
        sources, cover = tile_sources(masks, era, xs, ys, tile)
        clean = int((cover <= CLEAN_TOL).sum())
        total = cover.size
        used = len({int(v) for v in np.unique(sources) if v >= 0})
        board = assemble(frames, sizes, sources, xs, ys, tile, scale)
        path = out_dir / f"board_era{n}_{stamp(era[0]).replace(':','')}.jpg"
        board.save(path, quality=94)

        print(f"era {n}  {stamp(era[0])}-{stamp(era[1]-1)}  "
              f"({era[1]-era[0]} frames)")
        print(f"   tiles fully clear : {clean}/{total} ({100.0*clean/total:.1f}%)")
        print(f"   worst tile still covered : {cover.max()*100:.1f}%")
        print(f"   distinct frames used     : {used}")
        print(f"   wrote {path}")
        report.append({
            "era": n,
            "from": stamp(era[0]), "to": stamp(era[1] - 1),
            "frames": era[1] - era[0],
            "tiles_total": total,
            "tiles_fully_clear": clean,
            "clear_fraction": round(clean / float(total), 4),
            "worst_tile_covered": round(float(cover.max()), 4),
            "distinct_frames_used": used,
            "image": str(path),
        })

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nwrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
