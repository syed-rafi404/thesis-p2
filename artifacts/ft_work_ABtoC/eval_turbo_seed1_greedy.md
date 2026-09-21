# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_ABtoC\lora_turbo_seed1`
Split: `test.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.6% | 79.8% |
| WER, per clip mean | 109.7% | 168.1% |
| WER, whole split | 93.0% | 80.0% |
| CER, per clip median | 74.2% | 54.0% |
| CER, per clip mean | 85.1% | 116.5% |
| Term recall | 64.3% | 69.8% |
| Term precision | 84.7% | 66.7% |
| Term F1 | 73.1% | 68.2% |
| Clips that run away | 6 of 75 | 3 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 63 of 75 clips. Wilcoxon signed-rank p = 4.93e-07, sign test p = 1.69e-09.
- **CER**: fine-tune wins on 67 of 75 clips. Wilcoxon signed-rank p = 6.30e-09, sign test p = 1.01e-12.

Paired test on the mean per-clip WER, for reference: p = 0.5336 (sign-flip Monte Carlo, n=74, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR13/seg_029.wav**

- reference: mf-er value zero hobe kokhon? jokhon amra last fragment paya jabo. tahole ekhetre amader last fragment three number na? tahole ekhane mf-er flag-ta hobe zero. je er mane bujhay er pore ar kono fragment nai.
- base: the last fragment is 0, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last fragment, so we have the last
- tuned: je, er mane bujhe, er pore ar kono fragment nai. so, amra first a fragment ta ache bata chai, amra first a fragment a ache.

**BanglaASR10/seg_005.wav**

- reference: looping. okay. so basically eta ki hoy je jokhon ekta network destroy hoye geche ba down hoye ache, kono duita network er moddhe connection, tokhon loop amader je packet, eta khujte thake onno shob network e giye giye je kon network e basically path ta ache ekhono. toh jehetu ektai path chilo ebong sheita destroyed hoye giyeche.
- base: looping okay so basically it is key when the network is destroyed and downed and there is a connection between the network and the network is very happy that they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they are all connected to the network and they
- tuned: so, basically eta ki hoy je jokhn ekta network destroy hoye geche bar down hoye ache, kono dui etar network ke moddhe connection. takhon loop ta amr je packet eto khuste thake onno shob network ki ki hoye je kon network ke basically parta ache ekhono.

**BanglaASR13/seg_027.wav**

- reference: okay. so aa first-er-ta ami ektu solve kore dei. df-er value ei prottekgular khetre zero. because packetgulo as fragment hoitese, router porte parche je amar df-er value obviously zero deoya chhilo. jodi one deoya thakto, tahole aa packetgulo fragment hoto na. oikhane drop hoye jaito, and je sender chilo, tar kache eta message jaito je tumi fragment kore then amake pathao. right?
- base: okay so first it is to solve for a day dfa value is 0 because as fragment of the dfa value obviously 0 is also the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one is the one
- tuned: okay. so aa frustrate er amake to solve for e dei. df er value etar prorte gula kheta is zero. because begat gula as fragment thoi dise round ar korte parse deyam ar df er value obviously zero dey ausschilo.

**BanglaASR12/seg_005.wav**

- reference: tomader oi router ekta hocche acknowledgment dey. jokhon hocche je three way handshaking amra boli, ekta acknowledgment dey je tumi etotuku byte, oi je for example ager moto ponero-sho byte, tumi amare pathaite parba. er beshi dile ami nite parbo na. so aa because ei side hocche router-ta ache, tar hocche tomar ekta aa buffer ache je buffer-e basically message-ta rakhte pare ba je packet aa packet-ta ashe sheta rakhte pare.
- base: so, because inside the router is the best way to get the router, you can get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router to get the router
- tuned: so, ei side e ache route ta ache, taro hocche tomar ekta buffer ache, je buffer er basically message ta rakhte pare, but ei packet ta ashesh era rakhte pare.

**BanglaASR13/seg_009.wav**

- reference: to amader exam-e onek shomoy ektu wording-er mane aa patch dey sir-ra, sheta hocche jemon packet size-ta. packet size bole, total packet size-ta eto. onek shomoy packet size na bole bole je hocche data size-ta eto. toh tomar tokhon question-ta pore bujhte hobe. je tomar je packet-ta ache sheta ki including the header or just the data. thik ache? eita eita onek shomoy ekta tricks amra dekhte pai porikkhar question-er wording gulate.
- base: so, we have to patch the exam and we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size. we have to patch the packet size
- tuned: so amader exam e onekshomai ekta wording er patch deya sar na, sheita hocche je bon packet size ta, packet size bolle katol packet se stati, onekshom e packet size na bole bole je hocche data size ta eto. tu tomar pekhan question ta pore busth hbe, je tomar je packet ta asashe ta including the header or just the data, thikache?
