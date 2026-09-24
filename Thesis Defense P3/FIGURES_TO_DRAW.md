# The five figures you still have to draw

Last updated 2026-09-24.

Nine figures in the thesis are generated from the data and are finished. Five are drawings
that no script can produce, and they appear in the PDF as grey boxes. This file says what
each one must show, how to build it, and gives a prompt you can paste into an AI image or
diagram tool if you would rather start from a generated draft.

## How to put a finished figure in

1. Export as **PDF** if your tool can (vector, stays sharp at any zoom). Otherwise PNG at
   **300 dpi**, at least 2000 px wide.
2. Save it into `F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis\images\` using the
   exact file name in the table below. **No underscores or spaces in the file name.** LaTeX
   treats an underscore as a maths subscript and the build will fail.
3. Open the chapter file, find the `\figplaceholder{...}` line, and replace the whole
   command (all four braces, it spans several lines) with:

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.97\textwidth]{fig-1-1-overview}
\caption{The caption text, copied from the placeholder.}
\label{fig:fig-1-1-overview}
\end{figure}
```

4. Rebuild: `cd "F:\thesisP2\thesisP2\Thesis Defense P3\drafts\thesis"` then
   `latexmk -pdf main.tex`.

Keep `width=0.97\textwidth` for wide diagrams. Use `width=0.8\textwidth` for a tall one so
it does not run off the bottom of the page.

Each figure below has a **Rough shape** block in plain text. It is there so you can check
the arrangement before spending time on the artwork, not as a style to copy. Boxes, arrows
and labels should match; spacing, colour and icons are yours.

## Design rules that apply to all five

The generated figures already in the thesis set the house style, so match them:

- **Colours.** Grey `#9aa5b1` for the old or baseline thing, green `#2a9d4f` for the new or
  good thing, red `#d62828` for a failure, orange `#f77f00` for a partial result, dark ink
  `#1f2933` for text. Blue `#1d4ed8` and purple `#7b2cbf` are used for board boxes.
- **Fonts.** Any clean sans-serif. Draw text at a size that still reads when the whole
  drawing is scaled to 15 cm wide. A safe test: if a label is smaller than about 1/40 of the
  drawing's width, it will be too small on the page.
- **No drop shadows, no gradients, no 3D.** The panel will read these on paper.
- **White background**, not transparent. Transparent PNGs go grey in some PDF viewers.
- **Aspect ratio.** Keep the drawing wider than it is tall, roughly 16:9 to 2:1, except the
  Gantt chart which can be squarer. A drawing taller than it is wide wastes half a page.

---

## 1. `fig-1-1-overview` — the opening picture

**Where:** Section 1.1, page 2. **Caption:** "The InsightLens idea. A recorded Banglish
lecture becomes a lecture note that contains both the speech and the whiteboard."

**Purpose.** This is the first figure a panel member sees. It must be understandable by
someone who has read nothing else, including a non-technical examiner. No model names, no
arrows crossing each other, no jargon.

**What it shows.** Left to right, four things:

1. A camera or video icon, labelled **"Banglish lecture video"**.
2. An arrow into a rounded box containing three stacked rows:
   - "Speech to Banglish text"
   - "Whiteboard rebuilt and read"
   - "Notes written"
3. An arrow out to a page icon labelled **"Lecture note"**.
4. Under the page icon, two small tags side by side: **"Banglish"** and **"English"**.

**Rough shape.** Compare what you draw against this. The proportions do not matter, the
arrangement does.

```
   +---------------+        +------------------------------+        +---------------+
   |               |        |                              |        |   +-------+   |
   |   [ camera ]  | -----> |  Speech to Banglish text     | -----> |   | note  |   |
   |               |        |  Whiteboard rebuilt and read |        |   | page  |   |
   |               |        |  Notes written               |        |   +-------+   |
   +---------------+        +------------------------------+        +---------------+
      Banglish                                                         Lecture note
    lecture video                                                  (Banglish) (English)
```

**Tool.** Canva or draw.io, 20 minutes. draw.io is better here because the boxes and arrows
stay aligned.

**Prompt if you want a draft first:**

