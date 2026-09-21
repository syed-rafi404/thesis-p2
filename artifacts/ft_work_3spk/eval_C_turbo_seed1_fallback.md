# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed1`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 11, tuned 12 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.4% | 77.6% |
| WER, per clip mean | 93.8% | 77.0% |
| WER, whole split | 91.1% | 74.3% |
| CER, per clip median | 73.3% | 44.2% |
| CER, per clip mean | 75.7% | 47.0% |
| Term recall | 69.0% | 69.0% |
| Term precision | 87.3% | 95.7% |
| Term F1 | 77.1% | 80.2% |
| Clips that run away | 1 of 75 | 0 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 61 of 75 clips. Wilcoxon signed-rank p = 3.15e-10, sign test p = 3.81e-08.
- **CER**: fine-tune wins on 70 of 75 clips. Wilcoxon signed-rank p = 1.23e-12, sign test p = 9.82e-16.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=71, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_001.wav**

- reference: actually je jekono kono kichu measure korar ekta standard format ba standard form.
- base: so, what do you think about unit? what do you think about unit? what do you think about unit? you can't do it. you can't do it. you can't do it. it's a standard form.
- tuned: so amra kono amra bolte ki ki bujha? jekono kono major koror, ekta standard form, ekta standard form, let's amra ekta standard form.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key which when the network is destroyed or downed or downed or downed or downed or downed or downed or downed or downed in the network of the network which is a connection so now the package is not a key because the network will be able to get to this network so when the network was a bit destroyed or downed or the other things i will search for a lot of
- tuned: okay, so, basically eta ki hoy, je jokhn ekta network destroy hoye geche bar down hoye ache, kono dui eta network ke moddhe connection, tokhn amoddhe je package eto khuste theke onno sob network ke diye giye, je kon network ke basically, parta ache ekhono. toh jehetu ekta e parchile ebong jeta destroyed hoye giyeche, toh or ei je ei, mine, search korot a achi naah,

**BanglaASR10/seg_004.wav**

- reference: eta hocche ttl-er khub basic concept. toh eta diye ki prevent kora hoy? main shomossha jeta eta diye amra prevent korte pari, sheita hocche amader jekono packet er endless looping.
- base: this is a basic concept of etl. the main solution that we have to prevent is the main solution. this is the main solution that we have to prevent is the main solution. we have to make the package of the endless looping.
- tuned: main shomosh a jeta data dia amr prevent korte pari, seita hocche, amr jekono packet er endless looping.

**BanglaASR11/seg_007.wav**

- reference: amar je fragment er packet gula theke last packet, tar mane purata chole giyeche ei porjonto. okay. so eita bujha khub-e important chilo jokhon amra mtu er math gula dekhbo. mtu er math er khetre/ ar next video theke amra inshaallah mtu er math shuru korbo. thik ache. best of luck. assalamu alaikum.
- base: so, this is a very important thing to know about mtu or maths.
- tuned: amra je fragmented package gula theke last package ta amra pura ta cholei giyeche. okay. so eita bujha khub e important chilo jekhn amra empty er math gula dekhbe, empty er math er kethre. next video theke amra, encha alla empty er math choro korbo. thikase? best of luck. aa assalamualaikum.

**BanglaASR13/seg_030.wav**

- reference: er u porer shob case-e shegulo hobe one. mf equals to one, right? to eta hocche amader basically aa pura math-tar summary. tarpore amra jodi fragment value-ta ekhan theke ber korte chai je prottektar jonno fragment value.
- base: is
- tuned: er upore sob case a, sigula by one, mf equals to one, right. eta hoche amader basically, aa pura math taar summary. tarpore amra jodi fragment value ta ekhante ke ber korte chai, je prothe era jono fragment a.
