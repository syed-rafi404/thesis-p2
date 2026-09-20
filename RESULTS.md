# RESULTS — every number the thesis is allowed to claim

Written for the three of us writing the paper, poster and slides.

**The rule: if a number is not in this file, it does not go in the paper.**
Every row below has a command that regenerates it from data in this repo. If a
reviewer or panellist asks "where did that come from", the answer is a command,
not a memory. Numbers that were typed by hand and never computed are listed at
the bottom under "Retired claims" so nobody reuses them by accident.

Last regenerated: 2026-09-20.

---

## 1. Fine-tuning Whisper for Banglish — the headline result

This is the result the thesis rests on. It is new, it is significant, and it is
speaker-independent.

**Setup.** LoRA adapter on whisper-small. Trained on 70.4 minutes (1.17 h, 219
clips) from speaker A. Evaluated on 43.6 minutes (137 clips) from speaker B, who
appears in no training clip. Total corpus 1.9 h. Training takes about 3 minutes
on an RTX 3060.

| Metric (137 held-out clips) | Base | Fine-tuned | Absolute | Relative |
|---|---|---|---|---|
| WER, per-clip median | 96.1% | 81.8% | -14.3 pp | **-14.9%** |
| CER, per-clip median | 75.3% | 60.7% | -14.6 pp | **-19.4%** |
| Term F1 | 65.0% | 76.1% | +11.1 pp | +17.1% |
| Term recall | 73.0% | 88.8% | +15.8 pp | +21.6% |
| Term precision | 58.6% | 66.7% | +8.1 pp | +13.8% |

**Significance, paired per clip:**

| Test | Wins | Wilcoxon | Sign test |
|---|---|---|---|
| WER | 86 of 137 | p = 9.12e-03 | p = 3.52e-03 |
| CER | 97 of 137 | p = 2.19e-05 | p = 1.22e-06 |

**This replicated.** A second, independently trained run on the same 219 clips
reached WER median 77.1% and CER median 57.4%, winning on 95 and 106 of 137
clips with p = 1.12e-05 and p = 3.86e-08. The ASR gain is real in both runs.
Term F1 is not stable between them — see section 2.1 before quoting it.

**Report medians, never means.** Both models sometimes fall into a repetition
loop and emit far more words than were spoken, which pushes mean error rates
past 100% and swamps mean-based tests. The same comparison on means gives
p = 0.76, which is an artefact of those runaway clips, not evidence of no
effect. Runaway clips: 8 of 137 base, 18 of 137 tuned.

**The qualitative claim this supports** (we have the transcript pairs to show):
the base model translates into English and then loops; the fine-tuned model
transcribes Banglish. Example, BanglaASR7/seg_034:

- reference: `done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe.`
- base: `so, x or gate and x or gate and x or gate and x or gate and ...` (repeats to the token limit)
- tuned: `done. so, x or jodi amra bujhe jai, tahole last je exclusive gate, sheta o kintu amader bujha easier hoye chabe.`

Reproduce: `python scripts/run_p3_experiment.py --skip curve`
Artefacts: `ft_work/eval_whisper_small_1.9h.md` and `.json`

---

## 2. Data-scaling curve — how much transcription effort buys how much accuracy

Same recipe, same held-out speaker, nested subsets with a fixed seed, so the
only variable is the amount of training audio.

| Training audio | Clips | WER median | CER median | Term F1 | CER wins | Wilcoxon (CER) |
|---|---|---|---|---|---|---|
| 0 h (base) | — | 96.1% | 75.3% | 65.0% | — | — |
| 0.30 h | 55 | 91.3% | 65.0% | 78.3% | 92/137 | p = 0.081 |
| 0.60 h | 112 | 91.7% | 70.3% | 69.9% | 78/137 | p = 0.921 |
| 1.17 h (all) | 219 | **77.1%** | **57.4%** | 68.0% | 106/137 | **p = 3.86e-08** |

**On WER and CER the curve is clean and the story is simple:** under an hour of
audio buys you very little and is not statistically reliable (0.6 h is actually
worse than 0.3 h, and its gain has p = 0.92). At the full 1.17 h the fine-tune
improves WER median by 19.0 pp and CER median by 17.9 pp, winning on 95 and 106
of 137 clips respectively, with p below 1e-05 on both. The curve is still
falling steeply at our largest budget — it has not flattened, which is the
argument for the 8-hour corpus.

**Term F1 does not behave, and that is itself a finding.** See the variance
note below before quoting any Term F1 number.

Reproduce: `python scripts/run_scaling_curve.py --hours 0.3 0.6 1.17 --epochs 8`

Artefacts: `ft_work/curve/scaling_curve.md`

### 2.1 Run-to-run variance — read this before quoting Term F1

