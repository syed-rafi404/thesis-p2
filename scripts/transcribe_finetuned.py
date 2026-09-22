#!/usr/bin/env python
"""
=============================================================================
TRANSCRIBE WHOLE LECTURES WITH THE FINE-TUNED WHISPER
=============================================================================
finetune/evaluate.py scores the adapter on short held-out clips. The notes need
something different: a transcript of an entire lecture, in Banglish, written
next to the other pipeline outputs so scripts/regenerate_notes.py can use it.

Why this matters for the notes: the baseline transcript the summariser was fed
is Whisper's lossy English rendering, with lines like "tait gate involve" and
"9 gate" where the lecturer said NOR gate. With nothing real to work from, the
language model fell back on textbook memory. The fine-tuned transcript is the
lecturer's actual words, which is the raw material grounded notes need.

CHUNKING
--------
Whisper sees 30 seconds at a time. Cutting blindly every 28 seconds splits
words, so each boundary is moved to the quietest moment within a few seconds of
where it would fall, found from short-window audio energy. Speech pauses are
where energy drops, so cuts land between words.

RUNAWAY LOOPS
-------------
Both base and fine-tuned models occasionally loop, emitting a phrase dozens of
times: 18 of 137 held-out clips for the fine-tuned model. In a transcript that
feeds a summariser, one loop can dominate the notes. Loops are collapsed after
decoding: a phrase of two to twenty words repeated more than three times in a
row is cut back to two. The window has to be that wide: a real runaway from the
evaluation repeats a ten-word sentence, which an eight-word limit let through. A generation-time n-gram ban was rejected because the
lecturers legitimately repeat short phrases when reading out a truth table,
"0 plus 0, 0. 0 plus 1, 1", and a ban would corrupt exactly that. This is a
deployment decode setting; the reported WER and CER come from evaluate.py,
which does not apply it.

--no-adapter produces a base-model transcript with identical chunking and loop
handling, so that the fine-tune can be compared against its own base under
equal conditions rather than against a transcript produced some other way.

Usage:
    python scripts/transcribe_finetuned.py --run-dir <dir>
    python scripts/transcribe_finetuned.py --all
    python scripts/transcribe_finetuned.py --all --no-adapter --out-name transcript_base_small.txt
    python scripts/transcribe_finetuned.py --all --base openai/whisper-large-v3-turbo \\
        --adapter <ft_work>/lora_run
=============================================================================
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))
RUNS = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
sys.path.insert(0, str(REPO / "finetune"))

LANG, TASK = "en", "transcribe"      # must match train_lora.py
SR = 16000


def quiet_cuts(wave, chunk_s=28.0, search_s=3.0, frame_ms=30):
    """Chunk boundaries moved to the quietest point near each nominal cut."""
    import numpy as np
    frame = int(SR * frame_ms / 1000)
    n_frames = len(wave) // frame
    if n_frames == 0:
        return [(0, len(wave))]
    energy = np.sqrt(np.mean(
        wave[:n_frames * frame].reshape(n_frames, frame) ** 2, axis=1))
    cuts, pos = [0], 0
    step = int(chunk_s * SR)
    reach = int(search_s * SR)
    while pos + step < len(wave):
        target = pos + step
        lo, hi = max(pos + SR, target - reach), min(len(wave), target)
        f_lo, f_hi = lo // frame, max(lo // frame + 1, hi // frame)
        best = f_lo + int(np.argmin(energy[f_lo:f_hi])) if f_hi > f_lo else target // frame
        cut = best * frame
        if cut <= pos:
            cut = target
        cuts.append(cut)
        pos = cut
    cuts.append(len(wave))
    return list(zip(cuts[:-1], cuts[1:]))


LOOP = re.compile(r"\b((?:\S+\s+){1,19}?\S+)(?:[\s,.]+\1\b){3,}", re.IGNORECASE)


def collapse_loops(text):
    """Cut a phrase repeated more than three times running back to two copies."""
    prev = None
    while prev != text:
        prev = text
        text = LOOP.sub(lambda m: f"{m.group(1)} {m.group(1)}", text)
    return re.sub(r"\s+", " ", text).strip()


def load_model(base, adapter, device):
    import torch
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    dtype = torch.float16 if device == "cuda" else torch.float32
    if device == "cuda" and torch.cuda.is_bf16_supported():
        dtype = torch.bfloat16
    processor = WhisperProcessor.from_pretrained(base)
    processor.tokenizer.set_prefix_tokens(language=LANG, task=TASK)
    model = WhisperForConditionalGeneration.from_pretrained(base, torch_dtype=dtype)
    model.generation_config.language = LANG
    model.generation_config.task = TASK
    model.generation_config.forced_decoder_ids = None
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter).merge_and_unload()
    return model.to(device).eval(), processor


def _decode(model, processor, audio, device, **gen):
    import torch
    feats = processor.feature_extractor(
        audio, sampling_rate=SR, return_tensors="pt"
    ).input_features.to(device, dtype=model.dtype)
    with torch.no_grad():
        ids = model.generate(feats, language=LANG, task=TASK, max_new_tokens=200, **gen)
    return processor.batch_decode(ids, skip_special_tokens=True)


def transcribe(model, processor, wave, device, batch, chunk_s, decode="greedy"):
    """Greedy decode each chunk. decode="fallback" re-decodes looping chunks with
    Whisper's compression-ratio safeguard, the same one finetune/evaluate.py uses."""
    import torch
    spans = quiet_cuts(wave, chunk_s)
    texts = []
    for start in range(0, len(spans), batch):
        group = spans[start:start + batch]
        texts.extend(_decode(model, processor, [wave[a:b] for a, b in group], device,
                             do_sample=False))
        print(f"    {min(start + batch, len(spans))}/{len(spans)} chunks", end="\r", flush=True)
    print()
    if decode == "fallback":
        from evaluate import (COMPRESSION_RATIO_THRESHOLD, FALLBACK_SEED,
                              FALLBACK_TEMPERATURES, compression_ratio)
        for t in FALLBACK_TEMPERATURES:
            todo = [i for i, h in enumerate(texts)
                    if compression_ratio(h) > COMPRESSION_RATIO_THRESHOLD]
            if not todo:
                break
            torch.manual_seed(FALLBACK_SEED)
            for k in range(0, len(todo), batch):
                idx = todo[k:k + batch]
                redo = _decode(model, processor, [wave[spans[i][0]:spans[i][1]] for i in idx],
                               device, do_sample=True, temperature=t)
                for i, h in zip(idx, redo):
                    texts[i] = h
            print(f"    {len(todo)} looping chunks re-decoded at T={t}")
    return spans, [collapse_loops(t) for t in texts]


