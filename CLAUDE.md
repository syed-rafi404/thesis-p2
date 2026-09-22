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

**Where things stood at the last checkpoint (2026-09-22, on the 3060):** everything committed and
pushed. Since the 5090 session: the user hand-checked all 45 board answer keys (RESULTS.md 5.0 now
rests on them); spelling-fair WER computed (1.6); all 45 boards rebuilt with a learned person mask
plus a display clean-up (4.1.1-4.1.2); and **the user stated the final deliverable** (next section
but one; plan, status and open decisions in NEXT_STEPS.md "THE GOAL"). **Stage A (the notes
pipeline) was built on the 3060 the same day and tested with a stand-in model; the leak-free
transcripts were made there too. Next: stage B on the 5090, exact commands in NEXT_STEPS.md.**
Qwen never runs on the 3060, by the user's choice ("let the 5090 do the hard work").

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

## The final deliverable (the user's spec, 2026-09-22): build toward this

Video in, a usable lecture note out:
1. Fine-tuned Whisper -> Banglish transcript (`transcribe_finetuned.py`; done, measured).
2. Per board era: the clean board (`board_mosaic.py --person-model deeplab+shadow`, then
   `clean_board.py --mask`), numbered coloured boxes from `board_regions.find_regions`, each box
   **named and transcribed by the VLM** (Set-of-Mark style: boxes drawn and numbered on the image,
   Qwen2.5-VL answers per number). Look: `Temp/mockup_nand_board.jpg`.
3. A notes LLM combines board and transcript into a lecture note that refers to the boxes
   ("look at purple box 5"). Target look: `Temp/MOCKUP_lecture_note.html`.
4. Two versions per lecture: `english` (English text with the lecturer's Banglish words quoted and
   translated, as in the mockup) and `banglish`. The student picks. **Bangla (Bengali script) was
   dropped by the user on 2026-09-22** on Claude's advice: weakest quality, only LLM translation
   (not a contribution), extra checking before the defense. Future work; do not build it.

Agreed with the user, who asked to be pushed back on expectations:
- **The mockup is Claude's handwork.** Box names and all its text are Claude's; the first quote was
  hand-edited ("ma" -> "mane", "barcho lash" -> "bar"). Real parts: the board pixels, the box
  positions, the quotes (from `transcript_finetuned_v2.txt`, lecture 7). Never present it as output.
- Always the clean board; the raw-frame-with-teacher route is dropped.
- Quotes only word for word from the transcript the notes use (`transcript_loso.txt`, the
  leak-free one); a checker drops the rest. This replaces "fix the broken `mixed` quotes".
- Usefulness needs people: a survey of about 20 once everything is done, old vs new notes of the
  same lecture ("which helps more?", a paired before/after result) plus 1-5 ratings. Until then the
  thesis says "demonstrate". Offer to build the form.
- New prompt styles go beside the old ones (`src/summarizer/annotated_prompts.py`); `legacy` stays
  the default. The user said "go" on 2026-09-22 and stage A is built.
- Notes model: Qwen3-32B at 4-bit on the 5090 is proposed, **not confirmed**; the 7B produced the
  88.0%. Any new model gets board recall re-scored. Practical: Qwen3-32B in bf16 is about 65 GB to
  download, so check free space on the 5090's D: first and how 4-bit loading works there
  (bitsandbytes on Windows); Qwen3-14B loaded in 8-bit is the fallback. A paid-API row only if the
  user accepts sending lecture text out.
- **Scope frozen until the defense.** The 10 h of new data comes after it.
- Stages: A = build on the 3060 with a stand-in model; B = Qwen runs on the 5090 (VLM re-read of the
  new boards with old-vs-new scoring, box naming, notes x 2 languages, 7B vs 32B vs mockup side by
  side); C = the user's survey. Details: NEXT_STEPS.md "THE GOAL".

---

## The thesis as it now stands (details and numbers in RESULTS.md)

**THE HEADLINE NOW (RESULTS.md 1.5): leave-one-speaker-out, whisper-large-v3-turbo + LoRA, plain
greedy decoding, two seeds per fold.** Each of the three lecturers held out once, trained on the
other two (80–114 min): **CER 72.8% → 50.3%, WER 95.3% → 75.7%** (mean of six per-run medians), all
six runs significant (max p = 2.7e-06), every fold improves. No loop safeguard needed with the
large model. Folders `ft_work_BCtoA`, `ft_work_AC`, `ft_work_ABtoC`. The whisper-small results
below are the supporting history, and the reason the safeguard exists.