> A clean, flat, minimal horizontal flow diagram for an academic thesis, white background,
> no shadows, no 3D. Left to right: a simple line-art video camera icon labelled "Banglish
> lecture video"; an arrow to a rounded rectangle containing three stacked labels "Speech to
> Banglish text", "Whiteboard rebuilt and read", "Notes written"; an arrow to a document
> page icon labelled "Lecture note"; below the page, two small pill-shaped tags reading
> "Banglish" and "English". Muted palette of grey and green, dark grey text, sans-serif,
> generous white space, 16:9.

---

## 2. `fig-2-1-related-map` — where this work sits

**Where:** Section 2.2, page 9. **Caption:** "The areas of existing research this thesis
draws on, and where it sits between them."

**Purpose.** To show at a glance that the contribution is the overlap of four established
areas rather than one new area. This is the figure that answers "what is actually new here",
so it earns its place.

**What it shows.** Four labelled regions and one marked intersection:

- Bengali speech recognition
- Code-switched speech recognition
- Whiteboard content extraction from lecture video
- Lecture note generation with large models

In the middle, a small marked point labelled **"InsightLens (this thesis)"**.

**Two layouts, either is fine.** A four-circle Venn is the obvious one but four circles
overlap awkwardly; if it looks messy, use four boxes in a 2x2 grid with arrows pointing
inward to a centre box. The 2x2 version is easier to read and easier to draw.

**Rough shape**, the 2x2 version:

```
      +------------------------------+      +------------------------------+
      |  Bengali speech recognition  |      |  Code-switched speech        |
      |                              |      |  recognition                 |
      +------------------------------+      +------------------------------+
                      \                            /
                       \                          /
                        v                        v
                     +--------------------------------+
                     |   InsightLens (this thesis)    |   <-- filled green
                     +--------------------------------+
                        ^                        ^
                       /                          \
                      /                            \
      +------------------------------+      +------------------------------+
      |  Whiteboard content          |      |  Lecture note generation     |
      |  extraction from video       |      |  with large models           |
      +------------------------------+      +------------------------------+
```

**Tool.** draw.io for the 2x2 version, Canva for the Venn.

**Prompt:**

> A flat academic diagram on a white background. Four rounded rectangles arranged in a 2x2
> grid, labelled "Bengali speech recognition", "Code-switched speech recognition",
> "Whiteboard content extraction from lecture video", and "Lecture note generation with
> large models". Each has a thin arrow pointing inward to a smaller central rounded
> rectangle labelled "InsightLens (this thesis)", which is filled light green while the four
> outer boxes are light grey. Dark grey sans-serif text, no shadows, no gradients, balanced
> spacing, 4:3.

---

## 3. `fig-3-1-gantt` — the project schedule

**Where:** Section 3.6, page 21. **Caption:** "Project schedule."

**Purpose.** Rubric CO10 is about resource and schedule management, and this figure is the
evidence for it. It is worth 3 marks and a supervisor reads it.

**What it shows.** A horizontal Gantt chart, one row per phase, in this order:

| Row | Phase |
|---|---|
| 1 | Problem and baseline |
| 2 | Review and correction |
| 3 | Data collection and transcription |
| 4a | Experiments: speech track |
| 4b | Experiments: vision and notes track |
| 5 | Writing |

Rows 4a and 4b must be drawn as two bars that **overlap in time**, because the point made in
Section 3.6 is that the two machines ran in parallel. Row 3 runs long and overlaps rows 1, 2
and 4, because transcription continued while everything else happened.

Mark two vertical lines: **draft submission** and **slide submission**.

Put month names on the horizontal axis. Use your real project months; the exact dates are
yours to fill, not something the repository records.

**Rough shape.** The months below are placeholders; use your real ones. What matters is that
the two Experiments bars overlap, that the transcription bar is long and spans most of the
chart, and that the two deadlines are marked.

```
                            Apr   May   Jun   Jul   Aug   Sep
                             |     |     |     |     |     |
  Problem and baseline     [#####]                      :     :
  Review and correction        [####]                   :     :
  Data collection and          [#########################]    :
    transcription                                       :     :
  Experiments: speech                 [###########]     :     :
  Experiments: vision                   [###########]   :     :
    and notes                                           :     :
  Writing                                     [#########]     :
                                                        :     :
                                                    Draft^     ^Slides
```

**Tool.** Canva has Gantt templates and is fastest here. Excel with a stacked bar chart also
works if you prefer.

**Prompt:**

