#!/usr/bin/env python
"""
Does the headline (RESULTS.md 1.5) survive dropping clips built from unreadable timestamps?

prepare_data.py reads a segment boundary only when the timestamp is written exactly like
[1:34-1:53]. In the frozen ground truth behind every published number
(data/ground_truth_v1_2026-09-21) 9 of 156 timestamps are written with stray spaces
("[4:22- 4:45 ]", "[ 08:29 - 09:09]"): 8 in old lecture 13, 1 in old lecture 4. Their text joined
the previous segment, so the clips cut from those segments carry more words than their audio.

This finds those clips in the committed test manifests and recomputes the six headline runs
without them, from the per-clip scores already saved (no model is run). Both models were scored
on the same clips, so the defect adds noise to both sides rather than favouring the fine-tune;
this measures how much it moves the numbers.

    python scripts/check_merged_timestamps.py
"""
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "finetune"))
from prepare_data import LOOKS_LIKE_TS, parse_gt                   # noqa: E402

FROZEN = REPO / "data" / "ground_truth_v1_2026-09-21"
ART = REPO / "artifacts"
RUNS = [("hold out A, s42", "ft_work_BCtoA", "eval_turbo_seed42_greedy.json"),
        ("hold out A, s1", "ft_work_BCtoA", "eval_turbo_seed1_greedy.json"),
        ("hold out B, s42", "ft_work_AC", "eval_AC_turbo_seed42_greedy.json"),
        ("hold out B, s1", "ft_work_AC", "eval_AC_turbo_seed1_greedy.json"),
        ("hold out C, s42", "ft_work_ABtoC", "eval_turbo_seed42_greedy.json"),
        ("hold out C, s1", "ft_work_ABtoC", "eval_turbo_seed1_greedy.json")]


def wilcoxon_p(deltas):
    """Two-sided Wilcoxon signed-rank p, normal approximation with tied ranks (as evaluate.py)."""
    import math
    d = [x for x in deltas if x != 0]
    n = len(d)
    if n == 0:
        return 1.0
    order = sorted(range(n), key=lambda i: abs(d[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(d[order[j + 1]]) == abs(d[order[i]]):
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    w_plus = sum(r for r, x in zip(ranks, d) if x > 0)
    mean = n * (n + 1) / 4
    sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (w_plus - mean) / sd
    return math.erfc(abs(z) / math.sqrt(2))


def affected_segments():
    out = {}
    for path in sorted(FROZEN.glob("*_ground_truth.txt")):
        lecture = path.name.replace("_ground_truth.txt", "")
        for s, e, text in parse_gt(str(path)):
            if LOOKS_LIKE_TS.search(text):
                out.setdefault(lecture, []).append((s, e))
    return out


def main():
    bad_segments = affected_segments()
    print("segments with a merged, unread timestamp:",
          {k: len(v) for k, v in bad_segments.items()})
    rows = []
    for label, folder, name in RUNS:
        data = json.loads((ART / folder / name).read_text(encoding="utf-8"))
        manifest = {}
        for line in (ART / folder / "test.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                manifest[r["audio"]] = r
        bad = set()
        for audio, r in manifest.items():
            for s, e in bad_segments.get(r["lecture"], []):
                if r["start"] >= s - 0.5 and r["end"] <= e + 0.5:
                    bad.add(audio)
        base = {c["audio"]: c for c in data["per_clip"]["base"]}
        tuned = {c["audio"]: c for c in data["per_clip"]["tuned"]}
        keys_all = [a for a in base if a in tuned]
        keys_ok = [a for a in keys_all if a not in bad]
        med = lambda keys, side, m: 100 * statistics.median(side[a][m] for a in keys)
        rows.append({
            "run": label, "clips": len(keys_all), "dropped": len(keys_all) - len(keys_ok),
            "cer_all": (med(keys_all, base, "cer"), med(keys_all, tuned, "cer")),
            "cer_ok": (med(keys_ok, base, "cer"), med(keys_ok, tuned, "cer")),
            "wer_all": (med(keys_all, base, "wer"), med(keys_all, tuned, "wer")),
            "wer_ok": (med(keys_ok, base, "wer"), med(keys_ok, tuned, "wer")),
            "p_ok": wilcoxon_p([tuned[a]["cer"] - base[a]["cer"] for a in keys_ok]),
        })
    print(f"\n{'run':<16} {'clips':>5} {'drop':>4}   {'CER all':>15}   {'CER without':>15}   "
          f"{'WER without':>15}   Wilcoxon p (CER, without)")
    for r in rows:
        print(f"{r['run']:<16} {r['clips']:>5} {r['dropped']:>4}   "
              f"{r['cer_all'][0]:5.1f} -> {r['cer_all'][1]:5.1f}   "
              f"{r['cer_ok'][0]:5.1f} -> {r['cer_ok'][1]:5.1f}   "
              f"{r['wer_ok'][0]:5.1f} -> {r['wer_ok'][1]:5.1f}   {r['p_ok']:.1e}")
    mean = lambda key, i: sum(r[key][i] for r in rows) / len(rows)
    print(f"\nmean of six per-run medians, all clips   : CER {mean('cer_all', 0):.1f}% -> "
          f"{mean('cer_all', 1):.1f}%, WER {mean('wer_all', 0):.1f}% -> {mean('wer_all', 1):.1f}%")
    print(f"mean of six per-run medians, without them: CER {mean('cer_ok', 0):.1f}% -> "
          f"{mean('cer_ok', 1):.1f}%, WER {mean('wer_ok', 0):.1f}% -> {mean('wer_ok', 1):.1f}%")


if __name__ == "__main__":
    main()
