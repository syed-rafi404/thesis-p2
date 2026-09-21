# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test_7to9.jsonl`, clips scored: 137

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.7% | 96.3% |
| WER, per clip mean | 117.2% | 184.0% |
| WER, whole split | 91.7% | 145.5% |
| CER, per clip median | 75.4% | 72.9% |
| CER, per clip mean | 88.5% | 136.0% |
| Term recall | 72.4% | 86.2% |
| Term precision | 58.0% | 37.6% |
| Term F1 | 64.4% | 52.4% |
| Clips that run away | 9 of 137 | 44 of 137 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 67 of 137 clips. Wilcoxon signed-rank p = 9.16e-03, sign test p = 1.00e+00.
- **CER**: fine-tune wins on 67 of 137 clips. Wilcoxon signed-rank p = 2.96e-02, sign test p = 1.00e+00.

Paired test on the mean per-clip WER, for reference: p = 0.0003 (sign-flip Monte Carlo, n=135, 20000 resamples).

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

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: tahole ami simply jodi ei function ta use kore fili, tahole amake ei paks ta c g p a k a plus kore je dalota hobe, se ta amake return korbe, jemon 3.55 plus 3.7 plus 3.28 plus 3.5 ta hbe rata hobe.

**BanglaASR9/seg_031.wav**

- reference: sheirokom bhabe ami jodi cgpa er e suppose minimum ta dekhte chai minimum cgpa tahole ami eikhane min of cgpa diye dilam. tahole ki hobe? ei 5 ta cgpa er moddhe shob theke lowest jeita which is 3.28 eita amake show kore dibe.
- base: so, if i add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp
- tuned: shero kon bhabe ami jodi cg paeri, suppose minimum ta dekhte jai, minimum cgpa, tahole ami ekhane mean of cgpa dia dilam, tahole ki hobe ei pastase gpa moddhe sob teke lowest jeta, which is 3.28 eta ama ke, show kore dibe?
