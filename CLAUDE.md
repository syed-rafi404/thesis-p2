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
- **Defense ~October 2026 (weeks away as of 2026-09-20), 3 team members.** The plan and checklist live in [THESIS_DEFENSE.md](THESIS_DEFENSE.md). As of 2026-09-20 none of its section 1 / section 6 "now" items are done, including the hard-coded `p = 0.003`, `Cohen's d = 0.96` and `+5.7 pp` claims in `scripts/generate_thesis_figures.py` and `P2/core/abstract.tex`. Active P3 work:
  1. **Whisper LoRA fine-tune on Banglish** — scripts in `finetune/`, prepared data at `F:\thesisP2\ft_work` (219 train clips / 70 min speaker A, 137 test clips / 44 min speaker B, speaker-independent split). PoC still blocked: `ft_work/models/whisper-small/model.safetensors` is truncated (20 MB of 967 MB, header-checked 2026-09-20), so re-download before pointing `train_lora.py` at it. No adapter trained. Step-4 `evaluate.py` not yet written; for Term-F1 comparable to 73.9% it must reuse the term functions in `scripts/evaluate_ground_truth.py`, not `src/evaluation/evaluator.py`.
  2. Thesis chapters 3, 7, 9 in `P2/chapters/` are stubs/empty; `chapter_7.tex` is 0 bytes and **not `\input` in main.tex**.
  3. ~5× dataset expansion, gated on the fine-tune PoC showing gains on the existing data first. Transcribers follow [TRANSCRIPTION_GUIDE.md](TRANSCRIPTION_GUIDE.md) v1.0. `data/ground_truth/` still holds only the original 9 files (2026-02-03).
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
| Visual bias via LogitsProcessor | ❌ Failed → **disabled** | Causes hallucinations |
| YOLOv8-Pose gaze tracking | ❌ Failed | 0 detections across all videos |
| Temporal visual bias | ❌ Abandoned | No gain over global |

**Don't suggest reviving the failed approaches unless the user explicitly raises them.** They are documented as negative results.

---

## Environment

- OS: Windows 11, shell: PowerShell (use PS syntax: `$null`, `$env:VAR`, backtick continuation)
- GPU: NVIDIA RTX 5090, 32 GB VRAM, CUDA 12.4 (upgraded from RTX 3090 24 GB — older code may still assume 24 GB)
- Python: 3.10, conda env `thesis_v2`. The fine-tune scripts run in a separate env at `F:/thesisP2/envs/thesis_ft`
- Total model footprint ~33 GB; `src/model_registry.py` loads/unloads sequentially to fit 24 GB
- Repo root: `f:\thesisP2\thesisP2`
- Git note: repo has a "dubious ownership" warning on this machine. For git reads, pass it per command (`git -c safe.directory=F:/thesisP2/thesisP2 status`) rather than changing global config. Only run `git config --global --add safe.directory F:/thesisP2/thesisP2` after confirming.
- All work through 2026-09-20 is committed locally (five commits after the February P2 merge). Push status: check `git status -sb`; nothing is pushed automatically.

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
- Larger / more-diverse dataset (~5×) planned, gated on the fine-tune PoC; transcription effort (~5–8× real time) is the bottleneck.
- Transliteration fusion similarity scores are low — open question whether to improve or document as a limitation.
- `THESIS_P2_PROGRESS_LOG.md` is 0 bytes in the working tree. The 525-line version is in HEAD and a 2026-02-03 copy is in `Read Me/`; THESIS_DEFENSE.md cites its line 515.
- `config/config.yaml` and `src/model_registry.py` still default to Qwen2.5-14B, `gpu_memory_gb: 12` and `enable_wer: true`, contradicting the documented 7B setup (THESIS_DEFENSE.md section 5).
- Gaze tracking is a documented negative result; revisiting it would need a different model or different recordings.

---

*Maintained by Claude. Last refreshed: 2026-09-20 (verified repo state: exact-match metric, truncated whisper-small, defense checklist still open, no commits since Feb).*
