# Defense presentation: slide-by-slide plan

For the three of you to build the deck from. Every number here is in
[RESULTS.md](../RESULTS.md); do not add one that is not.

Target: **about 20 minutes**, then questions. Three speakers, roughly 6 minutes each.
Backup slides at the end are not presented, they are there so a question gets an answer
with a picture instead of a story.

**The slide count is not a budget.** The twenty below are the argument, not the page
count. If a slide holds a figure and four claims, split it across two or three; a
template page can be duplicated as many times as the content needs. Squeezing this
material into fifteen pages was tried once and produced a cramped deck with the ablation
and the hyperparameters cut out of it. Give each result the room it needs.

**The prose here is a script to speak from, not text to paste onto a slide.** On the
slide put the claim and the number. The sentences below are what you say over it.

Image paths are relative to the repository root. `T/` means
`Thesis Defense P3/drafts/thesis/images/` (PDF, for LaTeX) and `S/` means
`Thesis Defense P3/slide_images/` (PNG and JPG at 150 dpi, for Canva). Use `S/` when
building slides: Canva imports a PDF as a whole page, not as a placeable image.

| Slide | Canva-ready file in `S/` |
|---|---|
| 3  overview | `1-1-overview.png` |
| 4  baselines | `baselines.png` |
| 5  corpus | `datacomp.png` |
| 6  pipeline | `pipeline.png` |
| 7  Whisper + LoRA | `archwhisper.png` |
| 9  speech result | `asrfinal.png` |
| 11 whiteboard problem | `xnor-frame-before.jpg` |
| 12 reconstruction | `xnor-mosaic-raw.jpg`, `xnor-mosaic-clean.jpg` |
| 13 prompt vs model size | `boardreading.png` |
| 14 numbered boxes | `xnor-boxes.jpg` |
| 15 note quality | `notesrecall.png` |
| B1 clip scatter | `asr-clip-scatter.png` |
| B3 per-lecture | `perlecture.png` |
| B6 schedule | `3-1-gantt.png` |

**The one thing to get right:** your supervisor has asked more than once what is novel
apart from the dataset. Slide 17 answers it, and slide 13 is the evidence. Do not let the
deck become a dataset talk.

---

## Part 1 — the problem and the data (speaker 1, ~6 min)

### Slide 1. Title

```
+--------------------------------------------------------------+
|                                                              |
|   A Vision-Language Based Framework for Extracting and       |
|   Understanding Classroom Content in Dual Languages          |
|                                                              |
|   Syed Ar Rafi 24141215                                      |
|   Adiba Islam Khan 24141216                                  |
|   Ahsan Habib 22201027                                       |
|                                                              |
|   Supervisor      Dr. Md. Golam Rabiul Alam                  |
|   Co-supervisor   Md. Tanzim Reza                            |
|                                                              |
|   Department of CSE, Brac University                         |
+--------------------------------------------------------------+
```

### Slide 2. The problem, in one example

The strongest possible opener. Same ten seconds of a real lecture, three ways. Build it
as a table and let it sit for a beat before you speak.

```
+--------------------------------------------------------------+
|  One sentence from a digital logic class                     |
|                                                              |
|  What the lecturer said                                      |
|    "so ajke amra ei duita gate er inputs and outputs         |
|     kivabe create kore sheta dekhbo"                         |
|                                                              |
|  Off-the-shelf Whisper           -> English translation      |
|    "inputs and outputs create a sheet of a book..."          |
|                                                              |
|  A Bengali model                 -> Bengali script, and      |
|    [Bengali text, even for the English words]     often a    |
|    or a repetition loop: the same character over  collapse   |
|    and over for the whole clip                               |
|                                                              |
|  A faithful record of what was said -> Banglish              |
|    "so ajke amra ei duita gate er inputs and outputs..."     |
+--------------------------------------------------------------+
```

Say: **the class is taught in two languages at once, and no recogniser will write down
what was actually said.** Forced into English, Whisper invents English words nobody
spoke. Forced into Bengali, it writes Bengali script for the English terms and often
collapses into a repetition loop. Neither gives you a record of the lecture.

