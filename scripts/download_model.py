#!/usr/bin/env python
"""
=============================================================================
DOWNLOAD A MODEL INTO HF_HOME, RESUMABLY
=============================================================================
Downloads are the slowest step on this machine and the easiest to lose. This
fetches a repo into the shared cache and can be re-run after an interruption:
huggingface_hub keeps partial files and resumes them.

It refuses to start if the drive does not have room, because a half-filled
disk fails much later, in the middle of something else.

Usage:
    python scripts/download_model.py Qwen/Qwen3-32B --expect-gb 65
    python scripts/download_model.py Qwen/Qwen2.5-VL-3B-Instruct --expect-gb 8
=============================================================================
"""

import argparse
import os
import shutil
import sys
import time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--expect-gb", type=float, default=0,
                    help="refuse to start with less than this much free, plus 10 GB headroom")
    ap.add_argument("--allow", nargs="*", default=None,
                    help="only these patterns, e.g. *.safetensors *.json")
    args = ap.parse_args()

    home = os.environ.get("HF_HOME")
    target = Path(home) if home else Path.home() / ".cache" / "huggingface"
    free_gb = shutil.disk_usage(target.drive + "\\" if target.drive else "/").free / 1e9
    need = args.expect_gb + 10
    print(f"repo      : {args.repo}")
    print(f"HF_HOME   : {target}")
    print(f"free space: {free_gb:.0f} GB, need about {need:.0f} GB")
    if args.expect_gb and free_gb < need:
        sys.exit(f"not enough room: {free_gb:.0f} GB free, {need:.0f} GB wanted")

    from huggingface_hub import snapshot_download
    start = time.time()
    path = snapshot_download(args.repo, allow_patterns=args.allow,
                             max_workers=8)
    size = sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())
    print(f"\ndone in {(time.time() - start) / 60:.1f} min, {size / 1e9:.1f} GB")
    print(path)


if __name__ == "__main__":
    main()
