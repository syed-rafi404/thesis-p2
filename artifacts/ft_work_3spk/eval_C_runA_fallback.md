# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 2, tuned 10 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.0% | 80.7% |
| WER, per clip mean | 90.2% | 83.9% |
| WER, whole split | 91.1% | 77.3% |
| CER, per clip median | 68.4% | 46.4% |
| CER, per clip mean | 70.8% | 49.2% |
| Term recall | 65.9% | 76.7% |
| Term precision | 79.4% | 95.2% |
| Term F1 | 72.0% | 85.0% |
| Clips that run away | 0 of 75 | 1 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 53 of 75 clips. Wilcoxon signed-rank p = 2.73e-04, sign test p = 4.50e-04.
- **CER**: fine-tune wins on 63 of 75 clips. Wilcoxon signed-rank p = 2.84e-09, sign test p = 1.69e-09.

Paired test on the mean per-clip WER, for reference: p = 0.0240 (sign-flip Monte Carlo, n=73, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR11/seg_000.wav**

- reference: so sorry for the interruption, guys. toh amra hocche jeikhan theke skip korechilam, amra oikhan theke continue korbo. toh basically, amra jeta bolchilam je don't fragment jeta ache. don't fragment er jodi value ta zero set kora thake, tar mane router er kache permission ache packet tare fragment kore onnanno router e pathanor, right? kintu jodi don't fragment er value ta 1 thake, router ar packet re fragment korte parbe na. packet-ta.
- base: sorry for the interruption guys.
- tuned: so sorry for the interruption guys. toh amra hocche jekhane teke skip kore chelo amra ekhane teke continue korbo. so basically amra jeta bolchilam je don't fragment jeta ase, don't fragment keer ma, jodi value ta zero set kora thake. tar ma ne router er kache par mission a ache, packet a re fragment kore, urnno na router er pathar na. right jodi don't fragment a value ta one thake, router er packet ake fragment korte pare bena.

**BanglaASR10/seg_003.wav**

- reference: toh ei je destroy korar je technique ta ba method ta, eitake amra hocche set kori ttl diye. ttl bolte gele je etogula hop, hop bolte ekhane bujhachchi apnar router ba pc. toh etogula router-to-router jump er poreo jodi o destination theke kono acknowledgment na ashe, tahole amra aa packet ta ke destroy kore notun packet pathabo.
- base: the destroyer technique is set up by ttl. ttl says that the hop is the router or pc. if the router jumps from the destination and doesn't know the destination, then we destroy the packet or send it.
- tuned: toh ki je destroy corer je technique te ba map er te eta ke amra hocche set kori ttl diye. ttl bolte kele je etugula hop, hop bolte kane bujhachi abna router ba pc. etugula router to router jump er pore o jodi o destination theke ekon orojmer naase, tahole amra packet ta ke destroy kore nothub packet paddhobon.

**BanglaASR10/seg_010.wav**

- reference: ar df flag ta jeta ache seta hocche don't fragment. don't fragment flag ta thakle ki hoy? amra toh ekta concept, aa mane, common sense diye chinta korleo pari je jokhon duita network amader exist kore, ba duita network bolte ki ar ki, multiple network bujhachchi ami. jokhon multiple network amader exist kore, tokhon amra ki kori je eigular moddhe je, for example, copper wire use kori,
- base: the associated flag is called don't fragment. don't fragment the flag. we can think of a concept or a common sense. for example, when two networks exist, or when two networks exist, we can use copper wire.
- tuned: dont fragment. don't fragment ne flag ta thakle ki hoy. amra toh ekta concept ami common sense diye chinta korlo pari je, jokhn duitar network amader exist kore, duitar network bolte kiya ki multiple network bujhacche. jekon multiple network amader exist kore, kokhn amra ki kori? je eigular moddhe, ea je for example copper wire use kori, onar ebong

**BanglaASR13/seg_014.wav**

- reference: toh ami jehetu ponero-sho byte ekhane likhechi, tar mane ekhane amar data size-ta chouddo-sho ashi byte. ar jehetu bole diyechilam aage bish byte data, toh ami plus bish.
- base: i have written it for 15 years and my data size is 1480 bytes and if i have given the data size to 20 bytes, then i will give it to 20 bytes
- tuned: tomra ekhane amr data size ta chudhoso ashibai. ari jeti bole diacchi le maake 20 byte data to ami plus 20.

**BanglaASR10/seg_011.wav**

- reference: onnyanno onek type er wire amra use korte pari for connections. ekhon shob wire ba shob je connection, bakider to capability same na. for example, amra jodi optical fiber use kori, eita long range er khetre onek beshi capable. but amra short range e toh ar optical fiber use kori na, tokhon copper wire use kora hoy. oneke bole copper straight through je coppergula, cablegula, sorry. toh eigula amader basically ekta device theke onno device e connection er jonno toiri kora. for example, router to router, pc to pc.
- base: for example, we use the long range of the optical fiber.
- tuned: ekhon shob wire ba shob je connection pathe sedh. toh capability same na. for example amra je optical fiber use kore, ej long range er khetre only bg kbeber bbore. but amra short range eite or optical fiber use kore, naatokhn copper wire use kore hoy. onek ke bole copper straight through kore je cover bula, cable gula sorry. toh ei gula amader basically, ekta device tikol, device a connection er jorn na toi kore.
