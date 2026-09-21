#!/usr/bin/env python
"""
=============================================================================
PUT THE BOARD PICTURES INTO NOTES THAT ALREADY EXIST, WITHOUT THE LLM
=============================================================================
regenerate_notes.py asks the model to mark where each board belongs with
[[FIGURE n]] and then swaps the marker for the picture. Its first version only
recognised a marker standing alone on its line, so when the model wrote
"[[FIGURE 1]] board during 1:10-10:50:" the picture was dropped and the raw
marker stayed in the notes. This fixes notes already on disk: every leftover
marker becomes the picture and its caption, exactly as regenerate_notes.py now
does. Any text the model wrote after a marker is kept (only a leading
"board during m:ss-m:ss:" label goes), so board recall must not change; check
with scripts/rescore_verified_keys.py.

It also copies the board pictures beside the notes (figures_board/), so the
notes display on a machine that did not generate them.

Usage:
    python scripts/place_note_figures.py --all
    python scripts/place_note_figures.py --run-dir <lecture folder> --notes-name notes_C_vlm.md
=============================================================================
"""

import argparse
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("regen", REPO / "scripts" / "regenerate_notes.py")
regen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regen)

NOTES = ("notes_B_prompt.md", "notes_C_vlm.md", "notes_D_full.md")


def fix(run_dir, name):
    path = run_dir / name
    if not path.exists():
        return None
    figures = regen.load_figures(run_dir, regen.BOARDS / run_dir.name, regen.MIN_CLEAR, {})
    by_n = {f["n"]: f for f in figures}
    text = path.read_text(encoding="utf-8")
    out, placed, dropped = [], 0, 0
    for line in text.splitlines():
        m = regen.FIGURE_MARK.match(line)
        if not m:
            out.append(line)
            continue
        fig = by_n.get(regen.marker_number(m))
        rest = regen.marker_rest(m)            # never lose text written after a marker
        if not fig or f"({fig['image']})" in text:
            dropped += 1                       # unknown, or already shown elsewhere
            if rest:
                out.append(rest)
            continue
        out += [f"![Board {fig['from']}-{fig['to']}]({fig['image']})", "",
                f"*Figure {fig['n']}. The whiteboard during {fig['from']}–{fig['to']}, "
                f"reconstructed from {fig['frames']} video frames with the lecturer "
                f"removed; {fig['clear'] * 100:.0f}% of the board is unobstructed.*"]
        if rest:
            out += ["", rest]
        text += f"({fig['image']})"            # so a repeated marker is not placed twice
        placed += 1
    if placed or dropped:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return placed, dropped, len(figures)


def main():
    ap = argparse.ArgumentParser(description="Place board pictures into existing notes")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--notes-name", nargs="+", default=list(NOTES))
    args = ap.parse_args()
    runs = sorted(d for d in regen.RUNS.iterdir() if d.is_dir()) if args.all else [Path(args.run_dir)]
    for run_dir in runs:
        for name in args.notes_name:
            r = fix(run_dir, name)
            if r and (r[0] or r[1]):
                print(f"{run_dir.name:<16} {name:<20} placed {r[0]}, dropped {r[1]} "
                      f"({r[2]} boards available)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
