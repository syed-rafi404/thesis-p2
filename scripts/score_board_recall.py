#!/usr/bin/env python
"""
=============================================================================
BOARD-CONTENT RECALL: DOES WHAT WAS WRITTEN REACH THE NOTES?
=============================================================================
Scores a generated lecture summary on the one thing a language model cannot
fake: the specific facts the lecturer wrote on the whiteboard.

WHY NOT ANY OF THE EXISTING METRICS
-----------------------------------
Qwen knows digital logic, Python and database theory perfectly well without
watching the lecture. The baseline notes for BanglaASR7 print a correct NAND
truth table next to a definition that is plainly wrong, which is what reciting
from memory looks like. Any metric scored on general content therefore measures
the language model's prior knowledge, not the pipeline.

Term F1 is worse than useless here for a separate reason recorded in RESULTS.md
2.1: it is anti-correlated with transcription quality and has an 8 pp
run-to-run noise floor.

What a model cannot invent is that Adiba Noshin has a CGPA of 3.28 and studies
Economics. That exists only on the whiteboard. Scoring recall of those items
measures exactly one thing: whether board content survived the pipeline into
the notes. Measured on the existing baseline for BanglaASR8, 3 of 21 items
survived.

RECALL, NOT F1
--------------
Good notes legitimately contain a great deal that was never on the board, such
as explanation drawn from speech, so precision would punish exactly the
behaviour we want. Hallucination is tracked separately instead: items that look
like board facts but appear nowhere on the board.

GROUND TRUTH FORMAT
-------------------
One JSON file per lecture listing what is written on each board:

    {"lecture": "BanglaASR8",
     "boards": [
       {"era": 2, "image": "...board_era2_110.jpg",
        "items": [
          {"text": "Adiba Noshin", "kind": "name"},
          {"text": "3.28",         "kind": "number"},
          {"text": "Economics",    "kind": "term"},
          {"text": "Varchar(10)",  "kind": "code", "alt": ["varchar (10)"]}
        ]}
     ]}

`kind` is one of name, number, term, code. `alt` lists acceptable spellings;
matching is case-insensitive and whitespace-insensitive, and numbers must match
exactly because a wrong CGPA is worse than a missing one.

Usage:
    python scripts/score_board_recall.py --gt data/board_truth --notes-name final_lecture_notes.md
    python scripts/score_board_recall.py --gt data/board_truth --compare baseline_dir full_dir
=============================================================================
"""

import argparse
import json
import re
import sys
from math import comb
from pathlib import Path

RUNS = "output/live_focused/no_gaze/interval_10s"


def normalise(text):
    """Lowercase, collapse whitespace, drop punctuation that varies by transcriber."""
    text = text.lower()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[\s_]+", " ", text)
    return text.strip()


def contains(haystack, item):
    """Is this board item present in the notes?

    Numbers are matched on a word boundary so that 3.5 does not match 3.55 and
    an ID does not match a substring of a longer number. Everything else is a
    normalised substring test, which tolerates the model rewrapping or
    re-capitalising a phrase.
    """
    candidates = [item["text"]] + list(item.get("alt", []))
    for candidate in candidates:
        needle = normalise(candidate)
        if not needle:
            continue
        if item.get("kind") == "number":
            if re.search(rf"(?<![\d.]){re.escape(needle)}(?![\d.])", haystack):
                return True
        elif needle in haystack:
            return True
    return False


def score_notes(notes_text, boards):
    """Per board and overall recall, broken out by item kind."""
    haystack = normalise(notes_text)
    per_board, totals = [], {}
    for board in boards:
        items = board.get("items", [])
        hits = [it for it in items if contains(haystack, it)]
        misses = [it for it in items if it not in hits]
        by_kind = {}
        for it in items:
            k = it.get("kind", "term")
            slot = by_kind.setdefault(k, [0, 0])
            slot[1] += 1
            if it in hits:
                slot[0] += 1
        for k, (h, n) in by_kind.items():
            agg = totals.setdefault(k, [0, 0])
            agg[0] += h
            agg[1] += n
        per_board.append({
            "era": board.get("era"),
            "items": len(items),
            "found": len(hits),
            "recall": (len(hits) / len(items)) if items else None,
            "by_kind": {k: {"found": v[0], "total": v[1]} for k, v in by_kind.items()},
            "missed": [it["text"] for it in misses],
        })
    total_items = sum(b["items"] for b in per_board)
    total_found = sum(b["found"] for b in per_board)
    return {
        "boards": per_board,
        "items": total_items,
        "found": total_found,
        "recall": (total_found / total_items) if total_items else None,
        "by_kind": {k: {"found": v[0], "total": v[1],
                        "recall": v[0] / v[1] if v[1] else None}
                    for k, v in totals.items()},
    }


def sign_test(diffs):
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    n = pos + neg
    if n == 0:
        return None, pos, neg
    tail = sum(comb(n, k) for k in range(0, min(pos, neg) + 1))
    return min(1.0, 2.0 * tail / float(2 ** n)), pos, neg


