# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_final5h\lora_final`
Split: `test.jsonl`, clips scored: 177

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.9% | 189.8% |
| WER, per clip mean | 114.3% | 268.6% |
| WER, whole split | 91.1% | 222.0% |
| CER, per clip median | 67.7% | 118.7% |
| CER, per clip mean | 84.3% | 184.0% |
| Term recall | 73.5% | 0.0% |
| Term precision | 59.1% | 0.0% |
| Term F1 | 65.5% | 0.0% |
| Clips that run away | 13 of 177 | 82 of 177 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 17 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 1.00e+00.
- **CER**: fine-tune wins on 35 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 1.00e+00.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=177, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR27/seg_053.wav**

- reference: got it? so, basically amader main motto-ta, i guess, amra bujhte perechi je amader activation function use kora, regression-er value-gulo use kora, classification-er jinis-gulo use kora keno dorkar.
- base: got it? so basically, i am going to boost the activation function, the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value of the value
- tuned: toh amra jodi amra jodi amra jodi amader kori, amader amader amader kori, amader amader amader kori, amra kori, amra kori, amra kori, amra kintu amra kori, amra kintu amra kori.

**BanglaASR9/seg_036.wav**

- reference: course. course porjonto jawar kotha, amar 8 par korte hobe. tahole t2 + 8, eta amra ki t3? t3 ekhane, right? tarpor ami jodi t4 nei, t4 ki hobe?
- base: course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course course
- tuned: so, ekhon ekta ekta jinish, ekta ki? ekta ekta ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta ekta ekta je ekta je ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekhane,

**BanglaASR27/seg_038.wav**

- reference: okay, amra ei je etokhon dhore bolam je amra duita feature ba tinita feature niye kaj korbo. for example, amra ei je ektu age korchilam, ekta graph-e, sheta chilo feature one chilo age, right? ar feature two-te chilo hocche-apnar hocche tumor size. right?
- base: okay, i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that i am ready to say that
- tuned: toh amra jodi amra jodi amra jodi amra jodi amra kori, amra jodi amader je amader je amader kori, amra jodi amra jodi amra kori, amra kori, amra jodi amra kori, amra kori, amra kintu amra kori, amra kintu amra kori, amra kintu amra kintu amra kori, amra kintu amra kintu amra kintu amra kore, amra kintu amra kintu amra kintu amra kore, amra kintu amra kintu amra kintu amra kintu amra kintu amra kintu amra kintu kintu kore,

**BanglaASR9/seg_035.wav**

- reference: plus 4, eta holo amar t2-te tahole ki ashlo? info porjonto ami achi, mane ei porjonto ami just khali likhlam t2, okay? t2-te ei porjonto ache, tarpor ekhan theke r call koreche. r-e jodi jai, r-e jawar pore amake ki boleche?
- base: plus 4 add plus 4, so we have t2 where we have info port that is, so we have one thing to do is t2 and t2 where t2 is, so we have r called, so we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we have to go and we
- tuned: so, ekhon ekta ekta ekta ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta ekta je ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekhane,

**BanglaASR8/seg_009.wav**

- reference: bodmas rules follow korle multiplication er aage kintu bracket ashe, to ami jodi ekhane t1 = b - c likhe rakhi, tahole ki eta pacchi? okay? ekhon t2 = t2 times ki? t1* a, tahole etotuku holo amar ache purota ekhon t2 er bhitor, ar eta holo t1. okay?
- base: so, if you follow the rule of the rule of the rule of the rule, you can see that the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule of the rule
- tuned: so, ekhon ekta ekta ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta je ekta ekta ekta je ekta ekta ekta ekta ekta je ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekta ekhane, ekta ekta ekta ekhane ekta ekta ekhane ekhane ekh
