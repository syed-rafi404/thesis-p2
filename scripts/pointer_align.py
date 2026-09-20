#!/usr/bin/env python
"""
=============================================================================
THE LECTURER'S BODY AS A POINTER
=============================================================================
Where a lecturer is standing is where the lecture currently is. When she stands
in front of the truth table, she is writing the truth table, and what she says
in those seconds is about the truth table. So the thing that ruins the picture,
her body blocking the board, is also a free signal for which part of the board
the speech belongs to.

This matters because the project already tried to get that signal the usual way
and failed. YOLOv8-Pose gaze tracking returned zero detections across every
video, and it is written up as a negative result. The occlusion mask costs
nothing extra, is computed already for board_mosaic.py, and cannot return zero
detections, because a lecturer who is not blocking the board is a lecturer who
is not at the board.

WHAT THIS PRODUCES
------------------
For each region of the reconstructed board, the stretches of time the lecturer
spent in front of it, and the transcript of what was said during them. That is
a region-level alignment between speech and board content, which is what turns
a labelled figure into a figure carrying the lecturer's own words about each
part of the board.

HOW IT IS VALIDATED WITHOUT ANY MANUAL LABELS
---------------------------------------------
The claim "standing in front of a region means working on that region" is
testable, because working on a region usually means writing in it. If the claim
holds, a region should hold more ink after the lecturer has stood in front of it
than before. If the claim is false, occlusion should tell us nothing about where
new ink appears.

So for every occlusion episode the script measures the ink in that region
immediately before and immediately after, and compares that change against the
change over the same interval in the regions the lecturer was *not* standing in
front of. The control is measured across the identical time window, so anything
that affects the whole board equally cancels out.

The test is paired and rank based, for the same reason the ASR work uses rank
tests: a single episode where a lecturer fills a whole empty region swamps any
mean.

Usage:
    python scripts/pointer_align.py --lecture BanglaASR7_004
    python scripts/pointer_align.py --all
    python scripts/pointer_align.py --all --json output/pointer_alignment.json
=============================================================================
"""

import argparse
import glob
import json
import re
import sys
from bisect import bisect_right
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from board_regions import ink_mask, temporal_person_masks, find_regions   # noqa: E402
from board_mosaic import load_small, detect_erases, to_eras                # noqa: E402

RUNS = "output/live_focused/no_gaze/interval_10s"
GT_DIR = "data/ground_truth"
OCC_HI = 0.25          # above this the lecturer counts as standing at the region
OCC_LO = 0.06          # below this the region counts as clear enough to measure
MIN_REGION_INK = 150   # ignore specks


# ---------------------------------------------------------------------------
# Statistics, kept local so this runs in any interpreter with numpy
# ---------------------------------------------------------------------------

def wilcoxon(diffs):
    """Two-sided signed-rank test, normal approximation with tie correction."""
    vals = [d for d in diffs if d != 0]
    n = len(vals)
    if n < 6:
        return None
    order = sorted(range(n), key=lambda i: abs(vals[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(vals[order[j + 1]]) == abs(vals[order[i]]):
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    w_plus = sum(r for r, v in zip(ranks, vals) if v > 0)
    mean = n * (n + 1) / 4.0
    sd = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
    if sd == 0:
        return None
    z = (w_plus - mean) / sd
    return min(1.0, 2.0 * 0.5 * (1.0 - _erf(abs(z) / (2 ** 0.5))))


def _erf(x):
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741)
                * t - 0.284496736) * t + 0.254829592) * t * pow(2.718281828, -x * x)
    return y


def sign_test(diffs):
    """Exact two-sided binomial test on the signs."""
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    n = pos + neg
    if n == 0:
        return None, 0, 0
    from math import comb
    tail = sum(comb(n, k) for k in range(0, min(pos, neg) + 1))
    return min(1.0, 2.0 * tail / float(2 ** n)), pos, neg


# ---------------------------------------------------------------------------
# Transcript
# ---------------------------------------------------------------------------

