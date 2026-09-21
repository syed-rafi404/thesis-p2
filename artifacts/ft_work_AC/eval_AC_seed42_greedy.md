# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_AC_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 90.3% |
| WER, per clip mean | 112.3% | 207.1% |
| WER, whole split | 89.9% | 140.6% |
| CER, per clip median | 74.2% | 64.6% |
| CER, per clip mean | 85.0% | 170.7% |
| Term recall | 72.6% | 93.2% |
| Term precision | 64.6% | 43.6% |
| Term F1 | 68.3% | 59.4% |
| Clips that run away | 10 of 184 | 51 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 96 of 184 clips. Wilcoxon signed-rank p = 2.01e-01, sign test p = 6.06e-01.
- **CER**: fine-tune wins on 108 of 184 clips. Wilcoxon signed-rank p = 5.40e-01, sign test p = 2.20e-02.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=175, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: toh hol ei ta hocche amar x or gate ta and ei ta holo amar output. done. so, x or jodi amra bujhe jai, tahole last je exclusive gate, cheta o kintu amader bujha easier hoye chabe.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami ei sign ta diye exor ki bujhacchi mane, or mane ki, plus, ar exclusive or ami ei plus er bire ekta circle diye exclusive or ki bujhacchi. so, eta er input and output ki rakom hobe? so eta input and output ta ber kora ektu lengthy process.

**BanglaASR7/seg_009.wav**

- reference: or kortesi. erpor ami otar upore not kore ami final nor gate ta peye jacchi. so 0 plus 0 ki hobe? 0. 0 plus 1, 1. 1 plus 0, 1. 1 plus 1, 1.
- base: so, now first i will do what? i will do more. then i will note down the final nor gate. so, 0 plus 0, what will happen? 0, 0 plus 1, 1, 1 plus 0, 1, 0 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0,
- tuned: toh ekhon first ami ki kortesi? or kortesi. erpor ami oitar o pore note kore, final naar gate ta pejacchi. so, zero plus zero ki hobe? zero, zero plus one, one, one plus zero, one and one plus one.

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ektu age amra jeta bolam, computer shudhu ki ki niye kaaj kore? zero and one. so a r b l, zero and one er combination diye ki ki aa inputs possible? areta hoyte pare zero, zero. areta hoyte pare zero, one.

**BanglaASR7/seg_039.wav**

- reference: different input value er jonno output ashto aa. sorry. diff same input value er jonno output ashto 0 and different input valuer jonno output ashto 1.
- base: so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this as input value. so, i am going to write this
- tuned: okay. so, exorgeite kichilo, amr same input er jonno, mane same input value jonno amr output ashto one. and different input value jonno output ashto, aa sorry, same input value jonno amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto, amr output ashto,