We now have **two independent training runs on the identical 219 clips**, same
recipe, same seed, differing only in the order the manifest lists them. They do
not agree:

| Metric | Run A (standalone) | Run B (curve top point) | Spread |
|---|---|---|---|
| WER median | 81.8% | 77.1% | 4.7 pp |
| CER median | 60.7% | 57.4% | 3.3 pp |
| Term recall | 88.8% | 88.3% | 0.5 pp |
| Term precision | 66.7% | 55.3% | **11.4 pp** |
| Term F1 | 76.1% | 68.0% | **8.1 pp** |
| WER Wilcoxon | p = 9.12e-03 | p = 1.12e-05 | both significant |
| CER Wilcoxon | p = 2.19e-05 | p = 3.86e-08 | both significant |

**What replicates:** the ASR improvement. Both runs beat the base model on WER
and CER with p < 0.01, and Run B is the stronger of the two. Saying *"the gain
replicated across two independent training runs"* is a real strength and most
undergraduate theses cannot say it.

**What does not replicate:** Term F1, which swings 8.1 pp on identical data,
driven almost entirely by an 11.4 pp swing in term precision.

**Why, and this is the interesting part.** Term precision counts how many of
the 82 fixed English lexicon words the model emits. Run B transcribes *better*
Banglish — lower WER, lower CER — and therefore emits *fewer* English words,
which *lowers* its term precision. The metric penalises the model for doing the
task correctly. This is the same effect that made fusion look healthy at 73.9%
Term F1 while its WER sat at 146.8%.

**Consequences for what we write:**

1. Headline the WER and CER medians with their rank tests. Those are stable.
2. Never claim a Term F1 difference smaller than about 8 pp. The metric cannot
   resolve it. That includes the fusion result: +0.7 pp is an order of
   magnitude inside the noise floor, which independently confirms section 3.
3. Report both runs, or report Run A and note Run B replicates it more
   strongly. Do not quietly pick the better number.

---

## 3. Multimodal fusion — a measured negative result

Nine BanglaASR lectures, term metric (exact match, fixed 82-word English
lexicon), scored with the same functions that produce the headline 73.9%.

| Metric | Whisper baseline | Fused | Difference |
|---|---|---|---|
| Term recall | 65.7% | 66.5% | +0.9 pp |
| Term precision | 83.8% | 83.6% | -0.2 pp |
| Term F1 | 73.2% | 73.9% | **+0.7 pp** |
| WER | 82.6% | 146.8% | +64.1 pp |
| CER | 58.7% | 122.6% | +63.9 pp |

**Significance of the Term F1 difference (n = 9):**

- exact paired sign-flip permutation test: **p = 0.316**
- exact Wilcoxon signed-rank: **p = 0.359**
- paired Cohen's d: 0.37, on n = 9, too small to be stable

Per-video deltas in pp: -1.0, +3.5, +1.4, +1.6, +3.1, -1.0, -1.0, -0.9, +0.3.
Four of nine lectures get worse.

**Two further facts to state plainly:**

1. The visually-biased transcripts are **byte-identical to the baseline for all
   9 videos**. Those runs changed nothing at all.
2. Whisper is producing an **English translation, not a Banglish transcript**:
   the ground truth contains 3,078 Bengali function words, the Whisper output
   contains 54. The 82-word English term metric cannot distinguish a good
   translation from a good transcription, which is why Term F1 looks healthy
   while WER sits at 82.6%.

This is a genuine contribution stated as a negative result, and it sets up
section 1: fusion did not fix Banglish ASR, so we tested what would.

Reproduce: `python scripts/compute_fusion_stats.py`
Artefacts: `output/fusion_statistics.md` and `.json`

### 3.1 Visual bias strength sweep — measured, and a clean negative result

Run 2026-01-27, recorded in `output/bias_parameter_sweep.json`. One Java OOP
lecture, 6,461 characters of ground truth, recall against a 27-term technical
list. **This is a pilot on a single video, not a result on the 9-video
benchmark** — say so when writing about it.

| Bias strength | Term recall | Transcript length | Max word repeat |
|---|---|---|---|
| 0.00 (off) | **8.8%** | 279 chars | 5 |
| 0.25 | 4.1% | 149 chars | 3 |
| 0.50 | 4.1% | 149 chars | 3 |
| 0.75 | 4.1% | 149 chars | 3 |
| 1.00 | 4.1% | 149 chars | 3 |
| 1.25 | 4.1% | 149 chars | 3 |
| 1.50 | 4.1% | 149 chars | 3 |
| 2.00 | 4.1% | 149 chars | 3 |

The file records `optimal_bias: 0.0` — the sweep concluded against itself.

