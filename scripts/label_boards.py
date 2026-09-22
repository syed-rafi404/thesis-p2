#!/usr/bin/env python
"""
=============================================================================
NUMBERED, NAMED BOXES ON EACH CLEAN BOARD (the VLM names what is in each box)
=============================================================================
Step 2 of the final deliverable (CLAUDE.md, "The final deliverable"): for every board of a
lecture, draw numbered coloured boxes around the parts of the writing, then have the
vision-language model say what each box is ("Title", "Truth table", "Gate symbol") and copy
what is written in it. The notes (build_lecture_notes.py) then point at the boxes:
"look at the orange box 3".

WHERE THE BOXES COME FROM
-------------------------
--boxes ink (default)  measured from the ink on the clean board by board_regions.find_regions,
                       after whitening the board's metal frame at the image edges (it would
                       otherwise join everything into one box), dropping specks, and joining
                       boxes that sit side by side on one written line. The VLM sees the board
                       with the numbered boxes drawn on it (Set-of-Mark prompting) and names
                       each; a box it calls "none" (smudge, logo, board edge) is dropped.
--boxes vlm            the VLM finds the blocks itself and returns their coordinates
                       (Qwen2.5-VL grounding). Untested; an option to compare on the 5090.

Only the clean board is used; the lecturer is never boxed (decided with the user 2026-09-22).
Box pixels are never changed: boxes and names are drawn on top of the board.

Outputs, per lecture, in its run folder:
    board_boxes.json                       every board: boxes, colours, names, texts
    figures_annotated/<board>.jpg          the figure for the notes (boxes + names)
    figures_annotated/marked/<board>.jpg   what the VLM saw (boxes + numbers only)
    (--boxes vlm writes board_boxes_vlm.json and figures_annotated_vlm/ instead)
With --mock (no model; for testing the pipeline) the JSON is board_boxes_MOCK.json and names
are positional ("top centre block").

Usage:
    python scripts/label_boards.py --all
    python scripts/label_boards.py --lecture BanglaASR7_004 --mock
    python scripts/label_boards.py --show-prompt
=============================================================================
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_common as nc                                         # noqa: E402
from annotate_board import chip, load_font                        # noqa: E402
from board_regions import find_regions                            # noqa: E402

DEFAULT_VLM = "Qwen/Qwen2.5-VL-7B-Instruct"
MAX_BOXES = 10

NAME_PROMPT = """This is a classroom whiteboard from a university lecture. Numbered coloured boxes
have been drawn on it; each box surrounds one part of the writing. There are {n} boxes,
numbered 1 to {n}.

For every box, reply with:
- "id": the box number.
- "name": 1 to 4 words saying what kind of content the box holds, for example "Title",
  "Definition", "Truth table", "Gate symbol", "Block diagram", "SQL query", "Code",
  "List", "Worked example", "Formula". If the box holds no lecture writing (a smudge,
  a shadow, a logo or sticker, the edge of the board), use "none".
- "text": everything written inside that box, copied exactly: every number, name and
  symbol. For a bar over a term write NOT(...). Write a table as Markdown table rows.
  Write [illegible] for what cannot be read. Never guess.

Reply with JSON only: a list with one object per box, in box order, like
[{{"id": 1, "name": "Title", "text": "Digital Logic Design"}}]"""

GROUND_PROMPT = """This is a classroom whiteboard from a university lecture. Find each separate
block of writing on it: a title, a definition, a table, a diagram, a code block, a list, a
worked example. Ignore smudges, shadows, logos and the edge of the board.

For each block reply with:
- "bbox_2d": [x1, y1, x2, y2], the block's box in pixels of this image.
- "name": 1 to 4 words saying what kind of content it is (for example "Title", "Truth table").
- "text": everything written in the block, copied exactly. Never guess.

