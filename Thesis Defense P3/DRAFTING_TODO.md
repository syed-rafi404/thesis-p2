# Drafting TODO and the answers to the supervisor's questions

Written 2026-09-25. This file assumes the reader has none of the conversation that produced it.

It holds three things: the answers to the two questions the supervisor keeps asking, what is
already done from his list of six changes, and what is left. Every number here is in
[RESULTS.md](../../RESULTS.md) with the command that regenerates it. Do not quote a number from
this file that you cannot find there.

---

## Part 1. The two questions, answered

### "Are the existing models doing better than us?"

**No.** On the same 177 held-out clips, with the same references, normaliser and metric code:

| Model | CER as written | CER after transliteration | WER as written | WER after translit. |
|---|---|---|---|---|
| tugstugi Bengali Whisper-medium | 100.0 | **47.1** | 100.0 | 90.2 |
| Whisper-small-benglish | 89.9 | 66.0 | 95.8 | 93.3 |
| bangla-ASR-v5 | 98.6 | 73.0 | 100.0 | 97.0 |
| BanglaASR | 98.6 | 73.8 | 100.0 | 97.3 |
| MediBeng Whisper-tiny | 109.2 | already Latin | 146.5 | already Latin |
| Off-the-shelf whisper-large-v3-turbo | 67.7 | already Latin | 93.9 | already Latin |
| **This thesis** | **15.8** | - | **42.5** | - |

Best baseline is three times our error on CER, and on WER it is not close.

**The soft spot, which must be said before a panel says it.** Our 15.8 per cent is measured with
the test lecturers heard in training. The leave-one-speaker-out experiment (RESULTS.md 1.5), where
the lecturer is entirely unseen, gives CER around 50 per cent, which is roughly where the
transliterated tugstugi model sits. Those are different test sets so it is not a head-to-head, but
the honest answer to "would you still win on a lecturer you have never heard?" is "much less
clearly". Say it first.

**Never claim** that this thesis built a better Bengali recogniser than tugstugi. That was not
tested and would probably lose on Bengali script. The safe claim is narrower: for romanized
Banglish classroom speech nothing published is usable, and this is.

### "What is the novelty and contribution without the dataset?"

Four things, ranked by how well they survive attack. Chapter 6 already contains all of them; the
problem is that the corpus is listed first, so the whole thesis reads like a dataset paper.

**1. Prompt design beats model size for reading a handwritten board, measured.** Same
Qwen2.5-VL-7B, same 35 boards, only the prompt changed: board-content recall **31.2 per cent to
88.8 per cent**. Then scale was tested separately: 3B against 7B is **83.7 against 89.0**. So the
prompt is worth **+57.6 points and model size +5.3**, about eleven times more. Re-checked on a
held-out half of the boards (**28.4 to 84.7**) so it cannot be said the prompt was chosen on the
boards it is reported on. **Lead with this.** It transfers beyond our data and it is the
supervisor's own area.

**2. A note-quality metric that prior knowledge cannot satisfy.** Board-content recall scores only
facts physically written on the board, which the language model cannot invent from what it already
knows, so it separates grounding from world knowledge. It is validated: recall falls as items get
more guessable. Most note-generation work has no such measure. Our notes go 37.2 to 89.1 per cent
on it.

**3. A measured demonstration that English-string metrics are invalid for code-mixed ASR.** Term F1
is anti-correlated with transcription quality here, because a better Banglish transcript emits
fewer of the English lexicon words the metric counts, so improving the model makes the score worse.
It also swings 8.1 points between two runs on identical data. Found twice, independently, in one
project.

**4. The first measurement of what published Bengali and Banglish models actually emit on
spontaneous code-switched classroom speech.** Not a claim that they are bad. A measurement of what
they produce: four of five write Bengali script, the fifth translates to English, none writes
Banglish, and that holds even after a generous transliteration. Done 2026-09-25, RESULTS.md 1.10.

**Not a contribution, and it must not be claimed as one.** LoRA fine-tuning of Whisper is standard
practice. Applying it carefully is engineering. The board mosaic is engineering too, and the draft
already says so, which is correct and should stay.

**The sentence to give him:**

