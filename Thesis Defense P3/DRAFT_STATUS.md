# The draft: where it is and what you have to do

Last updated 2026-09-24.

The LaTeX project is at
`F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis\`
and it is a copy of BRAC's template with everything filled in. The pristine template is
untouched in `Thesis Defense P3\FINAL YEAR THESIS Template_CSE400_Fall 2024 ONWARDS\`.

**It compiles.** 110 pages, no errors, no unresolved references or citations.

To build it:

```
cd "F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis"
latexmk -pdf main.tex
```

MiKTeX is already installed on this PC, so this works as it is. The output is `main.pdf`
in the same folder.

---

## What is written

| Chapter | File | State |
|---|---|---|
| Front matter (title, declaration, approval, ethics, dedication, acknowledgement) | `core\*.tex` | written, student IDs still to fill |
| Abstract | `core\abstract.tex` | written |
| 1 Introduction | `chapters\chapter_1.tex` | written, 7 sections |
| 2 Literature Review | `chapters\chapter_2.tex` | written, from a fresh web search, 24 references |
| 3 Requirements, Impacts and Constraints | `chapters\chapter_3.tex` | written, all 8 sections |
| 4 Proposed Methodology | `chapters\chapter_5.tex` | written |
| 5 Result Analysis | `chapters\chapter_6.tex` | written, all 6 sections |
| 6 Conclusion | `chapters\chapter_9.tex` | written |
| Appendix A, the transcription standard | `appendix\appendix_1.tex` | written |
| Appendix B, the prompts | `appendix\appendix_2.tex` | written |
| Bibliography | `bibliography\references.bib` | 29 entries, each one checked on the web |

The chapter file names are the template's own and do not match the chapter numbers.
`chapter_5.tex` is Chapter 4 and `chapter_6.tex` is Chapter 5. A comment at the top of each
file says which chapter it is, and the mapping is also in `main.tex`.

---

## What only you can fill in

1. **The three student IDs.** They appear in `core\titlepage.tex`, `core\declaration.tex`
   and `core\approval.tex`. Search for `[Student ID]`.
2. **The thesis coordinator and the head of department** in `core\approval.tex`.
3. **The title.** I used
   *InsightLens: A Vision-Language Framework for Generating Lecture Notes from Code-Mixed
   Banglish Classroom Videos*. Two alternatives are in a comment at the top of
   `core\titlepage.tex`. Change it in `titlepage.tex` and in `approval.tex` if you prefer
   another.
4. **The division of work** in Section 1.7 (Team Overview). I wrote a plausible version and
   marked it with a `% TODO (Rafi)` comment. Correct it before submission.
5. **The AI declaration**, if the department requires one. Marked with a TODO in
   `core\ethics_statement.tex` and in Section 3.4.

---

## The five figures you need to draw

Each one appears in the PDF as a grey box that says what to draw. Make the image, put it in
`drafts\thesis\images\` with the exact file name below, then replace the whole
`\figplaceholder{...}{...}{...}{...}` line with:

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

Use PDF or PNG at 300 dpi. Do not put underscores in the file name, LaTeX dislikes them here.

## The eleven figures already in the document

These are real, generated from the data by `scripts/make_result_figures.py`, and are already
placed and captioned. Nothing to do.

`fig-data-composition`, `fig-data-segments`, `fig-data-per-lecture`, `fig-data-boards`,
`fig-asr-final`, `fig-asr-distribution`, `fig-asr-clip-scatter`, `fig-asr-per-lecture`,
`fig-board-reading`, `fig-board-completeness`, `fig-notes-recall`.

Plus three real images from the demo lecture BanglaASR29: `board-mosaic-raw` (the
reconstruction), `board-mosaic-clean` (after the clean-up) and `board-demo-5` (with the
numbered boxes the vision model named).

---

## Two things I changed in the project while writing

1. **RESULTS.md gained three sections**, because the draft uses numbers that were computed
   but had never been written down there, and the project rule is that a number in the paper
   must be in RESULTS.md with its command.
   - **1.7b**, the hyperparameter tuning table for the full 5.15 h corpus. This is the run
     that actually chose the final settings. Section 1.7 was only the rehearsal on 2.69 h.
   - **1.9**, the corpus statistics the data chapter and the figures use: 44 videos, 8.33 h,
     609 segments, the per-lecturer breakdown, 145 boards.
   - **5.5**, the note-file counters totalled over every delivered page, with a new script
     `scripts/count_note_counters.py` that regenerates them. Its scored-13 column reproduces
     5.4 exactly, which is the check that the two agree.
2. **A small correction.** CLAUDE.md describes the Bengali branch of the old pipeline as
   Wav2Vec2. The code loads `bangla-speech-processing/BanglaASR`, which is a Whisper-small
   model fine-tuned on Bengali Common Voice. The thesis says Whisper-small. Worth fixing in
   CLAUDE.md.

---

## How I wrote it, so you can keep the same voice

- Short sentences, ordinary words, no em dashes, colons only where a list really needs one.
- Every number comes from RESULTS.md. Nothing is rounded up or restated more strongly.
- Every negative result is in, at the same level of detail as the positive ones. That is what
  makes the positive ones believable to a panel.
- Where a claim has a caveat, the caveat is in the same paragraph, not in a footnote.
