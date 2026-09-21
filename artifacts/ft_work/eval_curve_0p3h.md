# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\curve\adapter_0p3h`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 94.0% |
| WER, per clip mean | 112.3% | 178.2% |
| WER, whole split | 89.9% | 144.1% |
| CER, per clip median | 74.2% | 74.3% |
| CER, per clip mean | 85.0% | 134.2% |
| Term recall | 72.6% | 83.3% |
| Term precision | 64.6% | 58.5% |
| Term F1 | 68.3% | 68.7% |
| Clips that run away | 10 of 184 | 65 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 85 of 184 clips. Wilcoxon signed-rank p = 9.16e-04, sign test p = 1.00e+00.
- **CER**: fine-tune wins on 97 of 184 clips. Wilcoxon signed-rank p = 5.76e-03, sign test p = 5.07e-01.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=175, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: tohole ei ta hojhe amar, x or get ta, and ei ta holo amar, output. done. so, x or jodi amra buche jain, tahole last je exclusive get, sheta o kinto amr te buche hoye chabe.

**BanglaASR7/seg_039.wav**

- reference: different input value er jonno output ashto aa. sorry. diff same input value er jonno output ashto 0 and different input valuer jonno output ashto 1.
- base: so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this
- tuned: okay, so, exor gete kichiro, amar same input er jono, mane same input value jono amar output ashto one. and different input value jono output ashto, aa sorry, the same input value jono amr output ashto one.

**BanglaASR7/seg_009.wav**

- reference: or kortesi. erpor ami otar upore not kore ami final nor gate ta peye jacchi. so 0 plus 0 ki hobe? 0. 0 plus 1, 1. 1 plus 0, 1. 1 plus 1, 1.
- base: so, now first i will do what? i will do more. then i will note down the final nor gate. so, 0 plus 0, what will happen? 0, 0 plus 1, 1, 1 plus 0, 1, 0 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0,
- tuned: so, ekhon first ami ki korte si? or korte si? erpore ami utoropore not kore ami, final nor getta pejacchi. so, zero plus zero hi hobe.

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ektu age amra jeta bollam, computer shudhu ki ki nia kaj kore? zero and one. so, a are b er, zero are one er combination diye ki ki, aa inputs possible? ekta hoyte pare zero, zero, ekta hoyte pare zero, one.

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: ta amake return korbe, jamo 3.55 plus 3.77 plus 3.28 plus 3.25.
