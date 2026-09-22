#!/usr/bin/env python
"""
Pick the validation lectures for the learning-rate check (2026-09-22) and record them.

Validation lectures are used only to choose the learning rate. They are then train-only for good:
every later split passes them as prepare_data.py --never-test, so no choice made on them is ever
scored on them. Picked at random from the lectures with ground truth, about 20% of each
lecturer's minutes (the same rule as the test split, with its own seed).

    python scripts/choose_lr_validation.py         -> data/splits/lr_validation.json
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "finetune"))
from prepare_data import choose_test_lectures, discover, gt_minutes, read_speaker   # noqa: E402

SEED = 2026
OUT = REPO / "data" / "splits" / "lr_validation.json"


def main():
    if OUT.exists():
        print(f"already chosen: {OUT} (delete it only if you mean to choose again)")
        print(OUT.read_text(encoding="utf-8"))
        return 0
    usable = []
    for stem, path, flagged in discover(str(REPO / "data" / "ground_truth")):
        if flagged:
            continue
        speaker = read_speaker(path, stem, {})
        minutes = gt_minutes(path)
        if speaker != "UNKNOWN" and minutes > 0:
            usable.append((stem, speaker, minutes))
    chosen = sorted(choose_test_lectures(usable, 0.2, SEED))
    record = {
        "purpose": "validation lectures for the learning-rate check; train-only in every later split "
                   "(prepare_data.py --never-test)",
        "chosen_on": "2026-09-22", "seed": SEED, "fraction": 0.2,
        "lectures": chosen,
        "minutes": {s: round(m, 1) for s, _, m in usable if s in chosen},
        "speakers": {s: spk for s, spk, _ in usable if s in chosen},
        "pool": {s: [spk, round(m, 1)] for s, spk, m in usable},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("lectures", "minutes", "speakers")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
