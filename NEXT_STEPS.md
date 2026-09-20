# NEXT STEPS — read this file, ignore everything else

If you are lost, start here. One page. Updated 2026-09-21.

---

## Already done. Do not touch these.

- Fine-tune result: WER 96.1% -> 81.8%, p = 0.009, replicated. **This is your thesis.**
- Scaling curve at 0.3 / 0.6 / 1.17 h
- Honest statistics; every fabricated number removed
- Board reconstruction for all 9 lectures, median 97.7% clean
- Board-content recall baseline: 40.1%
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

**1. Set up the environment.** One env with everything:

- torch for Blackwell: **CUDA 12.8, torch >= 2.7**. The current 2.5.1+cu121 will not run.
- numpy, Pillow, matplotlib, transformers, peft, soundfile, jiwer
- ffmpeg on PATH
- Qwen2.5-VL weights, about 16 GB

**2. Smoke test.** `python scripts/run_p3_experiment.py --skip curve`

**3. When the 8 hour data lands:**

```
python scripts/run_p3_experiment.py --test-speakers B,SPK04,SPK05 \
    --model openai/whisper-large-v3-turbo --curve-hours 2 4 6 8 --batch 8
```

Keep speaker B in the test set. It keeps the board ground truth valid.

**4. The VLM experiment** (only if 1-3 are done and there is time):
regenerate notes with the fine-tuned model and the reconstructed boards, then

```
python scripts/score_board_recall.py --compare <old_run_dir> <new_run_dir>
```

Baseline to beat: **40.1%**.

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
