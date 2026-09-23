# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_final5h\lora_final_s1`
Split: `test.jsonl`, clips scored: 177

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.9% | 41.7% |
| WER, per clip mean | 114.3% | 48.0% |
| WER, whole split | 91.1% | 40.1% |
| CER, per clip median | 67.7% | 16.2% |
| CER, per clip mean | 84.3% | 25.0% |
| Term recall | 73.5% | 95.5% |
| Term precision | 59.1% | 90.2% |
| Term F1 | 65.5% | 92.8% |
| Clips that run away | 13 of 177 | 2 of 177 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 168 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 4.21e-39.
- **CER**: fine-tune wins on 167 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 7.12e-38.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=177, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR27/seg_053.wav**

- reference: got it? so, basically amader main motto-ta, i guess, amra bujhte perechi je amader activation function use kora, regression-er value-gulo use kora, classification-er jinis-gulo use kora keno dorkar.
- base: got it? so basically, i am going to boost the activation function, the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value
- tuned: so, basically, amader main motor-ta, i guess, ami bujhte peracchi je amader activation function use kora, regulation-er value-gula use kora, classification-er jinish-gula use kora, keno dorkar.

**BanglaASR9/seg_036.wav**

- reference: course. course porjonto jawar kotha, amar 8 par korte hobe. tahole t2 + 8, eta amra ki t3? t3 ekhane, right? tarpor ami jodi t4 nei, t4 ki hobe?
- base: course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course
- tuned: course. course porjonto jaoar koto amar 8 par korte hobe. tahole t2 plus 8. eta ami ki? t3. t3 ekhane, right? tarpor ami jodi t4 nei, t4 ki hobe? t4 ki hobe?

**BanglaASR11/seg_019.wav**

- reference: ekhon ami jodi abar etar jonno similar table create kori. okay. a, b amar duita input. so amar possible combination hocche 0 0, 0 1, 1 0 and 1 1. ekhon ami ki korchi first e?
- base: so, we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will
- tuned: ekhon ami jodi abar etar jonno similar table create kori, okay, a b amar duita input. so amar possible combination hocche 0 0 0, 0 0.

**BanglaASR11/seg_043.wav**

- reference: now, a and b, x-nor gate er amra logical circuit ta dekhchi. toh x-or gate aage akbo. x-or gate akar pore ami ekta not gate evabe apply kore dibo. tahole ami peye jabo x-nor gate.
- base: x not gate is, i am logical circuit to see x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate
- tuned: so x nor gate er amra logical circuit ta dekhchi. x or gate age agbo, x or gate akar pore ekta not gate evabe apply.

**BanglaASR27/seg_038.wav**

- reference: okay, amra ei je etokhon dhore bolam je amra duita feature ba tinita feature niye kaj korbo. for example, amra ei je ektu age korchilam, ekta graph-e, sheta chilo feature one chilo age, right? ar feature two-te chilo hocche-apnar hocche tumor size. right?
- base: okay, i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that
- tuned: okay, amra ei je kondore bollam je amra duita feature ba tin-ta feature niye kaj korbo. for example, amra ei je ektu aage korschilam, aa ekta graphic-e, shekhane chilo baram je feature 1-e chilo hocche age, right? ar feature 2-te chilo hocche. apnar hocche tumor size, right?