**Earlier whisper-small result (corrected 2026-09-21).** The old split had
a leak: video 6 is the test speaker (user's `data/raw/Speaker2`; `scripts/verify_speakers.py`
confirms, 0.99 vs 0.77 similarity) but was trained on. **Never quote 96.1% → 81.8% again.**
Corrected: train videos 1–5 (55.6 min, speaker A), test 6–9 (184 clips, speaker B). Under plain
greedy decoding the fine-tune loops on 58 clips and does not beat base. With Whisper's standard
compression-ratio loop safeguard on both models (`evaluate.py --decode fallback`): **WER median
95.0% → 78.8–83.3%, CER 73.4% → 54.6–59.4%, p < 1e-05** over three training runs and two
safeguard seeds, every held-out lecture improves. Scaling curve (0.3 / 0.6 / 0.93 h): 84.6 / 80.6 /
83.3% WER, **flat within the 4.5 pp run-to-run noise after 0.3 h**, significant at every budget. The
old "still falling, so more data" argument came from the leaked split; drop it.
**Second unseen speaker (RESULTS.md 1.1):** Speaker3, videos 10–13 (label C, 75 clips): the A-only
adapters give CER 68.4% → 46.4–46.7%, p < 1e-08, significant even under greedy. Training on A+C
leans better on B in both seeds but is not significant (Wilcoxon p = 0.06–0.29; `ft_work_AC/`).
Done since: leave-one-speaker-out (1.5, the headline), answer keys for all 45 boards (5.0), and
spelling-fair / fuzzy WER (1.6: 74.8% and 68.2%, so the gap is not only spelling). The safeguard was
adopted after seeing the greedy result; say so, and report both. The old split re-run on the 5090 reproduces 81.8%, so the machine
is not the cause. **Read medians, not means, and read the sign of z, not just p.**

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
is an established area. Say so if asked. **2026-09-22 (RESULTS.md 4.1.1-4.1.2):** a pretrained
person-segmentation network (DeepLabV3) plus an exposure-corrected shadow mask replaces the temporal
lecturer mask as an option; it recovers writing the old mask lost (the TTL diagram; 7 of 8 digits of
the BanglaASR6 binary number, old 5), judged by eye, not yet scored by the VLM. The display clean-up
(`clean_board.py`) whitens the background, so a cleaned board is "enhanced", not unmodified; the
mosaic underneath still is unmodified. Generative inpainting was ruled out: it would invent writing.

**The VLM result for the supervisor — on hand-verified answer keys (RESULTS.md 5.0, 2026-09-22).**
Same Qwen2.5-VL-7B, only the prompt changed, 35 boards of lectures 1–9, 349 items: board-content
recall **31.2% (keyword prompt) → 88.8% (full transcription)**, better on 34 boards, worse on none,
sign p = 1.2e-10; numbers 0/67 → 65/67. A third lecturer's boards: 89.7%. Reconstructed board 95.7%
vs raw frame 88.8%: a trend (Wilcoxon p = 0.056, sign p = 0.23), absent for Speaker3: **the gain is
the prompt, not the reconstruction.** Say that plainly. Reconstruction limits found in the hand
check: it cannot remove glare, and loses content visible in only one frame (RESULTS.md 5.0).

---

## Board-content recall (the note-quality metric)

The generated notes had never been evaluated. `scripts/score_board_recall.py` scores recall of
facts written on the board, which the summarising model cannot invent from prior knowledge.
Baseline notes on the verified keys: **38.7%** over 194 items on lectures 7–9, **37.2%** over 349
items on lectures 1–9; numbers 6/67. (The draft-key figure was 40.1% over 167 items.) Recall falls
with guessability, a validity check. Items of 3 characters or fewer match as whole words only.

- Evaluation set: originally the 10 boards of BanglaASR7, 8, 9 (the held-out speaker); now all 45
  boards of lectures 1-13 have verified keys. **Leakage rule for notes that use a fine-tuned
  transcript:** each keyed lecture's transcript must come from an adapter that never heard its
  lecturer, i.e. the leave-one-speaker-out adapters: `ft_work_BCtoA` for A (videos 1-5),
  `ft_work_AC` for B (6-9), `ft_work_ABtoC` for C (10-13). `transcript_finetuned_v2.txt` came from
  the A-only adapter, so it is leak-free for 6-13 only.
- Ground truth: `data/board_truth/*.json` (lectures 7–9), `draft_lectures1to6/`, `draft_speaker3/`.
  Drafted by Claude, then **every one of the 45 boards checked by hand by the user on 2026-09-22**
  without seeing model output (67 added, 3 corrected). The "draft" folder names are historical.
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
- Fine-tuned transcripts for all 9 lectures sit in each lecture folder. Videos 1–5 are training
  lectures for the corrected adapter; only 6–9 are valid for evaluation.
