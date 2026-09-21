#!/usr/bin/env python
"""
=============================================================================
DATA-SCALING CURVE FOR THE BANGLISH FINE-TUNE
=============================================================================
Trains the same LoRA recipe on increasing amounts of training audio and scores
each one against the same held-out speaker, producing the curve that answers
"how much transcription effort actually buys how much accuracy".

That curve is a defensible result whichever way it bends. A rising curve says
more annotation is worth funding. A flat one says the bottleneck is elsewhere,
which is equally worth knowing before anyone transcribes another 20 hours.

Every subset is drawn from the same pool of extracted clips with a fixed seed,
so the smaller budgets are strict subsets of the larger ones and the only thing
that changes between points is the amount of data.

Usage:
    python scripts/run_scaling_curve.py --hours 0.3 0.6 1.2 --epochs 8
    python scripts/run_scaling_curve.py --hours 2 4 6 8        # once 8h lands
    python scripts/run_scaling_curve.py --dry-run              # print the plan

Outputs, under F:\\thesisP2\\ft_work\\curve\\:
    train_<h>h.jsonl          the subset manifest for each point
    adapter_<h>h/             the LoRA adapter trained on it
    eval_curve_<h>h.json/.md  its evaluation against the held-out speaker
    scaling_curve.json        every point in one file
    scaling_curve.md          a table ready for a chapter
=============================================================================
"""

import argparse
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))
CURVE_DIR = FT_DIR / "curve"


def find_python():
    """The interpreter that has torch, transformers and peft.

    Order: THESIS_PYTHON, the venv used on the original machine, then whatever
    is running this script. Keeps the curve runnable on a different box
    without edits.
    """
    candidates = [os.environ.get("THESIS_PYTHON"),
                  REPO.parent / "envs" / "thesis_ft" / "Scripts" / "python.exe",
                  REPO.parent / "envs" / "thesis_ft" / "bin" / "python",
                  sys.executable]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    return Path(sys.executable)


PYTHON = find_python()


