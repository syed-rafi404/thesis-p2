# Defense Q&A

Questions the panel may ask, and what to answer. Every number here comes from RESULTS.md
or the paper. Nothing is a guess.

**Rule for all answers: answer the question, say the number, then stop.** Do not add a
second weak point while you are answering the first one.

---

## 1. "Bengali is our language. Why did you write the transcript in English letters?"

**This is not a style choice. The other two options throw away half of what the lecturer
said.**

The lecturer changes language inside one sentence. Our example:
*Ekhon amra ei expression-er logical circuit dekhbo*. The grammar is Bengali. The
technical words are English.

Now try to write that sentence three ways:

| Way | What happens |
|---|---|
| Bengali script | *expression* and *logical circuit* get written by sound in Bengali. They stop being English words. |
| English | "Now we will look at the logical circuit of this expression." The Bengali is gone. **This is what normal Whisper does to us.** |
| Roman letters | Both languages stay as they are. Nothing is translated. Nothing is re-spelled. |

**Say this:** *"Any script belongs to one language. So it forces us to drop the other one.
Roman letters are the only way to keep both."*

This is also what people really do. In Bangladesh, mixed Bengali-English is written in
Roman letters. People call it Banglish.

---

## 2. "Why no notes in Bengali script?"

We left it out on purpose. It is in future work.

Making them is easy. We already make the English note by translating the Banglish note,
so Bengali would be the same step.

**The problem is scoring, not writing.** Our answer keys are in Roman letters. A Bengali
note would score near zero, but only because the letters do not match - not because the
note is bad. To add Bengali properly we first need a score that works across both scripts.

---

## 3. "Your test lecturers were also in training. Is that cheating?"

**No. We hold out whole lectures, never part of one.** Six full lectures, 177 clips,
1.05 hours. One lecture is never split between training and test.

It is true that the same lecturers appear in training, in *other* lectures. The paper says
this clearly.

We also answer the harder question separately. **We hold out one full lecturer at a time**
and train on the other two. CER 72.8 -> 50.3. WER 95.3 -> 75.7. All six runs are
significant. Both results are in the paper, and each one is labelled.

---

## 4. "Why 15.8 on one slide and 50 on the next?"

Two things changed at the same time, so **we cannot say which one caused it**:
the lecturer is new, *and* there is much less training data (80-114 minutes instead of
4.10 hours).

But we have a clue, inside the main result. Lecturer B gave only 0.7 hours of training
speech. B's test lecture scores **52 per cent** - almost the same as the unseen-lecturer
number. The other five lectures reach 12 to 16. Same experiment, lecturer was in training,
still 52 per cent.

So we think **less data is the bigger reason**, but we do not claim it as proof.

---

## 5. "You picked the prompt using the same boards you report."

**Yes. We say this in the paper.** When we picked the prompt, we had no held-out set.

So we split the boards and checked again. The rule was fixed first: odd lectures to choose
on, even lectures to report on. On the half we never used to choose:
**28.4 -> 84.7 per cent, better on 17 of 18 boards, worse on none.**

Then say the limit yourself: this split came *after* the first comparison, so it does not
cancel the original choice. It only answers a smaller question - does the prompt still win
on boards that had no part in choosing it. That is all we claim.

---

## 6. "Everyone knows prompts matter. Why is this a contribution?"

Do not defend it as a new discovery about prompts. **It is a broken part we found and
fixed.**

The old pipeline asked the vision model for keywords. There are 67 numbers written on the
35 boards. The old prompt found **zero** of them. We changed the question to "transcribe
everything written on the whiteboard" and it finds **65 of 67**. Board recall goes from
31.2 to 88.8 per cent, sign test p = 1.2e-10.

Then we ran two checks, and this is what makes it a finding and not a story:

- A model more than twice as big: +3.4 points. **Not significant.**
- Rebuilding the image instead of using a raw frame: +6.9 points. **Not significant.**

**So the problem was the question we asked, not the model and not the picture.**

---

## 7. "Why greedy decoding with no loop safeguard? Did you turn something off?"

We ran it both ways, on both models. The safeguard changes nothing:

| | greedy | with safeguard |
|---|---|---|
| Normal Whisper | 67.7% | 67.0% |
| Ours, seed 42 | 15.8% | 15.8% |
| Ours, seed 1 | 16.0% | 16.0% |

Our model loops on only 1 clip out of 177, so the safeguard has nothing to fix. Normal
Whisper loops on 13, and fixing all of them only helps it by 0.7 points.

