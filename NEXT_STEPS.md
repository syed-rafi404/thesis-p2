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

**A. Build on the 3060 (Claude). Built 2026-09-22 and tested with a stand-in model.**
Scripts: `label_boards.py` (boxes + VLM names), `build_lecture_notes.py` (sections, quote checker,
box-reference check, Markdown + HTML), `notes_page.py` (the page), `annotated_prompts.py` (the
prompts, beside the old ones), `make_loso_transcripts.py` (leak-free transcripts).
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
1. `git pull`. Then, before anything else, measure real run times from the 5090's own file
   timestamps (the copies on the 3060 all carry the git checkout time). Compare the write times of
   `lora_turbo_seed*\adapter_model.safetensors` and `eval_turbo_*.json` in
   `D:\T2520875\thesisP2\ft_work_ABtoC`, `ft_work_BCtoA`, `ft_work_AC`, and of
   `board_text_*.md` / `notes_*.md` in `output\live_focused\no_gaze\interval_10s\*`. Replace the
   estimated 10-hour table below with measured numbers.
2. The VLM reads the new clean boards; score old vs new boards on your answer keys. This gives the
   board work a real number instead of "looks better".
   ```
   python scripts/transcribe_boards.py --all --source clean
   python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 --compare-names board_text_mosaic.md board_text_clean.md
   python scripts/score_board_recall.py --runs output/speaker3_runs --gt data/board_truth/draft_speaker3 --compare-names board_text_mosaic.md board_text_clean.md
   ```
3. **Done on the 3060 (2026-09-22):** leak-free, timestamped transcripts for all 13 lectures,
   `transcript_loso.txt` in each lecture folder, each made by the model that never heard that
   lecturer (`scripts/make_loso_transcripts.py`). The notes use these.
4. The VLM names the boxes on every board:
   ```
   python scripts/label_boards.py --all
   python scripts/label_boards.py --all --boxes vlm      (optional: the VLM draws the boxes itself)
   ```
5. Notes in both languages: first with the 7B model (the one behind the 88.0%), then the bigger one
   (`pip install bitsandbytes` first; the 32B download is ~65 GB):
   ```
   python scripts/build_lecture_notes.py --all --language both --tag 7b
   python scripts/build_lecture_notes.py --all --language both --tag 32b --model Qwen/Qwen3-32B --quant 4bit
   python scripts/score_board_recall.py --gt data/board_truth data/board_truth/draft_lectures1to6 --compare-names notes_C_vlm.md notes_annotated_english_7b.md
   ```
   (and the same for `_32b`, and with `--runs output/speaker3_runs --gt data/board_truth/draft_speaker3`)
6. Side by side: the NAND section (lecture 7, board 3) from the 7B and the 32B, next to the mockup.
   Each notes page is `notes_annotated_<language>_<tag>.html` in the lecture folder; its `.json`
   counts quotes kept and removed and references to boxes that do not exist.

**C. You (no coding).**
1. Once the notes exist: the survey of about 20 people (old vs new notes of the same lecture,
   which helps more, plus 1-5 for useful / correct / easy to read). Claude can make the form.

**After the defense: the 10 hours of data (8 h train / 2 h test).**

**The split (your decision, 2026-09-22): random whole videos, not by speaker.** About 8 h train and
2 h test, chosen at random with a fixed seed so it can be repeated; every lecturer has videos on
both sides; a video is never cut in two. Two honesty rules: (1) the thesis says the test lecturers
were also heard in training, so this number is "new lectures from known lecturers", easier than an
unseen lecturer; (2) the unseen-lecturer result you already have (72.8% -> 50.3%, RESULTS.md 1.5)
stays as the second, harder number. The data script only splits by speaker today; Claude adds the
video option before the first training run (discussed on 2026-09-21, never built until now).

