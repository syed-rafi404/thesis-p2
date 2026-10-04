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

**The one thing to get right:** the panel will ask what is novel
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

**Built. On the slide:**

> **A student misses a class. All they have is the recording.**
>
> A video does not help. The board is blocked by the lecturer, and what is written is
> not always clear. And in a mixed classroom, a student from an English-medium
> background does not follow the harder Bangla the lecturer uses. To solve this, we
> built the first system that turns a code-mixed whiteboard lecture into a lecture
> note. We call it **InsightLens**.

`[IMAGE: S/1-1-overview.png]` — sits underneath the text block.

The English-medium point is the one to land, because it is the reason there are two
language versions at all. A student who cannot follow the harder Bangla loses the
explanation, not just the words, and the English note is what serves them.

If asked about "the first system", the boundary is the one Chapter 2 draws and it holds:
systems that turn lectures into notes assume slides and one language. NoteIt and M3AV are
the nearest, both slides, both monolingual. Whiteboard extraction is an established field
and we do not claim it. What was not found is the combination.

Do not say students take notes or search in Banglish. The Banglish transcript exists
because it is the only way to write down code-mixed speech without forcing it into one
language, not because anyone reads it.

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

Native Canva chart, left half, full height: CER above and WER below, four bars each -
off-the-shelf 67.7 / 93.9, fine-tuned seed 42 15.8 / 42.5, fine-tuned seed 1 16.0 / 41.7,
tuned rate 2e-3 seed 42 diverged 118.7 / 189.8.

**Colour the bars.** Off-the-shelf grey, the two fine-tuned bars green, the diverged bar
red. In one colour, 118.7 is the biggest thing on the slide and reads as a result instead
of a failure. This does more than any sentence.

Right half: a setup table, one result line, one footnote. A spec table reads like a real
engineering slide; short punchy fragments do not, and it carries information the chart
lacks - how much training data, and which model.

```
Training      22 lectures, 4.10 h
Test          6 lectures, 177 clips, 1.05 h
Model         Whisper large-v3-turbo + LoRA
Decoding      greedy, no safeguard
Seeds         42 and 1, both shown
```

```
Fine-tuned better on 164/177 and 167/177 clips,
and on all 6 test lectures. Wilcoxon p < 0.001.
```

Small, at the bottom:

```
2e-3 is the learning rate the tuning selected. This seed diverged;
shown for completeness.
```

Everything else is spoken, not printed: whole lectures held out, references written by
hand, error cut by roughly three quarters, and the pre-registered rate was 2e-3 - one of
its seeds reached 16.2 and the other collapsed on 82 of 177 clips, so the green bars are
the runner-up rate, run after we saw that, and the report says so.

To say: "Six lectures the model never heard. Error down by about three quarters, and the
two seeds agree to two-tenths of a point. Now the red bar - that is also ours."

Per-lecture numbers are backup B3; do not put them here.

### Slide 10. What happens on a lecturer the model has never heard

Subtitle, under the title:

```
Each lecturer held out once, trained on the other two.
```

The table is the slide. **Label the direction** - CER and WER are error rates and lower
is better, and a table of bare numbers gets read backwards (it happened while building
this slide).

```
Held out   Trained on      CER, lower is better    WER, lower is better
                           before -> after         before -> after
A          B + C, 83 min   74.2 -> 51.8 / 49.9     97.5 -> 76.2 / 75.8
B          A + C, 80 min   70.0 -> 48.8 / 52.1     93.8 -> 73.5 / 74.8
C          A + B, 114 min  74.2 -> 45.2 / 54.0     94.6 -> 74.5 / 79.8
```

Bottom:

```
Error falls by about a third for every lecturer, in both seeds.
Mean over six runs: CER 72.8 -> 50.3, WER 95.3 -> 75.7

Still a draft, not a transcript. Each fold trains on 80-114 minutes,
against 4.10 hours on the previous slide.
```

That last sentence is the one that matters: it concedes the number and explains it, so a
panellist has nothing left to extract.

