# CLAUDE.md — Working Agreement for Thesis P2

This file is the persistent context Claude loads on every session, on any machine. It is also
the handoff: a session on a new machine has none of the earlier conversation, only this file,
[NEXT_STEPS.md](NEXT_STEPS.md) and [RESULTS.md](RESULTS.md). Keep it current. If something here
goes stale, fix it rather than adding a contradictory note.

---

## Start here (new session, new machine)

1. Read [NEXT_STEPS.md](NEXT_STEPS.md). It is the user's one-page tracker and the ordered plan.
2. Run `python scripts/check_environment.py`. It checks GPU and torch build, packages, ffmpeg,
   disk, paths, data and weights, and prints the fix for anything missing.
3. Every number the thesis may claim is in [RESULTS.md](RESULTS.md) with the command that
   regenerates it. Section 7 lists retired, fabricated claims. Never reuse one.

**Where things stood at the last checkpoint (2026-09-21):** work on the RTX 3060 was finished and
pushed. The **RTX 5090** environment is now set up and passes the preflight (see "Two machines").
The copy of the repo on the 5090 predated the final push; run `git pull` before starting on a
freshly copied folder.
The 5090's first job is NEXT_STEPS.md step 5: the VLM board transcription (raw frame vs
reconstructed board) and regenerating the notes one change at a time. Those two need Qwen weights,
which the 3060 never had.

---

## The user

- Syed Ar Rafi, BRAC University CSE, **undergraduate**. Team of 3. Career-critical thesis.
  Full identity and supervisors are in the auto-memory, not here.
- **Defense is about one week from 2026-09-20.** Writing (chapters) is the user's job; coding and
  results are where they want help. Do not drift into writing unless asked.
- **Easily overwhelmed by volume.** They said so directly. Keep replies short, put tracking in
  NEXT_STEPS.md rather than in chat, ask one decision at a time, and act rather than list options.
- **Always give absolute Windows paths** for any file they should open, e.g.
  `F:\thesisP2\thesisP2\output\...`, never bare shorthand like `BanglaASR8/board_era1_000.jpg`.
- Wants blunt honesty ("am I cooked?", "be honest"). Give it.
- **The supervisor is a strong vision-language-model enthusiast** and wants the VLM story kept.
  Find real VLM results; never manufacture one. The honest framing is in the section below.

---

## What this project is

**InsightLens.** Pipeline: lecture video → audio (Whisper + BanglaASR) + vision (Qwen2.5-VL
whiteboard reading) → Qwen2.5-7B-Instruct → Markdown lecture notes.

Banglish = code-mixed Bengali + English written in the Roman alphabet, no standard spelling.

**Title is being revised.** Current: "InsightLens: A Vision-Language Based Accessibility Framework for
Extracting and Understanding Classroom Content in Dual Languages". The user will drop
"Accessibility". Advice given: replace "Dual Languages" with "Code-Mixed Banglish" (the correct,
searchable term); keep vision-language, which is now defensible via the board experiments below;
avoid "Understanding", which overclaims.

---

## The thesis as it now stands (details and numbers in RESULTS.md)

**One significant, replicated positive — the headline.** LoRA fine-tune of whisper-small on 1.17 h of
Banglish, tested on 137 clips of a speaker never seen in training: WER median 96.1% → 81.8%
(Wilcoxon p = 0.009), CER 75.3% → 60.7% (p = 2.2e-05). A second independent run on the same data
reached WER 77.1%, CER 57.4%, p < 1e-05. Scaling curve: under 1 h is unreliable; the curve is still
falling at 1.17 h, which argues for the larger corpus. **Read medians, not means**: runaway
repetition loops push mean error over 100%.

**Three measured negatives.** Fusion: +0.7 pp Term F1, p = 0.32, and the visually biased
transcripts are byte-identical to the baseline. Visual bias: any non-zero strength halves term
recall, `optimal_bias = 0.0`. Occlusion-as-pointer (speech-to-region alignment): 101 vs 81 over
191 episodes, Wilcoxon p = 0.054, sign test p = 0.159, not supported.