def wilcoxon(diffs):
    vals = [d for d in diffs if d != 0]
    n = len(vals)
    if n < 6:
        return None
    order = sorted(range(n), key=lambda i: abs(vals[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(vals[order[j + 1]]) == abs(vals[order[i]]):
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    w_plus = sum(r for r, v in zip(ranks, vals) if v > 0)
    mean = n * (n + 1) / 4.0
    sd = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
    if sd == 0:
        return None
    z = abs(w_plus - mean) / sd
    t = 1.0 / (1.0 + 0.3275911 * (z / 2 ** 0.5))
    erf = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                  - 0.284496736) * t + 0.254829592) * t * pow(2.718281828, -(z ** 2) / 2)
    return min(1.0, 1.0 - erf)


def load_truth(gt_dir):
    out = {}
    for path in sorted(Path(gt_dir).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out[data["lecture"]] = data["boards"]
    return out


def find_notes(root, lecture, name):
    """The notes file for a lecture, under a run directory."""
    direct = Path(root) / lecture / name
    if direct.exists():
        return direct
    hits = list(Path(root).glob(f"*{lecture}*/{name}"))
    return hits[0] if hits else None


def main():
    ap = argparse.ArgumentParser(description="Score board-content recall in generated notes")
    ap.add_argument("--gt", default="data/board_truth", help="Directory of board truth JSON")
    ap.add_argument("--notes-name", default="final_lecture_notes.md")
    ap.add_argument("--runs", default=RUNS, help="Run directory for a single scoring pass")
    ap.add_argument("--compare", nargs=2, metavar=("BASELINE", "FULL"),
                    help="Two run directories to compare, baseline first")
    ap.add_argument("--json", dest="json_out", default="output/board_recall.json")
    args = ap.parse_args()

    truth = load_truth(args.gt)
    if not truth:
        sys.exit(f"no board truth JSON found in {args.gt}")

    def run_over(root, label):
        results, missing = {}, []
        for lecture, boards in truth.items():
            path = find_notes(root, lecture, args.notes_name)
            if not path:
                missing.append(lecture)
                continue
            results[lecture] = score_notes(path.read_text(encoding="utf-8", errors="ignore"),
                                           boards)
        if missing:
            print(f"  [{label}] no notes found for: {', '.join(missing)}")
        return results

    if not args.compare:
        results = run_over(args.runs, "single")
        print(f"{'lecture':<18} {'found':>7} {'items':>7} {'recall':>8}")
        print("-" * 44)
        for lecture, r in sorted(results.items()):
            print(f"{lecture:<18} {r['found']:>7} {r['items']:>7} "
                  f"{(r['recall'] or 0)*100:>7.1f}%")
        items = sum(r["items"] for r in results.values())
        found = sum(r["found"] for r in results.values())
        print("-" * 44)
        print(f"{'TOTAL':<18} {found:>7} {items:>7} {(found/items*100) if items else 0:>7.1f}%")
        payload = {"mode": "single", "root": args.runs, "results": results}
    else:
        base_root, full_root = args.compare
        base = run_over(base_root, "baseline")
        full = run_over(full_root, "full")
        shared = sorted(set(base) & set(full))
        if not shared:
            sys.exit("no lecture has notes in both directories")

        diffs, rows = [], []
        for lecture in shared:
            for b, f in zip(base[lecture]["boards"], full[lecture]["boards"]):
                if b["recall"] is None or f["recall"] is None:
                    continue
                diffs.append(f["recall"] - b["recall"])
                rows.append((lecture, b["era"], b["recall"], f["recall"]))

        print(f"{'lecture':<18} {'era':>4} {'baseline':>9} {'full':>8} {'delta':>8}")
        print("-" * 52)
        for lecture, era, rb, rf in rows:
            print(f"{lecture:<18} {era:>4} {rb*100:>8.1f}% {rf*100:>7.1f}% "
                  f"{(rf-rb)*100:>+7.1f}")
        p_sign, pos, neg = sign_test(diffs)
        base_items = sum(base[l]["items"] for l in shared)
        base_found = sum(base[l]["found"] for l in shared)
        full_found = sum(full[l]["found"] for l in shared)
        print("-" * 52)
        print(f"boards compared          : {len(diffs)}")
        print(f"overall recall, baseline : {base_found}/{base_items} "
              f"({base_found/base_items*100:.1f}%)")
        print(f"overall recall, full     : {full_found}/{base_items} "
              f"({full_found/base_items*100:.1f}%)")
        print(f"full better on           : {pos} boards, worse on {neg}")
        print(f"exact sign test p        : {p_sign}")
        print(f"Wilcoxon signed-rank p   : {wilcoxon(diffs)}")
        payload = {"mode": "compare", "baseline": base_root, "full": full_root,
                   "boards": len(diffs), "sign_p": p_sign, "wilcoxon_p": wilcoxon(diffs),
                   "baseline_results": base, "full_results": full}

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                   encoding="utf-8")
    print(f"\nwrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