If the slide looks empty, the natural graphic is the three folds - three rows of three
boxes, two green marked *train* and one red marked *test*, the red moving along each row.

Three things to say, in this order:

1. **This is cross-validation over lecturers.** It is the answer to "your test lecturers
   were heard in training" - that objection applies to slide 9, and this slide is why it
   does not sink the work.
2. **It is much worse, and it should be.** 50 per cent character error is a draft, not a
   transcript. Do not dress it up.
3. **Part of the gap is data, not difficulty.** Two things changed at once - unseen
   lecturer and a third of the training speech - so they cannot be separated.

**Follow-up: "why 15.8 there and 50 here?"** Both changed at once and we cannot separate
them - but the evidence that volume is most of it sits inside slide 9. Lecturer B
contributed 0.7 h of training speech, and B's test lecture lands at 52 per cent, almost
exactly the unseen-lecturer number, while the other five reach 12 to 16. Same experiment,
lecturer heard in training, still 52 per cent. That is backup B3.

**Follow-up: "why is the WER still so high?"** Banglish has no standard spelling, so WER
counts a whole word wrong when the transcriber wrote "aami" and the model wrote "ami",
while CER counts the one character. Measured, not asserted (RESULTS.md 1.6): spelling-fair
nWER 74.8 and fuzzy fWER 68.2 against a plain 75.7, so canonical spelling is worth about
1 point and near-misses about 7. Say it straight: **the remaining word error is not mostly
spelling - we checked.**

Source: RESULTS.md 1.5, folders `ft_work_BCtoA`, `ft_work_AC`, `ft_work_ABtoC`; the
per-lecture table is RESULTS.md 1.8; the spelling variants are RESULTS.md 1.6.

## Part 3 — vision and notes (speaker 3, ~6 min)

### Slide 11. The whiteboard problem

`[IMAGE: S/xnor-frame-before.jpg]` - one real frame, right half. It is **BanglaASR7 era 5**
(10:50-14:00), the X-NOR board, not BanglaASR1.

**Do not put the 23.5% occlusion figure on this slide.** That number is BanglaASR1's.
Recomputed with the same method (brightness person mask, 640 px scan), BanglaASR7 is a
less occluded lecture and two of its 85 frames are under 5% covered, so "no clean frame
exists" is false here:

| | BanglaASR1 (RESULTS.md 4.1) | BanglaASR7 (this image) |
|---|---|---|
| Frames | 79 | 85 |
| Median frame covered | 23.6% | 16.7% |
| Best frame | 7.0% | 2.8% |

(23.6 against the published 23.5 confirms the method reproduces.)

**Mark the problem on the image**: a red outline around the empty output column and
around the arm. The panel should see what is wrong in two seconds, not ten.

Left panel, caption:

```
The arm is on the truth table.
The output column is not written yet.
```

Left panel, the measured part - from
`output/annotation_demo/all9/BanglaASR7_004/mosaic.json`, era 5:

```
This board, 10:50 - 14:00

20 frames available
the reconstruction needed 9 of them
result: 100 % of tiles clear
```

Then:

```
One frame is never the whole board.
This one took nine.
```

That is the honest claim for this lecture, and a better one: not "every frame is bad",
but **no single frame is enough**. Nine separate moments had to be combined to get one
complete board, which is exactly what slide 12 shows.

### Slide 12. What the reconstruction recovers

Two images side by side, the same X-NOR board as slide 11.

```
+----------------------------+  +----------------------------+
|  S/xnor-mosaic-raw.jpg     |  |  S/xnor-mosaic-clean.jpg   |
+----------------------------+  +----------------------------+
```

**Label both.** Nothing on the slide otherwise says which is which, and the two carry
different claims - this is the distinction a careful panellist will probe, so print it
rather than speak it.

Under the left image:

```
Reconstructed board - every pixel is unmodified camera output.
Nothing inpainted, nothing generated.
```

Under the right image:

