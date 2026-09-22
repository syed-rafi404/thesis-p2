#!/usr/bin/env python
"""
=============================================================================
PREFLIGHT FOR TRAINING ON THE NEW DATA: ARE THE NAMES, SPEAKERS AND TIMES RIGHT?
=============================================================================
Run this before run_p3_experiment.py on the machine that will train. It checks what would
silently corrupt the training data rather than crash:

  errors (exit code 1):
    - a ground-truth file with no video of the same name in data/raw
    - two different videos with the same name in data/raw (e.g. the pre-2026-09-22 layout,
      Speaker2/BanglaASR6.mp4, next to the new live_classroom/BanglaASR6.mp4)
    - a ground-truth file without "# Speaker ID:" (new files must say who is speaking)
    - timestamps prepare_data.py cannot read (their text would join the previous clip)
    - a transcript that runs past the end of its video (wrong video, or wrong times)
    - a Speaker ID that disagrees with the voice check (speaker_groups.py), when present
  reported:
    - files marked not ready in their name ("[Needs recheck]BanglaASR9..."), left out
    - videos with no ground truth (not used for training)
    - hours of ground truth per lecturer, and roughly what a 20% test split leaves

    python scripts/check_new_data.py
=============================================================================
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
sys.path.insert(0, str(REPO / "finetune"))
from prepare_data import (LOOKS_LIKE_TS, TS_RE, VIDEO_EXTS, discover, parse_gt,   # noqa: E402
                          raw_video, read_speaker)

VOICE = REPO / "output" / "speaker_check" / "speaker_groups.json"


def duration_s(path):
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gt-dir", default=str(REPO / "data" / "ground_truth"))
    ap.add_argument("--test-fraction", type=float, default=0.2)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    voice = {}
    if VOICE.exists():
        voice = {k: v["best"] for k, v in json.loads(VOICE.read_text(encoding="utf-8"))["lectures"].items()}
    errors, notes = [], []
    minutes_by_speaker = {}
    used = set()
    print(f"{'lecture':<14} {'speaker':<8} {'transcribed':>11} {'video':>7}  status")
    for stem, path, flagged in discover(args.gt_dir):
        name = os.path.basename(path)
        if flagged:
            notes.append(f"{name}: marked not ready by its name, left out")
            print(f"{stem:<14} {'':<8} {'':>11} {'':>7}  left out (marked not ready)")
            continue
        problems = []
        try:
            video = raw_video(stem)
        except SystemExit as e:
            video, problems = None, [str(e)]
        if video is None and not problems:
            problems.append("no video with this name in data/raw")
        speaker = read_speaker(path, stem, {})
        if speaker == "UNKNOWN":
            problems.append("no '# Speaker ID:' line")
        raw = "\n".join(ln for ln in Path(path).read_text(encoding="utf-8").splitlines()
                        if not ln.lstrip().startswith("#"))
        unread = [ln for ln in raw.splitlines() if LOOKS_LIKE_TS.search(ln) and not TS_RE.search(ln)]
        if unread:
            problems.append(f"{len(unread)} unreadable timestamp(s), first {unread[0].strip()[:24]}"
                            " (run validate_ground_truth.py --fix)")
        segs = parse_gt(path)
        if not segs:
            problems.append("no readable [m:ss-m:ss] segments")
        spoken = sum(e - s for s, e, _ in segs) / 60
        end = max((e for _, e, _ in segs), default=0)
        vdur = duration_s(video) if video else None
        if vdur is not None and end > vdur + 15:
            problems.append(f"transcript ends at {end / 60:.1f} min but the video is {vdur / 60:.1f} min")
        if voice.get(stem) and speaker != "UNKNOWN" and voice[stem] != speaker:
            problems.append(f"Speaker ID {speaker}, but the voice check says {voice[stem]}")
        status = "ok" if not problems else "; ".join(problems)
        print(f"{stem:<14} {speaker:<8} {spoken:>8.1f} min {('%.1f' % (vdur / 60)) if vdur else '?':>7}  {status}")
        if problems:
            errors.append(f"{name}: {status}")
        else:
            minutes_by_speaker[speaker] = minutes_by_speaker.get(speaker, 0) + spoken
        if video:
            used.add(os.path.normcase(os.path.abspath(video)))

    unused = []
    for root, _d, files in os.walk(REPO / "data" / "raw"):
        for f in files:
            p = os.path.normcase(os.path.abspath(os.path.join(root, f)))
            if os.path.splitext(f)[1] in VIDEO_EXTS and re.match(r"BanglaASR\d+$", os.path.splitext(f)[0]) \
                    and p not in used and "screen_recorded" not in p:
                unused.append(p)
    total = sum(minutes_by_speaker.values())
    print("\nground truth ready to train on: " + ", ".join(
        f"{k} {v / 60:.2f} h" for k, v in sorted(minutes_by_speaker.items())) + f"; total {total / 60:.2f} h")
    print(f"a {args.test_fraction:.0%} video split would leave about {total * (1 - args.test_fraction) / 60:.1f} h "
          f"to train and {total * args.test_fraction / 60:.1f} h to test")
    print(f"videos with no ground truth (not used for training): {len(unused)}")
    for n in notes:
        print("note: " + n)
    if not voice:
        print("note: no voice check yet (scripts/speaker_groups.py); Speaker IDs are taken on trust")
    if errors:
        print(f"\n{len(errors)} problem(s); fix before training:")
        for e in errors:
            print("  " + e)
        return 1
    print("\nall ground-truth files are consistent with their videos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
