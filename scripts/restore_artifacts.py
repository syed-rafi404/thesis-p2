#!/usr/bin/env python
"""
=============================================================================
PUT THE COMMITTED FINE-TUNE RESULTS BACK WHERE THE SCRIPTS EXPECT THEM
=============================================================================
The fine-tune work folders (ft_work, ft_work_3spk, ...) live beside the repo,
not in it. Their small, irreplaceable parts are committed under artifacts/:
adapters, evaluations, manifests, split.json, logs, and the extracted audio of
Speaker3, whose videos are not in git. Clips and the whisper-small weights are
not committed: clips are rebuilt here from the pipeline audio, and the base
model is reused from an existing folder or downloaded.

After `git pull` on another machine:

    python scripts/restore_artifacts.py            # shows the plan, changes nothing
    python scripts/restore_artifacts.py --apply    # does it

What --apply does, per work folder:
  1. If the existing ft_work is not the corrected split (no split.json with
     "speaker_map": "v2"; the 3060's original has no split.json at all), rename
     it to ft_work_v1_video6_in_train first, so nothing silently keeps using
     the leaked adapter or its manifests.
  2. Copy every committed file across. Files already present are left alone.
  3. Make sure ft_work/models/whisper-small exists: reuse the archived copy if
     there is one, otherwise download openai/whisper-small (the same model).
  4. Rebuild clips/ with prepare_data.py using the flags that made that folder,
     then check the rebuilt train and test manifests match the committed ones.
Nothing is ever deleted.
=============================================================================
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
ARTIFACTS = REPO / "artifacts"
PARENT = REPO.parent
ARCHIVE = "ft_work_v1_video6_in_train"

# The prepare_data.py flags that produced each folder. {self} is that folder.
PREPARE = {
    "ft_work": ["--only-speakers", "A,B", "--test-speakers", "B"],
    "ft_work_3spk": ["--test-speakers", "B,C", "--audio-dir", "{3spk}/audio_cache"],
    "ft_work_AC": ["--test-speakers", "B", "--audio-dir", "{3spk}/audio_cache"],
    "ft_work_v1_repro_5090": ["--speaker-map", "v1"],
    "ft_work_ABtoC": ["--test-speakers", "C", "--audio-dir", "{3spk}/audio_cache"],
    "ft_work_BCtoA": ["--test-speakers", "A", "--audio-dir", "{3spk}/audio_cache"],
}


def say(apply, msg):
    print(("  " if apply else "  [plan] ") + msg)


def is_leaked(ft_dir):
    """Anything but a folder marked as the corrected split counts as superseded.

    The 3060's original ft_work has no split.json at all, so absence must count.
    """
    split = ft_dir / "split.json"
    if not split.exists():
        return True
    try:
        return json.loads(split.read_text(encoding="utf-8")).get("speaker_map") != "v2"
    except (OSError, ValueError):
        return True


def copy_tree(src, dst, apply):
    copied = 0
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        target = dst / path.relative_to(src)
        if target.exists():
            continue
        copied += 1
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return copied


def ensure_base_model(ft_dir, apply):
    model = ft_dir / "models" / "whisper-small"
    if (model / "model.safetensors").exists():
        return
    archived = PARENT / ARCHIVE / "models" / "whisper-small"
    if (archived / "model.safetensors").exists():
        say(apply, f"copy base model from {archived}")
        if apply:
            shutil.copytree(archived, model, dirs_exist_ok=True)
        return
    say(apply, f"download openai/whisper-small into {model}")
    if apply:
        from huggingface_hub import snapshot_download
        snapshot_download("openai/whisper-small", local_dir=str(model),
                          allow_patterns=["*.json", "*.txt", "model.safetensors"])


def keys(path):
    with open(path, encoding="utf-8") as fh:
        return [(r["audio"], r["start"], r["end"], r["text"])
                for r in (json.loads(line) for line in fh if line.strip())]


def rebuild_clips(name, work, apply):
    if (work / "clips").is_dir() and any((work / "clips").iterdir()):
        return
    flags = [f.format(**{"3spk": str(PARENT / "ft_work_3spk")}) for f in PREPARE[name]]
    # Every committed folder was made from the ground truth as it was before the 2026-09-22
    # renumbering (old 6-9 are now named 10-13, old 10-13 are 14-17). That exact copy is frozen;
    # reading data/ground_truth instead would pair new names with old audio.
    frozen = REPO / "data" / "ground_truth_v1_2026-09-21"
    if frozen.is_dir():
        flags += ["--gt-dir", str(frozen)]
    say(apply, f"rebuild clips: prepare_data.py {' '.join(flags)}")
    if not apply:
        return
    # prepare_data.py rewrites the manifests; keep the committed ones to compare.
    saved = {f: keys(work / f) for f in ("train.jsonl", "test.jsonl") if (work / f).exists()}
    env = dict(os.environ, THESIS_FT_DIR=str(work))
    result = subprocess.run([sys.executable, str(REPO / "finetune" / "prepare_data.py"),
                             "--out", str(work), *flags], env=env)
    if result.returncode != 0:
        print(f"  prepare_data.py failed for {name}; clips not rebuilt")
        return
    for f, before in saved.items():
        same = keys(work / f) == before
        print(f"  {name}/{f}: {'matches the committed manifest' if same else 'MISMATCH, check before use'}")


def main():
    ap = argparse.ArgumentParser(description="Restore committed fine-tune artifacts")
    ap.add_argument("--apply", action="store_true", help="Make the changes; default is a dry run")
    ap.add_argument("--work-parent", default=None,
                    help="Folder that holds ft_work and friends; default: beside the repo")
    args = ap.parse_args()
    global PARENT
    if args.work_parent:
        PARENT = Path(args.work_parent)

    if not ARTIFACTS.is_dir():
        sys.exit(f"no {ARTIFACTS}; pull the repo first")
    print(f"repo      : {REPO}")
    print(f"work dirs : {PARENT}")
    print("mode      : " + ("apply" if args.apply else "dry run (add --apply to do it)") + "\n")

    names = [n for n in PREPARE if (ARTIFACTS / n).is_dir()]
    names.sort(key=lambda n: n != "ft_work_3spk")    # its audio feeds the other rebuilds
    for name in names:
        work = PARENT / name
        print(name)
        if name == "ft_work" and work.exists() and is_leaked(work):
            if (PARENT / ARCHIVE).exists():
                print(f"  {work} is the leaked split and {ARCHIVE} already exists; "
                      "move one of them by hand, then rerun")
                continue
            say(args.apply, f"rename the leaked {work.name} -> {ARCHIVE}")
            if args.apply:
                work.rename(PARENT / ARCHIVE)
        n = copy_tree(ARTIFACTS / name, work, args.apply)
        say(args.apply, f"copy {n} committed files into {work}")
        if name == "ft_work":
            ensure_base_model(work, args.apply)
        rebuild_clips(name, work, args.apply)
        print()
    print("done" if args.apply else "nothing changed; rerun with --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