- **Board recall, verified keys (RESULTS.md 5.0), lectures 7–9:** A original 38.7%, B grounded prompt
  + keywords 25.8% (down, n.s.), C + VLM board text **95.9%** (p = 0.0078), D + fine-tuned transcript
  92.3% (n.s. vs C). On 35 boards A → C is 37.2% → 88.0% (30 better, 1 worse). C's jump is mostly the
  board transcription passed into the notes; recall does not measure readability.
- **Known defect:** the `mixed` style's lecturer quotes do not work. D has none; C labels board text
  as "Lecturer:" and once pastes a whole English transcript paragraph. Fixing it is a summarizer
  prompt edit: discuss with the user first.
- Fine-tuned transcripts: use `transcript_finetuned_v2.txt` (corrected adapter, safeguard).
  `transcript_finetuned.txt` came from the leaked adapter; kept as a record only.

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

**What git carries now (force-added 2026-09-21, the repo is private):**
- `data\ground_truth\` (all 13 transcripts) and `data\board_truth\`. Not the videos.
- The text outputs of every lecture run in `output\live_focused\no_gaze\interval_10s\` (notes,
  transcripts, board transcriptions, evaluations), `output\annotation_demo\` (board mosaics),
  `output\speaker_check\`.
- `artifacts\<work dir>\`: adapters, evaluations, manifests, `split.json`, logs for `ft_work`,
  `ft_work_3spk` (including Speaker3's extracted audio), `ft_work_AC`, `ft_work_v1_repro_5090`.
  **After `git pull` on another machine run `python scripts/restore_artifacts.py --apply`.** It puts
  them beside the repo, archives a leaked old `ft_work`, reuses or downloads whisper-small, rebuilds
  clips and checks the manifests match. Tested on a mock 3060 layout.

**Still not in git — copy by hand if a machine needs them:** videos (`data\raw\SpeakerN\`), video
frames and `full_audio.wav` under `output\` (the 3060 already has them for videos 1–9), the older
P2 experiment folders in `output\`, and whisper-small weights (922 MB, over GitHub's file limit).
Environments are not portable; rebuild them.

Paths resolve through env vars with inferred defaults: `THESIS_REPO`, `THESIS_FT_DIR`
(default: sibling `ft_work`), `THESIS_PYTHON`, `THESIS_QWEN`, `THESIS_FIGURES`.

Git on the 3060 warns about dubious ownership. Pass `-c safe.directory=F:/thesisP2/thesisP2` per
command; only change global config after asking.

---

## What works vs. what doesn't (don't re-litigate unless asked)

| Component | State | Notes |
|---|---|---|
| Whisper large-v3-turbo ASR | Working | Outputs an English translation, not Banglish |
| Whisper-small + LoRA fine-tune | **Working, significant** (with loop safeguard) | Headline; corrected split, see above |
| BanglaASR (Bengali Unicode) | Working | Wav2Vec2 |
| Qwen2.5-VL whiteboard reading | **Evaluated, strong** | 88.8% board recall on 35 verified boards with `transcribe_boards.py`; keyword prompt 31.2% |
| Qwen2.5-7B-Instruct notes | Board recall 88.0% (C, 35 boards) | Lecturer-quote instruction broken; readability unmeasured |
| Board reconstruction (tiled mosaic) | **Working, measured** | median 97.7% tiles clear, 35 boards |
| Learned lecturer mask + clean-up | **Working, judged by eye** | All 45 boards; VLM scoring pending (5090) |
| Region detection | Working, **not evaluated** | No layout ground truth exists |
| VLM box naming, box-referring notes | **Built 2026-09-22, tested with a stand-in only** | Needs the Qwen runs on the 5090 (NEXT_STEPS stage B, exact commands there). Bangla notes dropped |
| Box finding on clean boards | Works well on sparse boards (NAND: the mockup's boxes), coarse on dense ones (one big box on BanglaASR8/13) | Not measured |
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
| `scripts/verify_speakers.py` | WavLM speaker embeddings per lecture; checks the speaker labels behind the split |
| `scripts/compare_evals.py` | Side-by-side table of `evaluate.py` results, with the direction of each test |
| `evaluate.py --decode fallback` | Whisper's compression-ratio loop safeguard for both models; `--fallback-seed`. Also in `run_p3_experiment.py`, `run_scaling_curve.py` (`--hours ... all`), `transcribe_finetuned.py` |
| `prepare_data.py --speaker-map` | `v2` (default, video 6 = B) or `v1` (the superseded leaked split, reproduction only) |
| `prepare_data.py --only-speakers` | Use only some speakers. **The section 1.0 headline is `--only-speakers A,B --test-speakers B`**; without it speaker C now joins training |
| `scripts/restore_artifacts.py` | After `git pull` elsewhere: restore `artifacts\` beside the repo and rebuild clips |
| `scripts/rescore_verified_keys.py` | Every RESULTS.md 5.0 number in one command |
| `scripts/banglish_wer.py` | Spelling-fair nWER and fuzzy fWER (RESULTS.md 1.6) |
| `scripts/place_note_figures.py` | Fixes `[[FIGURE n]]` markers in existing notes without the LLM |
| `board_mosaic.py` new flags (2026-09-22) | `--eras-from` / `--extend-to-erase` (denser frames, reused eras), `--save-occluder`, `--person-model temporal/deeplab/deeplab+shadow`. Defaults unchanged; boards byte-identical without the flags (checked) |
| `scripts/person_segment.py` | DeepLabV3 person masks and exposure-corrected shadow masks; needs torchvision (3060: the pyenv env; weights cached under `C:\Users\Rafi\.cache\torch`) |
| `scripts/clean_board.py` | Display clean-up ("whiteboard mode") and `--mask` occluder blanking; replaces background pixels. `--auto-crop` is unreliable; crop by hand |
| `scripts/compare_board_sets.py` | Sheets of old / new / new-cleaned boards |
| `scripts/notes_common.py` | Shared: lecture discovery (run folders 1-9 and `speaker3_runs` 10-13, new board folders), box colours with names, answer-key guard |
| `scripts/label_boards.py` | Final deliverable step 2: boxes on each clean board (frame stripped, specks dropped by dark-pixel count, line parts joined), VLM names + transcribes each box (Set-of-Mark), "none" boxes dropped; `--boxes vlm` lets the VLM draw them (untested); `--mock` for tests. Writes `board_boxes.json`, `figures_annotated/` |
| `scripts/build_lecture_notes.py` | Final deliverable step 3: one LLM call per board, transcript cut at board changes, quote checker (word for word, else deleted) and box-reference check, counted in the .json; title/takeaways/check-yourself call; `--tag`, `--quant 4bit`, `--mock`, `--dry-run` |
| `scripts/notes_page.py` | Markdown to one self-contained HTML page (images embedded, coloured box tags, click-to-reveal answers) |
| `src/summarizer/annotated_prompts.py` | The annotated-notes prompts (english, banglish); prompts.py untouched |
| `scripts/make_loso_transcripts.py` | Leak-free timestamped transcripts (`transcript_loso.txt`) from the leave-one-speaker-out adapters; run on the 3060 2026-09-22 for all 13 lectures |
| `transcribe_boards.py --source clean` | VLM full reading of the new clean boards, `board_text_clean.json/.md`, lectures 1-13 |

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

- **New data** (10 h in total) arriving from transcribers. They were told on 2026-09-21: 10–25 s
  segments, never over 30, and `# Speaker ID:` on every file. Validate with
  `scripts/validate_ground_truth.py`. **Split decided by the user (2026-09-22): by whole video,
  random with a fixed seed, about 8 h train / 2 h test, not by speaker.** Every lecturer must have
  videos on both sides; a video is never cut between train and test. `prepare_data.py` can only
  split by speaker today: add a video-level option (e.g. `--test-fraction 0.2 --split-seed N`, or
  `--test-videos`) before training; this was discussed on 2026-09-21 but never built.
  **`# Speaker ID:` lines are no longer required in the files (user, 2026-09-22).** The lecturer of
  each video comes from `scripts/verify_speakers.py` (voice embeddings) confirmed by the user, kept
  as a small lecture-to-lecturer table; the video-split option must use that table and must not
  skip files that lack the header (today `prepare_data.py` skips them). The thesis
  must state that test lecturers were heard in training (easier than unseen speakers); the
  leave-one-speaker-out result (RESULTS.md 1.5) stays as the unseen-lecturer number. Then
  `run_p3_experiment.py --model openai/whisper-large-v3-turbo --curve-hours 2 4 6 8` with the new
  split.