> Besides the corpus, the thesis shows that prompt design matters about eleven times more than
> model scale for reading a handwritten board, introduces a note-quality metric that a language
> model cannot satisfy from prior knowledge, demonstrates that English-string metrics penalise
> correct code-mixed transcription, and provides the first measurement of what published Bengali
> models actually output on spontaneous Banglish speech.

---

## Part 2. The supervisor's six changes: all six are done

| # | His request | State |
|---|---|---|
| 1 | Remove the figure from the Literature Review, discuss other studies instead | **Done.** The figure is gone, replaced by a paragraph framing the four areas, plus new discussion through Chapter 2 |
| 2 | At least 50 relevant references | **Done. 55 entries, every one cited, no dangling citations.** |
| 3 | Fix the inconsistent fonts | **Done.** See the note below on what the cause actually was |
| 4 | Fix formatting, for example a table alone on a page | **Done.** The lone table and the orphaned-fragment page are gone |
| 5 | PlotNeuralNet architecture diagrams for all models | **Done, 2026-09-25.** Three diagrams, each carrying a real input |
| 6 | Revise the pipeline figure, add methodology figures | **Done, 2026-09-25.** A new full pipeline figure plus two methodology figures |

### What item 3 actually was

No font package is loaded in `main.tex`, so the document is Computer Modern and `\texttt{}`
renders as Computer Modern Typewriter, which clashes visibly with the Roman body text. The only
monospace package installed on this machine is `courier`, which looks worse, so it was fixed by
rule instead of by swapping fonts:

- `\texttt{}` no longer appears anywhere in `chapters/`. Model names are ordinary text with
  consistent capitalisation (Whisper-small-benglish, not `whisper-small-benglish`).
- Banglish word forms are italic everywhere, which is the normal convention for citing a word
  form. The spelling table in Appendix A had its "use this" column in monospace and its "do not
  write" column in plain text; both are italic now.
- `\texttt{}` survives only in the appendices, where a file format is being specified.

If he objects again, the rule above is the thing to point at.

### What item 4 came down to

The cause was in `main.tex`: `\textfraction` was 0.07, which let a float take 93 per cent of a
page. It is now 0.12, and `\floatpagefraction` went from 0.75 to 0.85. Three float-only pages
remain and all three are full-width images with long captions, which genuinely fill a page.

### Items 5 and 6, and the decision behind them

The user asked on 2026-09-25 that the model diagrams show **our own data** as the input, in the
manner of the PlotNeuralNet examples where a real photograph enters the network. They do:

| Figure | What the input actually is |
|---|---|
| `fig-arch-whisper` | The real log-Mel array of `BanglaASR11/seg_011.wav`, made by Whisper's own feature extractor, with the model's real output beside it |
| `fig-arch-qwen-vl` | The real rebuilt board of the same lecture with our numbered boxes on it, and the box names the model really returned |
| `fig-arch-qwen-llm` | The real transcript minutes and board text that the note model receives |
| `fig-pipeline-full` | The whole system top to bottom, replacing the old hand-drawn pipeline figure |
| `fig-board-reconstruction` | How a clean board is built out of the video |
| `fig-notes-assembly` | How one board plus its minutes become one section of a note |

**The example clip was chosen on a rule, not for effect.** `BanglaASR11/seg_011.wav` has a
character error rate of 15.9 per cent against the run's median of 15.8, so the figures show a
typical clip. The first clip of that lecture would have been flattering to nobody in the other
direction: it over-runs and loops, at 73.5 per cent. All of this is recorded in RESULTS.md 1.8b.

Every dimension in the three model diagrams is read from the model's own `config.json` at build
time, so a figure cannot drift from the model it describes. Regenerate with:

```
python scripts\make_example_inputs.py --stage extract     (fine-tune interpreter)
python scripts\make_example_inputs.py --stage plot        (figures interpreter)
python scripts\make_arch_figures.py --qwen-config-dir <dir> --board-image <board.jpg>
python scripts\make_pipeline_figures.py
```

**All six figures sit upright.** The model diagrams were briefly set sideways, because at their
original width the labels shrank to about two fifths and stopped being readable. That was the wrong
fix and the user rejected it. They are upright now, made to fit by narrowing the drawing rather
than rotating the page: the block spacing was tightened, the input pictures reduced to thumbnails,
the label font raised from footnotesize to small, and the model's answer moved out of the drawing
and into the LaTeX caption, since a long quotation beside the last block was what made the figure
hundreds of points wider than the diagram needed.

