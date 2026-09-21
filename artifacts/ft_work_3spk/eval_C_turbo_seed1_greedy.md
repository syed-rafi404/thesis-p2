# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed1`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.6% | 79.5% |
| WER, per clip mean | 109.7% | 100.5% |
| WER, whole split | 93.0% | 84.0% |
| CER, per clip median | 74.2% | 46.7% |
| CER, per clip mean | 85.1% | 65.0% |
| Term recall | 64.3% | 60.5% |
| Term precision | 84.7% | 100.0% |
| Term F1 | 73.1% | 75.4% |
| Clips that run away | 6 of 75 | 5 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 56 of 75 clips. Wilcoxon signed-rank p = 3.94e-05, sign test p = 2.24e-05.
- **CER**: fine-tune wins on 65 of 75 clips. Wilcoxon signed-rank p = 1.50e-07, sign test p = 5.15e-11.

Paired test on the mean per-clip WER, for reference: p = 0.5038 (sign-flip Monte Carlo, n=71, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR13/seg_029.wav**

- reference: mf-er value zero hobe kokhon? jokhon amra last fragment paya jabo. tahole ekhetre amader last fragment three number na? tahole ekhane mf-er flag-ta hobe zero. je er mane bujhay er pore ar kono fragment nai.
- base: the last fragment is 0, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last
- tuned: je er mane bujhai er pore r kono fragment nai. toh amra ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane ekhane.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: okay, so, basically eta ki hoy, je jokhn ekta network destroy hoye geche bar down hoye ache, kono dui eta network ke moddhe connection, tokhn amoddhe je package eto khuste theke onno sob network ke diye giye, je kon network ke basically, parta ache ekhono. toh jehetu ekta e parchile ebong jeta destroyed hoye giyeche, toh or ei je ei, mine, search korot a achi naah,

**BanglaASR13/seg_027.wav**

- reference: okay. so aa first-er-ta ami ektu solve kore dei. df-er value ei prottekgular khetre zero. because packetgulo as fragment hoitese, router porte parche je amar df-er value obviously zero deoya chhilo. jodi one deoya thakto, tahole aa packetgulo fragment hoto na. oikhane drop hoye jaito, and je sender chilo, tar kache eta message jaito je tumi fragment kore then amake pathao. right?
- base: okay so first it is to solve for a day dfa value is 0 because as fragment of the dfa value obviously 0 is also the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one
- tuned: okay, so aa first er tar ami ekta solve kore dei, dfer value etar porottek gula khehta ish zero, because paket gula as fragment hoy deseche raotar korte parse thar amr dfer value obviously zero dey also jilu, di one dey wala thakto, tahole aa paket gula fragment hortona, okhane drop hoye jaitah, and je sender chula tarak asete message jaita, je tumi fragment kore dena amake pardhane.

**BanglaASR12/seg_005.wav**

- reference: tomader oi router ekta hocche acknowledgment dey. jokhon hocche je three way handshaking amra boli, ekta acknowledgment dey je tumi etotuku byte, oi je for example ager moto ponero-sho byte, tumi amare pathaite parba. er beshi dile ami nite parbo na. so aa because ei side hocche router-ta ache, tar hocche tomar ekta aa buffer ache je buffer-e basically message-ta rakhte pare ba je packet aa packet-ta ashe sheta rakhte pare.
- base: so, because inside the router is the best way to get the router, you can get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router
- tuned: so, because aa ei side hoche router ta ache taro hocche tomar ekta buffer ache, je buffer a basically message ta rakhte pare, baar je packet ta ashe rakhte pare.

**BanglaASR13/seg_009.wav**

- reference: to amader exam-e onek shomoy ektu wording-er mane aa patch dey sir-ra, sheta hocche jemon packet size-ta. packet size bole, total packet size-ta eto. onek shomoy packet size na bole bole je hocche data size-ta eto. toh tomar tokhon question-ta pore bujhte hobe. je tomar je packet-ta ache sheta ki including the header or just the data. thik ache? eita eita onek shomoy ekta tricks amra dekhte pai porikkhar question-er wording gulate.
- base: so, we have to patch the exam and we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size
- tuned: toh amr ekta data size ta ato, so amader exam e onne shoma eto wording er patch dei sarra, seta hoche e je bon package size ta, packet size ta ato. onne shume packet size na bole bole je hocche data size ta ato. tu tomar pabon question ta pore busthabe, je tomar je packet ta asha seta ki including the header or just the data, thikache?