```
After display clean-up - background whitened.
The strokes are camera pixels; the background is not.
```

Bottom strip. **Full sentences, not telegraphic lines** - "tiles" is a word the panel has
never heard, and three bare numbers with three different denominators compete rather than
add up:

```
This board was assembled from 9 different frames.

Across 35 boards, a median of 97.7 % of the board area
came from a view with nothing in front of it.

We checked 98 boards by hand: 82 complete, 9 with writing lost.
```

If that is still long, drop the middle line - it is the one the panel is least likely to
challenge.

Then the honest one, small:

```
The clean-up looks better but does not read better:
93.6 % -> 91.7 % board recall over 45 boards, p = 0.07.
Kept for display, not for the model.
```

Volunteering that last point is worth more than the rest of the slide: it says the
measurement that would have flattered the work was made and reported against itself. The
exact wording in RESULTS.md 4.1.2 is "no measured difference, with the point estimate
against the clean-up" - do not upgrade it to "the clean-up is worse".

**Watch the board counts, they are three different sets.** 97.7 % median tiles clear is
the **35** boards of lectures 1-9 (RESULTS.md 4.1); 93.6 -> 91.7 % is the **45** boards
with hand-verified answer keys; 82 of **98** is the human completeness check on the newer
lectures. The 145-board row in RESULTS.md counts every board the project produced and
carries no 97.7 %. An earlier version of this slide paired 97.7 % with 145.

Spoken, not printed: the same board as the previous slide; the glare bands on the left
are in every frame, so no choice of frame removes them, and that limit is in the report.

### Slide 13. The main finding — prompt beats model size

**Your supervisor is not on the panel.** This slide was built for him; for a general CSE
panel it still earns its time, but it is no longer the centrepiece. Lead the deck on the
corpus and the speech result, which land with any examiner, and present this as the
vision finding rather than as the headline.

`[IMAGE: S/boardreading.png]` - three panels, one change at a time, all on the **35
boards of lectures 1-9, 349 hand-verified items**:

```
The prompt   ask for keywords 31.2 %   ->  ask for the whole board 88.8 %
The model    Qwen2.5-VL-3B    85.4 %   ->  Qwen2.5-VL-7B          88.8 %
The image    raw frame        88.8 %   ->  rebuilt 95.7 %, cleaned 94.3 %
```

**Print the significance under each panel heading.** Without it the slide shows three
effect sizes and reads as three findings, when only the first is one:

```
The prompt   +57.6 points    sign p = 1.2e-10
The model     +3.4 points    sign p = 0.21, not significant
The image     +6.9 points    sign p = 0.23, not significant
```

Right panel, the rigour point - it pre-empts the sharpest question available here by
asking it first:

```
Only the first one is significant.

The prompt was chosen on these same boards.
Re-checked on a held-out half of the lectures:
28.4 % -> 84.7 %, better on 17 of 18 boards, worse on none.
```

**Mind which set each number belongs to.** The figure is the 35-board set, so the model
panel is 85.4 -> 88.8, **+3.4**, sign p = 0.21. The **+5.3** points and p = 0.053 in the
abstract and conclusion are the *combined 45-board* set (83.7 -> 89.0). Both are correct;
quoting one with the other's board count is not.

**Do not say "eleven times more".** It compares two things that are not commensurable,
and the ratio depends entirely on which endpoints you pick. Say the two tests instead:
changing the prompt moved board reading enormously; trebling the model did not measurably
move it. That is the stronger claim and the one the paper makes.

If asked whether the comparison is fair, two answers, both checkable: the prompt sent to
the 3B and the 7B was byte-identical, recorded in every output file; and the losing
keyword prompt was not a strawman invented to lose, it was the original pipeline's own
prompt, because the earlier code consumed a keyword list.

Spoken, not printed: the reconstruction trend disappears on the third lecturer (89.7 ->
85.1), so the prompt is the finding, not the image processing.

### Slide 14. From board to note

