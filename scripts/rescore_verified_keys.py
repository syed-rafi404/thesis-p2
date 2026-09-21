#!/usr/bin/env python
"""
=============================================================================
EVERY BOARD-RECALL RESULT, RESCORED ON THE HAND-VERIFIED ANSWER KEYS
=============================================================================
One command for all of RESULTS.md sections 5.1-5.3 after the 2026-09-22 hand
check of all 45 boards. Nothing is regenerated: the VLM transcriptions and the
notes already on disk are rescored with scripts/score_board_recall.py.

Sets of boards:
    10 boards   lectures 7-9, the original evaluation set (data/board_truth)
    35 boards   lectures 1-9 (adds data/board_truth/draft_lectures1to6)
    Speaker3    lectures 10-13 (data/board_truth/draft_speaker3), VLM only

Usage:
    python scripts/rescore_verified_keys.py
    python scripts/rescore_verified_keys.py --json output/board_recall_verified.json
=============================================================================
"""

import argparse
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sbr", REPO / "scripts" / "score_board_recall.py")
sbr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbr)

RUNS = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
S3_RUNS = REPO / "output" / "speaker3_runs"
KEY10 = [REPO / "data" / "board_truth"]
KEY35 = KEY10 + [REPO / "data" / "board_truth" / "draft_lectures1to6"]
KEYS3 = [REPO / "data" / "board_truth" / "draft_speaker3"]
KINDS = ["number", "name", "code", "term", "phrase"]


def per_board(keys, root, name):
    """Recall per board, in a fixed order, plus totals by kind."""
    truth = sbr.load_truth(keys)
    rows, kinds, found, total = [], {}, 0, 0
    for lecture in sorted(truth):
        path = sbr.find_notes(str(root), lecture, name)
        if path is None:
            raise SystemExit(f"missing {name} for {lecture} under {root}")
        r = sbr.score_notes(Path(path).read_text(encoding="utf-8"), truth[lecture])
        for b in r["boards"]:
            rows.append(b["recall"])
        for k, v in r["by_kind"].items():
            a = kinds.setdefault(k, [0, 0])
            a[0] += v["found"]
            a[1] += v["total"]
        found += r["found"]
        total += r["items"]
    return {"recall": found / total, "found": found, "items": total,
            "boards": rows, "by_kind": kinds}


def paired(a, b):
    diffs = [y - x for x, y in zip(a["boards"], b["boards"])]
    p, pos, neg = sbr.sign_test(diffs)
    return {"better": pos, "worse": neg, "sign_p": p, "wilcoxon_p": sbr.wilcoxon(diffs)}


def main():
    ap = argparse.ArgumentParser(description="Rescore all board-recall results on the verified keys")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    sets = {
        "10 boards (lectures 7-9)": (KEY10, RUNS, ["visual_keywords.json", "board_text_frame.md",
                                                    "board_text_mosaic.md", "final_lecture_notes.md",
                                                    "notes_B_prompt.md", "notes_C_vlm.md", "notes_D_full.md"]),
        "35 boards (lectures 1-9)": (KEY35, RUNS, ["visual_keywords.json", "board_text_frame.md",
                                                   "board_text_mosaic.md", "final_lecture_notes.md",
                                                   "notes_C_vlm.md"]),
        "Speaker3 (lectures 10-13)": (KEYS3, S3_RUNS, ["board_text_frame.md", "board_text_mosaic.md"]),
    }
    pairs = [("visual_keywords.json", "board_text_frame.md"), ("board_text_frame.md", "board_text_mosaic.md"),
             ("final_lecture_notes.md", "notes_B_prompt.md"), ("notes_B_prompt.md", "notes_C_vlm.md"),
             ("notes_C_vlm.md", "notes_D_full.md"), ("final_lecture_notes.md", "notes_C_vlm.md"),
             ("final_lecture_notes.md", "notes_D_full.md")]

    record = {}
    for label, (keys, root, names) in sets.items():
        scores = {n: per_board(keys, root, n) for n in names}
        n_boards = len(next(iter(scores.values()))["boards"])
        n_items = next(iter(scores.values()))["items"]
        print(f"\n=== {label}: {n_boards} boards, {n_items} items")
        print(f"{'source':<26}{'recall':>9}  " + "  ".join(f"{k:>8}" for k in KINDS))
        for n, s in scores.items():
            kinds = "  ".join(f"{'%d/%d' % tuple(s['by_kind'].get(k, (0, 0))):>8}" for k in KINDS)
            print(f"{n:<26}{100 * s['recall']:>8.1f}%  {kinds}")
        comps = {}
        for a, b in pairs:
            if a in scores and b in scores:
                c = paired(scores[a], scores[b])
                comps[f"{a} -> {b}"] = c
                sp = "n/a" if c["sign_p"] is None else f"{c['sign_p']:.2g}"
                wp = "n/a" if c["wilcoxon_p"] is None else f"{c['wilcoxon_p']:.2g}"
                print(f"  {a} -> {b}: better on {c['better']}, worse on {c['worse']}, "
                      f"sign p = {sp}, Wilcoxon p = {wp}")
        record[label] = {"scores": {n: {k: v for k, v in s.items() if k != "boards"}
                                    for n, s in scores.items()}, "paired": comps}

    if args.json:
        Path(args.json).write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