**The shape is the finding.** Turning the bias on halves term recall and
truncates the transcript from 279 to 149 characters. Turning it up further
changes nothing: every non-zero strength from 0.25 to 2.0 produces byte-identical
output. So this is not a tuning problem with a better alpha waiting to be found;
the mechanism fails the moment it engages. That is a much stronger statement
than "we picked a bad alpha", and it is what justifies moving to
verification-based fusion.

Note the config default is still `bias_strength: 2.0` in
`config/live_config.yaml`, the worst value in the sweep. The processor is
disabled, so it does not affect results, but expect a question about it.

Reproduce: the sweep script is not in the repo; the recorded output is the
artefact. Figure 6.6 plots it directly.
Artefacts: `output/bias_parameter_sweep.json`

---

## 4. Illustrated notes — board reconstruction

Frames selected from the lecture video, aligned to note sections by monotonic
dynamic programming, with the lecturer removed and the occluded board rebuilt
from temporally nearby clean frames.

| Quantity | Value | Trustworthy? |
|---|---|---|
| Lectures illustrated | 3 | yes |
| Figures placed | 15 (5.0 per lecture) | yes |
| Board occluded by the lecturer | mean 24.8%, max 32% | yes |
| Masked pixels that received a fill value | mean 99.8% | **yes, but see below** |

**CORRECTION (2026-09-21). Do not write "we recover 99.8% of the board."**
That 99.8% is the fraction of masked pixels that were *assigned some value*. It
says nothing about whether the value is correct. It is a coverage number being
mistaken for a fidelity number, and the two are not the same thing.

Visual inspection of `BanglaASR1/figures/fig_03_520.jpg` against its source
frame `frame_000032_000320s.jpg` shows two real failures:

1. **The lecturer is still visible** as a grey silhouette of his head,
   shoulder and arm, plus blocky rectangular patches. The mask under-covers him,
   most likely because his plaid shirt contains light squares that sit above the
   `PERSON_DARK = 118` brightness cut and are therefore never masked.
2. **Board text is lost.** At 5:20 he is writing `"App...` on the right. That
   text does not survive into the figure. Its `figures.json` entry records
   `rebuilt from 1 nearby frames` — a single donor frame, so wherever that donor
   also had him standing, the fill is simply wrong.

There is also a subtler problem: the figure shows *more* text than the source
frame did (the full `i) String / ii) Integer / iii) Float / iv) Bool` list),
because donors were drawn from later in the lecture. The figure is therefore not
a faithful picture of the board at 5:20.

**The inpainting approach above has been replaced.** See 4.1. Nothing in the
new pipeline is synthesised, so the fidelity question does not arise.

The occlusion percentage and the figure count are still fine to quote.

---

### 4.1 Tiled board reconstruction — measured over all 9 lectures

`scripts/board_mosaic.py`. The frame is cut into a grid of overlapping tiles.
For each tile independently, the pipeline finds a moment when the lecturer was
not standing in front of *that tile* and takes the tile from there. The tiles
are reassembled with raised-cosine blending.

**Every pixel of every output board is unmodified camera output.** Nothing is
inpainted, averaged or generated, which is why there is no fidelity number to
argue about: the only question is whether a tile found a clear moment, and that
is counted exactly.

The lecturer is never absent from the frame. Measured on BanglaASR1 over 79
frames: the board is 23.5% covered in the median frame, 7.0% in the best one,
and no frame is under 5%. Tiles work because he occupies one place at a time.

**Eras.** The board is erased and rewritten mid-lecture. On BanglaASR1 the
board reads `Data Type: i) String ...` at 6:20 and `pi = ...`, `age = 10` at
13:00. Taking each tile's latest clear view across the whole lecture would
assemble pre-erase and post-erase writing into a single board **that never
existed** — plausible and false. Erase events are therefore detected and each
era is mosaicked separately.

**Results, 9 lectures, 694 frames, 35 boards, 94 seconds total:**

| Lecture | Eras | Tiles fully clear (min / median / max) |
|---|---|---|
| BanglaASR1 | 6 | 87.5% / 92.6% / 94.5% |
| BanglaASR2 | 5 | 93.9% / 97.9% / 98.6% |
| BanglaASR3 | 1 | **100% / 100% / 100%** |
| BanglaASR4 | 4 | 97.9% / 98.0% / 98.2% |
| BanglaASR5 | 3 | 96.2% / 96.7% / 97.8% |
| BanglaASR6 | 6 | 96.6% / 97.3% / 97.7% |
| BanglaASR7 | 5 | 95.1% / 100% / 100% |
| BanglaASR8 | 3 | 88.6% / 91.3% / 100% |
| BanglaASR9 | 2 | 98.5% / 98.7% / 99.0% |

