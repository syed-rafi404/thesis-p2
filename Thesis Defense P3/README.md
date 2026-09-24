# Thesis Defense P3 — put the writing material here

Created 2026-09-24. This folder is for everything about **the document**, not the experiments.
The experiments are finished; see [RESULTS.md](../RESULTS.md) for every number and the command that
regenerates it.

## What to drop in here

| Put it in | What |
|---|---|
| `university_requirements/` | BRAC's thesis template, formatting rules, page limits, submission checklist, the AI-declaration rule, supervisor instructions, last year's accepted thesis if you have one |
| `drafts/` | Your chapters as you write them, any outline the supervisor gave you, feedback |
| here | Anything else: the old P2 report for reference, notes from a supervisor meeting |

Any format is fine: PDF, Word, screenshots, a pasted email. Tell me when something is in and I will
read it.

## Why it matters

Everything I write for the draft has to match BRAC's template — chapter numbering, figure and table
captions, citation style, the order of front matter. Without the template I would be guessing, and
reformatting 80-90 pages afterwards is a day you do not have.

## What is ready for the writing (2026-09-24)

- **Numbers:** [RESULTS.md](../RESULTS.md). Section 7 lists retired claims; never reuse one.
- **Figures:** ten, in `P2/figures/`, at 300 dpi as PNG and PDF, all computed from the data by
  `scripts/make_result_figures.py`:
  `fig_asr_final`, `fig_asr_distribution`, `fig_asr_clip_scatter`, `fig_asr_per_lecture`,
  `fig_data_composition`, `fig_data_segments`, `fig_data_per_lecture`, `fig_data_boards`,
  `fig_board_reading`, `fig_board_completeness`, `fig_notes_recall`.
  The eight `fig_5_*` and `fig_6_*` files in that folder are February's P2 figures and say nothing
  about this year's work; two of them were never sound. Do not reuse them without checking.
- **The deliverable to show:** `output/lectures/BanglaASR29/notes_annotated_english_via_banglish_final.html`
  (the demo lecture, never seen by any training) and its Banglish twin.
- **Q&A list:** NEXT_STEPS.md, "Q&A list", built up as findings appeared.

## The headline numbers, for quick reference

| | |
|---|---|
| ASR, six held-out lectures, 177 clips | CER **67.7% -> 15.8/16.0%**, WER 93.9% -> 42.5/41.7%, two seeds |
| ASR, unseen lecturer (harder question) | CER 72.8% -> 50.3% |
| Board reading, 349 hand-verified items | **31.2% -> 88.8%** by changing the prompt alone |
| Notes, board content reaching the page | 37.2% -> **89.1%** |
| Boards checked by hand | 82 of 98 complete; 9 real reconstruction losses |

Each one has a caveat that belongs with it. They are written beside the numbers in RESULTS.md, and
the thesis must carry them: the diverged seed, the metric that favours the translating model, the
two boards that carry the 2x2's item gain, and the absence of any human evaluation.
