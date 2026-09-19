# THESIS_DEFENSE.md — Living Plan to Defense

Working tracker for the run-up to defense (~Oct 2026). Updated as decisions land.
Keep this current; when something here goes stale, edit it rather than appending a contradiction.

Scope note: this file is the *plan*. Official P2 numbers stay in `P2_REPORT/`.
Narrative and history stay in `README.md` / `THESIS_P2_PROGRESS_LOG.md`.

Last updated: 2026-09-20 (corrected §0 whisper-small row, §3.2, §3.3)

---

## 0. Where things actually stand (measured, not remembered)

Verified 2026-08-05 by reading `F:\thesisP2\ft_work\manifest.jsonl` and `data/ground_truth/`.

| Fact | Value |
|---|---|
| Usable transcribed audio (clipped) | **1.90 h** (train 1.17 h / test 0.73 h) |
| Clips | 356 (219 train / 137 test) |
| Ground-truth tokens | 12,890 romanized tokens, 1,412 unique |
| Bengali-script leakage in GT | **0 tokens** — GT is cleanly romanized |
| Spelling drift across annotator | **Low** (see §4.1) |
| LoRA adapter trained | **No** — `ft_work/lora_whisper_small/` does not exist |
| `whisper-small` local copy | **Truncated** — `model.safetensors` is 20 MB of 967 MB (safetensors header check, 2026-09-20). Re-download needed. |
| Target dataset | 20–25 h |

The gap is **~10–13x more data**, not 2x. Plan accordingly (§3).

---

## 1. Defense-critical fixes (do these first, they are cheap)

These are correctness problems that an examiner can find in minutes. None require GPU time.

| # | Issue | Location | Status |
|---|---|---|---|
| 1 | `torch` used but never imported at module level → `NameError` on any non-live run | `run_thesis.py:158` (import sits at `:972`) | [ ] |
| 2 | `requirements.txt` pins `rouge==1.0.1`, but every script imports `rouge_score` (different package) → eval scripts fail on a clean install | `requirements.txt:129` | [ ] |
| 3 | `jiwer`, `nltk`, `ultralytics` imported but absent from `requirements.txt` (all try/except-guarded, so they fail *silently*) | `requirements.txt` | [ ] |
| 4 | Missing `__init__.py` in `src/evaluation/` and `src/research/` (inconsistent with the other 5 packages) | `src/` | [ ] |

### 1.1 The one that matters most

`scripts/generate_thesis_figures.py:506-526` renders these into a thesis figure:

```python
f1_vals      = [68.2, 71.5, 73.9]
improvements = [0, 3.3, 5.7]
...
ax4.text(..., 'p = 0.003 **', ...)
ax4.text(..., "Cohen's d = 0.96 (Large Effect)", ...)
```

**No statistical test exists anywhere in the repo.** Grep for `scipy.stats`, `ttest`, `wilcoxon`,
`mannwhitneyu`, `bootstrap`, `permutation_test` returns nothing (`scipy` is installed but never
used for this). The `68.2` baseline has no corresponding artifact on disk, and the abstract's
"cross-modal fusion improving baseline Whisper performance by 5.7 percentage points"
(`P2/core/abstract.tex:2`) traces back only to this hard-coded literal.

**This must be resolved before defense.** Two honest options:

- **(a) Compute it.** Score `transcript_whisper_baseline.txt` vs `transcript_fused.txt` with the
  same evaluator across the 9 videos, then run a paired test (Wilcoxon signed-rank, n=9) and report
  the real delta and real p-value — whatever they turn out to be. Both files exist in every
  `output/live_focused/no_gaze/interval_*/<video>/`, so this is a scripting job, no GPU.
- **(b) Remove it.** Delete panel (c) and (d) from the figure, and drop the "5.7 percentage points"
  clause from the abstract.

Option (a) is strictly better if the delta survives. Do (a), fall back to (b).

### 1.2 Sample size

`transcript_fused.txt` is **byte-identical across all three frame intervals**
(MD5 `CFD35922...` for BanglaASR1 at 10s/20s/30s, 17,601 bytes each). The frame interval changes the
visual/summarization branch, not the transcript being scored — so the 27 "runs" are 9 measurements
scored three times, and `avg27 == avg9` for every ASR metric.