Two other faults were fixed at the same time:

- **Arrow directions in the pipeline figure.** Curved `to[out=..,in=..]` paths that shared a start
  anchor looped back over the node they left, and the paths leaving the note model's south side cut
  straight through its own text. All the arrows are orthogonal now, with rounded corners.
- **Capitalisation.** Every box label and every sub-label that begins a phrase now starts with a
  capital. Four sub-labels stay lowercase on purpose, because they continue the line above them
  ("a large drop in ink between" / "consecutive frames"); capitalising those would break the
  sentence in the middle.

---

## Part 3. What is left

1. **Page count.** The draft is **93 pages**, past the 70 to 85 the user set. The user said on
   2026-09-25 to deal with this later. The honest options are trimming Chapter 3, or moving some
   result tables to an appendix.
2. **The user's own sections.** Section 1.7, the division of work, and the AI declaration if the
   department wants one.
3. **A reader study.** Still the largest open gap: note quality is measured by board-content
   recall, which cannot tell whether the surrounding explanation reads well. Chapter 6 says so.

## Part 4. Where things live

| What | Where |
|---|---|
| The LaTeX project | `F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis\` |
| Build | `cd` there, then `latexmk -pdf main.tex`. Currently clean: 0 errors, 0 undefined citations or references, worst overfull line 8.95pt, 88 pages |
| Every number, with its command | `F:\thesisP2\thesisP2\RESULTS.md`. The baseline comparison is section 1.10 |
| The baseline comparison in plain language | `F:\thesisP2\thesisP2\Thesis Defense P3\BASELINE_COMPARISON.md` |
| Baseline raw output, every clip kept | `F:\thesisP2\thesisP2\output\baseline_benchmark.json` and `baseline_benchmark_translit.json` |
| Baseline figure | `F:\thesisP2\thesisP2\P2\figures\fig_baselines.pdf`, rebuilt with `F:\thesisP2\envs\figs\Scripts\python.exe scripts\make_result_figures.py --set baselines` |
| Downloaded baseline models, about 5 GB | `F:\thesisP2\models\` |
| Figures the user draws by hand | `F:\thesisP2\thesisP2\Thesis Defense P3\FIGURES_TO_DRAW.md` |
| Draft status | `F:\thesisP2\thesisP2\Thesis Defense P3\DRAFT_STATUS.md` |

### Scripts added on 2026-09-25

| Script | What it does |
|---|---|
| `scripts/fetch_baseline_models.sh` | Downloads the published models over curl. Forces IPv4, because this machine's IPv6 route to the HuggingFace CDN stalls in the TLS handshake: 261 KB/s and constant failures against 1009 KB/s on IPv4. Resumes partial files and validates what it downloads, because a 307 redirect body will otherwise be saved as if it were the file |
| `scripts/benchmark_existing_models.py` | Scores each model on the 177 clips under **its own** generation config, and counts which alphabet it answered in |
| `scripts/rescore_baselines_transliterated.py` | Transliterates Bengali output to Roman and scores again, keeping the better of two schemes per clip. Needs `indic-transliteration`, installed to a scratch directory and reached through `THESIS_SCRATCH_LIBS` so the 3060 environment is untouched |
| `scripts/bin_to_safetensors.py` | Converts a `pytorch_model.bin` to safetensors. Needed because transformers 5.12.1 refuses to load a pickle checkpoint unless torch is 2.6 or newer, and the torch here is pinned at 2.5.1 and must not be changed |
| `scripts/fetch_bib_entries.py` | Builds BibTeX from the arXiv API so that author lists and titles are not typed from memory |

---

### One thing to know about the figure files

`images/input-mel.png`, `input-waveform.png` and `input-prompt.png` are the example inputs
drawn inside the model diagrams, and they are **not in git**, because `.gitignore` excludes
`*.png`. The compiled figure PDFs that embed them are in git, so the thesis builds on a fresh
clone without them. They only need regenerating if a diagram is changed, with
`scripts/make_example_inputs.py`.

### Checked on 2026-09-25, second review round

An outside model reviewed the PDF and raised five points. Two were real, one was real but
misdiagnosed, and two were false. All of them were checked against the source before anything
was changed.

| Raised | Verdict |
|---|---|
| Broken reference rendering as "Table eftab:perlecture" in 5.1.3 | **Real.** A `\ref` had lost its backslash to a carriage return, the same mangling recorded in Part 5. It produces no LaTeX warning and no `??`, so the build checks never saw it. Fixed, and every source file was swept again for the same class: nothing else survives. |
| Repetitive phrasing right after it | **Real**, and self-inflicted: the sentence added for the new figure reference repeated the one above it word for word. Rewritten. |
| Trailing ellipses in the List of Figures | **Misdiagnosed but real underneath.** Those are dot leaders, not ellipses. The actual fault was that full multi-sentence captions were being copied into the lists, one of them 986 characters long. Every long caption now has a short form, `\caption[short]{long}`, and the longest list entry is 125 characters. |
| "Insight Lens" and "InsightLens" used inconsistently | **False.** The source uses `InsightLens` four times and `Insight Lens` zero times; the PDF has six and zero. Nothing to fix. |
| List of Figures disagreeing with body captions on the name | **False**, same reason. |

The figures were corrected at the same time. The board and the transcript panel were being drawn
with PlotNeuralNet's `to_input`, which places a picture on the zy plane; the view transform then
**mirrors it and turns it upside down**, so the board appeared with "NAND gate" reading backwards
and the spectrogram ran backwards in time. They are plain upright nodes now. The inputs were also
enlarged, since at thumbnail size there was no point showing our own data, and the prompt boxes
were raised clear of the first block.

### The running example changed from the NAND board to the X-NOR board (2026-09-25)

On the NAND board the lecturer writes "NAND gate" but draws the **NOR** symbol, an OR body with
a bubble instead of an AND body. It was the one board reproduced four times as the showcase, so
the example moved to **era 5 of the same lecture**, the X-NOR board, where the truth table, the
symbol and the formula all agree.

Everything moved together, so the figures are now one moment of one lecture rather than four
unrelated examples:

| Figure | Now shows |
|---|---|
| 4.4, the Whisper diagram | Clip 41, 12:34 to 12:51, **inside era 5**, in which the lecturer reads out the exact column box 2 holds |
| 4.6, the occluded frame | 12:40, her arm across the half-finished table |
| 4.7 and 4.8, raw and clean board | The era 5 mosaic |
| 4.9 and 4.10, the boxes and the VLM | The era 5 board with the real Qwen box names |
| 4.11, the note model | The real note written from that board |

**Three things to know.**

1. The example clip's CER is **24.5 per cent against the median of 15.8**, so it is worse than
   typical, not better. The old clip was the median one; coherence was preferred over that,
   and the caption gives both numbers so nothing is hidden.
2. The vision model **swapped two names** on this board: box 3 is the block diagram and box 4 is
   the gate symbol, and it labelled each with the other's name. The figure is left as produced
   and the caption says so. It is a fair illustration of a real limitation.
3. The seven other NAND mentions in the text were **left alone on purpose**. They are separate
   findings that are still true: the old pipeline inventing a NAND definition, the Term F1
   discussion, the verbatim prompt in Appendix B, and the measured observation in Chapters 3 and
   5 that this lecturer mislabels XOR gates as NAND and NOR. That last one is the same error
   that prompted the change, and the thesis already reports it.

The labelled board was rebuilt without a GPU by `scripts/redraw_board_figure.py`, which redraws
from the box rectangles, colours and names already stored in `board_boxes.json`. It refuses to
run on a record whose `mock` flag is true. Full record in RESULTS.md 1.8b.

## Part 5. Two traps that cost time today

**Backslashes are mangled when passed through the shell.** `\\` arrives as `\`, which silently turns
a regex for `\texttt` into one for tab-e-x-t-t-t. This is already in CLAUDE.md and it still caught
three commands in this session, including once inside a quoted heredoc, which is supposed to be
safe. For anything containing a backslash, write the file with an editor tool, or build the pattern
with `chr(92)`.

**One correction is recorded in RESULTS.md 1.10 and should not be undone.** An earlier draft of that
section said the transliterated baselines "land where off-the-shelf Whisper sits". That was written
when only the two weakest models had been run. tugstugi disproves it at 47.1 per cent, which is
better than off-the-shelf Whisper's 67.7. The retraction is in the file on purpose.
