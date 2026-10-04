# RESULTS — every number the thesis is allowed to claim

Written for the three of us writing the paper, poster and slides.

**The rule: if a number is not in this file, it does not go in the paper.**
Every row below has a command that regenerates it from data in this repo. If a
reviewer or panellist asks "where did that come from", the answer is a command,
not a memory. Numbers that were typed by hand and never computed are listed at
the bottom under "Retired claims" so nobody reuses them by accident.

Last regenerated: 2026-09-21 (speaker split corrected; VLM and notes measured on the RTX 5090).

**Lecture numbers in this file are the OLD numbering.** On 2026-09-22 the lectures were renamed,
grouped by lecturer: old 6-9 are now 10-13 (lecturer B), old 10-13 are now 14-17 (lecturer C),
and new 6-9 are four new lectures. Every number below was computed with the old names and the
ground truth frozen in `data/ground_truth_v1_2026-09-21/`; to reproduce one, point
`prepare_data.py --gt-dir` at that folder. "BanglaASR7" in this file means the NAND lecture
(new name BanglaASR11).

---

## 1. Fine-tuning Whisper for Banglish — the headline result

This is the result the thesis rests on. It is significant, it replicated, and it
is speaker-independent. **It was re-run on 2026-09-21 after the speaker split
was found to be wrong; the numbers in 1.0 replace the ones in 1.3.**

### 1.0 Corrected split (current)

**What was wrong.** The original nine transcripts carry no Speaker ID, so
`finetune/prepare_data.py` labelled them by hand: videos 1-6 speaker A, 7-9
speaker B. Video 6 is speaker B. The user sorted the videos by lecturer into
`data/raw/Speaker1` (1-5) and `data/raw/Speaker2` (6-9), and a speaker-
verification model agrees without ambiguity: mean-voiceprint cosine similarity
0.99-1.00 within each group, 0.75-0.80 across, and 18 of 20 video-6 clips sit
closest to video 7. The old split therefore trained on 47 clips of the "unseen"
test speaker.

Reproduce: `python scripts/verify_speakers.py` -> `output/speaker_check/speaker_similarity.md`

**Setup.** LoRA adapter on whisper-small, same recipe as before (8 epochs, batch
8, r 16). Trained on 55.6 minutes (172 clips, videos 1-5) from speaker A.
Evaluated on 58.4 minutes (184 clips, videos 6-9) from speaker B, who appears in
no training clip. Training takes under a minute on the RTX 5090.

**Decoding, and why two numbers.** Under plain greedy decoding the corrected
fine-tune falls into repetition loops on 58 of 184 clips (base: 10), and the
loops decide the result. We therefore also report Whisper's standard loop
safeguard (Radford et al. 2023, section 4.5): a transcript whose gzip
compression ratio exceeds 2.4 is decoded again with sampling at T = 0.2, 0.4 ...
1.0 until it stops looping. It reads only the hypothesis, never the reference,
and is applied identically to the base and the fine-tuned model. **Be open that
it was adopted after the greedy result was seen**; the defence is that it is the
reference implementation's default, not something tuned here, and that both
numbers are reported. Only the compression-ratio half is used; the
log-probability half would resample most Banglish clips, not just loops.

| Metric (184 held-out clips) | Base | Fine-tuned, safeguard | Fine-tuned, greedy |
|---|---|---|---|
| WER, per-clip median | 95.0% | **78.8%** | 95.1% (base 96.0%) |
| CER, per-clip median | 73.4% | **54.6%** | 71.5% (base 74.2%) |
| Runaway clips | 1 | 4 | 58 (base 10) |
| Clips re-decoded by the safeguard | 9 | 64 | — |

**Significance, safeguard, paired per clip:**

| Test | Wins | Wilcoxon | Sign test |
|---|---|---|---|
| WER | 125 of 184 | p = 8.41e-07 (z = +4.93) | p = 1.29e-06 |
| CER | 139 of 184 | p = 1.20e-12 (z = +7.11) | p = 2.31e-12 |

Under greedy decoding the same adapter is significantly **worse** than base
(WER z = -2.62, p = 8.7e-03), driven entirely by loops. Read the sign of z: a
two-sided p alone does not say which way the difference goes.

**It replicated, and it is not one lucky draw.**

| Run | WER median | CER median | WER Wilcoxon | CER Wilcoxon |
|---|---|---|---|---|
| Run A, training seed 42, safeguard seed 0 | 78.8% | 54.6% | 8.4e-07 | 1.2e-12 |
| Run A, training seed 42, safeguard seed 1 | 82.0% | 57.6% | 8.5e-06 | 4.2e-11 |
| Run B, training seed 1, safeguard seed 0 | 82.4% | 59.4% | 1.0e-06 | 1.1e-12 |
| Run C, scaling-curve top point (same data, seed 42) | 83.3% | 58.4% | 4.8e-08 | 7.9e-14 |

Quote a range: **WER median 95.0% -> 78.8-83.3%, CER median 73.4% -> 54.6-59.4%,
p < 1e-05 in every run.** Under greedy decoding Run B gives WER 90.2%, CER 65.1%,
better but not significant (p = 0.92 and 0.15): greedy results are unstable
because they depend on which clips happen to loop.

**Every held-out lecture improves** (Run A, safeguard, WER / CER medians):
video 6 92.5 -> 70.0 / 72.0 -> 45.6; video 7 96.2 -> 79.7 / 68.5 -> 52.1;
video 8 96.1 -> 88.9 / 79.8 -> 66.7; video 9 94.4 -> 83.4 / 73.4 -> 57.2.

**On exactly the old 137 test clips** (videos 7-9, byte-identical clips), the
corrected adapter with the safeguard gives WER 95.7% -> 87.9% (p = 4.9e-03) and
CER 74.1% -> 59.8% (p = 1.4e-07). Smaller than on 184 clips because video 6
gains the most.

**Ruling out the new machine.** The superseded split, re-run on the 5090 with the
current software, gives WER median 81.8% under greedy decoding, the same as the
3060 run. So the change is caused by the split, not by the hardware or library
versions. With the safeguard the superseded split gives 77.4%, so the honest
result is close in size to the leaked one.

Reproduce:

```
python scripts/run_p3_experiment.py --skip curve --allow-validation-errors --only-speakers A,B --decode greedy fallback
python finetune/train_lora.py --adapter-out <ft_work>/lora_run_seed1 --epochs 8 --batch 8 --seed 1
python finetune/evaluate.py --adapter <ft_work>/lora_run_seed1 --decode fallback --tag run_seed1_fallback
python finetune/evaluate.py --adapter <ft_work>/lora_run --decode fallback --fallback-seed 1 --tag run_fallback_seed1
python scripts/compare_evals.py A=<ft_work>/eval_run_fallback.json B=<ft_work>/eval_run_seed1_fallback.json
```

Artefacts: `ft_work/eval_run*.json` and `.md`, `ft_work/split.json`
(`"speaker_map": "v2"`), control run in `ft_work_v1_repro_5090/`.

**Term F1** moves from 72.3% to 85.0% with the safeguard, but see 2.1: it swings
8 pp between identical runs and is anti-correlated with transcription quality.
Do not headline it.

### 1.1 A second unseen speaker (Speaker3, added 2026-09-21)

Four new lectures, BanglaASR10-13, in `data/raw/Speaker3`, labelled speaker C.
75 clips, 24.4 minutes. Voiceprints confirm a third, distinct lecturer:
similarity 0.99-1.00 within C, 0.81-0.85 to A, 0.59-0.67 to B.

The adapters trained on speaker A only (section 1.0, unchanged, identical
training clips) were scored on speaker C:

| Run | Decode | WER median | CER median | WER Wilcoxon | CER wins, Wilcoxon |
|---|---|---|---|---|---|
| Run A (seed 42) | safeguard | 93.0% -> **80.7%** | 68.4% -> **46.4%** | p = 2.7e-04 | 63/75, p = 2.8e-09 |
| Run B (seed 1) | safeguard | 93.0% -> **81.4%** | 68.4% -> **46.7%** | p = 4.4e-04 | 67/75, p = 2.3e-09 |
| Run A (seed 42) | greedy | 93.0% -> 83.3% | 68.6% -> 48.2% | p = 0.053 | 56/75, p = 1.1e-04 |
| Run B (seed 1) | greedy | 93.0% -> 86.2% | 68.6% -> 49.9% | p = 0.49 | 56/75, p = 4.9e-03 |

**The fine-tune generalizes to a second lecturer it never heard, in both runs.**
On this speaker the CER gain is significant even under plain greedy decoding
(runaway clips 7-8 of 75), so here the result does not depend on the safeguard.

Reproduce:

```
set THESIS_FT_DIR=<repo parent>\ft_work_3spk
python finetune/prepare_data.py --test-speakers B,C --out %THESIS_FT_DIR%
python scripts/verify_speakers.py
python finetune/evaluate.py --adapter <ft_work>\lora_run --base <ft_work>\models\whisper-small --split test_C.jsonl --decode fallback --tag C_runA_fallback
```

(`test_C.jsonl` is `test.jsonl` filtered to speaker C.) Artefacts: `ft_work_3spk/eval_C_*.json`.

### 1.2 Adding speaker C to training — a weak trend, not a result

Train on A + C (80.0 min), test on B (the same 184 clips), safeguard:

| Training | Seed 42 WER / CER | Seed 1 WER / CER |
|---|---|---|
| A only (55.6 min) | 78.8% / 54.6% | 82.4% / 59.4% |
| A + C (80.0 min) | 78.5% / 53.7% | 76.9% / 55.3% |

Paired per clip, A+C against A-only, same seed: A+C wins more of the clips
where the two differ on WER (sign test p = 0.006 and 0.014), but the size of the
gain is not significant (Wilcoxon p = 0.22 and 0.058), and CER shows no
significant difference (Wilcoxon p = 0.29 and 0.13). **Say "adding a second
training speaker leans better in both runs but is not significant at this
scale"**, no stronger. Under greedy decoding A+C still loops (51 and 59 clips).

Artefacts: `ft_work_AC/eval_AC_*.json`.

### 1.4 whisper-large-v3-turbo instead of whisper-small (2026-09-21, RTX 5090)

Same corrected split (train speaker A, 55.6 min), **same recipe unchanged**
(8 epochs, batch 8, LoRA r 16 on q/v, lr 1e-3; not re-tuned for the bigger
model, deliberately, to avoid tuning on the test set). Base model
`openai/whisper-large-v3-turbo`, 809M parameters. Training takes 101 s.

| Test speaker | Decode | WER median, base -> tuned | CER median, base -> tuned | Wilcoxon WER / CER |
|---|---|---|---|---|
| B (184 clips) | safeguard | 91.8% -> 79.2% (s42), 85.7% (s1) | 68.9% -> 58.2% (s42), 61.0% (s1) | all p < 1e-04 |
| B (184 clips) | **greedy** | 93.8% -> 82.8% (s42), 90.0% (s1) | 70.0% -> 61.4% (s42), 63.8% (s1) | p = 0.005 / 0.015 (s42), 0.048 / 0.034 (s1) |
| C (75 clips) | safeguard | 94.4% -> 76.9% (s42), 77.6% (s1) | 73.3% -> 51.8% (s42), 44.2% (s1) | all p < 1e-08 |
| C (75 clips) | **greedy** | 94.6% -> 79.2% (s42), 79.5% (s1) | 74.2% -> 54.4% (s42), 46.7% (s1) | all p < 6e-04 |

**The useful finding: the larger model's gain survives plain greedy decoding**,
on both unseen speakers and both seeds (all positive, all p < 0.05). It loops
far less (22-26 runaway clips of 184 against 58 for whisper-small), so with it
the headline does not depend on the loop safeguard. This answers the obvious
question about a safeguard adopted after seeing results.

**Large vs small, per clip, both fine-tuned, safeguard, same seed:** on speaker B
no significant difference (WER p = 0.16 and 0.52, CER p = 0.62 and 0.16); on
speaker C the large model is better on WER (p = 0.039 and 0.002) but not on CER
(p = 0.44 and 0.30). **Say: at one hour of data the larger model is not reliably
more accurate, but it is more robust.**

Reproduce: `python finetune/train_lora.py --model openai/whisper-large-v3-turbo --adapter-out <ft_work>/lora_turbo_seed42 --epochs 8 --batch 8 --seed 42`,
then `evaluate.py --base openai/whisper-large-v3-turbo --adapter <ft_work>/lora_turbo_seed42 --decode fallback`
(and `greedy`; and with `THESIS_FT_DIR=<ft_work_3spk> --split test_C.jsonl` for speaker C).
Artefacts: `ft_work/eval_turbo_*.json`, `ft_work_3spk/eval_C_turbo_*.json`.

**Training the large model on A + C (80.0 min, two speakers), test on B — the
strongest configuration measured:**

| Decode | WER median, base -> tuned (s42 / s1) | CER median, base -> tuned (s42 / s1) | Wilcoxon | Runaway |
|---|---|---|---|---|
| **greedy** | 93.8% -> **73.5% / 74.8%** | 70.0% -> **48.8% / 52.1%** | WER p = 2.3e-11 / 9.6e-12, CER p = 5.9e-09 / 2.6e-11 | 12 -> 12 / 11 |
| safeguard | 91.8% -> 72.1% / 73.1% | 68.9% -> 48.3% / 51.2% | all p < 1e-12 | 3 -> 2 / 3 |

Better than base on 134-143 of 184 clips. **No loop safeguard needed**: under
plain greedy decoding the fine-tune loops no more than the base model does.

A + C against A alone, large model, per clip, same seed, safeguard: A + C is
better on WER (z = +4.41 and +6.03, p < 0.001) and on CER (p = 0.004 and
< 0.001), in both seeds. **With the larger model, adding a second training
speaker helps significantly**; with whisper-small it was only a trend (1.2).
Caveat: A + C adds both a speaker and 24 minutes, so this cannot say which of
the two caused it.