Reply with JSON only: a list of objects, top to bottom and left to right."""


# ---------------------------------------------------------------------------
# Boxes from the ink
# ---------------------------------------------------------------------------

def strip_frame(image, margin=0.12, dark=150, band=8, frac=0.22):
    """Whiten everything between each image edge and the board's frame line near it.

    A frame edge is a long straight dark line close to the image edge. Rows (or columns)
    within `margin` of each edge are scored by the share of positions with a dark pixel
    within +-band of that row, which tolerates a slightly slanted edge. The innermost row
    above `frac` is the frame; everything from the image edge to just past it is blanked.
    Handwriting is never that long and straight, so it survives.
    """
    arr = np.asarray(image.convert("L"))
    h, w = arr.shape
    dark_px = arr < dark
    out = np.asarray(image.convert("RGB")).copy()

    def cut_for(lines):
        n = lines.shape[0]
        cum = np.vstack([np.zeros((1, lines.shape[1]), np.int32),
                         np.cumsum(lines, axis=0, dtype=np.int32)])
        best = 0
        for i in range(n):
            a, b = max(0, i - band), min(n, i + band + 1)
            if ((cum[b] - cum[a]) > 0).mean() > frac:
                best = i + band + 2
        return best

    mh, mw = int(h * margin), int(w * margin)
    top = cut_for(dark_px[:mh, :])
    bottom = cut_for(dark_px[h - mh:, :][::-1])
    left = cut_for(dark_px[:, :mw].T)
    right = cut_for(dark_px[:, w - mw:].T[::-1])
    if top:
        out[:top, :] = 255
    if bottom:
        out[h - bottom:, :] = 255
    if left:
        out[:, :left] = 255
    if right:
        out[:, w - right:] = 255
    return Image.fromarray(out)


def join_line_parts(regions, image_w, gap_ratio=1.8, max_gap_frac=0.04, min_overlap=0.5,
                    max_height_ratio=3.0):
    """Join boxes side by side on one written line ("DF" | "=>" | "Don't Fragment").

    The gap must be small both next to the letter height and in absolute terms (4% of the
    board width): letter height alone joined "NAND gate = AND+NOT" to a block diagram 156 px
    away, because both are about 100 px tall.
    """
    max_gap = max_gap_frac * image_w
    boxes = [dict(r) for r in regions]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            if boxes[i] is None:
                continue
            for j in range(len(boxes)):
                if i == j or boxes[j] is None:
                    continue
                a, b = boxes[i]["bbox"], boxes[j]["bbox"]
                ha, hb = a[3] - a[1], b[3] - b[1]
                shorter, taller = max(1, min(ha, hb)), max(ha, hb)
                if taller > max_height_ratio * shorter:
                    continue
                if min(a[3], b[3]) - max(a[1], b[1]) < min_overlap * shorter:
                    continue
                gap = max(b[0] - a[2], a[0] - b[2])
                if gap > gap_ratio * shorter or gap > max_gap:
                    continue
                boxes[i]["bbox"] = [min(a[0], b[0]), min(a[1], b[1]),
                                    max(a[2], b[2]), max(a[3], b[3])]
                boxes[i]["ink_pixels"] = boxes[i].get("ink_pixels", 0) + boxes[j].get("ink_pixels", 0)
                boxes[j] = None
                changed = True
        boxes = [b for b in boxes if b is not None]
    return boxes


def reading_order(boxes, image_h):
    tolerance = max(8, image_h // 14)
    ordered = sorted(boxes, key=lambda r: (r["bbox"][1], r["bbox"][0]))
    rows, current = [], []
    for box in ordered:
        if current and box["bbox"][1] - current[0]["bbox"][1] > tolerance:
            rows.append(sorted(current, key=lambda r: r["bbox"][0]))
            current = []
        current.append(box)
    if current:
        rows.append(sorted(current, key=lambda r: r["bbox"][0]))
    return [b for row in rows for b in row]


def is_writing(gray, region, w, h, dark=90, min_dark_px=100, edge=3):
    """False for leftovers that are not pen strokes.

    On a cleaned board the leftover smudges and frame scraps are light grey, while pen
    strokes have properly dark pixels. Measured on the TTL, NAND and MTU boards
    (2026-09-22): every box of writing had at least 231 pixels darker than 90 (the faint
    "DF"), every smudge or frame scrap 0 to 30. An ink-amount threshold could not tell them
    apart: "DF" has less ink than a smudge. Dark shadow blobs still pass; the VLM names
    those "none". Thin strips touching the image edge are the board's frame.
    """
    x1, y1, x2, y2 = region["bbox"]
    if region["area_fraction"] < 0.0006:
        return False
    touches = x1 <= edge or y1 <= edge or x2 >= w - edge or y2 >= h - edge
    if touches and ((y2 - y1) < 0.05 * h or (x2 - x1) < 0.04 * w):
        return False
    return int((gray[y1:y2, x1:x2] < dark).sum()) >= min_dark_px


def ink_boxes(image, max_boxes=MAX_BOXES):
    """Boxes around the writing of a clean board, numbered in reading order."""
    w, h = image.size
    stripped = strip_frame(image)
    gray = np.asarray(stripped.convert("L"))
    regions = find_regions(stripped, remove_person=False)
    regions = [r for r in regions if is_writing(gray, r, w, h)]
    regions = join_line_parts(regions, w)
    if len(regions) > max_boxes:
        regions = sorted(regions, key=lambda r: -r.get("ink_pixels", 0))[:max_boxes]
    pad = max(4, w // 240)
    boxes = []
    for r in reading_order(regions, h):
        x1, y1, x2, y2 = r["bbox"]
        boxes.append({"bbox": [max(0, x1 - pad), max(0, y1 - pad),
                               min(w, x2 + pad), min(h, y2 + pad)],
                      "ink_pixels": int(r.get("ink_pixels", 0))})
    return number(boxes)


def number(boxes):
    for k, box in enumerate(boxes, 1):
        name, hex_ = nc.colour(k)
        box.update({"id": k, "colour": name, "hex": hex_})
    return boxes


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_boxes(image, boxes, with_names):
    """Boxes and number chips (and names) on top of the unchanged board pixels."""
    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    w, h = canvas.size
    font = load_font(max(20, w // 64))
    line_w = max(3, w // 400)
    chip_h = getattr(font, "size", 20) + 12
    for box in boxes:
        draw.rectangle(box["bbox"], outline=box["hex"], width=line_w)
    placed = []
    for box in boxes:
        text = f"{box['id']}  {box['name']}" if with_names and box.get("name") else str(box["id"])
        size = (draw.textlength(text, font=font) + 12, chip_h)
        pos = chip_position(box, boxes, placed, size, w, h)
        placed.append([pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]])
        chip(draw, pos, text, font, box["hex"])
    return canvas


def chip_position(box, boxes, placed, size, w, h):
    """Where a label chip covers the least writing and the fewest other labels.

    Tried in order: above the box on the left, above on the right, below on the left,
    inside the top-left corner. Ties go to the earlier spot.
    """
    x1, y1, x2, y2 = box["bbox"]
    cw, ch = size
    spots = [(x1, y1 - ch - 2), (x2 - cw, y1 - ch - 2), (x1, y2 + 2), (x1 + 2, y1 + 2)]

    def overlap(a, b):
        return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))

    best, best_cost = None, None
    for sx, sy in spots:
        sx, sy = min(max(0, sx), w - cw), min(max(0, sy), h - ch)
        rect = [sx, sy, sx + cw, sy + ch]
        cost = sum(overlap(rect, other["bbox"]) for other in boxes if other is not box)
        cost += 4 * sum(overlap(rect, p) for p in placed)
        if best_cost is None or cost < best_cost:
            best, best_cost = (sx, sy), cost
    return best


# ---------------------------------------------------------------------------
# The vision-language model
# ---------------------------------------------------------------------------

def parse_json_list(text):
    """The first JSON list in a model reply, tolerating code fences and trailing commas."""
    text = re.sub(r"```(?:json)?", "", text)
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        return None
    chunk = re.sub(r",\s*([\]}])", r"\1", text[start:end + 1])
    try:
        data = json.loads(chunk)
    except json.JSONDecodeError:
        return None
    return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else None


class Vlm:
    def __init__(self, model_id, max_pixels):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from transcribe_boards import load_vlm
        self.model_id = model_id
        self.model, self.processor = load_vlm(model_id, max_pixels)

    def ask(self, image, prompt, max_new_tokens=1500):
        import torch
        messages = [{"role": "user", "content": [{"type": "image", "image": image},
                                                 {"type": "text", "text": prompt}]}]
        chat = self.processor.apply_chat_template(messages, tokenize=False,
                                                  add_generation_prompt=True)
        inputs = self.processor(text=[chat], images=[image], return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False,
                                      repetition_penalty=1.05)
        reply = self.processor.decode(out[0][inputs["input_ids"].shape[1]:],
                                      skip_special_tokens=True).strip()
        grid = inputs.get("image_grid_thw")
        seen = None
        if grid is not None:
            _, gh, gw = [int(v) for v in grid[0]]
            seen = (gw * 14, gh * 14)          # the image size the model actually saw
        return reply, seen


def name_boxes(vlm, marked, boxes):
    """Ask the VLM for each box's name and text. Returns (boxes, raw reply, parsed ok)."""
    reply, _ = vlm.ask(marked, NAME_PROMPT.format(n=len(boxes)))
    data = parse_json_list(reply)
    if data is None:
        reply2, _ = vlm.ask(marked, NAME_PROMPT.format(n=len(boxes))
                            + "\n\nYour previous answer was not valid JSON. Reply with the JSON list only.")
        data, reply = parse_json_list(reply2), reply + "\n---retry---\n" + reply2
    by_id = {}
    for d in data or []:
        try:
            by_id[int(d.get("id"))] = d
        except (TypeError, ValueError):
            continue
    for box in boxes:
        d = by_id.get(box["id"], {})
        box["name"] = str(d.get("name", "")).strip()
        box["text"] = str(d.get("text", "")).strip()
    return boxes, reply, data is not None


