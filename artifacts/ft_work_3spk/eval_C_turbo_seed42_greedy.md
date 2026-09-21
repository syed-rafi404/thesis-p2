# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed42`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.6% | 79.2% |
| WER, per clip mean | 109.7% | 123.7% |
| WER, whole split | 93.0% | 87.2% |
| CER, per clip median | 74.2% | 54.4% |
| CER, per clip mean | 85.1% | 81.2% |
| Term recall | 64.3% | 68.2% |
| Term precision | 84.7% | 96.7% |
| Term F1 | 73.1% | 80.0% |
| Clips that run away | 6 of 75 | 8 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 59 of 75 clips. Wilcoxon signed-rank p = 5.94e-04, sign test p = 6.11e-07.
- **CER**: fine-tune wins on 63 of 75 clips. Wilcoxon signed-rank p = 1.74e-05, sign test p = 1.69e-09.

Paired test on the mean per-clip WER, for reference: p = 0.5914 (sign-flip Monte Carlo, n=74, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR13/seg_029.wav**

- reference: mf-er value zero hobe kokhon? jokhon amra last fragment paya jabo. tahole ekhetre amader last fragment three number na? tahole ekhane mf-er flag-ta hobe zero. je er mane bujhay er pore ar kono fragment nai.
- base: the last fragment is 0, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last
- tuned: je er man er bujhai er porre r kono fragment nei. toh ami ekhane ki ki ki?

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: okay, so, basically eta ki hoy, jokhn ekta network destroy hoye geche parr down hoye ache, kono dui ta network ke moddhe connection, tokhn amd je package eta khuste theke unno sob network ke giye giye, je kon network ke basically parta ache ekhon oh. toh, jehetu ekta e parchile bongchara destroyed hoy giyeche, toh or ei je ei mane search koro ta fechbe,

**BanglaASR13/seg_027.wav**

- reference: okay. so aa first-er-ta ami ektu solve kore dei. df-er value ei prottekgular khetre zero. because packetgulo as fragment hoitese, router porte parche je amar df-er value obviously zero deoya chhilo. jodi one deoya thakto, tahole aa packetgulo fragment hoto na. oikhane drop hoye jaito, and je sender chilo, tar kache eta message jaito je tumi fragment kore then amake pathao. right?
- base: okay so first it is to solve for a day dfa value is 0 because as fragment of the dfa value obviously 0 is also the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one
- tuned: okay, so aa first er ta ami ekta solve kore dei, dfer value etar porod te gula khektai zero, because bager gula as fragment hoy dese se ra otar korte parse ta amr dfer value obviously zero deya osilu, jiji one dewa ala thakto, tahole aa peaker gula fragment hortone, okhane drop away jaitah, and je sender chila, tar kase je message jaito je, je tumi fragment kore deyna amake partah.

**BanglaASR12/seg_005.wav**

- reference: tomader oi router ekta hocche acknowledgment dey. jokhon hocche je three way handshaking amra boli, ekta acknowledgment dey je tumi etotuku byte, oi je for example ager moto ponero-sho byte, tumi amare pathaite parba. er beshi dile ami nite parbo na. so aa because ei side hocche router-ta ache, tar hocche tomar ekta aa buffer ache je buffer-e basically message-ta rakhte pare ba je packet aa packet-ta ashe sheta rakhte pare.
- base: so, because inside the router is the best way to get the router, you can get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router
- tuned: so, because, ei side o je router ta ache, taro hocche tomar ekta buffer ache, je buffer a basically message ta rakhte pare, baar je ek packet ta ashe shera rakhte pare.

**BanglaASR13/seg_009.wav**

- reference: to amader exam-e onek shomoy ektu wording-er mane aa patch dey sir-ra, sheta hocche jemon packet size-ta. packet size bole, total packet size-ta eto. onek shomoy packet size na bole bole je hocche data size-ta eto. toh tomar tokhon question-ta pore bujhte hobe. je tomar je packet-ta ache sheta ki including the header or just the data. thik ache? eita eita onek shomoy ekta tricks amra dekhte pai porikkhar question-er wording gulate.
- base: so, we have to patch the exam and we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size
- tuned: so amader exami onek shoma er wording er patch deya chara, sheta hoche e jemon packet size ta, packet size bole, total packet size ta ato. onesho be packet size na bole bole je hocche data size ta ato. so tomar tofn question ta pore busthabe, je tomar je packet ta asa sheta ki including the header or just the data, thikache?
