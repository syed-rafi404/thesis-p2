#!/usr/bin/env python
"""
=============================================================================
THE WHISPER SIDE ON THE FULL GROUND TRUTH, ONE COMMAND (pre-registered: data/splits/tuning_plan.md)
=============================================================================
When the ~6 h of ground truth is in data/ground_truth, this does, in order and by itself:

  0 check    check_new_data.py must pass (names, videos, Speaker IDs, timestamps, lengths, voices)
  1 test set the final test lectures: the random video split (20% of each lecturer, seed 0) with
             the three validation lectures locked out (--never-test); printed and recorded
  2 tuning data   every lecture except the test lectures, validation = BanglaASR2, 12, 14
  3 tuning   scripts/tune_whisper.py, all five pre-registered stages, in <work>
  4 final    run_p3_experiment.py --split-by video --tuned: the same test lectures, training on
             everything else, the chosen settings, seeds 42 and 1, off-the-shelf Whisper scored
             on the same test clips
  5 record   results copied to artifacts/, committed and pushed

The test lectures never enter tuning. On a card with less than 20 GB (the 3060) training uses
--grad-checkpointing (identical learning, less memory). Steps whose output exists are skipped, so
it can be restarted. Log: <work>/pipeline_log.txt.

    python scripts/whisper_full_pipeline.py              (the 3060 or the 5090)
    python scripts/whisper_full_pipeline.py --dry-run    (steps 0-2 only, prints the plan)
=============================================================================
"""
import argparse
import ctypes
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "finetune"))
PARENT = REPO.parent
BASE = "openai/whisper-large-v3-turbo"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gt-dir", default=str(REPO / "data" / "ground_truth"))
    ap.add_argument("--tune-dir", default=str(PARENT / "ft_work_tune6h"))
    ap.add_argument("--final-dir", default=str(PARENT / "ft_work_final6h"))
    ap.add_argument("--audio-dir", default=str(PARENT / "ft_work_3spk" / "audio_cache"))
    ap.add_argument("--skip-tuning", action="store_true",
                    help="Use the 2.1 h rehearsal's settings (the fallback if time runs out)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    from prepare_data import choose_test_lectures, discover, gt_minutes, read_speaker

    tune, final = Path(args.tune_dir), Path(args.final_dir)
    tune.mkdir(parents=True, exist_ok=True)
    log = tune / "pipeline_log.txt"

    def say(m):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {m}"
        print(line, flush=True)
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    env = dict(os.environ, HF_HUB_OFFLINE=os.environ.get("HF_HUB_OFFLINE", "1"),
               TRANSFORMERS_OFFLINE=os.environ.get("TRANSFORMERS_OFFLINE", "1"), PYTHONIOENCODING="utf-8")
    if Path(r"F:\thesisP2\hf_cache").exists():
        env.setdefault("HF_HOME", r"F:\thesisP2\hf_cache")
    py = sys.executable

    def run(cmd, extra_env=None, label=""):
        t = time.time()
        r = subprocess.run([str(c) for c in cmd], cwd=REPO, env=dict(env, **(extra_env or {})))
        say(f"{label}: exit {r.returncode}, {(time.time() - t) / 60:.1f} min")
        if r.returncode != 0:
            sys.exit(f"stopped at: {label}")

    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)   # stay awake while this runs
    except Exception:
        pass

    run([py, REPO / "scripts" / "check_new_data.py", "--gt-dir", args.gt_dir], label="0 check")

    val = json.loads((REPO / "data" / "splits" / "lr_validation.json").read_text(encoding="utf-8"))["lectures"]
    usable = []
    for stem, path, flagged in discover(args.gt_dir):
        if flagged:
            continue
        spk, minutes = read_speaker(path, stem, {}), gt_minutes(path)
        if spk != "UNKNOWN" and minutes > 0:
            usable.append((stem, spk, minutes))
    test = sorted(choose_test_lectures(usable, 0.2, 0, never=set(val)))
    total = sum(m for _, _, m in usable)
    tmin = sum(m for s, _, m in usable if s in test)
    say(f"1 test set: {', '.join(test)} ({tmin / 60:.2f} h of {total / 60:.2f} h); validation (train-only): "
        f"{', '.join(val)}")
    (tune / "final_test_lectures.json").write_text(json.dumps(
        {"test": test, "validation": val, "test_hours": round(tmin / 60, 2), "total_hours": round(total / 60, 2),
         "rule": "prepare_data choose_test_lectures(fraction 0.2, seed 0, never=validation)"}, indent=2),
        encoding="utf-8")

    if not (tune / "train.jsonl").exists():
        run([py, REPO / "finetune" / "prepare_data.py", "--gt-dir", args.gt_dir, "--out", tune,
             "--split-by", "video", "--test-lectures", ",".join(val), "--exclude-lectures", ",".join(test),
             "--audio-dir", args.audio_dir], {"THESIS_FT_DIR": str(tune)}, "2 tuning data")
    if args.dry_run:
        say("dry run: stopping before any training")
        return 0

    small_gpu = True
    try:
        import torch
        small_gpu = torch.cuda.get_device_properties(0).total_memory < 20 * 1024 ** 3
    except Exception:
        pass
    gc = ["--grad-checkpointing"] if small_gpu else []

    if not args.skip_tuning and not (tune / "tuning_result.json").exists():
        run([py, REPO / "scripts" / "tune_whisper.py"], {"THESIS_TUNE_DIR": str(tune), "THESIS_PYTHON": py},
            "3 tuning")
    tuned = str(REPO / "artifacts" / ("ft_work_lr" if args.skip_tuning else tune.name) / "tuning_result.json")

    final.mkdir(parents=True, exist_ok=True)
    fenv = {"THESIS_FT_DIR": str(final), "THESIS_PYTHON": py}
    common = [py, REPO / "scripts" / "run_p3_experiment.py", "--split-by", "video", "--test-fraction", "0.2",
              "--split-seed", "0", "--model", BASE, "--audio-dir", args.audio_dir, "--tuned", tuned]
    if not (final / "eval_final.json").exists():
        run(common + (["--extra-train-args", " ".join(gc)] if gc else []) + ["--tag", "final", "--skip", "curve"],
            fenv, "4 final, seed 42")
    if not (final / "eval_final_s1.json").exists():
        run(common + ["--extra-train-args", " ".join(gc + ["--seed", "1"]), "--tag", "final_s1",
                      "--skip", "validate", "prepare", "curve"], fenv, "4 final, seed 1")
    split = json.loads((final / "split.json").read_text(encoding="utf-8"))
    if sorted(split.get("test_lectures", [])) != test:
        say(f"WARNING: the final run's test lectures {split.get('test_lectures')} differ from step 1's {test}")

    table = subprocess.run([py, REPO / "scripts" / "compare_evals.py",
                            f"seed 42={final / 'eval_final.json'}", f"seed 1={final / 'eval_final_s1.json'}"],
                           capture_output=True, text=True, cwd=REPO).stdout
    head = ["# Final run on the full ground truth (random video split)", "",
            f"Test lectures (never used in tuning): {', '.join(test)}, {tmin / 60:.2f} h. Validation lectures "
            f"{', '.join(val)} (train-only). Settings: `{tuned}`.", ""]
    (final / "final_summary.md").write_text("\n".join(head) + table, encoding="utf-8")
    dst = REPO / "artifacts" / final.name
    dst.mkdir(parents=True, exist_ok=True)
    for f in list(final.iterdir()) + [tune / "final_test_lectures.json", log]:
        if f.is_file() and f.suffix in (".json", ".jsonl", ".md", ".txt", ".log"):
            (dst / f.name).write_bytes(f.read_bytes())
    g = ["git", "-c", "safe.directory=F:/thesisP2/thesisP2"]
    subprocess.run(g + ["add", "-f", "--", f"artifacts/{final.name}", f"artifacts/{tune.name}"], cwd=REPO)
    subprocess.run(g + ["commit", "-q", "-m",
                        "Final Whisper run on the full ground truth (tuned, 2 seeds)\n\n"
                        f"Test lectures {', '.join(test)} ({tmin / 60:.2f} h), never used in tuning. "
                        f"Summary: artifacts/{final.name}/final_summary.md. Committed automatically by "
                        "scripts/whisper_full_pipeline.py.\n\n"
                        "Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>\n"], cwd=REPO)
    for _ in range(3):
        if subprocess.run(g + ["push", "origin", "main"], cwd=REPO).returncode == 0:
            break
        time.sleep(30)
    say("5 record: finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
