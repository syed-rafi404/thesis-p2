# CLAUDE.md — Working Agreement for Thesis P2

This file is the persistent context Claude loads on every session. Keep it short and current. If something here goes stale, fix it — don't add a contradictory note.

---

## What this project is

**Multimodal Banglish Classroom Summarizer** — Undergraduate thesis (P2 phase, complete as of 2026-02-03).
Pipeline: lecture video → audio (Whisper + BanglaASR) + vision (Qwen2.5-VL whiteboard OCR) → fusion → Qwen2.5-7B-Instruct LLM → Markdown lecture notes.

Banglish = code-mixed Bengali + English (Romanized). Standard WER is unsuitable; we use **term-based metrics** (Recall / Precision / F1). Despite older docs, term matching is **exact**, over a fixed 82-term English lexicon; F1 equals the Sorensen-Dice of term counts. See THESIS_DEFENSE.md section 2.

For the full narrative read [README.md](README.md) and [THESIS_CONTEXT_SUMMARY.md](THESIS_CONTEXT_SUMMARY.md). For official results read [P2_REPORT/EVALUATION_SUMMARY.md](P2_REPORT/EVALUATION_SUMMARY.md). Do not duplicate those into this file.

---

## Current status (as of 2026-09-20)

- P2 evaluation: **Term F1 = 73.9%**, Precision = 83.6%, Recall = 66.5% across 9 BanglaASR videos. **NOT frozen** — user confirmed (2026-07-02) the poster and report can be regenerated, so pipeline improvements that change these numbers are allowed. Keep the old results reproducible for before/after comparison.
- The earlier poster-vs-"novelties failed" consistency concern is **resolved** — don't re-raise it.
- **Measured 2026-09-20 on output/live_focused/no_gaze/interval_10s, same term functions as the headline:** `transcript_whisper_baseline.txt` is an **English translation**, not a Banglish transcript (Bengali function words: 3,078 in GT vs 54 in Whisper output). Term F1 is 73.2% baseline vs 73.9% fused, a +0.66 pp gain with exact paired permutation p = 0.32 and Wilcoxon p = 0.36 (n = 9). WER is 82.6% baseline vs 146.8% fused. The global- and temporal-biased transcripts are byte-identical to the baseline for all 9 videos. The vision branch does not affect the scored transcript.
- **Defense is about ONE WEEK out (user, 2026-09-20), 3 team members.** The plan and checklist live in [THESIS_DEFENSE.md](THESIS_DEFENSE.md). Its section 1 code fixes are now **done** (torch import, rouge-score, missing deps, `__init__.py`). The fabricated statistics are also **done (2026-09-20)**: `generate_thesis_figures.py` panels (c) and (d) now compute from `output/fusion_statistics.json`, Figure 6.6 plots the real `output/bias_parameter_sweep.json`, `ABLATION` lost two rows no run produces, `OUTPUT_DIR` no longer points at the T2520785 machine, and the abstract clause now reports the null result. **matplotlib is not installed anywhere on this machine**, so the figures compile-check but cannot be rendered here. User says writing time exists; coding help is the constraint. Active P3 work:
  1. **Whisper LoRA fine-tune on Banglish — DONE as of 2026-09-20, and it works.** Weights re-downloaded (967 MB, verified), `train_lora.py` points at the local copy, training takes ~3 min on the 3060. Adapter: `F:\thesisP2\ft_work\lora_whisper_small`. Step-4 `finetune/evaluate.py` is written and run. On the 137 held-out clips of speaker B, never seen in training: WER median 96.1% -> 81.8%, CER median 75.3% -> 60.7%, Term F1 65.0% -> 76.1%. Fine-tune wins on 86/137 clips for WER (Wilcoxon p = 0.009) and 97/137 for CER (p = 2.2e-05). Report: `ft_work/eval_whisper_small_1.9h.md`. **Read medians, not means**: both models occasionally loop and emit more words than were spoken, which pushes mean error rates over 100% and swamps mean-based tests.
  2. **Scaling curve DONE (2026-09-20).** `ft_work/curve/scaling_curve.md`: 0.3 h -> WER median 91.3%, 0.6 h -> 91.7% (p = 0.92, not significant), 1.17 h -> **77.1% WER / 57.4% CER, 106/137 wins, p = 3.86e-08**. Under an hour buys little; the curve is still falling steeply at the top, which is the argument for the 8 h corpus.
  3. **Run-to-run variance is a finding, see RESULTS.md 2.1.** Two runs on the identical 219 clips give WER median 81.8% vs 77.1% and Term F1 76.1% vs 68.0%. WER/CER are stable and significant in both; **Term F1 swings 8.1 pp**, driven by an 11.4 pp precision swing, because better Banglish transcription emits fewer of the 82 English lexicon words. **Never quote a Term F1 difference under ~8 pp** — that noise floor alone disposes of the +0.7 pp fusion claim.
  4. **[RESULTS.md](RESULTS.md) is the single source of truth for every number.** If a number is not there with a command that regenerates it, it does not go in the paper. Section 7 lists retired (fabricated) claims so nobody re-pastes them.
  5. Thesis chapters 3, 7, 9 in `P2/chapters/` are stubs/empty; `chapter_7.tex` is 0 bytes and **not `\input` in main.tex**.
  6. **Dataset expansion is in flight.** User reported 2026-09-20: 6.5 hours of video in hand, 8+ hours with ground truth expected within days. Not yet on this machine. Transcribers follow [TRANSCRIPTION_GUIDE.md](TRANSCRIPTION_GUIDE.md) v1.0, and every incoming file should be run through `scripts/validate_ground_truth.py` before training. `data/ground_truth/` in the repo still holds only the original 9 files.