- **New lecture numbering (the user's, 2026-09-22), grouped by lecturer:** new 1-5 = old 1-5 (A),
  new 6-9 = four new lectures (A, per the user), new 10-13 = old 6-9 (B), new 14-17 = old 10-13 (C).
  `data/ground_truth` and `data/raw/live_classroom` use the new names; every ground-truth file now
  starts with `# Speaker ID: A|B|C` (added by Claude at the user's request, text otherwise
  unchanged). **Everything measured so far uses the OLD numbers**: RESULTS.md, `data/board_truth`,
  the run folders in `output/`, adapters' `split.json`, `transcript_loso.txt`, `ft_work/audio_cache`
  (its BanglaASR10-13.wav are old 10-13 = new 14-17). The exact ground truth behind the results is
  frozen in `data/ground_truth_v1_2026-09-21/` (git HEAD before the renumbering); to reproduce a
  result, pass `--gt-dir data/ground_truth_v1_2026-09-21` to `prepare_data.py`. **Before any new
  training**, make `find_audio` and the split use the old-to-new table: it resolves by number
  (run-folder audio, then the cache, then `data/raw`), so a new BanglaASR6 would silently get old
  lecture 6's audio, and an old-numbered run folder would get the wrong video from `data/raw`. The
  LEGACY_SPEAKERS map in `prepare_data.py` is old numbering; the headers override it. Confirm new
  6-9 = lecturer A with `verify_speakers.py` when their audio is extracted. New 6-8 are partial;
  new 9 ("[Needs recheck]" in its file name) has no timestamps yet, the user is adding them.
- **Board ground truth: verified** by the user on 2026-09-22, all 45 boards. Rescore everything with
  `scripts/rescore_verified_keys.py`. Checking sheet: `output/annotation_demo/verify_all_boards.html`.
- **ft_work layout on the 5090:** `ft_work\` is the corrected split; `ft_work_v1_video6_in_train\` is
  the 3060 run (evidence); `ft_work_v1_repro_5090\` is the old split re-run as a control;
  `ft_work_3spk\` holds speaker C clips and its evaluation; `ft_work_AC\` the A+C training run.
- **Qwen runs happened on the 5090 only.** Their outputs live in `output\` (gitignored):
  `board_text_frame.*`, `board_text_mosaic.*`, `board_text.json`, `notes_B_prompt.md`,
  `notes_C_vlm.md`, `notes_D_full.md`, `transcript_finetuned_v2.txt` in each lecture folder.
  The 3060 has no Qwen: copy `output\` across to see them; do not try to regenerate there.
- ffmpeg on the 5090: installed with winget 2026-09-21 (new shells find it).
- `prepare_data.py` now skips lectures with no known speaker instead of training on them, and warns
  when labels disagree with the `data\raw\SpeakerN` folders.
- **Lecturer quotes** in the `mixed` notes do not work (see above); the planned quote checker in
  the final deliverable replaces this fix.
- **Run times are estimates until measured on the 5090.** The user asked for actual numbers. First
  job on the 5090: read file write times in the original `ft_work_ABtoC`, `ft_work_BCtoA`,
  `ft_work_AC` folders (adapter saved vs eval JSON written) and in the lecture output folders
  (`board_text_*.md`, `notes_*.md`), then replace the estimate table in NEXT_STEPS.md with measured
  per-run times. Copies on the 3060 carry git checkout times and are useless for this. Measured on
  the 3060 only: whisper-small, ~3 min training on 1.17 h of audio, ~7 min per evaluation.
- **New board pictures in git (2026-09-22):** `output/annotation_demo/all9_deeplab_shadow/` and
  `output/annotation_demo/speaker3_2s_deeplab_shadow/` (boards, `_occluder.png`, `mosaic.json`,
  `clean/`, `compare_*.jpg`). Use these on the 5090 rather than regenerating: that needs the video
  frames, torchvision and, for Speaker3, the 2 s frames in `output/speaker3_runs_2s/`, which exist
  only on the 3060. The intermediate `speaker3_2s*` test folders are local to the 3060.
- **Reference notes** for 2 lectures would close the "summarizer never evaluated" gap as a pilot.
- **The report will be rewritten from scratch** by the user with Claude's help (said 2026-09-22);
  the old LaTeX in `P2/chapters/` will not be submitted. It still contains fabricated numbers
  (chapter_6: fusion p = 0.003, d = 0.96, the 68.2 / 71.5 / 42.3 / 73.9 table; chapter_5: 16,558
  characters). When helping with the rewrite, take every number from RESULTS.md, never from the
  old chapters, and check RESULTS.md section 7 (retired claims).
- **Figure 6.5** needs an error analysis or removal.
- `config/config.yaml` and `src/model_registry.py` default to Qwen2.5-14B, contradicting the 7B setup.
- `THESIS_P2_PROGRESS_LOG.md` is 0 bytes in the working tree; the full version is in HEAD.

---

*Maintained by Claude. Last refreshed 2026-09-22 on the 3060: the final deliverable spec, the new
board pictures, and the handoff for stage B on the 5090.*