We report greedy because **it removes a doubt**. Our older small-model result only beat
its baseline when the safeguard was on. So the obvious question is: maybe the safeguard is
doing the work. Here it is not. The gain is there without it.

---

## 8. "One of your seeds failed. Can we trust this?"

Say it before they ask.

At learning rate 2e-3 - the rate our tuning picked - one seed gave 16.2 per cent and the
other broke down into repetition loops: 118.7 per cent, 82 of 177 clips runaway. Same
data, same settings, only a different random number.

The pair we report is the **second-best rate, 1e-3**. We ran it after we saw that failure.
So that choice was not blind, and the paper says so.

What we can claim: the second-best rate is stable - its two seeds agree within 0.2 points.
The chosen rate is not stable.

The same setup has broken this way four times (rank 32, and all four projections, in both
the practice run and the final tuning). So it is repeatable, and fixing it is in future
work: warmup, gradient clipping, or a lower scaling factor.

---

## 9. "Twenty readers is very few."

Agreed. The paper calls it a pilot. Twenty readers, one lecture, both notes shown without
telling them which is which:

- Prefer overall: 15 to 4, p = 0.019
- Better layout: 18 to 2, p = 0.0004
- Explains concepts: 10 to 2, p = 0.039
- Easier to read: 10 to 4, **p = 0.18 - this one is not significant, and we do not claim it**

We did not correct for testing four things at once. If we do, only layout stays
significant.

**One weak point that actually helps us:** we did not shuffle the order. The old note was
always shown first, and people usually prefer what they see first. So the result came
*against* that bias, not because of it.

---

## 10. "Did you generate or paint in any part of the board?"

**No. Every pixel is real camera output.**

We cut the frame into small tiles. For each tile, we find a moment when the lecturer was
not standing in front of *that* tile, and we take the tile from there. Nothing is painted
in, averaged, or made up. So there is no question of fake content - the only question is
whether each tile found a clear moment, and we count that exactly. Median 97.7 per cent of
the board across 35 boards.

One honest point: the **clean-up step** whitens the background. So a cleaned board is
enhanced. The writing is real camera pixels; the white background is not. The board
underneath is untouched.

---

## 11. "How good is your box detection?"

**We have no number for it, and it is in our limitations.** There is no ground truth for
box positions, and building one was outside our scope.

What we can say: the boxes come from joined-up ink pixels. No model places them, so
nothing can be invented. It works well on boards with space between items, and becomes
rough on crowded boards, where it may return one big box.

---

## 12. "Are the notes factually correct?"

**Nothing in our work measures that. We already found one wrong fact by reading.** It is
our biggest open gap and the first item in future work. It needs a subject expert reading
the notes line by line against the recording.

What we *do* check, and count in every output file:

- Quotes are matched word for word against the transcript, and deleted if they do not
  match. 31 kept, 8 deleted - a 21 per cent rejection rate.
- Box numbers are checked against boxes that really exist.
- Anything not from the lecture is put inside a labelled box.

Be careful with scope: **quotes are checked in the Banglish notes only.** The English
notes have translated quotes, which are not checked. Never say "every quote is verified".

---

## 13. "How did you make the ground truth?"

A speech-to-text tool types a rough first draft. Then a person checks **every single word**
against the audio. About one hour of human work for every ten minutes of video, because
the tool produces almost no usable Banglish. The final references are about 69 per cent CER
away from what normal Whisper writes, so no machine draft survived into them.

The paper says the transcripts are human-made. If they ask directly about tools, the
honest answer is the one above: a speech tool was used only to type a first draft.

---

## 14. "Who did you record? Did they agree?"

**The three lecturers in the recordings are the authors of this research.** 44 lectures,
8.33 hours. No other students or staff are the subject of the recordings.

---

## 15. "Why Qwen2.5-VL-7B? Why not a bigger vision model?"

Because size is not what made board reading work. The 3B model with the same prompt gets
85.4 per cent; the 7B gets 88.8. That gap is not significant.

We did not run 32B or 72B for a simple reason: they need 68 GB and 147 GB of weights, we
had no disk space, and shrinking them would mix up two things - model size and the loss
from shrinking. So call it a **3B-vs-7B test**, not a study of scale.

---

## 16. "5.15 hours is very small for speech recognition."

True, and it is our first limitation. It is also the point of the corpus contribution: no
public corpus of real Bengali-English classroom speech in Roman letters existed, the
closest published ones are machine-made, and 5.15 hours is what one hour of checking per
ten minutes of video buys in one semester.

