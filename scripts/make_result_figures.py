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


def wrapnote(text, width=84):
    """Break a figure footnote into short lines.

    Saved with bbox_inches="tight", a long single-line note widens the figure's
    bounding box far beyond the plot, which then has to be scaled down to fit the
    page and takes the whole figure with it.
    """
    import textwrap
    return textwrap.fill(text, width=width)


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

    fig, axes = plt.subplots(2, 1, figsize=(6.6, 6.2))
    for ax, vals, name in ((axes[0], cer, "Character error rate"), (axes[1], wer, "Word error rate")):
        bars = ax.bar(range(len(vals)), vals, color=colours, width=0.62, edgecolor="white")
        for x, v in zip(range(len(vals)), vals):
            ax.text(x, v + 2, f"{v:.1f}%", ha="center", va="bottom", fontsize=11.5,
                    fontweight="bold", color=INK)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10.5)
        ax.set_ylabel(f"{name} (%)", fontsize=11.5)
        ax.set_ylim(0, max(vals) * 1.18)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.axhline(vals[0], color=BASE_C, linestyle="--", linewidth=1, alpha=0.8)
    fig.suptitle(wrapnote(f"Banglish ASR: {a['clips']} clips from six lectures held out "
                          f"of training (4.10 h of training speech)", 58),
                 fontsize=13, fontweight="bold", color=INK)
    note = ("Lower is better. Both stable seeds use learning rate 1e-3. The red bar is the rate the "
            "pre-registered tuning chose (2e-3): its other seed reached 16.2%, this one collapsed "
            "into repetition loops on 82 of 177 clips.")
    fig.text(0.5, -0.02, wrapnote(note), ha="center", va="top", fontsize=10, color="#52606d")
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
                        fontsize=10.5, color="white", fontweight="bold")
            bottoms[s] += v
    ax.set_xlabel("Lecturer")
    ax.set_ylabel("Hours of video")
    ax.set_title(f"The dataset: {sum(v['minutes'] for v in stats.values() if v['has_gt'])/60:.2f} h "
                 f"transcribed of {sum(v['minutes'] for v in stats.values())/60:.1f} h recorded",
                 fontsize=13, fontweight="bold", color=INK)
    ax.legend(fontsize=10.5, frameon=False)
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
            "sentence ends before training)", color=BAD_C, fontsize=10, va="top")
    over = sum(1 for d in segs if d > 30)
    ax.set_xlabel("Segment length (seconds)")
    ax.set_ylabel("Segments")
    ax.set_title(f"{len(segs)} transcribed segments, median {sorted(segs)[len(segs)//2]} s, "
                 f"{over} over 30 s", fontsize=13, fontweight="bold", color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_data_segments.{ext}", dpi=300)
    plt.close(fig)

    # 3. per lecture: transcribed minutes and speaking rate
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.0), sharex=True)
    keyed = [(n, v) for n, v in stats.items() if v["has_gt"]]
    xs = range(len(keyed))
    axes[0].bar(xs, [v["minutes"] for _, v in keyed],
                color=[colours.get(v["speaker"], "#9aa5b1") for _, v in keyed], edgecolor="white")
    for x, (n, _) in zip(xs, keyed):
        if n in test:
            axes[0].text(x, 0.4, "test", rotation=90, fontsize=8.5, color="white", ha="center", va="bottom")
    axes[0].set_ylabel("Transcribed minutes")
    axes[0].set_title("Per lecture: length and speaking rate (bar colour is the lecturer)",
                      fontsize=13, fontweight="bold", color=INK)
    axes[1].bar(xs, [v["words"] / max(v["minutes"], 0.01) for _, v in keyed],
                color=[colours.get(v["speaker"], "#9aa5b1") for _, v in keyed], edgecolor="white")
    axes[1].set_ylabel("Words per minute")
    axes[1].set_xticks(list(xs))
    axes[1].set_xticklabels([f"{n}" for n, _ in keyed], fontsize=9.5)
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
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.2))
    per = {}
    for b in boards:
        per[b["lecture"]] = per.get(b["lecture"], 0) + 1
    axes[0].bar(range(len(per)), [per[k] for k in sorted(per)], color="#7b2cbf", edgecolor="white")
    axes[0].set_xticks(range(len(per)))
    axes[0].set_xticklabels([str(k) for k in sorted(per)], fontsize=8.5, rotation=90)
    axes[0].set_xlabel("Lecture")
    axes[0].set_ylabel("Boards (erase-separated eras)")
    axes[0].set_title(f"{len(boards)} boards across {len(per)} lectures", fontsize=12.5,
                      fontweight="bold", color=INK)
    axes[1].hist(clear, bins=20, color="#2a9d4f", alpha=0.85, edgecolor="white")
    axes[1].axvline(sorted(clear)[len(clear) // 2], color=INK, linestyle="--", linewidth=1.2)
    axes[1].text(sorted(clear)[len(clear) // 2] - 1, axes[1].get_ylim()[1] * 0.9,
                 f"median {sorted(clear)[len(clear)//2]:.1f}%", ha="right", fontsize=10.5, color=INK)
    axes[1].set_xlabel("Tiles fully clear of the lecturer (%)")
    axes[1].set_ylabel("Boards")
    axes[1].set_title("Reconstruction quality per board", fontsize=12.5, fontweight="bold", color=INK)
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
                 fontsize=13, fontweight="bold", color=INK)
    ax.legend(frameon=False, fontsize=10.5)
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
    ax.text(lim * 0.52, lim * 0.6, "worse after\nfine-tuning", fontsize=10.5, color="#52606d")
    ax.text(lim * 0.45, lim * 0.12, f"better: {better} of {len(keys)} clips", fontsize=11,
            color=GOOD_C, fontweight="bold")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("Off-the-shelf error (%)")
    ax.set_ylabel("Fine-tuned error (%)")
    ax.set_title("Every held-out clip, before and after", fontsize=13, fontweight="bold", color=INK)
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
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    w = 0.38
    ax.bar([i - w / 2 for i in range(len(order))], [med(per[n]["base"]) for n in order], w,
           color=BASE_C, label="Off-the-shelf", edgecolor="white")
    ax.bar([i + w / 2 for i in range(len(order))], [med(per[n]["tuned"]) for n in order], w,
           color=GOOD_C, label="Fine-tuned", edgecolor="white")
    for i, n in enumerate(order):
        ax.text(i + w / 2, med(per[n]["tuned"]) + 1.5, f"{med(per[n]['tuned']):.0f}", ha="center",
                fontsize=10, color=INK)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([f"BanglaASR{n}\nlecturer {per[n]['speaker']}\n{len(per[n]['base'])} clips"
                        for n in order], fontsize=9.5)
    ax.set_ylabel("Median character error rate (%)")
    ax.set_title("Each held-out lecture on its own: all six improve, lecturer B's by far the least",
                 fontsize=13, fontweight="bold", color=INK)
    ax.legend(frameon=False, fontsize=10.5)
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


# ---------------------------------------------------------------------------
# Reading the board: what actually moves the number
# ---------------------------------------------------------------------------

BOARD_CACHE = REPO / "data" / "figure_inputs_board.json"


def vision_figures():
    """Two figures: what changes board reading, and the user's hand-check of 98 boards.

    Every percentage is re-scored from the board readings in this repo against the hand-verified
    answer keys (the cache is written by the scoring runs, not typed).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cache = json.loads(BOARD_CACHE.read_text(encoding="utf-8"))

    def pair(label):
        """Recall of each side, summed over the lectures in that comparison."""
        r = cache[label]["result"]
        out = []
        for side in ("baseline_results", "full_results"):
            found = sum(v["found"] for v in r[side].values())
            items = sum(v["items"] for v in r[side].values())
            out.append(100 * found / items)
        return out[0], out[1]

    # 1. the three things we changed, on the same 35 boards of lectures 1-9
    kw, full = pair("lectures1-9 keyword vs transcription")
    _, mosaic = pair("lectures1-9 frame vs mosaic")
    _, clean = pair("lectures1-9 mosaic vs clean")
    _, small = pair("lectures1-9 7B vs 3B")

    fig, axes = plt.subplots(1, 3, figsize=(7.8, 4.6), gridspec_kw={"width_ratios": [1.1, 1, 1.25]})
    panels = [
        ("The prompt", ["Ask for\nkeywords", "Ask for the\nwhole board"], [kw, full],
         [BAD_C, GOOD_C], f"+{full - kw:.1f} points"),
        ("The model", ["Qwen2.5-VL\n3B", "Qwen2.5-VL\n7B"], [small, full],
         ["#9aa5b1", GOOD_C], f"+{full - small:.1f} points"),
        ("The image", ["Raw video\nframe", "Reconstructed\nboard", "Cleaned\nboard"],
         [full, mosaic, clean], ["#9aa5b1", GOOD_C, "#f77f00"], f"+{mosaic - full:.1f} points"),
    ]
    for ax, (title, labels, vals, cols, delta) in zip(axes, panels):
        ax.bar(range(len(vals)), vals, color=cols, width=0.6, edgecolor="white")
        for x, v in enumerate(vals):
            ax.text(x, v + 1.5, f"{v:.1f}%", ha="center", fontsize=11.5, fontweight="bold", color=INK)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10.5)
        ax.set_ylim(0, 108)
        ax.set_title(f"{title}   ({delta})", fontsize=12.5, fontweight="bold", color=INK)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Board items the model read (%)")
    fig.suptitle(wrapnote("Reading the whiteboard: 35 boards of lectures 1-9, "
                          "349 hand-verified items", 70),
                 fontsize=13.5, fontweight="bold", color=INK)
    fig.text(0.5, -0.01, wrapnote(f"One change at a time, same boards, same answer keys. What you ask for is "
             f"worth {(full - kw) / (full - small):.0f}x the model size and "
             f"{(full - kw) / (mosaic - full):.0f}x the image processing. The cleaned board, which "
             f"looks best to a person, reads slightly worse than the reconstruction it came from."),
             ha="center", va="top", fontsize=10.5, color="#52606d")
    fig.tight_layout(rect=(0, 0.03, 1, 0.93))
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_board_reading.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 2. the human check of the newer lectures' boards
    check = json.loads((REPO / "data" / "board_completeness_2026-09-23.json").read_text(encoding="utf-8"))
    kinds = check["missing_by_kind"]
    sizes = [check["complete"], kinds.get("content", 0), kinds.get("erase_frame", 0),
             kinds.get("blurred", 0)]
    labels = [f"Complete\n{sizes[0]} boards", f"Writing lost\n{sizes[1]}",
              f"Era cut mid-wipe\n{sizes[2]}", f"Camera out of focus\n{sizes[3]}"]
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    wedges, _ = ax.pie(sizes, colors=[GOOD_C, BAD_C, "#f77f00", "#9aa5b1"], startangle=90,
                       wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.98, 0.5), frameon=False, fontsize=11)
    ax.set_title(f"Do the reconstructed boards keep everything?\n"
                 f"{check['boards_answered']} boards checked by hand, {check['complete_percent']}% complete",
                 fontsize=13, fontweight="bold", color=INK)
    fig.text(0.5, 0.02, wrapnote(f"Only the red slice is the reconstruction's fault: the orange boards were "
             "captured while the lecturer was wiping,\nand the grey ones were out of focus in every "
             "frame of the source video."), ha="center", fontsize=10, color="#52606d")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_board_completeness.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("vision figures written")
    print(f"  prompt {kw:.1f} -> {full:.1f} | 3B {small:.1f} | mosaic {mosaic:.1f} | clean {clean:.1f}")
    print(f"  completeness {check['complete']}/{check['boards_answered']} "
          f"({check['complete_percent']}%), content losses {kinds.get('content')}")


def notes_figures():
    """The notes: how much of the board reaches them, by route, and the 2x2 on the transcript.

    Scored here from the notes in git, so the figure and RESULTS 5.4 cannot drift apart.
    """
    import subprocess
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    recall = REPO / "output" / "board_recall.json"
    gt = ["--gt", "data/board_truth", "data/board_truth/draft_lectures1to6"]

    def score(a, b):
        """Recall of both files over the 35 boards, plus how the boards split."""
        subprocess.run([r"C:\Users\Rafi\miniconda3\envs\pyenv\python.exe",
                        str(REPO / "scripts" / "score_board_recall.py"), *gt, "--compare-names", a, b],
                       cwd=REPO, capture_output=True, text=True, errors="replace")
        r = json.loads(recall.read_text(encoding="utf-8"))
        vals = []
        for side in ("baseline_results", "full_results"):
            vals.append(100 * sum(v["found"] for v in r[side].values())
                        / sum(v["items"] for v in r[side].values()))
        return vals[0], vals[1], r

    original, banglish, _ = score("final_lecture_notes.md", "notes_annotated_banglish_7b.md")
    _, english, _ = score("final_lecture_notes.md", "notes_annotated_english_via_banglish_7b.md")
    _, english_direct, _ = score("final_lecture_notes.md", "notes_annotated_english_7b.md")
    base_bt, ft_bt, r1 = score("notes_annotated_banglish_base.md", "notes_annotated_banglish_7b.md")
    base_nb, ft_nb, r2 = score("notes_annotated_banglish_base_noboard.md", "notes_annotated_banglish_noboard.md")
    subprocess.run(["git", "-c", "safe.directory=F:/thesisP2/thesisP2", "checkout", "--",
                    "output/board_recall.json"], cwd=REPO)

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    names = ["Original\npipeline", "English\nwritten\ndirectly", "Banglish", "English\ntranslated\nfrom it"]
    vals = [original, english_direct, banglish, english]
    cols = [BASE_C, "#f77f00", GOOD_C, GOOD_C]
    axes[0].bar(range(4), vals, color=cols, width=0.62, edgecolor="white")
    for x, v in enumerate(vals):
        axes[0].text(x, v + 1.5, f"{v:.1f}%", ha="center", fontsize=11.5, fontweight="bold", color=INK)
    axes[0].set_xticks(range(4))
    axes[0].set_xticklabels(names, fontsize=10.5)
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("Board items reaching the notes (%)")
    axes[0].set_title("What the notes carry, by route", fontsize=13, fontweight="bold", color=INK)

    w = 0.36
    axes[1].bar([0 - w / 2, 1 - w / 2], [ft_bt, ft_nb], w, color=GOOD_C, label="Fine-tuned ASR",
                edgecolor="white")
    axes[1].bar([0 + w / 2, 1 + w / 2], [base_bt, base_nb], w, color=BASE_C,
                label="Off-the-shelf ASR", edgecolor="white")
    for x, v in ((0 - w / 2, ft_bt), (1 - w / 2, ft_nb), (0 + w / 2, base_bt), (1 + w / 2, base_nb)):
        axes[1].text(x, v + 1.5, f"{v:.0f}%", ha="center", fontsize=11, color=INK)
    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(["With the VLM's\nboard text", "Without it"], fontsize=11)
    axes[1].set_ylim(0, 105)
    axes[1].set_title("Does a better transcript help? No (p = 1.0 both ways)",
                      fontsize=13, fontweight="bold", color=INK)
    axes[1].legend(frameon=False, fontsize=10.5)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax.set_axisbelow(True)
    fig.text(0.5, -0.02, wrapnote(f"35 boards, 349 hand-verified items. Right: by board the split is 7 better "
             "/ 6 worse with board text and 10 / 9 without, so the item totals overstate it. Board "
             "recall cannot see whether the surrounding explanation is right - only people can."),
             ha="center", va="top", fontsize=10, color="#52606d")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_notes_recall.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("notes figure written")
    print(f"  original {original:.1f} | banglish {banglish:.1f} | english via {english:.1f} "
          f"| english direct {english_direct:.1f}")
    print(f"  2x2: ft {ft_bt:.1f}/{ft_nb:.1f}, base {base_bt:.1f}/{base_nb:.1f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", default="all",
                    choices=("all", "asr", "dataset", "asr-detail", "vision", "notes"))
    ap.add_argument("--no-diverged", action="store_true", help="leave the collapsed seed out")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.set in ("all", "asr"):
        asr_figure(show_diverged=not args.no_diverged)
    if args.set in ("all", "dataset"):
        dataset_figures()
    if args.set in ("all", "asr-detail"):
        asr_detail_figures()
    if args.set in ("all", "vision"):
        vision_figures()
    if args.set in ("all", "notes"):
        notes_figures()
    return 0


if __name__ == "__main__":
    sys.exit(main())



