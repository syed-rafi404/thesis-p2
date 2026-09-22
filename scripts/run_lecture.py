#!/usr/bin/env python
"""
=============================================================================
ONE LECTURE VIDEO IN, ANNOTATED LECTURE NOTES OUT
=============================================================================
The final deliverable (CLAUDE.md) as one command, for any lecture video, including one with no
ground truth that no model was trained on:

  1 audio        16 kHz mono wav from the video (ffmpeg)
  2 frames       one frame every --interval seconds, at most 1920 wide (ffmpeg)
  3 boards       the board with the lecturer removed, per era between erasures:
                 pass 1 finds the eras on 10 s frames, pass 2 rebuilds each era from the dense
                 frames and ends it at the first erasure it sees (board_mosaic.py, RESULTS 4.1.1),
                 with the person-detection network and shadow mask (4.1.2)
  4 clean        whiteboard clean-up with the lecturer mask (clean_board.py)
  5 transcript   fine-tuned Whisper, timestamped (transcribe_finetuned.py)
  6 boxes        numbered boxes on each clean board, named and read by the VLM, plus the
                 VLM's reading of the whole board (label_boards.py --board-text)
  7 notes        notes that point at the boxes, English and Banglish, Markdown + HTML
                 (build_lecture_notes.py)

Each step runs as its own process, so GPU memory is freed between models, and a step whose
output exists is skipped (--force redoes everything). On the 3060 no single environment has
every library, so --python-vision (Pillow, torchvision) and --python-ml (torch, transformers,
peft) can be different interpreters; on the 5090 one interpreter does everything. --mock uses
stand-ins for the two Qwen steps (6, 7), which never run on the 3060 by the user's choice.

Output: output/lectures/<name>/ (notes_annotated_<language>.html is the result); run_lecture.json
records every step's duration.

    python scripts/run_lecture.py --video data/raw/live_classroom/BanglaASR30.mp4 --adapter <lora>
    python scripts/run_lecture.py --video ... --adapter <lora> --mock      (3060: Qwen stand-ins)
=============================================================================
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
SCRIPTS = REPO / "scripts"
STEPS = ("audio", "frames", "boards", "clean", "transcript", "boxes", "notes")


def run(cmd, label):
    print(f"\n=== {label}\n$ {' '.join(str(c) for c in cmd)}", flush=True)
    t = time.time()
    result = subprocess.run([str(c) for c in cmd])
    if result.returncode != 0:
        sys.exit(f"step failed: {label} (exit {result.returncode})")
    return time.time() - t


def has_module(python, module):
    return subprocess.run([python, "-c", f"import {module}"], capture_output=True).returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--name", default=None, help="Lecture name; default the video's file name")
    ap.add_argument("--out", default=None, help="Default output/lectures/<name>")
    ap.add_argument("--interval", type=int, default=2, help="Seconds between frames for the boards")
    ap.add_argument("--era-interval", type=int, default=10, help="Seconds between frames for era detection")
    ap.add_argument("--person-model", default="deeplab+shadow", choices=("temporal", "deeplab", "deeplab+shadow"))
    ap.add_argument("--base", default="openai/whisper-large-v3-turbo")
    ap.add_argument("--adapter", default=None, help="Fine-tuned LoRA adapter for the transcript")
    ap.add_argument("--vlm", default="Qwen/Qwen2.5-VL-7B-Instruct")
    ap.add_argument("--llm", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--quant", choices=("none", "8bit", "4bit"), default="none")
    ap.add_argument("--language", choices=("english", "banglish", "both"), default="both")
    ap.add_argument("--tag", default="")
    ap.add_argument("--mock", action="store_true", help="Stand-ins for the VLM and the notes model")
    ap.add_argument("--python-vision", default=sys.executable)
    ap.add_argument("--python-ml", default=sys.executable)
    ap.add_argument("--steps", nargs="+", choices=STEPS, default=list(STEPS))
    ap.add_argument("--force", action="store_true", help="Redo steps whose output exists")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"no such video: {video}")
    name = args.name or video.stem
    out = Path(args.out) if args.out else REPO / "output" / "lectures" / name
    out.mkdir(parents=True, exist_ok=True)
    frames, frames_eras = out / "frames", out / "frames_eras"
    board_dir, pass1 = out / "boards" / name, out / "boards" / "pass1"
    clean_dir = out / "boards" / "clean"
    audio = out / "audio.wav"
    transcript = out / "transcript.txt"
    record_path = out / "run_lecture.json"
    record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.exists() else {}
    record.update({"video": str(video), "name": name, "mock": args.mock})
    timings = record.setdefault("seconds", {})
    todo = [s for s in STEPS if s in args.steps]
    fresh = lambda path: args.force or not Path(path).exists()

    if ("audio" in todo or "frames" in todo) and not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH")

    if "audio" in todo and fresh(audio):
        timings["audio"] = run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-ac", "1",
                                "-ar", "16000", "-vn", audio], "1 audio")

    boards_done = (board_dir / "mosaic.json").exists() and not args.force
    if "frames" in todo and not boards_done and (args.force or not any(frames.glob("frame_*.jpg"))):
        if frames.exists():
            shutil.rmtree(frames)
        frames.mkdir(parents=True)
        timings["frames"] = run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vf",
                                 f"fps=1/{args.interval},scale='min(1920,iw)':-2", "-q:v", "3",
                                 frames / "raw_%06d.jpg"], "2 frames")
        # board_mosaic.py and notes_common.py read the time from the name: frame_<i>_<s>s.jpg
        for i, f in enumerate(sorted(frames.glob("raw_*.jpg"))):
            f.rename(frames / f"frame_{i:06d}_{i * args.interval:06d}s.jpg")
        if frames_eras.exists():
            shutil.rmtree(frames_eras)
        frames_eras.mkdir()
        step = max(1, args.era_interval // args.interval)
        for i, f in enumerate(sorted(frames.glob("frame_*.jpg"))):
            if i % step == 0:
                target = frames_eras / f"frame_{i // step:06d}_{i * args.interval:06d}s.jpg"
                try:
                    os.link(f, target)
                except OSError:
                    shutil.copy2(f, target)

    if "boards" in todo and fresh(board_dir / "mosaic.json"):
        person = args.person_model
        if person.startswith("deeplab") and not has_module(args.python_vision, "torchvision"):
            print("\nWARNING: torchvision is missing in --python-vision; boards use the temporal "
                  "lecturer mask (RESULTS 4.1: worse when the lecturer stands still)")
            person = "temporal"
        pass1.mkdir(parents=True, exist_ok=True)
        t = run([args.python_vision, SCRIPTS / "board_mosaic.py", "--frames", frames_eras,
                 "--interval", args.era_interval, "--person-model", person,
                 "--out-dir", pass1, "--json", pass1 / "mosaic.json"], "3a boards: find the eras")
        board_dir.mkdir(parents=True, exist_ok=True)
        t += run([args.python_vision, SCRIPTS / "board_mosaic.py", "--frames", frames,
                  "--interval", args.interval, "--eras-from", pass1 / "mosaic.json",
                  "--extend-to-erase", "--person-model", person, "--save-occluder",
                  "--out-dir", board_dir, "--json", board_dir / "mosaic.json"],
                 "3b boards: rebuild each era from every frame")
        timings["boards"] = t
        record["person_model"] = person

    if "clean" in todo:
        clean_dir.mkdir(parents=True, exist_ok=True)
        t = 0.0
        for era in json.loads((board_dir / "mosaic.json").read_text(encoding="utf-8")):
            img = Path(era["image"])
            img = img if img.is_absolute() else REPO / img
            target = clean_dir / f"{name}_{img.stem}_clean.jpg"
            if fresh(target):
                t += run([args.python_vision, SCRIPTS / "clean_board.py", img, target, "--mask",
                          img.with_name(img.stem + "_occluder.png")], f"4 clean {img.name}")
        timings["clean"] = timings.get("clean", 0) + t

    if "transcript" in todo and fresh(transcript):
        if not args.adapter:
            sys.exit("--adapter is needed for the transcript (the fine-tuned LoRA folder)")
        timings["transcript"] = run([args.python_ml, SCRIPTS / "transcribe_finetuned.py",
                                     "--run-dir", out, "--audio", audio, "--base", args.base,
                                     "--adapter", args.adapter, "--timestamps",
                                     "--out-name", transcript.name], "5 transcript")
        record["asr"] = {"base": args.base, "adapter": str(args.adapter)}

    boxes_json = out / ("board_boxes_MOCK.json" if args.mock else "board_boxes.json")
    if "boxes" in todo and fresh(boxes_json):
        cmd = [args.python_vision if args.mock else args.python_ml, SCRIPTS / "label_boards.py",
               "--run-dir", out, "--board-dir", board_dir, "--board-text", "--model", args.vlm]
        timings["boxes"] = run(cmd + (["--mock"] if args.mock else []), "6 boxes and board text")

    if "notes" in todo:
        cmd = [args.python_ml, SCRIPTS / "build_lecture_notes.py", "--run-dir", out,
               "--board-dir", board_dir, "--language", args.language,
               "--transcript-file", transcript.name, "--board-text-file", "board_text_clean.json",
               "--model", args.llm, "--quant", args.quant]
        cmd += (["--tag", args.tag] if args.tag else []) + (["--mock"] if args.mock else [])
        timings["notes"] = run(cmd, "7 notes")
        record["notes_model"] = "MOCK" if args.mock else args.llm

    record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print("\n=== done. seconds per step: " + ", ".join(f"{k} {v:.0f}" for k, v in timings.items()))
    for page in sorted(out.glob("notes_annotated_*.html")):
        print(f"  {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