**Do not say students take notes in Banglish, or search in Banglish.** They do not, and
you cannot evidence it. Banglish here is the only way to write down code-mixed speech
without forcing it into one language or the other. It is a faithful transcript, and the
transcript is a means, not the product.

### Slide 3. Who this is for, and what we built

One line: a recorded Banglish whiteboard lecture in, a usable lecture note out.

The chain to say out loud, because it is the argument of the whole talk: the class is
code-mixed, so no recogniser transcribes it faithfully; without a faithful transcript the
note generator has nothing true to work from; so the speech model is adapted to produce
one; and the note is then written from the lecturer's real words rather than from a
model's guess at them.

`[IMAGE: S/1-1-overview.png]`

### Slide 4. What already exists, and what it actually produces

**This is a measured slide, not a related-work list.** Five published models run on our own
177 held-out clips.

`[IMAGE: S/baselines.png]`

| | CER as written | after transliteration |
|---|---|---|
| tugstugi Bengali Whisper-medium | 100.0 | 47.1 |
| whisper-small-benglish | 89.9 | 66.0 |
| bangla-ASR-v5 | 98.6 | 73.0 |
| BanglaASR | 98.6 | 73.8 |
| MediBeng Whisper-tiny | 109.2 | already Latin |
| Off-the-shelf Whisper turbo | 67.7 | already Latin |
| **Ours** | **15.8** | |

Two sentences, no more: **not one of the five produced romanised Banglish on a single
clip.** Four write Bengali script, the fifth translates to English. And when we
transliterate their output to Roman to be fair to them, the best still sits at 47.1
against our 15.8.

### Slide 5. The corpus

`[IMAGE: S/datacomp.png]`

44 recordings, 8.33 h. 28 transcribed by hand word by word, 5.15 h, 609 timed segments,
three lecturers. **Say plainly that the three lecturers are us** — it is in the ethics
statement and it is better said than discovered.

---

## Part 2 — speech (speaker 2, ~6 min)

### Slide 6. The system in one picture

`[IMAGE: S/pipeline.png]`

Walk it once, top to bottom, in about 40 seconds. Point out that the grey box on the left
is training and happens once, not per lecture.

### Slide 7. How the speech model was adapted

`[IMAGE: S/archwhisper.png]`

Whisper large-v3-turbo, weights frozen, LoRA rank 16 on the query and value projections.
Only the small matrices train. 809 million parameters untouched.

### Slide 8. How the settings were chosen, before any result was seen

This slide buys you credibility for everything after it.

```
+--------------------------------------------------------------+
|  Written down BEFORE any run                                 |
|                                                              |
|   validation lectures fixed   ->  2, 12, 14 (never tested)   |
|   search order fixed          ->  lr, rank, layers,          |
|                                   epochs, seed               |
|   acceptance rule fixed       ->  keep the default unless    |
|                                   the winner beats it by     |
|                                   more than the seed spread  |
|                                                              |
|   test set touched ONCE, at the end, with 2 seeds            |
+--------------------------------------------------------------+
```

### Slide 9. The speech result

`[IMAGE: S/asrfinal.png]`

**CER 67.7 -> 15.8 and 16.0 per cent** across two seeds, on six whole lectures never seen
in training, 177 clips. Better on 164 and 167 of them. Wilcoxon p < 1e-30.

**Then say the uncomfortable part yourself, before anyone asks.** At the learning rate the
pre-registered search chose, 2e-3, one seed reached 16.2 and the other collapsed into
repetition loops at 118.7 per cent with 82 runaway clips. The pair above is the
runner-up rate, run after we saw that, and the report says so. A panel that hears you
volunteer this stops looking for what else you hid.

### Slide 10. What happens on a lecturer the model has never heard

CER 72.8 -> 50.3, WER 95.3 -> 75.7, each lecturer held out in turn, all six runs
significant.

Say it straight: **the headline number has the test lecturers heard in training. This one
does not, and it is much worse.** Both are in the report and both are labelled.

---

## Part 3 — vision and notes (speaker 3, ~6 min)

### Slide 11. The whiteboard problem

`[IMAGE: S/xnor-frame-before.jpg]`

One frame. The lecturer's arm is across the truth table and the last two columns do not
exist yet. **No single frame of this era shows the finished board.**

### Slide 12. What the reconstruction recovers

