# The draft: where it is and what you have to do

Last updated 2026-09-24, after the first revision round.

The LaTeX project is at
`F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis\`
and it is a copy of BRAC's template with everything filled in. The pristine template is
untouched in `Thesis Defense P3\FINAL YEAR THESIS Template_CSE400_Fall 2024 ONWARDS\`.

**It compiles: 83 pages, no errors, no unresolved references or citations.**

To build it:

```
cd "F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis"
latexmk -pdf main.tex
```

MiKTeX is already installed on this PC. The output is `main.pdf` in the same folder.

---

## What changed in the revision round

| Your request | What was done |
|---|---|
| Abstract too big | Cut from about 380 words to 300, four paragraphs, one page. |
| Reads like an AI answer | Every chapter rewritten. The bold sentence-lead-ins are gone entirely (0 left, there were over 60). So are the phrases that gave it away: "the honest statement is", "worth stating", "that is the point", "read the by-board column", one-sentence paragraphs used for emphasis, and instructions addressed to the reader. The register is now third person past tense, which is what a thesis uses. |
| Too many sections | Chapter 2 went from 18 subsections to 7. Chapter 3 from 21 to 3. Chapter 4 from 25 to 12. Chapter 5 from 33 to 18. The document now has 31 sections and 40 subsections in total. |
| Too long | 110 pages to 83. |
| Too much technical detail | Removed the implementation constants (tile sizes, thresholds, pixel counts), shortened the code-fix list in 5.3, cut the Whisper architecture walk-through and the statistics primer in Chapter 2. The explanations you asked for (fine-tuning, LoRA, hyperparameter tuning, validation, ablation) are all still there. |
| Use the NAND board, not the CNN one | Done. All three board figures are now the digital logic lecture, BanglaASR11: the rebuilt board, the same board after clean-up, and the same board with six numbered boxes named by the model (Title, NAND gate, Definition, Block diagram, Truth table, Gate symbol). The CNN images were deleted. |

One extra benefit of the NAND board: it has no sticker on it, so the cosmetic defect that was
visible in the CNN figure no longer appears in any figure. It is still reported in Section
5.3.2 as a known defect.

---

## Chapter layout

| Chapter | File | Pages |
|---|---|---|
| Front matter | `core\*.tex` | i to xvi |
| 1 Introduction | `chapters\chapter_1.tex` | 1 to 6 |
| 2 Literature Review | `chapters\chapter_2.tex` | 7 to 14 |
| 3 Requirements, Impacts and Constraints | `chapters\chapter_3.tex` | 15 to 24 |
| 4 Proposed Methodology | `chapters\chapter_5.tex` | 25 to 38 |
| 5 Result Analysis | `chapters\chapter_6.tex` | 39 to 57 |
| 6 Conclusion | `chapters\chapter_9.tex` | 58 to 63 |
| Bibliography, 29 entries | `bibliography\references.bib` | 64 |
| Appendix A, the transcription standard | `appendix\appendix_1.tex` | 65 |
| Appendix B, the prompts | `appendix\appendix_2.tex` | 67 |

The chapter file names are the template's own and do not match the chapter numbers.
`chapter_5.tex` is Chapter 4 and `chapter_6.tex` is Chapter 5. A comment at the top of each
file says which chapter it is, and the mapping is also in `main.tex`.

The dedication page was removed. The template marks it optional and it cost a page.

---

## What only you can fill in

1. **The three student IDs.** In `core\titlepage.tex`, `core\declaration.tex` and
   `core\approval.tex`. Search for `[Student ID]`.
2. **The thesis coordinator and the head of department** in `core\approval.tex`.
3. **The title.** Currently *InsightLens: A Vision-Language Framework for Generating Lecture
   Notes from Code-Mixed Banglish Classroom Videos*. Two alternatives are in a comment at the
   top of `core\titlepage.tex`.
4. **The division of work** in Section 1.7. Marked with a `% TODO (Rafi)` comment.
5. **The AI declaration**, if the department requires one. Marked with a TODO in
   `core\ethics_statement.tex` and in Section 3.4.

---

## The five figures you need to draw

Each appears in the PDF as a grey box saying what to draw. Make the image, put it in
`drafts\thesis\images\` with the exact file name, then replace the whole
`\figplaceholder{...}` line with:

```latex
\begin{figure}[H]\centering
  \includegraphics[width=0.9\textwidth]{fig-1-1-overview}
  \caption{the caption text from the placeholder}\label{fig:fig-1-1-overview}
\end{figure}
```

| File name | Where | What it shows |
|---|---|---|
| `fig-1-1-overview` | Section 1.1 | The opening picture: video in, note out. Non-technical. |
| `fig-2-1-related-map` | Section 2.2 | Four research areas and where this thesis sits between them. |
| `fig-3-1-gantt` | Section 3.6 | Project schedule, one row per phase, two deadline markers. |
| `fig-4-1-pipeline` | Section 4.1 | **The main system diagram.** The most important one. |
| `fig-4-2-before-frame` | Section 4.4 | A raw video frame with the lecturer blocking the board. **Blur the face**, because the ethics statement says no person is identifiable. |

No underscores in the file names, LaTeX dislikes them in labels. PDF or PNG at 300 dpi.

## The figures already placed

Nine real figures, generated from the data and already captioned: `fig-data-composition`,
`fig-data-segments`, `fig-data-per-lecture`, `fig-asr-final`, `fig-asr-clip-scatter`,
`fig-asr-per-lecture`, `fig-board-reading`, `fig-notes-recall`, plus the three NAND board
images `nand-mosaic-raw`, `nand-mosaic-clean` and `nand-demo-3`.

`nand-demo-1`, `2`, `4` and `5` are the other four boards of the same lecture, kept in the
images folder in case you want one for the slides.

---

## Things changed in the project while writing

1. **RESULTS.md gained three sections**, because the draft uses numbers that were computed
   but never written down there, and the project rule is that a number in the paper must be
   in RESULTS.md with its command.
   - **1.7b**, the hyperparameter tuning table for the full 5.15 h corpus. This is the run
     that chose the final settings; Section 1.7 was only the rehearsal on 2.69 h.
   - **1.9**, the corpus statistics the data chapter and the figures use.
   - **5.5**, the note-file counters, regenerated by `scripts/count_note_counters.py`.
2. **A correction.** CLAUDE.md describes the Bengali branch of the old pipeline as Wav2Vec2.
   The code loads `bangla-speech-processing/BanglaASR`, a Whisper-small model fine-tuned on
   Bengali Common Voice. The thesis says Whisper-small.

---

## The voice, so you can match it when you edit

Short sentences, ordinary words, no em dashes, colons only where a list needs one. Third
person and past tense for what was done. No bold inside paragraphs. Every number comes from
RESULTS.md and nothing is stated more strongly than the test supports. Every negative result
is in, at the same level of detail as the positive ones, because that is what makes the
positive ones believable to a panel. Where a claim has a caveat, the caveat is in the same
paragraph.
