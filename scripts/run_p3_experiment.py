#!/usr/bin/env python
"""
=============================================================================
RUN THE WHOLE P3 FINE-TUNING EXPERIMENT
=============================================================================
One command that takes new lecture videos plus their transcripts and produces
every number the thesis needs: validation of the transcripts, a clip dataset
with a speaker-independent split, a trained adapter, an evaluation against
held-out speakers, and a data-scaling curve.

Written to be moved between machines. Nothing is hard-coded to one box:

    set THESIS_REPO=D:\\path\\to\\thesisP2          (optional, inferred otherwise)
    set THESIS_FT_DIR=D:\\path\\to\\ft_work         (optional, defaults beside the repo)
    set THESIS_PYTHON=D:\\envs\\ft\\Scripts\\python.exe   (optional, defaults to this one)

Typical use on the bigger GPU once all data is in:

    python scripts/run_p3_experiment.py --test-speakers SPK04,SPK05 ^
        --model openai/whisper-large-v3-turbo ^
        --curve-hours 2 4 6 8 --batch 8

Stages, each skippable:

    validate   every transcript against TRANSCRIPTION_GUIDE.md; stops on errors
    prepare    clip extraction and the speaker-independent split
    train      one LoRA adapter on all available training audio
    evaluate   base vs adapter on the held-out speakers
    curve      retrain and re-evaluate at several data budgets

Use --skip to leave stages out, for example --skip curve on a first pass.
=============================================================================
"""

import argparse
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))

STAGES = ("validate", "prepare", "train", "evaluate", "curve")


def find_python():
    for candidate in (os.environ.get("THESIS_PYTHON"),
                      REPO.parent / "envs" / "thesis_ft" / "Scripts" / "python.exe",
                      REPO.parent / "envs" / "thesis_ft" / "bin" / "python",
                      sys.executable):
        if candidate and Path(candidate).exists():
            return Path(candidate)
    return Path(sys.executable)


PYTHON = find_python()


def announce(stage, note=""):
    print("\n" + "=" * 70)
    print(f"  {stage.upper()}{'  -  ' + note if note else ''}")
    print("=" * 70)


def run(cmd, allow_fail=False):
    printable = " ".join(shlex.quote(str(c)) for c in cmd)
    print(f"$ {printable}\n")
    started = time.time()
    result = subprocess.run(cmd)
    took = time.time() - started
    if result.returncode != 0 and not allow_fail:
        print(f"\nstage failed after {took:.0f}s (exit {result.returncode})")
        return False
    print(f"\nfinished in {took / 60:.1f} min")
    return True


def gpu_report():
    try:
        import torch
    except ImportError:
        print("torch not importable in this interpreter; stages will use", PYTHON)
        return
    if not torch.cuda.is_available():
        print("no CUDA device visible")
        return
    name = torch.cuda.get_device_name(0)
    total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    bf16 = torch.cuda.is_bf16_supported()
    print(f"gpu: {name}, {total:.0f} GB, bf16 {'yes' if bf16 else 'no'}")
    if total >= 20:
        print("  plenty of memory: whisper-large-v3-turbo with LoRA is reasonable here")
    else:
        print("  12 GB class card: stay on whisper-small, or add --grad-checkpointing")


