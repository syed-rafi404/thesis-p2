"""Shared pieces for the annotated-notes pipeline (label_boards.py, build_lecture_notes.py).

Where things live
-----------------
Lecture run folders (transcripts, VLM output, notes):
    output/live_focused/no_gaze/interval_10s/<lecture>   lectures 1-9
    output/speaker3_runs/<lecture>                        lectures 10-13 (Speaker3)
Reconstructed boards (RESULTS.md 4.1.2), newest method first:
    output/annotation_demo/all9_deeplab_shadow/<lecture>/mosaic.json
    output/annotation_demo/speaker3_2s_deeplab_shadow/<lecture>/mosaic.json
    and, for each board, <root>/clean/<lecture>_<board stem>_clean.jpg

The answer key in data/board_truth is never read by anything that generates text; guard()
refuses it, as regenerate_notes.py does.
"""
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
RUN_ROOTS = [REPO / "output" / "live_focused" / "no_gaze" / "interval_10s",
             REPO / "output" / "speaker3_runs"]
BOARD_ROOTS = [REPO / "output" / "annotation_demo" / "all9_deeplab_shadow",
               REPO / "output" / "annotation_demo" / "speaker3_2s_deeplab_shadow"]
FRAME_DIRS = [REPO / "output" / "live_focused" / "no_gaze" / "interval_10s",
              REPO / "output" / "speaker3_runs_2s"]
FORBIDDEN = (REPO / "data" / "board_truth").resolve()

# Distinct colours with the names the notes use for them ("the orange box 3").
COLOURS = [("red", "#d62828"), ("blue", "#1d4ed8"), ("orange", "#f77f00"),
           ("green", "#2a9d4f"), ("purple", "#7b2cbf"), ("pink", "#d63384"),
           ("brown", "#8d5524"), ("teal", "#0e7c86"), ("olive", "#6b7f1a"), ("navy", "#1b2a6b")]


def colour(box_id):
    return COLOURS[(int(box_id) - 1) % len(COLOURS)]


def guard(path):
    """Refuse to read the evaluation answer key."""
    resolved = Path(path).resolve()
    if resolved == FORBIDDEN or FORBIDDEN in resolved.parents:
        sys.exit(f"refusing to read {path}: that is the board-recall answer key")
    return resolved


def secs(stamp):
    parts = [int(p) for p in str(stamp).split(":")]
    total = 0
    for p in parts:
        total = total * 60 + p
    return total


def stamp(seconds):
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def lecture_number(name):
    m = re.match(r"BanglaASR(\d+)", name)
    return int(m.group(1)) if m else 10 ** 6


def discover_lectures(board_roots=None):
    """{lecture name: {"run_dir": Path, "board_dir": Path}} for lectures that have boards."""
    board_roots = [Path(p) for p in (board_roots or BOARD_ROOTS)]
    runs = {}
    for root in RUN_ROOTS:
        if root.exists():
            for d in root.iterdir():
                if d.is_dir():
                    runs.setdefault(d.name, d)
    out = {}
    for root in board_roots:
        if not root.exists():
            continue
        for d in root.iterdir():
            if d.is_dir() and (d / "mosaic.json").exists() and d.name not in out:
                out[d.name] = {"run_dir": runs.get(d.name), "board_dir": d}
    return dict(sorted(out.items(), key=lambda kv: lecture_number(kv[0])))


def board_eras(board_dir):
    """The boards of one lecture in time order, with their clean and occluder images."""
    board_dir = Path(board_dir)
    root = board_dir.parent
    eras = json.loads((board_dir / "mosaic.json").read_text(encoding="utf-8"))
    out = []
    for era in eras:
        image = Path(era["image"])
        image = image if image.is_absolute() else REPO / image
        clean = root / "clean" / f"{board_dir.name}_{image.stem}_clean.jpg"
        occluder = image.with_name(image.stem + "_occluder.png")
        out.append({
            "era": era["era"], "from": era["from"], "to": era["to"],
            "start": secs(era["from"]), "end": secs(era["to"]),
            "stem": image.stem, "mosaic": image,
            "clean": clean if clean.exists() else None,
            "occluder": occluder if occluder.exists() else None,
            "clear_fraction": era.get("clear_fraction"),
        })
    return sorted(out, key=lambda e: e["start"])


def lecture_duration(name, eras):
    """Seconds of lecture, from the extracted frames if present, else from the last board."""
    for root in FRAME_DIRS:
        frames = root / name / "ingested" / "frames"
        if frames.exists():
            files = sorted(frames.glob("*.jpg"))
            if files:
                m = re.search(r"_(\d+)s\.jpg$", files[-1].name)
                if m:
                    return int(m.group(1)) + 10
    return (max(e["end"] for e in eras) + 60) if eras else 0


def boxes_file(run_dir, mock=False):
    return Path(run_dir) / ("board_boxes_MOCK.json" if mock else "board_boxes.json")


def utf8_console():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
