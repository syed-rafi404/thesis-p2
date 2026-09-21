# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 90.2% |
| WER, per clip mean | 112.3% | 136.7% |
| WER, whole split | 89.9% | 113.5% |
| CER, per clip median | 74.2% | 65.1% |
| CER, per clip mean | 85.0% | 101.5% |
| Term recall | 72.6% | 90.0% |
| Term precision | 64.6% | 60.8% |
| Term F1 | 68.3% | 72.6% |
| Clips that run away | 10 of 184 | 39 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 99 of 184 clips. Wilcoxon signed-rank p = 9.19e-01, sign test p = 3.38e-01.
- **CER**: fine-tune wins on 114 of 184 clips. Wilcoxon signed-rank p = 1.47e-01, sign test p = 1.46e-03.

Paired test on the mean per-clip WER, for reference: p = 0.0329 (sign-flip Monte Carlo, n=172, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: toh le eight a hoche amar, x or get ta, and eight a holo amar, output. done. so, x or jodi amra bucche jai, tahole last je exclusive gate, cheite o kinto amake buccha easier hoye chabe.

**BanglaASR7/seg_039.wav**

- reference: different input value er jonno output ashto aa. sorry. diff same input value er jonno output ashto 0 and different input valuer jonno output ashto 1.
- base: so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this
- tuned: okay, so, egzor geite kichilo, amr same input er jonno, mane same input value jonno amr output ashto one, and different input value jonno output ashto, aa sorry, same input value jonno output er jonno output er jonno, amr output ashto, okay.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami ei sign ta diye exor ki bujhacchi mane or mane ki? plus er exclusive or ami ei plus er byre ekta circle diye exclusive or ki bujhacchi. so, ei tar inputs and output ki rakom hobe. so ei tar input and output ta bare kora ektu hoore length e process.

**BanglaASR7/seg_009.wav**

- reference: or kortesi. erpor ami otar upore not kore ami final nor gate ta peye jacchi. so 0 plus 0 ki hobe? 0. 0 plus 1, 1. 1 plus 0, 1. 1 plus 1, 1.
- base: so, now first i will do what? i will do more. then i will note down the final nor gate. so, 0 plus 0, what will happen? 0, 0 plus 1, 1, 1 plus 0, 1, 0 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0,
- tuned: so ekhon first ami ki kortechi? or kortechi, erpor ami utar opore not kore, ami final nor gate ta prejachi. so, zero plus zero ki hobe?

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ekta age amra jeta bollam, computer shudhu ki ni e kaaj kore? zero and one. so, a are b er, zero are one er combination diye ki ki, ah inputs possible. ekta hoyte pare zero, zero, ekta hoyte pare zero, one.
