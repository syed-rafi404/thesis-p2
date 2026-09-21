# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 95.1% |
| WER, per clip mean | 112.3% | 172.5% |
| WER, whole split | 89.9% | 136.4% |
| CER, per clip median | 74.2% | 71.5% |
| CER, per clip mean | 85.0% | 129.2% |
| Term recall | 72.6% | 86.8% |
| Term precision | 64.6% | 46.1% |
| Term F1 | 68.3% | 60.2% |
| Clips that run away | 10 of 184 | 58 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 94 of 184 clips. Wilcoxon signed-rank p = 8.71e-03, sign test p = 8.25e-01.
- **CER**: fine-tune wins on 96 of 184 clips. Wilcoxon signed-rank p = 2.89e-02, sign test p = 6.06e-01.

Paired test on the mean per-clip WER, for reference: p = 0.0001 (sign-flip Monte Carlo, n=182, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: toh le ei ta hoche amar x or get ta, and ei ta holo amar output. done. so, x or jodi amra bujhe jain, tahole last je exclusive gate, chei ta o kinto amate bujha easier hoye chabe.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami ei sign ta diye exor ki bujhacchi mane or mane ki plus er exclusive or ami ei plus er byre ekta circle diye exclusive or ki bujhacchi. so, eight er input and output ki rakom hobe? so eight er input and output ta beer kora eittoh lengthy process.

**BanglaASR7/seg_009.wav**

- reference: or kortesi. erpor ami otar upore not kore ami final nor gate ta peye jacchi. so 0 plus 0 ki hobe? 0. 0 plus 1, 1. 1 plus 0, 1. 1 plus 1, 1.
- base: so, now first i will do what? i will do more. then i will note down the final nor gate. so, 0 plus 0, what will happen? 0, 0 plus 1, 1, 1 plus 0, 1, 0 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0, 1 plus 0,
- tuned: so, ekhon first ami ki kortesi? or kortesi, erpor ami utaropore not kore, final nor gate ta pe racchi. so, zero plus zero hi hobe.

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ekta age amra jeta bollam, computer shudhu ki ki nia kaaj kore? zero and one. so a are b er, zero er one er combination diye ki ki ah, inputs possible? ekta hoyte pare zero, zero, ekta hoyte pare zero, one.

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: tahole ami simply jodi ei function ta use kore fili, tahole amake ei paks ta c g p a k a plus kore je dalota hobe, se ta amake return korbe, jemon 3.55 plus 3.7 plus 3.28 plus 3.5 ta hbe rata hobe.