**If one headline is needed, it is this row:** whisper-large-v3-turbo, LoRA,
trained on two lecturers (80 min), tested on a third it never heard: CER
70.0% -> 48.8-52.1%, WER 93.8% -> 73.5-74.8%, plain greedy decoding, two seeds,
p < 1e-08. It is also the design the user proposed before seeing any of these
numbers: train on every speaker except the test one.

Reproduce: `THESIS_FT_DIR=<ft_work_AC>`, `train_lora.py --model openai/whisper-large-v3-turbo --data-dir <ft_work_AC> --adapter-out <ft_work_AC>/lora_turbo_AC_seed42 --epochs 8 --batch 8 --seed 42`,
then `evaluate.py --base openai/whisper-large-v3-turbo --adapter <ft_work_AC>/lora_turbo_AC_seed42 --decode greedy`.
Artefacts: `ft_work_AC/eval_AC_turbo_*.json`.

### 1.5 Leave-one-speaker-out with the large model — the headline (2026-09-21)

Every lecturer is held out once; the model trains on the other two. Same recipe
(whisper-large-v3-turbo, LoRA r 16, 8 epochs, batch 8, lr 1e-3), two training
seeds per fold, **plain greedy decoding, no loop safeguard**.

| Held-out lecturer | Trained on | WER median, base -> tuned (s42 / s1) | CER median, base -> tuned (s42 / s1) | Clips better (CER) | Wilcoxon |
|---|---|---|---|---|---|
| A, videos 1-5 (172 clips) | B + C, 82.9 min | 97.5% -> 76.2% / 75.8% | 74.2% -> 51.8% / 49.9% | 134, 138 of 172 | p < 1e-10 |
| B, videos 6-9 (184 clips) | A + C, 80.0 min | 93.8% -> 73.5% / 74.8% | 70.0% -> 48.8% / 52.1% | 124, 138 of 184 | p < 1e-08 |
| C, videos 10-13 (75 clips) | A + B, 114.0 min | 94.6% -> 74.5% / 79.8% | 74.2% -> 45.2% / 54.0% | 65, 67 of 75 | p < 1e-05 |

**Six of six runs significant under plain decoding.** Averaged over the six runs
(unweighted mean of per-run medians): **CER 72.8% -> 50.3%, WER 95.3% -> 75.7%.**
Runaway clips fall or stay level in every fold (A 15 -> 6-8, B 12 -> 11-12,
C 6 -> 3). With the loop safeguard the numbers are within about 1 pp and all
p < 1e-07.

**What to claim:** fine-tuning Whisper on about 80-114 minutes of transcribed
Banglish from two lecturers cuts the character error rate on a third, unseen
lecturer by about a third (72.8% -> 50.3% CER), for every one of the three
lecturers, in both seeds. **What not to claim:** that this is usable ASR (a 50%
CER is still high), or that it holds for many speakers (three is few).

Reproduce one fold (the others differ only in `--test-speakers`):

```
set THESIS_FT_DIR=<parent>\ft_work_BCtoA
python finetune/prepare_data.py --test-speakers A --out %THESIS_FT_DIR% --audio-dir <parent>\ft_work_3spk\audio_cache
python finetune/train_lora.py --model openai/whisper-large-v3-turbo --data-dir %THESIS_FT_DIR% --adapter-out %THESIS_FT_DIR%\lora_turbo_seed42 --epochs 8 --batch 8 --seed 42
python finetune/evaluate.py --base openai/whisper-large-v3-turbo --adapter %THESIS_FT_DIR%\lora_turbo_seed42 --decode greedy --tag turbo_seed42_greedy
```

Folders: `ft_work_BCtoA` (test A), `ft_work_AC` (test B), `ft_work_ABtoC` (test C).
Adapters that trained on B must never produce transcripts for notes scored on
B's boards.

**Data-quality check (2026-09-22).** `prepare_data.py` reads a segment boundary only
when a timestamp is written exactly like `[1:34-1:53]`. In the ground truth behind
these runs, 9 of 156 timestamps had stray spaces (`[4:22- 4:45 ]`, `[ 08:29 - 09:09]`:
8 in lecture 13, 1 in lecture 4), so their text joined the previous segment and 10
test clips (4 of A's, 6 of C's) carry more words than their audio. Both models were
scored on the same clips. Without those 10 clips: **CER 72.2% -> 49.6%, WER 95.3% ->
75.3%**, every run still p < 1e-07. The defect made the headline slightly
pessimistic; quote the published 72.8% -> 50.3%. `prepare_data.py` now warns about
such lines, and the current `data/ground_truth` files were repaired with
`validate_ground_truth.py --fix` (the frozen copy is left as it was, so the runs
reproduce).
Reproduce: `python scripts/check_merged_timestamps.py` (its "all clips" row
reproduces 72.8% -> 50.3% and 95.3% -> 75.7%).

### 1.6 Is the high WER only a spelling problem? No (2026-09-21)

Banglish has no standard spelling, so a panel will ask whether the ~75% WER is
inflated by "aami" against "ami". Two spelling-fair variants of WER were
computed on the same saved outputs, with rules committed before any rescoring
(`b98c422`, `scripts/banglish_wer.py`):

- **nWER**: both sides mapped to the transcription guide's section 4.1 spellings
  (the `CANONICAL` table `validate_ground_truth.py` already enforces), and runs
  of the same vowel collapsed.
- **fWER**: as nWER, and a word also counts as correct at >= 0.8 character
  similarity to the reference word (so words of 3 letters or fewer must match).

Headline runs of 1.5 (plain greedy decoding), mean of the six per-run medians:

| Metric | Base | Fine-tuned |
|---|---|---|
| Plain WER | 95.3% | 75.7% |
| Spelling-fair nWER | 95.0% | 74.8% |
| Fuzzy fWER | 92.7% | 68.2% |

The fine-tune is better in all six runs on all three measures (Wilcoxon p between
2.2e-16 and 2.7e-06). **The guide's spelling table moves WER by about 1 point and
near-miss spellings by about 7 more, so most of the word error is genuine
recognition error, not spelling.** Report plain WER and CER as the headline; use
this section to answer the spelling question. Per-run numbers: rerun the command.

Reproduce: `python scripts/banglish_wer.py --mean "hold out A s42=<parent>/ft_work_BCtoA/eval_turbo_seed42_greedy.json" ...`
(the six greedy files listed in 1.5).

### 1.8 THE FINAL ASR RESULT — 5.15 h, tuned, random video split (2026-09-23/24, 3060)

**This is the thesis's speech result.** The dataset is closed: 28 lectures, 5.15 h of hand-checked
Banglish. Whole lectures were held out at random (20% per lecturer, seed 0, rule fixed beforehand),
the three validation lectures of 1.7 were locked out of the test set, and the tuning never saw the
test lectures.

| | |
|---|---|
| Train | 22 lectures, **4.10 h** (A 90.7 min, B 58.4, C 159.8, minus the test lectures) |
| Test | **BanglaASR8, 9, 11, 15, 19, 27** - 6 lectures, **1.05 h**, 177 clips (A 19.9 min, B 14.2, C 29.1) |
| Model | whisper-large-v3-turbo + LoRA r16 (alpha 32, q_proj + v_proj), 8 epochs, batch 8, bf16, gradient checkpointing |
| Decoding | plain greedy; the loop safeguard is reported beside it |

**Median per-clip error on the 177 test clips, off-the-shelf against fine-tuned:**

| Learning rate | Seed | CER | WER | Runaway clips | Better / 177 | Wilcoxon |
|---|---|---|---|---|---|---|
| off-the-shelf | - | 67.7% | 93.9% | 13 | - | - |
| **1e-3** | **42** | **15.8%** | **42.5%** | 1 | 164 | p < 0.001 |
| **1e-3** | **1** | **16.0%** | **41.7%** | 1 | 167 | p < 0.001 |
| 2e-3 (the tuned choice) | 1 | 16.2% | 41.7% | 2 | 168 | p < 0.001 |
| 2e-3 (the tuned choice) | 42 | **118.7%** | 189.8% | **82** | 35 | **worse** |

**Two corrections to the p-values above (2026-10-03).** `evaluate.py` stored
`wilcoxon_p: 0.0` for these rows, because it computes `2 * (1 - normal_cdf(z))` and that
subtraction underflows for z above about 8.3. The z values were saved correctly, and the
asymptotic tail gives **1.3e-26 (s42 CER), 1.7e-29 (s1 CER)** - not below 1e-30, which is
what the stored zero was read as. Second and more important, the per-clip test treats 177
clips as independent when they come from 6 lectures and 3 lecturers, so the effective
sample is far smaller and any exponent of that size overstates the evidence. **Quote
`p < 0.001`, and lead with the clustering-free result: all 6 test lectures improve, a
two-sided sign test at p = 0.031.** 12 other eval files carry the same stored zero; none
of their numbers is quoted anywhere. The LOSO p-values of 1.5 (z = 5.9 to 8.2) did not
underflow and are correct as written.

**Headline: CER 67.7% -> 15.8-16.0%, WER 93.9% -> 41.7-42.5%**, two seeds agreeing to 0.2 points,
better on 164 and 167 of 177 clips. The error is cut by about three quarters.

**The gain is not a decoding trick.** The whisper-small result of 1.0 only beat its baseline with
Whisper's compression-ratio loop safeguard switched on, so the obvious challenge here is that the
safeguard is doing the work. It is not. Re-scored with `evaluate.py --decode fallback` on both
models:

| Seed | Greedy | With the safeguard | Runaway clips, greedy |
|---|---|---|---|
| 42 | 15.8% | **15.8%** | 1 of 177 |
| 1 | 16.0% | **16.0%** | 1 of 177 |

Identical to the first decimal, because the fine-tuned model loops on one clip in 177 and has
nothing for the safeguard to rescue (off-the-shelf Whisper loops on 13). Report the greedy numbers;
this table is the answer if anyone asks.

**The gain is uneven, and the pattern follows the training data** (`P2/figures/fig_asr_per_lecture`,
seed 42, median CER per lecture):

| Test lecture | Lecturer | Clips | Off-the-shelf | Fine-tuned | That lecturer's training speech |
|---|---|---|---|---|---|
| BanglaASR8 | A | 14 | 68% | 15% | 1.2 h |
| BanglaASR9 | A | 41 | 67% | 12% | 1.2 h |
| **BanglaASR11** | **B** | 46 | 70% | **52%** | **0.7 h** |
| BanglaASR15 | C | 8 | 88% | 12% | 2.2 h |
| BanglaASR19 | C | 12 | 65% | 12% | 2.2 h |
| BanglaASR27 | C | 56 | 73% | 16% | 2.2 h |

Every lecture improves, but **lecturer B's lecture improves least by a wide margin** - 52% where the
others reach 12-16% - and B contributed the least training speech. With one lecture per lecturer at
the low end this is an observation, not a controlled result: it cannot separate "less data from
this lecturer" from "this lecturer is harder". State it as the most likely reading and as the
argument for collecting more from under-represented lecturers.

**The instability, which must be reported with it.** At 2e-3 - the rate the pre-registered tuning
chose on the validation lectures (1.7) - one of the two seeds collapsed into repetition loops: 82 of
177 clips runaway, CER 118.7%, worse than doing nothing. Same data, same settings, different random
seed. This is the third time this configuration has shown the same fragility: LoRA rank 32 diverged
and all-four-projections diverged, in both the 2.1 h rehearsal and the 5.15 h tuning. **Do not quote
the 16.2% from 2e-3 without its failed twin.**

**A disclosure about the 1e-3 rows.** The pre-registered procedure chose 2e-3. The 1e-3 runs were
launched *after* seeing that divergence, so this choice was not blind, and the thesis must say so.
What can be claimed honestly: the runner-up rate from the same tuning table is stable across two
seeds on the test set, and its two seeds agree; the chosen rate is not. The selection rule itself is
unchanged and still recorded in `data/splits/tuning_plan.md`.

**Compared with the earlier headline (1.5).** That number - CER 72.8% -> 50.3% - holds out an entire
lecturer, so it answers a harder question with 80-114 min of training data. This one holds out whole
lectures from lecturers who are also in training, on 4.1 h. **Both belong in the thesis, labelled:**
this is "new lectures from known lecturers", 1.5 is "an unseen lecturer".

```
python scripts/whisper_full_pipeline.py --tune-dir F:\thesisP2\ft_work_tune5h --final-dir F:\thesisP2\ft_work_final5h
powershell -File claude_transfer/final_lr1e3.ps1     # the 1e-3 pair, same split and data
```
Artifacts: `artifacts/ft_work_final5h/` (2e-3, both seeds, and the loop-safeguard evaluations),
`artifacts/ft_work_final5h_lr1e3/` (1e-3, both seeds). Each folder's `split.json` freezes the split.

### 1.7 Hyperparameter tuning on a validation set, pre-registered (rehearsal, 2026-09-22/23, 3060)

The panel will ask how the settings were chosen. They are now chosen by a procedure written down
**before any run**: the plan in `data/splits/tuning_plan.md` (`64110e8`, addendum `8ebe3f8`) and the
validation lectures in `data/splits/lr_validation.json` (`1eaa11c`, seed 2026): **BanglaASR2 (A,
14.0 min), BanglaASR12 (B, 13.1), BanglaASR14 (C, 7.2)** — one per lecturer, locked out of every
test set afterwards (`prepare_data.py --never-test`). **The test set is never used for tuning.**

