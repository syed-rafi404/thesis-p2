#!/usr/bin/env python
"""
=============================================================================
THE PROMPT WAS CHOSEN ON THE SAME BOARDS THE HEADLINE REPORTS. THIS SPLITS THEM.
=============================================================================
RESULTS.md 5.0 reports that changing the prompt from keywords to full
transcription takes board-content recall from 31.2% to 88.8%. That comparison
was scored on all 35 boards of lectures 1-9 - the same boards the headline
number is reported on. The effect is very large, so selection is unlikely to
explain it, but "unlikely" is not "measured".

This splits the boards into a dev half and a test half, so the choice can be
made on one and reported on the other.

THE SPLIT RULE, fixed before looking at any per-half number:

    dev  = odd-numbered lectures  (1, 3, 5, 7, 9)
    test = even-numbered lectures (2, 4, 6, 8)

Split by lecture, not by board: boards inside one lecture share a lecturer, a
topic, a camera and a whiteboard, so putting some of a lecture's boards in each
half would leak. Odd/even is the simplest deterministic rule that does that;
it was not chosen from among several candidates, and no other split was tried.

Honest limit: this is a split applied after the original comparison was run,
not a protocol registered before it. It cannot undo the original selection. It
answers a narrower question - does the prompt still win on boards that played
no part in choosing it - and that is what it is reported as.

Usage:
    python scripts/prompt_selection_split.py
    python scripts/prompt_selection_split.py --json output/prompt_split.json
=============================================================================
"""

import argparse
import json
import re
import subprocess
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_common as nc                                          # noqa: E402

DEV_IS_ODD = True          # dev = odd lecture numbers
KEYWORD = "visual_keywords.json"
TRANSCRIPTION = "board_text_frame.md"


def sign_test(better, worse):
    """Two-sided exact sign test over the boards that changed."""
    n = better + worse
    if n == 0:
        return 1.0
    tail = sum(comb(n, k) for k in range(0, min(better, worse) + 1))
    return min(1.0, 2 * tail / 2 ** n)


def run_comparison(out_json):
    """Score keyword vs transcription over lectures 1-9 and return the raw per-board result."""
    cmd = [sys.executable, str(nc.REPO / "scripts" / "score_board_recall.py"),
           "--gt", "data/board_truth", "data/board_truth/draft_lectures1to6",
           "--compare-names", KEYWORD, TRANSCRIPTION,
           "--json", str(out_json)]
    subprocess.run(cmd, cwd=nc.REPO, check=True, capture_output=True)
    return json.loads(Path(out_json).read_text(encoding="utf-8"))


def halves(result):
    """Split the per-board scores into dev and test by lecture number."""
    keyword, full = result["baseline_results"], result["full_results"]
    out = {"dev": [], "test": []}
    for lecture in sorted(keyword):
        n = nc.lecture_number(lecture)
        half = "dev" if (n % 2 == 1) == DEV_IS_ODD else "test"
        for b0, b1 in zip(keyword[lecture]["boards"], full[lecture]["boards"]):
            out[half].append({
                "lecture": lecture, "era": b0["era"], "items": b0["items"],
                "keyword_found": b0["found"], "transcription_found": b1["found"],
            })
    return out


def summarise(boards):
    items = sum(b["items"] for b in boards)
    kw = sum(b["keyword_found"] for b in boards)
    tr = sum(b["transcription_found"] for b in boards)
    better = sum(1 for b in boards if b["transcription_found"] > b["keyword_found"])
    worse = sum(1 for b in boards if b["transcription_found"] < b["keyword_found"])
    return {
        "boards": len(boards), "items": items,
        "keyword": kw, "keyword_recall": kw / items if items else 0,
        "transcription": tr, "transcription_recall": tr / items if items else 0,
        "better": better, "worse": worse, "ties": len(boards) - better - worse,
        "sign_p": sign_test(better, worse),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="output/prompt_split.json")
    args = ap.parse_args()

    tmp = Path(args.json).with_suffix(".raw.json")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    result = run_comparison(tmp)
    split = halves(result)
    report = {"rule": "dev = odd-numbered lectures, test = even-numbered lectures",
              "keyword_file": KEYWORD, "transcription_file": TRANSCRIPTION,
              "dev": summarise(split["dev"]), "test": summarise(split["test"]),
              "all": summarise(split["dev"] + split["test"])}

    print("=" * 70)
    print("  PROMPT CHOICE: CHOSEN ON DEV, REPORTED ON TEST")
    print("=" * 70)
    print(f"  rule: {report['rule']}")
    print(f"\n{'half':<6}{'boards':>7}{'items':>7}{'keyword':>10}{'transcription':>15}"
          f"{'better/worse':>14}{'sign p':>9}")
    for half in ("dev", "test", "all"):
        s = report[half]
        print(f"{half:<6}{s['boards']:>7}{s['items']:>7}{s['keyword_recall']:>9.1%}"
              f"{s['transcription_recall']:>15.1%}{s['better']:>8}/{s['worse']:<5}"
              f"{s['sign_p']:>9.4f}")

    dev, test = report["dev"], report["test"]
    winner = "full transcription" if dev["transcription_recall"] > dev["keyword_recall"] else "keywords"
    print(f"\n  Chosen on dev: {winner}.")
    print(f"  Reported on test, which played no part in that choice: "
          f"{test['keyword_recall']:.1%} -> {test['transcription_recall']:.1%}, "
          f"better on {test['better']} boards, worse on {test['worse']}, "
          f"sign p = {test['sign_p']:.4f}.")

    Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
