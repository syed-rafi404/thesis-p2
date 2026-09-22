# NEXT STEPS — read this file, ignore everything else

If you are lost, start here. Updated 2026-09-22 (on the 3060).

---

## BEFORE THE DEFENSE: what matters most (2026-09-22)

1. **The report will be rewritten from scratch** (you, with Claude, when the time comes). The old
   LaTeX in `P2\chapters\` will NOT be submitted. It still contains fabricated numbers (fusion
   p = 0.003, Cohen's d = 0.96, the 68.2 / 71.5 / 42.3 / 73.9 table, 16,558 characters), so
   **never copy a number or a sentence from it. Numbers come only from RESULTS.md.**
2. **Be able to explain everything.** Claude can write a one-page explanation plus the 15 likely
   panel questions with honest answers.
3. **Check BRAC's rule on declaring AI help**; include a statement if it asks for one.
4. The notes pipeline (THE GOAL below) and the survey: a strong bonus, not needed to pass.

If fusion was shown as a success in P2 (report or poster), prepare one sentence: "re-analysis showed
the earlier fusion claim did not hold; the measured effect is +0.7 points, not significant."

---

## THE GOAL: what the finished thesis does (your words, 2026-09-22)

Put in a Banglish lecture video; get back a lecture note a student can actually use.

1. **Speech.** Fine-tuned Whisper writes a Banglish transcript. Not 100% right, but better than
   off-the-shelf Whisper.
2. **Board.** A clean picture of each board with the lecturer removed, numbered coloured boxes
   around each part (title, definition, truth table, ...), each box named by the VLM.
   Look: `F:\thesisP2\thesisP2\Temp\mockup_nand_board.jpg`
3. **Notes.** An LLM combines the board (from the VLM) and the transcript into a real lecture note
   that points at the boxes ("look at the purple box 5").
   Target look: `F:\thesisP2\thesisP2\Temp\MOCKUP_lecture_note.html`
4. **Two versions of every note:** English (with the lecturer's own Banglish words quoted and
   translated, like the mockup) and Banglish. The student picks one.
   **Bangla dropped (decided 2026-09-22):** it would be the weakest version, it is only the LLM
   translating (not our contribution), and it adds checking work before the defense. Future work.

### Where each part stands

| Part | Status |
|---|---|
| 1. Fine-tuned Whisper transcript | **Done, measured.** 72.8% -> 50.3% of characters wrong, for every lecturer |
| 2a. Clean board | **Done** for all 45 boards (person-detection network + shadow + clean-up). Judged by eye; VLM score still to come |
| 2b. Box positions | **Done** (found from the ink). Never measured; sometimes splits or merges boxes |
| 2c. Box names by the VLM | **Not built** |
| 3. Notes that point at the boxes | **Not built** (the parts exist) |
| 4. Two languages | English and Banglish options exist in the code; the new layout is not built |

### What we agreed to expect (honest limits)

- **The mockup is Claude's handwork, not pipeline output.** Box names and all the text were
  written by Claude; the first lecturer quote was hand-edited ("ma" -> "mane", "barcho lash" ->
  "bar"). Call it the target design, never a result.
- The real notes will be plainer than the mockup. A bigger notes model (Qwen3-32B) closes part of
  the gap, not all: it only reads the VLM's text, never the board itself.
- **Always the clean board.** The "VLM draws boxes around the teacher" route is dropped.
- **Every version inherits the transcript's errors** (about half the characters wrong). The board
  carries most of the facts.
- **"The notes are good" needs people.** A survey of about 20 people once everything is done.
  Show each person the old notes and the new notes of the same lecture: "which helps you more?"
  plus a 1-5 rating. That gives a before/after result ("16 of 20 preferred the new notes"), not
  just a score. Without it, say "we demonstrate", not "we show the notes are good".

### The plan (scope frozen; nothing new until the defense)

**A. Build on the 3060 (Claude, about a day). Waiting for your "go".**
1. VLM box naming: numbered boxes drawn on the clean board; Qwen2.5-VL names each box and writes
   what is in it.
2. New notes prompt: one section per board, points at the boxes, two languages (english with
   quoted Banglish, and banglish). Quotes only word for word from the transcript: a checker drops
   any quote that is not in it (this also fixes the old broken-quotes problem). The old prompts
   stay.
3. Page builder: Markdown + HTML with the annotated board, like the mockup.
4. One command for a whole lecture.
5. Tested here with a stand-in for Qwen (the 3060 cannot hold it).

**B. Run on the 5090 (a few hours).**
1. `git pull`
2. The VLM reads the new clean boards; score old vs new boards on your answer keys. This gives the
   board work a real number instead of "looks better".
3. Notes for all lectures x 2 languages with the chosen notes model; re-score board recall (the
   88.0% came from the 7B model).
4. Side by side: the NAND section from Qwen2.5-7B vs Qwen3-32B vs the mockup.

**C. You (no coding).**
1. Once the notes exist: the survey of about 20 people (old vs new notes of the same lecture,
   which helps more, plus 1-5 for useful / correct / easy to read). Claude can make the form.

**After the defense: the 10 hours of data (8 h train / 2 h test).** 5090 time, estimated from the
2026-09-21 evening runs (about 1 h per large-Whisper training run on about 1.5 h of audio, including
evaluation) and scaled up; the first real run gives the true number:

| Job | Estimate | Needed? |
|---|---|---|
| Final fine-tune, 8 h / 2 h split, 2 seeds | 6-10 h | yes (headline) |
| Fine-tuned transcripts for all lectures (~50) | ~1 h | yes (notes need them) |
| Clean boards for new lectures | ~1 h | yes |
| VLM reads and names all boards (~200) | 2-4 h | yes |
| Notes for all lectures x 2 languages (Qwen3-32B) | 3-5 h | yes |
| Leave-one-speaker-out with more data, 1 seed | 3-4 h per lecturer | good, not required |
| Scaling curve 2 / 4 / 6 / 8 h | 8-12 h | nice to have |

Required: ~15-20 h (a night and a day). Everything: ~35-50 h (about two days nonstop). All runs
unattended. No new board answer keys for new lectures: the 45 checked boards already carry the VLM
result.

**Who does what.** Claude: all coding, all runs, RESULTS.md, survey form and analysis, report
structure/tables/figures. You: the go-aheads, checking outputs (~30 min per round), the 10 h of
transcripts in the right format and the videos on the 5090, keeping the 5090 on, the ~20 survey
people, and writing the report.

### Decisions still open (one at a time)

1. "Go" on building A.
2. Notes model: Qwen3-32B on the 5090 (recommended) or keep the 7B. Optional extra row: a paid API
   model (Claude or GPT) as "best possible", only if you accept sending lecture text out and a few
   dollars.
3. Figure 6.5: an error analysis, or drop the figure.

---

## The final numbers

Quote only these; each has its command in RESULTS.md.

| What | Result | RESULTS.md |
|---|---|---|
| Speech: fine-tuned Whisper, each lecturer held out once | CER 72.8% -> **50.3%**, WER 95.3% -> **75.7%**; 6 of 6 runs p < 1e-05, plain decoding | 1.5 |
| Is the WER only spelling? | No: spelling-fair WER 74.8%, fuzzy WER 68.2% | 1.6 |
| VLM reading the board, 35 hand-verified boards | keyword prompt 31.2% -> full transcription **88.8%**; better on 34 boards, worse on 0 | 5.0 |
| VLM on a third lecturer's boards | **89.7%** | 5.0 |
| Notes, 35 boards | board content in the notes: 37.2% -> **88.0%** | 5.0 |

- **Never quote:** 96.1% -> 81.8% (leaked split), "the curve is still falling", or board-recall
  numbers from RESULTS.md 5.1-5.3 (draft keys).
- Board answer keys: all 45 boards checked by you on 2026-09-22. Done.
- Example transcript lines (lecture 6, clip 22: human / off-the-shelf / fine-tuned) are real,
  word for word, from `artifacts\ft_work_AC\eval_AC_turbo_seed42_greedy.json`. Keep the "..."
  when showing them: the full clip gets worse after the cut.

## The board pictures (2026-09-22, on the 3060)

- All 45 boards rebuilt with a pretrained person-detection network (DeepLabV3) plus a shadow
  detector, then a whiteboard clean-up. Recovers writing the old method lost: the TTL diagram
  (lecture 10), and 7 of 8 digits of lecture 6's binary number (old: 5). RESULTS.md 4.1.1-4.1.2.
- Cleaned boards: `F:\thesisP2\thesisP2\output\annotation_demo\all9_deeplab_shadow\clean\`
  (lectures 1-9) and `F:\thesisP2\thesisP2\output\annotation_demo\speaker3_2s_deeplab_shadow\clean\`
  (lectures 10-13). Side-by-side sheets `compare_*.jpg` in the two folders above. Both are in git.
- A cleaned board's white background is not camera pixels (the writing is). Say "enhanced" when
  you show one.
- Generative AI fill-in was not used on purpose: it would invent writing.

## If someone asks "what is the thesis"

> Banglish classroom speech is unsolved. We fine-tuned Whisper on our own lectures: on a lecturer
> it never heard, the share of characters it gets wrong drops from 73% to 50%, for each of three
> lecturers. A vision-language model reads the whiteboard: 31% -> 89% of the board content, by
> changing only how we ask it. Together they produce lecture notes that carry 88% of what was on
> the board, against 37% before. Fusing vision into the speech model does not work, and we show
> why; the metric the field used is anti-correlated with transcription quality, and we show that
> too.

## Writing (your team)

The report is rewritten from scratch later, with Claude's help. The old `P2\chapters\` LaTeX is a
record only; never copy numbers from it.

## Moving between PCs

After `git pull` on a PC that has not run it yet:

```
python scripts/restore_artifacts.py --apply
```

On the 3060 use `F:\thesisP2\envs\thesis_ft\Scripts\python.exe`. It puts the adapters and results
beside the repo and rebuilds the audio clips.

---

## History (older entries, kept as a record)

- **2026-09-21, the speaker split was wrong, and is fixed.** Video 6 is the same lecturer as 7-9;
  the old split trained on it. Everything was re-run. The old run is kept untouched as
  `ft_work_v1_video6_in_train`.
- **2026-09-21, Speaker3 (videos 10-13) added.** A genuinely third lecturer (voiceprints agree).
  This made leave-one-speaker-out possible, which is now the headline (RESULTS.md 1.5).
- **2026-09-21, the VLM and notes experiments** ran on the 5090 (keyword vs full-transcription
  prompt; notes A-D one change at a time). Commands and final numbers on the verified keys:
  RESULTS.md 5.0. The 5.1-5.3 numbers used draft keys and are superseded.
- **2026-09-22, on the 3060:** answer keys verified; spelling-fair WER (1.6); boards rebuilt
  (4.1.1-4.1.2); the mockup; this plan.

## Where the detail lives

- **[RESULTS.md](RESULTS.md)** — every number, and the command that regenerates it.
  If a number is not there, it does not go in the paper.
- **[CLAUDE.md](CLAUDE.md)** — context for the next Claude session, on any machine.

You do not need to remember any of it. It is written down.