**One methodological finding, possibly the most interesting page.** The inherited Term F1 metric is
anti-correlated with transcription quality (better Banglish emits fewer of the 82 English lexicon
words) and swings 8.1 pp between two runs on identical data. **Never quote a Term F1 difference
under about 8 pp.**

**The visual deliverable.** Board reconstruction by tiled mosaicking over erase-separated eras:
across 9 lectures, 35 boards, median 97.7% of tiles fully clear, 6 boards at 100%, every pixel
unmodified camera output. It is engineering, not algorithmic novelty; whiteboard occlusion removal
is an established area. Say so if asked.

**The honest VLM story for the supervisor.** The VLM result so far is not negative; the
*fusion* result is. The VLM's actual job, reading the board, was never evaluated, and it was
crippled by its inputs: keyword prompts on occluded raw frames. For the DBMS lecture it returned
four broken fragments of one name, four words not on the board, and **not one CGPA or student ID**.
The experiment that can give a real VLM positive is ready: same model and prompt, raw frame vs
reconstructed board, scored by board-content recall on the 10 held-out boards.

---

## Board-content recall (the note-quality metric)

The generated notes had never been evaluated. `scripts/score_board_recall.py` scores recall of
facts written on the board, which the summarising model cannot invent from prior knowledge.
Baseline notes: **40.1%** over 167 items. By kind: terms 78.7%, code 50.0%, names 30.0%,
**numbers 8.5%**, the lecturer's phrasings **0%**. Recall falls with guessability, a validity check.

- Evaluation set: the 10 boards of BanglaASR7, 8, 9, the held-out speaker, so no fine-tune leakage.
  **Keep speaker B in `--test-speakers` when new data arrives** so this stays valid.
- Ground truth: `data/board_truth/*.json`, drafted by reading the boards. **The user is verifying it
  by hand.** Three items are flagged `"verify": true`.
- `data/board_truth` is the answer key. **Never feed it to any generator.** `regenerate_notes.py`
  refuses the path outright.

---

## Why the notes were bland, and the fix

Two independent causes. (1) The prompt asked for "comprehensive notes that explain each concept
clearly", so Qwen recited a textbook, including a NAND definition the lecturer never said. (2) The
input transcript was unusable: "tait gate involve. তর্মানে 9 gate হচে" where the lecturer said NOR
gate. The fine-tuned transcript of the same passage: "and baani kichilo multiplication. so a into b.
erpor e ami ki korbo? not korbo."