What this small corpus still supports: 28 lectures, 609 timed segments, about 39,100
words, six whole lectures held out, two seeds, and error cut by 75 per cent.

---

## 17. "Why seed 42? Is it better than seed 1?"

**No. A seed only decides where the random numbers start. It has no quality of its own.**
42 is just a habit from a famous book, and it became a default in tutorials. 1 is just as
random.

Our own results prove it:

| | seed 42 | seed 1 |
|---|---|---|
| Validation (tuning) | **33.6** | 39.1 |
| Test, 1e-3 | 15.8 | 16.0 |
| Test, 2e-3 | **118.7 - broke down** | 16.2 |

Seed 42 beat seed 1 by 5.4 points during tuning. Then, at the rate tuning picked, seed 42
was the one that broke down, and seed 1 was fine. **The "better" seed completely flipped.**

- If asked *"why 42?"*: no reason, it is just a common default. It means nothing. That is
  why we report two seeds every time.
- If asked *"why two seeds?"*: show them this table.

Also worth saying: a 5.4-point gap from the seed alone is already a warning. A stable
setup gives nearly the same result with any seed. That same instability is what later
caused the breakdown, and it is why our rule said the winner must beat the default by
**more than** the seed gap.

---

## 18. "There is a 2025 paper that fine-tunes Whisper on Bangla. Is your work the same?"

The paper: Sifat, SUST, *IJCDS* 2025. A 115.9-hour Bangla conversational corpus, Whisper
fine-tuned at five sizes, best WER **19.6 per cent** with large-v3 turbo.

**It is not our work, for four reasons.**

**1. Opposite goal.** Their Section 3.A lists why they chose Whisper, and reason 5 is
*"Support for Native Script: the model ensures accurate language representation by
supporting transcription directly in the Bangla script."* They chose Whisper **because**
it writes Bengali script. We adapted Whisper **because** it refuses to write Banglish.

**2. Their own literature review rejects what we built.** They describe earlier Banglish
work as *"limited by its dependence on non-native Bangla representations"* and say
*"outputs in Banglish have limited applicability to native Bangla."* A 2025 published
review treats romanised output as a defect. That is the field walking away from our space,
in print.

**3. Their numbers are not comparable, and their design is weaker than ours.**

| | Sifat 2025 | Ours |
|---|---|---|
| Split | 70/15/15 random over a pooled corpus | whole lectures held out |
| Same speaker in train and test? | almost certainly - nothing stops it | no, checked with voice embeddings |
| Seeds | one run | two, both reported |
| Significance tests | none | Wilcoxon and sign test on every claim |
| Baseline | 50% WER *"as reported by OpenAI"*, not measured | 67.7% measured on our own clips |

Their random split is **the same leak we found in our own work and retired.**

**4. No vision.** Half our thesis has no counterpart there.

**Say this:** *"That is monolingual Bangla in Bengali script, from a 115.9-hour
conversational corpus, split randomly so the same speakers appear in training and test.
Their own review calls Banglish output a limitation. Their 19.6 and our 42.5 are different
languages, different scripts and different splits. That is exactly why we never compare
published numbers - we ran five published models on our own held-out clips instead."*

---

## 19. "Is the lecturer blocking the board in every lecture?"

**No, and the paper says "one lecture", not all of them.**

The measurement is BanglaASR1: 79 frames, 23.5 per cent of the board covered in the middle
frame, 7.0 per cent in the clearest, and no frame below 5 per cent.

We checked a second lecture with the same method. BanglaASR7 is less blocked: median 16.7
per cent, best frame 2.8 per cent, and **two of its 85 frames are below 5 per cent**.

**The honest answer, which is stronger than the original claim:**

> *"No, that is one lecture. Some are less blocked than others. But even in a less blocked
> lecture one frame is still not enough, because when the board is clear it is not finished
> yet. The X-NOR board needed nine different frames to rebuild."*

That answer does not depend on the lecturer being in the way at every moment.

---

## 20. "Your own example in Table 1.1 has mistakes too."

**Yes. Say so before they do.**

The reference ends *easier hoye **jabe***; our model wrote *easier hoye **chabe***. And
*sheitao* came out as *sheta o*.

**Say this:** *"Yes - that is what 16 per cent character error looks like. It is a good
draft, not a finished transcript. That is exactly why the paper says the speech model is
good enough to be a draft and not good enough to be trusted unchecked."*

Do not pretend the table is perfect. It is a real output, and showing a real one with its
real errors is the point.

---

## 21. "You invented a score, then fixed the system by feeding in exactly what that score measures. Isn't that circular?"