Build as a two-step reveal on one slide.

```
+----------------------------+  +----------------------------+
|  S/xnor-mosaic-raw.jpg     |  |  S/xnor-mosaic-clean.jpg   |
|  every pixel from a real   |  |  background whitened for   |
|  frame, lecturer removed   |  |  readability               |
+----------------------------+  +----------------------------+
```

Tiled mosaic over erase-separated eras, median 97.7 per cent of tiles clear across 145
boards. **Nothing is generated.** We hand-checked 98 boards: 82 complete, 9 with writing
genuinely lost. Say the 9.

### Slide 13. The main finding — prompt beats model size

**This is the slide for your supervisor. Give it the most time.**

`[IMAGE: S/boardreading.png]`

```
   Same model. Same 35 boards. Only the prompt changed.

     keyword prompt        31.2 % ####
     full transcription    88.8 % ###########################

   Same boards. Only the model size changed.

     Qwen2.5-VL-3B         83.7 % #########################
     Qwen2.5-VL-7B         89.0 % ###########################

     prompt  +57.6 points        size  +5.3 points
             about eleven times more
```

Then the honesty line that makes it stick: **the prompt was chosen on the boards it is
reported on.** So we split the boards by a rule fixed in advance, odd lectures to develop
and even to report, and on the half we never touched it is 28.4 -> 84.7, better on 17 of
18 boards and worse on none.

### Slide 14. From board to note

`[IMAGE: S/xnor-boxes.jpg]`

Our code finds the blocks of writing and numbers them. **The model does not place the
boxes** — it is shown the board with the boxes already on it and asked to name and
transcribe each number. That is Set-of-Mark prompting.

If anyone looks closely: on this board the model swapped two names, calling the block
diagram "Gate symbol" and the gate symbol "Block diagram". It is in the caption in the
report. Say it before they say it.

### Slide 15. The notes, and what stops them making things up

`[IMAGE: S/notesrecall.png]`

**Say what language the note is in, and why there are two.** The note is produced in
Banglish and in English, each written wholly in its own language. The Banglish version
can quote the lecturer's real words, which is why the word-for-word quotation check runs
on it. The English version reads naturally for a student who does not want Banglish, but
its quotations are translations and therefore cannot be verified the same way. The
student picks; the system does not decide for them.

Board content reaching the notes: **37.2 -> 89.1 per cent** over 35 boards. Over all 13
lectures the Banglish notes reach 87.2 per cent and the translated English notes 87.4, so
neither language loses board content to the other.

```
   Three controls, all counted in every output file
     quotations       checked word for word against the transcript,
                      deleted when they fail   -> 31 kept, 8 deleted
     box references   checked against boxes that exist -> 1 survived
     extra material   confined to a labelled box
```

### Slide 16. Does it actually help a reader

Twenty readers, one lecture, the two notes shown blind. **Say which was which:** the note
they preferred is the Banglish one from this system; the note it beat is the earlier
pipeline's English prose.

Say the limit in the same breath, and do not let this become a claim about language. The
two notes differ in five ways at once — board images, numbered box references, checked
quotations, three times the length, and language — so the study measures the pipeline as
a whole. It does not show that readers wanted Banglish, and we do not claim it does.

| | ours | original | same | p |
|---|---|---|---|---|
| prefer overall | 15 | 4 | 1 | 0.019 |
| better layout | 18 | 2 | 0 | 0.0004 |
| explains concepts | 10 | 2 | 8 | 0.039 |
| easier to read | 10 | 4 | 6 | 0.18 |

**Call it a pilot out loud.** Twenty people, one lecture, no correction for multiple
comparisons; under Bonferroni only layout survives. Ease of reading did not reach
significance and we do not claim it.

---

## Part 4 — closing (whoever is strongest on questions, ~3 min)

### Slide 17. What is new here, apart from the dataset

**Have this slide ready and do not rush it. It is the question he keeps asking.**

```
1  Prompt design matters about 11x more than model size for reading a
   handwritten board.      57.6 points against 5.3, re-checked on a
                           held-out half of the boards.

2  A note-quality measure a language model cannot satisfy from prior
   knowledge.              It scores only facts physically on the board.

3  English-word measures are invalid for code-mixed speech.
                           They reward translating and punish transcribing.

4  First measurement of what published Bengali models actually emit on
   spontaneous Banglish.   Five models, none produce Banglish.

   The corpus is a contribution too, but it is not the only one, and
   none of these four depends on it.
```

