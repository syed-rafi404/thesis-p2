#!/usr/bin/env python
"""
Put several finetune/evaluate.py results side by side: medians, wins, the
direction and p-value of the Wilcoxon test, and runaway clips.

A positive z means the fine-tune is better than the base model; a negative z
means it is worse. The p-value alone does not say which.

Usage:
    python scripts/compare_evals.py LABEL=path/to/eval_x.json LABEL2=path/to/eval_y.json
"""

import json
import sys


def row(label, path):
    d = json.load(open(path, encoding="utf-8"))
    b, t, rt = d["base"], d["tuned"], d["rank_tests"]
    out = [label, d.get("decode", "greedy"), str(b["clips"])]
    for m in ("wer", "cer"):
        out.append(f"{100 * b[m + '_median_per_clip']:.1f} -> {100 * t[m + '_median_per_clip']:.1f}")
        r = rt[m]
        direction = "better" if r["wilcoxon_z"] > 0 else "worse"
        out.append(f"{r['better']}/{r['total']}, {direction}, p = {r['wilcoxon_p']:.1e}")
    out.append(f"{b['runaway_clips']} -> {t['runaway_clips']}")
    return out


def main():
    head = ["run", "decode", "clips", "WER median", "WER: wins, direction, Wilcoxon",
            "CER median", "CER: wins, direction, Wilcoxon", "runaway clips"]
    rows = [row(*arg.split("=", 1)) for arg in sys.argv[1:]]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for r in rows:
        print("| " + " | ".join(r) + " |")


if __name__ == "__main__":
    main()