Report **n = 9**. Describing 27 as "statistical validity"
(`THESIS_P2_PROGRESS_LOG.md:515`) will not survive a question.

---

## 2. What the headline metric actually measures

Not a fix — a **wording** problem. The numbers are real and reproducible
(`scripts/evaluate_ground_truth.py` regenerates them exactly), but they are described inaccurately.

`extract_technical_terms()` (`evaluate_ground_truth.py:166`) does:

```python
words = re.findall(r'\b\w+\b', text_lower)
count = words.count(term.lower())      # exact match
```

So the term metric is:

- **exact string matching**, not fuzzy. `rapidfuzz` is used only for the separate
  `fuzzy_similarity` number, never for term matching.
- bounded by an **82-word hard-coded English whitelist** (`:64-87`) containing
  **zero romanized-Bengali terms**, and — for the DBMS videos — zero SQL terms
  (`select`, `join`, `table`, `query` are all absent; `boolean` and `logic` are the only gate-adjacent hits for DLD).
- algebraically the **Sørensen–Dice coefficient of two word-count histograms**:
  with `M = Σ min(gt_t, asr_t)`, F1 `= 2M/(G+A)` — verified exact to 3 decimals on all 9 videos.

Consequence for precision: the ASR emits fewer whitelist tokens than GT in **9/9** videos
(mean A/G = 0.796). When `A < G`, `M` is pulled toward `A`, so `precision = M/A` is driven upward
mechanically. **83.6% precision partly reflects under-emission, not correctness.** It also cannot
detect a hallucinated term that is outside the whitelist — which is exactly the failure mode the
visual-bias experiment produced.

**Action:** rewrite the metric definition in Ch. 5 to say what it does — *"count-overlap agreement
(Sørensen–Dice) over a fixed technical-term lexicon, exact match"* — and state the whitelist
limitation explicitly as a threat to validity. Do **not** claim it "accommodates transliteration
variance through fuzzy matching"; that claim is currently made in `README.md:59`,
`chapter_1.tex:153`, and `chapter_2.tex:492`, and the code does not support it.

This is a cheap fix that turns a discoverable weakness into evidence of rigor. Keep the numbers.

---

## 3. Fine-tuning plan at 20–25 h

The existing `finetune/` scripts are well-built and the design (speaker-independent split, timestamp
parsing instead of forced alignment, deterministic label normalization) is sound. What changes at
10x data is the **target model** and the **annotation protocol**.

### 3.1 Model target moves up

At 1.9 h, `whisper-small` + LoRA is correct — anything larger overfits.
At 20–25 h on a 32 GB 5090, the right target is **`whisper-large-v3` + LoRA**.

| | Now (1.9 h) | At 20–25 h |
|---|---|---|
| Base | `whisper-small` (244M) | **`whisper-large-v3`** (1.55B) |
| Why | avoids overfit on tiny data; fast loop | 20 h is enough to adapt a large model without collapse |
| LoRA | r=16, `q_proj`/`v_proj` | r=32, add `k_proj`/`o_proj`, lr 1e-4 |
| Fits 32 GB? | trivially | yes — bf16 + grad checkpointing + 8-bit optim, batch 8 |

Keep `whisper-small` as the **fast iteration loop** (a full run is minutes). Only promote a recipe
to large-v3 once it wins on small. Do not fine-tune large-v3 as the first experiment.

Note `train_lora.py:130` sets `fp16=True`. On a 5090 (Blackwell), switch to **`bf16=True`** — it is
more numerically stable for Whisper and the hardware supports it natively.

### 3.2 Unblock the PoC now (do not wait for 20 h)

The smoke test died in `huggingface_hub` network code, not in the training logic.
**Correction 2026-09-20:** `ft_work/models/whisper-small/model.safetensors` is **not** complete —
it is 20,008,960 of 966,995,080 bytes (2.1%). Re-download it first (e.g. `huggingface-cli download
openai/whisper-small --local-dir F:\thesisP2\ft_work\models\whisper-small`), confirm the file is
~967 MB, then apply the one-line fix:

```python
# finetune/train_lora.py:38
MODEL = r"F:\thesisP2\ft_work\models\whisper-small"   # was "openai/whisper-small"
```

or set `$env:HF_HUB_OFFLINE=1`. Then:

```powershell
python finetune\train_lora.py --smoke     # 2 steps, proves the pipeline
python finetune\train_lora.py             # full run, writes the adapter
```

