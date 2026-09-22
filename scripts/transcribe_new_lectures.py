#!/usr/bin/env python
"""
Transcripts for the lectures outside the 13 scored ones (new numbers 6-9 and 18-43), so the 5090
can make notes for every video with run_lecture.py (which skips steps whose output exists).

Each lecture is transcribed by the leave-one-speaker-out adapter that never heard its lecturer,
the same rule as the 13 scored lectures' transcript_loso.txt: lecturer A (new 1-9) by
ft_work_BCtoA, C (new 14-43) by ft_work_ABtoC, B (new 10-13) by ft_work_AC. The lecturer comes from
the voice check (output/speaker_check/speaker_groups.json). Writes
output/lectures/<name>/transcript.txt (and audio.wav) through run_lecture.py --steps audio transcript.

    python scripts/transcribe_new_lectures.py
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PARENT = REPO.parent
ADAPTER = {"A": PARENT / "ft_work_BCtoA" / "lora_turbo_seed42",
           "B": PARENT / "ft_work_AC" / "lora_turbo_AC_seed42",
           "C": PARENT / "ft_work_ABtoC" / "lora_turbo_seed42"}
SCORED_NEW = set(range(1, 6)) | set(range(10, 18))       # the 13 scored lectures, new numbers


def main():
    voice = json.loads((REPO / "output" / "speaker_check" / "speaker_groups.json").read_text(encoding="utf-8"))["lectures"]
    videos = {}
    for f in (REPO / "data" / "raw" / "live_classroom").iterdir():
        m = re.fullmatch(r"BanglaASR(\d+)", f.stem)
        if m and f.is_file():
            videos[int(m.group(1))] = f
    todo = [n for n in sorted(videos) if n not in SCORED_NEW]
    env = dict(os.environ, HF_HUB_OFFLINE=os.environ.get("HF_HUB_OFFLINE", "1"),
               TRANSFORMERS_OFFLINE=os.environ.get("TRANSFORMERS_OFFLINE", "1"), PYTHONIOENCODING="utf-8")
    if Path(r"F:\thesisP2\hf_cache").exists():
        env.setdefault("HF_HOME", r"F:\thesisP2\hf_cache")
    done = 0
    for n in todo:
        name = f"BanglaASR{n}"
        out = REPO / "output" / "lectures" / name / "transcript.txt"
        if out.exists():
            print(f"{name:<14} already transcribed")
            done += 1
            continue
        spk = voice.get(name, {}).get("best")
        if spk not in ADAPTER:
            print(f"{name:<14} skipped: no lecturer from the voice check")
            continue
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "run_lecture.py"), "--video", str(videos[n]),
                            "--steps", "audio", "transcript", "--adapter", str(ADAPTER[spk])],
                           cwd=REPO, env=env, capture_output=True, text=True)
        ok = r.returncode == 0 and out.exists()
        done += ok
        print(f"{name:<14} lecturer {spk}, {ADAPTER[spk].parent.name}: {'ok' if ok else 'FAILED ' + r.stderr[-300:]}", flush=True)
    print(f"{done} of {len(todo)} lectures have a transcript")
    return 0 if done == len(todo) else 1


if __name__ == "__main__":
    sys.exit(main())
