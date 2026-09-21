# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 14, tuned 31 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 91.8% | 79.2% |
| WER, per clip mean | 96.1% | 86.8% |
| WER, whole split | 81.4% | 62.7% |
| CER, per clip median | 68.9% | 58.2% |
| CER, per clip mean | 69.2% | 61.8% |
| Term recall | 81.5% | 89.7% |
| Term precision | 83.9% | 85.1% |
| Term F1 | 82.7% | 87.3% |
| Clips that run away | 3 of 184 | 4 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 123 of 184 clips. Wilcoxon signed-rank p = 5.15e-10, sign test p = 5.69e-06.
- **CER**: fine-tune wins on 119 of 184 clips. Wilcoxon signed-rank p = 3.81e-08, sign test p = 8.38e-05.

Paired test on the mean per-clip WER, for reference: p = 0.0206 (sign-flip Monte Carlo, n=170, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR6/seg_046.wav**

- reference: so eigula gelo amar kichu fundamental gates.
- base: not way, i can put b hochi. so, a gula gello amal itch fundamental gates.
- tuned: so ei gula gelo amar kichu fundamental ke.

**BanglaASR7/seg_040.wav**

- reference: so ami eta x-or jehetu amar eta, so eta ekhane apply kore dicchi.
- base: zho no output ashto 0 and different input value zho no output ashto 1. so eta mi xor jehi to aamari eta so eta ekhanen
- tuned: so eta ami inshor jehito amr eta, so eta ekhane apre kacheche.

**BanglaASR6/seg_039.wav**

- reference: so, erokom bhabe additon er maddhome or er gate ta kaj korche.
- base: 1 equals to 1. so, this is the addition of the math and math.
- tuned: so, erokom bhabe addition er maddhome or er ger ta hbe holo.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a direct input is b. what is the output? first step, we will do the end. the end means multiplication. so, a into b. what do we do? not. so, a, b is a whole
- tuned: taole output ki hobe? amake first a end korte hobe. end wane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so a b erupore ekta whole button korte hobe.

**BanglaASR9/seg_031.wav**

- reference: sheirokom bhabe ami jodi cgpa er e suppose minimum ta dekhte chai minimum cgpa tahole ami eikhane min of cgpa diye dilam. tahole ki hobe? ei 5 ta cgpa er moddhe shob theke lowest jeita which is 3.28 eita amake show kore dibe.
- base: so
- tuned: sero kum bhabe ami jodi cgpa e suppose minimum ta dekhte je, minimum cgpa. tahole ami ekhane min of gpa diye dilam. tahole ki hobe? ei pachra cgpa moddhe sob theke lowest eta which is 3.28, eta amake show kore dibe.
