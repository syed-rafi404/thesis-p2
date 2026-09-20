#!/usr/bin/env python
"""
=============================================================================
ILLUSTRATE LECTURE NOTES WITH ANNOTATED VIDEO FRAMES
=============================================================================
Post-processing step. Takes a finished run directory and produces a second
Markdown file in which each section is illustrated by the board/screen frame
that belongs to it, with the relevant regions boxed and labelled.

It never modifies the original notes and never re-runs ASR, fusion or the
summarizer. Everything it needs is already saved by the pipeline:

    <run_dir>/final_lecture_notes.md
    <run_dir>/temporal_visual_context.json     (per-frame keywords, optional)
    <run_dir>/ingested/frames/*.jpg

Two annotation modes:

    --no-vlm   (default) labels come from the keywords already extracted for
               that frame. No GPU, no model download. Good for checking the
               selection and layout.

    --vlm      asks a vision-language model for a caption and bounding boxes
               for the regions that matter to this section, then draws them.

Usage:
    python scripts/illustrate_notes.py --run-dir output/live_focused/no_gaze/interval_10s/BanglaASR1
    python scripts/illustrate_notes.py --run-dir <dir> --vlm --model Qwen/Qwen2.5-VL-7B-Instruct

Outputs:
    <run_dir>/final_lecture_notes_illustrated.md
    <run_dir>/figures/fig_NN_mmss.jpg
    <run_dir>/figures/figures.json      selection record, for evaluation
=============================================================================
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit("Pillow is required: pip install pillow")


# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------

BOX_COLORS = ["#e8590c", "#1c7ed6", "#2f9e44", "#ae3ec9", "#f08c00"]
CAPTION_BAR_H = 0.085      # fraction of image height
MIN_VISUAL_CHANGE = 4.0    # mean abs pixel diff (0-255) to call a frame "new"
PERSON_DARK = 118          # below this brightness a pixel may be the lecturer
PERSON_SAT = 42            # above this colourfulness a pixel may be the lecturer
MASK_WIDTH = 480           # work out the person mask at this width, then scale up
DEVIATION_DIFF = 26        # deviation from the reconstructed board that means "covered"
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "was", "it",
    "this", "that", "we", "you", "for", "on", "with", "as", "be", "can", "will",
    "what", "how", "example", "examples", "lecture", "notes", "section",
}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_sections(md_text):
    """Split Markdown into sections at ## / ### headings."""
    lines = md_text.splitlines()
    sections, cur = [], None
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,6})\s+(.*\S)\s*$", line)
        if m:
            if cur:
                cur["end"] = i
                sections.append(cur)
            cur = {"level": len(m.group(1)), "title": m.group(2), "start": i, "end": len(lines)}
    if cur:
        sections.append(cur)
    for s in sections:
        s["body"] = "\n".join(lines[s["start"] + 1:s["end"]])
    return lines, sections


def timestamp_from_name(name):
    """frame_000003_000030s.jpg -> 30.0"""
    m = re.search(r"_(\d+)s\.", name)
    return float(m.group(1)) if m else None


def load_frames(run_dir):
    """Frames on disk, each with a timestamp and any keywords the VLM found."""
    frames_dir = run_dir / "ingested" / "frames"
    if not frames_dir.is_dir():
        return []

    on_disk = {p.name: p for p in sorted(frames_dir.glob("*.jpg"))}

    # Keywords are stored with absolute paths from the machine that ran the
    # pipeline, so match on file name only.
    kw_by_name = {}
    tvc = run_dir / "temporal_visual_context.json"
    if tvc.is_file():
        try:
            data = json.loads(tvc.read_text(encoding="utf-8"))
            for entry in data.get("frame_keywords", []):
                name = Path(str(entry.get("frame_path", ""))).name
                kw_by_name[name] = [k for k in entry.get("keywords", []) if k]
        except (ValueError, OSError):
            pass

    frames = []
    for name, path in on_disk.items():
        t = timestamp_from_name(name)
        if t is None:
            continue
        frames.append({"path": path, "t": t, "keywords": kw_by_name.get(name, [])})
    frames.sort(key=lambda f: f["t"])
    return frames


# ---------------------------------------------------------------------------
# Frame selection
# ---------------------------------------------------------------------------

