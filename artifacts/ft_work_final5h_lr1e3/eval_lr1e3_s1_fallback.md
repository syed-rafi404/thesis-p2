# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_final5h_lr1e3\lora_lr1e3_s1`
Split: `test.jsonl`, clips scored: 177

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 19, tuned 2 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.3% | 41.7% |
| WER, per clip mean | 91.1% | 45.8% |
| WER, whole split | 85.6% | 39.2% |
| CER, per clip median | 67.0% | 16.0% |
| CER, per clip mean | 68.5% | 23.4% |
| Term recall | 66.9% | 95.5% |
| Term precision | 83.9% | 91.5% |
| Term F1 | 74.4% | 93.4% |
| Clips that run away | 0 of 177 | 0 of 177 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 171 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 4.24e-43.
- **CER**: fine-tune wins on 169 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 2.23e-40.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=176, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR11/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. eta gailo amal or get completed.
- tuned: eita gelo amar or gate complete.

**BanglaASR11/seg_040.wav**

- reference: so ami eta x-or jehetu amar eta, so eta ekhane apply kore dicchi.
- base: zho no output ashto 0 and different input value zho no output ashto 1. so eta mi xor jehi to aamari eta so eta ekhanen
- tuned: so eita ekhane abar ekta kintu.

**BanglaASR9/seg_011.wav**

- reference: name-er offset koto? name-er offset holo four. and erpore ja ashbe, shetar offset hobe holo four theke plus eight, jodi ekta floating point number hoy. toh etai stack pointer-ta kibhabe kaj kore?
- base: so, what do we do with tag pointer?
- tuned: name-er offset koto? name-er offset holo four. and erpore jaa ashbe setar offset chhbe four theke plus eight, jodi ekta floating point number hoy. toh etai stack point-er-ta kibhabe kaj kore?

**BanglaASR11/seg_000.wav**

- reference: hello everyone, welcome to the second class of digital logic design. so goto class e amra ki dekhechilam? kichu fundamental gates er amra introductory lesson dekhechilam.
- base: hello everyone, welcome to the second class of digital logic design. so what did we have seen in this class? yes, fundamental gates. we have seen the introductory lesson. so, now we have the universal gate. what is the universal gate?
- tuned: hello everyone, welcome to the second class of digital logic design. so goto class e amra ki dekhechilam? kichu fundamental gates er amra introductory lesson dekhechilam. so ajke asbe amra universal gate.

**BanglaASR9/seg_005.wav**

- reference: width ki? eta ekta common question. width holo ashole amra ekta variable ki poriman jayga store kore, toh shetai width. tarpor amra dekhbo holo offset.
- base: so what is the width? this is a common question width is the same variable store so that width so we can see the offset
- tuned: width ki? eta ekta common question. width holo ashole amra ekta variable ki poriman jayga store kore. to setai width. tarpore amra dekhbo holo offset.
