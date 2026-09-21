# NEXT STEPS — read this file, ignore everything else

If you are lost, start here. One page. Updated 2026-09-21.

---

## 2026-09-21: the speaker split was wrong, and is now fixed

- Video 6 is the same lecturer as 7-9 (your `data\raw\Speaker2` folder; the audio agrees:
  `output\speaker_check\speaker_similarity.md`). The old split trained on it, so the "unseen
  speaker" had been heard. **Do not quote 96.1% -> 81.8% any more.**
- New split: train 1-5 (55.6 min), test 6-9 (184 clips). Plain greedy decoding: no gain,
  the fine-tune loops on 58 clips. With Whisper's standard loop safeguard on both models:
  **WER 95.0% -> 78.8-83.3%, CER 73.4% -> 54.6-59.4%, p < 1e-05, replicated 3 times**, better
  in all four lectures.
- Scaling curve: 18 minutes of data already gives most of the gain; after that it is flat within
  noise. **Drop the old "the curve is still falling" argument**; it came from the leaked split.
- Old run kept untouched in `D:\T2520875\thesisP2\ft_work_v1_video6_in_train\`.

## On the 3060 (or any other PC): two commands

```
git pull
python scripts/restore_artifacts.py --apply
```

The second one puts the corrected adapters and results beside the repo, archives the old leaked
`F:\thesisP2\ft_work` as `ft_work_v1_video6_in_train`, and rebuilds the audio clips. Run it with
the 3060's fine-tune Python: `F:\thesisP2\envs\thesis_ft\Scripts\python.exe`. The 3060 cannot run
Qwen; the Qwen results are already in the repo.

## 2026-09-21: Speaker3 (videos 10-13) added

- A genuinely third lecturer (voiceprints agree). The adapter trained on Speaker1 alone also
  improves on Speaker3: **CER 68.4% -> 46.4-46.7%, p < 1e-08, both runs**; significant even
  without the loop safeguard. The thesis claim is now "generalizes to two unseen lecturers".
- Training on Speaker1+3 did not measurably help Speaker2 (one run; the rest was interrupted).
- Open question from the user: add spelling-normalized and fuzzy WER (fairer for Banglish).

## 2026-09-21: step 5 done — the VLM result

- **VLM reading the board: 47.3% -> 97.0%** board-content recall, same model, only the prompt
  changed (p = 0.008). Numbers 0/47 -> 47/47. Reconstructed board adds almost nothing (98.2%).
- **Notes:** 40.1% -> 95.8% with the VLM board text (p = 0.008). The new prompt alone went *down*
  (27.5%); the fine-tuned transcript did not add recall (92.2%).
- **Broken:** the lecturer quotes in `mixed` notes. Needs a prompt fix; ask Claude.
- **Your job now:** verify `data\board_truth\*.json` by hand. Every VLM number rests on it.
- All numbers and commands: RESULTS.md sections 1.0, 5.2, 5.3.

---

## Moving to the 5090 — copy these four things

**DONE 2026-09-21**, except `claude_checkpoint\`, which was not copied. Optional: CLAUDE.md
carries everything needed to work.

Git only carries the code. Copy these from the 3060 as well:

| From the 3060 | Why |
|---|---|
| `F:\thesisP2\thesisP2\output\` | fine-tuned transcripts for all 9 lectures, board mosaics, baseline notes |
| `F:\thesisP2\thesisP2\data\` | videos and ground truth |
| `F:\thesisP2\ft_work\` | the trained adapter, whisper-small, clips |
| `F:\thesisP2\claude_checkpoint\` | Claude's memory; read `RESTORE.md` inside |

Easiest: copy the whole `F:\thesisP2\` folder, but skip `envs\`, because environments don't work
when moved to another machine. If you can, put the repo at the same path, `F:\thesisP2\thesisP2`.
Then the paths and Claude's memory need no changes.

Your first message to Claude on the 5090:

> Repo is at `<path>`. ft_work is at `<path>`. output\ and data\ are copied.
> Read CLAUDE.md and NEXT_STEPS.md, then run scripts/check_environment.py.

---

## Already done. Do not touch these.

- Fine-tune result: WER 96.1% -> 81.8%, p = 0.009, replicated. **This is your thesis.**
- Scaling curve at 0.3 / 0.6 / 1.17 h
- Honest statistics; every fabricated number removed
- Board reconstruction for all 9 lectures, median 97.7% clean
- Board-content recall baseline: 40.1%
- Fine-tuned transcripts for all 9 lectures (`transcript_finetuned.txt` in each lecture folder)
- New note prompts with the language switch: english / banglish / mixed. **Built but not run yet.**
  They need Qwen, so they run on the 5090.
- Everything committed and pushed to GitHub

**If nothing else happens, you can defend with this.**

---

## Do now, before the 5090 (5 minutes, not technical)

**Message your transcribers:**

> Two rules for the new files. Every segment 10-25 seconds, never over 30,
> broken at a natural pause. And one line at the top of each file:
> `# Speaker ID: SPK04` — same ID for the same lecturer across videos.