def visual_change(path_a, path_b, size=96):
    """Mean absolute difference between two frames, 0-255."""
    try:
        a = Image.open(path_a).convert("L").resize((size, size))
        b = Image.open(path_b).convert("L").resize((size, size))
    except OSError:
        return 0.0
    hist = ImageChops.difference(a, b).histogram()
    total = sum(hist)
    if not total:
        return 0.0
    return sum(i * n for i, n in enumerate(hist)) / total


def board_change_series(frames, size=96, window=5):
    """How much the *board* changed, with the lecturer removed.

    A plain frame difference is dominated by the person moving in front of the
    board, so it cannot tell writing from walking. Taking a per-pixel median
    over a short window of frames suppresses anything that moves and keeps
    what stays put, which is the board. Differences are then computed between
    consecutive backgrounds.
    """
    small = []
    for f in frames:
        try:
            small.append(Image.open(f["path"]).convert("L").resize((size, size)).tobytes())
        except OSError:
            small.append(None)
    valid = [p for p in small if p is not None]
    if len(valid) < 2:
        return [0.0] * len(frames)

    half = max(1, window // 2)
    backgrounds = []
    for i in range(len(small)):
        lo, hi = max(0, i - half), min(len(small), i + half + 1)
        stack = [p for p in small[lo:hi] if p is not None]
        if not stack:
            backgrounds.append(backgrounds[-1] if backgrounds else [0] * (size * size))
            continue
        mid = len(stack) // 2
        backgrounds.append([sorted(px)[mid] for px in zip(*stack)])

    out = [255.0]
    for i in range(1, len(backgrounds)):
        a, b = backgrounds[i - 1], backgrounds[i]
        out.append(sum(abs(x - y) for x, y in zip(a, b)) / len(a))
    return out


def select_candidates(frames, min_change=MIN_VISUAL_CHANGE):
    """Keep frames that add new board content, drop near-duplicates.

    A frame is a candidate if it introduces keywords not seen before, or if the
    board itself changed since the last frame kept. The board is static most of
    the time, so this usually removes a large share of the frames.
    """
    changes = board_change_series(frames)
    seen, out = set(), []
    pending = 0.0
    for f, change in zip(frames, changes):
        new_kw = [k for k in f["keywords"] if k.lower() not in seen]
        pending += change
        if new_kw or pending >= min_change or not out:
            out.append({**f, "new_keywords": new_kw, "change": round(pending, 2)})
            seen.update(k.lower() for k in f["keywords"])
            pending = 0.0
    return out


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9_]+", text.lower()) if w not in STOPWORDS and len(w) > 2}


def score_matrix(sections, candidates):
    """Keyword overlap between each section and each candidate frame."""
    grid = {}
    for si, sec in enumerate(sections):
        sec_tokens = tokens(sec["title"] + " " + sec["body"])
        if not sec_tokens:
            continue
        for ci, cand in enumerate(candidates):
            kw_tokens = tokens(" ".join(cand["keywords"]))
            if not kw_tokens:
                continue
            overlap = sec_tokens & kw_tokens
            if not overlap:
                continue
            score = len(overlap) / len(kw_tokens) ** 0.5 + 0.25 * len(cand["new_keywords"])
            grid[(si, ci)] = (score, sorted(overlap))
    return grid