### Slide 18. What did not work

Say this slide with a straight face. It is why the rest is believable.

```
   dual-ASR fusion              +0.7 pp, p = 0.32          no effect
   visual bias on the decoder   any strength hurts recall  abandoned
   occlusion as a pointer       p = 0.054 / 0.159          not supported
   board clean-up for the VLM   93.6 -> 91.7               made it worse
```

The last one is the interesting one: we built the clean-up expecting it to help the model
read, measured it, and it did not. We kept it because it looks better to a human and said
so.

### Slide 19. Limitations

- Three lecturers, one university, one language pair.
- 5.15 hours is small for speech recognition.
- Training was unstable at the chosen learning rate; one seed diverged.
- The board-reading prompt was selected on the boards it is reported on; a held-out half
  supports it but does not undo the selection.
- The reader study is a pilot of twenty.
- Nothing here measures whether the generated prose is **true**. One factual error was
  found by reading.

### Slide 20. Future work, and thank you

Reader study at scale with learning measured rather than preference; factual checking of
the generated prose; more lecturers and institutions.

---

# Backup slides — not presented, kept for questions

Put these after a "Thank you" slide. Each one is a question you can answer with a picture.

| # | If they ask | Slide to jump to |
|---|---|---|
| B1 | "Did you leak training data into test?" | The split, and the leak we found and fixed |
| B2 | "Why not BLEU or ROUGE?" | Term F1 moving the wrong way |
| B3 | "Is 15.8 per cent good?" | Per-lecture breakdown |
| B4 | "Why not a bigger vision model?" | 3B vs 7B, and why 32B/72B were not run |
| B5 | "Who was recorded? Consent?" | Ethics: the lecturers are the authors |
| B6 | "How long does it take to run?" | Runtimes per stage |
| B7 | "Show me a whole note" | A real generated page |

### B1. The leak we found in our own work

An earlier split trained on a video that was also the test speaker. We found it with voice
embeddings, corrected it, and **retired the old numbers**. `scripts/verify_speakers.py`
confirmed the speaker labels, 0.99 against 0.77 similarity. Never quote 96.1 -> 81.8.

`[IMAGE: S/asr-clip-scatter.png]`

### B2. Why we did not use the inherited metric

Term F1 counts English lexicon words. A better Banglish transcript emits **fewer** of
them, so the metric moves **the wrong way** as transcription improves, and it swings 8.1
points between two runs on identical data. We found this twice, independently, in one
project. That is why note quality is scored on board content instead.

### B3. Per-lecture breakdown

`[IMAGE: S/perlecture.png]`

Every one of the six test lectures improves. Lecturer B's improves least, ending at 52
against 12 to 16 for the others, and lecturer B contributed the least training speech at
0.7 hours. One lecture per lecturer, so this is an observation, not a controlled result.

### B4. Model size

3B gets 83.7, 7B gets 89.0, on the same 45 boards with the same prompt. 32B and 72B were
not run: 68 GB and 147 GB of weights, no disk room, and quantising them would confound
size with quantisation loss. Call it a **3B-vs-7B ablation**, not a scale study.

### B5. Ethics

The three people recorded are the three of us. No third-party participant, no external
consent to obtain, no student as a subject. Recordings in Brac classrooms and other
classrooms available to us. Nothing is published; no lecture content leaves our machines,
because every model runs locally.

### B6. Runtime

`[IMAGE: S/3-1-gantt.png]` or the machine-time table from Section 3.3.

Two machines: an RTX 3060 for development, an RTX 5090 for the Qwen runs and the long
fine-tunes. Decoding 177 clips takes about 100 seconds for a whisper-small model.

### B7. A whole generated note

`[IMAGE: output/survey_pipeline/note_B.html]` — open it live if the room allows. Board
images, numbered coloured boxes, checked quotations, self-check questions.

Every board with its boxes: `output/board_boxes_review/index.html`.

---

# Questions you should rehearse answers to

