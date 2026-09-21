# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_BCtoA\lora_turbo_seed1`
Split: `test.jsonl`, clips scored: 172

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 27, tuned 7 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.4% | 74.2% |
| WER, per clip mean | 97.3% | 80.1% |
| WER, whole split | 89.0% | 52.3% |
| CER, per clip median | 72.6% | 49.6% |
| CER, per clip mean | 73.9% | 53.9% |
| Term recall | 64.1% | 87.4% |
| Term precision | 88.2% | 97.9% |
| Term F1 | 74.2% | 92.3% |
| Clips that run away | 1 of 172 | 1 of 172 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 135 of 172 clips. Wilcoxon signed-rank p = 8.88e-16, sign test p = 2.63e-14.
- **CER**: fine-tune wins on 139 of 172 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 1.11e-16.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=166, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR1/seg_008.wav**

- reference: but ekhane mojar bepar ta hocche ki, pyhton e amader eto koshto kore kon type er data er je data type jeta sheta ekhane likhte hobe na. amra ki korte pari? amra shudhu ekhane num likhe amra value ta boshiye dite pari. python nije nijei bujhe jabe je ei value ta ashole ki. eta ki mm o ki bujhbe? je hae, eta ekta integer value karon ki ekhane kono amar decimal point nai. decimal point ache ekhane but eta toh amra real life e ashole visible na jinishta.
- base: but, it is the most important thing that we have to do with python. we have to write this type of data. what is it? we have to write everything. we have to write everything. we have to write everything. python is not a problem. it is not a decimal point. it is not a decimal point. but it is not visible in real life.
- tuned: but ekhane mojar bapar ta hocche ki, python-e amader eto koshto kore kun type er data je type jeta sheta ekhane likhte hobe ta. amra ki korte pari? amra shudhu ekhane nam likhe amra value ta boshye dite pari. python nije ni je bujhe jabe je e value ta ashole ki. eta ki buh o ki bujbe? je heta ekta integer value. karon ki ekhane kono amar decimal point nai. decimal point ache ekhane, but eta toh amra real life e ashole visible na jinishte.

**BanglaASR1/seg_014.wav**

- reference: toh cholo amra dekhi ekta ekta kore. string. string holo jekono jinish jemon dhoro boli je, jodi boli je amar nam omuk, amar nam tomuk. amar nam dhorlam je, amar nam holo ahsan. thikache? toh amra ki likhte pari string er moddhe? jekono jinish er nam. ami je kotha gula boltesi egular je ekta subtitle ache, shegula keo tumi string hishabe dekhte paro.
- base: i will see that string has a certain kind of the word. i will say the name of my name is amuk. my name is amuk. my name is amuk. my name is amuk. my name is amuk. my name is amuk. what do you say? i will say string and the word name. i will say a few people. i will say the same things. i will say the same thing. which one will say string.
- tuned: tokhon amra dekhi ekta ekta kore string. string holo je kono jimish jemon dhoro boli je jodi boli je aman nam obok, aman nam tomo. aman nam dhorlam je aman nam holo ansan. thik ache? toh amra ki likhte pari? string er moddhe je kono jimish er nam. ami je kotha gula boltesi, egular je ekta subtile ache. shegulo koho tumi string hishabe dekhte paro. string bujhon ar jonno.

**BanglaASR1/seg_043.wav**

- reference: is aa above age limit. erokom ami true false erokom boolean diye check kori je ami hae ami check korte chai je eta ki amar thik? yes, true. jodi na hoy tahole false. so, egulai use kore next class e amra arithmetic operation kora shuru korbo.
- base: so, we will use this next class. we will start arithmetic operations.
- tuned: erokom ami true false erokom bulli and diye check kori je hain ami check korte chai je eta ki amar thik? yes, true. jodi na hoye tala false. so egula use kore next class e amra arithmetic operation kora shuru korbo.

**BanglaASR2/seg_021.wav**

- reference: ebong tomra toh obviously first time ei bhul ta korbai, seta holo je, ami jokhn input ta nicchi, eta by default, always string hisabei ashbe. so kew jodi number ta bole je ten. ashole, je pacche seta ekta string hisabe ashtese ekhane.
- base: so, obviously first time i'm going to talk about this. so, i'm not going to say that input is not going to be used. so, by default always string is going to be used. so, when i say 10, i'm going to say that this is the string is used.
- tuned: so obviously first name e bhulta korba, sheta holo je ami jekhon input ta nicchi, eta by default always string hishabe ashbe. so keba jodi number ta bole je 10, ashole je pacche sheta ekta string hishabe ashtese ekhane.

**BanglaASR1/seg_030.wav**

- reference: variable er naming er shobcheye first je rule sheta hocche amra kokhonoi kono integer value diye kono variable er name shuru korte parbo na. tahole error ashbe. jemon amra jodi example dei. jemon dhoro 1 lkhlam. eta ki ekta integer value ekta whole number.
- base: first rule is that we have to give integer value, so we have to give the variable number. we have to give example, we have to give one number. we have to give integer value, and we have to give whole number. 1 and 5. we have to give name equal to, we have to give it to the rough.
- tuned: sobtheke first je rule sheta hocche amra kokhon noi kono integer value diye kono ekta variable er nam shudu korte parbuna, tahole ero rajbe. jemon amra jodi example dei jemon thoro one likhlam. eta ki ekta integer value, ekta whole number. one er porjhjodi ami lekhi je name equal to thoro rough-e likhlam.
