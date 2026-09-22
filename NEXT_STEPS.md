# NEXT STEPS — read this file, ignore everything else

If you are lost, start here. Updated 2026-09-22 (on the 3060).

---

## MASTER PLAN, DAY BY DAY (set 2026-09-22 evening)

| Day | Who | Task |
|---|---|---|
| 22 Sep (today) | You + team | Ground truth for ~3 more hours (videos from 18-43); lecture 9's timestamps, then remove "[Needs recheck]" from its name. Tell Claude if any tool drafted a transcript (those are training-only). |
| 22-23 Sep night | 3060 (runs by itself) | **Hyperparameter tuning, pre-registered** (`data\splits\tuning_plan.md`, committed before any result): learning rate (5e-4, 1e-3, 2e-3), then LoRA rank (8, 16, 32), adapted layers (q,v vs q,k,v,o), epochs from the validation-loss curve, and a second seed for the winner; the default is kept unless the winner beats it by more than its seed-to-seed difference. Scored on 3 validation lectures fixed beforehand (BanglaASR2, 12, 14), never test. About 7-8 trainings, done around 01:00-02:00; committed and pushed by itself. Results: `artifacts\ft_work_lr\tuning_summary.md`, chosen settings `tuning_result.json`; logs in `F:\thesisP2\ft_work_lr\`. The 6 h and 10 h runs use them with `--tuned`. |
| 23 Sep | Claude on the 5090 | "FIRST THING ON THE 5090" below; measure real run times; notes pipeline (stage B): VLM on clean boards with old-vs-new board score, box names, notes with the 7B and scoring; start the 32B download. |
| 23 Sep | You + Claude | Start the report from scratch: Claude gives structure, tables, figures from RESULTS.md; you write. (Optional: the board check page, 30-40 min.) |
| 24 Sep | Claude on the 5090 | Notes with the 32B; NAND section side by side; fix what the first real runs show. When the ground truth arrives: `check_new_data.py`, `set_speaker_ids.py --apply`, `validate_ground_truth.py --fix`. |
| 24 Sep | You + Claude | Writing continues. |
| **25 Sep** | Claude on the 5090 | **6 h run**, 2 seeds (~2-2.5 h); RESULTS.md and figures updated the same day. |
| **26 Sep** | You | **Draft submission.** Claude first checks every number in it against RESULTS.md. |
| **27 Sep** | Claude on the 5090 | **10 h run** + scaling curve (~6-7 h; needs the rest of the ground truth by the morning); then the demo: `run_lecture.py` on a video with no transcript (~30 min, you confirm the video). RESULTS.md and figures updated. |
| 28 Sep | You + Claude | Slides (Claude drafts content: numbers, figures, demo screenshots, honest limits); Q&A prep. 5090 spare only if a run failed. |
| **29 Sep** | You | **Slides submission.** |
| Before the defense | You | BRAC's rule on declaring AI help; rehearse. |

Dropped or later: Bangla notes (dropped), the classmate survey (not now), Figure 6.5 (drop; the
report is rewritten anyway).

**Training speed, measured on the 3060 (2026-09-22):** the big Whisper (large-v3-turbo + LoRA, the
headline recipe: batch 8, 8 epochs) trains here only with `--grad-checkpointing` (same learning,
less memory: 6.1 of 12 GB; without it, out of memory at ~18 GB), at 1.5 clips/s. For the 6 h run
(~950 training clips x 8 epochs) that is about **1.5 h per seed on the 3060, ~3 h for two seeds**.
The 5090 needs no checkpointing and is roughly 4x faster: an estimate of **20-30 min per seed**
there (the earlier "about 1 h per seed" was conservative). **So the 3060 is a real backup** if the
5090 is busy: same command with `--extra-train-args "--grad-checkpointing"`, and
`HF_HUB_OFFLINE=1` (on the 3060 a network lookup crashes Python; the models are cached).

---

## FIRST THING ON THE 5090 (the 3060 session ended 2026-09-22 ~15:00)

Your first message to Claude on the 5090:

> git pull first. Read CLAUDE.md and NEXT_STEPS.md, then do "FIRST THING ON THE 5090". The
> previous conversation is in Random\473f0a12-fd36-4593-bbe1-2fd1f6c78790.jsonl; read it only if
> something is unclear. The videos are copied to data\raw\live_classroom.

Claude, on the 5090, in order:
1. `git pull`. Then confirm the 3060's automatic push arrived: `git log --oneline -8` shows
   "Boards for the newer lectures (6-9, 18-43) and the board completeness check page", and
   `output\lectures\board_completeness_check.html` exists. If not, the 3060 job did not finish:
   its log is `F:\thesisP2\claude_transfer\finish_log.txt` on the 3060 (push from there later).
   Nothing for the 25 Sep and 27 Sep runs depends on those boards; only the demo does.
2. Videos: the user's USB has them in `H:\Thesis Dataset\` (43 files, BanglaASR1-43, checked equal
   by name and size to the 3060's `data\raw\live_classroom` on 2026-09-22; `BanglaASR39.mp4` was
   still called `video_20260523_232405.mp4` on the USB and was renamed). Copy them into
   `D:\T2520875\thesisP2\thesisP2\data\raw\live_classroom\` and move the old
   `data\raw\Speaker1`, `Speaker2`, `Speaker3` folders out of `data\raw` (e.g. to
   `D:\T2520875\old_raw_layout\`), asking the user first. Then `python scripts/check_new_data.py`
   must pass.
3. Memory: the USB's `H:\claude_checkpoint\claude_memory_for_5090.zip`; its README.txt says where
   the conversation and the memory notes go.
4. `python scripts/check_environment.py`, and free space on D:: about 170 GB is needed (videos ~75
   GB at 10 h, Qwen2.5 models ~31 GB already there, Qwen3-32B ~65 GB).
5. Measure the real run times from this machine's file timestamps (stage B step 1 below), then go
   on with "TASKS IN ORDER" step 4 (23/24 Sep).

---

## TASKS IN ORDER, TO REACH THE GOAL (set 2026-09-22; survey left out on purpose)

On the 3060 (Claude), before the 5090 sessions:
1. **DONE 2026-09-22.** `run_lecture.py --video <file>`: one command, video in, annotated notes
   out. Tested on BanglaASR19 (no ground truth, never trained on) with Qwen stand-ins: all steps
   real except the two Qwen ones; 4.2 min of video in about 2.3 min on the 3060.
2. Boards for the newer lectures 6-9 and 18-43, made here (this PC has the person-detection
   library) and pushed. Then the 5090 needs no extra library: `run_lecture.py` skips steps whose
   output exists.
3. Pick the demo video: one with no ground truth (never trained on). Claude suggests one with a
   clear board; you confirm.

On the 5090:
4. 23/24 Sep: notes pipeline for the 13 scored lectures (stage B); fix what the first real run
   shows; measure real run times. (Only for a video recorded after today would the 5090 need the
   person-detection library, torchvision; without it the board step falls back to the older
   lecturer mask and says so.)
5. 25 Sep: the 6 h run (draft).
6. 27 Sep: the 10 h run and scaling curve; then `run_lecture.py` on the demo video with the final
   model (~30 min): the demo for the slides.
   ```
   python scripts/run_lecture.py --video data\raw\live_classroom\BanglaASR<demo>.mp4 --adapter <ft_work>\lora_final --tag final
   ```

After (no GPU):
7. RESULTS.md and figures updated for the draft (26 Sep) and the slides (29 Sep).

You: copy the videos to the 5090 and move the old `data\raw\Speaker1-3` folders there out of
`data\raw`; name ground-truth files `BanglaASR<n>_ground_truth.txt`; lecture 9's timestamps;
confirm the demo video (not needed for the 26 Sep draft).

**Carry on the USB to the 5090:** the videos, and
`F:\thesisP2\claude_transfer\claude_memory_for_5090.zip` (the whole conversation and Claude's
memory; its README.txt says where each file goes). Everything else comes with `git pull`.

**Optional check by you (~30-40 min, any PC):** open
`output\lectures\board_completeness_check.html` (on the 5090 after `git pull`:
`D:\T2520875\thesisP2\thesisP2\output\lectures\board_completeness_check.html`). Each new clean
board is shown next to two real video frames; mark "all there" or "something missing". Then press
"Copy my results" and paste it to Claude. It turns "the new boards look clean" into a number you
checked yourself. Not needed for the results in RESULTS.md.

---

## DATES AND 5090 SESSIONS (set 2026-09-22)

Draft submission **26 Sep**. Slides **29 Sep**.

| When | 5090 job | About how long | Longest unbroken |
|---|---|---|---|
| 23 or 24 Sep | Notes pipeline (stage B below): VLM on clean boards, box names, notes 7B and 32B, scoring | 4-6 h incl. the ~65 GB 32B download (resumes) | ~1 h |
| **25 Sep** | **6 h run**: ~4.8 h train / 1.2 h test, 2 seeds, no scaling curve (results go in the draft) | ~2-2.5 h | ~1 h |
| **27 Sep** | **10 h run**: ~8 h train / 2 h test, 2 seeds, scaling curve 2/4/6/8 h (results go in the slides) | ~6-7 h | ~1.5 h |
| 28 Sep | Spare, only if a run failed | - | - |

After 27 Sep the 5090 is not needed: results, figures and slides need no GPU. Times are estimates
until the first sitting measures them (stage B step 1). For the 25th, drop `--curve-hours ...` from
the run command in "Running it on the 5090".

On the 3060: nothing required. Optional: board pictures for new lectures 6-9 and 18-43 (only if
you want notes for them; ~1 h here). If ground truth arrives on the 3060 first, Claude checks it
with `check_new_data.py`, fixes it and pushes it.

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

### The plan (everything before the defense)

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

**BEFORE the defense (your decision, 2026-09-22): the 10 hours of data (8 h train / 2 h test).**
**Deadline: the final transcripts must be in at least 2 days before the defense**, so the 5090 has
time to train, evaluate and the results can be written up. Everything that does not need the data
is built and tested (below); when the data lands it is one command on the 5090.

**The split (your decision, 2026-09-22): random whole videos, not by speaker.** About 8 h train and
2 h test, chosen at random with a fixed seed so it can be repeated; every lecturer has videos on
both sides; a video is never cut in two. Two honesty rules: (1) the thesis says the test lecturers
were also heard in training, so this number is "new lectures from known lecturers", easier than an
unseen lecturer; (2) the unseen-lecturer result you already have (72.8% -> 50.3%, RESULTS.md 1.5)
stays as the second, harder number.

**Ready (built and tested on the 3060, 2026-09-22):**
- `prepare_data.py --split-by video --test-fraction 0.2 --split-seed 0`: picks whole lectures per
  lecturer, close to 20% of each lecturer's minutes, keeps everyone on both sides, and warns if a
  lecturer ends up only in the test set. Tested on the 2.7 h there is now.
- The new numbering is handled: each lecture gets its own audio (checked lecture by lecture: new
  10-13 use old 6-9's recordings, new 14-17 Speaker3's, new 6-8 their own new videos).
- Files you mark by name, like `[Needs recheck]BanglaASR9...`, are skipped until you remove the
  marker. Remove it when lecture 9's timestamps are in.
- Timestamps with stray spaces were repaired in all current files (`validate_ground_truth.py --fix`,
  a `.bak` copy of each original sits beside it), and the script now warns about any it cannot read.
  The same defect touched 10 test clips of the published headline; without them it is 72.2% ->
  49.6% CER, so the published number stands (RESULTS.md 1.5).

**The plan as it stands (2026-09-22): ~10 h of video on the 5090, ground truth for ~6 h.** Only
lectures with ground truth are used to train and test; videos without it are not. With a 20% video
split that is about 4.8 h to train and 1.2 h to test.

**Running it on the 5090, in order:**

1. **You:** copy `F:\thesisP2\thesisP2\data\raw\live_classroom\` (all videos, new names) to the
   5090's `D:\T2520875\thesisP2\thesisP2\data\raw\live_classroom\`, and move the old
   `data\raw\Speaker1`, `Speaker2`, `Speaker3` folders on the 5090 out of `data\raw` (they use the
   old numbers; if a video name exists twice with different content the run stops).
2. **You:** every new ground-truth file named exactly `BanglaASR<n>_ground_truth.txt`, the same
   `<n>` as its video, in `data\ground_truth`. No Speaker ID line needed. Lecture 9: add its
   timestamps and remove "[Needs recheck]" from the name.
3. **Claude, on the 5090:**
   ```
   git pull
   python scripts/validate_ground_truth.py --fix
   python scripts/speaker_groups.py              (only if videos were added after 2026-09-22)
   python scripts/set_speaker_ids.py --apply
   python scripts/check_new_data.py
   python scripts/run_p3_experiment.py --split-by video --test-fraction 0.2 --split-seed 0 --model openai/whisper-large-v3-turbo --audio-dir D:\T2520875\thesisP2\ft_work_3spk\audio_cache --tuned --tag final
   python scripts/run_p3_experiment.py --split-by video --split-seed 0 --model openai/whisper-large-v3-turbo --skip validate prepare curve --tuned --extra-train-args "--seed 1" --tag final_s1
   ```
   `--tuned` takes the settings chosen by the pre-registered tuning
   (`artifacts\ft_work_lr\tuning_result.json`, 22-23 Sep night). The split locks the three
   validation lectures out of the test set by itself. For the 27 Sep 10 h run add
   `--curve-hours 2 4 6 8` to the first command. On the 3060 instead of the 5090: add
   `--grad-checkpointing` inside `--extra-train-args` and set `HF_HUB_OFFLINE=1`.
   `check_new_data.py` stops on anything that would corrupt training silently: a transcript with no
   matching video, a name used by two videos, a missing Speaker ID, unreadable timestamps, a
   transcript longer than its video, a Speaker ID the voice check disagrees with. The runner runs
   it first and will not train until it passes. The second training seed matches how the headline
   was run (two seeds). Rough time for ~6 h of ground truth: about 1 h per seed, 2-3 h for the
   curve.

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
   paired with the old lecture 6 audio (fixed: the scripts now use this table). New 6-8 are
   complete: their videos are short (6.7, 7.8, 5.0 min), not partly transcribed as Claude first
   said. New 9 has no timestamps yet; you are adding them.

   **Voice check of all 43 videos (2026-09-22, `output\speaker_check\speaker_groups.md`): 1-9 are
   lecturer A, 10-13 B, 14-43 C**, exactly as you said. Same lecturer scores 0.98-0.998, different
   lecturers 0.59-0.90. So ground truth for 18-43 gets `# Speaker ID: C`; `set_speaker_ids.py` adds
   it automatically.
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
