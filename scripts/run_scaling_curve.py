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
    result = subprocess.run(cmd, capture_output=True, text=True)
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
    ap.add_argument("--hours", nargs="+", type=float, default=[0.3, 0.6, 1.2],
                    help="Training budgets in hours")
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

    for hours in args.hours:
        if hours > available + 1e-6:
            print(f"  [skip] {hours}h requested but only {available:.2f}h available")
            continue

        tag = f"{hours:g}h".replace(".", "p")
        subset, actual = subset_for(rows, hours, args.seed)
        manifest_path = CURVE_DIR / f"train_{tag}.jsonl"
        adapter_path = CURVE_DIR / f"adapter_{tag}"
        eval_tag = f"curve_{tag}"
        eval_json = FT_DIR / f"eval_{eval_tag}.json"

        print(f"[{hours:g}h] {len(subset)} clips, {actual:.2f}h actual")
        if args.dry_run:
            continue
        if args.skip_existing and eval_json.exists():
            print("    already evaluated, reusing")
        else:
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
            if run([str(PYTHON), str(REPO / "finetune" / "evaluate.py"),
                    "--adapter", str(adapter_path),
                    "--split", args.test_manifest,
                    "--batch", str(args.batch),
                    "--tag", eval_tag]
                   + (["--base", args.model] if args.model else []), "evaluate") is None:
                continue

        if not eval_json.exists():
            print("    no evaluation output, skipping this point")
            continue
        record = json.loads(eval_json.read_text(encoding="utf-8"))
        points.append({
            "hours_requested": hours,
            "hours_actual": actual,
            "clips": len(subset),
            "base": record["base"],
            "tuned": record["tuned"],
            "rank_tests": record.get("rank_tests", {}),
        })
        tuned = record["tuned"]
        print(f"    WER median {tuned.get('wer_median_per_clip', 0) * 100:.1f}%  "
              f"CER median {tuned.get('cer_median_per_clip', 0) * 100:.1f}%  "
              f"Term F1 {tuned.get('term_f1', 0) * 100:.1f}%\n")

    if not points:
        print("no points completed")
        return 1

    (CURVE_DIR / "scaling_curve.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    base = points[0]["base"]
    pct = lambda d, k: f"{d.get(k, 0) * 100:.1f}%"
    lines = [
        "# Data-scaling curve, Banglish LoRA fine-tune",
        "",
        f"Base model scored on the same held-out speaker: "
        f"WER median {pct(base, 'wer_median_per_clip')}, "
        f"CER median {pct(base, 'cer_median_per_clip')}, "
        f"Term F1 {pct(base, 'term_f1')}.",
        "",
        "| Training audio | Clips | WER median | CER median | Term recall | Term F1 | Wins on CER |",
        "|---|---|---|---|---|---|---|",
    ]
    for p in points:
        t = p["tuned"]
        cer_stats = (p.get("rank_tests") or {}).get("cer") or {}
        wins = f"{cer_stats.get('better', '?')}/{cer_stats.get('total', '?')}"
        lines.append(
            f"| {p['hours_actual']:.2f} h | {p['clips']} | {pct(t, 'wer_median_per_clip')} "
            f"| {pct(t, 'cer_median_per_clip')} | {pct(t, 'term_recall')} "
            f"| {pct(t, 'term_f1')} | {wins} |"
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