STAMP = re.compile(r"\[(\d+):(\d+)\s*-\s*(\d+):(\d+)\]")


def load_transcript(name):
    """Ground-truth segments as (start_s, end_s, text), both layouts supported."""
    base = re.match(r"(BanglaASR\d+)", name)
    if not base:
        return []
    path = Path(GT_DIR) / f"{base.group(1)}_ground_truth.txt"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    out, pending = [], None
    for line in lines:
        if line.lstrip().startswith("#"):
            continue
        m = STAMP.search(line)
        if m:
            if pending and pending[2].strip():
                out.append(pending)
            start = int(m.group(1)) * 60 + int(m.group(2))
            end = int(m.group(3)) * 60 + int(m.group(4))
            pending = [start, end, line[m.end():].strip()]
        elif pending is not None:
            pending[2] = (pending[2] + " " + line.strip()).strip()
    if pending and pending[2].strip():
        out.append(pending)
    # the header carries two example stamps; drop segments that duplicate a span
    seen, clean = set(), []
    for s, e, t in out:
        if (s, e) in seen:
            continue
        seen.add((s, e))
        clean.append((s, e, t))
    return sorted(clean)


def speech_between(segments, t0, t1):
    """Transcript text overlapping [t0, t1]."""
    parts = [t for s, e, t in segments if e > t0 and s < t1]
    return " ".join(parts).strip()


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def region_series(masks, inks, regions, scale):
    """Per region, per frame: how covered it is, and how much ink is visible."""
    occ = np.zeros((len(regions), len(masks)), dtype=np.float32)
    ink = np.zeros((len(regions), len(masks)), dtype=np.float32)
    h, w = masks[0].shape
    for r, region in enumerate(regions):
        x1, y1, x2, y2 = [int(v * scale) for v in region["bbox"]]
        x1, x2 = max(0, min(w, x1)), max(0, min(w, x2))
        y1, y2 = max(0, min(h, y1)), max(0, min(h, y2))
        if x2 <= x1 or y2 <= y1:
            continue
        for i, (m, k) in enumerate(zip(masks, inks)):
            occ[r, i] = m[y1:y2, x1:x2].mean()
            ink[r, i] = k[y1:y2, x1:x2].sum()
    return occ, ink


def episodes(occ_row, lo, hi, start, end):
    """Maximal runs inside [start, end) where the region is heavily covered."""
    spans, i = [], start
    while i < end:
        if occ_row[i] < hi:
            i += 1
            continue
        j = i
        while j + 1 < end and occ_row[j + 1] >= hi:
            j += 1
        before = None
        for b in range(i - 1, start - 1, -1):
            if occ_row[b] <= lo:
                before = b
                break
        after = None
        for a in range(j + 1, end):
            if occ_row[a] <= lo:
                after = a
                break
        if before is not None and after is not None:
            spans.append((before, i, j, after))
        i = j + 1
    return spans


