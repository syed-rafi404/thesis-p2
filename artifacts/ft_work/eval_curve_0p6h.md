# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\curve\adapter_0p6h`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.0% | 92.6% |
| WER, per clip mean | 112.3% | 151.8% |
| WER, whole split | 89.9% | 126.1% |
| CER, per clip median | 74.2% | 64.5% |
| CER, per clip mean | 85.0% | 113.1% |
| Term recall | 72.6% | 96.1% |
| Term precision | 64.6% | 50.1% |
| Term F1 | 68.3% | 65.9% |
| Clips that run away | 10 of 184 | 48 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 99 of 184 clips. Wilcoxon signed-rank p = 4.01e-01, sign test p = 3.38e-01.
- **CER**: fine-tune wins on 116 of 184 clips. Wilcoxon signed-rank p = 7.35e-01, sign test p = 4.97e-04.

Paired test on the mean per-clip WER, for reference: p = 0.0014 (sign-flip Monte Carlo, n=173, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: toh le, ei ta hoche amar, x or gate ta, and ei ta holo amar, output. done. so, x or jodi amra bucche jain, tahole last je exclusive gate, seite o kinto amr te buccha easier hoyechebe.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami ei sign ta diye exor ki bujhacchi mane or mane ki? plus er exclusive or ami ei plus er bhai re ekta circle diye exclusive or ki bujhacchi. so, ei tar inputs and output ki rekom hobe? so ei tar input and output ta bare kora ektu lengthy process.

**BanglaASR6/seg_022.wav**

- reference: so, ektu aage amra jeta bollam computer shudhu ki ki niye kaj kore? 0 and 1. so a ar b er 0 and 1 er combination diye ki ki inputs possible. ekta hoite pare 0, 0 arekta hoite pare 0, 1.
- base: so, what we have to say is, what is the computer's work? 0 and 1. so, a, r, b, l, 0 and 1 are the combinations given, what are the inputs possible? 1 can be 0, 0, 1 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1, 0 can be 1
- tuned: so, ekto age amra jeta bollam, computer shudhu ki niya kaaj kore? zero and one. so, a, r, b, er, zero are one er combination diye ki ki aa inputs possible? ekta hoyte pare zero, zero, ekta hoyte pare zero, one.

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: tahole ami sim de jodi ei function ta use kore fili, tahole amake ei pass ta c g p a k a plus kore je valo ta hobe, seta amake return korbe, jemo 3.55 plus 3.77 plus 3.28 plus 3.25.

**BanglaASR9/seg_031.wav**

- reference: sheirokom bhabe ami jodi cgpa er e suppose minimum ta dekhte chai minimum cgpa tahole ami eikhane min of cgpa diye dilam. tahole ki hobe? ei 5 ta cgpa er moddhe shob theke lowest jeita which is 3.28 eita amake show kore dibe.
- base: so, if i add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp
- tuned: shiro kon bhabe ami jodi cg paeri, suppose minimum ta dektejai, minimum cg pa. tahole ekhane main of cg pa e diye dilam, tahole ki hobe? ei pastar cg pa e modhe sob teke lowest cheta, which is 3.28, eta amake sho kore dibe?