5090 time, estimated from a
measured 3060 run (file timestamps in `F:\thesisP2\ft_work_v1_video6_in_train\`, 2026-09-20:
whisper-small trained on 1.17 h of audio in ~3 min, each evaluation ~7 min), scaled for the larger
model (~7x the work) and the faster card (~4x). Training time grows with the training data;
evaluation time grows with the test data. The first real run gives the true number:

| Job | Estimate | Needed? |
|---|---|---|
| Final fine-tune, 8 h / 2 h split, 2 seeds, with evaluation | 1.5-2.5 h | yes (headline) |
| Fine-tuned transcripts for all lectures (~50) | 0.5-1 h | yes (notes need them) |
| Clean boards for new lectures (mostly frame extraction) | ~1 h | yes |
| VLM reads and names all boards (~200) | 1-1.5 h | yes |
| Notes for all lectures x 2 languages (Qwen3-32B, 4-bit) | 3-5 h (~1 h for the ~10 test lectures only) | yes |
| Leave-one-speaker-out with more data, 1 seed | 1-1.5 h per lecturer | good, not required |
| Scaling curve 2 / 4 / 6 / 8 h | 3-4 h | nice to have |

Required: ~7-11 h (best guess ~9 h). Everything: ~15-20 h (best guess ~17 h). Plus the Qwen3-32B
download (~65 GB; resumes if interrupted). All runs unattended.

**It can be split into sittings.** The longest unbroken job is one training run on 8 h of audio,
about 1 h (1.5 h with its evaluation; evaluation can also be a separate sitting), because
`train_lora.py` saves nothing until the end (`save_strategy="no"`). Transcripts, clean boards, VLM
and notes all take `--run-dir` and go one lecture at a time, so they stop and continue anywhere.
Suggested sittings: (1) train seed 1 + evaluate, ~1.5 h; (2) seed 2 + evaluate, ~1.5 h;
(3) transcripts + clean boards, ~1.5-2 h; (4) VLM, ~1-1.5 h; (5-7) notes in batches, ~1-1.5 h each.
If even 1 h unbroken is hard: Claude can make training save after each epoch so it can resume
(small change, same results; ask first, it touches the training code). (A first estimate of
15-20 / 35-50 h was too high: it scaled evaluation time with the training data.) No new board answer keys for new lectures: the 45 checked boards already carry the VLM
result.

**Who does what.** Claude: all coding, all runs, RESULTS.md, survey form and analysis, report
structure/tables/figures. You: the go-aheads, checking outputs (~30 min per round), the 10 h of
transcripts in the right format and the videos on the 5090, keeping the 5090 on, the ~20 survey
people, and writing the report.

### Decisions still open (one at a time)

0. **New lecture numbering (yours, 2026-09-22), grouped by lecturer: 1-9 lecturer A, 10-13
   lecturer B, 14-17 lecturer C.** `# Speaker ID:` lines added to all 17 ground-truth files.

   | New name | Was | Lecturer |
   |---|---|---|
   | 1-5 | 1-5 | A |
   | 6-9 | (new lectures) | A |
   | 10-13 | 6-9 | B |
   | 14-17 | 10-13 | C |

   Everything measured so far (RESULTS.md, answer keys, lecture folders, transcripts) uses the OLD
   numbers; the exact ground truth behind those results is frozen in
   `F:\thesisP2\thesisP2\data\ground_truth_v1_2026-09-21\`. Before any new training, Claude makes
   the scripts use this table: they find audio by number, and without it a new BanglaASR6 would be
   paired with the old lecture 6 audio. The new files need timestamp fixes (the checker can repair
   them) and are partial (new 6: 6.7 min, 7: 7.8 min, 8: 5.0 min). New 9 has no timestamps yet;
   you are adding them.
   **Speaker ID lines are NOT needed in the files** (decided 2026-09-22): the split is by random
   video. Claude still needs to know which lecturer each video is (to keep every lecturer on both
   sides, and for the thesis sentence "test lecturers were also heard in training"); it works that
   out by voice with `scripts/verify_speakers.py`, and you confirm.

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
