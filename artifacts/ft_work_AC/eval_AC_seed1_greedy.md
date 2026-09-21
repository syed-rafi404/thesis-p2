# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_AC_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 98.8% |
| WER, per clip mean | 112.3% | 217.8% |
| WER, whole split | 89.9% | 141.1% |
| CER, per clip median | 74.2% | 70.9% |
| CER, per clip mean | 85.0% | 190.0% |
| Term recall | 72.6% | 92.9% |
| Term precision | 64.6% | 33.2% |
| Term F1 | 68.3% | 48.9% |
| Clips that run away | 10 of 184 | 59 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 84 of 184 clips. Wilcoxon signed-rank p = 5.32e-03, sign test p = 1.00e+00.
- **CER**: fine-tune wins on 99 of 184 clips. Wilcoxon signed-rank p = 2.82e-02, sign test p = 3.38e-01.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=174, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: toh hol ei ta hocche amar x or get ta, and ei ta holo amar output. done. so, x or jodi amra bujhe jain, tahole last je exclusive gate, sheta o kintu amader bujha easier hoyechabe.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami ei sign ta diye exor ki bujhacchi mane, or mane ki, plus er exclusive or ami ei plus er byre ekta circle diye exclusive or ki bujhacchi. so, eta er input and output ki rakom hobe? so, eta er input and output ta ber kora ektu lengthy process.

**BanglaASR7/seg_021.wav**

- reference: ei 0 tao hoye jabe 1. and lastly ei 1 ta hoye jabe ki? 0. so eije column ta, eita hocche amar nand gate er output. and lastly nand gate dekhte, nand gate er jodi amra logical circuit ta aki.
- base: so, 0 to be 1, a 0 to be 1, a 0 to be 1 and lastly a 1 to be 0. so, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column
- tuned: so zero ta hoye chabe one, ei zero ta hoye chabe one, ei zero ta hoye chabe one, and lastly ei one ta hoye chabe ki? zero. so ei je column ta, ei ta hocche amar land gate er output. and lastly, land gate dekta, land gate er jodi amra kore.

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ektu age amra jeta bollam, computer shudhu ki niya kaaj kore? zero and one. so a, r, b, er zero er one er combination diye ki ki aa inputs possible? ekta hoyte pare zero, zero.

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: tahole ami sim de jodi ei function ta use kore fili, tahole amake ei path ta cgpa kei plus kore je value ta hobe, seta amake return korbe, jemo three point five five, plus three point seven, plus three point two eight, plus three point five nine, okay?
