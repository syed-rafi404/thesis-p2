"""Side-by-side sheets for two sets of reconstructed boards, plus the second set cleaned.

Columns: (1) boards from --old, (2) boards from --new, (3) --new after clean_board.py with its
occluder mask (needs board_mosaic.py --save-occluder). The cleaned boards are also written to
<new>/clean/. Boards are matched by lecture folder and file name.

    python scripts/compare_board_sets.py --old output/annotation_demo/all9 \
        --new output/annotation_demo/all9_deeplab_shadow --per-sheet 6
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clean_board as cb  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--per-sheet", type=int, default=6)
    ap.add_argument("--width", type=int, default=480)
    args = ap.parse_args()

    old, new = Path(args.old), Path(args.new)
    out = new / "clean"
    out.mkdir(parents=True, exist_ok=True)
    boards = sorted(p for p in new.glob("*/board_era*.jpg") if (old / p.parent.name / p.name).exists())
    W = args.width
    H = W * 9 // 16
    labels = ("old", "new", "new + clean-up")
    sheets = []
    for start in range(0, len(boards), args.per_sheet):
        chunk = boards[start:start + args.per_sheet]
        sheet = Image.new("RGB", (3 * W + 40, len(chunk) * (H + 30) + 10), "white")
        draw = ImageDraw.Draw(sheet)
        for k, p in enumerate(chunk):
            img = Image.open(p).convert("RGB")
            occ_path = p.with_name(p.stem + "_occluder.png")
            occ = Image.open(occ_path).convert("L") if occ_path.exists() else None
            cleaned, _ = cb.clean(img, occluder=occ)
            cleaned.save(out / f"{p.parent.name}_{p.stem}_clean.jpg", quality=92)
            y = 10 + k * (H + 30)
            draw.text((10, y), f"{p.parent.name} {p.stem}   columns: " + " | ".join(labels), fill="black")
            before = Image.open(old / p.parent.name / p.name).convert("RGB")
            for c, im in enumerate((before, img, cleaned)):
                sheet.paste(im.resize((W, H)), (10 + c * (W + 10), y + 16))
        path = new / f"compare_{start // args.per_sheet + 1}.jpg"
        sheet.save(path, quality=85)
        sheets.append(path)
    print(f"{len(boards)} boards, {len(sheets)} sheets:")
    for s in sheets:
        print(f"  {s}")


if __name__ == "__main__":
    main()