> A simple horizontal Gantt chart for an academic report, white background, flat design, no
> 3D. Six horizontal bars with a month axis along the bottom. Row labels on the left:
> "Problem and baseline", "Review and correction", "Data collection and transcription",
> "Experiments: speech", "Experiments: vision and notes", "Writing". The two Experiments
> bars overlap in time to show parallel work, and the Data collection bar is long and spans
> most of the chart. Two vertical dashed lines near the right labelled "Draft" and "Slides".
> Muted grey and green bars, dark grey sans-serif text, thin gridlines.

---

## 4. `fig-4-1-pipeline` — the system diagram

**Where:** Section 4.1.2, page 26. **Caption:** "The InsightLens pipeline. Each stage writes
a file that the next stage reads."

**This is the most important figure in the thesis.** A panel will look at it for longer than
any other page, and most defence questions about the architecture will be asked while
pointing at it. Spend the most time here.

**What it shows.** Six blocks with the file passed between each pair written on the arrow:

1. **Video** (the input)
2. **Preprocessing** — audio at 16 kHz, frames every 2 s
3. **Stage 1, Speech** — Whisper large-v3-turbo with a LoRA adapter
   → arrow labelled `transcript.txt (timestamped Banglish)`
4. **Stage 2, Board** — erase detection, era split, tiled mosaic with a person mask,
   clean-up → arrow labelled `one clean board image per era`
5. **Stage 3, Board reading** — box finding, numbered coloured boxes drawn, Qwen2.5-VL names
   and transcribes each box → arrow labelled `board_boxes.json`
6. **Stage 4, Notes** — Qwen2.5-7B writes one section per board, then the quote checker and
   the box-reference check → arrow labelled `notes in Banglish and English`

**Three things that make this diagram good rather than generic:**

- **Show the two inputs merging.** Stage 4 receives both the transcript from stage 1 and the
  board text from stage 3. Draw both arrows arriving at stage 4. This is the single most
  important structural fact about the system and a plain left-to-right chain hides it.
- **Put the file name on every arrow.** The design principle in Section 4.1.1 is that each
  stage writes a file the next stage reads. The file names make that visible.
- **Mark which machine ran what**, if there is room. Stages 1 and 2 on the 12 GB card,
  stages 3 and 4 on the 32 GB card. A small label or a background tint for each half.

**Layout.** Top to bottom works better than left to right here, because the merge at stage 4
needs vertical space. A4 portrait suits a tall diagram.

**Rough shape.** This is the one to check carefully. If your drawing has a single straight
chain from top to bottom, it is wrong: the flow splits after preprocessing and joins again at
stage 4.

```
                         +-----------------------------+
                         |       Lecture video         |
                         +-----------------------------+
                                       |
                                       v
                         +-----------------------------+
                         |  Audio 16 kHz mono          |
                         |  Frames every 2 s           |
                         +-----------------------------+
                            |                      |
                    audio   |                      |   frames
                            v                      v
      +---------------------------+   +-----------------------------+
      | STAGE 1   SPEECH          |   | STAGE 2   BOARD             |
      | Whisper large-v3-turbo    |   | erase detection -> eras     |
      | + LoRA adapter            |   | tiled mosaic, person mask   |
      |                           |   | display clean-up            |
      +---------------------------+   +-----------------------------+
                    |                               |
     transcript.txt |                               | one clean board
      (timestamped  |                               | image per era
        Banglish)   |                               v
                    |                 +-----------------------------+
                    |                 | STAGE 3   BOARD READING     |
                    |                 | our code finds and numbers  |
                    |                 |   the boxes                 |
                    |                 | Qwen2.5-VL names and        |
                    |                 |   transcribes each box      |
                    |                 +-----------------------------+
                    |                               |
                    |                               | board_boxes.json
                    |                               |
                    +--------------+   +------------+
                                   |   |
                                   v   v
                         +-----------------------------+
                         | STAGE 4   NOTES             |
                         | Qwen2.5-7B, one call per    |
                         |   board                     |
                         | quote checker               |
                         | box-reference check         |
                         +-----------------------------+
                                       |
                                       v
                         +-----------------------------+
                         |  Lecture note               |
                         |  Banglish | English         |
                         |  Markdown | HTML            |
                         +-----------------------------+

   left branch: 12 GB card          right branch and stage 4: 32 GB card
```

Three checks against your drawing:

1. Two arrows arrive at stage 4, one from stage 1 and one from stage 3.
2. Every arrow between stages carries a file name.
3. Stage 3 sits below stage 2, not beside it. It reads what stage 2 produced.