**This is the sharpest question available on the notes work. Be ready for it.**

The honest part first: **yes, most of the gain is the board text reaching the notes.** Our
own results say so - variant C's jump is mostly the board transcription being passed in.
Do not pretend otherwise.

**The answer:**

> *"That is not a trick, that is the finding. The question was whether the facts on the
> board were reaching the notes. They were not - 6 of 67 numbers. The fix was to make them
> reach, and now it is 65 of 67. The measure was built to detect that gap, and it did."*

**Three things that defend the measure itself:**

1. **It cannot be satisfied by guessing.** Board items are things the model cannot produce
   from prior knowledge - a student's CGPA, an ID number, the values in a specific truth
   table. Fluency scores and reference-overlap scores can be satisfied without ever reading
   the lecture. This one cannot.

2. **It behaves like a valid measure.** Recall falls as items get more guessable. If it
   were measuring nothing, that pattern would not appear.

3. **It caught things we did not want to hear.** The fine-tuned transcript does **not**
   improve board recall over the off-the-shelf one - 89 against 79 by item, and by board it
   is 7 better and 6 worse. A measure built to flatter us would not have reported that.

**What not to claim:** board-content recall does **not** say the notes are readable, well
written, or true. It only says the board's facts are present. The paper says this
explicitly, and the factual-correctness gap is listed as our biggest open problem (Q12).

---

## 22. "If your own metric was broken, why should we trust your other numbers?"

**The broken one is the metric we inherited and dropped. The ones we report are a
different kind.**

| Metric | Built from | Status |
|---|---|---|
| Term F1 | a fixed list of **82 English words** | **retired** - moves 8.1 points on identical data, and the wrong way |
| CER / WER | the **human Banglish reference** for that exact clip | reported |
| Board-content recall | **hand-verified answer keys** of what is on each board | reported |

**The obvious follow-up: "WER is text too. Why is it safe?"**

> *"Because WER compares our output with what the lecturer actually said, in whatever
> language they said it. Term F1 compares our output with a fixed English word list. One
> measures distance from the truth; the other measures how English the text is. In a
> code-mixed lecture those are opposite things."*

A model that translates everything into English scores **well** on Term F1 and **terribly**
on WER, because the reference is Banglish. That is the whole difference.

**Say the limit too:** board-content recall is also a string match, and it has its own
blind spot - it cannot see a Bengali-script note, which is why Bengali notes were dropped
(Q2). Every measure has a scope. Ours are stated.

---

## 23. "How do you find the boxes on the board?"

Short version: **find the ink, group the ink that touches, draw a rectangle round each
group.** No model places a box.

**Step 0.** Start from the clean rebuilt board, never a raw video frame. The lecturer is
not in it, so he can never be boxed by accident.

**Step 1 - erase the board's metal frame.** It is a dark line all the way round. Leave it
and every piece of writing connects through it, so the whole board comes back as one
giant box.

**Step 2 - find the ink.** A pixel is pen if it is **darker than a blurred copy of its own
surroundings**, or strongly coloured. We compare each pixel with its own neighbourhood
instead of one fixed darkness value, because the board has glare and is brighter on one
side; a single threshold would call the dark side ink and miss writing on the bright side.

**Step 3 - group touching ink.** Flood fill: start at an ink pixel, spread to every ink
pixel touching it, and that patch is one group.

**Step 4 - rectangle per group, then tidy.**
- leftmost, rightmost, topmost, bottommost pixel of the group = the rectangle
- drop specks: too little ink, or too small in both directions
- merge rectangles that touch or nearly touch, repeatedly, so one word is not five boxes
- a second pass rejoins pieces of a single written line that had wide spacing

**Only then does the model appear.** It sees the board with numbered boxes already drawn
and gives, per number, a short name and the text inside. A box it calls "none" - a smudge,
a logo, the board edge - is dropped.

**Say this:** *"The boxes come from joined-up ink pixels. No model places them, so there is
nothing for a model to invent. The model only supplies the words."*

See Q11 for how accurate the box finding is - there is no number for it.

---

## 24. "How does the model name each box?"

The boxes are drawn by code (Q23). The **names come from the model**, in one call per
board.

**What it sees:** the board image with the numbered coloured boxes already drawn on it.
That is the trick - the numbers are *in the picture*, so the model can point at a region
by saying "box 3". This is **Set-of-Mark prompting**.

**What it is asked**, shortened from the real prompt:

