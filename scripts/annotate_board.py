#!/usr/bin/env python
"""
=============================================================================
RENDER AN ANNOTATED BOARD FIGURE
=============================================================================
Takes a lecture frame, the content regions found by board_regions.py, and a
label for each region, and draws a figure a student can read: every block of
the board outlined, named, and explained, with the spoken context underneath.

WHY NOTHING IS GENERATED
------------------------
A vision-language model cannot draw, and for this job it must not. If a model
redrew the board, every stroke in the figure would be something the model
invented, and a truth table or an automaton that looks plausible but differs
from what the lecturer actually wrote is worse than no figure at all.

So the pixels of the board are never touched. The figure is the real frame with
a geometric overlay:

    board_regions.py   geometry   decides WHERE the content is
    the VLM            text       decides WHAT each region is called
    this file          PIL        draws boxes and text onto the real pixels

Every mark on the output is therefore traceable. A box comes from measured ink,
a name comes from a recorded model reply, and the caption comes from the
transcript. Nothing in the image is synthesised, which is exactly the property
that makes the figure usable as evidence in a thesis.

The VLM is a reader here, not a painter.

Usage:
    python scripts/annotate_board.py --frame f.jpg --labels labels.json --out fig.jpg

labels.json is a list, one entry per region id:
    [{"id": 1, "label": "Topic title", "note": "Digital Logic Design"}, ...]
Regions without a label are drawn but left unnamed.
=============================================================================
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from board_regions import find_regions            # noqa: E402

BOX_COLOURS = ["#e63946", "#2a9d8f", "#f4a261", "#4361ee", "#b5179e", "#43aa8b"]
PANEL_BG = "#12151a"
PANEL_FG = "#eef2f6"
CAPTION_FG = "#b8c4d0"


def load_font(px, bold=True):
    names = ("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names + ("DejaVuSans.ttf",):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def chip(draw, xy, text, font, fill, fg="white", pad=6):
    """A filled rounded label chip, so text stays readable over any background."""
    x, y = xy
    w = draw.textlength(text, font=font)
    h = getattr(font, "size", 16)
    box = [x, y, x + w + 2 * pad, y + h + 2 * pad]
    try:
        draw.rounded_rectangle(box, radius=max(3, pad // 2), fill=fill)
    except AttributeError:                      # very old Pillow
        draw.rectangle(box, fill=fill)
    draw.text((x + pad, y + pad), text, font=font, fill=fg)
    return box


def render(image, regions, labels, caption="", stamp="", title=""):
    """Draw boxes and names on the frame, with an explanation panel beneath."""
    image = image.convert("RGB")
    w, h = image.size
    by_id = {int(entry["id"]): entry for entry in labels if "id" in entry}

    named = [r for r in regions if by_id.get(r["id"], {}).get("label")]
    panel_rows = named or regions
    name_font = load_font(max(17, w // 78))
    body_font = load_font(max(15, w // 95), bold=False)
    head_font = load_font(max(20, w // 62))
    line_h = getattr(body_font, "size", 16) + 7

    # Measure the panel before creating the canvas, so nothing is clipped.
    probe = ImageDraw.Draw(image.copy())
    text_width = w - int(w * 0.06)
    wrapped = []
    for region in panel_rows:
        entry = by_id.get(region["id"], {})
        name = entry.get("label") or region.get("position", "")
        note = entry.get("note", "")
        body = f"{name}. {note}" if note else name
        wrapped.append((region["id"], wrap(probe, body, body_font, text_width - 54)))

    panel_h = int(line_h * sum(len(t) for _, t in wrapped)
                  + line_h * len(wrapped) * 0.45
                  + (getattr(head_font, "size", 20) + 18 if title else 0)
                  + (line_h if caption else 0) + 34)

    canvas = Image.new("RGB", (w, h + panel_h), PANEL_BG)
    canvas.paste(image, (0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    line_w = max(3, w // 440)

    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        colour = BOX_COLOURS[(region["id"] - 1) % len(BOX_COLOURS)]
        entry = by_id.get(region["id"], {})
        draw.rectangle([x1, y1, x2, y2], outline=colour, width=line_w)

        tag = str(region["id"])
        name = entry.get("label", "")
        text = f"{tag}  {name}" if name else tag
        chip_h = getattr(name_font, "size", 18) + 12
        above = y1 - chip_h - 4
        pos = (x1, above if above > 2 else min(h - chip_h - 2, y2 + 4))
        chip(draw, pos, text, name_font, colour)

    y = h + 16
    if title:
        draw.text((int(w * 0.03), y), title, font=head_font, fill=PANEL_FG)
        y += getattr(head_font, "size", 20) + 14

    for region_id, lines in wrapped:
        colour = BOX_COLOURS[(region_id - 1) % len(BOX_COLOURS)]
        draw.rectangle([int(w * 0.03), y + 4, int(w * 0.03) + 5, y + line_h * len(lines)],
                       fill=colour)
        for i, line in enumerate(lines):
            prefix = f"{region_id}. " if i == 0 else "   "
            draw.text((int(w * 0.03) + 16, y), prefix + line, font=body_font, fill=PANEL_FG)
            y += line_h
        y += int(line_h * 0.45)

    if caption:
        label = f'[{stamp}] "{caption}"' if stamp else f'"{caption}"'
        for line in wrap(draw, label, body_font, text_width):
            draw.text((int(w * 0.03), y), line, font=body_font, fill=CAPTION_FG)
            y += line_h

    return canvas


def main():
    ap = argparse.ArgumentParser(description="Draw an annotated figure of a lecture board")
    ap.add_argument("--frame", required=True)
    ap.add_argument("--labels", default=None,
                    help="JSON list of {id, label, note}. Without it, positions are used")
    ap.add_argument("--regions", default=None,
                    help="Reuse a saved regions JSON instead of detecting again")
    ap.add_argument("--out", required=True)
    ap.add_argument("--caption", default="", help="What the lecturer was saying")
    ap.add_argument("--stamp", default="", help="Timestamp, for example 6:40")
    ap.add_argument("--title", default="", help="Heading for the panel")
    args = ap.parse_args()

    frame = Path(args.frame)
    if not frame.exists():
        sys.exit(f"no such frame: {frame}")
    image = Image.open(frame)

    if args.regions:
        regions = json.loads(Path(args.regions).read_text(encoding="utf-8"))
    else:
        regions = find_regions(image)

    labels = []
    if args.labels:
        labels = json.loads(Path(args.labels).read_text(encoding="utf-8"))

    canvas = render(image, regions, labels,
                    caption=args.caption, stamp=args.stamp, title=args.title)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=92)
    print(f"regions drawn : {len(regions)}")
    print(f"labels applied: {sum(1 for e in labels if e.get('label'))}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