Without the Speaker ID the speaker-independent split silently breaks, and that
split is what makes the headline result credible. This is the only urgent thing.

---

## When the 5090 is ready (in order, stop when tired)

**Steps 1 and 2 are DONE (2026-09-21).** Only the Qwen weights are left; they download
automatically on the first run of step 5a, to `D:\T2520875\hf_cache`.

**1. Set up the environment.** One env with everything:

- torch for Blackwell: **CUDA 12.8, torch >= 2.7**. The current 2.5.1+cu121 will not run.
- numpy, Pillow, matplotlib, transformers, peft, soundfile, jiwer
- ffmpeg on PATH
- Qwen2.5-VL weights, about 16 GB

**2. Preflight.** `python scripts/check_environment.py`

It checks every package, the GPU, disk, ffmpeg, paths and the data, and prints the
exact command to fix anything missing. Get it to zero failures before going on.

**3. Smoke test.** `python scripts/run_p3_experiment.py --skip curve`

**4. When the 8 hour data lands:**

```
python scripts/run_p3_experiment.py --test-speakers B,SPK04,SPK05 \
    --model openai/whisper-large-v3-turbo --curve-hours 2 4 6 8 --batch 8
```

Keep speaker B in the test set. It keeps the board ground truth valid.

**5. The VLM experiment and the better notes.** Copy-paste in order. Each step
changes one thing, so you can say which change caused which gain.

The fine-tuned transcripts are **already done** (made on the 3060), in each
lecture folder as `transcript_finetuned.txt`. Copy `output\` across and skip
straight to 5a.

5a. The VLM on its own: raw frame vs reconstructed board. **This is the result
your supervisor wants.**

```
python scripts/transcribe_boards.py --all --source frame
python scripts/transcribe_boards.py --all --source mosaic
python scripts/score_board_recall.py --notes-name board_text_frame.md
python scripts/score_board_recall.py --notes-name board_text_mosaic.md
```

5b. The notes, one change at a time. Baseline is 40.1%.

```
python scripts/regenerate_notes.py --all --language mixed --board-source keywords --out-name notes_B_prompt.md
python scripts/regenerate_notes.py --all --language mixed --board-source boards   --out-name notes_C_vlm.md
python scripts/regenerate_notes.py --all --language mixed --board-source boards   --transcript-file transcript_finetuned.txt --out-name notes_D_full.md
```

5c. Score each step against the one before:

```
python scripts/score_board_recall.py --compare-names final_lecture_notes.md notes_B_prompt.md
python scripts/score_board_recall.py --compare-names notes_B_prompt.md notes_C_vlm.md
python scripts/score_board_recall.py --compare-names notes_C_vlm.md notes_D_full.md
```

B tells you what the new prompt alone did. C tells you what the VLM reading the
reconstructed board added. D tells you what the fine-tuned transcript added.

5d. To show your supervisor the language options, run the D command three times
with `--language english`, `--language banglish` and `--language mixed`, and
compare them side by side.

---

## Jobs for your teammates (no coding)

- **Verify the board ground truth** in `data/board_truth/*.json`, about 40 minutes.
  It was drafted by reading images; items marked `"verify": true` were unclear.
  One CGPA is either 3.77 or 3.57 — check the video.
- **Writing.** Chapters 3, 7, 9 are still stubs. `chapter_7.tex` is 0 bytes and
  is not `\input` in main.tex.

---

## If someone asks "what is the thesis"

> Banglish classroom ASR is unsolved. We built the full pipeline and measured
> every branch. Fine-tuning works: 19 points of WER on a speaker the model never
> heard, replicated. Visual fusion does not, and we show why. The metric the
> field uses is anti-correlated with transcription quality, and we show that too.
> We also reconstruct the whiteboard with the lecturer removed, from real pixels
> only.

One positive, three negatives, one methodological finding. That is a thesis.

---

## Where the detail lives

- **[RESULTS.md](RESULTS.md)** — every number, and the command that regenerates it.
  If a number is not there, it does not go in the paper.
- **[CLAUDE.md](CLAUDE.md)** — context for the next Claude session, on any machine.

You do not need to remember any of it. It is written down.
