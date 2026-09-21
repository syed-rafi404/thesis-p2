# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.0% | 83.3% |
| WER, per clip mean | 90.2% | 100.4% |
| WER, whole split | 91.1% | 85.8% |
| CER, per clip median | 68.6% | 48.2% |
| CER, per clip mean | 72.0% | 61.2% |
| Term recall | 68.2% | 75.2% |
| Term precision | 80.0% | 59.1% |
| Term F1 | 73.6% | 66.2% |
| Clips that run away | 0 of 75 | 7 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 48 of 75 clips. Wilcoxon signed-rank p = 5.30e-02, sign test p = 2.03e-02.
- **CER**: fine-tune wins on 56 of 75 clips. Wilcoxon signed-rank p = 1.11e-04, sign test p = 2.24e-05.

Paired test on the mean per-clip WER, for reference: p = 0.1581 (sign-flip Monte Carlo, n=73, 20000 resamples).

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

**BanglaASR13/seg_014.wav**

- reference: toh ami jehetu ponero-sho byte ekhane likhechi, tar mane ekhane amar data size-ta chouddo-sho ashi byte. ar jehetu bole diyechilam aage bish byte data, toh ami plus bish.
- base: i have written it for 15 years and my data size is 1480 bytes and if i have given the data size to 20 bytes, then i will give it to 20 bytes
- tuned: tomra ekhane amr data size ta chudhoso ashibai. ari jeti bole diacchi le maake 20 byte data to ami plus 20.

**BanglaASR10/seg_011.wav**

- reference: onnyanno onek type er wire amra use korte pari for connections. ekhon shob wire ba shob je connection, bakider to capability same na. for example, amra jodi optical fiber use kori, eita long range er khetre onek beshi capable. but amra short range e toh ar optical fiber use kori na, tokhon copper wire use kora hoy. oneke bole copper straight through je coppergula, cablegula, sorry. toh eigula amader basically ekta device theke onno device e connection er jonno toiri kora. for example, router to router, pc to pc.
- base: for example, we use the long range of the optical fiber.
- tuned: ekhon shob wire ba shob je connection pathe sedh. toh capability same na. for example amra je optical fiber use kore, ej long range er khetre only bg kbeber bbore. but amra short range eite or optical fiber use kore, naatokhn copper wire use kore hoy. onek ke bole copper straight through kore je cover bula, cable gula sorry. toh ei gula amader basically, ekta device tikol, device a connection er jorn na toi kore.

**BanglaASR11/seg_004.wav**

- reference: toh porer packet-ta jabe ek hajar byte-e, packet three. toh eita hocche porer eita first er ponerosho byte, eita porer ponerosho byte, eita hocche ek jhajar byte, right? toh amar more fragment ki kore? more fragment bole dey je erpore ar ki kon fragment ashbe? jemon jodi ei case e chinta kori, ei je packet ta ami send korbo, ekhane header er field er moddhe more fragment e deoya thakbe one.
- base: the packet is 100 bytes, packet 3 so this is the first and 15 bytes this is 15 bytes this is 100 bytes so what i do more fragment, more fragment is said that after that any fragment will come if i do this, the packet i will send here is the header file more fragment will come
- tuned: so, ei deh hocche porer eta first er ponoroso byte, eta porer ponoroso byte, eta hocche eikhajar byte, right. toh amar more fragment ki kore? more fragment bole dei je, ei porer ar ki kono fragment asbe? jemon jodi ei kese kese chinta kori, ei je packet ta mi scene kor baikhnye, head er er file er moddhe, more fragment er deothakhbe one.
