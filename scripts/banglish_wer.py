#!/usr/bin/env python
"""
=============================================================================
SPELLING-FAIR WORD ERROR RATE FOR BANGLISH
=============================================================================
Banglish has no standard spelling. When the reference says "ami" and the model
writes "aami", plain WER counts a whole wrong word although the model heard the
word correctly. This rescoring removes that one unfairness and nothing else.

It re-reads the per-clip reference and hypothesis that finetune/evaluate.py
already saved, so nothing is decoded again and no GPU is needed. The base and
the fine-tuned model are rescored with identical rules.

THE RULES (fixed before any number was computed with them)
----------------------------------------------------------
Both reference and hypothesis, after the normalize_banglish() already applied
by evaluate.py:

1. Spelling table. Every variant listed in TRANSCRIPTION_GUIDE.md section 4.1
   is mapped to its canonical form, using the CANONICAL table that
   scripts/validate_ground_truth.py already enforces ("aami" -> "ami",
   "seta" -> "sheta", "gulo" -> "gula" ...). That table was written for the
   transcribers, before these evaluations.
2. Vowel length. A run of the same vowel is collapsed to one ("aamar" ->
   "amar"), the amar/aamar merge that finetune/prepare_data.py already names
   as COLLAPSE_VOWELS.

nWER  = WER after rules 1 and 2.
fWER  = fuzzy WER on the same text: a word counts as correct when its
        character similarity to the reference word, 1 - edit distance / longer
        length, is at least 0.8. Words of three letters or fewer therefore
        must match exactly, so "na" never matches "ta".

Plain WER and CER stay the headline metrics; these are reported beside them.

Usage:
    python scripts/banglish_wer.py LABEL=path/to/eval_x.json [LABEL2=...]
    python scripts/banglish_wer.py --mean LABEL=... LABEL=...   # also average the runs
=============================================================================
"""

import argparse
import importlib.util
import io
import contextlib
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FUZZY_THRESHOLD = 0.8
VOWEL_RUN = re.compile(r"([aeiou])\1+")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


CANONICAL = _load(REPO / "scripts" / "validate_ground_truth.py", "vgt").CANONICAL
_ev = _load(REPO / "finetune" / "evaluate.py", "ev")
edit_distance, wilcoxon_signed_rank, sign_test = (
    _ev.edit_distance, _ev.wilcoxon_signed_rank, _ev.sign_test)


def spelling_fair(text):
    """Rules 1 and 2, applied word by word."""
    words = []
    for w in text.split():
        w = CANONICAL.get(w, w)
        w = VOWEL_RUN.sub(r"\1", w)
        w = CANONICAL.get(w, w)
        words.append(w)
    return words


def similar(a, b):
    if a == b:
        return True
    longest = max(len(a), len(b))
    return longest > 0 and 1 - edit_distance(list(a), list(b)) / longest >= FUZZY_THRESHOLD


def fuzzy_edit_distance(ref, hyp):
    """Word-level edit distance where a near-identical spelling is a match."""
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (0 if similar(r, h) else 1))
        prev = cur
    return prev[-1]


def clip_scores(ref_text, hyp_text):
    ref, hyp = spelling_fair(ref_text), spelling_fair(hyp_text)
    if not ref:
        return 0.0, 0.0
    return edit_distance(ref, hyp) / len(ref), fuzzy_edit_distance(ref, hyp) / len(ref)


def score_run(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    base, tuned = d["per_clip"]["base"], d["per_clip"]["tuned"]
    out = {"decode": d.get("decode", "greedy"), "clips": len(base)}
    per = {"wer": ([c["wer"] for c in base], [c["wer"] for c in tuned])}
    b_n, b_f = zip(*(clip_scores(c["reference"], c["hypothesis"]) for c in base))
    t_n, t_f = zip(*(clip_scores(c["reference"], c["hypothesis"]) for c in tuned))
    per["nwer"], per["fwer"] = (list(b_n), list(t_n)), (list(b_f), list(t_f))
    for key, (b, t) in per.items():
        deltas = [x - y for x, y in zip(b, t)]            # positive = fine-tune better
        p, n, z = wilcoxon_signed_rank(deltas)
        better = sum(1 for x in deltas if x > 0)
        out[key] = {"base": statistics.median(b), "tuned": statistics.median(t),
                    "better": better, "wilcoxon_p": p, "wilcoxon_z": z,
                    "sign_p": sign_test(better, n)}
    return out


def main():
    ap = argparse.ArgumentParser(description="Spelling-fair WER for Banglish evaluations")
    ap.add_argument("runs", nargs="+", help="LABEL=path/to/eval_*.json")
    ap.add_argument("--mean", action="store_true",
                    help="Also print the unweighted mean of the per-run medians")
    ap.add_argument("--json", default=None, help="Write every number to this file")
    args = ap.parse_args()

    rows, record = [], {}
    for arg in args.runs:
        label, path = arg.split("=", 1)
        r = score_run(path)
        record[label] = r
        cells = [label, r["decode"], str(r["clips"])]
        for key in ("wer", "nwer", "fwer"):
            s = r[key]
            direction = "better" if (s["wilcoxon_z"] or 0) > 0 else "worse"
            cells.append(f"{100 * s['base']:.1f} -> {100 * s['tuned']:.1f} "
                         f"({s['better']}/{r['clips']}, {direction}, p = {s['wilcoxon_p']:.1e})")
        rows.append(cells)

    head = ["run", "decode", "clips", "plain WER median", "spelling-fair nWER median",
            "fuzzy fWER median"]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for cells in rows:
        print("| " + " | ".join(cells) + " |")

    if args.mean:
        print()
        for key, name in (("wer", "plain WER"), ("nwer", "spelling-fair nWER"),
                          ("fwer", "fuzzy fWER")):
            b = statistics.mean(r[key]["base"] for r in record.values())
            t = statistics.mean(r[key]["tuned"] for r in record.values())
            print(f"mean of {len(record)} per-run medians, {name}: {100 * b:.1f}% -> {100 * t:.1f}%")

    if args.json:
        Path(args.json).write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    sys.exit(main())