def main():
    ap = argparse.ArgumentParser(description="Transcribe whole lectures with the fine-tuned Whisper")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--base", default=str(FT_DIR / "models" / "whisper-small"))
    ap.add_argument("--adapter", default=str(FT_DIR / "lora_whisper_small"))
    ap.add_argument("--no-adapter", action="store_true",
                    help="Base model only, same chunking, for a like-for-like comparison")
    ap.add_argument("--chunk-s", type=float, default=28.0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--out-name", default="transcript_finetuned.txt")
    ap.add_argument("--timestamps", action="store_true",
                    help="Prefix each chunk with its [M:SS-M:SS] span")
    ap.add_argument("--decode", default="greedy", choices=("greedy", "fallback"),
                    help="fallback re-decodes looping chunks with Whisper's safeguard")
    ap.add_argument("--audio", default=None,
                    help="With --run-dir: transcribe this 16 kHz wav instead of looking the lecture "
                         "up by name (run_lecture.py, for a video outside the dataset)")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    if args.all:
        runs = [d for d in sorted(RUNS.iterdir()) if d.is_dir()]
    elif args.run_dir:
        runs = [Path(args.run_dir)]
    else:
        sys.exit("pass --run-dir <dir> or --all")

    import numpy as np
    import soundfile as sf
    import torch
    from prepare_data import find_audio

    device = "cuda" if torch.cuda.is_available() else "cpu"
    adapter = None if args.no_adapter else args.adapter
    if adapter and not Path(adapter).exists():
        sys.exit(f"adapter not found: {adapter}")
    print(f"base    : {args.base}")
    print(f"adapter : {adapter or '(none, base model only)'}")
    print(f"decode  : {args.decode}")
    print(f"device  : {device}\n")
    model, processor = load_model(args.base, adapter, device)

    for run_dir in runs:
        m = re.match(r"(BanglaASR\d+)", run_dir.name)
        stem = m.group(1) if m else run_dir.name
        audio_path = args.audio or find_audio(stem)
        if not audio_path:
            print(f"{run_dir.name:<18} skipped: no audio found for {stem}")
            continue
        wave, sr = sf.read(audio_path)
        if getattr(wave, "ndim", 1) > 1:
            wave = wave.mean(axis=1)
        if sr != SR:
            print(f"{run_dir.name:<18} skipped: {audio_path} is {sr} Hz, expected {SR}")
            continue
        wave = wave.astype(np.float32)
        print(f"{run_dir.name:<18} {len(wave)/SR/60:.1f} min of audio")
        spans, texts = transcribe(model, processor, wave, device, args.batch, args.chunk_s,
                                  args.decode)

        lines = []
        for (a, b), text in zip(spans, texts):
            if not text:
                continue
            if args.timestamps:
                s, e = int(a / SR), int(b / SR)
                lines.append(f"[{s//60}:{s%60:02d}-{e//60}:{e%60:02d}] {text}")
            else:
                lines.append(text)
        out = run_dir / args.out_name
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"                   {len(spans)} chunks -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
