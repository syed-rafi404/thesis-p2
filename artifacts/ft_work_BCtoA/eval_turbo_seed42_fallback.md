# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_BCtoA\lora_turbo_seed42`
Split: `test.jsonl`, clips scored: 172

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 27, tuned 11 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.4% | 74.8% |
| WER, per clip mean | 97.3% | 79.9% |
| WER, whole split | 89.0% | 52.4% |
| CER, per clip median | 72.6% | 50.2% |
| CER, per clip mean | 73.9% | 53.8% |
| Term recall | 64.1% | 86.9% |
| Term precision | 88.2% | 96.4% |
| Term F1 | 74.2% | 91.4% |
| Clips that run away | 1 of 172 | 1 of 172 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 135 of 172 clips. Wilcoxon signed-rank p = 5.33e-15, sign test p = 2.63e-14.
- **CER**: fine-tune wins on 140 of 172 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 2.60e-17.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=162, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR1/seg_014.wav**

- reference: toh cholo amra dekhi ekta ekta kore. string. string holo jekono jinish jemon dhoro boli je, jodi boli je amar nam omuk, amar nam tomuk. amar nam dhorlam je, amar nam holo ahsan. thikache? toh amra ki likhte pari string er moddhe? jekono jinish er nam. ami je kotha gula boltesi egular je ekta subtitle ache, shegula keo tumi string hishabe dekhte paro.
- base: i will see that string has a certain kind of the word. i will say the name of my name is amuk. my name is amuk. my name is amuk. my name is amuk. my name is amuk. my name is amuk. what do you say? i will say string and the word name. i will say a few people. i will say the same things. i will say the same thing. which one will say string.
- tuned: tokhon amra dekhi ekta ekta kore string. string holo je konor jinis jemon dhoro boli je jodi boli je amar nam obuk. amar nam tomu. amar nam dhorlam je amar nam holo ansan. thik ache? toh amra ki likhte pari? string er moddhe je kono jinishan nam. ami je kotha gulo boltesi, eigular je ekta sub title ache. shegulo koho tumi string hishabe dekhte paro?

**BanglaASR1/seg_008.wav**

- reference: but ekhane mojar bepar ta hocche ki, pyhton e amader eto koshto kore kon type er data er je data type jeta sheta ekhane likhte hobe na. amra ki korte pari? amra shudhu ekhane num likhe amra value ta boshiye dite pari. python nije nijei bujhe jabe je ei value ta ashole ki. eta ki mm o ki bujhbe? je hae, eta ekta integer value karon ki ekhane kono amar decimal point nai. decimal point ache ekhane but eta toh amra real life e ashole visible na jinishta.
- base: but, it is the most important thing that we have to do with python. we have to write this type of data. what is it? we have to write everything. we have to write everything. we have to write everything. python is not a problem. it is not a decimal point. it is not a decimal point. but it is not visible in real life.
- tuned: but ekhane mojar bapar ta hocche ki, python-e amader eto koshto kore kun type er data je type jeta sheta ekhane likhte hobe ta. amra ki korte pari? amra shudhu ekhane nam likhe amra value ta boshe dite pari. python nije ni jei bujhe jabe je e value ta asho likehi. eta o ki bujbe? je eta ekta integer value, karon ki ekhane kon amar decimal point, right? decimal point ache ekhane, but eta toh amra real life e asole visible na jinishte.

**BanglaASR1/seg_020.wav**

- reference: tarpore ashi sheta holo float. float ki? float holo jeshob gulo amar whole number na. jemon dhoro three point five, two point five. erokom different jotogulo number ache. jemon amra jodi pi er value dekhi sheta ki?
- base: so, we have to look at float. float is the same number as we have whole number. this is 3.5, 2.5. this is different number. so, we have to look at the pi value. so, this is 3.1412.
- tuned: tarpore ashi sheta holo float. float ki? float holo jesobgulo amar whole number na. jemon dhoro 3.5. 2.5. erokhon different jotogulo number ache. jemon amra jodi payer value dekhi sheta ki? 3.14.

**BanglaASR1/seg_043.wav**

- reference: is aa above age limit. erokom ami true false erokom boolean diye check kori je ami hae ami check korte chai je eta ki amar thik? yes, true. jodi na hoy tahole false. so, egulai use kore next class e amra arithmetic operation kora shuru korbo.
- base: so, we will use this next class. we will start arithmetic operations.
- tuned: erokhon ami true false erokom bulyan diye check kori je haa ami check korte chai je eta ki amar thik, yes true. er jodi na hoy tala false. so egula use kore next class e amra arithmetic operation kora shuru korbo.

**BanglaASR3/seg_016.wav**

- reference: ebong input ta ekta string hisabe first a if er kache check korbe, je hae weather ki rain? jodi hoy rain, tahole ki korbe? bring umbrella. weather jodi rain na hoy, jodi sunny check korbe, weather ki sunny? sudhu sunny e hote hobe. karon rain ami check kore aschi, eibar sunny check korbo, sunny jodi hoy, wear white color. tarpore jodi rain o na hoy sunny o nah hoy, duniyar onno jekono word er jonno. ami print korbo, print just come, okay?
- base: input, i would prefer a string to check whether is rain or rain. the thing is to bring umbrella whether is rain or sun or sunburn is the same as rain. so as in the same case, i will print just come
- tuned: emog input ta ekta string hisabe first e if er kache check korbe cho haa whether ki rain. jodi hoy rain, tahole ki korbe? bring umbrella. whether jodi rain na hoy, jodi sunny check korbe. whether ki sunny? shudhu sunny hote hobe. tarano rain ami check kore ar sherpa sunny check korbo. sunny jodi hoy oyer white color. taharpore jodi rain o na hoy, sunny o na hoy, duniar onno jekono word en jonno ami print korbo print just come, okay?
