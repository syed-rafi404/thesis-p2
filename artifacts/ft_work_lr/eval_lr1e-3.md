# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_lr\lora_lr1e-3`
Split: `test.jsonl`, clips scored: 102

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.7% | 64.8% |
| WER, per clip mean | 116.7% | 86.1% |
| WER, whole split | 93.7% | 58.0% |
| CER, per clip median | 73.2% | 45.4% |
| CER, per clip mean | 90.5% | 63.3% |
| Term recall | 74.3% | 87.5% |
| Term precision | 60.0% | 83.0% |
| Term F1 | 66.4% | 85.2% |
| Clips that run away | 8 of 102 | 7 of 102 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 80 of 102 clips. Wilcoxon signed-rank p = 6.27e-09, sign test p = 6.42e-09.
- **CER**: fine-tune wins on 78 of 102 clips. Wilcoxon signed-rank p = 5.61e-09, sign test p = 7.68e-08.

Paired test on the mean per-clip WER, for reference: p = 0.0026 (sign-flip Monte Carlo, n=97, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so eitai hocche query language er kaj. so ami first e ei jitable ta, ei table ta oto kono bhabe create kora hoyeche, right?

**BanglaASR12/seg_004.wav**

- reference: so first ei amar ekta database er name dite hobe. suppose database er nam hocche 'university'. er moddhe ekta table ache, shetar nam dhorlam 'student_info'.
- base: so first, i am a database name. suppose database name is university. in the middle, the table is, what name is student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student,
- tuned: so, first e amar ekta database er nam dite hobe. suppose database er nam hocche university. er moddhe ekta table ache sheitar nam dhorlam student, er moddhe ekta table ache sheitar nam dhorlam student, er moddhe ki hobe?

**BanglaASR2/seg_009.wav**

- reference: ekhon print hobe ki? ami jokhn code ta print korbo, hobe ki? first a ei line a ashbe. ei name variable ta pabe, tarpor check korbe je, ei input function call kora hoyeche. function korbe ki, user ke message ta dibe? what is your name? user ekta name dibe. jemon amar naam rafi, ami ekhane raafi dibo.
- base: i am print first and then i will paste the name variable and check the input name and we will use the function function and use the name as a message and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and
- tuned: ekhon print hobe ki? ami jokhon code ta print korbo, hobe ki, first e eleine ashbe. eleine ashar por ei name variable ta pabe. tarpor check korbe je input nam er amar ekta function call kore heche. function korbe ki? user ke message ta dibe. what is your name? user ekta name dibe jemon amar nam rafi.

**BanglaASR14/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: looping. okay. so basically eta ki hoy je jokhon ekta aa network destroy hoye geche, bar down hoye ache, kono duita network ke moddhe connection. tokhon aa loop amader je packet eto khushte thake onno shob network ke giye giye, je kon network ke basically aa parta ache ekhono. toh jehetu ekta type parchile bongcheta destroyed hoye giyeche, toh or ei je ei mane search korota ache,

**BanglaASR2/seg_010.wav**

- reference: ekhn ei rafi naam ta hobe ki? ei name er moddhe store kore rakhbe. jeta age ki hoyechilo ekhane? name equals to erokom. jinish ta evabei kaaj korbe jodi user ei rafi value ta dei. tarpore, ei print function a ashbe, print holo python er bulit in ekta function, jeta dia amra kono jinish print kori.
- base: the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to
- tuned: jeita aage ki hoye shulo ekhane, name is equal to, erokom. jinishta shulo ebhabe kaaj hobe jokhudi user ei rough e value ta dey. tarpore ei principal e jeta shulo ekhane korte paro abar value korte paro ki ki hobe?
