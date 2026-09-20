#!/usr/bin/env python
"""
=============================================================================
FUSION STATISTICS - COMPUTED, NOT ASSUMED
=============================================================================
Regenerates every ASR number the thesis reports, from the transcripts saved in
`output/live_focused/no_gaze/`, using the same term functions that produced the
73.9% headline (`scripts/evaluate_ground_truth.py`).

It exists because `scripts/generate_thesis_figures.py` hard-codes a p-value of
0.003, an effect size of 0.96 and a 5.7 point improvement, and no statistical
test existed anywhere in the repository. This script computes the real values.

What it reports:

  * Term recall / precision / F1 for the plain Whisper baseline and for the
    fused transcript, per video and averaged.
  * Word and character error rate for both, so the trade-off is visible.
  * The paired difference between them, with an exact sign-flip permutation
    test and an exact Wilcoxon signed-rank test (n = 9, so both are exact).
  * Cohen's d for paired samples, reported with the caveat that n = 9.
  * A check of whether the frame-interval runs are independent measurements.

No GPU, no models, no third-party statistics package.

Usage:
    python scripts/compute_fusion_stats.py
    python scripts/compute_fusion_stats.py --interval 20s

Outputs:
    output/fusion_statistics.json
    output/fusion_statistics.md
=============================================================================
"""

import argparse
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
import re
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUTPUT_BASE = REPO / "output" / "live_focused" / "no_gaze"
GT_DIR = REPO / "data" / "ground_truth"


# --------------------------------------------------------------------------- setup
def load_reference_metric():
    """Import the scoring functions behind the reported numbers, unchanged."""
    try:
        import rich  # noqa: F401
        stub_needed = False
    except ImportError:
        stub_needed = True
    for name in ("rich", "rich.console", "rich.table", "rich.panel",
                 "rich.progress", "rich.box", "rich.markdown"):
        if stub_needed and name not in sys.modules:
            stub = types.ModuleType(name)
            stub.__getattr__ = lambda _n: type(
                "_Any", (), {"__init__": lambda s, *a, **k: None,
                             "__getattr__": lambda s, n: (lambda *a, **k: None)}
            )
            sys.modules[name] = stub
    spec = importlib.util.spec_from_file_location(
        "egt", REPO / "scripts" / "evaluate_ground_truth.py"
    )
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- metrics
def edit_distance(ref, hyp):
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1]


def wer(ref, hyp, egt):
    r = egt.normalize_text(ref).split()
    return edit_distance(r, egt.normalize_text(hyp).split()) / len(r) if r else 0.0


try:
    import jiwer as _jiwer
except ImportError:
    _jiwer = None


def cer(ref, hyp, egt):
    """Character error rate.

    Full-transcript character alignment is O(n*m) and these transcripts run to
    tens of thousands of characters, so use jiwer when it is installed and
    report nothing rather than stalling when it is not.
    """
    r, h = egt.normalize_text(ref), egt.normalize_text(hyp)
    if not r:
        return 0.0
    if _jiwer is not None:
        return float(_jiwer.cer(r, h))
    return None


def exact_permutation_p(deltas):
    """Two-sided paired sign-flip test on the mean difference."""
    deltas = [d for d in deltas if abs(d) > 1e-12]
    n = len(deltas)
    if n == 0:
        return 1.0, 0
    observed = abs(sum(deltas))
    hits = sum(
        1 for signs in itertools.product((1, -1), repeat=n)
        if abs(sum(s * d for s, d in zip(signs, deltas))) >= observed - 1e-12
    )
    return hits / 2 ** n, n


def exact_wilcoxon_p(deltas):
    """Exact two-sided Wilcoxon signed-rank test."""
    nz = [d for d in deltas if abs(d) > 1e-12]
    n = len(nz)
    if n == 0:
        return 1.0, None, 0
    order = sorted(range(n), key=lambda i: abs(nz[i]))
    rank = {idx: r for r, idx in enumerate(order, 1)}
    w_plus = sum(rank[i] for i in range(n) if nz[i] > 0)
    total = n * (n + 1) / 2
    stat = min(w_plus, total - w_plus)
    dist = [
        sum(r for r, take in zip(range(1, n + 1), signs) if take)
        for signs in itertools.product((0, 1), repeat=n)
    ]
    p = sum(1 for x in dist if min(x, total - x) <= stat) / len(dist)
    return p, w_plus, n


