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


# ---------------------------------------------------------------------------
# The dataset, read from data/ground_truth and the extracted audio
# ---------------------------------------------------------------------------

TS = None


def lecture_stats():
    """Per lecture: lecturer, transcribed minutes, segment durations, word count.

    Timestamps come from the ground truth itself, so the figures cannot drift from the data the
    model trained on. Lectures with no ground truth contribute their audio duration only, taken
    from the 16 kHz mono wav (32000 bytes a second) that transcription left behind.
    """
    import re
    global TS
    TS = TS or re.compile(r"^\[(\d+):(\d{2})\s*-\s*(\d+):(\d{2})\]\s*(.*)$")
    out = {}
    for path in sorted((REPO / "data" / "ground_truth").glob("BanglaASR*_ground_truth.txt")):
        n = int(re.match(r"BanglaASR(\d+)", path.name).group(1))
        speaker, segs, words = "?", [], 0
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# Speaker ID:"):
                speaker = line.split(":", 1)[1].strip()
            m = TS.match(line.strip())
            if m:
                a = int(m.group(1)) * 60 + int(m.group(2))
                b = int(m.group(3)) * 60 + int(m.group(4))
                if b > a:
                    segs.append(b - a)
                words += len(m.group(5).split())
        out[n] = {"speaker": speaker, "segments": segs, "minutes": sum(segs) / 60, "words": words,
                  "has_gt": True}
    # The lecturer of an untranscribed lecture comes from the voice check, not from a guess.
    voice_path = REPO / "output" / "speaker_check" / "speaker_groups.json"
    voice = json.loads(voice_path.read_text(encoding="utf-8"))["lectures"] if voice_path.exists() else {}
    for d in sorted((REPO / "output" / "lectures").glob("BanglaASR*")):
        n = int(re.match(r"BanglaASR(\d+)", d.name).group(1))
        wav = d / "audio.wav"
        if n not in out and wav.exists():
            out[n] = {"speaker": voice.get(d.name, {}).get("best", "?"), "segments": [],
                      "minutes": wav.stat().st_size / 32000 / 60, "words": 0, "has_gt": False}
    return dict(sorted(out.items()))


# The three folders that hold the boards in use. Sweeping output/** instead pulls in superseded
# runs (all9 before the learned mask, the speaker3_2s test folders) and counts 263 boards where
# the thesis has 143: 35 for lectures 1-9, 10 for 10-13, and 98 for the newer lectures.
BOARD_ROOTS = [REPO / "output" / "annotation_demo" / "all9_deeplab_shadow",
               REPO / "output" / "annotation_demo" / "speaker3_2s_deeplab_shadow",
               REPO / "output" / "lectures"]