**Getting a trained adapter on the current 1.9 h is worth doing this week**, even if the result is
weak. It de-risks the whole P3 story: if the plumbing works end-to-end at 1.9 h, scaling is a data
problem, not an engineering problem. A negative result at 1.9 h is also publishable context
("adaptation requires >N hours").

### 3.3 Step 4 (`evaluate.py`) is still unwritten — write it before the data lands

It must reuse the term functions in `scripts/evaluate_ground_truth.py` (`TECHNICAL_TERMS`,
`extract_technical_terms`, `compute_term_metrics`) so fine-tuned numbers are directly comparable
to the 73.9% baseline. **Not** `src/evaluation/evaluator.py`: that is a different evaluator
(fuzzy `partial_ratio >= 85`, recall only) and did not produce the headline numbers. Minimum contents:

- decode held-out speaker-B clips with base vs. adapter
- score both with the **same** term metric (and report the Dice caveat from §2)
- add **normalized WER** as a secondary metric — see §4.2
- paired test across clips, report effect size

Without step 4 there is no way to claim the fine-tune helped.

---

## 4. Data expansion: the actual bottleneck

### 4.1 Annotation consistency is currently good — protect it

Measured across all 9 GT files: **0 Bengali-script tokens**, and the apparent "variants" are real
Bengali inflections rather than spelling drift:

```
kore 114 | korte 90 | korbo 50 | kori 36 | kora 28 | korchi 8     <- morphology, correct
hocche 88 | hoy 78                                                 <- distinct words, correct
```

That consistency exists because **one person** transcribed everything. Going to 20–25 h means
multiple annotators, and that is where romanization drift (`amra`/`aamra`/`amara`) will enter and
directly become label noise in the fine-tune.

**Freeze a romanization style guide before mass transcription starts.** This is the highest-leverage
action available right now and costs a day. Minimum:

- one canonical spelling per common function word (a starter list falls out of the 1,412-token vocab already collected)
- rule for English technical terms inside Bengali sentences (keep English spelling: `variable`, not `bhariyebol`)
- rule for Bengali inflectional suffixes (keep them attached: `classero`, not `class ero`)
- rule for numerals, code identifiers, and spoken punctuation
- 10-minute overlap sample transcribed by every annotator, to measure inter-annotator agreement once

Also: the GT template header (`# INSTRUCTIONS:` ... `# Example: [0:00-0:30] Assalamualaikum...`)
contains example timestamps. `prepare_data.py:101` already strips `#` lines *before* regex-matching,
so those examples do not leak in as fake segments — that guard is correct and must be preserved in
any new tooling.

### 4.2 Add normalized WER as a secondary metric

The "WER is invalid for Banglish" position is sound as stated, but at 20 h with a fine-tune, WER
becomes the metric reviewers will expect. The defensible middle ground: report **WER after
deterministic normalization** — the exact `normalize_banglish()` already in
`finetune/prepare_data.py:62` (lowercase, unify punctuation, strip non-ASCII, collapse 3+ runs), and
optionally with `COLLAPSE_VOWELS=True` to fold `amar`/`aamar`.

Frame it as: *"raw WER is uninformative under free romanization; we report normalized WER, defined
by an auditable public normalizer, alongside term-level metrics."* That is stronger than excluding
WER entirely, and it costs nothing — `jiwer` is already wired in (once §1 fix 3 lands).

### 4.3 Effort math — read this before committing to 25 h

At the documented 5–8x real-time transcription rate:

| Target | Human hours | Split 3 ways |
|---|---|---|
| +10 h audio | 50–80 h | 17–27 h each |
| +20 h audio | 100–160 h | 33–53 h each |
| +25 h audio | 125–200 h | 42–67 h each |

Defense is ~2–3 months out and thesis chapters 3, 7, 9 are still stubs (7 is 0 bytes and not
`\input` in `main.tex`). 25 h of transcription **and** three chapters **and** a large-v3 fine-tune
is not obviously reachable.

**Recommendation:** commit to **8–10 h** as the defense-scope target (a genuine 4–5x expansion,
enough to show a real scaling curve), and present 20–25 h as future work. If transcription outruns
that, great — the pipeline scales. Do not let a 25 h commitment eat the chapters; an unfinished
thesis with a big dataset defends worse than a finished one with a modest dataset.