def match_sections(sections, candidates, max_figures):
    """Align note sections to frames, keeping both in order.

    A lecture moves forward in time and the notes follow it, so a figure for a
    later section should not come from an earlier moment in the video. This is
    a monotonic alignment: it maximises total match score subject to both the
    section index and the frame time increasing. Solved exactly by dynamic
    programming over (section, frame, figures used).
    """
    grid = score_matrix(sections, candidates)
    n, m, K = len(sections), len(candidates), max_figures

    best = {}

    def solve(si, ci, used):
        """Best achievable score from section si onward, frames from ci onward."""
        if si >= n or used >= K:
            return 0.0, []
        key = (si, ci, used)
        if key in best:
            return best[key]
        # Option 1: this section gets no figure.
        top, plan = solve(si + 1, ci, used)
        # Option 2: pair it with some later frame.
        for cj in range(ci, m):
            entry = grid.get((si, cj))
            if not entry:
                continue
            score, overlap = entry
            rest, rest_plan = solve(si + 1, cj + 1, used + 1)
            total = score + rest
            if total > top:
                top = total
                plan = [{"section": si, "cand": cj, "score": round(score, 3), "overlap": overlap}] + rest_plan
        best[key] = (top, plan)
        return best[key]

    sys.setrecursionlimit(10000 + n * 20)
    _, chosen = solve(0, 0, 0)

    # Fallback: no usable keywords at all, for instance when the vision branch
    # failed for this lecture. Spread figures over the most changed frames.
    if not chosen and candidates and sections:
        ranked = sorted(range(m), key=lambda i: -candidates[i]["change"])[:max_figures]
        for n_i, ci in enumerate(sorted(ranked)):
            if n_i >= len(sections):
                break
            chosen.append({"section": n_i, "cand": ci, "score": 0.0, "overlap": []})

    return chosen


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

_MASK_CACHE = {}


def _person_mask(np, image, key=None):
    """Mask of the lecturer, without masking the handwriting.

    The board is bright and nearly grey; the lecturer is darker or more
    colourful. Pen strokes are also dark, so a plain threshold would erase the
    writing too. Eroding then dilating removes anything as thin as a stroke and
    keeps only large blobs, which is the person.

    Morphology runs on a downscaled copy, which is both far faster and less
    sensitive to single-pixel noise. The mask is then scaled back up.
    """
    if key is not None and key in _MASK_CACHE:
        return _MASK_CACHE[key]

    full_w, full_h = image.size
    scale = MASK_WIDTH / float(full_w)
    small = image.resize((MASK_WIDTH, max(1, int(full_h * scale))))
    arr = np.asarray(small, dtype=np.int16)
    gray = arr.mean(axis=2)
    saturation = arr.max(axis=2) - arr.min(axis=2)
    raw = ((gray < PERSON_DARK) | (saturation > PERSON_SAT)).astype(np.uint8) * 255

    img = Image.fromarray(raw)
    img = img.filter(ImageFilter.MinFilter(5))    # erode: thin strokes vanish
    img = img.filter(ImageFilter.MaxFilter(11))   # dilate: restore the blob
    mask = np.asarray(img.resize((full_w, full_h), Image.NEAREST), dtype=bool)

    if key is not None:
        _MASK_CACHE[key] = mask
    return mask


def _reconstruct_with_numpy(np, frames, idx, lo, hi, paths):
    """Replace the lecturer with the board behind him.

    For every pixel he covers, take the value from the frame closest in time
    where that same pixel is clear. Pixels he does not cover keep this frame's
    own values, so writing made at this moment stays sharp.
    """
    base = Image.open(frames[idx]["path"]).convert("RGB")
    target = np.asarray(base, dtype=np.uint8)

    order = sorted(range(lo, hi), key=lambda i: abs(i - idx))
    frames_rgb, masks = {}, {}
    for i in order:
        im = Image.open(frames[i]["path"]).convert("RGB")
        if im.size != base.size:
            im = im.resize(base.size)
        frames_rgb[i] = np.asarray(im, dtype=np.uint8)
        masks[i] = _person_mask(np, im, key=str(frames[i]["path"]))

    # Second pass. Parts of clothing can be as pale and as grey as the board,
    # so the colour test alone misses them. Build a reference board from the
    # pixels no frame flagged as person, then flag whatever deviates from it by
    # a large connected amount. The erode/dilate step means pen strokes, which
    # are thin, survive this test and are never painted over.
    total = np.zeros(target.shape, dtype=np.float32)
    count = np.zeros(target.shape[:2], dtype=np.float32)
    for i, arr in frames_rgb.items():
        clear = ~masks[i]
        total[clear] += arr[clear]
        count[clear] += 1
    reference = total / np.maximum(count, 1)[:, :, None]
    deviation = np.abs(target.astype(np.float32) - reference).mean(axis=2)
    dev_raw = Image.fromarray(((deviation > DEVIATION_DIFF) * 255).astype(np.uint8))
    scale = MASK_WIDTH / float(dev_raw.width)
    dev_small = dev_raw.resize((MASK_WIDTH, max(1, int(dev_raw.height * scale))))
    dev_small = dev_small.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(11))
    dev_mask = np.asarray(dev_small.resize(dev_raw.size, Image.NEAREST), dtype=bool)
    dev_mask &= count > 0
    masks[idx] = masks[idx] | dev_mask

    hole = masks[idx]
    covered = float(hole.mean())
    if covered > 0.6:      # mostly person, nothing worth reconstructing
        return base, "single frame (too much occlusion to rebuild)"

    out = target.copy()
    remaining = hole.copy()
    used = 0
    for i in order:
        if i == idx or not remaining.any():
            continue
        fillable = remaining & ~masks[i]
        if not fillable.any():
            continue
        out[fillable] = frames_rgb[i][fillable]
        remaining &= ~fillable
        used += 1

    if remaining.any():
        stack = np.stack([frames_rgb[i] for i in order])
        median = np.median(stack, axis=0).astype(np.uint8)
        out[remaining] = median[remaining]

    recovered = covered - float(remaining.mean())
    return (
        Image.fromarray(out),
        f"lecturer covered {covered:.0%}, {recovered / covered:.0%} rebuilt from {used} nearby frames"
        if covered > 0 else "no occlusion detected",
    )


