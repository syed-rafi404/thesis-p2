"""Redraw one board's labelled figure from the box records already on disk.

label_boards.py normally draws this straight after the vision model answers. When the
drawn file is missing or was left behind by a --mock run, the figure can still be rebuilt
exactly, because board_boxes.json holds the box rectangles, the colours and the names and
text the model returned. Nothing is invented and no GPU is needed.

The script refuses to run on a record whose "mock" flag is true, so a stand-in model's
output cannot be redrawn and mistaken for the real thing.

    python scripts/redraw_board_figure.py ^
      --boxes output/live_focused/no_gaze/interval_10s/BanglaASR7_004/board_boxes.json ^
      --era 5 --out "Thesis Defense P3/drafts/thesis/images/xnor-boxes.jpg"
"""
import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
sys.path.insert(0, str(REPO / "scripts"))

from PIL import Image                                              # noqa: E402
from label_boards import draw_boxes                                # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boxes", required=True, help="a board_boxes.json")
    ap.add_argument("--era", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--source", default=None,
                    help="override the board image the record points at")
    ap.add_argument("--no-names", action="store_true",
                    help="numbers only, which is what the model is shown")
    args = ap.parse_args()

    rec = json.loads(Path(args.boxes).read_text(encoding="utf-8"))
    if rec.get("mock"):
        sys.exit("this record came from a --mock run; its names are not model output")
    boards = [b for b in rec["boards"] if b["era"] == args.era]
    if not boards:
        sys.exit("no era %d in %s" % (args.era, args.boxes))
    board = boards[0]

    src = Path(args.source) if args.source else REPO / board["source_image"]
    if not src.exists():
        sys.exit("board image not found: %s" % src)

    img = Image.open(src)
    out = draw_boxes(img, board["boxes"], with_names=not args.no_names)
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=92)

    print("lecture %s, era %d, %s to %s" % (rec["lecture"], board["era"],
                                            board["from"], board["to"]))
    print("model   %s (mock=%s)" % (rec.get("model"), rec.get("mock")))
    print("source  %s  %dx%d" % (src, img.width, img.height))
    print("wrote   %s" % dest)
    for b in board["boxes"]:
        first = (b.get("text") or "").splitlines()[:1]
        print("  %d %-7s %-14s %s" % (b["id"], b["colour"], b["name"],
                                      first[0][:58] if first else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