**"What is novel apart from the dataset?"**
Slide 17. Lead with the prompt result, not the corpus.

**"Would your model still win on a lecturer it has never heard?"**
Much less clearly. 15.8 has the test lecturers heard in training. Leave-one-speaker-out is
about 50, which is in the same region as the best baseline after transliteration. Both are
in the report and both are labelled. **Do not dodge this one.**

**"You beat the published Bengali models. Are you claiming a better Bengali recogniser?"**
No. We did not test that and we would probably lose on Bengali script. The claim is
narrower: for romanised Banglish classroom speech nothing published is usable.

**"Do students actually write or search in Banglish?"**
Be straight: we have no evidence that they take lecture notes or search in it, and we do
not claim it. What we know is that the class is spoken in code-mixed Bengali and English,
and that no recogniser writes that down faithfully. Romanised Banglish is the only form
that holds both languages in one stream without forcing the speech into one of them, so
it is what a faithful transcript has to look like. The transcript is an intermediate
step. What the student reads is the note, and that is produced in English as well.
**If anyone quotes the abstract or Chapter 1 back at you on this, concede the sentence
rather than defend it** — the technical argument does not depend on it.

**"Board recall did not improve when the transcript improved. Does the transcript matter?"**
Board recall measures facts written on the board, and the board text is supplied to the
note model separately, so that measure is blind to the transcript by construction. It does
not say the transcript is irrelevant to note quality; it says this measure cannot see it.
Testing that properly needs readers.

**"Why is the reader study only twenty people?"**
Because it is a pilot and we report it as one. Under a Bonferroni correction only the
layout result survives. It closes the gap as a first result, not as a settled one.

**"Did you use AI to write this?"**
Answer honestly and briefly, whatever the truth is. If asked about the transcripts
specifically: a speech tool typed a first draft and a human checked every word against the
audio, about an hour of human work per ten minutes of video.

---

# Practical notes

- **Rehearse the handoffs.** Three speakers means two transitions; both should be one
  sentence, not a pause.
- **Slide 13 is the one to slow down on.** Everything else can be trimmed if you are long.
- **Do not read the numbers off the slides.** Say what they mean; the panel can read.
- **If a number is challenged, say where it comes from.** Every one has a command in
  RESULTS.md, and saying so is a strong answer.
- Export the deck to PDF as well as the native format, and put `note_B.html` on the
  laptop in case they ask to see a real output.

---

# Changed in the paper after this plan was written (2026-09-27)

Nothing here changes the argument, but the deck should not contradict the submitted PDF.

- **The submitted thesis is 88 pages**, not 91. Three pages of padding and two stranded
  stubs came out: the approval page no longer spills the Head of Department's signature
  onto a page of its own, and the contents lists no longer carry the body paragraph skip.
- **"thesis" became "research"** in 52 places of the body text, at the supervisor's RA's
  request. The title page, approval page and declaration keep the word, because there it
  is the university's own wording for the degree. Worth matching in what you say.
- **"romanized" became "romanised"** throughout, to match the document's own -ise
  convention. Corrected in this file too.
- **The baselines figure was redrawn** as horizontal bars. Seven model names collided on
  the old vertical axis and the two "109" labels sat on top of each other. It also lost a
  wrong bar: MediBeng was showing an "after transliteration" result, but it wrote zero
  Bengali script, so there was nothing to transliterate and the bar implied a test that
  was never run. `S/baselines.png` is the corrected one.
- **Section 1.6 no longer says the notes were never read by anyone.** That sentence
  predated the reader study and contradicted Section 5.1.7. It now names the pilot and
  states that ease of reading was the one question of four that did not reach
  significance. **Say it that way on slide 16 as well** — the survey does not license a
  readability claim, and under a Bonferroni correction only the layout result survives.
- **Three stale cross-references were fixed.** Passages pointing at "Section 2.2.3" for
  the code-switched evaluation literature actually wanted 2.2.4; the baseline section had
  been inserted and pushed it down. If you quote a section number on a slide, take it
  from the final PDF.
- **Supervisor and co-supervisor signatures, and all three student signatures, are in**
  the approval and declaration pages. The Thesis Coordinator and Head of Department slots
  are still blank by design.