> *"Numbered coloured boxes have been drawn on it; each box surrounds one part of the
> writing. For every box, reply with: `id`, the box number; `name`, 1 to 4 words saying
> what kind of content it holds, for example Title, Definition, Truth table, Gate symbol,
> Block diagram, SQL query, Code, List, Worked example, Formula - if the box holds no
> lecture writing, use "none"; `text`, everything written inside, copied exactly. Write
> [illegible] for what cannot be read. **Never guess.**"*

It replies with JSON, one entry per box. **Name and text come from the same single call**,
not two.

**Three things that prompt is doing:**

1. **The example names steer the vocabulary.** Without them the model writes long
   descriptive sentences instead of short labels. It is still free to invent its own.
2. **"none" is an escape hatch.** A smudge or sticker gets a box too, because ink is ink.
   "none" is how those get dropped afterwards.
3. **"Never guess" and [illegible]** give it permission to fail. Without that, a model
   asked to read unclear handwriting invents something plausible.

**Two repairs needed in practice:**

- **Broken JSON.** Boards with code make the model emit unescaped quotes, breaking the
  whole reply. A salvage parser reads the fields one by one. Without it a single bad board
  loses **all** its boxes.
- **Runaway loops.** On one board the model emitted the same backslash line 512 times -
  42,037 characters. A guard collapses it.

**It does make mistakes.** On the X-NOR board it swapped two names: the block diagram was
called "Gate symbol" and the gate symbol "Block diagram". **The text in both was correct**,
so nothing wrong reached the notes. Say that second sentence with the first.

---

## 25. "Why does the vision model read every board twice?"

It does. Two separate runs, two prompts, and **both results go into the same note-writing
call**:

```
Box 1 (red), Title: Digital Logic Design
Box 2 (blue), Truth table: A | B | A(+)B ...
Box 3 (orange), Gate symbol: A - X-NOR - A(+)B
...

THE WHOLE BOARD, AS READ BY THE VISION MODEL
<the full continuous reading>
```

So the board content reaches the note model twice. That is deliberate, not an oversight.

**What only the box run gives you:**

- **Number and colour.** Without them the note cannot say "look at purple box 5" and the
  reader cannot find it on the picture. That is the deliverable.
- **Grouping** - which pieces of text belong together as one thing.
- **The junk filter.** The ink detector boxes everything dark: smudges, stickers, cable
  shadows. The model answering `"none"` is how those are thrown away. **The naming step is
  also the filtering step.**

**What only the whole-board run gives you:**

- **Insurance.** Box detection has no accuracy number (Q11), and on crowded boards the
  merge can return one big box. The whole-board reading still has the content when the
  boxes are wrong.
- **The measured number.** 88.8% was scored on this run. The per-box reading was never
  scored separately - do not quote 88.8% as box-reading accuracy.

**The three short answers:**

- *Why not boxes only?* You would lose whatever the box finder missed, and you would have
  no scored board-reading result.
- *Why the whole text too?* It is the version that was measured, and it covers for a box
  finder that was not.
- *Why name a box if you already have its text?* The name labels the picture for the
  student, and `"none"` is how smudges get removed.

**Admit the cost:** two VLM passes per board, and duplicated text into the note model.
Deliberate redundancy - one pass is the map, the other is the safety net.

---

## 26. "Isn't the prompt finding just you fixing your own mistake? What did you invent?"

**Concede the first half immediately.** The keyword prompt was in our own earlier pipeline.
Nobody made that mistake for us.

**Then give the two things that make it more than a bug report.**

**1. The old prompt was not stupid - it was right for a different job.** The keyword
extractor existed to feed the ASR decoder a list of likely words. For that job a keyword
list is the correct output. The error was **reusing it for a second job**, feeding the
summariser, where a keyword list throws away structure and every number. That is a
design-level mistake, and it is invisible until someone measures the downstream effect.

**2. The controls are the part nobody had.** "We fixed our prompt" is not a result. "We
fixed our prompt **and checked whether a bigger model or a better image would have fixed
it instead, and neither does**" is. Before measuring, all three guesses were live:

- 7B too small for handwriting? **No** - 3B gets 85.4.
- Image too messy? **No** - rebuilding gives +6.9, not significant.
- The question? **Yes** - +57.6, p = 1.2e-10.

Someone facing an empty-looking board extraction now knows which to try first.

**What it actually is:** a measured diagnosis - *a VLM asked for keywords loses 100 per
cent of the numbers on the board, and neither scale nor image quality recovers them.*

**The wider version of this question: "what did you invent?"**