def board_stats():
    """Per lecture: how many boards, and each board's fully-clear tile fraction."""
    import re
    rows, seen = [], set()
    for root in BOARD_ROOTS:
        for mos in sorted(root.glob("**/mosaic.json")):
            if "pass1" in mos.parts or "clean" in mos.parts:
                continue
            m = re.search(r"BanglaASR(\d+)", mos.parent.name)
            if not m:
                continue
            n = int(m.group(1))
            key = (root.name, n)
            if key in seen:
                continue
            seen.add(key)
            try:
                eras = json.loads(mos.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            eras = eras if isinstance(eras, list) else eras.get("eras", [])
            for e in eras:
                if isinstance(e, dict):
                    rows.append({"lecture": n, "set": root.name, "clear": e.get("clear_fraction")})
    return rows


def dataset_figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    stats = lecture_stats()
    split = json.loads((FINAL_2E3 / "split.json").read_text(encoding="utf-8"))
    test = {int(s.replace("BanglaASR", "")) for s in split.get("test_lectures", [])}
    colours = {"A": "#1d4ed8", "B": "#f77f00", "C": "#2a9d4f"}

    # 1. hours per lecturer, split three ways
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    kinds = [("train", "in training", 0.95), ("test", "held out for testing", 0.6),
             ("none", "no transcript (vision only)", 0.25)]
    bottoms = {s: 0.0 for s in "ABC"}
    for key, label, alpha in kinds:
        vals = []
        for s in "ABC":
            h = sum(v["minutes"] / 60 for n, v in stats.items()
                    if v["speaker"] == s and ((key == "none" and not v["has_gt"])
                                              or (key == "test" and v["has_gt"] and n in test)
                                              or (key == "train" and v["has_gt"] and n not in test)))
            vals.append(h)
        ax.bar(list("ABC"), vals, bottom=[bottoms[s] for s in "ABC"], label=label,
               color=[colours[s] for s in "ABC"], alpha=alpha, edgecolor="white")
        for s, v in zip("ABC", vals):
            if v > 0.15:
                ax.text("ABC".index(s), bottoms[s] + v / 2, f"{v:.1f} h", ha="center", va="center",
                        fontsize=9, color="white", fontweight="bold")
            bottoms[s] += v
    ax.set_xlabel("Lecturer")
    ax.set_ylabel("Hours of video")
    ax.set_title(f"The dataset: {sum(v['minutes'] for v in stats.values() if v['has_gt'])/60:.2f} h "
                 f"transcribed of {sum(v['minutes'] for v in stats.values())/60:.1f} h recorded",
                 fontsize=11.5, fontweight="bold", color=INK)
    ax.legend(fontsize=9, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_data_composition.{ext}", dpi=300)
    plt.close(fig)

    # 2. segment lengths, against the 30 s window
    segs = [d for v in stats.values() for d in v["segments"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.hist(segs, bins=range(0, max(segs) + 5, 2), color="#1d4ed8", alpha=0.85, edgecolor="white")
    ax.axvline(30, color=BAD_C, linestyle="--", linewidth=1.4)
    ax.text(31, ax.get_ylim()[1] * 0.92, "Whisper's 30 s window\n(longer segments are split at\n"
            "sentence ends before training)", color=BAD_C, fontsize=8.5, va="top")
    over = sum(1 for d in segs if d > 30)
    ax.set_xlabel("Segment length (seconds)")
    ax.set_ylabel("Segments")
    ax.set_title(f"{len(segs)} transcribed segments, median {sorted(segs)[len(segs)//2]} s, "
                 f"{over} over 30 s", fontsize=11.5, fontweight="bold", color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_data_segments.{ext}", dpi=300)
    plt.close(fig)

    # 3. per lecture: transcribed minutes and speaking rate
    fig, axes = plt.subplots(2, 1, figsize=(10, 6.4), sharex=True)
    keyed = [(n, v) for n, v in stats.items() if v["has_gt"]]
    xs = range(len(keyed))
    axes[0].bar(xs, [v["minutes"] for _, v in keyed],
                color=[colours.get(v["speaker"], "#9aa5b1") for _, v in keyed], edgecolor="white")
    for x, (n, _) in zip(xs, keyed):
        if n in test:
            axes[0].text(x, 0.4, "test", rotation=90, fontsize=7, color="white", ha="center", va="bottom")
    axes[0].set_ylabel("Transcribed minutes")
    axes[0].set_title("Per lecture: length and speaking rate (bar colour is the lecturer)",
                      fontsize=11.5, fontweight="bold", color=INK)
    axes[1].bar(xs, [v["words"] / max(v["minutes"], 0.01) for _, v in keyed],
                color=[colours.get(v["speaker"], "#9aa5b1") for _, v in keyed], edgecolor="white")
    axes[1].set_ylabel("Words per minute")
    axes[1].set_xticks(list(xs))
    axes[1].set_xticklabels([f"{n}" for n, _ in keyed], fontsize=8)
    axes[1].set_xlabel("Lecture")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_data_per_lecture.{ext}", dpi=300)
    plt.close(fig)

    # 4. the boards
    boards = board_stats()
    clear = [100 * b["clear"] for b in boards if b["clear"] is not None]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    per = {}
    for b in boards:
        per[b["lecture"]] = per.get(b["lecture"], 0) + 1
    axes[0].bar(range(len(per)), [per[k] for k in sorted(per)], color="#7b2cbf", edgecolor="white")
    axes[0].set_xticks(range(len(per)))
    axes[0].set_xticklabels([str(k) for k in sorted(per)], fontsize=7, rotation=90)
    axes[0].set_xlabel("Lecture")
    axes[0].set_ylabel("Boards (erase-separated eras)")
    axes[0].set_title(f"{len(boards)} boards across {len(per)} lectures", fontsize=11,
                      fontweight="bold", color=INK)
    axes[1].hist(clear, bins=20, color="#2a9d4f", alpha=0.85, edgecolor="white")
    axes[1].axvline(sorted(clear)[len(clear) // 2], color=INK, linestyle="--", linewidth=1.2)
    axes[1].text(sorted(clear)[len(clear) // 2] - 1, axes[1].get_ylim()[1] * 0.9,
                 f"median {sorted(clear)[len(clear)//2]:.1f}%", ha="right", fontsize=9, color=INK)
    axes[1].set_xlabel("Tiles fully clear of the lecturer (%)")
    axes[1].set_ylabel("Boards")
    axes[1].set_title("Reconstruction quality per board", fontsize=11, fontweight="bold", color=INK)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_data_boards.{ext}", dpi=300)
    plt.close(fig)

    print(f"dataset figures written to {OUT}")
    print(f"  lectures with ground truth {sum(1 for v in stats.values() if v['has_gt'])}, "
          f"total recorded {sum(v['minutes'] for v in stats.values())/60:.1f} h")
    print(f"  segments {len(segs)}, over 30 s {over}")
    print(f"  boards {len(boards)}, median clear {sorted(clear)[len(clear)//2]:.1f}%")


# ---------------------------------------------------------------------------
# The ASR result in detail, from the per-clip records the evaluator saves
# ---------------------------------------------------------------------------

def asr_detail_figures():
    """Three views the headline bars cannot give: the spread, who wins clip by clip, per lecture."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads((FINAL_1E3 / "eval_lr1e3.json").read_text(encoding="utf-8"))
    base = {r["audio"]: r for r in d["per_clip"]["base"]}
    tuned = {r["audio"]: r for r in d["per_clip"]["tuned"]}
    keys = [k for k in base if k in tuned]
    bx = [100 * base[k]["cer"] for k in keys]
    tx = [100 * tuned[k]["cer"] for k in keys]

    # 1. the distribution, not just the median
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    bins = range(0, 210, 10)
    ax.hist([min(v, 200) for v in bx], bins=bins, color=BASE_C, alpha=0.75,
            label="Off-the-shelf Whisper", edgecolor="white")
    ax.hist([min(v, 200) for v in tx], bins=bins, color=GOOD_C, alpha=0.8,
            label="Fine-tuned", edgecolor="white")
    ax.set_xlabel("Character error rate of one clip (%), capped at 200")
    ax.set_ylabel("Clips")
    ax.set_title(f"Error spread over {len(keys)} held-out clips, not just the median",
                 fontsize=11.5, fontweight="bold", color=INK)
    ax.legend(frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_asr_distribution.{ext}", dpi=300)
    plt.close(fig)

    # 2. clip by clip: below the diagonal is an improvement
    fig, ax = plt.subplots(figsize=(5.8, 5.6))
    better = sum(1 for a, b in zip(bx, tx) if b < a)
    ax.scatter([min(v, 200) for v in bx], [min(v, 200) for v in tx], s=18, alpha=0.55,
               color="#1d4ed8", edgecolors="none")
    lim = 205
    ax.plot([0, lim], [0, lim], color=INK, linewidth=1, linestyle="--")
    ax.text(lim * 0.52, lim * 0.6, "worse after\nfine-tuning", fontsize=9, color="#52606d")
    ax.text(lim * 0.45, lim * 0.12, f"better: {better} of {len(keys)} clips", fontsize=9.5,
            color=GOOD_C, fontweight="bold")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("Off-the-shelf error (%)")
    ax.set_ylabel("Fine-tuned error (%)")
    ax.set_title("Every held-out clip, before and after", fontsize=11.5, fontweight="bold", color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.2, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_asr_clip_scatter.{ext}", dpi=300)
    plt.close(fig)

    # 3. per test lecture, so no single lecture can be carrying the result
    per = {}
    for k in keys:
        n = base[k]["video"]
        per.setdefault(n, {"base": [], "tuned": [], "speaker": base[k]["speaker"]})
        per[n]["base"].append(100 * base[k]["cer"])
        per[n]["tuned"].append(100 * tuned[k]["cer"])
    med = lambda xs: sorted(xs)[len(xs) // 2]
    order = sorted(per)
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    w = 0.38
    ax.bar([i - w / 2 for i in range(len(order))], [med(per[n]["base"]) for n in order], w,
           color=BASE_C, label="Off-the-shelf", edgecolor="white")
    ax.bar([i + w / 2 for i in range(len(order))], [med(per[n]["tuned"]) for n in order], w,
           color=GOOD_C, label="Fine-tuned", edgecolor="white")
    for i, n in enumerate(order):
        ax.text(i + w / 2, med(per[n]["tuned"]) + 1.5, f"{med(per[n]['tuned']):.0f}", ha="center",
                fontsize=8.5, color=INK)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([f"BanglaASR{n}\nlecturer {per[n]['speaker']}\n{len(per[n]['base'])} clips"
                        for n in order], fontsize=8)
    ax.set_ylabel("Median character error rate (%)")
    ax.set_title("Each held-out lecture on its own: all six improve, lecturer B's by far the least",
                 fontsize=11.5, fontweight="bold", color=INK)
    ax.legend(frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_asr_per_lecture.{ext}", dpi=300)
    plt.close(fig)

    print("asr detail figures written")
    print(f"  clips {len(keys)}, better after fine-tuning {better}")
    print("  per lecture medians: " + ", ".join(f"{n} {med(per[n]['base']):.0f}->{med(per[n]['tuned']):.0f}"
                                                for n in order))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", default="all", choices=("all", "asr", "dataset", "asr-detail"))
    ap.add_argument("--no-diverged", action="store_true", help="leave the collapsed seed out")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.set in ("all", "asr"):
        asr_figure(show_diverged=not args.no_diverged)
    if args.set in ("all", "dataset"):
        dataset_figures()
    if args.set in ("all", "asr-detail"):
        asr_detail_figures()
    return 0


if __name__ == "__main__":
    sys.exit(main())

