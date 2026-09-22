# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_lr\lora_lr2e-3_r8`
Split: `test.jsonl`, clips scored: 102

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.7% | 63.2% |
| WER, per clip mean | 116.7% | 152.7% |
| WER, whole split | 93.7% | 73.4% |
| CER, per clip median | 73.2% | 42.7% |
| CER, per clip mean | 90.5% | 146.3% |
| Term recall | 74.3% | 84.0% |
| Term precision | 60.0% | 69.8% |
| Term F1 | 66.4% | 76.2% |
| Clips that run away | 8 of 102 | 13 of 102 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 77 of 102 clips. Wilcoxon signed-rank p = 1.49e-04, sign test p = 2.45e-07.
- **CER**: fine-tune wins on 77 of 102 clips. Wilcoxon signed-rank p = 5.07e-05, sign test p = 2.45e-07.

Paired test on the mean per-clip WER, for reference: p = 0.9215 (sign-flip Monte Carlo, n=99, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so eitai hocche query language er kaaj. so mysq well er ami first e eijitai table ta, ei table ta auto kono bhabe create kora hocche, right?

**BanglaASR12/seg_004.wav**

- reference: so first ei amar ekta database er name dite hobe. suppose database er nam hocche 'university'. er moddhe ekta table ache, shetar nam dhorlam 'student_info'.
- base: so first, i am a database name. suppose database name is university. in the middle, the table is, what name is student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student,
- tuned: so first e amar ekta database er nam dite hobe. suppose database er nam hocche university. er moddhe ekta table ache sheitar nam dhorlam student, student kori.

**BanglaASR14/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche, bar down hoye ache, kono duita network ke moddhe connection. tokhon aa loop amader je packet eto khushte thake, onno shob network e giye je kon network ke basically patha ache ekhono. toh jhetu ektai parchile ebongchita destroyed hoye giyeche, toh or ei je ei mane search korotate achi,

**BanglaASR2/seg_009.wav**

- reference: ekhon print hobe ki? ami jokhn code ta print korbo, hobe ki? first a ei line a ashbe. ei name variable ta pabe, tarpor check korbe je, ei input function call kora hoyeche. function korbe ki, user ke message ta dibe? what is your name? user ekta name dibe. jemon amar naam rafi, ami ekhane raafi dibo.
- base: i am print first and then i will paste the name variable and check the input name and we will use the function function and use the name as a message and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and
- tuned: ekhon print hobe ki? ami jokhon kotta print korbo? hobe ki, first e e line e ashbe, e line e asher por ei name variable ta pabe, tarpor check korbe je input namer amar ekta function call kore koreche. function korbe ki? user ke message ta dibe?

**BanglaASR2/seg_039.wav**

- reference: and, okay, so dekho, ami jokhn f string nia jokhn jinish ta yaa kortesi, sorry ekhane ekta bracket hobe, ami sesh kore dei, eittoh. so ekhane ami jokhn f string ditesi dekho, ami f string er moddhe shudhu, the sum of , eta ekta string hisabe, tarpore jokhn ami curly braces dicchi ekhane, tokhn etar moddhe ami ashole variable ta
- base: and so, i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have a string that i have
- tuned: and, so dekho, ami jokhn f string niye jokhn jinish ta ya kortesi, sorry ekhane ekta bracket hobe, ami sesh kore dei, eitoh. so ekhane ami jokhn f string ditesi, dekho, ekhane ami ekta bracket hobe, ekhane ami sesh kore dei, eitoh.