**Tool.** draw.io. Do not use an AI image generator for this one; they cannot keep six
labelled boxes and eight labelled arrows accurate, and a wrong arrow in this figure is worse
than no figure. Use the prompt below only to get a first layout you then correct by hand.

**Prompt (for a draft layout only, check every label afterwards):**

> A technical pipeline diagram for a thesis, flat design, white background, no shadows, top
> to bottom flow. Box 1 "Lecture video". Box 2 "Audio 16 kHz + frames every 2 s". The flow
> then splits into two parallel branches. Left branch, box 3 "Stage 1 Speech: Whisper
> large-v3-turbo + LoRA adapter" with an output arrow labelled "transcript.txt". Right
> branch, box 4 "Stage 2 Board: erase detection, tiled mosaic, person mask, clean-up" with
> an output arrow labelled "clean board per era", feeding box 5 "Stage 3 Board reading: box
> finding + Qwen2.5-VL names each box" with an output arrow labelled "board_boxes.json".
> Both branches then converge into box 6 "Stage 4 Notes: Qwen2.5-7B, quote checker,
> box-reference check", which outputs to a document icon labelled "Notes in Banglish and
> English". Muted grey boxes with green accents, dark grey sans-serif labels, thin arrows.

---

## 5. `fig-4-2-before-frame` — one raw frame

**Where:** Section 4.4.2, page 34, immediately before the rebuilt board. **Caption:** "A
single frame of the same lecture, showing why one frame is not enough."

**Purpose.** The rebuilt board in Figure 4.5 only makes sense next to a frame where the
lecturer is standing in front of the writing. Without this, a reader does not see what the
reconstruction solved.

**This one is not drawn, it is chosen.** Pick a frame from the digital logic lecture, the
same one used for Figures 4.5 to 4.7, where the lecturer is clearly blocking part of the
board. Frames for that lecture are under
`F:\thesisP2\thesisP2\output\live_focused\no_gaze\interval_10s\BanglaASR7_004\ingested\frames\`.
If that folder is not on the machine you are working on, any frame from
`F:\thesisP2\thesisP2\output\lectures\BanglaASR29\frames\` shows the same thing; the caption
says "the same lecture", so change the caption to name whichever lecture you use.

**You must blur or pixelate the face before using it.** The ethics statement on page iii
says no person is identifiable in any figure, and the approval page is signed against that
statement. A strong Gaussian blur or a mosaic block over the head is enough. Do not crop the
person out entirely, because the whole point of the figure is that he is in the way.

**Optional and better:** make it a two-panel figure, the raw frame on the left and the
rebuilt board on the right, with a short label under each ("one frame" and "rebuilt from the
whole era"). If you do that, replace Figure 4.5 with the combined image and delete the
separate placeholder.

**Rough shape**, if you make it the two-panel version:

```
   +-------------------------------+   +-------------------------------+
   |  +-------------------------+  |   |  +-------------------------+  |
   |  | ####                    |  |   |  |  Digital Logic Design   |  |
   |  | ####  lecturer standing |  |   |  |  NAND gate = AND + NOT  |  |
   |  | ####  in front of the   |  |   |  |  A B | AB | (AB)'       |  |
   |  | ####  writing           |  |   |  |  0 0 |  0 |   1  ...    |  |
   |  +-------------------------+  |   |  +-------------------------+  |
   |     face blurred              |   |                               |
   +-------------------------------+   +-------------------------------+
        one frame                        rebuilt from the whole era
```

**Tool.** Canva, or any photo editor with a blur brush. Five minutes.

No AI prompt for this one. It must be a real frame from your own recording, because its
purpose is evidence.

---

## What happens if you do not finish them

The document compiles and submits with the grey boxes in place; nothing breaks. But each box
is visibly an unfinished figure, and `fig-4-1-pipeline` in particular is the figure a panel
expects in a systems thesis. If time runs short, the order to finish them in is:

1. `fig-4-1-pipeline` — do this one whatever else happens
2. `fig-1-1-overview` — first impression, and quick to draw
3. `fig-4-2-before-frame` — five minutes, and it completes the board story
4. `fig-3-1-gantt` — 3 rubric marks depend on the section it sits in
5. `fig-2-1-related-map` — the text already makes the argument without it