- `src/summarizer/prompts.py`: grounded prompts. **Language is a switch, by the user's choice:**
  `english`, `banglish`, `mixed` (English with the lecturer's Banglish quoted), plus `legacy`.
- **`legacy` is the original prompt, verified character-identical by AST comparison, and is the
  default**, because the 40.1% baseline was produced with it. Do not edit it.
- Fine-tuned transcripts for all 9 lectures were **already produced on the 3060** and sit in each
  lecture folder as `transcript_finetuned.txt`. Videos 1–6 are training lectures for that adapter;
  only 7–9 are valid for evaluation.
- The new notes have **not been generated or seen yet**. That needs Qwen on the 5090. Do not claim
  they are better until they have been generated and scored.

---

## Two machines

| | RTX 3060, 12 GB (dev, `F:\thesisP2`) | RTX 5090, 32 GB (final runs) |
|---|---|---|
| Role | Built and tested everything | Qwen VLM + LLM runs, 8 h fine-tune |
| torch | 2.5.1+cu121 — **do not disturb** | 2.11.0+cu128 (Blackwell, sm_120, needs torch ≥ 2.7). 2.5.1+cu121 would import, see the card, then fail |
| Weights | whisper-small + LoRA only, no Qwen | Qwen2.5-VL-7B-Instruct, Qwen2.5-7B-Instruct (download to `HF_HOME`) |

**5090 setup (done 2026-09-21).** Repo `D:\T2520875\thesisP2\thesisP2`, ft_work
`D:\T2520875\thesisP2\ft_work` (the default sibling, no env var needed). One interpreter for
everything: `C:\Program Files\Python312\python.exe` (packages in the user site), with transformers
5.12.1 (same as the 3060), peft 0.21.0, accelerate, matplotlib, Pillow, rich, scipy.
**`HF_HOME=D:\T2520875\hf_cache`** is set as a user env var because C: has only 25 GB free and the
two Qwen models are about 31 GB. No ffmpeg; step 5 does not need it, new audio data will.
The LoRA `adapter_config.json` still names the 3060's `F:\` base path; harmless, both loaders
pass the base model in explicitly.

A third machine produced the original P2 pipeline results: **RTX 3090, 24 GB**, paths under
`C:\Users\T2520785`. The abstract's hardware claim is about that machine and is correct.
**P2 pipeline results = 3090; P3 fine-tuning results = 3060.**

3060 interpreters: `F:\thesisP2\envs\thesis_ft\Scripts\python.exe` (torch, transformers 5.12.1, peft,
soundfile, jiwer, numpy; **no Pillow, no matplotlib**). `C:\Users\Rafi\miniconda3\envs\pyenv\python.exe`
has **Pillow and numpy** and ran all the vision scripts. matplotlib is installed nowhere on the 3060.
The `thesis_v2` conda env in older notes does not exist here. On the 5090, put everything in one env.

**Not in git — must be copied between machines:**
- `output\` (gitignored): past runs, the 9 `transcript_finetuned.txt`, the board mosaics in
  `output\annotation_demo\all9\`, the baseline notes the comparison needs.
- `data\` (gitignored), except `data\board_truth\` which was force-added.
- `ft_work\`, a sibling of the repo: clips, manifests, `split.json`, adapters, `models\whisper-small`.
- Environments are not portable; rebuild them.

Paths resolve through env vars with inferred defaults: `THESIS_REPO`, `THESIS_FT_DIR`
(default: sibling `ft_work`), `THESIS_PYTHON`, `THESIS_QWEN`, `THESIS_FIGURES`.

Git on the 3060 warns about dubious ownership. Pass `-c safe.directory=F:/thesisP2/thesisP2` per
command; only change global config after asking.

---

## What works vs. what doesn't (don't re-litigate unless asked)

| Component | State | Notes |
|---|---|---|
| Whisper large-v3-turbo ASR | Working | Outputs an English translation, not Banglish |
| Whisper-small + LoRA fine-tune | **Working, significant** | The headline result |
| BanglaASR (Bengali Unicode) | Working | Wav2Vec2 |
| Qwen2.5-VL whiteboard reading | Runs; **never evaluated** | Keyword prompt discards numbers; fix is `transcribe_boards.py` |
| Qwen2.5-7B-Instruct notes | Runs; output was bland | Grounded prompts added, not yet run |
| Board reconstruction (tiled mosaic) | **Working, measured** | median 97.7% tiles clear, 35 boards |
| Region detection | Working, **not evaluated** | No layout ground truth exists |
| Fusion (dual-ASR, CMV) | Negative | +0.7 pp, p = 0.32 |
| Visual bias via LogitsProcessor | Failed, disabled | `config/live_config.yaml` still defaults `bias_strength: 2.0` |
| YOLOv8-Pose gaze tracking | Failed | 0 detections |
| Occlusion-as-pointer alignment | Not supported | p = 0.054 / 0.159 |
| Old inpainting in `illustrate_notes.py` | **Superseded** | Left a ghost and lost text; replaced by the mosaic |

Don't suggest reviving failed approaches unless the user raises them.

---

## Tooling added 2026-09-20/21 (all standalone; the P2 pipeline was not modified except as noted)

| Script | Purpose |
|---|---|
| `scripts/check_environment.py` | **Run first on a new machine.** Checks the torch build against the card's architecture |
| `scripts/run_p3_experiment.py` | One command: validate, prepare, train, evaluate, scaling curve |
| `finetune/prepare_data.py` | Speaker-independent split from `# Speaker ID:` headers; missing header → `UNKNOWN`, silently breaking the split |
| `finetune/train_lora.py` | LoRA training; bf16 auto; `--model`, `--data-dir`, `--train-file`, LoRA flags |
| `finetune/evaluate.py` | Base vs LoRA: median and mean WER/CER, rank tests, runaway count |
| `scripts/run_scaling_curve.py` | Nested data budgets |
| `scripts/validate_ground_truth.py` | Checks transcripts against TRANSCRIPTION_GUIDE.md |
| `scripts/compute_fusion_stats.py` | Measured fusion statistics |
| `scripts/board_mosaic.py` | Tiled board reconstruction by era |
| `scripts/board_regions.py` | Content regions on a board; temporal occluder masks |
| `scripts/best_frames.py` | Clearest frame per region (simpler, superseded by the mosaic) |
| `scripts/annotate_board.py` | Draws boxes and labels on real pixels; the VLM supplies text only |
| `scripts/illustrate_from_mosaic.py` | Puts mosaic boards into notes behind a 95% clear gate |
| `scripts/pointer_align.py` | Occlusion-as-pointer experiment (negative) |
| `scripts/score_board_recall.py` | Note-quality metric; `--compare`, `--compare-names` |
| `scripts/make_verify_sheet.py` | HTML sheet for verifying board ground truth |
| `scripts/transcribe_finetuned.py` | Whole-lecture fine-tuned transcripts; quiet-point chunking; loop collapse |
| `scripts/transcribe_boards.py` | Full VLM board transcription; `--source frame` or `mosaic` |
| `scripts/regenerate_notes.py` | Notes from a finished run; `--language`, `--board-source`, `--dry-run` |
| `src/summarizer/prompts.py` | Legacy and grounded prompts. `generator.py` gained a `notes_language` argument, default `legacy` |

`scripts/generate_thesis_figures.py` now computes rather than asserts: fusion panels, the real bias
sweep, per-video transcript lengths counted from files. **Figure 6.5 (failure modes) has no
analysis behind it** and prints a warning; label a sample of errors or drop it.

---

## How to work in this repo

- **Compute, never assert.** Every reported number needs a command in RESULTS.md. This thesis had
  a fabricated p = 0.003, an invented alpha sweep, invented ablation rows, wrong per-video lengths and
  unsourced failure-mode shares. Check provenance before trusting any number in a figure or table.
- **Report negatives as negatives.** The user accepted this; don't spin a null result.
- Edits to ASR, fusion, evaluator or summarizer: discuss first, keep old behaviour reproducible.
- `scripts/` is the experimental record; add freely, don't delete. `output/` is evidence; don't clean it.
- `data/ground_truth/` is read-only. The original 9 files break the 30 s rule (98% of segments over
  30 s) and lack Speaker IDs; leave them, they produced the headline result.
- Heavy models: don't run the full pipeline to verify a small change; use `--mock --skip-gaze` or a
  dry run.
- No emoji in new code or docs. Existing files have some; leave them.
- Bash heredocs have mangled `\n` and backslashes several times here. Use the Edit/Write tools for code
  containing escapes.
- Commit and push when the user asks; end commit messages with the Co-Authored-By line in effect.

---

## Open threads

- **New data** (~8 h) arriving from transcribers. They were told on 2026-09-21: 10–25 s segments,
  never over 30, and `# Speaker ID:` on every file. Validate with `scripts/validate_ground_truth.py`,
  then `run_p3_experiment.py --test-speakers B,<new ids> --model openai/whisper-large-v3-turbo
  --curve-hours 2 4 6 8`.
- **Board ground truth** being verified by the user; three items flagged.
- **Reference notes** for 2 lectures would close the "summarizer never evaluated" gap as a pilot.
- **Chapters 3, 7, 9** are stubs; `chapter_7.tex` is 0 bytes and not `\input` in main.tex.
- **Figure 6.5** needs an error analysis or removal.
- `config/config.yaml` and `src/model_registry.py` default to Qwen2.5-14B, contradicting the 7B setup.
- `THESIS_P2_PROGRESS_LOG.md` is 0 bytes in the working tree; the full version is in HEAD.

---

*Maintained by Claude. Last refreshed 2026-09-21 as the handoff from the 3060 to the 5090.*