def load_manifest(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def write_manifest(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def subset_for(rows, hours, seed):
    """Deterministic nested subsets: a smaller budget is a subset of a larger one."""
    shuffled = list(rows)
    random.Random(seed).shuffle(shuffled)
    budget, kept, total = hours * 3600, [], 0.0
    for row in shuffled:
        if total >= budget:
            break
        kept.append(row)
        total += row.get("dur", 0.0)
    kept.sort(key=lambda r: (str(r.get("video")), r.get("start", 0)))
    return kept, total / 3600


def run(cmd, label):
    print(f"    $ {' '.join(str(c) for c in cmd[:3])} ...")
    started = time.time()
    # Explicit UTF-8: on Windows the default cp1252 cannot decode the children's
    # progress bars and Banglish examples, and the reader thread crashes noisily.
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        tail = (result.stderr or result.stdout or "").strip().splitlines()[-12:]
        print(f"    {label} FAILED:")
        for line in tail:
            print(f"      {line}")
        return None
    print(f"    {label} finished in {time.time() - started:.0f}s")
    return result.stdout


def main():
    ap = argparse.ArgumentParser(description="Train and evaluate across training-set sizes")
    ap.add_argument("--hours", nargs="+", default=["0.3", "0.6", "1.2"],
                    help="Training budgets in hours; 'all' means the whole training pool")
    ap.add_argument("--decode", nargs="+", default=["greedy"], choices=("greedy", "fallback"),
                    help="Decoding(s) to evaluate each adapter with; see finetune/evaluate.py")
    ap.add_argument("--epochs", type=float, default=8.0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--train-manifest", default=str(FT_DIR / "train.jsonl"))
    ap.add_argument("--test-manifest", default="test.jsonl")
    ap.add_argument("--model", default=None, help="Base model, e.g. openai/whisper-large-v3-turbo")
    ap.add_argument("--extra-train-args", default="",
                    help="Passed straight to train_lora.py, e.g. \"--grad-checkpointing --lora-r 32\"")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Reuse any point already evaluated")
    args = ap.parse_args()

    print(f"interpreter  : {PYTHON}")

    rows = load_manifest(args.train_manifest)
    available = sum(r.get("dur", 0.0) for r in rows) / 3600
    print(f"training pool: {len(rows)} clips, {available:.2f} hours")
    print(f"budgets      : {args.hours} hours, {args.epochs} epochs each\n")

    CURVE_DIR.mkdir(parents=True, exist_ok=True)
    points = []

    for requested in args.hours:
        hours = available if requested == "all" else float(requested)
        if hours > available + 1e-6:
            print(f"  [skip] {hours}h requested but only {available:.2f}h available")
            continue

        tag = "all" if requested == "all" else f"{hours:g}h".replace(".", "p")
        subset, actual = subset_for(rows, hours, args.seed)
        manifest_path = CURVE_DIR / f"train_{tag}.jsonl"
        adapter_path = CURVE_DIR / f"adapter_{tag}"
        # Greedy keeps the original file names so earlier curves still line up.
        eval_tags = {d: f"curve_{tag}" + ("" if d == "greedy" else f"_{d}") for d in args.decode}
        eval_jsons = {d: FT_DIR / f"eval_{t}.json" for d, t in eval_tags.items()}

        print(f"[{tag}] {len(subset)} clips, {actual:.2f}h actual")
        if args.dry_run:
            continue
        pending = [d for d in args.decode
                   if not (args.skip_existing and eval_jsons[d].exists())]
        if not pending:
            print("    already evaluated, reusing")
        else:
            if not (args.skip_existing and (adapter_path / "adapter_config.json").exists()):
                write_manifest(manifest_path, subset)
                if run([str(PYTHON), str(REPO / "finetune" / "train_lora.py"),
                        "--train-file", str(manifest_path),
                        "--adapter-out", str(adapter_path),
                        "--epochs", str(args.epochs),
                        "--batch", str(args.batch),
                        "--seed", "42"]
                       + (["--model", args.model] if args.model else [])
                       + args.extra_train_args.split(), "train") is None:
                    continue
            for d in pending:
                run([str(PYTHON), str(REPO / "finetune" / "evaluate.py"),
                     "--adapter", str(adapter_path),
                     "--split", args.test_manifest,
                     "--batch", str(args.batch),
                     "--decode", d,
                     "--tag", eval_tags[d]]
                    + (["--base", args.model] if args.model else []), f"evaluate ({d})")

        for d in args.decode:
            if not eval_jsons[d].exists():
                print(f"    no {d} evaluation output, skipping")
                continue
            record = json.loads(eval_jsons[d].read_text(encoding="utf-8"))
            points.append({
                "hours_requested": requested,
                "hours_actual": actual,
                "clips": len(subset),
                "decode": d,
                "base": record["base"],
                "tuned": record["tuned"],
                "rank_tests": record.get("rank_tests", {}),
            })
            tuned = record["tuned"]
            print(f"    {d:8} WER median {tuned.get('wer_median_per_clip', 0) * 100:.1f}%  "
                  f"CER median {tuned.get('cer_median_per_clip', 0) * 100:.1f}%  "
                  f"Term F1 {tuned.get('term_f1', 0) * 100:.1f}%")
        print()

    if not points:
        print("no points completed")
        return 1

    (CURVE_DIR / "scaling_curve.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    pct = lambda d, k: f"{d.get(k, 0) * 100:.1f}%"
    lines = ["# Data-scaling curve, Banglish LoRA fine-tune", ""]
    for d in args.decode:
        first = next((p for p in points if p["decode"] == d), None)
        if first:
            base = first["base"]
            lines.append(f"Base model, {d} decoding, same held-out speaker: "
                         f"WER median {pct(base, 'wer_median_per_clip')}, "
                         f"CER median {pct(base, 'cer_median_per_clip')}, "
                         f"Term F1 {pct(base, 'term_f1')}.")
    lines += [
        "",
        "A positive z means the fine-tune beats the base model on that metric.",
        "",
        "| Training audio | Clips | Decode | WER median | CER median | Term F1 "
        "| Wins on CER | CER Wilcoxon | Runaway clips |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for p in points:
        t = p["tuned"]
        cer_stats = (p.get("rank_tests") or {}).get("cer") or {}
        wins = f"{cer_stats.get('better', '?')}/{cer_stats.get('total', '?')}"
        z, pv = cer_stats.get("wilcoxon_z"), cer_stats.get("wilcoxon_p")
        wil = f"z = {z:+.2f}, p = {pv:.1e}" if z is not None and pv is not None else "n/a"
        lines.append(
            f"| {p['hours_actual']:.2f} h | {p['clips']} | {p['decode']} "
            f"| {pct(t, 'wer_median_per_clip')} | {pct(t, 'cer_median_per_clip')} "
            f"| {pct(t, 'term_f1')} | {wins} | {wil} | {t.get('runaway_clips', '?')} |"
        )
    lines += [
        "",
        "Every row uses the same held-out speaker and the same recipe; only the amount",
        "of training audio changes. Subsets are nested and drawn with a fixed seed, so",
        "a smaller budget is a strict subset of every larger one.",
        "",
    ]
    (CURVE_DIR / "scaling_curve.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {CURVE_DIR / 'scaling_curve.json'}")
    print(f"wrote {CURVE_DIR / 'scaling_curve.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