- Scope is **undergrad** — keep methodological additions minimal.

---

## What works vs. what doesn't (don't re-litigate these unless asked)

| Component | State | Notes |
|---|---|---|
| Whisper large-v3-turbo ASR (no visual bias) | ✅ Working | Primary transcript |
| BanglaASR (Bengali Unicode) | ✅ Working | Wav2Vec2 fine-tuned |
| Qwen2.5-VL-7B whiteboard OCR | ✅ Working | Structured extraction |
| Qwen2.5-7B-Instruct summarizer | ✅ Working | FP16 batch / 4-bit live |
| Anti-hallucination post-processing | ✅ Working | `src/audio/visual_bias_processor.py` |
| Term-based evaluator | ✅ Working | Headline numbers: `scripts/evaluate_ground_truth.py` (exact match, 82-term lexicon). `src/evaluation/evaluator.py` is a different fuzzy, recall-only evaluator |
| Transliteration fusion (dual-ASR) | ⚠️ Partial | Low similarity (0.02–0.07) |
| Cross-modal verification (CMV) | ⚠️ Partial | Detects errors, doesn't correct |
| Visual bias via LogitsProcessor | ❌ Failed → **disabled** | `output/bias_parameter_sweep.json` (1 lecture, 27 terms): bias off = 8.8% term recall, **every** non-zero strength 0.25–2.0 = 4.1% and byte-identical output. Recorded `optimal_bias: 0.0`. Note `config/live_config.yaml` still defaults `bias_strength: 2.0` |
| YOLOv8-Pose gaze tracking | ❌ Failed | 0 detections across all videos |
| Temporal visual bias | ❌ Abandoned | No gain over global |

**Don't suggest reviving the failed approaches unless the user explicitly raises them.** They are documented as negative results.

---

## Environment

- OS: Windows 11, shell: PowerShell (use PS syntax: `$null`, `$env:VAR`, backtick continuation)
- GPU: **NVIDIA RTX 3060, 12 GB VRAM** (verified via `nvidia-smi`, 2026-09-20). Earlier notes here claimed an RTX 5090 with 32 GB; that is wrong for this machine. Plan VRAM against 12 GB.
- Free disk is tight: about 21 GB on each of C: and F: (2026-09-20). A 16 GB VLM download does not fit comfortably.
- Fine-tuning env: `F:\thesisP2\envs\thesis_ft\Scripts\python.exe` — torch 2.5.1+cu121, transformers 5.12.1, peft, datasets, accelerate, soundfile, jiwer. No bitsandbytes, and none is needed for LoRA.
- No Qwen weights are on this machine; the P2 pipeline runs came from a different PC (paths under `C:\Users\T2520785`), which has an **RTX 3090, 24 GB** (confirmed by the user 2026-09-20). So the abstract's hardware claim is correct. Two machines, do not conflate: **P2 pipeline results = 3090, P3 fine-tuning results = this 3060**.
- Python: the `thesis_v2` conda env referenced by older notes **does not exist on this machine** (only `corner` and `pyenv` under `C:\Users\Rafi\miniconda3\envs`, and `conda` is not on PATH). Working interpreter for everything P3 is `F:/thesisP2/envs/thesis_ft/Scripts/python.exe`. **matplotlib is installed in none of them**, so `scripts/generate_thesis_figures.py` cannot render here.
- Total model footprint ~33 GB; `src/model_registry.py` loads/unloads sequentially. The uncommitted-then-committed 12 GB adaptation (4-bit/8-bit VLM, 14B 4-bit LLM) matches this 3060, but needs bitsandbytes, which is not installed.
- Repo root: `f:\thesisP2\thesisP2`
- Git note: repo has a "dubious ownership" warning on this machine. For git reads, pass it per command (`git -c safe.directory=F:/thesisP2/thesisP2 status`) rather than changing global config. Only run `git config --global --add safe.directory F:/thesisP2/thesisP2` after confirming.
- Commits: five landed 2026-09-20 covering work up to that point; the tooling listed below is **not yet committed**. Nothing is pushed automatically; check `git status -sb`.

---

## New tooling (2026-09-20)

Written this session, all standalone, none touch the P2 pipeline:

| Script | What it does |
|---|---|
| `finetune/evaluate.py` | Base vs LoRA on held-out clips: WER/CER median and mean, term metric, Wilcoxon and sign tests, runaway-clip count |
| `scripts/compute_fusion_stats.py` | Recomputes every ASR number from saved transcripts. Replaces the hard-coded `p = 0.003` and `+5.7 pp`. Real answer: **+0.66 pp, p = 0.32**, and all 9 fused transcripts are byte-identical across frame intervals |
| `scripts/validate_ground_truth.py` | Checks incoming transcripts against TRANSCRIPTION_GUIDE.md: 30 s limit, timestamp format, gaps, ASCII, spelling list, speaking rate, filler rate. `--fix` repairs only meaning-preserving issues |
| `scripts/run_scaling_curve.py` | Trains and evaluates across training-set sizes, writes `ft_work/curve/scaling_curve.md` |
| `scripts/illustrate_notes.py` | Adds annotated frames to generated notes, rebuilding the board with the lecturer removed |

`finetune/prepare_data.py` now reads Speaker IDs from file headers, splits by speaker rather than
video number, extracts audio from raw video with ffmpeg when needed, supports `--train-hours` for
scaling curves, and writes `split.json`. Regression-checked: reproduces the original 219/137 split exactly.

`finetune/train_lora.py` takes `--data-dir`, `--train-file`, `--test-file`, `--adapter-out`, `--model`, `--seed`.

---

## Entry points

```powershell
# Single video, full pipeline
python run_thesis.py "data\raw\lecture.mp4" -o "output\my_lecture"

# Live mode (4-bit LLM, lower VRAM)
python run_thesis.py "data\raw\lecture.mp4" --live --interval 45

# Mock VLM, no gaze (fast iteration)
python run_thesis.py "data\raw\lecture.mp4" --mock --skip-gaze

# Batch over data\raw\
python batch_process.py
python batch_process.py --limit 3

# Official P2 evaluation. evaluate_ground_truth.py reproduces the headline numbers (per THESIS_DEFENSE.md, not re-run 2026-09-20).
# p2_evaluation.py writes to a hard-coded C:/Users/T2520785 path from another machine.
python scripts\evaluate_ground_truth.py
python scripts\p2_evaluation.py
python scripts\evaluate_existing_transcripts.py
```

Configs: `config\config.yaml` (FP16 batch), `config\live_config.yaml` (4-bit live).

---

## How to work in this repo

- **Treat the pipeline as a working artifact.** It produced the reported numbers. Edits that touch ASR, fusion, evaluator, or summarizer should be discussed before being made.
- **`scripts/` is exploratory.** Many one-off evaluation/analysis scripts live there. It's fine to add new ones; don't delete old ones without checking — they're part of the experimental record.
- **`output/` is full of past runs.** Don't clean it up. Specific dirs like `output/comprehensive/`, `output/live_focused/`, `output/L1..L7/`, `output/test_*/` are evidence of prior experiments.
- **`data/ground_truth/`** holds the manually transcribed reference text — treat it as read-only.
- **Models are heavy.** Don't run the full pipeline just to "verify" a small change — use `--mock --skip-gaze` or hit a single module's unit path.
- **Romanization is non-standard.** Multiple spellings of the same Bengali word are valid; that's why WER is excluded. When generating examples or test strings, follow what already appears in transcripts and ground truth.
- **No emoji in code or new docs** unless the user explicitly asks. (Existing files have some — leave them.)

---

## Open threads / known gaps

- Thesis chapters 3, 7, 9 are stubs (1, 2, 5, 6 have content); no chapter_4/chapter_8 files exist — confirm the required chapter list against the BRAC template.
- Dataset expansion to ~8 hours is under way; transcription effort (~5–8× real time) is the bottleneck. When it lands: run the validator, then `prepare_data.py --test-speakers <ids>`, then `scripts/run_scaling_curve.py --hours 2 4 6 8`.
- **Defense is ~1 week out as of 2026-09-20**, not a month. Priorities in order: the fine-tune result (done), honest statistics (done), chapters 3/7/9 (writing, user says there is time), illustrated notes as the visible contribution.
- Validator output on the existing 9 ground-truth files: 95 errors, 63 warnings. Mostly segments over the 30 s Whisper window, plus smart quotes and a few spellings that contradict the guide. Ground truth is read-only; do not auto-fix without asking.
- Transliteration fusion similarity scores are low — open question whether to improve or document as a limitation.
- `THESIS_P2_PROGRESS_LOG.md` is 0 bytes in the working tree. The 525-line version is in HEAD and a 2026-02-03 copy is in `Read Me/`; THESIS_DEFENSE.md cites its line 515.
- `config/config.yaml` and `src/model_registry.py` still default to Qwen2.5-14B, `gpu_memory_gb: 12` and `enable_wer: true`, contradicting the documented 7B setup (THESIS_DEFENSE.md section 5).
- Gaze tracking is a documented negative result; revisiting it would need a different model or different recordings.

---

*Maintained by Claude. Last refreshed: 2026-09-20 (fine-tune trained and evaluated; fusion statistics computed; GPU corrected to RTX 3060 12 GB; validator, scaling-curve and illustration tooling added).*