def clean_board_image(frames, idx, window=9):
    """Rebuild the board with the lecturer removed.

    The person moves between frames and the writing does not, so a per-pixel
    median over a window of nearby frames keeps the board and erases whoever
    is standing in front of it. Falls back to picking the least occluded
    nearby frame when numpy is unavailable.

    Returns (image, method).
    """
    half = max(1, window // 2)
    lo, hi = max(0, idx - half), min(len(frames), idx + half + 1)
    paths = [f["path"] for f in frames[lo:hi]]
    if len(paths) < 3:
        return Image.open(frames[idx]["path"]).convert("RGB"), "single frame"

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        try:
            return _reconstruct_with_numpy(np, frames, idx, lo, hi, paths)
        except (OSError, ValueError, MemoryError):
            pass

    # Fallback: the frame closest to the local background has the least of the
    # lecturer in it.
    size = 96
    smalls = []
    for p in paths:
        try:
            smalls.append(Image.open(p).convert("L").resize((size, size)).tobytes())
        except OSError:
            smalls.append(None)
    usable = [s for s in smalls if s is not None]
    if not usable:
        return Image.open(frames[idx]["path"]).convert("RGB"), "single frame"
    mid = len(usable) // 2
    background = [sorted(px)[mid] for px in zip(*usable)]

    best_i, best_d = None, None
    for i, s in enumerate(smalls):
        if s is None:
            continue
        d = sum(abs(a - b) for a, b in zip(s, background)) / len(background)
        if best_d is None or d < best_d:
            best_i, best_d = i, d
    chosen = paths[best_i if best_i is not None else 0]
    return Image.open(chosen).convert("RGB"), f"least occluded of {len(usable)} frames"


def load_font(px):
    for name in ("segoeuib.ttf", "arialbd.ttf", "segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def mmss(seconds):
    return f"{int(seconds) // 60}:{int(seconds) % 60:02d}"


def draw_annotation(img, out_path, regions, caption, stamp):
    """Draw boxes with numbered labels and a caption bar under the frame."""
    img = img.convert("RGB")
    w, h = img.size
    bar_h = max(48, int(h * CAPTION_BAR_H))
    canvas = Image.new("RGB", (w, h + bar_h), "#111111")
    canvas.paste(img, (0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")

    line_w = max(3, w // 400)
    tag_font = load_font(max(18, w // 45))
    cap_font = load_font(max(15, w // 65))

    for i, reg in enumerate(regions):
        box = reg.get("bbox")
        if not box or len(box) != 4:
            continue
        x1, y1, x2, y2 = box
        x1, x2 = sorted((max(0, min(w, x1)), max(0, min(w, x2))))
        y1, y2 = sorted((max(0, min(h, y1)), max(0, min(h, y2))))
        if x2 - x1 < 4 or y2 - y1 < 4:
            continue
        color = BOX_COLORS[i % len(BOX_COLORS)]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_w)

        tag = str(i + 1)
        tw = draw.textlength(tag, font=tag_font)
        th = tag_font.size if hasattr(tag_font, "size") else 16
        pad = max(4, line_w * 2)
        draw.rectangle([x1, max(0, y1 - th - 2 * pad), x1 + tw + 2 * pad, y1], fill=color)
        draw.text((x1 + pad, max(0, y1 - th - pad)), tag, fill="white", font=tag_font)

    legend = "  ".join(
        f"{i + 1}. {r.get('label', '')}" for i, r in enumerate(regions) if r.get("label")
    )
    text = caption if not legend else f"{caption}\n{legend}"
    draw.text((12, h + 8), f"[{stamp}]  {text}", fill="#f1f3f5", font=cap_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=90)
    return out_path


# ---------------------------------------------------------------------------
# Annotation sources
# ---------------------------------------------------------------------------

def keyword_annotation(cand, section_title):
    """No-GPU fallback: label the frame with what was already extracted."""
    kws = cand["new_keywords"] or cand["keywords"]
    # Drop OCR debris: bare numbers, date fragments like "01-", stray letters.
    labels = [
        k for k in kws
        if len(k.strip()) > 2 and re.search(r"[A-Za-z]{3}", k)
    ][:4]
    caption = f"Board during: {section_title}"
    return [{"label": k, "bbox": None} for k in labels], caption


VLM_PROMPT = (
    "You are annotating one frame from a recorded classroom lecture.\n"
    "The lecture notes section being illustrated is titled: \"{title}\".\n"
    "Find up to 4 regions of the whiteboard or screen that a student would need "
    "to understand this section. Prefer written code, values, table cells and "
    "labelled diagrams over decoration.\n"
    "Reply with JSON only, no prose:\n"
    '{{"caption": "one sentence, max 20 words", '
    '"regions": [{{"label": "short text, max 6 words", "bbox": [x1, y1, x2, y2]}}]}}\n'
    "bbox values are integers from 0 to 1000, relative to image width and height."
)


class VLMAnnotator:
    """Lazy wrapper so the script runs without torch installed."""

    def __init__(self, model_id, max_new_tokens=384):
        from transformers import AutoModelForImageTextToText, AutoProcessor
        import torch

        self.torch = torch
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_id, torch_dtype=torch.float16, device_map="auto"
        )
        self.max_new_tokens = max_new_tokens

    def annotate(self, image, section_title):
        image = image.convert("RGB")
        w, h = image.size
        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": VLM_PROMPT.format(title=section_title)},
            ],
        }]
        prompt = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.processor(text=[prompt], images=[image], return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens, do_sample=False)
        trimmed = out[0][inputs["input_ids"].shape[1]:]
        raw = self.processor.decode(trimmed, skip_special_tokens=True)
        return parse_vlm_json(raw, w, h)


def parse_vlm_json(raw, width, height):
    """Pull the JSON object out of the reply and scale boxes to pixels."""
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        return [], ""
    try:
        data = json.loads(match.group(0))
    except ValueError:
        return [], ""
    regions = []
    for reg in data.get("regions", [])[:5]:
        box = reg.get("bbox") or reg.get("bbox_2d")
        pixels = None
        if isinstance(box, (list, tuple)) and len(box) == 4:
            try:
                vals = [float(v) for v in box]
            except (TypeError, ValueError):
                vals = None
            if vals:
                scale = 1000.0 if max(vals) <= 1000 else max(width, height)
                pixels = [
                    int(vals[0] / scale * width), int(vals[1] / scale * height),
                    int(vals[2] / scale * width), int(vals[3] / scale * height),
                ]
        regions.append({"label": str(reg.get("label", ""))[:60], "bbox": pixels})
    return regions, str(data.get("caption", ""))[:200]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Illustrate lecture notes with annotated frames")
    ap.add_argument("--run-dir", required=True, help="A finished output directory for one lecture")
    ap.add_argument("--notes", default="final_lecture_notes.md", help="Notes file inside run-dir")
    ap.add_argument("--out", default=None, help="Output Markdown path")
    ap.add_argument("--max-figures", type=int, default=6)
    ap.add_argument("--vlm", action="store_true", help="Use a vision model for captions and boxes")
    ap.add_argument("--model", default="Qwen/Qwen2.5-VL-7B-Instruct")
    ap.add_argument("--min-change", type=float, default=MIN_VISUAL_CHANGE)
    ap.add_argument("--no-clean-board", dest="clean_board", action="store_false",
                    help="Use the raw frame instead of removing the lecturer")
    ap.add_argument("--clean-window", type=int, default=31,
                    help="How many neighbouring frames to rebuild the board from")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    notes_path = run_dir / args.notes
    if not notes_path.is_file():
        sys.exit(f"Notes not found: {notes_path}")

    md = notes_path.read_text(encoding="utf-8")
    lines, sections = load_sections(md)
    if not sections:
        sys.exit("No '##' sections found in the notes")

    frames = load_frames(run_dir)
    if not frames:
        sys.exit(f"No frames found under {run_dir / 'ingested' / 'frames'}")

    candidates = select_candidates(frames, args.min_change)
    chosen = match_sections(sections, candidates, args.max_figures)
    if not chosen:
        sys.exit("No frame could be matched to any section")

    print(f"frames on disk    : {len(frames)}")
    print(f"candidate frames  : {len(candidates)}  (duplicates dropped)")
    print(f"figures to produce: {len(chosen)}")

    annotator = None
    if args.vlm:
        print(f"loading {args.model} ...")
        annotator = VLMAnnotator(args.model)

    figures_dir = run_dir / "figures"
    record, inserts = [], {}

    frame_index = {f["path"]: i for i, f in enumerate(frames)}

    for n, pick in enumerate(chosen, start=1):
        cand = candidates[pick["cand"]]
        sec = sections[pick["section"]]
        stamp = mmss(cand["t"])

        if args.clean_board:
            image, board_method = clean_board_image(
                frames, frame_index[cand["path"]], args.clean_window
            )
        else:
            image, board_method = Image.open(cand["path"]).convert("RGB"), "single frame"

        if annotator:
            regions, caption = annotator.annotate(image, sec["title"])
            source = "vlm"
            if not caption:
                regions, caption = keyword_annotation(cand, sec["title"])
                source = "keywords (vlm returned nothing usable)"
        else:
            regions, caption = keyword_annotation(cand, sec["title"])
            source = "keywords"

        out_img = figures_dir / f"fig_{n:02d}_{stamp.replace(':', '')}.jpg"
        draw_annotation(image, out_img, regions, caption, stamp)

        rel = f"figures/{out_img.name}"
        labels = ", ".join(r["label"] for r in regions if r.get("label"))
        block = [
            "",
            f"![Figure {n}]({rel})",
            "",
            f"**Figure {n}.** {caption} Frame at {stamp}." + (f" Highlighted: {labels}." if labels else ""),
            "",
        ]
        inserts.setdefault(sec["end"], []).extend(block)

        record.append({
            "figure": n,
            "image": rel,
            "timestamp_sec": cand["t"],
            "timestamp": stamp,
            "source_frame": cand["path"].name,
            "section": sec["title"],
            "match_score": pick["score"],
            "matched_terms": pick["overlap"],
            "new_keywords_in_frame": cand["new_keywords"],
            "visual_change_from_previous": cand["change"],
            "annotation_source": source,
            "board_reconstruction": board_method,
            "regions": regions,
        })
        print(f"  figure {n}: {stamp}  ->  {sec['title'][:44]}  ({source}, {board_method})")

    out_lines = []
    for i, line in enumerate(lines):
        out_lines.append(line)
        if i + 1 in inserts:
            out_lines.extend(inserts[i + 1])
    if len(lines) in inserts:
        out_lines.extend(inserts[len(lines)])

    out_lines += ["", "---", "", "## Figure Index", ""]
    out_lines += ["| Figure | Time | Section | Source |", "|---|---|---|---|"]
    for r in record:
        out_lines.append(f"| {r['figure']} | {r['timestamp']} | {r['section']} | {r['annotation_source']} |")

    out_path = Path(args.out) if args.out else run_dir / "final_lecture_notes_illustrated.md"
    out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    (figures_dir / "figures.json").write_text(json.dumps(record, indent=2), encoding="utf-8")

    print(f"\nwrote {out_path}")
    print(f"wrote {figures_dir / 'figures.json'}")


if __name__ == "__main__":
    main()
