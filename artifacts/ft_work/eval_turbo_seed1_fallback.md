# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 14, tuned 28 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 91.8% | 85.7% |
| WER, per clip mean | 96.1% | 89.6% |
| WER, whole split | 81.4% | 66.7% |
| CER, per clip median | 68.9% | 61.0% |
| CER, per clip mean | 69.2% | 63.1% |
| Term recall | 81.5% | 88.6% |
| Term precision | 83.9% | 83.8% |
| Term F1 | 82.7% | 86.2% |
| Clips that run away | 3 of 184 | 5 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 107 of 184 clips. Wilcoxon signed-rank p = 3.38e-05, sign test p = 3.22e-02.
- **CER**: fine-tune wins on 109 of 184 clips. Wilcoxon signed-rank p = 8.65e-05, sign test p = 1.48e-02.

Paired test on the mean per-clip WER, for reference: p = 0.0217 (sign-flip Monte Carlo, n=172, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_040.wav**

- reference: so ami eta x-or jehetu amar eta, so eta ekhane apply kore dicchi.
- base: zho no output ashto 0 and different input value zho no output ashto 1. so eta mi xor jehi to aamari eta so eta ekhanen
- tuned: so, eta ami x or je hito amar eta, so eta ekhane apre ekhane ekhane.

**BanglaASR6/seg_033.wav**

- reference: tar mane, amar duita input thakbe ekta output thakbe, duitar multiplication input er multiplication hoye ami output ta pabo. ekta jodi zero thake jekono output er jekono input er moddhe tahole kintu ami zero as an output peye jabo.
- base: so, this is our and gate. that means, our due to input and output has the output. due to input and multiplication, i will output. act is 0 in the same way. that is the output. now, i will show the next fundamental gate.
- tuned: tarmane amr duita input thakbe, ekta output thakbe, duitar input er multiplication hoy ami output ta pabo, ekta jodi zero thake jekono output er moddhe, tahole kintu ami zero as a output peye jabo.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a direct input is b. what is the output? first step, we will do the end. the end means multiplication. so, a into b. what do we do? not. so, a, b is a whole
- tuned: taole output ki hobe? amake first a and korte hobe. and korte hbe? and korte chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so a, b erupore ekta whole barter korte hobe.

**BanglaASR9/seg_001.wav**

- reference: so select ki kore? select hocche shudhumatro data amar database er je table shekhan theke data retrieve kore. retrieve kore bolte? jemon dhoro ami student id 401201, ei student id-r full name ba first name, last name dekhte chacci.
- base: so select key, select ho c h e, s u dhu m a t r o d e t a b eze j e table, check a n t e k e data k e retrieve kore. retreat kore b olt e, jamon dharo, a me student id 401201. a student id, full name, first name,
- tuned: so, select ki kore? select hocche, shudhu maktro data er, amr database er je table, se ekan theke data ke retrieve kore. retrieve kore bolte, jemon dhoro ami student id 401201, ei student id er full name ba, first name er ekta command kore hbe.

**BanglaASR9/seg_010.wav**

- reference: so ei sql command ta jodi ami run kori tahole amake output hishebe ki dibe? first ei o search dekhbe je amake ki dekhate hobe? amake dekhate hobe cgpa?
- base: done. so, one sql comment which i ran, is that i will show you what you want to do. first, i will show you what you see. so, see cgpa. so, see student info.
- tuned: done! so, ei sql command a jodi ami ran kori, tahole amake output hishebe ki dibe? first a o search dekhbe je amake ki be dekhate hobe? ki be dekhate hobe? amake dekhate hobe cgp a.
