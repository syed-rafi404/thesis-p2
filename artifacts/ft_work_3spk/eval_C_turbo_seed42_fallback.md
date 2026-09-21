# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed42`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 11, tuned 11 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.4% | 76.9% |
| WER, per clip mean | 93.8% | 79.7% |
| WER, whole split | 91.1% | 75.1% |
| CER, per clip median | 73.3% | 51.8% |
| CER, per clip mean | 75.7% | 52.4% |
| Term recall | 69.0% | 72.9% |
| Term precision | 87.3% | 94.9% |
| Term F1 | 77.1% | 82.5% |
| Clips that run away | 1 of 75 | 0 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 63 of 75 clips. Wilcoxon signed-rank p = 3.47e-09, sign test p = 1.69e-09.
- **CER**: fine-tune wins on 70 of 75 clips. Wilcoxon signed-rank p = 7.08e-11, sign test p = 9.82e-16.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=71, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR12/seg_001.wav**

- reference: actually je jekono kono kichu measure korar ekta standard format ba standard form.
- base: so, what do you think about unit? what do you think about unit? what do you think about unit? you can't do it. you can't do it. you can't do it. it's a standard form.
- tuned: so, unit amra kano bolte si, unit bolte ki bujhaya? jekono kono major koror, ekta standard form, let's say, unit bolte ki bujhaya?

**BanglaASR10/seg_004.wav**

- reference: eta hocche ttl-er khub basic concept. toh eta diye ki prevent kora hoy? main shomossha jeta eta diye amra prevent korte pari, sheita hocche amader jekono packet er endless looping.
- base: this is a basic concept of etl. the main solution that we have to prevent is the main solution. this is the main solution that we have to prevent is the main solution. we have to make the package of the endless looping.
- tuned: main shomosh a jeta data dia amr prevent korte pari, seita hocche, amr jekono packet er endless looping.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key which when the network is destroyed or downed or downed or downed or downed or downed or downed or downed or downed in the network of the network which is a connection so now the package is not a key because the network will be able to get to this network so when the network was a bit destroyed or downed or the other things i will search for a lot of
- tuned: okay, so, basically eta ki hoy, jokhn ekta network destroy hoye geche parr down hoye ache, kono dui ta network ke moddhe connection, tokhn amd je package eta khuste theke unno sob network ke giye giye, je kon network ke basically parta ache ekhon oh. toh, jehetu ekta e parchile bongchara destroyed hoy giyeche, toh or ei je ei mane search koro ta fechbe,

**BanglaASR11/seg_004.wav**

- reference: toh porer packet-ta jabe ek hajar byte-e, packet three. toh eita hocche porer eita first er ponerosho byte, eita porer ponerosho byte, eita hocche ek jhajar byte, right? toh amar more fragment ki kore? more fragment bole dey je erpore ar ki kon fragment ashbe? jemon jodi ei case e chinta kori, ei je packet ta ami send korbo, ekhane header er field er moddhe more fragment e deoya thakbe one.
- base: the packet is 100 bytes packet 3, so here is the packet faster than 15 bytes, here is the packet, 100 bytes, right? so what do we do with the more fragment? more fragment is 1, so if the packet is 1, the packet is 1,
- tuned: pore eta first er ponor osho byte, eta porer ponor osho byte, eta hoche ekhajer byte, right. toh amar more fragment ki kore? more fragment bole deije, er pore ar ki kono fragment ashbe? jemon jodi ei keache kese chinta kori, ei je packet tar mi scene korba ikhane, header er file er moddhe, more fragment er deyo thakbe one, one.

**BanglaASR13/seg_030.wav**

- reference: er u porer shob case-e shegulo hobe one. mf equals to one, right? to eta hocche amader basically aa pura math-tar summary. tarpore amra jodi fragment value-ta ekhan theke ber korte chai je prottektar jonno fragment value.
- base: is
- tuned: mf equals to one, right. eta hoche amoder basically aa pura math ta summary. tarpore amra jodi fragment value ta ekhane ber korte chai je proti era jono fragment value ta ekhane.
