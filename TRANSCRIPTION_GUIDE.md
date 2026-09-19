# Banglish Lecture Transcription Guide

**For the transcription team.** Read Sections 1–4 before your first file. Sections 5–8 are lookup.

This produces training data for a speech-recognition model. The model copies exactly what you
write — including your mistakes. Consistency between transcribers matters more than any individual
transcriber's judgment. When this guide conflicts with your instinct, **follow the guide**.

Version 1.0 · 2026-08-05

---

## 1. The single most important rule

> **Keep every segment under 30 seconds.**

The model can only ever see 30 seconds of audio at once. Anything longer gets cut by software that
does not know where sentences end, which produces audio that does not match its text — the worst
kind of training data.

The existing 9 files did not follow this rule. Their segments run a median of **79 seconds**, up to
**225 seconds**, and **98% are over 30s**. Those files now need repair. **Do not copy that pattern.**

**Target: 10–25 seconds per segment. Hard ceiling: 30.**

Always break at a natural pause — end of sentence, or where the lecturer takes a breath. Never break
mid-word or mid-phrase.

```
GOOD                                      BAD
[0:00-0:18]  one idea, ends at a pause    [0:00-1:27]  eight sentences jammed together
[0:18-0:35]  next idea                    [1:27-2:19]  five more
[0:35-0:52]  next idea
```

---

## 2. Output format

One `.txt` file per video, UTF-8, named `BanglaASR<N>_ground_truth.txt`.

```
# BanglaASR12 Ground Truth Transcription
# Topic: Python Functions
# Speaker ID: SPK03
# Video duration: 14:22
# Transcriber: RH
# Date: 2026-08-12
# Style guide version: 1.0

# ============================================================================

[0:00-0:16] Assalamualaikum shobai. Aj amra dekhbo je kivabe python e function likhte hoy.
[0:16-0:33] Function mane hocche ekta code block jeta amra baar baar call korte pari.
[0:33-0:51] Toh amra jodi likhi def, tarpore function er name, ei je greet.
```

Rules for the format:

- Timestamp is exactly `[M:SS-M:SS]`. **No space anywhere inside the brackets.**
  Write `[2:19-2:48]`. Not `[2:19- 2:48]`, not `[01:55 - 03:16]`.
- Each segment starts on a **new line**, timestamp first, then one space, then the text.
- Every `#` line is ignored by the software. Use `#` for notes to yourself or the team.
- End timestamp of one segment = start timestamp of the next. No gaps, no overlaps.

**Speaker ID matters.** We need to test on speakers the model never trained on, so every file must
say who is speaking. If you do not know, write `SPK_UNKNOWN` and flag it.

---

## 3. Write it exactly as spoken

This is the part that differs most from what you may expect.

### 3.1 Keep the fillers

Write `um`, `uh`, `aaa`, `ahm`, `mane`, `je`, `tahole`, `okay`, `thik ache` — every one of them,
every time.

You may have noticed that ChatGPT's and Perplexity's voice input silently drop these. **Those are
consumer products optimizing for a clean-looking result. We are building a research system, and our
goal is the opposite: accuracy against what was actually said.**

Three concrete reasons:

1. **The model needs to learn them.** Fillers are roughly 5% of real lecture speech (measured on the
   existing files: 671 filler tokens out of 12,890). If they never appear in training text, the
   model has no idea what to do when it hears one, and will usually hallucinate a real word in its
   place.
2. **Removing them corrupts the timing.** Your text must match the audio in that time window. If the
   lecturer says "um" for a full second and you delete it, the text no longer lines up.
3. **It makes our error rate a lie.** If our reference text is cleaner than reality, every score we
   publish is wrong in our favour. That is the kind of thing that gets caught at defense.

Cleaning up is a separate, automated, later step. It is not your job, and doing it by hand destroys
information we cannot recover.

```
Lecturer says:  "So ekhane, aaa, amra ekta variable nibo, um, jeta hocche num."
WRITE:          So ekhane, aaa, amra ekta variable nibo, um, jeta hocche num.
NOT:            So ekhane amra ekta variable nibo jeta hocche num.
```

### 3.2 The one thing you do remove: abandoned restarts

If the lecturer starts a sentence, stops, and starts over completely differently, keep only the
version they finished.

```
Heard:  "Ami likhbo— na na, ami age screen e dekhai."
WRITE:  Na na, ami age screen e dekhai.
```

If you are unsure whether it is a restart or a filler, **keep it**. Keeping too much is a small
problem; deleting real speech is a big one.