def main():
    ap = argparse.ArgumentParser(description="Run the full P3 fine-tuning experiment")
    ap.add_argument("--test-speakers", default="B",
                    help="Comma-separated Speaker IDs held out, matching the transcript headers")
    ap.add_argument("--model", default=None,
                    help="Base model path or hub id. Defaults to the local whisper-small")
    ap.add_argument("--epochs", type=float, default=8.0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--curve-hours", nargs="+", type=float, default=None,
                    help="Training budgets for the scaling curve, in hours")
    ap.add_argument("--extra-train-args", default="",
                    help='Passed to train_lora.py, e.g. "--grad-checkpointing --lora-r 32"')
    ap.add_argument("--tag", default="run")
    ap.add_argument("--only-speakers", default=None,
                    help="Passed to prepare_data.py: use only these speakers, e.g. A,B")
    ap.add_argument("--split-by", choices=("speaker", "video"), default="speaker",
                    help="Passed to prepare_data.py. video = random whole lectures in the test "
                         "set, the user's plan for the 10 h data (--test-speakers is then ignored)")
    ap.add_argument("--test-fraction", type=float, default=0.2)
    ap.add_argument("--split-seed", type=int, default=0)
    ap.add_argument("--test-lectures", default=None,
                    help="Passed to prepare_data.py with --split-by video: fixed test lectures")
    ap.add_argument("--audio-dir", default=None,
                    help="Passed to prepare_data.py: folder of old-numbered 16 kHz wavs, e.g. "
                         "<parent>/ft_work_3spk/audio_cache for lecturer C")
    ap.add_argument("--decode", nargs="+", default=["greedy"], choices=("greedy", "fallback"),
                    help="Decoding(s) to evaluate with. fallback adds Whisper's loop "
                         "safeguard to both models; greedy alone reproduces earlier numbers")
    ap.add_argument("--skip", nargs="*", default=[], choices=STAGES,
                    help="Stages to leave out")
    ap.add_argument("--allow-validation-errors", action="store_true",
                    help="Continue even when transcripts fail validation")
    args = ap.parse_args()

    print(f"repo       : {REPO}")
    print(f"work dir   : {FT_DIR}")
    print(f"interpreter: {PYTHON}")
    gpu_report()

    adapter = FT_DIR / f"lora_{args.tag}"
    todo = [s for s in STAGES if s not in args.skip]
    print(f"stages     : {', '.join(todo)}")

    if "validate" in todo:
        # Names, videos, Speaker IDs, readable timestamps, transcript length vs video, voice
        # check. These silently corrupt training data, so this gate is never skipped by
        # --allow-validation-errors.
        announce("validate", "ground truth against the videos (check_new_data.py)")
        if not run([str(PYTHON), str(REPO / "scripts" / "check_new_data.py"),
                    "--test-fraction", str(args.test_fraction)]):
            print("\nThe ground truth does not match the videos. Fix what check_new_data.py lists.")
            return 1
        # Report only. run(..., allow_fail=True) always returns True, so this check never
        # stopped a run, including every published one (their files have segments over 30 s,
        # which prepare_data.py splits at sentence ends). Kept visible, not blocking;
        # --allow-validation-errors is accepted for old command lines and changes nothing.
        announce("validate", "transcripts against the style guide (report only)")
        run([str(PYTHON), str(REPO / "scripts" / "validate_ground_truth.py"), "--quiet"],
            allow_fail=True)

    if "prepare" in todo:
        if args.split_by == "video":
            announce("prepare", f"clips and a random video split, {args.test_fraction:.0%} test, "
                                f"seed {args.split_seed}")
        else:
            announce("prepare", f"clips and split, holding out {args.test_speakers}")
        cmd = [str(PYTHON), str(REPO / "finetune" / "prepare_data.py"),
               "--test-speakers", args.test_speakers, "--out", str(FT_DIR),
               "--split-by", args.split_by, "--test-fraction", str(args.test_fraction),
               "--split-seed", str(args.split_seed)]
        cmd += ["--only-speakers", args.only_speakers] if args.only_speakers else []
        cmd += ["--test-lectures", args.test_lectures] if args.test_lectures else []
        cmd += ["--audio-dir", args.audio_dir] if args.audio_dir else []
        if not run(cmd):
            return 1

    if "train" in todo:
        announce("train", f"LoRA adapter -> {adapter.name}")
        cmd = [str(PYTHON), str(REPO / "finetune" / "train_lora.py"),
               "--data-dir", str(FT_DIR),
               "--adapter-out", str(adapter),
               "--epochs", str(args.epochs),
               "--batch", str(args.batch)]
        if args.model:
            cmd += ["--model", args.model]
        cmd += shlex.split(args.extra_train_args)
        if not run(cmd):
            return 1

    if "evaluate" in todo:
        for decode in args.decode:
            announce("evaluate", f"base vs fine-tuned on the held-out speakers, {decode}")
            tag = args.tag if decode == "greedy" else f"{args.tag}_{decode}"
            cmd = [str(PYTHON), str(REPO / "finetune" / "evaluate.py"),
                   "--adapter", str(adapter),
                   "--batch", str(args.batch),
                   "--decode", decode,
                   "--tag", tag]
            if args.model:
                cmd += ["--base", args.model]
            if not run(cmd):
                return 1
            report = FT_DIR / f"eval_{tag}.md"
            if report.exists():
                print("\n" + report.read_text(encoding="utf-8").split("## Examples")[0])

    if "curve" in todo and args.curve_hours:
        announce("curve", f"budgets {args.curve_hours} hours")
        cmd = [str(PYTHON), str(REPO / "scripts" / "run_scaling_curve.py"),
               "--hours", *[str(h) for h in args.curve_hours],
               "--epochs", str(args.epochs),
               "--batch", str(args.batch),
               "--decode", *args.decode,
               "--skip-existing"]
        if args.model:
            cmd += ["--model", args.model]
        if args.extra_train_args:
            cmd += ["--extra-train-args", args.extra_train_args]
        if not run(cmd):
            return 1
    elif "curve" in todo:
        print("\nskipping the curve: pass --curve-hours to run it")

    announce("done")
    print("Artifacts:")
    for path in sorted(FT_DIR.glob("eval_*.md")):
        print(f"  {path}")
    curve = FT_DIR / "curve" / "scaling_curve.md"
    if curve.exists():
        print(f"  {curve}")
    print(f"  {FT_DIR / 'split.json'}   (the frozen train/test split)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