`[IMAGE: S/xnor-boxes.jpg]` - the same X-NOR board, era 5, with the numbered coloured
boxes (`figures_annotated/board_era5_1050.jpg`).

Slide text:

```
Our code finds the blocks of writing and numbers them.
The model never places a box. It is shown the board with the
boxes already drawn, and names and transcribes each one.
```

What it returned for this board:

```
1  Title          4  Block diagram
2  Truth table    5  Formula
3  Gate symbol
```

The payoff line, at the bottom - this is why the step exists and what links the slide to
the notes:

```
The notes can now say "look at purple box 5".
```

**Not printed.** Say "this is Set-of-Mark prompting" aloud rather than on the slide.

Same for the error: on this board boxes 3 and 4 have each other's names - the rectangular
block diagram is labelled "Gate symbol" and the gate symbol "Block diagram" (verified in
`board_boxes.json`, era 5). The **text** transcribed inside both is correct, so nothing
wrong reaches the notes. Raise it only if asked, and give that second sentence with it.

### Slide 15. The notes, and what stops them making things up

`[IMAGE: S/notesrecall.png]` - two panels. Left: what the notes carry by route. Right:
board recall by transcript and by whether the board text was given.

**Layout.** Add the title bar as on the other slides, and scale the figure to fill the
left ~60 per cent at full height; as first built it sat small in the lower left with two
thirds of the slide empty.

Right column:

```
Board content reaching the notes     37 %  ->  89 %

The English note is translated from the Banglish one.
Written directly in English it carries only 56 %.
```

```
Three checks on every page

Quotations      checked word for word against the transcript,
                deleted if they fail - 31 kept, 8 deleted
Box numbers     checked against the boxes that exist
Extra material  confined to a labelled box
```

Print the "8 deleted". A check that never rejects anything is decoration; one that throws
away a fifth of the quotations is doing work.

**Spoken, for the right-hand panel of the figure**, because a panellist will ask what it
shows: giving the model the board text is what moves recall, 89 against 71. The better
transcript does not show up in this measure at all - by board it is 7 better and 6 worse.
That is why the speech result is reported on its own terms and not as a notes result.

**Answers, not bullets** - true, in the paper, but nothing on this slide shows them, and
there are enough printed caveats already:

- The language instruction is only partly obeyed: in the Banglish notes the quotations are
  Banglish but much of the explanatory prose comes out in English. Chapter 4 says so. It is
  a limitation of the generator, not a property of the output.
- Quotes are verified word for word in the **Banglish** notes only; the English notes quote
  in translation and are not verified (27 such quotes). Never say "every quote is verified".
- One reference to a box that does not exist survived the check, across the 13 Banglish
  files.
- Over all 13 lectures the Banglish notes reach 87.2 per cent and the translated English
  notes 87.4, so neither language loses board content to the other.

### Slide 16. Does it actually help a reader

Twenty readers, one lecture, the two notes shown blind. **Say which was which:** the note
they preferred is this system's; the note it beat is the earlier pipeline's plain prose.
Both are largely English — the new one quotes the lecturer in Banglish, but its
explanations are English too, so **this is not a comparison of languages** and should not
be presented as one.

Say the limit in the same breath. The two notes differ in four ways at once — board
images, numbered box references, checked quotations and three times the length — so the
study measures the pipeline as
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

### Slide 17. What is new here

**Have this slide ready and do not rush it. "What is new here?" is the question every
panel asks, and your supervisor is not in the room to answer it for you.**

Title: "What is new here" - the old title, "apart from the dataset", talked the corpus
out of being a contribution. It is one.

Bold headline, one thin line under each. Everything else is spoken.

```
1  A hand-checked Banglish corpus
   28 lectures, 5.15 hours, transcribed word by word. None existed.

2  The prompt, not the model size, is what reads a board
   +57.6 points, p = 1.2e-10. A 3x larger model: not significant.

3  A note measure a model cannot satisfy from prior knowledge
   It scores only what is physically written on the board.

4  English-word measures are invalid for code-mixed speech
   They reward translating and punish transcribing.

5  What published Bengali models actually emit on Banglish
   Five models. Not one produces Banglish.
```

