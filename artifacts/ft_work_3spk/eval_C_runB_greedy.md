# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run_seed1`
Split: `test_C.jsonl`, clips scored: 75

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.0% | 86.2% |
| WER, per clip mean | 90.2% | 108.5% |
| WER, whole split | 91.1% | 89.9% |
| CER, per clip median | 68.6% | 49.9% |
| CER, per clip mean | 72.0% | 68.9% |
| Term recall | 68.2% | 68.2% |
| Term precision | 80.0% | 92.6% |
| Term F1 | 73.6% | 78.6% |
| Clips that run away | 0 of 75 | 8 of 75 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 47 of 75 clips. Wilcoxon signed-rank p = 4.90e-01, sign test p = 3.70e-02.
- **CER**: fine-tune wins on 56 of 75 clips. Wilcoxon signed-rank p = 4.93e-03, sign test p = 2.24e-05.

Paired test on the mean per-clip WER, for reference: p = 0.0338 (sign-flip Monte Carlo, n=73, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR13/seg_014.wav**

- reference: toh ami jehetu ponero-sho byte ekhane likhechi, tar mane ekhane amar data size-ta chouddo-sho ashi byte. ar jehetu bole diyechilam aage bish byte data, toh ami plus bish.
- base: i have written it for 15 years and my data size is 1480 bytes and if i have given the data size to 20 bytes, then i will give it to 20 bytes
- tuned: khoro amra ekhane amr data size ta chudhoso ashibai. aari jeti bole diachi lam aake bish by data to ami plus bish.

**BanglaASR10/seg_003.wav**

- reference: toh ei je destroy korar je technique ta ba method ta, eitake amra hocche set kori ttl diye. ttl bolte gele je etogula hop, hop bolte ekhane bujhachchi apnar router ba pc. toh etogula router-to-router jump er poreo jodi o destination theke kono acknowledgment na ashe, tahole amra aa packet ta ke destroy kore notun packet pathabo.
- base: the destroyer technique is set up by ttl. ttl says that the hop is the router or pc. if the router jumps from the destination and doesn't know the destination, then we destroy the packet or send it.
- tuned: tote ki je destroy corer je technique te ba method ta eta ke amra hocche set kori ttl dia, ttl bolte kele je eitugula hop, hop bolte kane bujhachi abne router er ba pc. eitugula router to router jump er pore hoj jodi o destination theke gong acknowledgement naache, tahole amra packet taake destroy kore nothu packet padhabe.

**BanglaASR10/seg_010.wav**

- reference: ar df flag ta jeta ache seta hocche don't fragment. don't fragment flag ta thakle ki hoy? amra toh ekta concept, aa mane, common sense diye chinta korleo pari je jokhon duita network amader exist kore, ba duita network bolte ki ar ki, multiple network bujhachchi ami. jokhon multiple network amader exist kore, tokhon amra ki kori je eigular moddhe je, for example, copper wire use kori,
- base: the associated flag is called don't fragment. don't fragment the flag. we can think of a concept or a common sense. for example, when two networks exist, or when two networks exist, we can use copper wire.
- tuned: so, ekta jeta ki je, jeta hote jeta jeta jeta hote don't fragment. don't fragment flag ta thakle ki hoy? amra toh ekta concept ami common sense diye chinta korle pari je, jokhn duitar network amader exist kore, ba duitar network bolte kiya ki multiple network bujhachche, jokhn multiple network amader exist kore, kohona ki kori?

**BanglaASR10/seg_017.wav**

- reference: but router ki kore, always shortest path-tai ney. toh eibhabe amader ekta router hocche fragment kore thake. ekhon jodi don't fragment factor zero deya thake, tokhoni shudhumatro router ei fragmentation ta korte parbe. jodi non-fragment zero na thake, for example jodi 1 thake, tar mane ki je router er kache shei permission nai, etake fragment korar.
- base: always short is path is not there. so, in this way, we will fragment a router. now, if the don't fragment is 0, then the router will be able to fragment it. if the don't fragment is 0, for example, if it is 1, then i will not have the shape i mission.
- tuned: toh ei babe amote ekta router hocche fragment kore thake. ekhon, jodi don't fragment factor zero thee o theke, dokhn e sudhu matro router ei fragment ashbhe korte parbe. jodi don't fragment zero na theke, for example jodi one theke, thar mane ki je router er kaste shape iar mission nai eta ke fragment kora.

**BanglaASR13/seg_029.wav**

- reference: mf-er value zero hobe kokhon? jokhon amra last fragment paya jabo. tahole ekhetre amader last fragment three number na? tahole ekhane mf-er flag-ta hobe zero. je er mane bujhay er pore ar kono fragment nai.
- base: we will get the last fragment, here we have the last fragment 3 but here we have the last fragment 0 which means there is no fragment after this
- tuned: amra last fragment aje bo tade, ekhate amra last fragment 3 number na, thon likhn emr reflect ashobe, zero. je er mane bujai, er por e ar kono fragment nai.
