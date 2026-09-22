#!/usr/bin/env python
"""
Leak-free, timestamped fine-tuned transcripts for the 13 keyed lectures.

Each lecture is transcribed by the leave-one-speaker-out adapter that never heard its lecturer
(CLAUDE.md, leakage rule for notes; RESULTS.md 1.5 for the adapters):
    lecturer A (lectures 1-5)    ft_work_BCtoA/lora_turbo_seed42      trained on B + C
    lecturer B (lectures 6-9)    ft_work_AC/lora_turbo_AC_seed42      trained on A + C
    lecturer C (lectures 10-13)  ft_work_ABtoC/lora_turbo_seed42      trained on A + B
Base model openai/whisper-large-v3-turbo, plain greedy decoding (as in the 1.5 headline), 28 s
chunks cut at quiet points, each line prefixed with its [m:ss-m:ss] span. Output:
transcript_loso.txt in each lecture's run folder, which build_lecture_notes.py prefers.

Usage:
    python scripts/make_loso_transcripts.py                 # all 13
    python scripts/make_loso_transcripts.py --lecture BanglaASR7_004
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_common as nc                                         # noqa: E402

BASE = "openai/whisper-large-v3-turbo"
FT_ROOT = nc.REPO.parent
ADAPTERS = {"A": FT_ROOT / "ft_work_BCtoA" / "lora_turbo_seed42",
            "B": FT_ROOT / "ft_work_AC" / "lora_turbo_AC_seed42",
            "C": FT_ROOT / "ft_work_ABtoC" / "lora_turbo_seed42"}


def speaker(name):
    n = nc.lecture_number(name)
    return "A" if n <= 5 else ("B" if n <= 9 else "C")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lecture", action="append")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--out-name", default="transcript_loso.txt")
    args = ap.parse_args()
    nc.utf8_console()

    import numpy as np
    import soundfile as sf
    import torch
    import transcribe_finetuned as tf
    from prepare_data import find_audio

    lectures = nc.discover_lectures()
    if args.lecture:
        lectures = {n: lectures[n] for n in args.lecture}
    device = "cuda" if torch.cuda.is_available() else "cpu"
    by_speaker = {}
    for name, info in lectures.items():
        by_speaker.setdefault(speaker(name), []).append((name, info))

    for spk, items in sorted(by_speaker.items()):
        adapter = ADAPTERS[spk]
        if not adapter.exists():
            sys.exit(f"adapter missing: {adapter} (run scripts/restore_artifacts.py --apply)")
        print(f"lecturer {spk}: {adapter.parent.name}/{adapter.name}")
        model, processor = tf.load_model(BASE, str(adapter), device)
        for name, info in items:
            m = __import__("re").match(r"(BanglaASR\d+)", name)
            audio = find_audio(m.group(1))
            if not audio or info["run_dir"] is None:
                print(f"  {name:<16} skipped: no audio or run folder")
                continue
            wave, sr = sf.read(audio)
            wave = (wave.mean(axis=1) if getattr(wave, "ndim", 1) > 1 else wave).astype(np.float32)
            if sr != tf.SR:
                print(f"  {name:<16} skipped: {sr} Hz")
                continue
            spans, texts = tf.transcribe(model, processor, wave, device, args.batch, 28.0, "greedy")
            lines = []
            for (a, b), text in zip(spans, texts):
                if text:
                    s, e = int(a / tf.SR), int(b / tf.SR)
                    lines.append(f"[{s // 60}:{s % 60:02d}-{e // 60}:{e % 60:02d}] {text}")
            out = info["run_dir"] / args.out_name
            header = f"# LOSO transcript: {BASE} + {adapter.parent.name}/{adapter.name} (never heard lecturer {spk})\n"
            out.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
            print(f"  {name:<16} {len(wave) / tf.SR / 60:.1f} min, {len(lines)} chunks -> {out}")
        del model
        if device == "cuda":
            torch.cuda.empty_cache()
    return 0


if __name__ == "__main__":
    sys.exit(main())