def analyse(name, interval=10.0):
    frames = sorted(glob.glob(str(Path(RUNS) / name / "ingested" / "frames" / "*.jpg")))
    if not frames:
        return None
    smalls, sizes = load_small(frames)
    masks, _ = temporal_person_masks(np, smalls)
    inks = [ink_mask(np, s) & ~m for s, m in zip(smalls, masks)]
    eras = to_eras(detect_erases(inks, masks), len(frames))
    segments = load_transcript(name)
    scale = masks[0].shape[1] / float(sizes[0][0])

    lecture = {"lecture": name, "frames": len(frames), "eras": [],
               "episodes": [], "paired": []}

    for n, (start, end) in enumerate(eras, 1):
        board_path = (Path("output/annotation_demo/all9") / name /
                      f"board_era{n}_{int(start*interval)//60}"
                      f"{int(start*interval)%60:02d}.jpg")
        source = Image.open(board_path) if board_path.exists() else Image.open(frames[end - 1])
        regions = [r for r in find_regions(source) if r["ink_pixels"] >= MIN_REGION_INK]
        if not regions:
            continue
        occ, ink = region_series(masks, inks, regions, scale)
        lecture["eras"].append({"era": n, "regions": len(regions),
                                "from": start, "to": end - 1})

        for r, region in enumerate(regions):
            for before, i0, i1, after in episodes(occ[r], OCC_LO, OCC_HI, start, end):
                gain = float(ink[r, after] - ink[r, before])
                others = [float(ink[q, after] - ink[q, before])
                          for q in range(len(regions))
                          if q != r and occ[q, i0:i1 + 1].mean() < OCC_HI]
                if not others:
                    continue
                control = float(np.median(others))
                t0, t1 = before * interval, after * interval
                lecture["episodes"].append({
                    "era": n,
                    "region": region["id"],
                    "bbox": region["bbox"],
                    "from_s": t0, "to_s": t1,
                    "from": f"{int(t0)//60}:{int(t0)%60:02d}",
                    "to": f"{int(t1)//60}:{int(t1)%60:02d}",
                    "ink_gain": gain,
                    "control_gain": control,
                    "speech": speech_between(segments, t0, t1)[:600],
                })
                lecture["paired"].append(gain - control)
    return lecture


def summarise(lectures):
    diffs = [d for lec in lectures for d in lec["paired"]]
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    p_sign, _, _ = sign_test(diffs)
    return {
        "episodes": len(diffs),
        "occluded_region_gained_more": pos,
        "control_gained_more": neg,
        "median_difference_px": float(np.median(diffs)) if diffs else 0.0,
        "wilcoxon_p": wilcoxon(diffs),
        "sign_test_p": p_sign,
    }


def main():
    ap = argparse.ArgumentParser(description="Align speech to board regions via occlusion")
    ap.add_argument("--lecture", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", dest="json_out", default="output/pointer_alignment.json")
    ap.add_argument("--examples", type=int, default=3)
    args = ap.parse_args()

    names = ([Path(p).name for p in sorted(glob.glob(str(Path(RUNS) / "*")))]
             if args.all else [args.lecture])
    names = [n for n in names if n]
    if not names:
        sys.exit("pass --lecture <name> or --all")

    lectures = []
    for name in names:
        print(f"analysing {name} ...")
        lec = analyse(name)
        if not lec:
            print("   no frames, skipped")
            continue
        n_ep = len(lec["episodes"])
        wins = sum(1 for d in lec["paired"] if d > 0)
        print(f"   {len(lec['eras'])} eras, {n_ep} occlusion episodes, "
              f"region gained more ink in {wins}/{n_ep}")
        lectures.append(lec)

    stats = summarise(lectures)
    print("\n" + "=" * 68)
    print("DOES STANDING IN FRONT OF A REGION PREDICT WRITING IN IT?")
    print("=" * 68)
    print(f"occlusion episodes analysed        : {stats['episodes']}")
    print(f"occluded region gained more ink    : {stats['occluded_region_gained_more']}")
    print(f"an unoccluded region gained more   : {stats['control_gained_more']}")
    print(f"median paired difference (px)      : {stats['median_difference_px']:.0f}")
    print(f"Wilcoxon signed-rank p             : {stats['wilcoxon_p']}")
    print(f"exact sign test p                  : {stats['sign_test_p']}")

    best = sorted((e for lec in lectures for e in lec["episodes"] if e["speech"]),
                  key=lambda e: -(e["ink_gain"] - e["control_gain"]))[:args.examples]
    if best:
        print("\nStrongest alignments, region and what was said while standing there:")
        for e in best:
            print(f"\n  {e['from']}-{e['to']}  region {e['region']} "
                  f"(ink +{e['ink_gain']:.0f}, control {e['control_gain']:+.0f})")
            print(f"    \"{e['speech'][:260]}\"")

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(
        json.dumps({"summary": stats, "lectures": lectures}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"\nwrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
