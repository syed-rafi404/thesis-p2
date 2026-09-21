#!/usr/bin/env python
"""
=============================================================================
WHO IS SPEAKING IN EACH LECTURE? A MEASURED CHECK ON THE SPEAKER SPLIT
=============================================================================
The headline fine-tune claims its test speaker was never heard in training.
That claim is only as good as the speaker label on each lecture. The original
nine lectures carry no Speaker ID in their transcripts; the labels came from a
hand-written mapping in finetune/prepare_data.py.

This script checks the labels against the audio. It embeds clips from every
lecture with a speaker-verification model (WavLM x-vectors, trained for
exactly this) and reports:

    1. lecture-to-lecture cosine similarity of the mean voiceprint
    2. for each lecture, which other lecture its clips sit closest to
    3. the folder each video sits in under data/raw/, for comparison

Same speaker usually scores clearly higher than different speakers. The
numbers are evidence, not a verdict; the person who recorded the lectures
has the final word.

Usage:
    python scripts/verify_speakers.py
    python scripts/verify_speakers.py --clips-per-lecture 30
=============================================================================
"""

import argparse
import json
import os
import re
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))
OUT = REPO / "output" / "speaker_check"
MODEL = "microsoft/wavlm-base-plus-sv"
SR = 16000


def raw_folders():
    """Map lecture number to the folder its video sits in under data/raw."""
    found = {}
    raw = REPO / "data" / "raw"
    for path in raw.rglob("*"):
        m = re.fullmatch(r"BanglaASR(\d+)", path.stem)
        if m and path.is_file() and path.parent != raw:
            found[int(m.group(1))] = path.parent.name
    return found


def pick_clips(lecture_dir, n, min_s, max_s):
    """Evenly spaced clips across the lecture, trimmed to max_s seconds."""
    wavs = sorted(lecture_dir.glob("seg_*.wav"))
    usable = []
    for w in wavs:
        info = sf.info(str(w))
        if info.frames / info.samplerate >= min_s:
            usable.append(w)
    if len(usable) > n:
        idx = np.linspace(0, len(usable) - 1, n).round().astype(int)
        usable = [usable[i] for i in idx]
    out = []
    for w in usable:
        audio, sr = sf.read(str(w), dtype="float32")
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        assert sr == SR, f"{w} is {sr} Hz, expected {SR}"
        out.append(audio[: int(max_s * SR)])
    return out


def main():
    ap = argparse.ArgumentParser(description="Check lecture speaker labels against the audio")
    ap.add_argument("--clips-dir", default=str(FT_DIR / "clips"))
    ap.add_argument("--clips-per-lecture", type=int, default=20)
    ap.add_argument("--min-s", type=float, default=6.0, help="Skip clips shorter than this")
    ap.add_argument("--max-s", type=float, default=15.0, help="Trim clips to this length")
    args = ap.parse_args()

    from transformers import AutoFeatureExtractor, WavLMForXVector

    device = "cuda" if torch.cuda.is_available() else "cpu"
    extractor = AutoFeatureExtractor.from_pretrained(MODEL)
    model = WavLMForXVector.from_pretrained(MODEL).to(device).eval()

    clips_dir = Path(args.clips_dir)
    lectures = sorted((int(m.group(1)), d) for d in clips_dir.iterdir()
                      if d.is_dir() and (m := re.fullmatch(r"BanglaASR(\d+)", d.name)))
    folders = raw_folders()

    emb = {}
    for n, d in lectures:
        vecs = []
        for audio in pick_clips(d, args.clips_per_lecture, args.min_s, args.max_s):
            inputs = extractor(audio, sampling_rate=SR, return_tensors="pt").to(device)
            with torch.no_grad():
                v = model(**inputs).embeddings[0]
            vecs.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
        emb[n] = np.stack(vecs)
        print(f"BanglaASR{n}: {len(vecs)} clips embedded")

    ids = [n for n, _ in lectures]
    cent = {n: emb[n].mean(axis=0) / np.linalg.norm(emb[n].mean(axis=0)) for n in ids}
    sim = np.array([[float(cent[a] @ cent[b]) for b in ids] for a in ids])

    # For each lecture: which OTHER lecture do its individual clips sit closest to?
    nearest = {}
    for a in ids:
        votes = {}
        for v in emb[a]:
            best = max((b for b in ids if b != a), key=lambda b: float(v @ cent[b]))
            votes[best] = votes.get(best, 0) + 1
        nearest[a] = dict(sorted(votes.items(), key=lambda kv: -kv[1]))

    lines = ["# Speaker check: which lectures share a voice", "",
             f"Model `{MODEL}`, {args.clips_per_lecture} clips per lecture "
             f"({args.min_s:.0f}-{args.max_s:.0f} s), cosine similarity of the mean "
             "x-vector. Higher means more alike.", "",
             "| | " + " | ".join(str(b) for b in ids) + " | data/raw folder |",
             "|---|" + "---|" * len(ids) + "---|"]
    for i, a in enumerate(ids):
        row = " | ".join(("**1.00**" if a == b else f"{sim[i, j]:.2f}")
                         for j, b in enumerate(ids))
        lines.append(f"| {a} | {row} | {folders.get(a, '-')} |")
    lines += ["", "## Closest other lecture, per clip", ""]
    for a in ids:
        top = ", ".join(f"{b} ({c})" for b, c in nearest[a].items())
        lines.append(f"- BanglaASR{a} ({folders.get(a, '-')}): {top}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "speaker_similarity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "speaker_similarity.json").write_text(json.dumps({
        "model": MODEL, "lectures": ids, "similarity": sim.round(4).tolist(),
        "nearest_votes": {str(k): {str(b): c for b, c in v.items()} for k, v in nearest.items()},
        "raw_folders": {str(k): v for k, v in folders.items()},
    }, indent=2), encoding="utf-8")
    print("\n" + "\n".join(lines))
    print(f"\nwrote {OUT / 'speaker_similarity.md'}")


if __name__ == "__main__":
    main()
