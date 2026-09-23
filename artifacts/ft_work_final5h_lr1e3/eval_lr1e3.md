# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_final5h_lr1e3\lora_lr1e3`
Split: `test.jsonl`, clips scored: 177

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.9% | 42.5% |
| WER, per clip mean | 114.3% | 50.2% |
| WER, whole split | 91.1% | 42.9% |
| CER, per clip median | 67.7% | 15.8% |
| CER, per clip mean | 84.3% | 26.9% |
| Term recall | 73.5% | 93.4% |
| Term precision | 59.1% | 89.6% |
| Term F1 | 65.5% | 91.5% |
| Clips that run away | 13 of 177 | 1 of 177 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 167 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 7.12e-38.
- **CER**: fine-tune wins on 164 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 1.94e-34.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=177, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR27/seg_053.wav**

- reference: got it? so, basically amader main motto-ta, i guess, amra bujhte perechi je amader activation function use kora, regression-er value-gulo use kora, classification-er jinis-gulo use kora keno dorkar.
- base: got it? so basically, i am going to boost the activation function, the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value
- tuned: so basically amader main motor-ta i guess amra bujhte berechi je amader activation function use kora, regulation-er value-gula use kora, classification-er jinishgula use kora keno dorkar.

**BanglaASR9/seg_036.wav**

- reference: course. course porjonto jawar kotha, amar 8 par korte hobe. tahole t2 + 8, eta amra ki t3? t3 ekhane, right? tarpor ami jodi t4 nei, t4 ki hobe?
- base: course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course
- tuned: course porjonto jaar koto amar 8 par korte hobe. tahole t2 plus 8. eta ami ki? t3. t3 ekhane, right? tarpor ami jodi t4 nei, t4 ki hobe? t4 plus 8.

**BanglaASR11/seg_019.wav**

- reference: ekhon ami jodi abar etar jonno similar table create kori. okay. a, b amar duita input. so amar possible combination hocche 0 0, 0 1, 1 0 and 1 1. ekhon ami ki korchi first e?
- base: so, we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will
- tuned: ekhon ami jodi abar etar jonno similar table create kori. okay. a, b amar duita input. so amar possible combination hocche 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,

**BanglaASR11/seg_043.wav**

- reference: now, a and b, x-nor gate er amra logical circuit ta dekhchi. toh x-or gate aage akbo. x-or gate akar pore ami ekta not gate evabe apply kore dibo. tahole ami peye jabo x-nor gate.
- base: x not gate is, i am logical circuit to see x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate
- tuned: so ebhane ami ekta not gate er amra logical circuit dekhchi. so ebhane ami ekta not gate aage akbo, x or gate akar pore ekta not gate evabe apply kaj.

**BanglaASR27/seg_038.wav**

- reference: okay, amra ei je etokhon dhore bolam je amra duita feature ba tinita feature niye kaj korbo. for example, amra ei je ektu age korchilam, ekta graph-e, sheta chilo feature one chilo age, right? ar feature two-te chilo hocche-apnar hocche tumor size. right?
- base: okay, i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that
- tuned: amra ei je khondore bollam je amra duita feature ba tin-ta feature niye kaj korbo. for example, amra ei je ektu age korsilam, aa ekta graph ake, shekhane chilo poram. feature one-e chilo hocche age, right? ar feature two-te chilo hocche, apnar hocche tumor size.
