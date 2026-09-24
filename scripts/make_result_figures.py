#!/usr/bin/env python
"""
Thesis figures for the 2026-09 results, computed from the evaluation files, never typed in.

Needs matplotlib, which is in the isolated environment made for this on 2026-09-24
(`F:\\thesisP2\\envs\\figs\\Scripts\\python.exe`); neither working environment has it.

    <figs python> scripts/make_result_figures.py

Writes fig_asr_final.png/.pdf into P2/figures/ beside the older February figures, which belong to
the P2 pipeline and say nothing about these results.
"""
import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("THESIS_FIGURES") or REPO / "P2" / "figures")
FINAL_1E3 = REPO.parent / "ft_work_final5h_lr1e3"
FINAL_2E3 = REPO.parent / "ft_work_final5h"

INK = "#1f2933"
BASE_C = "#9aa5b1"
GOOD_C = "#2a9d4f"
BAD_C = "#d62828"


def read(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"cer": 100 * d["tuned"]["cer_median_per_clip"], "wer": 100 * d["tuned"]["wer_median_per_clip"],
            "base_cer": 100 * d["base"]["cer_median_per_clip"], "base_wer": 100 * d["base"]["wer_median_per_clip"],
            "clips": d["tuned"]["clips"], "runaway": d["tuned"].get("runaway_clips"),
            "base_runaway": d["base"].get("runaway_clips")}


def asr_figure(show_diverged=True):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a = read(FINAL_1E3 / "eval_lr1e3.json")
    b = read(FINAL_1E3 / "eval_lr1e3_s1.json")
    bad = read(FINAL_2E3 / "eval_final.json") if show_diverged else None

    labels = ["Off-the-shelf\nWhisper", "Fine-tuned\nseed 42", "Fine-tuned\nseed 1"]
    cer = [a["base_cer"], a["cer"], b["cer"]]
    wer = [a["base_wer"], a["wer"], b["wer"]]
    colours = [BASE_C, GOOD_C, GOOD_C]
    if bad:
        labels.append("Tuned rate 2e-3,\nseed 42 (diverged)")
        cer.append(bad["cer"])
        wer.append(bad["wer"])
        colours.append(BAD_C)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, vals, name in ((axes[0], cer, "Character error rate"), (axes[1], wer, "Word error rate")):
        bars = ax.bar(range(len(vals)), vals, color=colours, width=0.62, edgecolor="white")
        for x, v in zip(range(len(vals)), vals):
            ax.text(x, v + 2, f"{v:.1f}%", ha="center", va="bottom", fontsize=10,
                    fontweight="bold", color=INK)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylabel(f"{name}, median per clip (%)", fontsize=10)
        ax.set_ylim(0, max(vals) * 1.18)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.axhline(vals[0], color=BASE_C, linestyle="--", linewidth=1, alpha=0.8)
    fig.suptitle(f"Banglish ASR: {a['clips']} clips from six lectures held out of training "
                 f"(4.10 h of training speech)", fontsize=11.5, fontweight="bold", color=INK)
    note = ("Lower is better. Both stable seeds use learning rate 1e-3. The red bar is the rate the "
            "pre-registered tuning chose (2e-3): its other seed reached 16.2%, this one collapsed "
            "into repetition loops on 82 of 177 clips.")
    fig.text(0.5, -0.02, note, ha="center", va="top", fontsize=8.5, color="#52606d", wrap=True)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_asr_final.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / 'fig_asr_final.png'} and .pdf")
    print(f"  from {FINAL_1E3.name}: base CER {a['base_cer']:.1f} -> {a['cer']:.1f} / {b['cer']:.1f}")
    if bad:
        print(f"  diverged run: CER {bad['cer']:.1f}, {bad['runaway']} runaway clips of {bad['clips']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-diverged", action="store_true", help="leave the collapsed seed out")
    args = ap.parse_args()
    asr_figure(show_diverged=not args.no_diverged)
    return 0


if __name__ == "__main__":
    sys.exit(main())
