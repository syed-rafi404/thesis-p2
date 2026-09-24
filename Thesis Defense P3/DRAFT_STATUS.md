# The draft: where it is and what you have to do

Last updated 2026-09-24, after the second revision round.

The LaTeX project is at
`F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis\`
and it is a copy of BRAC's template with everything filled in. The pristine template is
untouched in `Thesis Defense P3\FINAL YEAR THESIS Template_CSE400_Fall 2024 ONWARDS\`.

**It compiles: 85 pages, no errors, no unresolved references, no citations missing.**

To build it:

```
cd "F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis"
latexmk -pdf main.tex
```

MiKTeX is already installed on this PC. The output is `main.pdf` in the same folder.

---

## Chapter layout

| Chapter | File | Pages |
|---|---|---|
| Front matter | `core` | i to xv |
| 1 Introduction | `chapters/chapter_1.tex` | 1 to 6 |
| 2 Literature Review | `chapters/chapter_2.tex` | 7 to 14 |
| 3 Requirements, Impacts and Constraints | `chapters/chapter_3.tex` | 15 to 23 |
| 4 Proposed Methodology | `chapters/chapter_5.tex` | 24 to 37 |
| 5 Result Analysis | `chapters/chapter_6.tex` | 38 to 58 |
| 6 Conclusion | `chapters/chapter_9.tex` | 59 to 63 |
| Bibliography, 29 entries | `bibliography/references.bib` | 64 |
| Appendix A, the transcription standard | `appendix/appendix_1.tex` | 65 |
| Appendix B, the prompts | `appendix/appendix_2.tex` | 67 |

15 figures and 21 tables.

The chapter file names are the template's own and do not match the chapter numbers.
`chapter_5.tex` is Chapter 4 and `chapter_6.tex` is Chapter 5. A comment at the top of each
file says which chapter it is, and the mapping is also in `main.tex`.

The dedication page was removed. The template marks it optional and it cost a page.

---

## Done in the second revision round

| Problem | Fix |
|---|---|
| Title changed | Now *A Vision-Language Based Framework for Extracting and Understanding Classroom Content in Dual Languages*, on the title page and the approval page. |
| Approval page ran off the page | The signature blocks were written with single backslashes instead of double, so all four lines ran together inside a 6 cm box. Rebuilt as right-aligned 10.5 cm blocks. |
| Figure text overlapping | The three-panel board figure had its panel titles on one line each, wider than the panels; the delta now sits on a second line and the tick labels are shorter. The notes figure had a 53-character title in a 3.4 cm panel; it wraps onto two lines. |
| Graphs too small | The figures were being scaled down to 0.32 to 0.52 of natural size, because unwrapped footnotes stretched their saved bounding boxes. Footnotes and suptitles are now wrapped, the widest canvases are narrower, the ASR figure is stacked vertically, and fonts are larger. Page scale is now 0.73 to 0.99. |
| Text out of the margin | 53 overfull lines down to 13, the worst from 85 pt to 9 pt. Verbatim prompt blocks set in footnotesize, column padding reduced from 6 pt to 4 pt so the wide tables fit, an unbreakable model name split across two lines in a narrow table cell, and `\emergencystretch` added for the bibliography identifiers. Nothing now runs visibly past the margin. |
| Cross references | Three hand-written section numbers had drifted when sections were merged. They are now `\ref` to labels, so they cannot drift again. Checked: no `??` anywhere in the PDF, no TODO text leaking into the output. |

---

## What only you can fill in

1. **The division of work** in Section 1.7. Marked with a `% TODO (Rafi)` comment. I wrote a
   plausible version; correct it before submission.
2. **The AI declaration**, if the department requires one. Marked with a TODO in
   `core/ethics_statement.tex` and in Section 3.4.
3. **The five figures.** See `FIGURES_TO_DRAW.md` beside this file for what each one must
   show, how to build it, and a prompt if you want a draft from an AI tool first.

Student IDs, the supervisor, the co-supervisor, the thesis coordinator and the head of
department are all filled in. One thing to check: on the approval page the thesis
coordinator is currently the same person as the supervisor. If that is right, leave it.

---

## Figures already in the document

Ten are generated from the data and are finished: `fig-data-composition`,
`fig-data-segments`, `fig-asr-final`, `fig-asr-clip-scatter`, `fig-asr-per-lecture`,
`fig-board-reading`, `fig-notes-recall`, and the three NAND board images `nand-mosaic-raw`,
`nand-mosaic-clean` and `nand-demo-3`.

`nand-demo-1`, `2`, `4` and `5` are the other four boards of the same lecture, kept in the
images folder in case you want one for the slides.

To regenerate the data figures after any change:

```
F:\thesisP2\envs\figs\Scripts\python.exe scripts\make_result_figures.py --set all
```

then copy them into `drafts\thesis\images\` with hyphens instead of underscores in the
file names. The script prints the values it drew, which is how to check that nothing moved.

---

## Things changed in the project while writing

1. **RESULTS.md gained three sections**, because the draft uses numbers that were computed
   but never written down there, and the project rule is that a number in the paper must be
   in RESULTS.md with its command.
   - **1.7b**, the hyperparameter tuning table for the full 5.15 h corpus. This is the run
     that chose the final settings; Section 1.7 was only the rehearsal on 2.69 h.
   - **1.9**, the corpus statistics the data chapter and the figures use.
   - **5.5**, the note-file counters, regenerated by `scripts/count_note_counters.py`.
2. **`make_result_figures.py` changed in presentation only.** Canvas sizes, font sizes and
   line wrapping. No data, no computation. The script's printed output still matches
   RESULTS.md exactly, which is the check that nothing moved.
3. **A correction.** CLAUDE.md describes the Bengali branch of the old pipeline as Wav2Vec2.
   The code loads `bangla-speech-processing/BanglaASR`, a Whisper-small model fine-tuned on
   Bengali Common Voice. The thesis says Whisper-small.

---

## One thing to watch if you edit the .tex files yourself

Do not paste LaTeX through a shell heredoc or a quick Python one-liner. Both silently turn
`\\` into `\` and `\t` into a tab, which is exactly what broke the approval page the first
time: `\\` line breaks became ordinary spaces and four lines collapsed into one. Edit the
files directly in VS Code.

---

## The voice, so you can match it when you edit

Short sentences, ordinary words, no em dashes, colons only where a list needs one. Third
person and past tense for what was done. No bold inside paragraphs. Every number comes from
RESULTS.md and nothing is stated more strongly than the test supports. Every negative result
is in, at the same level of detail as the positive ones, because that is what makes the
positive ones believable to a panel. Where a claim has a caveat, the caveat is in the same
paragraph.
