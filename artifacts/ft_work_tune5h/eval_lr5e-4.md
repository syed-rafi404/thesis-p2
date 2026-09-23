# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_tune5h\lora_lr5e-4`
Split: `test.jsonl`, clips scored: 101

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 97.6% | 60.0% |
| WER, per clip mean | 116.8% | 89.5% |
| WER, whole split | 93.8% | 65.6% |
| CER, per clip median | 73.8% | 37.9% |
| CER, per clip mean | 91.9% | 64.6% |
| Term recall | 74.3% | 88.1% |
| Term precision | 62.2% | 75.1% |
| Term F1 | 67.7% | 81.1% |
| Clips that run away | 8 of 101 | 9 of 101 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 79 of 101 clips. Wilcoxon signed-rank p = 8.02e-08, sign test p = 1.01e-08.
- **CER**: fine-tune wins on 80 of 101 clips. Wilcoxon signed-rank p = 1.25e-07, sign test p = 2.73e-09.

Paired test on the mean per-clip WER, for reference: p = 0.0148 (sign-flip Monte Carlo, n=98, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so eitai hocche query language er kaj. so mysql er ami first e ei je table ta, ei table te oto kono bhabe create kora hoyeche, right?

**BanglaASR12/seg_004.wav**

- reference: so first ei amar ekta database er name dite hobe. suppose database er nam hocche 'university'. er moddhe ekta table ache, shetar nam dhorlam 'student_info'.
- base: so first, i am a database name. suppose database name is university. in the middle, the table is, what name is student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student,
- tuned: so amra ekta database er nam dite hobe. suppose database er nam hocche university. er moddhe ekta table ache shetar nam dhorlam, student, student, student.

**BanglaASR2/seg_009.wav**

- reference: ekhon print hobe ki? ami jokhn code ta print korbo, hobe ki? first a ei line a ashbe. ei name variable ta pabe, tarpor check korbe je, ei input function call kora hoyeche. function korbe ki, user ke message ta dibe? what is your name? user ekta name dibe. jemon amar naam rafi, ami ekhane raafi dibo.
- base: i am print first and then i will paste the name variable and check the input name and we will use the function function and use the name as a message and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and
- tuned: ekhon print hobe ki? ami jokhon code tar print korbo, hobe ki, first a l i ne ashbe. l ne ashar por ei name variable ta pabe. tarpor check korbe je input nam er amar ekta function call kora heche. function korbe ki? user ke message ta dibe. what is your name? user ekta name dibe jemon amar nam rafi.

**BanglaASR14/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: so basically it is a key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all
- tuned: okay. so basically eita ki hoy? je jokhon ekta network destroy hoye geche, but down hoye ache, kono duita network-er moddhe connection tokhon loop, amader je packet-e eta khuhte thake, onno shob network-e giye giye je kon network-e basically parta ache ekhono. to jehetu ekta pathchile ebog jeta destroyed hoye giyeche, to or ei je ei, mane, search korata ache,

**BanglaASR2/seg_039.wav**

- reference: and, okay, so dekho, ami jokhn f string nia jokhn jinish ta yaa kortesi, sorry ekhane ekta bracket hobe, ami sesh kore dei, eittoh. so ekhane ami jokhn f string ditesi dekho, ami f string er moddhe shudhu, the sum of , eta ekta string hisabe, tarpore jokhn ami curly braces dicchi ekhane, tokhn etar moddhe ami ashole variable ta
- base: and so, i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have
- tuned: okay. so dekho, ami jokhon f string niye jokhon jinishta ia kortesi, sorry ekhane ekta bracket hobe, ami sesh kore dei, ektoh. so ekhane ami jokhon f string ditesi, dekho ami ekhane ekta bracket hobe, ekhane ami shesh kore dei, ekta.