Be at peace with this before the defense. Almost nothing here is an invention. The corpus
is collected. LoRA is Hu et al. Set-of-Mark is Yang et al. The reconstruction is, in our
own paper's words, "engineering assembled from known parts." Our contributions are
**artifacts, measurements and diagnoses**.

That is normal for a systems thesis. The failure mode is pretending otherwise.

**Say this:** *"No, we did not invent a new algorithm. We built a system from known parts
and measured every stage of it, including the parts that failed. The new things are the
corpus, the numbers, and knowing which part was actually broken."*

---

## 27. "Why not just tell Whisper the right language? Why fine-tune at all?"

**Because there is no right language to tell it.**

Before Whisper writes anything it is given marker tokens: which language, and whether to
transcribe or translate. The design assumes **one utterance = one language**. There is no
token for "Bengali and English mixed".

| What you tell it | What you get |
|---|---|
| Bengali | Bengali script, English technical words spelled phonetically |
| English | a translation - the Bengali is gone |
| auto-detect | it picks one; on our audio, usually English |

**No setting means "write both, as spoken."** Fine-tuning teaches the model a behaviour
its token scheme has no name for. That is the architectural reason an adapter was needed
rather than a better prompt.

**The follow-up: "why does it repeat itself?"**

The decoder is autoregressive - each word is chosen from the words already written - with
a strong internal language model. On audio it cannot follow, it stops listening to the
audio and starts listening to itself. Each repeat makes the next more likely, and nothing
stops it except the token limit.

**"Did you try the known fixes?"** Yes, one of them. Whisper's own rule re-decodes a
hypothesis whose gzip compression ratio is too high, because repetitive text compresses
unusually well. We ran it on both models and it changes our numbers by 0.0-0.2 points
(Q7), because our model loops on 1 clip in 177. WhisperX's approach - segmenting with an
external voice detector before decoding - we did not use; our clips come from the human
transcript's own timestamps.

**Why we count loops instead of averaging them away:** one looping clip can score over 100
per cent error and destroy a mean. We report medians and print the runaway count: 13 of
177 off-the-shelf, 1 of 177 ours, 82 of 177 for the seed that diverged.

---

## 28. "Why Wilcoxon and a sign test? Why not a t-test? And why medians?"

All of this answers one question: **we changed something - did it really help, or did we
get lucky?**

**Sign test = count wins and losses.** On each board, did the new version beat the old one?
Count them up. If new wins 34 of 35, that is like flipping a coin 35 times and getting
heads 34 times - it does not happen by luck. **It ignores how big each win was.**

**Wilcoxon = same, but big wins count more.** It also looks at the size of each gap.

**Why run both: they can disagree, and that tells you something.** Imagine new wins by 2
points on three boards, loses by 2 on two boards, and wins by 30 on one. The sign test
says 3-2, almost a tie. Wilcoxon says the single 30-point win outweighs everything. Which
do you believe? The cautious one - one lucky board should not decide a result.

**That is exactly our 3B vs 7B case:**

```
sign test   p = 0.21    says: no real difference
Wilcoxon    p = 0.021   says: there is one
```

The 7B does not win on more boards; on one or two it wins by a lot. **We reported the
cautious one and did not claim significance.** If a panellist spots the 0.021, say exactly
that.

When both agree - the prompt result, better on 34 of 35, sign p = 1.2e-10 - the finding is
solid.

**What a p-value is:** the chance of a result this good if the change did nothing.
p = 0.21 could easily be luck. p = 0.021 happens by luck twice in a hundred.
p = 1.2e-10 essentially never.

**Why the direction is printed next to every p-value:** a p-value only says "this is
surprising". It does not say *surprisingly good* or *surprisingly bad*. A fine p-value can
belong to the side that lost, so we always write which side won.

**Why medians, not averages.** Five clips score 10, 12, 15, 18, **925** - the last one is a
clip where Whisper got stuck in a loop. The average is 196, which is a lie; no clip was
near 196. The median is 15, which is honest. **One broken clip destroys an average but
cannot destroy a median.**

**Why not a t-test:** it works on averages, so the 925 would wreck it. Sign test and
Wilcoxon work on order - the 925 is just "one loss", nothing more.

**Why "paired":** both systems run on the same clips, so we compare one at a time. A hard
clip is hard for both. The unit changes by experiment: **clips** for speech (177),
**boards** for the board and note work (35), **readers** for the survey (20).

---

## 29. "How did you train an 809-million-parameter model on a 12 GB card?"

Two separate tricks. They fix **different** memory problems, and neither alone was enough.

