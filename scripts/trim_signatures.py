"""Crop the scanned signatures for the thesis front matter and size them to match.

Two problems with the supplied scans, both of which show on the page.

The first is blank paper. The scans carry very different margins around the
writing: Ahsan's ink fills 80 per cent of its canvas height, Adiba's only 47.
Placing them at a common height therefore prints some signatures much smaller
than others, and sizing them so the writing matches instead makes the roomier
images tall enough to overflow the blank signing gap above the rule and collide
with the text above it. Cropping each scan to its own ink removes both problems.

The second is shape. Even cropped, the signatures are not the same shape at all:
Adiba's is 2.44 times as wide as it is tall, Rafi's only 1.38. Giving those a
common height makes Rafi's a third narrower than hers and it reads as an
accident. Giving them a common width would invert the same complaint. So each
height here is set to hold sqrt(width * height) constant, which is the scale a
reader judges by, and the result is written to sizes.tex for the document to
read. No height is typed into the LaTeX by hand.

Two of the files are also mislabelled: rafi.PNG is a JPEG, and earlier drops had
no extension at all. graphicx picks its reader from the extension and would fail
on both. Re-encoding every crop as a real PNG settles it. Originals are untouched.

Usage:
    python scripts/trim_signatures.py                 report only
    python scripts/trim_signatures.py --apply         write crops and sizes.tex
"""
import math
import os
import pathlib
import sys

import numpy as np
from PIL import Image

REPO = pathlib.Path(os.environ.get("THESIS_REPO") or pathlib.Path(__file__).resolve().parents[1])
SRC = REPO / "Thesis Defense P3" / "drafts" / "thesis" / "esign"
OUT = SRC / "trimmed"

# A pixel counts as ink below this grey level. The scans are dark writing on
# white, so the exact value is not delicate; 160 sits well clear of both.
INK = 160
# Blank kept around the writing, as a fraction of the cropped height, so the
# strokes do not touch the edge of the placed box.
MARGIN = 0.06
# The constant sqrt(width * height), in centimetres, that every signature is
# scaled to. 1.54 puts a typical signature near 1.05cm tall, which fits inside
# the 1.25cm signing gap on the approval page, the tighter of the two.
VISUAL_SIZE = 1.54
# A ceiling, so a nearly square signature cannot climb out of the signing gap.
# The binding gap is the declaration's 1.6cm, not the approval page's 1.25cm:
# the two committee signatures are wide enough that their computed heights come
# out near 1.0cm and never approach this, so only the student signatures can
# reach it and they all sit on the declaration.
MAX_HEIGHT = 1.35

APPLY = "--apply" in sys.argv


def crop_to_ink(path):
    """Return the image cropped to its writing, or None if it is not an image."""
    im = Image.open(path)
    fmt, size = im.format, im.size
    rgb = im.convert("RGB")
    grey = np.array(rgb.convert("L"))
    ink = grey < INK
    if not ink.any():
        return None
    ys, xs = np.nonzero(ink)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pad = int(round((y1 - y0 + 1) * MARGIN))
    box = (max(0, x0 - pad), max(0, y0 - pad),
           min(grey.shape[1], x1 + 1 + pad), min(grey.shape[0], y1 + 1 + pad))
    cropped = rgb.crop(box)
    paper = int(np.percentile(np.array(cropped.convert("L")), 95))
    return cropped, fmt, size, paper


rows = []
for p in sorted(SRC.iterdir()):
    if p.is_dir():
        continue
    try:
        got = crop_to_ink(p)
    except Exception as exc:
        print("  %-24s skipped (%s)" % (p.name, exc))
        continue
    if got is None:
        print("  %-24s skipped (no ink found)" % p.name)
        continue
    cropped, fmt, size, paper = got
    aspect = cropped.size[0] / cropped.size[1]
    height = min(MAX_HEIGHT, VISUAL_SIZE / math.sqrt(aspect))
    stem = p.stem.lower().replace(" ", "-")
    rows.append(dict(src=p, name=p.name, fmt=fmt, size=size, crop=cropped,
                     paper=paper, aspect=aspect, height=height, stem=stem))

print("%-24s %-5s %-12s %-12s %-6s %-7s %-8s %s"
      % ("source", "fmt", "original", "cropped", "paper", "aspect", "height", "width"))
print("-" * 92)
for r in rows:
    print("%-24s %-5s %-12s %-12s %-6d %-7.2f %-8s %.2fcm"
          % (r["name"], r["fmt"], "%dx%d" % r["size"], "%dx%d" % r["crop"].size,
             r["paper"], r["aspect"], "%.2fcm" % r["height"], r["height"] * r["aspect"]))

odd = [r for r in rows if r["paper"] < 250]
if odd:
    print()
    print("WARNING: off-white paper, will show as a grey rectangle on the page: %s"
          % ", ".join(r["name"] for r in odd))

if not APPLY:
    print()
    print("report only; pass --apply to write into %s" % OUT)
    raise SystemExit

OUT.mkdir(exist_ok=True)
for r in rows:
    dest = OUT / (r["stem"] + ".png")
    r["crop"].save(dest, "PNG")
    print("wrote %s" % dest)

sizes = OUT / "sizes.tex"
with open(sizes, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("% Generated by scripts/trim_signatures.py. Do not edit by hand.\n")
    fh.write("% One height per cropped signature, set so that sqrt(width*height)\n")
    fh.write("%% is the same for all of them and no signature exceeds %.2fcm.\n" % MAX_HEIGHT)
    for r in rows:
        fh.write("\\expandafter\\def\\csname esignh@%s\\endcsname{%.3fcm}\n"
                 % (r["stem"], r["height"]))
print("wrote %s" % sizes)
