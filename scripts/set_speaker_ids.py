#!/usr/bin/env python
"""
Add "# Speaker ID: X" to ground-truth files that do not have one yet, from the voice check.

The label for each lecture comes from output/speaker_check/speaker_groups.json
(scripts/speaker_groups.py). On 2026-09-22 that check agreed with the user on every video:
1-9 lecturer A, 10-13 B, 14-43 C (new numbering). A file that already has a Speaker ID is left
alone; a lecture the voice check marked unsure (margin under 0.05) or unlike all three lecturers
(best similarity under 0.85) is left alone too and listed, because a person has to decide it.
Only the header line is added; the transcription text is not touched.

    python scripts/set_speaker_ids.py            # show what would change
    python scripts/set_speaker_ids.py --apply
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GT = REPO / "data" / "ground_truth"
VOICE = REPO / "output" / "speaker_check" / "speaker_groups.json"
HEADER = re.compile(r"^\s*#\s*speaker\s*id\s*:\s*(\S+)", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--gt-dir", default=str(GT))
    args = ap.parse_args()
    if not VOICE.exists():
        sys.exit("no voice check yet: run scripts/speaker_groups.py first")
    voice = json.loads(VOICE.read_text(encoding="utf-8"))["lectures"]
    todo, ask = [], []
    for path in sorted(Path(args.gt_dir).glob("*_ground_truth.txt")):
        m = re.search(r"(BanglaASR\d+)_ground_truth\.txt$", path.name)
        if not m:
            continue
        raw = path.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = (raw[3:] if bom else raw).decode("utf-8")
        head = [ln for ln in text.splitlines()[:40] if ln.lstrip().startswith("#")]
        if any(HEADER.match(ln) for ln in head):
            continue
        v = voice.get(m.group(1))
        if not v:
            ask.append(f"{path.name}: not in the voice check (rerun scripts/speaker_groups.py)")
            continue
        if v["margin"] < 0.05 or v["similarity"] < 0.85:
            ask.append(f"{path.name}: voice check unsure (best {v['best']}, similarity "
                       f"{v['similarity']}, margin {v['margin']}); decide by hand")
            continue
        todo.append((path, v["best"], bom, text))
    for path, label, bom, text in todo:
        print(f"{'add' if args.apply else 'would add'}  # Speaker ID: {label}   {path.name}")
        if args.apply:
            nl = "\r\n" if "\r\n" in text else "\n"
            path.write_bytes((b"\xef\xbb\xbf" if bom else b"")
                             + (f"# Speaker ID: {label}{nl}" + text).encode("utf-8"))
    for line in ask:
        print("ASK  " + line)
    if not todo and not ask:
        print("every ground-truth file already has a Speaker ID")
    elif todo and not args.apply:
        print("\nrerun with --apply to write these")
    return 0


if __name__ == "__main__":
    sys.exit(main())
