"""Render the real inputs our models receive, for the architecture figures.

A block diagram with a stock photo at the front says nothing about this project.
These are the actual tensors and files from our own data, so the figures show a
reader what the system really consumes:

  input-waveform.png   the waveform of one held-out test clip
  input-mel.png        the log-Mel spectrogram of that same clip, produced by
                       Whisper's own feature extractor, so it is literally the
                       array the encoder is given
  input-prompt.png     the transcript minutes and the board text that the
                       note-writing model receives, set as text

The clip is BanglaASR11/seg_000.wav, the first clip of the first held-out test
lecture, and the same one quoted in the figures and in RESULTS.md 1.10.

Two environments are needed because neither has everything: the fine-tuning
environment has transformers and soundfile but no matplotlib, and the figures
environment has matplotlib but no soundfile. So the arrays are extracted in one
and drawn in the other.

    <ft python>   scripts/make_example_inputs.py --stage extract
    <figs python> scripts/make_example_inputs.py --stage plot
"""
import argparse
import os
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
# seg_041 of lecture 11, 754 to 771 s. It is inside board era 5, the era whose board
# the vision figures use, and in it the lecturer reads out the very column of the truth
# table that box 2 of that board contains. So the audio, the frame, the rebuilt board and
# the note in the figures are all one moment of one lecture rather than four unrelated
# examples. Its character error rate is 24.5 per cent against the run's median of 15.8,
# so it is a slightly worse than typical clip, which is the safe direction to err in.
CLIP = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work_final5h")) / \
    "clips" / "BanglaASR11" / "seg_041.wav"
OUT = REPO / "Thesis Defense P3" / "drafts" / "thesis" / "images"
CACHE = Path(os.environ.get("TEMP", ".")) / "example_inputs"

# What the fine-tuned model actually produced for this clip, from eval_lr1e3.json, and
# the box names the vision model actually returned for era 5, from board_boxes.json.
# Neither is written for the figure.
TRANSCRIPT = ("so first ele ami pabo 0 0 equals to 0, 0 1 equals to 1, 1 0 equals "
              "to 1, 1 1 equals to 0. x or banano amar shesh. ekhon eitake ami not "
              "kore felbo. not mane ki? inverse ta baupar felbo.")
BOARD = ("box 2  \"Truth table\"\n"
         "       X-NOR gate: X-OR+NOT\n"
         "       A | B | A(+)B | A(+)B bar\n"
         "box 3  \"Gate symbol\"\n"
         "box 5  \"Formula\"\n"
         "       X-NOR -> A bar B bar + AB")


def extract():
    import numpy as np
    import soundfile as sf
    from transformers import WhisperFeatureExtractor

    CACHE.mkdir(parents=True, exist_ok=True)
    audio, sr = sf.read(str(CLIP))
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    np.save(CACHE / "wave.npy", audio.astype("float32"))

    fe = WhisperFeatureExtractor.from_pretrained(
        str(next((Path(os.environ["HF_HOME"]) / "hub" /
                  "models--openai--whisper-large-v3-turbo" / "snapshots").iterdir())))
    feats = fe(audio, sampling_rate=sr, return_tensors="np").input_features[0]
    np.save(CACHE / "mel.npy", feats)
    print("clip      %s" % CLIP)
    print("duration  %.2f s at %d Hz" % (len(audio) / sr, sr))
    print("mel shape %s (mel bins x frames), range %.2f to %.2f"
          % (feats.shape, feats.min(), feats.max()))
    print("cached in %s" % CACHE)


def plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    OUT.mkdir(parents=True, exist_ok=True)
    wave = np.load(CACHE / "wave.npy")
    mel = np.load(CACHE / "mel.npy")

    # Waveform: no axes, it is used as a picture of the input, not as a plot.
    fig, ax = plt.subplots(figsize=(4.0, 1.5))
    ax.plot(np.linspace(0, len(wave) / 16000, len(wave)), wave,
            linewidth=0.35, color="#2a6f8f")
    ax.set_xlim(0, len(wave) / 16000)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "input-waveform.png", dpi=260, transparent=True,
                bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)

    # Only the part of the 30 s window the clip actually fills is worth showing;
    # the rest is the padding Whisper adds and is flat.
    used = int(mel.shape[1] * min(1.0, (len(wave) / 16000) / 30.0))
    fig, ax = plt.subplots(figsize=(4.0, 2.6))
    ax.imshow(mel[:, :used], aspect="auto", origin="lower", cmap="magma")
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "input-mel.png", dpi=260, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    # The note model's input is text, so its "picture" is that text.
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.axis("off")
    ax.text(0.02, 0.97, "transcript for this board", fontsize=8.5, fontweight="bold",
            va="top", color="#1f2933", transform=ax.transAxes)
    ax.text(0.02, 0.86, TRANSCRIPT, fontsize=7.2, va="top", wrap=True,
            color="#3e4c59", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.35", fc="#eef2f6", ec="#cbd2d9", lw=0.6))
    ax.text(0.02, 0.50, "board text from the vision model", fontsize=8.5,
            fontweight="bold", va="top", color="#1f2933", transform=ax.transAxes)
    ax.text(0.02, 0.39, BOARD, fontsize=7.2, va="top", family="monospace",
            color="#3e4c59", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.35", fc="#f2f6ee", ec="#cbd2d9", lw=0.6))
    fig.savefig(OUT / "input-prompt.png", dpi=260, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    for f in ("input-waveform.png", "input-mel.png", "input-prompt.png"):
        print("  wrote %s" % (OUT / f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("extract", "plot"), required=True)
    args = ap.parse_args()
    return extract() if args.stage == "extract" else plot()


if __name__ == "__main__":
    sys.exit(main() or 0)