This run is the **rehearsal** on the ground truth available on 2026-09-22 (new numbering, 2.69 h:
395 training clips / 126.8 min, 102 validation clips / 34.2 min). The plan's addendum requires the
same procedure to be repeated on the full ground truth, and that repeat supersedes these settings
(`scripts/whisper_full_pipeline.py` step 3).

Fixed throughout: whisper-large-v3-turbo + LoRA, batch 8, bf16, gradient checkpointing, greedy
decoding, alpha = 2 x rank. Starting point: lr 1e-3, rank 16, `q_proj,v_proj`, 8 epochs, seed 42.
Score: median per-clip CER on the validation clips. Off-the-shelf Whisper on the same clips: **CER
73.2%, WER 96.7%**.

| Stage | Run | Val CER | Val WER | Note |
|---|---|---|---|---|
| 1 learning rate | lr 5e-4 | 45.9% | 66.2% | 76/102 clips better, Wilcoxon p = 2.8e-07 |
| 1 | lr 1e-3 (the starting point) | 45.4% | 64.8% | 78/102, p = 5.6e-09 |
| 1 | **lr 2e-3** | **42.1%** | 67.6% | 80/102, p = 5.9e-10; runaway clips 8 -> 4 |
| 2 LoRA rank | lr 2e-3, rank 8 | 42.7% | 63.2% | |
| 2 | lr 2e-3, rank 32 | 117.3% | 179.9% | **diverged** |
| 3 adapted layers | lr 2e-3, `q,k,v,out` | 73.6% | 96.8% | **no better than off-the-shelf** |
| 4 epochs | lr 2e-3, 4 epochs | 45.9% | 65.9% | the validation-loss minimum; worse CER |
| 5 stability | lr 2e-3, seed 1 | 43.8% | 68.3% | seed spread 1.7 points |

**Chosen: lr 2e-3, rank 16, `q_proj,v_proj`, 8 epochs** — 3.3 CER points better than the starting
point, more than its seed-to-seed spread (1.7), which is what the pre-registered noise rule
requires. Applied by `run_p3_experiment.py --tuned`.

Three findings worth stating, none of them favourable:

- **Capacity hurts at the faster rate.** Rank 32 diverged outright and adapting all four attention
  projections landed on the off-the-shelf model's error. More adapter parameters are not better
  here; the 2 h of speech does not support them.
- **Validation loss is a poor proxy for CER.** The loss bottoms out at epoch 4 (1.740, against
  1.889 at epoch 8), so stage 4 retrained there — and CER got worse, 42.1% -> 45.9%. Select on the
  metric that is reported, not on the loss.
- **The margin is small next to seed noise.** 3.3 points against a 1.7-point spread from one seed
  change, measured on 34 minutes of validation speech. It passes the rule, but it is not a large
  effect, and the repeat on the full data may choose differently.

Cost on the 3060: 7 trainings, about 36 min each (18 min for the 4-epoch one) plus 4-7 min per
evaluation, 20:17 to 01:40 unattended, committed and pushed by the script itself (`b4c80fc`,
`633c404`).

