# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_tune5h\lora_lr2e-3_qkvo`
Split: `test.jsonl`, clips scored: 101

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 97.6% | 174.4% |
| WER, per clip mean | 116.8% | 272.2% |
| WER, whole split | 93.8% | 165.6% |
| CER, per clip median | 73.8% | 134.7% |
| CER, per clip mean | 91.9% | 253.2% |
| Term recall | 74.3% | 0.0% |
| Term precision | 62.2% | 0.0% |
| Term F1 | 67.7% | 0.0% |
| Clips that run away | 8 of 101 | 36 of 101 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 6 of 101 clips. Wilcoxon signed-rank p = 4.16e-12, sign test p = 1.00e+00.
- **CER**: fine-tune wins on 17 of 101 clips. Wilcoxon signed-rank p = 8.03e-12, sign test p = 1.00e+00.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=100, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so, ekhane amra ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ek

**BanglaASR2/seg_010.wav**

- reference: ekhn ei rafi naam ta hobe ki? ei name er moddhe store kore rakhbe. jeta age ki hoyechilo ekhane? name equals to erokom. jinish ta evabei kaaj korbe jodi user ei rafi value ta dei. tarpore, ei print function a ashbe, print holo python er bulit in ekta function, jeta dia amra kono jinish print kori.
- base: the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to
- tuned: so, ekhane amra ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ek

**BanglaASR2/seg_009.wav**

- reference: ekhon print hobe ki? ami jokhn code ta print korbo, hobe ki? first a ei line a ashbe. ei name variable ta pabe, tarpor check korbe je, ei input function call kora hoyeche. function korbe ki, user ke message ta dibe? what is your name? user ekta name dibe. jemon amar naam rafi, ami ekhane raafi dibo.
- base: i am print first and then i will paste the name variable and check the input name and we will use the function function and use the name as a message and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and
- tuned: so, ekhane amra ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ek

**BanglaASR14/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: so basically it is a key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all
- tuned: so, ekhane amra ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ek

**BanglaASR2/seg_039.wav**

- reference: and, okay, so dekho, ami jokhn f string nia jokhn jinish ta yaa kortesi, sorry ekhane ekta bracket hobe, ami sesh kore dei, eittoh. so ekhane ami jokhn f string ditesi dekho, ami f string er moddhe shudhu, the sum of , eta ekta string hisabe, tarpore jokhn ami curly braces dicchi ekhane, tokhn etar moddhe ami ashole variable ta
- base: and so, i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have
- tuned: so, ekhane amra ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ekta, ek
