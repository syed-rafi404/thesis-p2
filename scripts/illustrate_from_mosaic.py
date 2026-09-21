#!/usr/bin/env python
"""
=============================================================================
PUT THE RECONSTRUCTED BOARDS INTO THE LECTURE NOTES
=============================================================================
The figures in the notes are the era mosaics built by board_mosaic.py, not raw
video frames. The lecturer is absent from them, so the worry that every figure
would have a body in the middle of it does not arise: 26 of the 35 boards across
the 9 lectures are at least 95% clear of the lecturer and 6 are completely clear.

A quality gate enforces that. Any board below --min-clear is left out rather
than printed with a person standing in front of the content. It is better to
show four clean boards than six where two look broken, and the ones that fail
are usually short eras at the very start of a lecture where the board is nearly
empty anyway.

HOW A BOARD IS MATCHED TO A SECTION
-----------------------------------
Both sequences are chronological: the eras run in time order, and the notes
follow the lecture from beginning to end. Each board is therefore placed at the
proportional position in the notes that its era occupies in the lecture, keeping
the order intact.

This is a crude alignment and it is labelled as one. Every figure carries the
time range of the era it came from, so a reader can check the placement against
the video instead of trusting it. A better alignment needs each region read, and
that needs the VLM.

Usage:
    python scripts/illustrate_from_mosaic.py --run-dir <lecture output dir>
    python scripts/illustrate_from_mosaic.py --all
    python scripts/illustrate_from_mosaic.py --all --min-clear 0.9
=============================================================================
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from illustrate_notes import load_sections   # noqa: E402

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
BOARDS = REPO / "output" / "annotation_demo" / "all9"
MIN_CLEAR = 0.95


def pick_boards(mosaic, min_clear):
    """Eras clean enough to show, in time order."""
    return [e for e in mosaic if e.get("clear_fraction", 0) >= min_clear]


def assign(sections, boards):
    """Spread boards across sections proportionally, preserving order.

    Only sections at heading level 2 or 3 are candidates, so a figure does not
    land under a fourth-level sub-point.
    """
    slots = [i for i, s in enumerate(sections) if s["level"] <= 3]
    if not slots or not boards:
        return {}
    out, used = {}, set()
    for n, board in enumerate(boards):
        pos = (n + 0.5) / len(boards)
        want = slots[min(len(slots) - 1, int(pos * len(slots)))]
        while want in used and want + 1 < len(sections):
            want += 1
        used.add(want)
        out[want] = board
    return out


def illustrate(run_dir, boards_dir, min_clear, notes_name, out_name):
    notes = Path(run_dir) / notes_name
    mosaic_json = Path(boards_dir) / "mosaic.json"
    if not notes.exists():
        return None, f"no {notes_name}"
    if not mosaic_json.exists():
        return None, "no mosaic.json; run board_mosaic.py first"

    mosaic = json.loads(mosaic_json.read_text(encoding="utf-8"))
    usable = pick_boards(mosaic, min_clear)
    dropped = len(mosaic) - len(usable)
    if not usable:
        return None, f"no board is at least {min_clear*100:.0f}% clear"

    lines, sections = load_sections(notes.read_text(encoding="utf-8", errors="ignore"))
    placement = assign(sections, usable)

    fig_dir = Path(run_dir) / "figures_board"
    fig_dir.mkdir(parents=True, exist_ok=True)

    inserts, manifest = {}, []
    for n, (idx, board) in enumerate(sorted(placement.items()), 1):
        src = REPO / board["image"] if not Path(board["image"]).is_absolute() else Path(board["image"])
        if not src.exists():
            continue
        dest = fig_dir / f"board_{n:02d}_era{board['era']}.jpg"
        shutil.copyfile(src, dest)
        clear = board["clear_fraction"] * 100
        caption = (f"**Figure {n}.** Whiteboard as it stood during "
                   f"{board['from']}&ndash;{board['to']}, reconstructed from "
                   f"{board['distinct_frames_used']} video frames with the lecturer "
                   f"removed. {clear:.1f}% of the board is unobstructed.")
        inserts.setdefault(sections[idx]["end"], []).append(
            f"\n![Board {board['from']}-{board['to']}]({dest.relative_to(Path(run_dir)).as_posix()})\n\n"
            f"{caption}\n"
        )
        manifest.append({"figure": n, "era": board["era"], "from": board["from"],
                         "to": board["to"], "clear_fraction": board["clear_fraction"],
                         "section": sections[idx]["title"],
                         "image": str(dest.relative_to(Path(run_dir)).as_posix())})

    out_lines = []
    for i, line in enumerate(lines):
        out_lines.append(line)
        for block in inserts.get(i + 1, []):
            out_lines.append(block)

    if manifest:
        out_lines.append("\n---\n")
        out_lines.append(
            "*Figures are reconstructed whiteboards. Each is assembled from tiles taken "
            "from moments when the lecturer was not standing in front of that part of the "
            "board, so every pixel is unmodified video; nothing is generated. A figure "
            "shows the board's state across the time range given, not a single instant. "
            f"Boards less than {min_clear*100:.0f}% clear of the lecturer were left out"
            + (f" ({dropped} of {len(mosaic)} here)." if dropped else ".") + "*\n")

    out_path = Path(run_dir) / out_name
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    (fig_dir / "figures.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return (len(manifest), dropped, len(mosaic), out_path), None


def main():
    ap = argparse.ArgumentParser(description="Insert reconstructed boards into lecture notes")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--boards-dir", default=None,
                    help="Where board_mosaic.py wrote this lecture's boards")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--min-clear", type=float, default=MIN_CLEAR,
                    help="Skip boards less clear than this (0-1)")
    ap.add_argument("--notes-name", default="final_lecture_notes.md")
    ap.add_argument("--out-name", default="final_lecture_notes_boards.md")
    args = ap.parse_args()

    if args.all:
        jobs = [(d, BOARDS / d.name) for d in sorted(RUNS.iterdir()) if d.is_dir()]
    elif args.run_dir:
        run = Path(args.run_dir)
        jobs = [(run, Path(args.boards_dir) if args.boards_dir else BOARDS / run.name)]
    else:
        sys.exit("pass --run-dir <dir> or --all")

    total_figs = 0
    for run_dir, boards_dir in jobs:
        result, problem = illustrate(run_dir, boards_dir, args.min_clear,
                                     args.notes_name, args.out_name)
        if problem:
            print(f"{run_dir.name:<18} skipped: {problem}")
            continue
        figs, dropped, total, out_path = result
        total_figs += figs
        print(f"{run_dir.name:<18} {figs} figures placed, "
              f"{dropped} of {total} boards below the gate")
        print(f"                   {out_path}")
    print(f"\n{total_figs} figures across {len(jobs)} lectures, "
          f"gate at {args.min_clear*100:.0f}% clear")
    return 0


if __name__ == "__main__":
    sys.exit(main())
