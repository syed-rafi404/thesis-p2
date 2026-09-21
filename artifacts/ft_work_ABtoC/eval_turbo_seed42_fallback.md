# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_ABtoC\lora_turbo_seed42`
Split: `test.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 11, tuned 5 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.4% | 74.3% |
| WER, per clip mean | 93.8% | 76.0% |
| WER, whole split | 91.1% | 72.6% |
| CER, per clip median | 73.3% | 44.4% |
| CER, per clip mean | 75.7% | 48.2% |
| Term recall | 69.0% | 73.6% |
| Term precision | 87.3% | 95.0% |
| Term F1 | 77.1% | 83.0% |
| Clips that run away | 1 of 75 | 0 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 61 of 75 clips. Wilcoxon signed-rank p = 1.60e-09, sign test p = 3.81e-08.
- **CER**: fine-tune wins on 67 of 75 clips. Wilcoxon signed-rank p = 2.64e-12, sign test p = 1.01e-12.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=68, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_001.wav**

- reference: actually je jekono kono kichu measure korar ekta standard format ba standard form.
- base: so, what do you think about unit? what do you think about unit? what do you think about unit? you can't do it. you can't do it. you can't do it. it's a standard form.
- tuned: so unit amra kiano bolte si itake? unit bolte ki bujhay actually je jekono kono kishir major koror ekta standard form, standard form let

**BanglaASR10/seg_004.wav**

- reference: eta hocche ttl-er khub basic concept. toh eta diye ki prevent kora hoy? main shomossha jeta eta diye amra prevent korte pari, sheita hocche amader jekono packet er endless looping.
- base: this is a basic concept of etl. the main solution that we have to prevent is the main solution. this is the main solution that we have to prevent is the main solution. we have to make the package of the endless looping.
- tuned: main shomosh ta jeta eta diye ama prevent korte pari sheita hocche amader jekono packet er endless looping.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key which when the network is destroyed or downed or downed or downed or downed or downed or downed or downed or downed in the network of the network which is a connection so now the package is not a key because the network will be able to get to this network so when the network was a bit destroyed or downed or the other things i will search for a lot of
- tuned: okay, so basically eta ki hoy je jokhn ekta network destroy hoye gache bar down hoye ache kono dui tar network ke moddhe connection. tokhn amod e je packet etar khushte theke unno shob network ke gie gie je kon network ke basically parta ache ekhono.

**BanglaASR11/seg_006.wav**

- reference: but jokhon amra packet three te chole jabo, jekhane ek hajar byte matro jabe, because achei ar ek hajar byte, so 100 byte jabe, tokhon amra dekhte pabo mf-er moddhe value-ta zero. tar mane o bujhachche je amar eitai last packet chilo.
- base: but when you have to use the package 3, you can use 100 bytes, because it is 100 bytes. so, when you have to use the token, you can use the value of 0. so, i have to ask you to use the last package.
- tuned: but jokhon amra packet three te chole jabo, jikhane ekhajer byte makro jabe, because achi ei ekhajer byte. so ekhane ekhane jebe tokhon ami dhorte debo, ei fer moddhe valut er zero. tar mane o bujhacche je amar eitai last packet chilo.

**BanglaASR13/seg_030.wav**

- reference: er u porer shob case-e shegulo hobe one. mf equals to one, right? to eta hocche amader basically aa pura math-tar summary. tarpore amra jodi fragment value-ta ekhan theke ber korte chai je prottektar jonno fragment value.
- base: is
- tuned: er upore shob keithe shigula be 1. emf equals to 1, right? eta hocche amader basically aa pura matter summary. tarpore amra jodi fragment value ta ekhane ke ber korte chai jebong.