def ground_boxes(vlm, image):
    """The VLM finds the blocks itself (--boxes vlm)."""
    reply, seen = vlm.ask(image, GROUND_PROMPT)
    data = parse_json_list(reply) or []
    w, h = image.size
    sx, sy = (w / seen[0], h / seen[1]) if seen else (1.0, 1.0)
    boxes = []
    for d in data:
        bb = d.get("bbox_2d") or d.get("bbox")
        if not (isinstance(bb, list) and len(bb) == 4):
            continue
        x1, y1, x2, y2 = [float(v) for v in bb]
        box = [int(max(0, x1 * sx)), int(max(0, y1 * sy)), int(min(w, x2 * sx)), int(min(h, y2 * sy))]
        if box[2] - box[0] < 8 or box[3] - box[1] < 8:
            continue
        boxes.append({"bbox": box, "name": str(d.get("name", "")).strip(),
                      "text": str(d.get("text", "")).strip()})
    return number(reading_order(boxes, h)), reply, bool(data)


def mock_names(boxes, image):
    from board_regions import describe
    w, h = image.size
    for box in boxes:
        box["name"] = describe({"bbox": box["bbox"]}, w, h)
        box["text"] = ""
    return boxes


# ---------------------------------------------------------------------------

def label_lecture(name, info, vlm, args):
    run_dir = info["run_dir"]
    if run_dir is None:
        print(f"{name:<16} skipped: no run folder")
        return
    eras = nc.board_eras(info["board_dir"])
    fig_dir = run_dir / ("figures_annotated_vlm" if args.boxes == "vlm" else "figures_annotated")
    (fig_dir / "marked").mkdir(parents=True, exist_ok=True)
    boards = []
    for era in eras:
        src = era["clean"] or era["mosaic"]
        image = Image.open(src).convert("RGB")
        reply, ok = "", True
        if args.boxes == "vlm" and vlm is not None:
            boxes, reply, ok = ground_boxes(vlm, image)
        else:
            boxes = ink_boxes(image)
            marked = draw_boxes(image, boxes, with_names=False)
            marked.save(fig_dir / "marked" / f"{era['stem']}.jpg", quality=90)
            if vlm is None:
                boxes = mock_names(boxes, image)
            else:
                boxes, reply, ok = name_boxes(vlm, marked, boxes)
        found = len(boxes)
        boxes = number([b for b in boxes if b.get("name", "").lower() not in ("none", "")
                        or vlm is None])
        figure = draw_boxes(image, boxes, with_names=True)
        fig_name = f"{era['stem']}{'_MOCK' if vlm is None else ''}.jpg"
        figure.save(fig_dir / fig_name, quality=90)
        boards.append({
            "era": era["era"], "from": era["from"], "to": era["to"],
            "clean": era["clean"] is not None,
            "source_image": str(Path(src).relative_to(nc.REPO)) if nc.REPO in Path(src).parents else str(src),
            "figure": (fig_dir / fig_name).relative_to(run_dir).as_posix(),
            "boxes_found": found, "boxes_kept": len(boxes), "vlm_json_ok": ok,
            "boxes": boxes, "vlm_reply": reply,
        })
        print(f"{name:<16} {era['from']:>5}-{era['to']:<5} boxes {found} -> {len(boxes)}"
              f"{'' if ok else '   (VLM reply was not JSON; names left empty)'}")
    payload = {"lecture": name, "boxes_from": args.boxes,
               "model": None if vlm is None else vlm.model_id, "mock": vlm is None,
               "prompt": GROUND_PROMPT if args.boxes == "vlm" else NAME_PROMPT,
               "boards": boards}
    out = nc.boxes_file(run_dir, mock=vlm is None)
    if args.boxes == "vlm":
        out = out.with_name(out.stem + "_vlm.json")          # board_boxes_vlm.json, kept apart
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{name:<16} -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lecture", action="append", help="Lecture name, e.g. BanglaASR7_004 (repeatable)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--boxes", choices=("ink", "vlm"), default="ink")
    ap.add_argument("--model", default=DEFAULT_VLM)
    ap.add_argument("--max-pixels", type=int, default=1920 * 1080)
    ap.add_argument("--mock", action="store_true", help="No model: positional names, for testing")
    ap.add_argument("--show-prompt", action="store_true")
    args = ap.parse_args()
    nc.utf8_console()

    if args.show_prompt:
        print(NAME_PROMPT.format(n=6) if args.boxes == "ink" else GROUND_PROMPT)
        return 0
    lectures = nc.discover_lectures()
    if args.lecture:
        missing = [n for n in args.lecture if n not in lectures]
        if missing:
            sys.exit(f"no boards for {missing}; known: {', '.join(lectures)}")
        lectures = {n: lectures[n] for n in args.lecture}
    elif not args.all:
        sys.exit("pass --lecture <name>, --all or --show-prompt")

    vlm = None if args.mock else Vlm(args.model, args.max_pixels)
    for name, info in lectures.items():
        label_lecture(name, info, vlm, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
