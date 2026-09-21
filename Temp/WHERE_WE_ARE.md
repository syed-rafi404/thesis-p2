# Where we are — one page

## The idea has not changed

A lecture video goes in; lecture notes come out. Three stages: **hear** the lecturer,
**read** the whiteboard, **write** the notes.

## P2 — what you built

```
video -> audio -> Whisper (English translation) + BanglaASR (Bengali script)
      -> fused with keywords the VLM spotted on the board
      -> Qwen writes notes
Measured with Term F1 = 73.9%
```

## What P3 found when we tested each piece honestly

- **Fusing vision into speech did not help** (+0.7 points, not significant). Kept as a negative result.
- **Term F1 was a broken ruler.** It rewards English words, so better Banglish scored worse,
  and it swung 8 points between identical runs. Replaced by CER/WER for speech and
  board-content recall for notes.
- So instead of fusing, we made each stage good on its own.

## The pipeline now

```
lecture video
 |-- audio -----------> Whisper large-v3-turbo + our LoRA adapter
 |                      (trained on your Banglish transcripts)   -> Banglish transcript
 |-- a frame every 10 s -> Qwen2.5-VL, "transcribe the whole board" -> board text
 |        (optional)  -> board reconstruction: lecturer-free board pictures for the notes
 '-- transcript + board text -> Qwen2.5-7B, grounded prompt -> lecture notes + board pictures
```

What changed from P2: speech is **fine-tuned** (was off the shelf), the board is **fully
transcribed** (was keywords), **no fusion step**, and the notes prompt says "use what this
lecturer said and wrote" (was "explain each concept", which made Qwen recite a textbook).

Today these stages are separate scripts run one after another; they can be joined into one
command for the final system.

## What it achieves (measured; every number is in RESULTS.md)

| Stage | Before | Now |
|---|---|---|
| Speech: character error on a lecturer never heard in training | 72.8% | **50.3%** |
| Board reading: share of board content recovered, 35 hand-checked boards | 31.2% | **88.8%** |
| Notes: share of board content that reaches the notes, 35 boards | 37.2% | **88.0%** |

## The thesis in one sentence

Reading the board with a vision-language model, plus a little targeted speech data, makes
code-mixed classroom content recoverable; fusing vision into speech recognition does not.

## When the 10 hours arrive

- **The story does not change.** The same experiments run again with more data behind them.
- Transcribers: segments of 10-25 seconds, and `# Speaker ID:` at the top of every file.
- On the 5090: validate the transcripts, then re-train and re-evaluate with each lecturer held
  out once. About an hour of GPU time.
- Honest expectation: more **lecturers** should help (two training lecturers beat one); more
  hours from the **same** lecturer helped little. We will know when it runs.

## The only things left

1. ~~Check the board answer keys~~ Done 2026-09-22, all 45 boards.
2. Put the RESULTS.md numbers into the chapters (fine-tune: section 1.5; board and notes: section 5.0).
3. Re-run everything when the 10 hours are ready.
