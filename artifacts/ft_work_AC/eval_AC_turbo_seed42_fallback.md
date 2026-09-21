# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_turbo_AC_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 14, tuned 12 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 91.8% | 72.1% |
| WER, per clip mean | 96.1% | 77.6% |
| WER, whole split | 81.4% | 52.3% |
| CER, per clip median | 68.9% | 48.3% |
| CER, per clip mean | 69.2% | 55.7% |
| Term recall | 81.5% | 93.6% |
| Term precision | 83.9% | 91.0% |
| Term F1 | 82.7% | 92.3% |
| Clips that run away | 3 of 184 | 2 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 137 of 184 clips. Wilcoxon signed-rank p = 2.22e-15, sign test p = 2.11e-11.
- **CER**: fine-tune wins on 129 of 184 clips. Wilcoxon signed-rank p = 3.34e-13, sign test p = 4.92e-08.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=167, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR6/seg_046.wav**

- reference: so eigula gelo amar kichu fundamental gates.
- base: not way, i can put b hochi. so, a gula gello amal itch fundamental gates.
- tuned: so ei gula gelo amar kichu fundamental gain.

**BanglaASR7/seg_040.wav**

- reference: so ami eta x-or jehetu amar eta, so eta ekhane apply kore dicchi.
- base: zho no output ashto 0 and different input value zho no output ashto 1. so eta mi xor jehi to aamari eta so eta ekhanen
- tuned: so eta ami xor jehito amar eta, so eta ekhane apply kache.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a direct input is b. what is the output? first step, we will do the end. the end means multiplication. so, a into b. what do we do? not. so, a, b is a whole
- tuned: ta hole output ki hobe? amake first a end korte hobe. end wani ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab erupore ekta whole button.

**BanglaASR6/seg_033.wav**

- reference: tar mane, amar duita input thakbe ekta output thakbe, duitar multiplication input er multiplication hoye ami output ta pabo. ekta jodi zero thake jekono output er jekono input er moddhe tahole kintu ami zero as an output peye jabo.
- base: so, this is our and gate. that means, our due to input and output has the output. due to input and multiplication, i will output. act is 0 in the same way. that is the output. now, i will show the next fundamental gate.
- tuned: toh cholo, etai hocche amar end gate. tar mane amar duita input thakbe, ekta output thakbe, duitar multiplication, input er multiplication hoy ami output ta pabo. ekta jodi zero thake jekono output er, jekono input er moddhe tahole kintu ami zero as a output peye jabo.

**BanglaASR9/seg_001.wav**

- reference: so select ki kore? select hocche shudhumatro data amar database er je table shekhan theke data retrieve kore. retrieve kore bolte? jemon dhoro ami student id 401201, ei student id-r full name ba first name, last name dekhte chacci.
- base: so select key, select ho c h e, s u dhu m a t r o d e t a b eze j e table, check a n t e k e data k e retrieve kore. retreat kore b olt e, jamon dharo, a me student id 401201. a student id, full name, first name,
- tuned: so select ki kore? select hocche shudhu matro data er database er je table, seikan theke data ke retrieve kore. retweet kore bolte, jemon dhoro ami student id 401201.
