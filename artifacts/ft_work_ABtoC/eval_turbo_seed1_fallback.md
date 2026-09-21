# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_ABtoC\lora_turbo_seed1`
Split: `test.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 11, tuned 5 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.4% | 79.3% |
| WER, per clip mean | 93.8% | 81.0% |
| WER, whole split | 91.1% | 73.5% |
| CER, per clip median | 73.3% | 53.9% |
| CER, per clip mean | 75.7% | 53.6% |
| Term recall | 69.0% | 69.0% |
| Term precision | 87.3% | 95.7% |
| Term F1 | 77.1% | 80.2% |
| Clips that run away | 1 of 75 | 2 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 63 of 75 clips. Wilcoxon signed-rank p = 7.60e-08, sign test p = 1.69e-09.
- **CER**: fine-tune wins on 67 of 75 clips. Wilcoxon signed-rank p = 4.63e-10, sign test p = 1.01e-12.

Paired test on the mean per-clip WER, for reference: p = 0.0010 (sign-flip Monte Carlo, n=74, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_001.wav**

- reference: actually je jekono kono kichu measure korar ekta standard format ba standard form.
- base: so, what do you think about unit? what do you think about unit? what do you think about unit? you can't do it. you can't do it. you can't do it. it's a standard form.
- tuned: so unit amra kiano bolte si. taki unit bolte ki bujhaye actually je jekono kono kish major koror ekta standard form, standard form let's say.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key which when the network is destroyed or downed or downed or downed or downed or downed or downed or downed or downed in the network of the network which is a connection so now the package is not a key because the network will be able to get to this network so when the network was a bit destroyed or downed or the other things i will search for a lot of
- tuned: so, basically eta ki hoy je jokhn ekta network destroy hoye geche bar down hoye ache, kono dui etar network ke moddhe connection. takhon loop ta amr je packet eto khuste thake onno shob network ki ki hoye je kon network ke basically parta ache ekhono.

**BanglaASR10/seg_004.wav**

- reference: eta hocche ttl-er khub basic concept. toh eta diye ki prevent kora hoy? main shomossha jeta eta diye amra prevent korte pari, sheita hocche amader jekono packet er endless looping.
- base: this is a basic concept of etl. the main solution that we have to prevent is the main solution. this is the main solution that we have to prevent is the main solution. we have to make the package of the endless looping.
- tuned: main shomosh ta jeta ei ta diye amar prevent korte pari sheita hocche, amr jekono packet er endless looping.

**BanglaASR10/seg_003.wav**

- reference: toh ei je destroy korar je technique ta ba method ta, eitake amra hocche set kori ttl diye. ttl bolte gele je etogula hop, hop bolte ekhane bujhachchi apnar router ba pc. toh etogula router-to-router jump er poreo jodi o destination theke kono acknowledgment na ashe, tahole amra aa packet ta ke destroy kore notun packet pathabo.
- base: so, the destroyer method is set for ttl. ttl is called hop, hop is called router and pc. so, if the router is a router, then the destination is not available. so, we destroy the packet and then we will destroy the packet.
- tuned: tokhon je destroy korar je technique ta ba method ta etake amra hocche set kori ttl diye. ttl bolte gele jeta gula hop hop bolte kane bujhacchi, abnay router ba pc. toh eto gula router to router jump er poreo jodi o destination theke kon acknowledgement na ashe. tahole amra aa packet taake destroy kore noth packet pathabo.

**BanglaASR11/seg_006.wav**

- reference: but jokhon amra packet three te chole jabo, jekhane ek hajar byte matro jabe, because achei ar ek hajar byte, so 100 byte jabe, tokhon amra dekhte pabo mf-er moddhe value-ta zero. tar mane o bujhachche je amar eitai last packet chilo.
- base: but when you have to use the package 3, you can use 100 bytes, because it is 100 bytes. so, when you have to use the token, you can use the value of 0. so, i have to ask you to use the last package.
- tuned: but jokhn amra packet three te chole jabo jekhane ekhjar byte makro jabe because achei era ekhjar byte. so, ekhane ekhjar byte e jabe jekhn amra jokhn amra value debo, emay fer moddhe valuta zero. tar mane o bujhacche je amar eitai last packet chilo.