### LoRA - makes the trained part small

Normally fine-tuning changes the model's weight matrices. LoRA **freezes** them and trains
two small matrices beside each one, adding the two paths together.

The attention matrices are 1280 x 1280:

```
full fine-tune of one matrix   1280 x 1280      = 1,638,400 values
LoRA at rank 16                16 x (1280+1280) =    40,960 values
```

**Forty times fewer.** And because AdamW stores extra bookkeeping for every trained value,
the saving is larger than it looks.

Two more things it buys:
- The original model is untouched, so the adapter is a small separate file.
- **That is how the leak-free transcripts work**: three adapters, each trained without one
  lecturer, so each lecture gets a transcript from an adapter that never heard its
  lecturer. With full fine-tuning you would need three complete copies of Whisper.

### Gradient checkpointing - makes the memory used while running small

Training goes forward (audio in, prediction out) then backward (work out the weight
changes). The backward pass **needs the intermediate results from the forward pass**, so
normally every layer's output is kept in memory. For 32 encoder layers and 4 decoder
layers at batch 8, that is about **18 GB**. The card has 12.

Checkpointing keeps only a few points along the way and **recomputes** anything else when
it is needed.

```
without it   ~18 GB   does not fit, training fails
with it       6.1 GB  fits
```

Like a long maths problem: keep every tenth line of working instead of every line, and
redo a few lines when you need one you threw away. **Less paper, more time.** It cost
speed - 1.5 clips per second, about 1.5 hours per seed.

### Why both were needed

| | What it reduces |
|---|---|
| LoRA | the weights being trained, and the optimiser's bookkeeping |
| Gradient checkpointing | the intermediate results stored during the forward pass |

LoRA alone is not enough: even with only the small adapters training, the forward pass
still runs through all 809 million frozen parameters and still produces all those
intermediate results.

**Say this:** *"LoRA made the trained part small; gradient checkpointing made the memory
used while running it small. Together they put an 809-million-parameter model on a 12 GB
consumer card."*

---

### "What are query and value, and why adapt only those?"

Every transformer layer does **attention**: each word looks at the other words and decides
which matter. Think of a library:

- **Query** - what you are looking for. *"I need something about logic gates."*
- **Key** - the label on each book's spine. *"This one is about gates."*
- **Value** - what is actually inside the book.

Compare your query against every key, get a match score, then take a blend of the values
weighted by those scores.

In a sentence: in *"the lecturer wrote it on the board"*, the word **it** sends a query -
*"I am a pronoun, I need the thing referred to"*. Earlier words advertise with keys. The
query matches the noun's key, so **it** pulls in that noun's value.

**They are computed, not stored.** Each comes from multiplying the input by a learned
matrix - `W_q`, `W_k`, `W_v`, `W_o` - each 1280 x 1280 in Whisper, in all 32 encoder and
4 decoder layers. "Adapting q and v" means LoRA on `W_q` and `W_v` only; `W_k` and `W_o`
stay frozen.

| Matrix | Controls |
|---|---|
| `W_q` | what each position **asks for** |
| `W_k` | how each position **advertises itself** |
| `W_v` | what information **gets carried forward** |
| `W_o` | how the result is **recombined** |

Query and value cover *what to look for* and *what to pass along*. The LoRA paper tested
the combinations and found this pair best per parameter spent; speech work followed. It
fits our problem: we are not teaching the model to hear differently, we are changing
**what it writes**.

### "Your tuning says q,k,v,o scored 134.7%. Isn't more capacity supposed to help?"

**It did not underperform - it diverged.** 134.7% is a model collapsed into repetition
loops, the same failure as the diverged seed. Every divergence we saw is at the same
learning rate:

```
lr 2e-3, rank 32        126.6%
lr 2e-3, q,k,v,o        134.7%
lr 2e-3, final seed 42  118.7%
```

Adapting four projections instead of two roughly doubles the trained parameters and so
the change applied per step, which tipped a rate already on the edge.

**Concede the real limitation:** our tuning was **stage-wise** - learning rate first, then
rank, then layers - so every later stage ran at 2e-3. We therefore **cannot say q,k,v,o
is worse in general**, only that it breaks at that rate. At 1e-3 it might be fine.

---

## 30. "A p-value of 1e-26 cannot be real. Are these credible?"

**A fair challenge, and the answer has three parts. Concede the first two.**

**1. Arithmetically the number is right** - 177 paired clips with z = 10.7 does give about
1e-26 under the Wilcoxon normal approximation.