### 3.3 Never fix the lecturer

Transcribe errors, slips and repeats exactly as they happen.

```
Heard:  "Ei function ta, ei function ta return kore ekta value."
WRITE:  Ei function ta, ei function ta return kore ekta value.   (repeat is real — keep it)

Heard:  "Python e amra list use kori... sorry, tuple use kori."
WRITE:  Python e amra list use kori, sorry, tuple use kori.       (do not silently correct)
```

---

## 4. Spelling: one word, one spelling

This is where transcribers disagree most, and where disagreement does the most damage. If you write
`kore` and someone else writes `koree` for the same word, the model sees two unrelated words and
learns both badly.

**These rulings are final. Do not improvise.**

The list below was derived from what the team already wrote most often across the 9 completed files,
so it should mostly match your instincts.

### 4.1 Core word list — memorise these

| Meaning | **USE THIS** | Do NOT write |
|---|---|---|
| I / my | `ami` / `amar` | amr, aami |
| we | `amra` | aamra, amraa |
| this | `eta` / `ei` | etaa, eee |
| that | `sheta` | seta, shetaa |
| one / a | `ekta` | ektaa, akta, ekhta |
| two | `duita` | duta, duito |
| here | `ekhane` | ekhaane, ekane |
| now | `ekhon` | ekhone, akhon |
| does / doing | `kore` | koree, koore, kore |
| I do | `kori` | koree |
| will do | `korbo` | korobo |
| to do | `korte` | korate |
| is happening | `hocche` | hoche, hochhe, hoicche |
| becomes / will be | `hoy` / `hobe` | hoye (unless truly "hoye"), hobey |
| is / exists | `ache` | achhe, ase |
| if | `jodi` | zodi |
| but | `kintu` | kintuh |
| then / so | `tahole` | tahle |
| after that | `tarpore` | tarpor |
| inside | `moddhe` | modhye, majhe |
| from | `theke` | theka |
| plural marker | `gula` | gulo |
| thing | `jinish` | jinis |
| good | `bhalo` | valo, bhaalo |
| for (purpose) | `jonno` | jonne, jonyo |
| and | `ebong` / `ar` | ebong is preferred in writing |
| no / not | `na` | naa |
| take it as | `dhoro` | dhori (unless "I take") |
| like / such as | `jemon` | jemne |
| can | `pari` | paari |

Note `gula` and `tarpore` above: those are the majority spellings in the existing files, even though
`gulo` and `tarpor` may look more standard to you. We are matching the existing data.

### 4.2 English technical words stay English

Write the English spelling, even though it is pronounced with a Bengali accent.

```
WRITE:  variable, function, parameter, argument, class, object, database,
        table, query, loop, array, string, integer, boolean, compile
NOT:    bhariabel, fangshan, tebil, luup
```

### 4.3 Bengali endings on English words — separate with a space

```
WRITE:  function ta, class er, variable gula, parameter ke, database e
NOT:    functionta, classer, variablegula
```

### 4.4 Code and identifiers stay verbatim

If the lecturer says a name that appears on screen, spell it the way it appears on screen —
capitalisation included.

```
WRITE:  So ekhane ami userName variable ta nilam.
WRITE:  Amra print() function call korbo.
```

### 4.5 Numbers

Write digits for numeric values, words when part of a Bengali phrase.

```
WRITE:  ekhane 5 ta data ache
WRITE:  duita column ache
WRITE:  student ID hocche 101
```

---

## 5. ASCII only — no smart quotes

The file must contain plain ASCII characters only.

Word and Google Docs silently convert `"` into `"` `"` and `'` into `'`. Those characters get
mangled by our software. The existing files already contain **73 damaged characters** because of
this, and each one is a corrupted training example.

**Type directly in a plain-text editor: Notepad, VS Code, or Notepad++.**
If you must draft in Word, turn off AutoCorrect → "Smart quotes" first.

```
WRITE:  So ekhane amra "What is a variable" ei question ta dekhbo.
NOT:    So ekhane amra "What is a variable" ei question ta dekhbo.
```

Never paste Bengali script (`আমরা`). Everything is romanized, always.

---

## 6. Special situations

| Situation | What to write |
|---|---|
| Student asks something audible | `[4:10-4:19] Student: Sir, parameter ki optional?` |
| Lecturer answers | `[4:19-4:31] Hae, python e default value dite pari.` |
| Cannot hear a word | `[unclear]` — e.g. `ekhane amra [unclear] use korbo` |
| Cannot hear a long stretch | `[inaudible 0:12]` and note the length |
| Laughter, if meaningful | `(laughs)` |
| Long silence over 5s | `[pause]` |
| Background noise drowns speech | `[noise]` |
| English sentence spoken fully | Write it normally — code-switching is expected and normal |

