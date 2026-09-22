# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_lr\lora_lr5e-4`
Split: `test.jsonl`, clips scored: 102

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 96.7% | 66.2% |
| WER, per clip mean | 116.7% | 97.4% |
| WER, whole split | 93.7% | 64.0% |
| CER, per clip median | 73.2% | 45.9% |
| CER, per clip mean | 90.5% | 74.3% |
| Term recall | 74.3% | 82.8% |
| Term precision | 60.0% | 96.7% |
| Term F1 | 66.4% | 89.2% |
| Clips that run away | 8 of 102 | 7 of 102 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 79 of 102 clips. Wilcoxon signed-rank p = 9.94e-07, sign test p = 2.28e-08.
- **CER**: fine-tune wins on 76 of 102 clips. Wilcoxon signed-rank p = 2.79e-07, sign test p = 7.44e-07.

Paired test on the mean per-clip WER, for reference: p = 0.2026 (sign-flip Monte Carlo, n=100, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so, etai hocche query language er kaj. so mysql er ami first e ei je table ta, ei table ta oto kono bhabe create kora hoyeche, right?

**BanglaASR12/seg_004.wav**

- reference: so first ei amar ekta database er name dite hobe. suppose database er nam hocche 'university'. er moddhe ekta table ache, shetar nam dhorlam 'student_info'.
- base: so first, i am a database name. suppose database name is university. in the middle, the table is, what name is student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student, student,
- tuned: so first e amar ekta database er nam dite hobe. suppose database er nam hocche university. er moddhe ekta table ache sheitar naam dhorlam student, er moddhe kintu ekta student.

**BanglaASR2/seg_009.wav**

- reference: ekhon print hobe ki? ami jokhn code ta print korbo, hobe ki? first a ei line a ashbe. ei name variable ta pabe, tarpor check korbe je, ei input function call kora hoyeche. function korbe ki, user ke message ta dibe? what is your name? user ekta name dibe. jemon amar naam rafi, ami ekhane raafi dibo.
- base: i am print first and then i will paste the name variable and check the input name and we will use the function function and use the name as a message and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and then i will give the name and
- tuned: ekhon print hobe ki, ami jokhon code ta print korbo, hobe ki, first a elei neashbe. elei neashar por ei name variable ta pabe, tarpor check korbe je input name er amr ekta function call kora ache. function korbe ki? user ke message ta dibe. what is your name? user ekta name dibe, jemon amar nam raffi, ami ekhane raffi dibo.

**BanglaASR14/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: looping. okay. so basically eta ki hoy je jokhon ekta aa network destroy hoye geche but down hoye ache, kono duita network ke moddhe connection. tokhon aa loop amader je packet eita khushte thake onno shob network ke gie gie je kon network ke basically parta ache ekhono. toh jehetu ekta eitai pacchile ebong jeta destroyed hoye giyeche, toh or ei je ei mane search korota ache.

**BanglaASR2/seg_010.wav**

- reference: ekhn ei rafi naam ta hobe ki? ei name er moddhe store kore rakhbe. jeta age ki hoyechilo ekhane? name equals to erokom. jinish ta evabei kaaj korbe jodi user ei rafi value ta dei. tarpore, ei print function a ashbe, print holo python er bulit in ekta function, jeta dia amra kono jinish print kori.
- base: the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to the name is equal to
- tuned: jeita aage ki hoye shulu ekhane, name is equal to, erokho. jinishta ashola evabe kaj khobe, jokhodi user ei rough e value ta deya. tarpore, ei principal ta ekta value ta deya hobe, ekta value ta deya hobe.