**Across all 35 boards: median 97.7% of tiles fully clear, mean 96.5%,
range 87.5% to 100%.** Six boards reach 100%, 26 of 35 reach 95% or better,
and only 2 fall below 90%.

**Quote the range, not the best case.** Two things drive the weak boards:

1. **Short eras.** Six eras are under 8 frames, and they cluster at the bottom
   of the range (90.9%, 91.3%, 93.9%). Fewer frames means fewer chances for a
   tile to be seen clear.
2. **A lecturer who stands still.** BanglaASR1 is the worst lecture at every
   era because he holds one position far longer than the others do. Its video
   is also heavily compressed, so the whiteboard shows macroblocking in the
   source file, which no amount of processing can remove.

Where a tile never finds a clear moment the residue is left visible and
reported as `worst_tile_covered` rather than filled in. A visible gap is honest;
a plausible invention is not.

Reproduce: `python scripts/board_mosaic.py --frames <dir> --out-dir <dir>`
Artefacts: `output/annotation_demo/all9/*/mosaic.json`

### 4.2 Region detection and annotation — status

`scripts/board_regions.py` finds the content blocks on a reconstructed board by
grouping ink, splitting oversized blocks and rejoining boxes that form one
written line. On the BanglaASR7 NAND board it returns 6 regions matching the
title, the gate name, its definition, the block diagram, the truth table and the
standard symbol. `scripts/annotate_board.py` draws the boxes and an explanation
panel onto the real pixels.

**The labels are not yet produced by a model.** The VLM path has never run,
because no Qwen weights exist on this machine. Every annotated figure shown so
far carries labels written by hand in the exact JSON shape the model must
return. Do not describe the annotation as working until it has run on the 5090.

Claimable today: board reconstruction and region detection, with the numbers
above. Not claimable today: annotation quality.

Reproduce: `python scripts/illustrate_notes.py <run_dir>`
Artefacts: `final_lecture_notes_illustrated.md`, `figures/figures.json`

---

## 5. P2 system numbers (unchanged, still true)

| Metric | Value |
|---|---|
| Term F1 | 73.9% |
| Term precision | 83.6% |
| Term recall | 66.5% |
| Corpus | 9 lectures, 73,141 characters, 3 domains |

Reproduce: `python scripts/evaluate_ground_truth.py`

---

## 6. Blanks still to fill

| Blank | Fills when | Command |
|---|---|---|
| Curve at 2 / 4 / 6 / 8 h | the 8 h corpus lands | `run_p3_experiment.py --curve-hours 2 4 6 8` |
| whisper-large-v3-turbo instead of small | on the 5090 | add `--model openai/whisper-large-v3-turbo` |
| Multi-speaker held-out set | new speaker IDs exist | `--test-speakers SPK04,SPK05` |
| Illustration on all 9 lectures | now, it just needs running | `illustrate_notes.py` per run dir |
| Ground-truth corpus stats | new transcripts arrive | `validate_ground_truth.py` |

Current validator state on the original 9 files: 95 errors, 63 warnings, 83
segments, 1.91 hours, 12,890 words, and all 9 are missing a Speaker ID header.
The errors are mostly segments longer than the 30-second Whisper window.

---

## 7. Retired claims — never reuse these

These appeared in `P2/core/abstract.tex` and `scripts/generate_thesis_figures.py`.
None of them was ever computed by any code in this repository; they were literal
strings drawn onto a figure.

| Retired claim | What it should be |
|---|---|
| Baseline Whisper Term F1 = 68.2% | 73.2% |
| Fusion improves baseline by 5.7 pp | +0.7 pp |
| p = 0.003 | p = 0.32 (permutation), 0.36 (Wilcoxon) |
| Cohen's d = 0.96, large effect | d = 0.37, n = 9, unstable |
| "+ Cleaning" stage = 71.5% | no such ablation exists |
| "Visual-Only" mode = 42.3% | the pipeline has no visual-only mode |
| Bias sweep: Light 69.8, Medium 67.1, Heavy 58.4 | see section 3.1 — the real sweep is 8.8% then flat 4.1% |
| Light bias improves over no bias | it halves term recall; optimal bias is 0.0 |

The hardware claim in the abstract is **correct and stays**: P2 ran on an
NVIDIA RTX 3090, 24 GB (confirmed by the author, 2026-09-20), on the machine
with paths under `C:/Users/T2520785`. The RTX 3060, 12 GB referenced elsewhere
in the repo is the current development machine and is what the P3 fine-tuning
numbers were produced on. Keep the two straight when writing the setup section:
P2 pipeline results come from the 3090, P3 fine-tuning results from the 3060.

If a panellist asks how p = 0.003 was obtained, there is no answer, because no
test was run. That single slide puts every other number in the thesis in doubt,
including the fine-tuning result, which is real. Replace, do not defend.