Use `[unclear]` freely. A guess that is wrong is worse than an honest `[unclear]`, because the model
will learn the wrong word. Nobody is judged on how few unclears they have.

---

## 7. Your workflow

1. Open the video and a plain-text editor side by side.
2. Fill in the header, including **Speaker ID**.
3. Play 10–25 seconds. Pause.
4. Write the timestamp, then exactly what you heard — fillers included.
5. Replay that same window once to check the text matches the audio.
6. Continue. Each segment starts where the previous one ended.
7. When finished, run the self-check in Section 8.

Expect roughly **5–8 minutes of work per 1 minute of video**. A 15-minute lecture is around 1.5–2
hours. This is normal — do not rush it, and take breaks, because accuracy drops sharply when tired.

Save often. Save as UTF-8.

---

## 8. Self-check before you submit

Go through every line:

- [ ] Every segment is **under 30 seconds**
- [ ] Every timestamp reads `[M:SS-M:SS]` with **no spaces inside the brackets**
- [ ] End time of each segment equals the start time of the next — no gaps, no overlaps
- [ ] Fillers (`um`, `aaa`, `mane`, `je`, `tahole`) are **present**, not cleaned out
- [ ] Spellings follow the Section 4.1 table
- [ ] English technical terms are spelled in English
- [ ] Bengali endings are separated by a space (`function ta`, not `functionta`)
- [ ] No smart quotes, no Bengali script, no emoji — ASCII only
- [ ] Header is filled in, including Speaker ID
- [ ] File is UTF-8, named `BanglaASR<N>_ground_truth.txt`

Then spot-check: pick 3 random segments, play that exact time range, and confirm the text matches
word for word. If any one fails, check the whole file.

---

## 9. Full worked example

```
# BanglaASR12 Ground Truth Transcription
# Topic: Python Functions
# Speaker ID: SPK03
# Video duration: 03:04
# Transcriber: RH
# Date: 2026-08-12
# Style guide version: 1.0

# ============================================================================

[0:00-0:14] Assalamualaikum shobai. Aj amra dekhbo je kivabe python e function likhte hoy.
[0:14-0:31] Toh function mane hocche, aaa, ekta code block jeta amra baar baar call korte pari.
[0:31-0:49] Dekho, amra jodi ekta kaj barbar korte chai, tahole prottek bar oi code ta likhbo na.
[0:49-1:05] Amra ekbar function banabo, tarpore shudhu call korbo. Thik ache?
[1:05-1:23] Python e function define korte amra def keyword use kori. Def mane define.
[1:23-1:41] Tarpore function er name, jemon ekhane ami likhchi greet, tar por bracket ar colon.
[1:41-1:58] So ekhane ami likhlam def greet name, ei je name ta holo amar parameter.
[1:58-2:16] Ekhon, um, parameter ar argument er difference ta bujhte hobe.
[2:16-2:34] Parameter hocche jeta ami define korar shomoy likhi, ei je name.
[2:34-2:52] Ar argument hocche jeta ami call korar shomoy pathai, jemon greet Alice.
[2:52-3:04] Tahole output e ashbe Hello Alice. Bujhte parcho shobai?
```

Notice in the example:

- Every segment is 12–18 seconds — well under the limit
- `aaa` at 0:14 and `um` at 1:58 are kept
- `thik ache` at 0:49 is kept
- `function`, `parameter`, `argument`, `def` are English
- `function er`, `name ta` use a space before the ending
- Spellings match Section 4.1 throughout

---

## 10. Questions and disagreements

If you hit a word that is not in Section 4.1 and you are unsure of the spelling:

1. Write your best guess **and** flag it with a `#` comment on the line below.
2. Post it in the team channel.
3. Once we agree, it gets added to Section 4.1 and this version number goes up.

```
[3:12-3:28] Ekhane amra recursion use korbo.
# QUERY: heard something like "rikarshon" - spelled it as English "recursion", confirm?
```

**Do not quietly invent a spelling.** One person's private convention, repeated across 3 hours of
audio, is a large amount of corrupted training data — and it is very hard to find afterwards.

---

*Guide version 1.0 — spellings derived from the 9 completed transcripts. Report problems to the*
*thesis team; this document is expected to change as new words come up.*