Files: `artifacts/ft_work_lr/tuning_summary.md` (the same table), `tuning_result.json` (the chosen
settings), `lr_check_summary.md` (stage 1 with the rank tests); logs and adapters in
`F:\thesisP2\ft_work_lr\`.

Reproduce: `python scripts/tune_whisper.py` with `THESIS_TUNE_DIR` set to a work folder prepared by
`prepare_data.py --split-by video --test-lectures BanglaASR2,BanglaASR12,BanglaASR14`
(stage 1 alone: `claude_transfer/lr_check.ps1`).

### 1.7b The SAME tuning repeated on the full 5.15 h corpus - the run that chose the final settings

**This is the tuning behind 1.8, and it supersedes 1.7.** 1.7 is the rehearsal on 2.69 h; the
plan's addendum required the procedure to be repeated on the closed corpus, and
`whisper_full_pipeline.py` step 3 did that on 2026-09-23 (362.6 min on the 3060, 7 trainings and
their evaluations). Same plan, same three validation lectures (BanglaASR2, 12, 14), test lectures
never touched. Off-the-shelf Whisper on these validation clips: **CER 73.8%, WER 97.6%**.

| Stage | Run | lr | rank | layers | epochs | seed | val CER | val WER | val loss, last / min |
|---|---|---|---|---|---|---|---|---|---|
| 1 learning rate | lr5e-4 | 5e-4 | 16 | q,v | 8 | 42 | 37.9% | 60.0% | 1.782 / 1.685 |
| 1 learning rate | lr1e-3 (the default) | 1e-3 | 16 | q,v | 8 | 42 | 42.2% | 61.9% | 1.811 / 1.667 |
| 1 learning rate | **lr2e-3** | 2e-3 | 16 | q,v | 8 | 42 | **33.6%** | **54.5%** | 1.801 / 1.683 |
| 2 LoRA rank | lr2e-3_r8 | 2e-3 | 8 | q,v | 8 | 42 | 40.1% | 64.1% | 1.813 / 1.693 |
| 2 LoRA rank | lr2e-3_r32 | 2e-3 | 32 | q,v | 8 | 42 | **126.6% diverged** | 200.0% | 4.663 / 4.663 |
| 3 adapted layers | lr2e-3_qkvo | 2e-3 | 16 | q,k,v,o | 8 | 42 | **134.7% diverged** | 174.4% | 4.877 / 2.037 |
| 4 epochs | lr2e-3_e5 | 2e-3 | 16 | q,v | 5 | 42 | 39.4% | 59.6% | 1.666 / 1.656 |
| 5 stability | lr2e-3_s1 | 2e-3 | 16 | q,v | 8 | 1 | 39.1% | 59.6% | 1.815 / 1.681 |

**Chosen: lr 2e-3, rank 16, q_proj + v_proj, 8 epochs** - 8.6 CER points better than the default,
more than the 5.4-point seed spread the noise rule requires. The same three negatives as the
rehearsal reappear, on 2x the data: **rank 32 diverged, all four projections diverged, and the
validation-loss minimum (5 epochs, loss 1.666 against 1.801) scored 5.8 CER points worse.** Select
on the reported metric, not on the loss.

Note for the writing: **1.8's test-set divergence at this same 2e-3 is the third and fourth
appearance of the same fragility**, and it is why 1.8 reports the 1e-3 pair beside it.

File: `artifacts/ft_work_tune5h/tuning_summary.md` (this table), `tuning_result.json` (the chosen
settings), `artifacts/ft_work_final5h/pipeline_log.txt` (timings: tuning 362.6 min, final seed 42
80.3 min, seed 1 66.9 min).
Reproduce: `python scripts/whisper_full_pipeline.py --tune-dir <dir> --final-dir <dir>` (step 3).

### 1.8b The worked example used throughout the methodology chapter (2026-09-25, revised)

Every figure in the methodology chapter now carries **one moment of one lecture**: the same
seventeen seconds of audio, the frame taken while it was spoken, the board that minute
produced, and the note written from it. Lecture **BanglaASR11** (old numbering 7, the
`BanglaASR7_004` run folder), **board era 5, 10:50 to 14:00**, the X-NOR gate.

| | value |
|---|---|
| Clip | `BanglaASR11/seg_041.wav`, 754.0 to 771.1 s, 17.06 s, 16 kHz |
| CER, fine-tuned | **24.5%** (run median 15.8%) |
| WER, fine-tuned | **43.6%** (run median 42.5%) |
| Reference | `so 1st cell e ami pabo 0, 0 equals to 0. 0, 1 equals to 1. 1, 0 equals to 1. 1, 1 equals to 0. x-or banano amar shesh. ekhon etake ami not kore felbo. not mane ki?` |
| Fine-tuned output | `so first ele ami pabo 0 0 equals to 0, 0 1 equals to 1, 1 0 equals to 1, 1 1 equals to 0. x or banano amar shesh. ekhon eitake ami not kore felbo. not mane ki? inverse ta baupar felbo.` |
| Frame | 760 s (12:40), the lecturer writing that column with her arm across the board |
| Mel array | 128 mel bins x 3000 frames, values -0.75 to 1.25, from `WhisperFeatureExtractor` |

**Why this clip and not a median one.** The clip says out loud the exact column of the
truth table that box 2 of that board contains, so the audio, the frame, the board and the
note are the same event rather than four unrelated examples. Its CER is 24.5 per cent
against the run's median of 15.8, so it is **worse than typical, not better**, which is the
safe direction for a worked example. The figure caption gives both numbers.

**Box names the VLM returned for era 5** (`board_boxes.json`, `mock: false`, model
`Qwen/Qwen2.5-VL-7B-Instruct`): 1 Title, 2 Truth table, 3 Gate symbol, 4 Block diagram,
5 Formula. **Two of these are swapped and the figure is left as the model produced it:**
box 3 is the block diagram and box 4 is the gate symbol. Both names describe something
that is on the board, which is why a naming error of this kind survives a recall measure
that scores content rather than labels. The caption says so.

**Why the example moved off the NAND board (era 3).** On that board the lecturer labels the
gate NAND but draws the NOR symbol, an OR body with a bubble rather than an AND body. The
thesis already reports that this lecturer mislabels gates, in Chapter 3 and in Chapter 5,
so the error is not hidden; it was simply a poor choice for the one board reproduced four
times as the showcase. Era 5 is correct throughout: the truth table, the symbol and the
formula all agree.

Files: `xnor-frame-before.jpg`, `xnor-mosaic-raw.jpg`, `xnor-mosaic-clean.jpg`,
`xnor-boxes.jpg` in the thesis images folder. The old `nand-*.jpg` files are left in place,
unused, as a record.

Reproduce: `scripts/make_example_inputs.py --stage extract` then `--stage plot` (two
interpreters, see the file header); `scripts/redraw_board_figure.py --era 5` to redraw the
labelled board from the stored box records without a GPU; `scripts/make_arch_figures.py`.
Per-clip numbers come from `ft_work_final5h_lr1e3/eval_lr1e3.json`, key `per_clip.tuned`.

### 1.9 Corpus statistics as the figures and the thesis report them (2026-09-24)

Computed from `data/ground_truth/*.txt` and the videos themselves, by the same code that draws
`P2/figures/fig_data_*` (`scripts/make_result_figures.py`, `lecture_stats()` and `board_stats()`).
Quote these in the data chapter.

| Quantity | Value |
|---|---|
| Lecture recordings | **44**, **8.33 h** of video (ffprobe over `data/raw/live_classroom`) |
| With a hand-checked transcript | **28** lectures, **5.15 h** of timed speech (5.23 h of video) |
| Vision only, no transcript | **16** lectures, **3.10 h** |
| Transcribed segments | **609** |
| Segment length | median **24 s**, mean 30.4 s, max 225 s, **83 over 30 s** (the 9 pre-guide files) |
| Words transcribed | **about 39,100** |
| Lecturer A | 9 lectures, 1.51 h, 141 segments, ~126 words/min |
| Lecturer B | 4 lectures, 0.97 h, 39 segments, ~97 words/min |
| Lecturer C | 15 lectures, 2.66 h, 429 segments, ~138 words/min |
| Boards reconstructed in total | **145** across **40** lectures (35 + 10 + 100, the three board roots) |
| Clear-tile fraction over all 145 | median **100%**, mean **98.4%**, worst board **76.6%** |
| Shortest / longest recording | **3.4 min** / **36.4 min** |
| Voice check, all 43 videos with a reference | same lecturer **0.979-0.998**, other lecturers **0.590-0.899**, smallest margin 0.087 |


The 35-board figures in 4.1 (median 97.7% of tiles clear) are the lectures 1-9 subset and are the
ones to quote for that set; the 145-board row above covers every board the project produced,
including the newer lectures and BanglaASR44.

Reproduce: `python scripts/make_result_figures.py --set dataset` (and the two helper functions
directly for the table).

### 1.10 Published Bengali and Banglish models run on our own test clips (2026-09-25, 3060)

**The question.** Chapter 2 compared this work with other systems by quoting the error rates
printed in their own papers on their own data, which is an argument rather than a measurement.
This runs the published models on the same 177 held-out clips as 1.8, with the same references,
the same normaliser (`normalize_banglish`) and the same metric code (`evaluate.py`'s `wer` and
`cer`), so every row sits on one scale.

**Two decisions that make this fair, both of which must be stated whenever the table is used.**
1. Each model decodes under **its own** generation config. `evaluate.py` forces the `en` and
   `transcribe` tokens, which is right for our model and wrong for somebody else's; a Bengali
   model was trained to emit Bengali, and forcing it into English mode would break it for
   reasons that would be our fault. No language or task token is imposed here.
2. The alphabet each model wrote in is counted and reported beside its error rate. Our
   references are romanized, and `normalize_banglish` drops every non-ASCII character, so a
   Bengali-script answer scores near 100 per cent however well the model heard the speech.
   **The error rates in this table are not a ranking of recognition quality.** Read them with
   the script column or they will be misread.

| Model | CER median | WER median | Script written | ASCII kept | Runaway |
|---|---|---|---|---|---|
| `the-blue-panther/whisper-small-benglish` | **89.9%** | **95.8%** | Bengali script 124 clips, mixed 53, romanized 0 | 12% | 0 |
| `bangla-speech-processing/BanglaASR` | **98.6%** | **100.0%** | Bengali script all 177 clips | 2% | 1 |
| `bengaliAI/tugstugi_bengaliai-asr_whisper-medium` | **100.0%** | **100.0%** | Bengali script all 177 clips | **0%** | 0 |
| `arif11/bangla-ASR-v5` | **98.6%** | **100.0%** | Bengali script all 177 clips | 2% | 1 |
| `pr0mila-gh0sh/MediBeng-Whisper-Tiny` | **109.2%** | **146.5%** | Latin 176 clips, empty 1 | 189% | **70** |
| `openai/whisper-large-v3-turbo` off the shelf (from 1.8) | 67.7% | 93.9% | Latin (English translation) | - | see 1.8 |
| **This thesis, large-v3-turbo + LoRA (from 1.8)** | **15.8 / 16.0%** | **42.5 / 41.7%** | romanized Banglish | - | 0 |

**The orthography objection, answered rather than argued with.** The obvious reply to the row
above is that it penalises a model for its alphabet, not its hearing. So every Bengali-script
run in every hypothesis was transliterated to Roman and the clips were scored again, with the
references untouched. Two deterministic transliterations were tried, ITRANS as emitted and
ITRANS with the unpronounced word-final inherent "a" removed, and **the better of the two is
reported for each clip**, which is deliberately generous:

| Model | CER raw | CER transliterated | WER raw | WER transliterated |
|---|---|---|---|---|
| `tugstugi_bengaliai-asr_whisper-medium` | 100.0% | **47.1%** | 100.0% | **90.2%** |
| `whisper-small-benglish` | 89.9% | **66.0%** | 95.8% | **93.3%** |
| `bangla-ASR-v5` | 98.6% | **73.0%** | 100.0% | **97.0%** |
| `BanglaASR` | 98.6% | **73.8%** | 100.0% | **97.3%** |
| `MediBeng-Whisper-Tiny` | 109.2% | 109.2% (already Latin) | 146.5% | 146.5% |
| Off-the-shelf whisper-large-v3-turbo | 67.7% | - (already Latin) | 93.9% | - |
| This thesis (from 1.8) | - | **15.8 / 16.0%** | - | **42.5 / 41.7%** |

Transliteration recovers a great deal, which confirms these models really are hearing the speech
and that most of the raw gap was the alphabet. **The strongest case is the one that must be
quoted:** `tugstugi_bengaliai-asr_whisper-medium` goes from a perfect 100.0 per cent CER, with
not one ASCII character surviving, to **47.1 per cent** once its Bengali is romanized. That is
**better than off-the-shelf whisper-large-v3-turbo (67.7 per cent)**, so it is simply untrue to
say these models are no better than an untuned Whisper. It is still three times the error of the
fine-tuned model (15.8 per cent).

**The defensible claims, and the ones that are not.**
- Defensible: no published model writes romanized Banglish, so none can be dropped into this
  pipeline as it stands. Four of the five write Bengali script; the fifth translates to English.
- Defensible: even after a generous transliteration, the best of them is at 47.1 per cent CER
  against 15.8, and WER hardly moves at all (100.0 to 90.2). Transliteration fixes the alphabet
  and cannot invent Banglish spelling, which has no standard form; the same effect is measured
  directly in 1.6.
- **Not defensible, and an earlier draft of this section said it:** that the transliterated
  baselines "land where off-the-shelf Whisper sits". That was written when only the two weakest
  models had been run, and tugstugi disproves it.
- Not defensible: that these are bad models. They are good at the task they were built for. The
  mismatch is the target orthography and the domain, not their quality.

Reproduce: `scripts/rescore_baselines_transliterated.py`, output
`output/baseline_benchmark_translit.json`. It needs `indic-transliteration`, which is installed
into a scratch directory and put on `sys.path` through `THESIS_SCRATCH_LIBS` so that the 3060's
`thesis_ft` environment is not modified (checked afterwards: torch 2.5.1+cu121, CUDA still
available, package absent from the env).

**What the Benglish model actually produces.** It does code-switch, and it is not a bad model.
It writes the English words in Latin and the Bengali words in Bengali script, which is a
different target from ours, not a failed attempt at ours. Clip `BanglaASR11/seg_000.wav`:

- Reference: `hello everyone, welcome to the second class of digital logic design. so goto class e amra ki dekhechilam? kichu fundamen...`
- Hypothesis: `Hello এর্প্রিভান welcome to the second class of digital logic design সো বতকলাস আমরা কি দেখে ছিলাম কিছু fundamental গেইত...`

`এর্প্রিভান` is the English word *everyone* spelled out in Bengali script. On 124 of the 177
clips the output is majority Bengali script and on the other 53 it is mixed; **not one clip came
back as romanized Banglish.** Only 12 per cent of the reference character count survives ASCII
normalisation. This is the measured form of the novelty claim in Section 2.2.2: the nearest
published model to this thesis solves a neighbouring problem in a different orthography, so a
student who reads Banglish cannot use its output.

**BanglaASR is the stricter case and the more useful row for the thesis**, because it is the
Bengali branch of this project's own earlier pipeline, so it is the "what we had before"
measurement. It writes Bengali script on every one of the 177 clips and does not code-switch at
all: the English technical terms come back in Bengali letters too. The same clip reads
`আলু এ পিভান বলকন্তু দ্য সেক্যান্ড ক্লাস অব ডিজিটাল লজিক ডিজাইন` where the lecturer said
"hello everyone, welcome to the second class of digital logic design". Two per cent of the
reference character count survives ASCII normalisation, and the WER is exactly 100 per cent:
**not one word of any reference was matched.** This is the direct evidence for the claim in the
notes chapter that the old Bengali-script transcript was unusable as input to the summariser.

Reproduce (weights fetched by `scripts/fetch_baseline_models.sh`, which downloads over curl
because a HuggingFace lookup from Python crashes this machine, and over IPv4 because the LFS
CDN's IPv6 route from here stalls in the TLS handshake):

```
bash scripts/fetch_baseline_models.sh F:/thesisP2/models
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1
set THESIS_FT_DIR=F:\thesisP2\ft_work_final5h
F:\thesisP2\envs\thesis_ft\Scripts\python.exe scripts\benchmark_existing_models.py ^
  --models-dir F:\thesisP2\models --batch 8
```

Output: `output/baseline_benchmark.json`, one entry per model with every clip's hypothesis kept.
Decoding all 177 clips takes about 100 s for a whisper-small model on the 3060.

`arif11/bangla-ASR-v5` ships only `pytorch_model.bin`, and transformers 5.12.1 refuses to load a
pickle checkpoint unless torch is 2.6 or newer (CVE-2025-32434). The torch on the 3060 is pinned
at 2.5.1 and must not be touched, so the weights were converted once with
`scripts/bin_to_safetensors.py`, which reads them with `weights_only=True` and writes safetensors.
No environment was modified.

**MediBeng is the third distinct failure mode and the only one that scores above 100 per cent.**
It writes the Latin alphabet, so on the script column it looks like the right kind of output, but
it is a translation system: it renders the lecture into English and pads. Its output runs to
**189 per cent of the reference character count**, 70 of the 177 clips are runaways by
`evaluate.py`'s definition, and the error rates exceed 100 per cent because insertions are
counted. Its model card reports WER 0.01 and BLEU 0.98, which is what synthetic clinical training
data produces; on real spontaneous classroom speech it is the weakest of the three. Transliteration
does nothing for it because it already writes Latin. **This row is the argument against reading
any published error rate as a property of the model rather than of its test set.**

**The other architecture, checked from the output vocabulary rather than by running it.**
wav2vec2 is the other main family for Bengali, and a table of Whisper rows alone invites the
question of whether the finding is an artefact of one architecture. A CTC model can only ever
emit characters that are in its output vocabulary, and that file is a few kilobytes, so the
question is answerable without downloading 1.2 GB of weights:

| Model | Vocabulary | Bengali characters | Latin letters present |
|---|---|---|---|
| `arijitx/wav2vec2-large-xlsr-bengali` | 111 | 74 | 25 of 26 (no `q`) |
| `tanmoyio/wav2vec2-large-xlsr-bengali` | 119 | 71 | 17 of 26 (no h, i, j, k, m, q, x, y, z) |

**This did not come out the way it was expected to, and the honest reading is the narrower one.**
Both vocabularies are Bengali-dominant, and `tanmoyio` **cannot** produce romanized Banglish at
all: without h, i, k, m or y it cannot spell `kichu`, `ami` or `hobe`. But `arijitx` has an almost
complete Latin alphabet, so it is not structurally prevented from writing romanized text, and the
claim "no wav2vec2 Bengali model can write Banglish" would be false. What the vocabularies show
is that these models are built to write Bengali script, not that emitting Latin is impossible for
every one of them. Running `arijitx` is the only way to settle its row and it is queued behind
the Whisper models.

Fetched with `curl .../resolve/main/vocab.json`; counted by Unicode block.

**All five Whisper-family models are run.** `arijitx/wav2vec2-large-xlsr-bengali` is the one
candidate left unmeasured; its vocabulary is in the table above but its weights were not
downloaded, and the thesis says so rather than implying the survey is exhaustive. Note also that
`pr0mila-gh0sh/MediBeng-Whisper-Tiny` now redirects to `The-Data-Dilemma/MediBeng-Whisper-Tiny`;
the repository moved to an organisation account, which matters because Chapter 2 cites it.

### 1.3 Superseded: the leaked split (do not quote)

Kept so the correction is documented. The old run is untouched in
`ft_work_v1_video6_in_train/`; reproduce it with `prepare_data.py --speaker-map v1`.

**Setup.** LoRA adapter on whisper-small. Trained on 70.4 minutes (1.17 h, 219
clips) labelled speaker A, **of which 47 clips (video 6) were in fact speaker B**.
Evaluated on 43.6 minutes (137 clips) from speaker B. Total corpus 1.9 h.
Training takes about 3 minutes on an RTX 3060.

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

Reproduce (superseded split): `THESIS_FT_DIR=<new dir>`, then
`python finetune/prepare_data.py --speaker-map v1 --out <new dir>`, `train_lora.py`,
`evaluate.py`. Done on the 5090 into `ft_work_v1_repro_5090/`: WER 96.7% -> 81.8%.
Artefacts: `ft_work_v1_video6_in_train/eval_whisper_small_1.9h.md` and `.json`

---

## 2. Data-scaling curve — how much transcription effort buys how much accuracy

Same recipe, same held-out speaker, nested subsets with a fixed seed, so the
only variable is the amount of training audio.

### 2.0 Corrected split (current), with the loop safeguard

Speaker A videos 1-5 only; tested on all 184 clips of speaker B (videos 6-9).
Base model: WER median 95.0%, CER median 73.4%.

| Training audio | Clips | WER median | CER median | WER wins, Wilcoxon | CER wins, Wilcoxon |
|---|---|---|---|---|---|
| 0.30 h | 54 | 84.6% | 59.5% | 116/184, p = 2.3e-06 | 136/184, p = 3.2e-11 |
| 0.60 h | 109 | 80.6% | 56.6% | 115/184, p = 4.3e-07 | 145/184, p = 1.3e-15 |
| 0.93 h (all) | 172 | 83.3% | 58.4% | 119/184, p = 4.8e-08 | 142/184, p = 7.9e-14 |

**Read it honestly: the curve is flat within noise after 0.3 h.** Three runs on
the identical 0.93 h gave WER 78.8%, 82.4% and 83.3%, a spread of 4.5 pp, which
is larger than any step on this curve. What the data does support: **18 minutes
of transcribed Banglish already buys most of the gain, and the gain is
significant at every budget.** What it no longer supports: the old claim that
the curve "is still falling steeply at 1.17 h". That claim came from the leaked
split. Whether 8 hours and several speakers move it further is exactly what the
new corpus will answer.

Under greedy decoding the same adapters are erratic (runaway clips 65, 48, 51;
CER z = -2.76, +0.34, -0.64): greedy numbers measure the loops, not the model.

Reproduce: `python scripts/run_scaling_curve.py --hours 0.3 0.6 all --epochs 8 --batch 8 --decode greedy fallback`
Artefacts: `ft_work/curve/scaling_curve.md`, `ft_work/eval_curve_*.json`

### 2.0b Superseded: the curve on the leaked split (do not quote)

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

#### 4.1.1 Speaker3 boards: denser frames (2026-09-22)

Speaker3 (videos 10-13) stands in front of the board far more, and at the default 10 s
frame spacing only 1 of his 10 boards reached 95% clear (worst 59%; the TTL board 67%).
Re-extracting frames every 2 s gives each tile five times as many chances to be seen
clear. At 2 s the erase detector mistakes his movement for erasing, so the eras are taken
from the 10 s run and each is extended to the first erase the 2 s frames detect after it
(`--eras-from ... --extend-to-erase`); ending at the old 10 s boundary cut off "Don't
Fragment", written in the last seconds before the wipe.

| Lecture | 10 s frames | 2 s frames, same eras extended |
|---|---|---|
| BanglaASR10 | 71 / 70 / 67 / 91% | 80 / 90 / 95 / 96% |
| BanglaASR11 | 85 / 59% | 96 / 88% |
| BanglaASR12 | 85 / 83% | 93 / 94% |
| BanglaASR13 | 90 / 99% | 98 / 100% |

Boards at 95% or better: 1 -> 5 of 10; worst 59% -> 88%.

```
python scripts/board_mosaic.py --frames output/speaker3_runs_2s/BanglaASR{n}/ingested/frames --interval 2 \
  --eras-from output/annotation_demo/all9/BanglaASR{n}/mosaic.json --extend-to-erase --save-occluder \
  --out-dir output/annotation_demo/speaker3_2s_hybrid_occ/BanglaASR{n} --json .../mosaic.json
```

The VLM recall numbers in 5.0 used the 10 s boards; these have not been read by the VLM.

**Display clean-up (not a measurement).** Where the lecturer stood for most of an era the
mosaic still shows a faint blocky ghost of him. `scripts/clean_board.py` applies the
"whiteboard mode" of document-scanner apps: flatten the background and fade everything that
is not clearly darker than its surroundings to white, then blank the pixels the mosaic itself
flags as the lecturer (`--mask`, from `--save-occluder`). Every board becomes readable on a
white background; a few dark scraps of shirt remain near the bottom-left of 3 boards, plus the
board frame and a sticker. **This replaces background pixels**, so a cleaned board is not
"unmodified camera output": the strokes are camera pixels, the background is not. Say so
wherever one is shown. Writing that was behind the lecturer for a whole era is still missing;
the clean-up cannot recover it. Automatic cropping to the writing was tried and was not
reliable (leftover specks chain the crop out to the whole board); crop by hand.
Before/after: `output/annotation_demo/speaker3_2s_hybrid_clean/sheet_1.jpg`, `sheet_2.jpg`.

#### 4.1.2 A learned person mask (2026-09-22)

The default lecturer mask (`temporal_person_masks`) is "whatever differs from the usual board".
It fails two ways on Speaker3: when he stands still the usual board contains him, and when the
camera's auto-exposure darkens the frame every pixel differs, so whole frames read as covered
(BanglaASR10 at 4:30: 100% of the writing area "covered" while most of it is visible). Tiles
then skip exactly the late frames that hold the last writing.

`--person-model deeplab+shadow` replaces it with (1) torchvision's pretrained
DeepLabV3-ResNet101 person class, frame by frame, and (2) a shadow mask: board darker than
usual after dividing out each frame's exposure gain, with pen-stroke-thin marks eroded away
(`scripts/person_segment.py`). Same eras, same frames, same tiling.

Checked by eye on all 10 Speaker3 boards (before/after sheets below), **not measured**: the
"% tiles clear" figure is computed with the mask itself, so it is not comparable across masks.
- Writing the old mask lost is recovered: the diagram drawn at the end of the TTL board
  (BanglaASR10 era 3) and "MF -> More Fragment" (BanglaASR11 era 1).
- The network alone leaves the shadow as sharp blocks; with the shadow mask and the display
  clean-up (4.1.1) the boards are as clean as or cleaner than the old method's, with faint
  grey smudges left on some.
- **Lectures 1-9 (35 boards, 10 s frames, the same eras as 4.1):** the new mosaic matches the old
  on every board and recovers a little on some: BanglaASR2 era 2 "Name = R" (old "Name="),
  BanglaASR9 era 1 "sum()" (old "su"), and the BanglaASR6 binary number (the loss in 5.0,
  true value 01011011): old board "0 _ _ _ 1011", new board "0 _ 011011", 7 of 8 digits.
  With the clean-up every one of the 35 is a clean white board. Sheets:
  `output/annotation_demo/all9_deeplab_shadow/compare_1.jpg` ... `compare_6.jpg`, made by
  `python scripts/compare_board_sets.py --old output/annotation_demo/all9 --new output/annotation_demo/all9_deeplab_shadow`.
- **The VLM has now read all 45 new boards (2026-09-23, 5090), and the clean-up does NOT help it:
  93.6% -> 91.7%, better on 1 board, worse on 7.** See the measured comparison below.

**A human check of the newer lectures' boards (2026-09-23): 82 of 98 complete (83.7%), and only
9 boards lose writing the reconstruction should have kept.**

The user went through all 98 boards of lectures 6-9 and 18-43 in
`output/lectures/board_completeness_check.html`, each shown beside two real video frames from the
same time, answering one question — does the clean board contain everything that was written? —
and naming what was missing. Answers: `data/board_completeness_2026-09-23.json`
(sheet built by `scripts/make_board_check_sheet.py`).

| Verdict | Boards | |
|---|---|---|
| **Complete** | **82** | **83.7% of 98** |
| Missing something | 16 | |
| ... writing genuinely lost | 9 | 9.2% |
| ... era cut while the board was being wiped | 4 | the board is half erased in every frame of that era |
| ... camera out of focus for the whole era | 3 | unreadable in the source video, not a reconstruction fault |

**The nine real losses**, with the user's own description: BanglaASR6 era 1 `t4`; BanglaASR8 era 2
`b, t2`; BanglaASR22 era 2 `100`; BanglaASR28 era 8 the word "Hybrid"; BanglaASR32 era 2 numbers;
BanglaASR33 era 4 numbers and era 5 a diagram with arrows and numbers; BanglaASR35 era 1 a diagram;
BanglaASR41 era 1 a VLSM tree, missing entirely. Seven of the nine are single tokens or one
diagram; **BanglaASR41 era 1 is the one bad case**, a whole tree absent.

Counting only the boards whose source frames were usable (dropping the 4 mid-erase and 3
out-of-focus eras): **82 of 91, 90.1%**.

Two faults worth separating, because they have different fixes:

- **Writing lost by the reconstruction (9 boards).** Same causes as 5.0: glare, and strokes that
  appear in only one frame. This is the number to quote for the reconstruction.
- **Era boundaries cut during an erase (4 boards).** Not a mosaic fault at all: `board_mosaic.py`
  ended the era while the lecturer was still wiping, so every frame in it shows a half-erased
  board. Fixable by holding the era open until the wipe finishes; not attempted before the defense.

This does not contradict the other board numbers, which count different things: 4.1's **97.7%
median of tiles fully clear** counts tiles, not whether writing survived, and 5.0's **88.8% item
recall** is a different lecture set, judged by the VLM against answer keys.

**The VLM reading of the new boards — a measured negative (2026-09-23, RTX 5090)**

The clean-up was judged by eye and looked better. Read by the same Qwen2.5-VL-7B with the same
prompt, on the same hand-verified answer keys, it is slightly worse than the old mosaic:

| Set | Boards | Old mosaic | New clean board | Better / worse | Sign test |
|---|---|---|---|---|---|
| Lectures 1-9 | 35 | 334/349 (95.7%) | 329/349 (94.3%) | 0 / 5 | p = 0.0625 |
| Speaker3, lectures 10-13 | 10 | 74/87 (85.1%) | 71/87 (81.6%) | 1 / 2 | p = 1.0 |
| **Combined** | **45** | **408/436 (93.6%)** | **400/436 (91.7%)** | **1 / 7** | **p = 0.0703** |

```
python scripts/transcribe_boards.py --all --source clean
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 \
  --compare-names board_text_mosaic.md board_text_clean.md
python scripts/score_board_recall.py --runs output/speaker3_runs --gt data/board_truth/draft_speaker3 \
  --compare-names board_text_mosaic.md board_text_clean.md
```

Not significant either way, so the honest statement is **no measured difference, with the point
estimate against the clean-up**, not "the clean-up is worse". What changed, item by item:

- **The one gain is the board the clean-up was built for.** BanglaASR10 era 3, the TTL board whose
  end-of-era diagram the old mask lost: 57.1% -> 71.4%, and "Don't Fragment" becomes readable on
  both era 3 and era 4. The 4.1.2 claim above about that board holds.
- **The losses are single fine-detail items**, and they are the kind of thing a clean-up erases:
  long code strings (`weather = input("Today's weather: ")`, `elements = ("Apple", 7, 3.1416, True)`),
  a written-out sentence, the decimal `3.77` on two different boards of BanglaASR9, and on
  BanglaASR13 `20B - 60B`, `2.7` and `Header + Data`.
- **There is almost no headroom to win.** The old mosaic is already at 95.7% on lectures 1-9, and
  37 of the 45 boards score identically on both. A rebuild can lose thin strokes; it cannot gain
  much.

So the clean boards are worth keeping for **how they look** in the notes (every one is a clean white
board, and 4.1.2's eye check stands), not for what the model reads off them. Do not claim the
rebuild improved board reading. The 5.0 headline numbers stay on the old mosaic boards.

**A decode loop, found here.** On BanglaASR10 era 3 the model read the board correctly, then tried
to draw the diagram's diagonal and emitted the same backslash line 512 times: 42,037 characters.
`transcribe_boards.py` now collapses a run of identical lines and records how many it dropped
(`runaway_lines_removed` in the JSON). It changes no score, since repeated backslashes match no
answer-key item; it matters because that text is pasted into the notes prompt. This is the same
failure class as the Whisper runaway that made the compression-ratio safeguard necessary (1.0).

```
python scripts/board_mosaic.py --frames output/speaker3_runs_2s/BanglaASR{n}/ingested/frames --interval 2 \
  --eras-from output/annotation_demo/speaker3_2s_hybrid/BanglaASR{n}/mosaic.json \
  --person-model deeplab+shadow --save-occluder \
  --out-dir output/annotation_demo/speaker3_2s_deeplab_shadow/BanglaASR{n} --json .../mosaic.json
```
Sheets: `output/annotation_demo/speaker3_2s_deeplab_shadow/compare_1.jpg`, `compare_2.jpg`
(old + clean-up | new | new + clean-up). Cleaned boards in `.../speaker3_2s_deeplab_shadow/clean/`.
Generative inpainting was not tried on purpose: it fills the covered area with plausible
pixels, which on a board means invented writing.

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

### 4.3 Occlusion as a pointer — tried, and NOT supported

`scripts/pointer_align.py`. The idea: where the lecturer stands is where the
lecture currently is, so the occlusion mask we already compute is a free
substitute for the gaze tracking that failed. It would give a region-level
alignment between speech and board content.

**The test, which needs no manual labels.** If standing in front of a region
means working on it, that region should hold more ink after the lecturer leaves
than before. Every occlusion episode is therefore measured as ink gained in the
occluded region, against the median ink gained over the identical interval by
the regions the lecturer was *not* standing in front of.

**Result over all 9 lectures, 191 episodes:**

| | |
|---|---|
| Occluded region gained more ink | 101 |
| An unoccluded region gained more | 81 |
| Median paired difference | 9 px |
| Wilcoxon signed-rank | **p = 0.054** |
| Exact sign test | **p = 0.159** |

**This does not support the claim.** A 101 to 81 split is a weak majority, the
sign test is nowhere near significant, and the Wilcoxon sits just the wrong side
of 0.05. Per lecture the result swings wildly, from 20/26 on BanglaASR6 to
**2/21 on BanglaASR8**, which is strongly against.

**Why the test probably measures the wrong thing.** Ink gain detects *writing*,
and a lecturer standing in front of a region is often *explaining* it, adding no
ink at all. BanglaASR8 fits exactly that: it is the DBMS lecture, where a large
table is drawn once and then discussed at length. Those episodes are precisely
the ones where the pointer signal would still be useful for aligning speech, and
they count as failures here. The test is a conservative proxy for attention, not
a measure of it.

**What is true anyway.** The strongest alignments are qualitatively convincing.
At 10:50-12:10 the lecturer stands at region 2, gains 1,993 ink pixels against a
control of 6, and says *"Ekhon ami jodi X-OR er logical circuit dekhi. Eta
dekhte kirokom hoy? A ekta input B arekta input."* The speech is unmistakably
about the region being written.

**How to write this up.** As an attempted extension that did not validate, with
the reason. Do not claim speech-to-region alignment works. Testing it properly
needs the region's *content*, so that spoken terms can be matched against what
is actually written there, and that needs the VLM to read each region, which has
not run. Until then this is a third honest negative result, alongside visual
bias and fusion.

Reproduce: `python scripts/pointer_align.py --all`
Artefacts: `output/pointer_alignment.json`

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

### 5.0 Board-content recall on the hand-verified answer keys — QUOTE THESE (2026-09-22)

On 2026-09-22 the user checked every one of the 45 boards against its image,
**without seeing any model output**: 67 items added, 3 corrected, the disputed
CGPA confirmed as 3.77 from the video frame at 5:00 (commit `76f91c4`; the exact
corrections are in `scripts/apply_board_check_2026_09_22.py`). The scorer was
also tightened: items of 3 characters or fewer, and items marked `whole_word`,
must stand alone, so "CS" is no longer found inside "economics" or "OR gate"
inside "NOR gate". Everything below is rescored on those keys with nothing
regenerated. **These numbers replace those in 5.1 to 5.3, which were computed on
the draft keys; the conclusions did not change.**

**The VLM reading the board, same Qwen2.5-VL-7B, only the prompt changes:**

| Boards | Keyword prompt | Full transcription, raw frame | Reconstructed board | Keyword -> frame |
|---|---|---|---|---|
| 10 boards, lectures 7-9, 194 items | 41.2% | **96.9%** | 97.9% | better on 9, worse on 0, sign p = 0.0039 |
| **35 boards, lectures 1-9, 349 items** | **31.2%** | **88.8%** | 95.7% | **better on 34, worse on 0, sign p = 1.2e-10, Wilcoxon p = 3.7e-07** |
| Speaker3, 10 boards, 87 items | not run | 89.7% | 85.1% | — |

By kind, 35 boards, keyword -> full transcription: numbers **0/67 -> 65/67**,
names 43/47 -> 45/47, code 14/111 -> 90/111, terms 47/94 -> 89/94, phrases
5/30 -> 21/30.

#### The prompt was chosen on the same boards this reports (2026-09-23)

**State this plainly in the thesis.** The keyword-versus-transcription comparison above was scored
on all 35 boards of lectures 1-9, which are the same boards the 88.8% headline is reported on.
There was no held-out set when the prompt was chosen.

To give a number that selection cannot explain, the boards are split by lecture and the choice is
re-made on one half only. **The rule, fixed before any per-half number was looked at: dev = odd
lectures (1, 3, 5, 7, 9), test = even lectures (2, 4, 6, 8).** Split by lecture rather than by
board, because boards within a lecture share a lecturer, topic, camera and whiteboard. Odd/even is
the simplest deterministic rule; no other split was tried.

| Half | Boards | Items | Keyword | Full transcription | Better / worse | Sign test |
|---|---|---|---|---|---|---|
| dev (choose here) | 17 | 173 | 34.1% | 93.1% | 17 / 0 | p = 1.5e-05 |
| **test (report here)** | **18** | **176** | **28.4%** | **84.7%** | **17 / 0** | **p = 1.5e-05** |
| all (the 5.0 headline) | 35 | 349 | 31.2% | 88.8% | 34 / 0 | p = 1.2e-10 |

Full transcription wins on dev, and on the test half, which played no part in that choice, it still
gives **28.4% -> 84.7%, better on 17 of 18 boards and worse on none**. The conclusion does not
depend on the selection.

**The honest limit of this check:** it is a split applied after the original comparison was run,
not a protocol registered before it, so it cannot undo the original selection. It answers the
narrower question - does the prompt still win on boards that played no part in choosing it - and
that is all it should be claimed as. Quote either the 88.8% with the sentence above about
selection, or the 84.7% test-half figure; do not quote 88.8% as if it were held out.

```
python scripts/prompt_selection_split.py
```

#### Model size: Qwen2.5-VL-3B against the 7B (2026-09-23)

Same prompt, same raw-frame boards, same answer keys, only the model changes. This asks whether
the board-reading result needs a 7B model at all.

| Boards | Qwen2.5-VL-3B | Qwen2.5-VL-7B | 7B better / worse | Sign test |
|---|---|---|---|---|
| 35 boards, lectures 1-9, 349 items | 85.4% | 88.8% | 11 / 5 | p = 0.21 (Wilcoxon p = 0.021) |
| Speaker3, 10 boards, 87 items | 77.0% | 89.7% | 5 / 1 | p = 0.22 (Wilcoxon p = 0.075) |
| **Combined, 45 boards, 436 items** | **83.7%** | **89.0%** | **16 / 6** | **p = 0.053** |

**The point worth making: the prompt matters far more than the model size.** Changing the prompt is
worth **+57.6 pp** (31.2% -> 88.8%); going from 3B to 7B is worth **+5.3 pp**, and that gap is not
significant by the sign test on either set separately. A 3B model at 85.4% already carries most of
the board. The 7B is the better model and stays the one reported, but the thesis should not present
model scale as the thing that made board reading work.

The 7B figures here (310/349 = 88.8%, 78/87 = 89.7%) are recomputed from the stored outputs and
match 5.0 exactly, which also checks that the scorer and the keys have not drifted.

**Not run: the larger VL models, and why.** Checked against the Hugging Face API on 2026-09-23:
Qwen2.5-VL-32B-Instruct is **68.3 GB** of weights and Qwen2.5-VL-72B-Instruct is **146.8 GB**. The
5090's D: drive had 62 GB free at the time, with the Qwen3-32B notes model still downloading into
it, so neither fits. Both would also have to be quantised to run in 32 GB of VRAM, which would
confound model size with quantisation loss and make the comparison less clean than the 3B-vs-7B one
above, where both models run in bf16. **So this is a 3B-against-7B ablation, not a scale study, and
the thesis should say exactly that.**

```
python scripts/transcribe_boards.py --all --source frame --model Qwen/Qwen2.5-VL-3B-Instruct --tag 3b
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 \
  --compare-names board_text_frame_3b.md board_text_frame.md
python scripts/score_board_recall.py --runs output/speaker3_runs --gt data/board_truth/draft_speaker3 \
  --compare-names board_text_frame_3b.md board_text_frame.md
```

**Reconstructed board against raw frame:** 35 boards 88.8% -> 95.7%, better on 8,
worse on 3, sign p = 0.23, Wilcoxon p = 0.056; Speaker3 89.7% -> 85.1%, worse on
one board. **A trend on lectures 1-9, not significant, and absent for Speaker3.**
Keep saying: the prompt is what makes the VLM read the board.

**Two limits of the reconstruction the hand check exposed**, worth a sentence each
in the thesis: (1) **glare** from the ceiling lights sits in every frame, so no
choice of frame removes it (BanglaASR8, the CGPA 3.77 cell); (2) **content visible
in only one frame can be lost**: on BanglaASR6 the binary number 01011011 is fully
written only at 3:00, covered at 3:10 and wiped by 3:20, so the reconstruction
fills the middle digits from earlier frames and shows only "0 ... 1011".

**The notes:**

| Notes | 10 boards (7-9), 194 items | 35 boards (1-9), 349 items |
|---|---|---|
| A. original pipeline | 38.7% | 37.2% |
| B. grounded prompt, keyword board input | 25.8% (vs A: better 1, worse 3, p = 0.62) | — |
| C. + VLM board transcription | **95.9%** (vs B: better 8, worse 0, p = 0.0078) | **88.0%** (vs A: better 30, worse 1, p = 3e-08) |
| D. + fine-tuned transcript | 92.3% (vs C: better 1, worse 6, p = 0.12) | — |

A -> C on 10 boards: better on 8, worse on 0, p = 0.0078. By kind on 35 boards,
A -> C: numbers 6/67 -> 65/67, names 19/47 -> 45/47. The readings of 5.3 still
apply: B's drop is the textbook recitation going away; C's jump is mostly the
board transcription passing into the notes; D adds no board recall.

Reproduce every number in this section: `python scripts/rescore_verified_keys.py --json output/board_recall_verified.json`

### 5.4 The annotated notes — the deliverable, measured (2026-09-23, RTX 5090)

The notes a student would actually be handed: one section per board, each pointing at the
numbered coloured boxes the VLM named, the lecturer quoted, a step-by-step walk through the board,
and anything the lecturer did not say confined to a labelled "Background" box. Built for all 13
scored lectures in both languages by `build_lecture_notes.py`, from `transcript_loso.txt` in every
case, so the transcript came from a Whisper adapter that never heard that lecture's lecturer.
**No leakage warnings on any of the 26 files.**

**These are the numbers from the second build (2026-09-23, after two prompt changes: each language
version written wholly in its own language, and the fuller step-by-step explanation with the
Background box).** The first build's numbers are kept below, because the change moved them a lot.

**Board-content recall, 35 boards of lectures 1-9, 349 items:**

| Notes | Recall | Against the original notes (A) |
|---|---|---|
| A. original pipeline | 37.2% | - |
| **New annotated notes, Banglish** | **89.1%** | **better on 32 boards, worse on 0, sign p = 4.7e-10, Wilcoxon p = 8.0e-07** |
| New annotated notes, English | 55.9% | better on 29, worse on 4, sign p = 1.1e-05, Wilcoxon p = 2.1e-06 |
| C. paste the VLM board transcription (5.0) | 88.0% | better on 30, worse on 1 |

**Speaker3, lectures 10-13, 10 boards, 87 items** (no earlier notes exist for these, so this is an
absolute score): Banglish **79.3%**, English 75.9%.

Across all 13 lectures, 436 items: **Banglish 87.2%, English 59.9%.**

**The Banglish notes now match variant C**, which was the previous best: 88.0% -> 89.1%, better on
14 boards, worse on 8, sign p = 0.29, Wilcoxon p = 0.34. **Statistically indistinguishable, and
that is the point.** C reaches its number by pasting the VLM's raw board transcription into the
notes; the annotated notes reach the same number while being a readable lecture note with boxes,
quotes and a step-by-step explanation. The 17.8 pp gap reported after the first build is closed.

**What the two prompt changes did, and the honest caveat.**

| | First build | Second build | Change |
|---|---|---|---|
| Banglish, 35 boards | 53.6% | **89.1%** | **+35.5 pp** |
| English, 35 boards | 70.2% | 55.9% | **-14.3 pp** |
| Banglish, Speaker3 | 67.8% | 79.3% | +11.5 pp |
| English, Speaker3 | 72.4% | 75.9% | +3.5 pp |

**The languages swapped places.** The reason is the language-purity rule. Board content is written
in Banglish and mixed technical English; a Banglish note reproduces those strings as they were
written, so the scorer finds them, while an English note now translates them into English prose,
where the scorer cannot. **This is partly a measurement artefact and must be said as such**: the
English notes did not necessarily get worse for a reader, they got worse at containing the board's
exact strings. The spelling-fair matching of 1.6 has never been applied to this metric and would
probably narrow the gap.

**The caveat that matters for attribution: the two prompt changes landed together**, so this
comparison cannot say how much of the movement is the language rule and how much is the fuller
step-by-step explanation. Separating them needs a third build with one change at a time, which has
not been run. Do not attribute the +35.5 pp to either change alone.

**Quote the Banglish number as the deliverable's result** (89.1%, or 87.2% over all 13 lectures),
and state that the English version trades exact board strings for readability to an English-medium
reader.

```
python scripts/label_boards.py --all
python scripts/build_lecture_notes.py --all --language both --tag 7b
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6   --compare-names final_lecture_notes.md notes_annotated_banglish_7b.md
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6   --compare-names notes_C_vlm.md notes_annotated_banglish_7b.md
python scripts/score_board_recall.py --runs output/speaker3_runs --gt data/board_truth/draft_speaker3   --notes-name notes_annotated_banglish_7b.md
```

#### Two routes to the English notes (2026-09-23)

The user's spec described the English notes as a translation of the Banglish ones; what was built
writes each language straight from the board and the transcript. Both now exist and are scored:

- `--language english` writes English directly from the board and transcript.
- `--language english_via_banglish` writes the section in Banglish, then translates it with the
  same model, keeping the Markdown, tables, box numbers and colours.

**Board-content recall, 35 boards of lectures 1-9, 349 items:**

| Route | Recall | Speaker3 (87 items) | All 13 lectures (436 items) |
|---|---|---|---|
| English, written directly | 55.9% | 75.9% | 59.9% |
| **English, translated from the Banglish** | **89.4%** | **79.3%** | **87.4%** |
| Banglish (the source of the translation) | 89.1% | 79.3% | 87.2% |

**Translating the Banglish notes recovers almost exactly what writing English directly loses**:
89.4% against the Banglish original's 89.1%, and 87.4% against 87.2% over all 13 lectures. That
supports the reading in 5.4 above - the direct-English deficit is the model paraphrasing the
board's strings into English prose, not the notes carrying less of the lecture - and it makes the
user's original spec (English as a translation of the Banglish) the better of the two routes on
this metric.

**The caveat, and it is a big one: the +33.5 pp is carried by four boards.**

| | Boards | Net items |
|---|---|---|
| Dense boards, 39-42 items each (BanglaASR8 eras 2 and 3, BanglaASR9 eras 1 and 2) | 4 | **+113** |
| Every other board | 31 | +4 |

Of the 130 items gained, **113 (87%) come from those four boards**, and across the other 31 the two
routes are level. Counted by board rather than by item the comparison is **10 better, 7 worse,
18 tied, sign test p = 0.63, Wilcoxon p = 0.084 - not significant.** There are real regressions:
BanglaASR4 era 4 and BanglaASR5 era 2 each fall from 6 of 7 items to 2 of 7.

**So state it this way:** the translated route is dramatically better on dense, number-heavy boards,
where writing English directly loses most of the content, and indistinguishable from it on ordinary
boards. Do not quote "89.4% vs 55.9%" without saying that four of thirty-five boards produce almost
all of the difference. This is the same board-count-versus-item-count trap as elsewhere in this
file: the metric is item-weighted, so a handful of dense boards can move it a long way.

**A defect in this route, found and fixed (2026-09-23).** The translation left the section labels in
Banglish: across the 13 files, **97 instances** of `Ek line e:`, `Mone rakho:` and
`Extra jana kotha`, so a page billed as English still showed Banglish headings, and **3 files
returned the one-line summary in capitals**. Recall is unaffected, the labels being structure rather
than board content, but the claim "no Banglish left" did not hold as built.

`scripts/fix_translated_labels.py --apply` maps them without running the model, since the labels are
a fixed set written by our own prompt rather than free text. All 97 labels and all 3 shouted lines
are gone, and the 28 Background boxes now read "Background (not said in the lecture)".

The shouted lines needed care: lower-casing them wholesale would have destroyed "Python", "TTL" and
"DBMS". Each word's casing is instead taken from how the same file writes that word elsewhere,
counting only mid-sentence capitals as evidence, because headings title-case ordinary words and
every sentence capitalises its first. So "THE SECTIONS COVER TTL AND FRAGMENTATION IN NETWORK
PARAMETERS." becomes "The sections cover TTL and fragmentation in network parameters."

```
python scripts/fix_translated_labels.py --dry-run     # what it would change
python scripts/fix_translated_labels.py --apply
```

```
python scripts/build_lecture_notes.py --all --language english_via_banglish --tag 7b
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6   --compare-names notes_annotated_english_7b.md notes_annotated_english_via_banglish_7b.md
python scripts/score_board_recall.py --runs output/speaker3_runs --gt data/board_truth/draft_speaker3   --notes-name notes_annotated_english_via_banglish_7b.md
```

#### Does fine-tuning the ASR improve the notes? A 2x2 (2026-09-24)

The question the user asked: the fine-tuned transcript is much better as a transcript (1.8, CER
67.7% -> 15.8%), but does any of that reach the notes? Four builds, 13 scored lectures, Banglish
only, everything else held constant. The board text is the other input, so it is crossed with the
ASR to see which one the notes actually live on.

**Item totals, 35 boards of lectures 1-9, 349 items:**

| | With VLM board text | Without board text |
|---|---|---|
| **Fine-tuned ASR** | **89.1%** (311) | 70.8% (247) |
| Off-the-shelf ASR | 78.5% (274) | 73.6% (257) |

**The same four cells counted by board, which is the test that matters:**

| Comparison | Item change | Better / worse boards | Sign test | Wilcoxon |
|---|---|---|---|---|
| With board text: base -> fine-tuned | +10.6 pp | 7 / 6 | **p = 1.0** | p = 0.81 |
| Without board text: base -> fine-tuned | -2.8 pp | 10 / 9 | **p = 1.0** | p = 0.72 |
| Fine-tuned ASR: no board -> board text | +18.3 pp | 13 / 7 | p = 0.26 | p = 0.16 |
| Off-the-shelf ASR: no board -> board text | +4.9 pp | 10 / 4 | p = 0.18 | p = 0.052 |

**Not one of the four is significant.** Read the by-board column, not the percentages.

**The headline answer: fine-tuning the ASR does not measurably improve the notes.** With board text
the boards split 7 better and 6 worse; without it, 10 and 9. Both are as close to a coin toss as
the data can get.

**Where the +10.6 pp actually comes from, and it is not the ASR in general.** Of the +37 items,
**two boards of BanglaASR9 give +50 between them**, and across the other 31 boards the fine-tuned
transcript is **13 items worse**. So the one apparently large ASR effect in the table is two boards
out of thirty-five, with the rest pointing gently the other way. Quoting "+10.6 pp" as the benefit
of fine-tuning for the notes would be wrong.

**Why this is not a disappointment, and how to say it.** The board carries the facts the metric
scores; the transcript carries the explanation, which this metric cannot see. 5.0 already found
the same shape (C vs D: adding the fine-tuned transcript to board text changed nothing). So the
honest sentence for the thesis is: **the notes' factual content comes from the vision side, and the
ASR improvement shows up in readability and in the quotes rather than in board recall** - and the
quotes are real, 31 kept word for word across the 13 Banglish files. It is also the reason the
fine-tuning result is reported on its own terms in 1.8, as a transcription result, not as a notes
result.

**The board-text rows are a trend, not a result.** Adding board text is worth +18.3 pp with the
fine-tuned ASR and +4.9 pp with the off-the-shelf one, but by board those are p = 0.26 and p = 0.18
(Wilcoxon 0.052). With 35 boards this metric cannot resolve them. Note the two rows disagree about
where the gain sits: with the fine-tuned ASR, 53 of the 64 items come from the 4 dense boards; with
the off-the-shelf ASR the dense boards contribute -3 and the gain is spread over the other 31.

```
python scripts/build_lecture_notes.py --all --language banglish --transcript-file transcript_base.txt --tag base
python scripts/build_lecture_notes.py --all --language banglish --board-text-file none.json --tag noboard
python scripts/build_lecture_notes.py --all --language banglish --transcript-file transcript_base.txt --board-text-file none.json --tag base_noboard
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6   --compare-names notes_annotated_banglish_base.md notes_annotated_banglish_7b.md
python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6   --compare-names notes_annotated_banglish_base_noboard.md notes_annotated_banglish_noboard.md
```

#### The Background box: does the model put false things in it?

The prompt now asks for standard material the lecturer did not say in a separate
`### Background` section, two to four sentences, and `notes_page.py` renders it as a dashed,
labelled aside so a reader can see it is not the lecture. This is the controlled version of the
failure that produced the old textbook NAND definition: the material is still generated, but it is
fenced and labelled instead of passing as something the lecturer said.

**Read by hand, 2026-09-23, three lectures (BanglaASR1 and 2, Python; BanglaASR6, logic gates),
11 Background boxes: no false statement found.** Spot checks: "`input()` returns a string, so
convert with `int()` or `float()` before arithmetic" (true), "otherwise you get concatenation
instead of addition" (true), "Python is case-sensitive, so `myName` and `MyName` differ" (true),
"an AND gate outputs 1 only when both inputs are 1" (true), "a NOT gate inverts a binary signal"
(true). **This is 11 boxes of 62, checked by one reader; it is not a guarantee.** The honest
statement is that a hand check of a sample found nothing false, not that the boxes are correct.

**The quality criticism that is fair:** the Background boxes are generic and repetitive. Several
end on filler of the form "understanding X is essential for designing more complex systems", and
three different boards of BanglaASR6 each restate what an AND gate does. They are true but carry
little information, which is a readability point the recall metric cannot see.

**Why the better transcript does not win: the metric favours the worse one (2026-09-24, 3060).**
Scoring the two transcripts themselves against the same answer keys, before any notes are written:

| Transcript, 35 boards, 349 items | Board items it contains |
|---|---|
| Off-the-shelf Whisper (CER 67.7%) | **106 (30.4%)** |
| Fine-tuned Whisper (CER 15.8%) | 91 (26.1%), better on 1 board, worse on 9, sign p = 0.021, Wilcoxon p = 0.0069 |

**The far worse transcript carries significantly more of the board's content**, and the mechanism is
mechanical: off-the-shelf Whisper *translates into English*, and the answer keys are largely English
technical strings ("NAND gate", "MySQL", "Create table Student_info", code). Its output is unusable
as a transcript while still emitting those exact strings. The fine-tuned model writes what the
lecturer actually said, in Banglish, and "amra NAND gate dekhbo" does not string-match an English
key item. This is the same trap as the Term F1 finding in section 3: **a measure built out of
English strings rewards a model that translates and penalises one that transcribes.** Report the 2x2
with this beside it, or the null result will be read as "fine-tuning was pointless".

Reproduce: `python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 --compare-names transcript_base.txt transcript_loso.txt`

**What this null result does and does not say.** It says the fine-tuned transcript changes almost
nothing that *board-content recall* can see, and that metric only asks whether facts written on the
board reach the notes. It does **not** say the transcript is irrelevant to note quality: the metric
is blind by construction to whether the explanation around those facts is correct, readable or even
in the right language. The transcripts differ enormously as transcripts - CER 67.7% against 15.8%
(1.8) - and an English page built from a 67% error transcript will contain sentences that are simply
wrong. Nothing here measures that. **Testing it properly needs people**, which is the survey in
NEXT_STEPS: the same lecture's notes from the two transcripts, side by side, "which would you
rather study from". Until that exists, the defensible claim is the narrow one above.

**One defect found and fixed.** The model wrote the heading four different ways - `Background`,
`Background (not said in the lecture)`, `Extra jana kotha`, `Extra jana kotha (lecture e bola hoy
ni)` - and **11 of the 21 boxes in the first rebuild used a bare heading with no disclaimer**. The
heading is what the rendered label shows, so those boxes were fenced but not labelled as
non-lecture content, which is the whole point of the box. `notes_page.py` now normalises the label
at render time, so a shortened heading still carries the disclaimer. All 62 boxes across the 26
pages now read "Background (not said in the lecture)" or "Extra jana kotha (lecture e bola hoy ni)".

**The quote checker, and exactly which files it covers.** In the first build (2026-09-23 morning,
before the language split below) it kept 83 lecturer quotes across the 26 files and deleted 14 that
were not word for word in the transcript, a 14% rejection rate, and left **0 references to a box
that does not exist**.

**Then the design changed, and the claim must be narrowed.** An English-medium reader cannot read a
Banglish quote, so the English notes now quote the lecturer **in English translation**, and a
translation cannot be matched against a Banglish transcript. The word-for-word checker therefore
**does not run on the English files**; it runs on the Banglish ones, which keep the lecturer's real
words. Each file records `quotes_word_for_word_checked` and `quotes_translated`, and its footer says
which it is.

**So the supportable claim is: quotes in the Banglish notes are verified word for word against the
transcript; quotes in the English notes are translations and are not verified.** Do not say "every
quote in the notes is verified".

**Counts from the second build (the current files), 13 lectures per language:**

| | Banglish | English |
|---|---|---|
| Quotes kept, verified word for word | **31** | 0 (not applicable) |
| Quotes deleted as not in the transcript | 8 (a 21% rejection rate) | 0 (checker does not run) |
| Quotes given as translation, unverified | 0 | **27** |
| `quotes_word_for_word_checked` | true, 13 of 13 files | false, 13 of 13 files |
| References to a box that does not exist | 1 | 0 |
| LaTeX rewritten to plain text | 6 | 44 |

The one bad box reference out of 13 Banglish files is worth fixing if there is time; it is counted,
not silent.

**Hand-checked, and the translations held up.** In the Qwen3-32B English notes for BanglaASR7_004,
two quotes looked invented because no string in the transcript matches them. Tracing them back by
hand, both are faithful translations of real lines:

| English quote in the notes | The transcript line it translates |
|---|---|
| "OR plus NOT makes NOR gate." | "toh, inverse version. tar mane **or plus not**, ei duita fundamental gates mile amar **nor gate** ta built hocche" |
| "First we do OR, then apply NOT." | "eitoh, ekhon, **first time a ki kortesi? or kortesi. erpore ami otar opore not kore** ami final nor get ta peracchi" |

So on this page the translation is doing its job. **That is a sample of two, not a guarantee**, and
it is exactly the class of error the automatic check can no longer catch. **If the thesis shows an
English notes page, say its quotes are model translations, not verified transcript text**, and
point at a Banglish page for the verified ones.

**What the checker does and does not cover.** It deletes a *blockquote* whose text is not in the
transcript. A second counter, `inline_quotes_unverified`, flags quoted spans of four words or more
inside ordinary paragraphs that match neither the transcript nor the board, and **only flags them;
it does not delete them**. That count is 47 over the 26 files. Reading them, most are not errors:
they are the English translation lines, which by design do not match a Banglish transcript, and
spans of code caught by the quote regex. So do not claim "every quotation in the notes is
verified". The supportable claim is: **83 block quotes verified word for word against the
transcript, 14 rejected.**

**One real defect, found and fixed here (2026-09-23).** Three times across the 26 files the model
copied the prompt's own example text into the notes instead of leaving the quote out, producing
`The lecturer mentioned, "exact words from the transcript"` in two Banglish files. `check_quotes`
could not catch it, because it looks for quotes that are absent from the transcript and this is
not a quote at all, and two of the three were not blockquotes so the blockquote pattern never saw
them. `strip_prompt_placeholders()` now removes the prompt's placeholder text, taking the whole
line when nothing else is on it and only the introducing clause otherwise, and records
`prompt_placeholders_removed` per board. The two lectures were rebuilt; **recall is unchanged**
(Banglish 53.6% and 67.8% before and after), so the fix is a readability fix, not a scoring one.

### 5.1 Board-content recall — the baseline, and why this metric

*(Numbers in 5.1 to 5.3 were computed on the draft keys and are superseded by 5.0.)*

The generated notes had never been evaluated against anything. `scripts/score_board_recall.py`
scores them on the one thing the summarising model cannot fake: the specific
facts written on the whiteboard.

**Why not any existing metric.** Qwen knows digital logic, Python and database
theory without watching the lecture. The baseline notes for BanglaASR7 print a
correct NAND truth table beside a definition that is plainly wrong, which is
what reciting from memory looks like. Anything scored on general content
measures the model's priors. Term F1 additionally has the problems in 2.1.

What a model cannot invent is that Adiba Noshin has a CGPA of 3.28 and studies
Economics. Recall is the measure, not F1: good notes legitimately contain much
that was never on the board, so precision would punish the desired behaviour.

**Evaluation set.** The 10 boards of BanglaASR7, 8 and 9 — the held-out speaker,
so there is no leakage from ASR fine-tuning. **Keep speaker B in the test set
when the new data lands and this stays valid.** Ground truth drafted from the
reconstructed boards in `data/board_truth/*.json`; every item still needs human
verification before publication.

**Baseline, current pipeline, 167 items over 10 boards:**

| Lecture | Found | Items | Recall |
|---|---|---|---|
| BanglaASR7 (logic gates) | 12 | 21 | 57.1% |
| BanglaASR8 (DBMS) | 25 | 77 | 32.5% |
| BanglaASR9 (SQL) | 30 | 69 | 43.5% |
| **Total** | **67** | **167** | **40.1%** |

**By item kind, and this is the diagnostic part:**

| Kind | Found | Total | Recall |
|---|---|---|---|
| term | 37 | 47 | **78.7%** |
| code | 14 | 28 | 50.0% |
| name | 12 | 40 | 30.0% |
| number | 4 | 47 | **8.5%** |
| phrase | 0 | 5 | **0.0%** |

**Recall falls monotonically with how guessable an item is.** Generic terms the
model already knows survive at 78.7%; the numbers that exist only on the board
survive at 8.5%; the lecturer's own phrasings, such as `same input = 0` and
`different input = 1`, survive at zero. BanglaASR7 scores highest overall
precisely because gate truth tables are textbook content.

That ordering is a validity check on the metric: it behaves the way a measure
of "did board content reach the notes" should behave.

**What the baseline loses.** On BanglaASR9 era 2 the notes contain none of the
query `Select ID, CGPA from Student_Info`, none of its answer `110112 / 3.98`,
and none of the student IDs or CGPAs.

Reproduce the baseline: `python scripts/score_board_recall.py --gt data/board_truth`
Artefacts: `output/board_recall_baseline.json`

### 5.2 The vision-language model reading the board — a measured positive (2026-09-21)

Same model (Qwen2.5-VL-7B-Instruct), same 10 held-out boards, same 167 items,
same scorer. What changes is the prompt: the original pipeline asked for
keywords; `scripts/transcribe_boards.py` asks for a full transcription, every
number exactly, `[illegible]` rather than a guess.

| VLM output scored | Recall | Numbers | Names | Code | Terms | Phrases |
|---|---|---|---|---|---|---|
| Keyword prompt, raw frames (`visual_keywords.json`) | 47.3% | **0/47** | 38/40 | 5/28 | 36/47 | 0/5 |
| Keyword prompt, every per-frame output pooled | 49.1% | — | — | — | — | — |
| **Full transcription, raw frame** | **97.0%** | **47/47** | 38/40 | 27/28 | 47/47 | 3/5 |
| Full transcription, reconstructed board | 98.2% | 47/47 | 38/40 | 27/28 | 47/47 | 5/5 |

**Keyword vs full transcription, raw frames:** better on 8 of 10 boards, worse on
none; exact sign test p = 0.0078, Wilcoxon p = 0.012. **This is the VLM result:
the model reads the board; the keyword prompt threw the content away.** On the
DBMS board it now returns the whole student table, every ID, name, CGPA,
department and date, where the keyword prompt returned name fragments and not
one number.

**Reconstruction adds little on top.** Raw frame 97.0% vs reconstructed board
98.2%: one board better, none worse, sign test p = 1.0. The raw frame used is the
last frame of each era, when the board is fullest, which is often clear enough.
Say so plainly: the reconstruction is a visual deliverable, not the reason the
VLM reads well. Also note the answer key was drafted from the reconstructed
boards, which if anything favours the mosaic.

**Caveats.** (1) The answer key is not yet hand-verified; three items are flagged.
The VLM read the disputed CGPA as 3.77 on one board and 3.7 on the next. (2) Ten
boards from three lectures of one speaker.

#### 5.2b The same comparison on all 35 boards of the 9 lectures (2026-09-21)

An answer key for the other 25 boards (lectures 1-6, 126 items) was drafted by
reading the reconstructed board images, **without looking at any Qwen output**,
and committed before scoring (commit `4fd21d1`, folder
`data/board_truth/draft_lectures1to6/`). The VLM is valid on every lecture,
because it reads images and never touches the audio or the ASR split.

| VLM output, 35 boards, 293 items | Recall | Numbers | Names | Code | Terms | Phrases |
|---|---|---|---|---|---|---|
| Keyword prompt | 34.8% | **0/54** | 43/47 | 8/85 | 46/85 | 5/22 |
| **Full transcription, raw frame** | **91.5%** | **52/54** | 45/47 | 75/85 | 80/85 | 16/22 |
| Full transcription, reconstructed board | 95.9% | 53/54 | 45/47 | 78/85 | 85/85 | 20/22 |

- Keyword -> full transcription (raw frame): better on **32 of 35 boards, worse
  on none**; sign test p = 4.7e-10, Wilcoxon p = 8.0e-07. On the 25 new boards
  alone: 18.3% -> 84.1%, better on 24, worse on 0, p = 1.2e-07.
- Raw frame -> reconstructed board: 91.5% -> 95.9%, better on 7, worse on 2,
  sign p = 0.18, Wilcoxon p = 0.066. **A trend, not significant.** On the 25 new,
  code-heavy boards the gap is larger (84.1% -> 92.9%, 6 vs 2, p = 0.29).
- Notes (5.3 C) on the same 35 boards: 38.9% -> 88.7%, better on 28, worse on 1,
  sign p = 1.1e-07. Notes C for lectures 1-5 use the baseline Whisper transcript,
  not the fine-tuned one, so they carry no speaker-A leakage.

**Caveat that matters for the 35-board numbers:** the 25-board key was drafted
by an AI model (Claude) and is unverified; the original 10-board key was drafted
the same way. Two AI readers can misread the same handwriting the same way, so
human verification of both keys is what makes these numbers publishable.
Reproduce: `python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 --compare-names visual_keywords.json board_text_frame.md`
(`--gt` alone keeps the original 10 boards, so every earlier number is unchanged).

#### 5.2c A third speaker's boards (Speaker3, lectures 10-13, 2026-09-21)

A different room, camera and lecturer. Frames every 10 s were extracted from the
videos (`output/speaker3_runs/*/ingested/frames`), boards reconstructed with the
same `board_mosaic.py` defaults, and a 69-item answer key drafted from the
reconstructions and committed before the VLM ran (`bb1a28d`,
`data/board_truth/draft_speaker3/`).

**The reconstruction does much worse here:** 59-99% of tiles clear, against a
median of 97.7% on lectures 1-9. The eras are short and the lecturer stays in
front of the same part of the board, so there is often no clear view to borrow;
the lecturer remains partly visible, and the board runs off the right edge of the
camera frame. This is a real limit of the method: it needs the lecturer to move.

| VLM, full transcription, 10 boards, 69 items | Recall |
|---|---|
| Raw frame | **89.9%** |
| Reconstructed board | 84.1% |

The reconstruction is equal on 9 boards and worse on one (lecture 13's
fragmentation worked example, 85% -> 65%). There is no keyword baseline for this
speaker: the original pipeline never ran on these videos. What this adds: **the
full-transcription VLM reads a third lecturer's boards at 90%**, including the
fragment offsets 185 and 370, and the reconstruction is not what makes it work.

Reproduce: `python scripts/transcribe_boards.py --run-dir output/speaker3_runs/BanglaASR1N --source frame`
(and `mosaic`) for N = 0..3, then
`python scripts/score_board_recall.py --gt data/board_truth/draft_speaker3 --runs output/speaker3_runs --notes-name board_text_frame.md`.

Reproduce:

```
python scripts/transcribe_boards.py --all --source frame
python scripts/transcribe_boards.py --all --source mosaic
python scripts/score_board_recall.py --compare-names visual_keywords.json board_text_frame.md
python scripts/score_board_recall.py --compare-names board_text_frame.md board_text_mosaic.md
```

### 5.3 The notes, one change at a time (2026-09-21)

Qwen2.5-7B-Instruct, `--language mixed`, all 9 lectures regenerated, scored on
the same 10 boards.

| Notes | What changed | Recall | vs previous row |
|---|---|---|---|
| A. `final_lecture_notes.md` | original pipeline | 40.1% | — |
| B. `notes_B_prompt.md` | grounded prompt, keyword board input | 27.5% | better 1, worse 3, p = 0.63 |
| C. `notes_C_vlm.md` | + VLM full board transcription | **95.8%** | better 8, worse 0, **p = 0.0078** |
| D. `notes_D_full.md` | + fine-tuned transcript (corrected adapter, safeguard) | 92.2% | better 1, worse 6, p = 0.13 |

C vs A directly: better on 8 boards, worse on 0, p = 0.0078. D vs A: 6 and 0,
p = 0.031.

**How to read this honestly.**

- **B went down, not up.** The grounded prompt stops the model reciting a
  textbook, and the textbook was where some guessable terms came from. With
  keywords as the only board input there is nothing better to replace them.
- **C's jump is mostly pass-through.** The notes paste the VLM's board
  transcription into the figures nearly verbatim, so C's recall is close to the
  VLM's own 97%. Claim "board content now reaches the notes", not "the notes are
  better written". Recall does not measure readability.
- **D does not add recall, and should not be expected to.** This metric counts
  board content, which comes from the VLM. The transcript's value is the
  lecturer's words, which this metric does not score.
- **Known defect, visible by reading the notes:** the `mixed` style is meant to
  quote the lecturer 2-5 times. D contains no quotes at all; C labels lines
  copied from the board as "Lecturer:", and one C note pastes a whole paragraph
  of the English baseline transcript. The quote instruction does not work yet.

Reproduce: the three `regenerate_notes.py` commands in NEXT_STEPS.md step 5b,
with `transcript_finetuned_v2.txt` for D, then
`score_board_recall.py --compare-names <before> <after>`.

The fine-tuned transcripts used for D were remade with the corrected adapter:
`scripts/transcribe_finetuned.py --all --adapter <ft_work>/lora_run --decode fallback
--out-name transcript_finetuned_v2.txt`. The older `transcript_finetuned.txt` came
from the leaked adapter and is kept only as a record.

---

### 5.6 Reader study, the first human evaluation of the notes (2026-09-25)

**Twenty readers, one lecture, the two notes shown blind.** The lecture is BanglaASR11
(the `BanglaASR7_004` run folder). Note A was the original pipeline's note
(`final_lecture_notes.md`, English prose, no board images, no box references, 653 words).
Note B was this system's note (`notes_annotated_banglish_7b.md`, board images, numbered
box references, checked quotations, Banglish, 2339 words). Every mention of a model or a
method was stripped from both pages before they were shown, so a reader could not tell
which system produced which page (verified: zero occurrences of Whisper, Qwen, LoRA,
fine-tuned, off-the-shelf or any transcript filename in either page).

| Question | This thesis (B) | Original (A) | Same | of decided | p |
|---|---|---|---|---|---|
| Prefer overall | **15** | 4 | 1 | 15 / 19 | **0.019** |
| Easier to read and understand | 10 | 4 | 6 | 10 / 14 | 0.180 |
| Better layout | **18** | 2 | 0 | 18 / 20 | **0.0004** |
| Explains concepts more clearly | **10** | 2 | 8 | 10 / 12 | **0.039** |

Test: two-sided exact binomial on the readers who expressed a preference, which is the
sign test for a paired preference. Ties are excluded rather than split, the standard
convention and the conservative choice, since each "about the same" removes evidence
rather than adding half a vote to the winner.

**What may be claimed and what may not.**
- Three of the four questions favour this system. **Ease of reading does not reach
  significance** (10 of 14, p = 0.18) and must not be reported as if it did.
- **No correction for multiple comparisons.** Four tests at 0.05 give roughly an 18 per
  cent family-wise error rate. Under Bonferroni (0.0125) **only the layout result
  survives**; the overall preference and the concept question become suggestive. Say so.
- **The comparison moves several things at once**: board images, box references, checked
  quotations, language and three times the length. It measures the pipeline as a whole
  and cannot attribute the preference to any one change.
- **Order was not randomised.** Note A was always shown first. Position bias usually
  favours the first item, so this works against the reported result, not for it.
- **n = 20, one lecture, convenience sample.** A pilot. No reader was asked to study a
  note and then answer questions about the lecture, which is the test that would measure
  learning rather than preference.

Raw responses: `Thesis Defense P3/drafts/thesis/survey.txt` (tab separated, 20 rows).
Reproduce: `python scripts/analyse_survey.py`, which writes `output/survey_results.json`.
The two pages and the key saying which is which:
`scripts/make_survey_pair.py --lecture BanglaASR7_004 --a final_lecture_notes.md
--b notes_annotated_banglish_7b.md --out output/survey_pipeline`.

**This closes the "no human evaluation" gap as a pilot, not as a settled result.** The
thesis text says exactly that in Section 5.2.7 and in the limitations list.

### 5.5 The note-file counters, totalled over every delivered page (2026-09-24)

`build_lecture_notes.py` writes its checks into the `.json` beside every page.
`scripts/count_note_counters.py` adds them up, taking **one deliverable build per lecture per
language** (`_final` if a rebuild exists, else `_7b`, else untagged) and **excluding the
`_base`, `_noboard`, `_base_noboard` ablation builds of 5.4**, which are experiments and not
delivered notes.

| Counter | 13 scored lectures | All 42 lectures with notes |
|---|---|---|
| Banglish: quotes kept, verified word for word | **31** | **106** |
| Banglish: quotes deleted, not in the transcript | **8** (21%) | **26** (20%) |
| Banglish: references to a box that does not exist | **1** | **10** |
| English via Banglish: quotes given as translation | 15 | 60 |
| English via Banglish: quotes dropped as untranslatable | **19** | **49** |
| English via Banglish: references to a box that does not exist | 1 | 10 |
| English written directly: quotes given as translation | 27 | - |

The scored-13 Banglish column reproduces 5.4 exactly (31 kept, 8 deleted, 1 bad box reference),
which is the check that the counter script and 5.4 agree. **42 lecture folders carry notes**, not
43: the run folders mix old and new lecture numbering, so count folders, not lecture numbers.

The untranslatable drops are the largest remaining defect in the English pages. A dropped quote
costs the page a lecturer's voice; it is counted, never silent.

Reproduce:
```
python scripts/count_note_counters.py
python scripts/count_note_counters.py --scored-only
```

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
| Fine-tune WER 96.1% -> 81.8%, CER 75.3% -> 60.7% "on a speaker never seen in training" (and the 77.1% / 57.4% replication, and the 0.3 / 0.6 / 1.17 h curve) | **computed, but on a leaked split**: video 6 is the test speaker and was in training. Use section 1.0: WER 95.0% -> 78.8-83.3%, CER 73.4% -> 54.6-59.4%, with the loop safeguard. The "curve still falling, so more data" argument also goes: the corrected curve is flat within noise after 0.3 h (section 2.0) |
| Baseline Whisper Term F1 = 68.2% | 73.2% |
| Fusion improves baseline by 5.7 pp | +0.7 pp |
| p = 0.003 | p = 0.32 (permutation), 0.36 (Wilcoxon) |
| Cohen's d = 0.96, large effect | d = 0.37, n = 9, unstable |
| "+ Cleaning" stage = 71.5% | no such ablation exists |
| "Visual-Only" mode = 42.3% | the pipeline has no visual-only mode |
| Bias sweep: Light 69.8, Medium 67.1, Heavy 58.4 | see section 3.1 — the real sweep is 8.8% then flat 4.1% |
| Light bias improves over no bias | it halves term recall; optimal bias is 0.0 |
| Figure 6.5 failure modes: phonetic 35%, term confusion 25%, repetition 18%, visual 12%, alignment 10% | **no analysis produced these**. Round numbers summing to 100. Label a sample of errors or drop the figure. Only repetition is measurable today: under greedy decoding 10/184 clips base, 58/184 fine-tuned (corrected split) |
| Per-video transcript lengths in Figure 5.7 (e.g. BanglaASR3 = 16,558 chars) | wrong for 8 of 9 videos; now counted from the files. BanglaASR3 is 3,561. The corpus **total** in the abstract, 73,141, is within 1.7% of the measured 71,885 and can stay |

The hardware claim in the abstract is **correct and stays**: P2 ran on an
NVIDIA RTX 3090, 24 GB (confirmed by the author, 2026-09-20), on the machine
with paths under `C:/Users/T2520785`. The RTX 3060, 12 GB referenced elsewhere
in the repo is the current development machine and is what the P3 fine-tuning
numbers were produced on. Keep the two straight when writing the setup section:
P2 pipeline results come from the 3090, P3 fine-tuning results from the 3060.

If a panellist asks how p = 0.003 was obtained, there is no answer, because no
test was run. That single slide puts every other number in the thesis in doubt,
including the fine-tuning result, which is real. Replace, do not defend.
