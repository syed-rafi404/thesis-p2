#!/usr/bin/env python
"""
Everything the 3060 owes the 5090, run once the final Whisper model exists (NEXT_STEPS "OPEN TASKS").

  1. transcript_base.txt for the 13 scored lectures: off-the-shelf Whisper, no adapter. Tomorrow's
     2x2 needs it to answer "does fine-tuning the ASR improve the notes?".
  2. transcript_final.txt for the demo lecture: the final adapter, so the demo shows the finished
     system. Written under a new name so the existing notes keep the transcript they were built on.
  3. BanglaASR44: boards and transcript here, because this machine has torchvision for the person
     mask; the 5090 falls back to the worse temporal mask without it.

Skips whatever already exists, so it can be re-run.

    python scripts/tonight_after_training.py --adapter <final lora> [--demo BanglaASR29]
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import notes_common as nc                                          # noqa: E402

VISION_PY = r"C:\Users\Rafi\miniconda3\envs\pyenv\python.exe"
BASE = "openai/whisper-large-v3-turbo"


def env():
    e = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", PYTHONIOENCODING="utf-8")
    e.setdefault("HF_HOME", r"F:\thesisP2\hf_cache")
    return e


def transcribe(run_dir, out_name, adapter):
    """One whole-lecture transcript. adapter="" is off-the-shelf Whisper (the loader skips peft)."""
    out = Path(run_dir) / out_name
    if out.exists():
        print(f"  {Path(run_dir).name:<16} {out_name}: already there")
        return True
    cmd = [sys.executable, str(REPO / "scripts" / "transcribe_finetuned.py"), "--run-dir", str(run_dir),
           "--base", BASE, "--adapter", adapter, "--timestamps", "--out-name", out_name]
    r = subprocess.run(cmd, cwd=REPO, env=env(), capture_output=True, text=True, errors="replace")
    ok = r.returncode == 0 and out.exists()
    print(f"  {Path(run_dir).name:<16} {out_name}: {'ok' if ok else 'FAILED ' + ((r.stderr or '') + (r.stdout or ''))[-300:]}",
          flush=True)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adapter", required=True, help="the final LoRA, e.g. F:\\thesisP2\\ft_work_final5h\\lora_final")
    ap.add_argument("--demo", default="BanglaASR29")
    ap.add_argument("--video-44", default=str(REPO / "data" / "raw" / "live_classroom" / "BanglaASR44.mp4"))
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    if not Path(args.adapter).exists():
        sys.exit(f"no adapter at {args.adapter}: did the final run finish?")

    print("1. off-the-shelf transcripts for the 13 scored lectures")
    lectures = nc.discover_lectures()
    done = sum(transcribe(info["run_dir"], "transcript_base.txt", "")
               for name, info in lectures.items() if info.get("run_dir"))
    print(f"   {done} of {len(lectures)}")

    print(f"2. {args.demo}: transcript from the final adapter")
    transcribe(REPO / "output" / "lectures" / args.demo, "transcript_final.txt", args.adapter)

    print("3. BanglaASR44: boards and transcript")
    v = Path(args.video_44)
    if not v.exists():
        alt = list(v.parent.glob("BanglaASR44.*"))
        v = alt[0] if alt else v
    if not v.exists():
        print("   no BanglaASR44 video found; skipped")
    else:
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "run_lecture.py"), "--video", str(v),
                            "--steps", "audio", "frames", "boards", "clean", "transcript",
                            "--adapter", args.adapter, "--python-vision", VISION_PY],
                           cwd=REPO, env=env(), capture_output=True, text=True, errors="replace")
        out = REPO / "output" / "lectures" / "BanglaASR44" / "transcript.txt"
        print(f"   exit {r.returncode}, transcript {'written' if out.exists() else 'MISSING'}")
        if r.returncode != 0:
            print("   " + ((r.stderr or "") + (r.stdout or ""))[-500:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