**2. But it answers a question nobody needed answered.** A p-value is the chance of this
data **if the two models were identical**. That was never plausible - one writes English
translations, the other writes Banglish. The tiny number reflects how silly the null
hypothesis is, not how strong the work is.

**3. The real problem: 177 clips are not 177 independent observations.** They come from
**6 lectures and 3 lecturers**. Clips from one lecture share a speaker, a room, a
microphone and a topic, so they vary together. Wilcoxon assumes independence; ours are
clustered. The effective sample is far below 177, so the per-clip p overstates the
evidence.

**The bracket to quote:**

| Unit | Result | p |
|---|---|---|
| per clip | better on 164 of 177 | ~1e-26, assumes independence |
| **per lecture** | **better on 6 of 6** | **0.031**, assumes nothing |

The truth is between them. **The per-lecture result is the one that survives the
objection**, because lectures really are independent of each other.

**Say this:** *"You are right that clips within a lecture are not independent. At the
lecture level it is 6 of 6, which is p = 0.03 - still significant, and that is the
conservative version. We report the per-clip test because it is standard in ASR, but the
lecture-level result is the one that assumes nothing."*

**What actually makes the result convincing** is not the p-value: error cut by three
quarters, every lecture improved, and two random seeds agreeing to 0.2 points. Lead with
those.

**A related correction we made ourselves (2026-10-03).** The tables once read
`p < 1e-30`. The evaluation code stored `wilcoxon_p: 0.0` because `1 - normal_cdf(z)`
underflows above z = 8.3, and the zero was read as "smaller than any threshold". The true
values were 1.3e-26 and 1.7e-29. We now quote `p < 0.001` everywhere and fixed the code
to report the asymptotic tail. If asked, this is a numerical bug that was found and
corrected, not a figure anyone invented.

---

## 31. "What is an era?" / "Walk us through the board pipeline."

**An era = one filling of the board, the stretch between two erases.** Each era produces
one board image. BanglaASR7 has five in fourteen minutes, one per topic (intro, NOR, NAND,
X-OR, X-NOR). "145 boards" means 145 eras across 40 lectures.

**Why the word is needed:** the mosaic takes each tile from whatever moment that tile was
unobstructed. Searching the whole lecture, it would take the left half from the NAND board
and the right half from the X-NOR board and produce a clean picture of a board **that never
existed**. Detecting the wipe and rebuilding each era separately prevents that.

**It is our own coinage - the panel will not know it.** Say "one filling of the board" and
gloss it once.

### The pipeline in order

1. **Frames** - one every 2 seconds, at most 1920 wide.
2. **Split into eras** - erase events detected on a coarser 10-second pass.
3. **Rebuild each era as a mosaic.** Cut the frame into small overlapping tiles; find the
   lecturer with DeepLabV3 plus a shadow mask; for each tile separately take it from a
   moment when he was not in front of *that* tile; blend back together. **Every pixel is
   real camera output** (Q10). The X-NOR board needed 9 different frames.
4. **Clean up for display** - whiten the background. Cosmetic only: the strokes are camera
   pixels, the white behind them is not.
5. **Find boxes** (Q23) - erase the board frame, find ink, group touching ink, rectangle
   per group, drop specks, merge near-touching rectangles.
6. **Draw numbered coloured boxes** on top; pixels underneath unchanged.
7. **The vision model reads it twice** (Q25) - whole board for the 88.8% number, and per
   box for the names and the figure (Q24).
8. **Both go to the note model** with the transcript.

**The shape to state:** steps 1-6 are ordinary image processing with no model deciding
anything. A model appears only at step 7, and only to supply words.

### Seeds, while we are here

A seed fixes the random number generator - the LoRA matrices' starting values and the
order examples are shuffled. Same seed, same run exactly. 42 and 1 are arbitrary (Q17).
**We run two to check the result is not luck:** 15.8 and 16.0 means the method works;
16.2 and 118.7 at 2e-3 means it does not.

---

## Never say these

- "96.1 -> 81.8" - we retired it. It came from a split with a leak.
- "The clean-up made it worse" - p = 0.07. There is no direction to claim. Say "no
  measured difference".
- "The prompt is worth 17 times the model size" - that divides by a number that is not
  significant.
- "Every quote in the notes is verified" - Banglish notes only.
- "Wilcoxon p < 1e-30" - the real value is about 1e-26, and clips are clustered. Say
  "p < 0.001" and "better on all 6 lectures".
- Any Term F1 difference below about 8 points - that metric moves 8 points by itself on
  the same data.