def cohens_d_paired(deltas):
    n = len(deltas)
    if n < 2:
        return 0.0
    mean = sum(deltas) / n
    var = sum((d - mean) ** 2 for d in deltas) / (n - 1)
    sd = var ** 0.5
    return mean / sd if sd else 0.0


# --------------------------------------------------------------------------- data
def read(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def collect(interval, egt):
    base_dir = OUTPUT_BASE / f"interval_{interval}"
    if not base_dir.is_dir():
        sys.exit(f"no such directory: {base_dir}")

    rows = []
    for video_dir in sorted(p for p in base_dir.iterdir() if p.is_dir()):
        name = video_dir.name
        gt = egt.load_ground_truth(name)
        baseline = read(video_dir / "transcript_whisper_baseline.txt")
        fused = read(video_dir / "transcript_fused.txt")
        if not gt or not baseline or not fused:
            print(f"  ! skipping {name}: missing ground truth or transcripts")
            continue

        gt_terms = egt.extract_technical_terms(gt)
        row = {"video": name}
        for label, text in (("baseline", baseline), ("fused", fused)):
            terms = egt.compute_term_metrics(gt_terms, egt.extract_technical_terms(text))
            row[label] = {
                "term_recall": terms["recall"],
                "term_precision": terms["precision"],
                "term_f1": terms["f1"],
                "gt_terms": terms["gt_terms"],
                "asr_terms": terms["asr_terms"],
                "wer": wer(gt, text, egt),
                "cer": cer(gt, text, egt),
                "words": len(text.split()),
            }
        row["gt_words"] = len(gt.split())
        rows.append(row)
    return rows


def check_interval_independence():
    """Are the three frame-interval runs independent measurements of the ASR?"""
    findings = {}
    intervals = sorted(p.name for p in OUTPUT_BASE.iterdir() if p.is_dir())
    for video in sorted({d.name for i in intervals for d in (OUTPUT_BASE / i).iterdir() if d.is_dir()}):
        digests = {}
        for interval in intervals:
            path = OUTPUT_BASE / interval / video / "transcript_fused.txt"
            if path.is_file():
                digests[interval] = hashlib.md5(path.read_bytes()).hexdigest()
        if len(digests) > 1:
            findings[video] = {
                "identical_across_intervals": len(set(digests.values())) == 1,
                "digests": digests,
            }
    return findings


# --------------------------------------------------------------------------- report
def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else float('nan')


def build_report(rows, interval, independence):
    metrics = ("term_recall", "term_precision", "term_f1", "wer", "cer")
    averages = {
        label: {m: mean([r[label][m] for r in rows]) for m in metrics}
        for label in ("baseline", "fused")
    }
    for label in averages:
        for m in list(averages[label]):
            if averages[label][m] is None:
                averages[label][m] = float('nan')
    deltas = [r["fused"]["term_f1"] - r["baseline"]["term_f1"] for r in rows]
    perm_p, perm_n = exact_permutation_p(deltas)
    wil_p, w_plus, wil_n = exact_wilcoxon_p(deltas)

    identical = sum(1 for v in independence.values() if v["identical_across_intervals"])

    summary = {
        "interval": interval,
        "videos": len(rows),
        "averages": averages,
        "term_f1_delta_mean_pp": mean(deltas) * 100,
        "term_f1_delta_per_video_pp": [d * 100 for d in deltas],
        "permutation_test": {"p_value": perm_p, "n": perm_n, "method": "exact two-sided sign-flip"},
        "wilcoxon": {"p_value": wil_p, "w_plus": w_plus, "n": wil_n, "method": "exact two-sided signed-rank"},
        "cohens_d_paired": cohens_d_paired(deltas),
        "independence": {
            "videos_checked": len(independence),
            "identical_fused_transcript_across_intervals": identical,
        },
    }

    pct = lambda v: f"{v * 100:.1f}%"
    lines = [
        "# Fusion statistics, computed from saved transcripts",
        "",
        f"Source: `output/live_focused/no_gaze/interval_{interval}/`, {len(rows)} videos.",
        "Scoring functions imported unchanged from `scripts/evaluate_ground_truth.py`.",
        "",
        "## Baseline Whisper vs fused transcript",
        "",
        "| Metric | Whisper baseline | Fused | Difference |",
        "|---|---|---|---|",
    ]
    for m, nice in (("term_recall", "Term recall"), ("term_precision", "Term precision"),
                    ("term_f1", "Term F1"), ("wer", "Word error rate"), ("cer", "Character error rate")):
        b, f = averages["baseline"][m], averages["fused"][m]
        lines.append(f"| {nice} | {pct(b)} | {pct(f)} | {(f - b) * 100:+.1f} points |")

    lines += [
        "",
        "## Is the Term F1 difference significant?",
        "",
        f"- Mean difference: **{mean(deltas) * 100:+.2f} percentage points** in favour of fusion.",
        f"- Exact paired sign-flip permutation test: **p = {perm_p:.3f}** (n = {perm_n}).",
        f"- Exact Wilcoxon signed-rank test: **p = {wil_p:.3f}** (n = {wil_n}).",
        f"- Paired Cohen's d: **{cohens_d_paired(deltas):.2f}**, on n = {len(deltas)}, which is too small for a stable effect size.",
        "",
        "Per-video differences in percentage points: "
        + ", ".join(f"{d * 100:+.1f}" for d in deltas) + ".",
        "",
        "## Sample size",
        "",
        f"Videos with a fused transcript identical across all frame intervals: "
        f"**{identical} of {len(independence)}**.",
        "",
        "The frame interval changes the visual and summarisation branch, not the transcript",
        "being scored. The interval runs are therefore not independent measurements of ASR",
        "quality, and the effective sample size is the number of videos, not the number of runs.",
        "",
        "## Per video",
        "",
        "| Video | F1 base | F1 fused | Delta | WER base | WER fused |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['video']} | {pct(r['baseline']['term_f1'])} | {pct(r['fused']['term_f1'])} "
            f"| {(r['fused']['term_f1'] - r['baseline']['term_f1']) * 100:+.1f} "
            f"| {pct(r['baseline']['wer'])} | {pct(r['fused']['wer'])} |"
        )
    lines.append("")
    return summary, "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Compute the real fusion statistics")
    ap.add_argument("--interval", default="10s", help="Frame interval folder, e.g. 10s")
    args = ap.parse_args()

    egt = load_reference_metric()
    rows = collect(args.interval, egt)
    if not rows:
        sys.exit("no videos scored")
    independence = check_interval_independence()
    summary, markdown = build_report(rows, args.interval, independence)

    out_dir = REPO / "output"
    (out_dir / "fusion_statistics.json").write_text(
        json.dumps({"summary": summary, "per_video": rows}, indent=2), encoding="utf-8"
    )
    (out_dir / "fusion_statistics.md").write_text(markdown, encoding="utf-8")

    avg = summary["averages"]
    print(f"videos scored          : {summary['videos']}")
    print(f"term F1, baseline      : {avg['baseline']['term_f1'] * 100:.1f}%")
    print(f"term F1, fused         : {avg['fused']['term_f1'] * 100:.1f}%")
    print(f"difference             : {summary['term_f1_delta_mean_pp']:+.2f} percentage points")
    print(f"permutation p-value    : {summary['permutation_test']['p_value']:.3f}")
    print(f"wilcoxon p-value       : {summary['wilcoxon']['p_value']:.3f}")
    print(f"WER baseline / fused   : {avg['baseline']['wer'] * 100:.1f}% / {avg['fused']['wer'] * 100:.1f}%")
    print(f"identical across runs  : {summary['independence']['identical_fused_transcript_across_intervals']}"
          f" of {summary['independence']['videos_checked']} videos")
    print(f"\nwrote {out_dir / 'fusion_statistics.json'}")
    print(f"wrote {out_dir / 'fusion_statistics.md'}")


if __name__ == "__main__":
    main()