**The corpus numbers, for when he asks** (RESULTS.md, the data chapter table): 44 lecture
recordings, 8.33 h of video; 28 transcribed against the audio word by word, 5.15 h, 609
timed segments, about 39,100 words, to a written standard. No comparable corpus of
spontaneous Bengali-English classroom speech in the Roman alphabet could be found, and the
nearest published corpora in this language pair are synthetic.

**Two phrases to keep:** "as far as we could find" on item 5, and "the nearest published
corpora are synthetic" on item 1. Both are what make the claims survive a challenge.

The order differs from Chapter 9, which lists the corpus fifth because it ranks by how far
each result travels beyond this data. On a slide, lead with the thing nobody can argue
with.

### Slide 18. What did not work

Say this slide with a straight face. It is why the rest is believable.

```
dual-ASR fusion             +0.7 pp, p = 0.32            no effect
visual bias on the decoder  any strength halves recall   abandoned
occlusion as a pointer      p = 0.054 / 0.159            not supported
board clean-up for the VLM  93.6 -> 91.7, p = 0.07       no measured gain
Term F1, inherited metric   swings 8.1 pp on identical data   retired
```

Line under it:

```
All five were built, measured, and reported as they came out.
```

**Never write "the clean-up made it worse."** RESULTS.md 4.1.2: "no measured difference,
with the point estimate against the clean-up, not 'the clean-up is worse'". At p = 0.07
there is no direction to claim.

The Term F1 row moved here from slide 17, and this is where it does its work: a metric
inherited from the earlier pipeline, found to move the wrong way as transcription
improves, and then dropped. That says more about the project's standards than any
positive result does.

Spoken: the clean-up is the one you most wanted to work - built expecting it to help the
model read, measured, no gain. Kept because it looks better to a person, and the report
says exactly that.

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

### Slide 21. Key references

Ten, grouped so the slide argues rather than lists. The headings do the work.

```
WHAT WE BUILT ON
Radford et al. 2023    Whisper: robust speech recognition via
                       large-scale weak supervision. ICML
Hu et al. 2022         LoRA: low-rank adaptation of large
                       language models. ICLR
Bai et al. 2025        Qwen2.5-VL technical report
Yang et al. 2023       Set-of-Mark prompting for visual grounding
Chen et al. 2017       DeepLabV3: rethinking atrous convolution

WHERE THE PROBLEM SITS
Sitaram et al. 2019    A survey of code-switched speech and
                       language processing
Kadaoui et al. 2024    PolyWER: evaluating code-switched speech
                       recognition. EMNLP Findings
Fahim et al. 2024      BanglaTLit: back-transliteration of
                       romanised Bangla. EMNLP Findings
Ghosh 2025             MediBeng Whisper Tiny: code-switched
                       Bengali-English, synthetic

THE NEAREST PRIOR WORK ON BOARDS
Davila & Zanibbi 2017  Whiteboard video summarization via
                       spatio-temporal conflict minimization. ICDAR
```

Small print at the bottom: `Full bibliography: 55 references, Chapter 7.`

Why these ten. Group one says plainly what is off the shelf, so nobody thinks Whisper or
LoRA is being claimed. Group two is where the corpus claim lives - BanglaTLit is
romanised Bangla **text**, MediBeng is **synthetic**, and neither is spontaneous
classroom speech, which is what makes "no comparable corpus" survive. Group three is the
one paper closest to the board work, and the right citation when saying the
reconstruction is engineering rather than novelty.

Keys in `bibliography/references.bib`: radford2023whisper, hu2022lora, bai2025qwen25vl,
yang2023som, chen2017deeplabv3, sitaram2019survey, kadaoui2024polywer, fahim2024banglatlit,
ghosh2025medibeng, davila2017whiteboard.

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
