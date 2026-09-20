#!/usr/bin/env python
"""
=============================================================================
PREFLIGHT: IS THIS MACHINE READY TO RUN THE THESIS PIPELINE?
=============================================================================
Run this first on a new machine. It checks everything the pipeline needs and,
for anything missing, prints the command that fixes it. Five seconds here
instead of discovering a missing package forty minutes into a training run.

The check that matters most on a new GPU is the PyTorch build. An RTX 5090 is
Blackwell, compute capability 12.0, and needs a CUDA 12.8 build, which means
torch 2.7 or newer. The torch 2.5.1+cu121 that the older machine used will
import fine, see the card, and then fail the moment it touches it. This script
catches that up front by comparing the card's compute capability against the
architectures the installed torch was actually compiled for.

Usage:
    python scripts/check_environment.py
    python scripts/check_environment.py --quiet     # only problems
=============================================================================
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))

OK, WARN, FAIL = "ok", "warn", "FAIL"
results = []


def record(status, label, detail="", fix=""):
    results.append((status, label, detail, fix))


def check_python():
    v = sys.version_info
    detail = f"{v.major}.{v.minor}.{v.micro} at {sys.executable}"
    record(OK if v >= (3, 9) else FAIL, "Python", detail,
           "" if v >= (3, 9) else "Use Python 3.10 or newer")


def check_torch():
    try:
        import torch
    except ImportError:
        record(FAIL, "torch", "not installed",
               "pip install torch --index-url https://download.pytorch.org/whl/cu128")
        return
    detail = f"{torch.__version__}, CUDA {torch.version.cuda}"
    if not torch.cuda.is_available():
        record(FAIL, "torch CUDA", detail + ", no device visible",
               "Check the driver, then reinstall torch with a matching CUDA build")
        return

    name = torch.cuda.get_device_name(0)
    total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    major, minor = torch.cuda.get_device_capability(0)
    record(OK, "GPU", f"{name}, {total:.0f} GB, compute {major}.{minor}")

    # Does this torch actually have kernels for this card?
    try:
        built = torch.cuda.get_arch_list()
    except Exception:
        built = []
    needed = f"sm_{major}{minor}"
    if built and needed not in built:
        record(FAIL, "torch build",
               f"{detail}; built for {', '.join(built)} but this card is {needed}",
               "pip install --upgrade torch --index-url "
               "https://download.pytorch.org/whl/cu128   (needs torch >= 2.7 for Blackwell)")
    else:
        record(OK, "torch build", detail + f", supports {needed}")

    record(OK if torch.cuda.is_bf16_supported() else WARN, "bf16",
           "supported" if torch.cuda.is_bf16_supported() else "not supported, fp16 will be used")

    if total >= 20:
        record(OK, "VRAM headroom",
               f"{total:.0f} GB: whisper-large-v3-turbo and a 7B VLM both fit")
    else:
        record(WARN, "VRAM headroom",
               f"{total:.0f} GB: stay on whisper-small or add --grad-checkpointing")


def check_packages():
    needed = {
        "numpy": "numpy", "PIL": "Pillow", "matplotlib": "matplotlib",
        "transformers": "transformers", "peft": "peft",
        "soundfile": "soundfile", "jiwer": "jiwer",
    }
    missing = []
    for module, package in needed.items():
        try:
            mod = __import__(module)
            record(OK, package, getattr(mod, "__version__", ""))
        except ImportError:
            missing.append(package)
            record(FAIL, package, "not installed")
    if missing:
        record(WARN, "install them all",
               "", "pip install " + " ".join(missing))


def check_ffmpeg():
    path = shutil.which("ffmpeg")
    if not path:
        record(FAIL, "ffmpeg", "not on PATH",
               "Install ffmpeg and put it on PATH; audio extraction needs it")
        return
    try:
        out = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=15)
        record(OK, "ffmpeg", out.stdout.splitlines()[0][:60] if out.stdout else path)
    except Exception:
        record(WARN, "ffmpeg", f"found at {path} but would not run")


def check_disk():
    for label, path in (("repo drive", REPO), ("work drive", FT_DIR.parent)):
        try:
            free = shutil.disk_usage(str(path)).free / (1024 ** 3)
        except OSError:
            record(WARN, label, f"{path} not reachable")
            continue
        status = OK if free >= 40 else (WARN if free >= 20 else FAIL)
        record(status, label, f"{free:.0f} GB free at {path}",
               "" if free >= 40 else "Qwen2.5-VL weights alone are about 16 GB")


def check_paths():
    record(OK if REPO.exists() else FAIL, "repo", str(REPO))
    record(OK if FT_DIR.exists() else WARN, "work dir", str(FT_DIR),
           "" if FT_DIR.exists() else
           "Set THESIS_FT_DIR, or place ft_work beside the repo. It is created on first run")

    pieces = {
        "train.jsonl": FT_DIR / "train.jsonl",
        "test.jsonl": FT_DIR / "test.jsonl",
        "clips/": FT_DIR / "clips",
        "models/whisper-small": FT_DIR / "models" / "whisper-small",
        "lora adapter": FT_DIR / "lora_whisper_small",
    }
    for label, path in pieces.items():
        record(OK if path.exists() else WARN, f"  {label}",
               "present" if path.exists() else "missing, will be rebuilt by prepare_data.py")


def check_data():
    gt = REPO / "data" / "ground_truth"
    files = sorted(gt.glob("*.txt")) if gt.exists() else []
    if not files:
        record(FAIL, "ground truth", f"no .txt in {gt}",
               "Copy data/ from the other machine; it is gitignored and does not clone")
        return
    record(OK, "ground truth", f"{len(files)} transcript files")

    missing_id, long_segs = [], 0
    import re
    stamp = re.compile(r"\[(\d+):(\d+)\s*-\s*(\d+):(\d+)\]")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"#\s*speaker\s*id\s*:", text, re.IGNORECASE):
            missing_id.append(path.name)
        for m in stamp.finditer(text):
            start = int(m.group(1)) * 60 + int(m.group(2))
            end = int(m.group(3)) * 60 + int(m.group(4))
            if end - start > 30:
                long_segs += 1

    if missing_id:
        record(FAIL if len(missing_id) == len(files) else WARN,
               "  Speaker ID headers", f"{len(missing_id)} of {len(files)} files missing",
               "Add '# Speaker ID: SPK04'. Without it every new lecture becomes one "
               "speaker called UNKNOWN and the speaker-independent split silently breaks")
    else:
        record(OK, "  Speaker ID headers", "all files have one")

    record(OK if long_segs == 0 else WARN, "  segment length",
           "all under 30s" if long_segs == 0 else f"{long_segs} segments over 30s",
           "" if long_segs == 0 else
           "Long segments get split by estimated timing, which misaligns text and audio")

    truth = REPO / "data" / "board_truth"
    n = len(list(truth.glob("*.json"))) if truth.exists() else 0
    record(OK if n else WARN, "board truth", f"{n} lecture files")

    runs = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
    n = len(list(runs.glob("*/final_lecture_notes.md"))) if runs.exists() else 0
    record(OK if n else WARN, "baseline notes", f"{n} lectures",
           "" if n else "Needed as the 'before' for the board-recall comparison; "
                        "output/ is gitignored, so copy it across")


def check_vlm():
    candidates = [os.environ.get("THESIS_QWEN"), FT_DIR / "models" / "qwen2.5-vl",
                  Path.home() / ".cache" / "huggingface" / "hub"]
    for c in candidates:
        if c and Path(c).exists():
            hits = list(Path(c).glob("**/*Qwen*VL*")) if "hub" in str(c) else [Path(c)]
            if hits:
                record(OK, "Qwen VL weights", str(hits[0])[:70])
                return
    record(WARN, "Qwen VL weights", "not found",
           "Needed only for annotation and the board-recall comparison. "
           "Set THESIS_QWEN, or let transformers download about 16 GB")


def main():
    ap = argparse.ArgumentParser(description="Check this machine can run the pipeline")
    ap.add_argument("--quiet", action="store_true", help="Show only warnings and failures")
    args = ap.parse_args()

    print("=" * 72)
    print("  PREFLIGHT CHECK")
    print("=" * 72)

    for fn in (check_python, check_torch, check_packages, check_ffmpeg,
               check_disk, check_paths, check_data, check_vlm):
        try:
            fn()
        except Exception as exc:                      # a broken check must not stop the rest
            record(WARN, fn.__name__, f"check itself failed: {exc}")

    fixes = []
    for status, label, detail, fix in results:
        if args.quiet and status == OK:
            continue
        mark = {OK: "  ok  ", WARN: " warn ", FAIL: " FAIL "}[status]
        print(f"[{mark}] {label:<24} {detail}")
        if fix:
            fixes.append((label, fix))

    fails = sum(1 for r in results if r[0] == FAIL)
    warns = sum(1 for r in results if r[0] == WARN)
    print("-" * 72)
    print(f"{len(results) - fails - warns} ok, {warns} warnings, {fails} failures")

    if fixes:
        print("\nTo fix:")
        for label, fix in fixes:
            print(f"  {label}:\n      {fix}")

    if fails == 0:
        print("\nReady. Next: python scripts/run_p3_experiment.py --skip curve")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
