#!/usr/bin/env python
"""
=============================================================================
HOW LONG DOES EACH JOB ACTUALLY TAKE ON THIS MACHINE?
=============================================================================
Every timing in NEXT_STEPS.md was an estimate scaled from a 3060 run. This
script replaces the estimates with measurements taken from this machine's own
file write times and from the trainer's own reported runtime.

It only reads. Nothing is recomputed, so the numbers are whatever the machine
actually did on the day the work ran.

Two kinds of evidence, in order of trust:

  1. `train_runtime` printed by the HuggingFace trainer into the run log. This
     is the training loop's own clock and excludes model loading. Trusted.
  2. Differences between file write times (mtime). A job's output file is
     written when that job ends, so the gap between two consecutive outputs is
     the time the second one took. This includes process start-up and model
     loading for the first item of a run, so per-item rates are taken from the
     second item onward.

Copies made by `git clone` or `git pull` carry the checkout time, not the time
the work ran, so this is only meaningful on the machine that did the work. The
script says so for any folder whose files all share one timestamp.

Usage:
    python scripts/measure_run_times.py
    python scripts/measure_run_times.py --json       # machine-readable
=============================================================================
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_PARENT = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work")).parent
LECTURES = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"

# Model loading, measured as the gap between one run's last evaluation and the
# next run's adapter, minus that run's own training time. Consistent at ~70 s.
LOAD_S = 70

# The planned runs, as hours of ground-truth audio at an 80/20 video split.
PLANNED = [("6 h run (25 Sep)", 6.0), ("10 h run (27 Sep)", 10.0)]
CURVE_HOURS = [2, 4, 6, 8]        # the scaling-curve budgets
ALL_LECTURES = 43                 # every recorded lecture
ALL_BOARDS = 200                  # boards across all 43, at the rate the 13 scored ones set

# The fine-tune folders that hold whisper-large-v3-turbo runs, and the prefix
# their adapters and evaluations use. Folders that do not exist are skipped.
TURBO_RUNS = [
    ("ft_work", "turbo", "A only, test B"),
    ("ft_work_AC", "turbo_AC", "A+C, test B"),
    ("ft_work_ABtoC", "turbo", "A+B, test C"),
    ("ft_work_BCtoA", "turbo", "B+C, test A"),
]


def mtime(path):
    return dt.datetime.fromtimestamp(path.stat().st_mtime)


def clip_stats(path):
    """Clip count and total audio hours in a prepare_data jsonl."""
    if not path.exists():
        return 0, 0.0
    n, sec = 0, 0.0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            n += 1
            if "dur" in obj:
                sec += float(obj["dur"])
            elif "start" in obj and "end" in obj:
                sec += float(obj["end"]) - float(obj["start"])
    return n, sec / 3600.0


def train_runtimes(log_path):
    """Every `train_runtime` the trainer printed, with its rate, epochs and model.

    A log names its model only when it is not the default, so a log with no
    `--model` line trained whisper-small. The two models differ by about 3x in
    speed, so they must never be averaged together.
    """
    if not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    named = re.findall(r"openai/whisper-[a-z0-9.-]+", text, re.I)
    model = named[0] if named else "openai/whisper-small"
    out = []
    pattern = (r"\{'train_runtime': '([\d.]+)'.*?"
               r"'train_samples_per_second': '([\d.]+)'.*?"
               r"'epoch': '([\d.]+)'")
    for m in re.finditer(pattern, text):
        out.append((float(m.group(1)), float(m.group(2)), float(m.group(3)), model))
    return out


def measure_finetunes(report):
    """Training and evaluation times for the large-model runs."""
    rows = []
    # The trainer's own clock, from whichever log covers each run.
    logs = list(FT_PARENT.glob("*.log")) + [p for d in TURBO_RUNS
                                            for p in (FT_PARENT / d[0]).glob("*.log")]
    seen = set()
    for log in sorted(set(logs)):
        for runtime, rate, epochs, model in train_runtimes(log):
            passes = runtime * rate                    # sample-passes = clips x epochs
            key = (round(runtime, 1), round(rate, 2))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "source": "trainer clock",
                "log": str(log.relative_to(FT_PARENT)),
                "model": model,
                "train_runtime_s": runtime,
                "clips_per_s": rate,
                "epochs": epochs,
                "sample_passes": round(passes),
                "clips": round(passes / epochs) if epochs else None,
            })
    report["training"] = rows

    # Evaluation: the gap between an adapter and the evaluation that follows it.
    evals = []
    for folder, prefix, what in TURBO_RUNS:
        d = FT_PARENT / folder
        if not d.is_dir():
            continue
        n_test, h_test = clip_stats(d / "test.jsonl")
        n_train, h_train = clip_stats(d / "train.jsonl")
        for seed in ("seed42", "seed1"):
            adapter = d / f"lora_{prefix}_{seed}" / "adapter_model.safetensors"
            if not adapter.exists():
                continue
            t0 = mtime(adapter)
            for mode in ("fallback", "greedy"):
                ev = d / f"eval_{prefix}_{seed}_{mode}.json"
                if not ev.exists():
                    continue
                secs = (mtime(ev) - t0).total_seconds()
                if 0 < secs < 3600:
                    evals.append({
                        "folder": folder, "what": what, "seed": seed, "decode": mode,
                        "test_clips": n_test, "test_hours": round(h_test, 2),
                        "train_clips": n_train, "train_hours": round(h_train, 2),
                        "seconds": round(secs),
                        "s_per_test_clip": round(secs / n_test, 2) if n_test else None,
                    })
                t0 = mtime(ev)   # the next mode starts when this one ended
    report["evaluation"] = evals


def spans(paths):
    """Per-item seconds from a run's output files, skipping the first item.

    The first file of a run also carries process start-up and model loading, so
    it is excluded from the rate and reported separately.
    """
    times = sorted(mtime(p) for p in paths)
    if len(times) < 3:
        return None
    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])]
    total = (times[-1] - times[0]).total_seconds()
    return {
        "items": len(times),
        "span_s": round(total),
        "s_per_item": round(total / (len(times) - 1), 1),
        "slowest_gap_s": round(max(gaps), 1),
    }


def lecture_outputs(name, window_minutes=30):
    """Files called `name` across the lecture folders, grouped into one run.

    Files written far apart belong to different runs (a later re-run, or a git
    checkout), so only the largest cluster within `window_minutes` is used.
    """
    found = [d / name for d in sorted(LECTURES.iterdir()) if (d / name).exists()] \
        if LECTURES.is_dir() else []
    if not found:
        return None, []
    found.sort(key=mtime)
    best, run = [], [found[0]]
    for p in found[1:]:
        if (mtime(p) - mtime(run[-1])).total_seconds() <= window_minutes * 60:
            run.append(p)
        else:
            best = max(best, run, key=len)
            run = [p]
    best = max(best, run, key=len)
    return spans(best), best


def board_count():
    """Boards the VLM had to read, counted from its own output."""
    total = 0
    if not LECTURES.is_dir():
        return 0
    for d in LECTURES.iterdir():
        p = d / "board_text_frame.json"
        if p.exists():
            obj = json.loads(p.read_text(encoding="utf-8"))
            total += len(obj) if isinstance(obj, list) else len(obj.get("boards", obj))
    return total


def measure_qwen(report):
    boards = board_count()
    jobs = {}
    for label, fname in [
        ("VLM board transcription, raw frame", "board_text_frame.md"),
        ("VLM board transcription, mosaic", "board_text_mosaic.md"),
        ("Notes B (grounded prompt), 7B", "notes_B_prompt.md"),
        ("Notes C (+ VLM board text), 7B", "notes_C_vlm.md"),
        ("Notes D (+ fine-tuned transcript), 7B", "notes_D_full.md"),
        ("Whole-lecture fine-tuned transcript", "transcript_finetuned_v2.txt"),
    ]:
        s, files = lecture_outputs(fname)
        if s:
            jobs[label] = s
            if "board" in fname and boards:
                per_lecture_boards = boards / len(files) if files else 0
                jobs[label]["s_per_board"] = round(
                    s["span_s"] / max(boards - per_lecture_boards, 1), 1)
    report["qwen"] = {"boards_total": boards, "jobs": jobs}


def project(report):
    """What the planned runs will take, from the measured rates.

    Deliberately pessimistic: the slowest measured training rate and the
    slowest measured evaluation rate, so the number is a ceiling rather than a
    best case.
    """
    turbo = [r for r in report["training"] if "turbo" in r["model"]]
    evals = report["evaluation"]
    if not turbo or not evals:
        return
    clips_per_s = min(r["clips_per_s"] for r in turbo)
    epochs = max(r["epochs"] for r in turbo)

    # Clips per hour of audio, from the runs themselves rather than assumed.
    ratios = [r["train_clips"] / r["train_hours"] for r in evals if r["train_hours"]]
    clips_per_hour = sum(ratios) / len(ratios)

    worst = {}
    for r in evals:
        worst[r["decode"]] = max(worst.get(r["decode"], 0), r["s_per_test_clip"])
    both = sum(worst.values())

    runs = []
    for name, hours in PLANNED:
        train_h, test_h = hours * 0.8, hours * 0.2
        train_clips = round(train_h * clips_per_hour)
        test_clips = round(test_h * clips_per_hour)
        train_min = (train_clips * epochs / clips_per_s + LOAD_S) / 60
        eval_min = test_clips * both / 60
        runs.append({
            "name": name, "hours": hours,
            "train_hours": round(train_h, 1), "test_hours": round(test_h, 1),
            "train_clips": train_clips, "test_clips": test_clips,
            "train_min": train_min, "eval_min": eval_min,
            "total_two_seeds_h": 2 * (train_min + eval_min) / 60,
        })
    # The scaling curve retrains at each budget and evaluates on the same test
    # set every time, so it is four trainings plus four evaluations.
    curve_train = sum(round(h * clips_per_hour) * epochs / clips_per_s + LOAD_S
                      for h in CURVE_HOURS) / 60
    curve_eval = len(CURVE_HOURS) * runs[-1]["eval_min"]

    # The Qwen jobs, from the per-item rates measured above, over every lecture.
    jobs = report["qwen"]["jobs"]
    def rate(label, key="s_per_item"):
        return jobs.get(label, {}).get(key)

    qwen = []
    vlm = rate("VLM board transcription, raw frame", "s_per_board")
    if vlm:
        qwen.append(("VLM reads all boards", ALL_BOARDS * vlm / 60, "measured"))
        qwen.append(("VLM names the boxes on all boards", ALL_BOARDS * vlm / 60,
                     "assumes naming costs the same as transcribing"))
    notes = rate("Notes D (+ fine-tuned transcript), 7B")
    if notes:
        qwen.append((f"Notes, {ALL_LECTURES} lectures x 2 languages, 7B",
                     ALL_LECTURES * 2 * notes / 60, "measured"))
        qwen.append((f"Notes, {ALL_LECTURES} lectures x 2 languages, Qwen3-32B 4-bit",
                     ALL_LECTURES * 2 * notes * 5 / 60,
                     "NOT measured: guesses 5x the 7B, verify on the first lecture"))
    tr = rate("Whole-lecture fine-tuned transcript")
    if tr:
        qwen.append((f"Fine-tuned transcripts, {ALL_LECTURES} lectures",
                     ALL_LECTURES * tr / 60, "measured on 5-15 min lectures"))

    report["projection"] = {
        "clips_per_hour": round(clips_per_hour),
        "train_clips_per_s": round(clips_per_s, 1),
        "epochs": epochs,
        "s_per_clip_both_modes": round(both, 2),
        "runs": runs,
        "curve_min": curve_train + curve_eval,
        "qwen": [{"job": j, "minutes": m, "basis": b} for j, m, b in qwen],
    }


def show(report):
    print("=" * 74)
    print("  MEASURED RUN TIMES ON THIS MACHINE")
    print("=" * 74)

    print("\nTRAINING (LoRA, the trainer's own clock, model load excluded)")
    if not report["training"]:
        print("  no training logs found beside the repo")
    for model in sorted({r["model"] for r in report["training"]}, reverse=True):
        rows = [r for r in report["training"] if r["model"] == model]
        print(f"  {model}")
        for r in rows:
            print(f"    {r['clips']:>4} clips x {r['epochs']:.0f} epochs   "
                  f"{r['train_runtime_s']:>6.1f} s   {r['clips_per_s']:>5.1f} clips/s   "
                  f"({r['log']})")
        rates = [r["clips_per_s"] for r in rows]
        print(f"    -> {min(rates):.1f}-{max(rates):.1f} clips/s")
    if report["training"]:
        print("  model load adds about 70 s per run (from the file timestamps)")

    print("\nEVALUATION (base + tuned on the whole test set, one decode mode)")
    for r in report["evaluation"]:
        print(f"  {r['folder']:<14} {r['seed']:<7} {r['decode']:<9} "
              f"{r['test_clips']:>4} clips ({r['test_hours']:.2f} h)  "
              f"{r['seconds']:>4} s   {r['s_per_test_clip']} s/clip")
    per = [r["s_per_test_clip"] for r in report["evaluation"] if r["s_per_test_clip"]]
    if per:
        print(f"  -> {min(per):.1f}-{max(per):.1f} s per test clip per decode mode")

    q = report["qwen"]
    print(f"\nQWEN JOBS ({q['boards_total']} boards across the lecture folders)")
    for label, s in q["jobs"].items():
        extra = f", {s['s_per_board']} s/board" if "s_per_board" in s else ""
        print(f"  {label:<42} {s['items']:>2} lectures in {s['span_s']:>4} s "
              f"({s['s_per_item']} s/lecture{extra})")
    if not q["jobs"]:
        print("  no Qwen outputs found (this machine has not run them)")

    print("\nNot measured here: Qwen3-32B notes (never run on this machine) and")
    print("clean-board building (ran on the 3060).")

    p = report.get("projection")
    if p:
        print("\n" + "=" * 74)
        print(f"  PROJECTED, at {p['clips_per_hour']} clips per hour of audio")
        print("=" * 74)
        print(f"  slowest measured training rate {p['train_clips_per_s']} clips/s; "
              f"slowest evaluation {p['s_per_clip_both_modes']} s per test clip "
              f"(greedy + fallback)")
        for run in p["runs"]:
            print(f"\n  {run['name']}: {run['train_hours']} h train / "
                  f"{run['test_hours']} h test "
                  f"({run['train_clips']} / {run['test_clips']} clips)")
            print(f"    train, per seed        {run['train_min']:>5.0f} min "
                  f"(incl. {LOAD_S} s model load)")
            print(f"    evaluate, per seed     {run['eval_min']:>5.0f} min (both decode modes)")
            print(f"    two seeds, total       {run['total_two_seeds_h']:>5.1f} h")
        print(f"\n  scaling curve {'/'.join(str(h) for h in CURVE_HOURS)} h, 1 seed"
              f"      {p['curve_min'] / 60:>5.1f} h")
        print("\n  Qwen jobs over every lecture:")
        for j in p["qwen"]:
            print(f"    {j['job']:<52} {j['minutes']:>5.0f} min   ({j['basis']})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print the raw measurements")
    args = ap.parse_args()

    report = {"machine": os.environ.get("COMPUTERNAME", ""), "measured": dt.datetime.now().isoformat(timespec="seconds")}
    measure_finetunes(report)
    measure_qwen(report)
    project(report)

    if args.json:
        json.dump(report, sys.stdout, indent=2)
        print()
    else:
        show(report)


if __name__ == "__main__":
    main()
