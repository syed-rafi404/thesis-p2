#!/usr/bin/env python
"""
=============================================================================
WHICH LECTURER IS IN EACH VIDEO? VOICEPRINTS FOR EVERY VIDEO, WITH OR WITHOUT GROUND TRUTH
=============================================================================
verify_speakers.py needs transcribed clips, so it cannot look at videos that have no ground
truth yet. This samples the audio directly: up to --windows evenly spaced 8 s windows per
video (the quietest fifth dropped), embeds each with the same speaker-verification model
(microsoft/wavlm-base-plus-sv), and averages them into one voiceprint per video.

Three reference lecturers, from videos whose lecturer is already established (new numbering,
2026-09-22): A = lectures 1-5, B = 10-13, C = 14-17 (verify_speakers.py confirmed the old
labels behind these on 2026-09-21). Every video is compared with each reference (a reference
video is compared with the others of its lecturer, never with itself). A video whose best
similarity is low for all three may be a fourth lecturer. The numbers are evidence; the person
who recorded the lectures has the final word.

Writes output/speaker_check/speaker_groups.json and .md; check_new_data.py compares each
ground-truth file's "# Speaker ID:" with this.

    python scripts/speaker_groups.py
=============================================================================
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
sys.path.insert(0, str(REPO / "finetune"))
from prepare_data import VIDEO_EXTS, find_audio                       # noqa: E402

MODEL = "microsoft/wavlm-base-plus-sv"
SAFETENSORS_PR = "refs/pr/8"            # SFconvertbot's safetensors copy, for torch < 2.6
SR = 16000
REFERENCES = {"A": range(1, 6), "B": range(10, 14), "C": range(14, 18)}
OUT = REPO / "output" / "speaker_check"


def windows(wave, n, win_s=8.0):
    w = int(win_s * SR)
    if len(wave) < w:
        return [wave]
    starts = np.linspace(0, len(wave) - w, num=max(n, 1) + 2)[1:-1].astype(int)
    chunks = [wave[s:s + w] for s in starts]
    rms = np.array([np.sqrt(np.mean(c ** 2)) for c in chunks])
    keep = rms >= np.percentile(rms, 20)
    return [c for c, k in zip(chunks, keep) if k]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--windows", type=int, default=16)
    ap.add_argument("--audio-dir", default=None, help="Old-numbered wavs, as for prepare_data.py")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    import torch
    from transformers import AutoFeatureExtractor, WavLMForXVector
    device = "cuda" if torch.cuda.is_available() else "cpu"
    extractor = AutoFeatureExtractor.from_pretrained(MODEL)
    # The model's main branch has only pytorch_model.bin, which transformers refuses to load on
    # torch < 2.6 (CVE-2025-32434); the 3060 must stay on torch 2.5.1. Hugging Face's own
    # conversion bot (SFconvertbot) published the same weights as safetensors in refs/pr/8.
    major, minor = (int(x) for x in torch.__version__.split(".")[:2])
    revision = {} if (major, minor) >= (2, 6) else {"revision": SAFETENSORS_PR, "use_safetensors": True}
    model = WavLMForXVector.from_pretrained(MODEL, **revision).to(device).eval()

    videos = {}
    for root, _d, files in os.walk(REPO / "data" / "raw"):
        for f in files:
            base, ext = os.path.splitext(f)
            m = re.fullmatch(r"BanglaASR(\d+)", base)
            if m and ext in VIDEO_EXTS and "screen_recorded" not in root:
                videos[int(m.group(1))] = base
    prints = {}
    for n in sorted(videos):
        stem = videos[n]
        wav = find_audio(stem, args.audio_dir, "new")
        if not wav:
            print(f"{stem:<14} no audio")
            continue
        wave, sr = sf.read(wav, dtype="float32")
        if wave.ndim > 1:
            wave = wave.mean(axis=1)
        chunks = windows(wave, args.windows)
        with torch.no_grad():
            feats = extractor(chunks, sampling_rate=SR, return_tensors="pt", padding=True).to(device)
            emb = model(**feats).embeddings
            emb = torch.nn.functional.normalize(emb, dim=-1).mean(0)
        prints[stem] = torch.nn.functional.normalize(emb, dim=-1).cpu().numpy()
        print(f"{stem:<14} {len(wave) / SR / 60:5.1f} min, {len(chunks)} windows")

    def centroid(label, exclude=None):
        vs = [prints[f"BanglaASR{i}"] for i in REFERENCES[label]
              if f"BanglaASR{i}" in prints and f"BanglaASR{i}" != exclude]
        c = np.mean(vs, axis=0)
        return c / np.linalg.norm(c)

    result = {}
    for stem, v in prints.items():
        sims = {lab: float(np.dot(v, centroid(lab, exclude=stem))) for lab in REFERENCES}
        ranked = sorted(sims.items(), key=lambda kv: -kv[1])
        result[stem] = {"best": ranked[0][0], "similarity": round(ranked[0][1], 3),
                        "margin": round(ranked[0][1] - ranked[1][1], 3),
                        "sims": {k: round(s, 3) for k, s in sims.items()}}

    ref_of = {f"BanglaASR{i}": lab for lab, r in REFERENCES.items() for i in r}
    lines = ["# Which lecturer is in each video (voiceprints, 2026-09-22)", "",
             f"Model {MODEL}; references A = 1-5, B = 10-13, C = 14-17 (new numbering); up to "
             f"{args.windows} 8 s windows per video. Same lecturer typically scores clearly higher "
             "than a different one; low best similarity for all three may mean a fourth lecturer.", "",
             "| Video | Best match | Similarity | Margin over next | A | B | C | Note |",
             "|---|---|---|---|---|---|---|---|"]
    for stem in sorted(result, key=lambda s: int(re.search(r"\d+", s).group())):
        r = result[stem]
        note = []
        if stem in ref_of:
            note.append("reference" + ("" if ref_of[stem] == r["best"] else f", DISAGREES with {ref_of[stem]}"))
        if r["margin"] < 0.05:
            note.append("unsure")
        if r["similarity"] < 0.85:
            note.append("unlike all three")
        lines.append(f"| {stem} | {r['best']} | {r['similarity']:.3f} | {r['margin']:.3f} | "
                     f"{r['sims']['A']:.3f} | {r['sims']['B']:.3f} | {r['sims']['C']:.3f} | {', '.join(note)} |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "speaker_groups.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "speaker_groups.json").write_text(json.dumps({"model": MODEL, "references": {
        k: list(v) for k, v in REFERENCES.items()}, "lectures": result}, indent=2), encoding="utf-8")
    print("\n" + "\n".join(lines[5:]))
    print(f"\nwrote {OUT / 'speaker_groups.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
