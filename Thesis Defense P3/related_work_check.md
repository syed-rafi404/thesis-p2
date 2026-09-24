# Related work: what already exists near this thesis (checked 2026-09-24)

Written because the claim "ours is the only Banglish ASR" came up. It is **not safe as stated**.
A web search found systems close enough that a panel member would find them in a minute. Read this
before writing the related-work chapter or any "first of its kind" sentence.

## The neighbours

| Work | What it is | How close |
|---|---|---|
| [`the-blue-panther/whisper-small-benglish`](https://huggingface.co/the-blue-panther/whisper-small-benglish) | Whisper-small fine-tuned for Bengali-English code-switched audio | **Closest.** The name alone appears in any "Benglish ASR" search. Check what orthography it outputs |
| [Asrarul-BS23/whisper-finetuning](https://github.com/Asrarul-BS23/whisper-finetuning) | whisper-large-v3 + LoRA on Bengali-English code-switched speech, for meetings | Same model, same method, different domain |
| [MediBeng Whisper Tiny](https://www.medrxiv.org/content/10.1101/2025.04.25.25326406v3.full) | Fine-tuned code-switched Bengali-English for clinical use | **Translates to English** rather than transcribing, so a different task; reports WER 0.01 and BLEU 0.98, which suggests synthetic or very easy data - worth reading before citing |
| [WILDRE 2026 code-mixed speech data](https://aclanthology.org/2026.wildre-1.5/) | Bengali-English and Hindi-English code-mixed speech with disfluencies | A dataset paper in the same space |
| [Code-switched ASR for Indic languages](https://arxiv.org/pdf/2203.16578) | Broader Indic code-switching ASR | Background, plus the transliterated-WER idea, which is relevant to our metric finding |
| Bengali long-form ASR and diarization papers (arXiv 2603.03158, 2605.08214, 2603.04809) | Bengali ASR, Bengali script output | Adjacent, not code-mixed romanised |

## What is still defensible, if each is verified

1. **The output orthography** - romanised Banglish as the transcription target, not Bengali script and
   not an English translation. This is the real distinction; confirm what `whisper-small-benglish`
   emits before leaning on it.
2. **The domain** - university lectures with the whiteboard read alongside the speech. Nothing found
   combines both.
3. **The pipeline** - video in, lecture notes out that point at numbered regions of a reconstructed
   board.
4. **The evaluation finding** - measures built from English strings penalise faithful code-mixed
   transcription (RESULTS 5.4 and section 3). The transliterated-WER idea in the Indic paper above is
   the nearest relative and should be cited.
5. **Method rigour** - hand-verified ground truth, speaker-independent testing, pre-registered
   tuning, negatives reported. Most neighbours have none of this.

## Two things to do before the defense

- **Soften every "first" sentence** to something precise and checkable. "To our knowledge the first
  X" is the sentence a panel goes hunting for.
- **Benchmark at least one neighbour.** Running `whisper-small-benglish` on our test clips costs
  about 20 minutes on any GPU and turns "we were not aware of it" into a row in a table. If no GPU is
  available before the defense, say in the limitations that the comparison is outstanding.