**Prioritize new speakers over new hours.** The current split is 1 speaker in train, 1 in test.
Going 2 h -> 10 h with 6 speakers is worth far more than 2 h -> 25 h with 2 speakers, because it is
the only way to support a generalization claim. Same for domains: more DBMS/DLD balances the
Python-heavy set.

---

## 5. Models on the 5090 (32 GB)

Decision: **no VLM download for now** (user, 2026-08-05). Recorded here for the record.

| Component | Current | Verdict |
|---|---|---|
| ASR | `whisper-large-v3-turbo` | **Keep.** Changing the base invalidates the 73.9% baseline. The fine-tune is the upgrade path. |
| ASR (Bengali) | `BanglaASR` | **Keep.** Fusion similarity is 0.02–0.07; swapping it does not fix that. |
| VLM | `Qwen2.5-VL-7B` | **Deferred.** A larger VLM improves whiteboard OCR, but it is not on the critical path and would require re-running the visual branch. |
| LLM | `Qwen2.5-7B-Instruct` | **Keep for now.** Summarization quality is not rigorously evaluated, so an upgrade buys no defensible number. |

On closed models (Kimi, GPT-4V, Gemini): **do not adopt.** A thesis contribution that depends on a
proprietary API is not reproducible, and it would undercut the benchmark contribution — which is
currently the strongest thing in the project.

Config drift to fix while here: `config/config.yaml` declares `Qwen2.5-14B-Instruct`,
`gpu_memory_gb: 12`, and `evaluation.enable_wer: true` — all three contradict the documented setup
(7B, 32 GB, WER excluded). `model_registry.py:201` also defaults to `Qwen2.5-14B-Instruct` while
README says 7B. Reconcile before anyone tries to reproduce from config.

---

## 6. Ordered plan

**Now (this week, no GPU needed)**
- [ ] §1 fixes 1–4 (torch import, `rouge-score`, missing deps, `__init__.py`)
- [ ] §1.1 decide (a) compute or (b) remove the `p=0.003` / `d=0.96` / `+5.7pp` claims
- [ ] §1.2 switch all reporting from n=27 to n=9
- [ ] §3.2 point `MODEL` at the local `whisper-small`, run `--smoke`, then a full run

**Next (2 weeks)**
- [ ] §4.1 write and freeze the romanization style guide **before** mass transcription
- [ ] §3.3 write `finetune/evaluate.py` on top of `src/evaluation/evaluator.py`
- [ ] §2 rewrite the metric definition in Ch. 5 + add the whitelist threat-to-validity paragraph
- [ ] §4.2 add normalized WER alongside term metrics

**Then (ongoing)**
- [ ] Transcribe toward 8–10 h, prioritizing **new speakers**
- [ ] Re-run the fine-tune at each of ~4 h / ~7 h / ~10 h to produce a **data-scaling curve**
      (this is a genuinely defensible result regardless of whether the fine-tune wins)
- [ ] Promote the winning recipe to `whisper-large-v3` once it beats base on small
- [ ] Chapters 3, 7, 9

---

## 7. Defense Q&A — the questions that will actually be asked

Prepare real answers for these. Each maps to something above.

1. *"Your F1 uses a fixed 82-word English list. How is that a Banglish metric?"*
   -> §2. Answer honestly: it measures technical-term capture, the lexicon is a limitation,
   here is the normalized-WER number as a complement.
2. *"Where does p = 0.003 come from?"*
   -> §1.1. Either show the paired test, or the claim is gone by then.
3. *"You report 27 runs. Are they independent?"*
   -> §1.2. No. n = 9. Say so first, before being asked twice.
4. *"Precision 83.6% but recall 66.5% — is the system accurate or just quiet?"*
   -> §2. Partly quiet: it under-emits in 9/9 videos, which inflates precision. Acknowledge it.
5. *"Two of six contributions failed. What did you learn?"*
   -> Strongest answer in the project. Self-reinforcing bias loops; verification-after beats
   biasing-during. This is a real finding — lead with it rather than defending it.
6. *"One speaker in training. Will this generalize?"*
   -> §4.3. No claim of generalization is currently supported; that is exactly why expansion
   prioritizes speakers over hours.

---

*Maintained alongside CLAUDE.md. When a checkbox lands, tick it here and update §0.*
