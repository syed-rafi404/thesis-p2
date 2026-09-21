# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_v1_repro_5090\lora_run`
Split: `test.jsonl`, clips scored: 137

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.7% | 81.8% |
| WER, per clip mean | 117.2% | 126.1% |
| WER, whole split | 91.7% | 99.2% |
| CER, per clip median | 75.4% | 61.4% |
| CER, per clip mean | 88.5% | 91.8% |
| Term recall | 72.4% | 89.8% |
| Term precision | 58.0% | 51.5% |
| Term F1 | 64.4% | 65.4% |
| Clips that run away | 9 of 137 | 23 of 137 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 83 of 137 clips. Wilcoxon signed-rank p = 3.52e-02, sign test p = 1.64e-02.
- **CER**: fine-tune wins on 96 of 137 clips. Wilcoxon signed-rank p = 1.22e-03, sign test p = 2.95e-06.

Paired test on the mean per-clip WER, for reference: p = 0.5313 (sign-flip Monte Carlo, n=128, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_034.wav**

- reference: done. so x-or jodi amra bujhe jai tahole last je exclusive gate sheitao kintu amader bujha easier hoye jabe. ekhon amra dekhbo x-nor gate.
- base: so, x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or gate and x or
- tuned: tahole eita hocche amar x or gate ta and eita holo amar output. done. so x or jodi amra buche jaayin tahole last je exclusive gate cheita o kintu amate bucha easier hoye chape.

**BanglaASR7/seg_026.wav**

- reference: mane or mane ki? plus. ar ami exclusive orami plus er baire circle diye ami exclusive or ke bujhacchi. so eitar inputs and output kirokom hobe? so eitar input and output ta ber kora ektu lengthy process.
- base: so, i am a scientist and i am asking you what is the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the order of the
- tuned: so ami a sign ta diye exor ki bujhacchi mane or mane ki. plus ar exclusive or ami ei plus er bhai ekta circle diye exclusive or ki bujhacchi. so etar inputs and outputs ki rekom hobe? so etar input and output ta ber kora ektu lengthy process.

**BanglaASR7/seg_021.wav**

- reference: ei 0 tao hoye jabe 1. and lastly ei 1 ta hoye jabe ki? 0. so eije column ta, eita hocche amar nand gate er output. and lastly nand gate dekhte, nand gate er jodi amra logical circuit ta aki.
- base: so, 0 to be 1, a 0 to be 1, a 0 to be 1 and lastly a 1 to be 0. so, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is a column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column, a is column
- tuned: so zero ta hobe one, ei zero ta hobe one, ei zero ta hobe one. and lastly ei one ta hobe ki? zero. so ej column ta eita hocche amar nand gate er output. and lastly nand gate dekta nand gate er jodi ami kori.

**BanglaASR9/seg_032.wav**

- reference: ekhon ami chacchi je cgpa gular sum ber korte. tahole ami simply jodi ei function ta use kore feli, tahole amake ei 5 ta cgpa ke plus kore je value ta hobe sheita amake return korbe, jemon 3.55 plus 3.77 plus 3.28 plus 3.98 plus 3.40.
- base: so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function. so, we will have to return this function.
- tuned: tahole ami simply jodi ei function ta use kore fili, tahole amake ei5 ta c g p a k a plus kore je valota hobe, sheta amake return korbe. je amr 3.55 plus 3.7 plus 3.28 plus 3.8 plus 3.5.

**BanglaASR9/seg_031.wav**

- reference: sheirokom bhabe ami jodi cgpa er e suppose minimum ta dekhte chai minimum cgpa tahole ami eikhane min of cgpa diye dilam. tahole ki hobe? ei 5 ta cgpa er moddhe shob theke lowest jeita which is 3.28 eita amake show kore dibe.
- base: so, if i add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp, then i will add minimum of cgp
- tuned: shereokom bhabe ami jodi, sijitoyeri, suppose minimum ta dekhte je, minimum cgp. tahole amekhane main of cgp e diye dilam, tahole ki hobe ei pastar cgp er moddhe sob theke lowest jeta which is 3.28, eita amake show kore dibe.
