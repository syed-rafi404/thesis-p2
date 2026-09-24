# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `F:\thesisP2\ft_work_final5h_lr1e3\lora_lr1e3`
Split: `test.jsonl`, clips scored: 177

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 19, tuned 6 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.3% | 42.3% |
| WER, per clip mean | 91.1% | 47.6% |
| WER, whole split | 85.6% | 40.7% |
| CER, per clip median | 67.0% | 15.8% |
| CER, per clip mean | 68.5% | 24.8% |
| Term recall | 66.9% | 93.9% |
| Term precision | 83.9% | 89.9% |
| Term F1 | 74.4% | 91.9% |
| Clips that run away | 0 of 177 | 0 of 177 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 171 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 4.24e-43.
- **CER**: fine-tune wins on 168 of 177 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 4.21e-39.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=177, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR11/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. eta gailo amal or get completed.
- tuned: eita gelo amar or gate completed.

**BanglaASR9/seg_002.wav**

- reference: toh amra cholo shobar aage ekta dekhe nei, ekta struct-er kibhabe, jemon dhoro ekta struct jodi hoy, struct x, right? etar moddhe amra ki rakhte pari? integer rakhte pari, int aa age. aa tarpor amra character rakhte pari, right?
- base: so let's see the structs. what is struct? integer, age, and character.
- tuned: toh amra cholo shobar aage ekta dekhen ekta struct er kivabe? jemon dhoro ekta struct jodi hoy, struct x, right? etar moddhe amra ki rakhte pari? integer rakhte pari. int aa age. aa tarpor amra character rakhte pari, right?

**BanglaASR9/seg_040.wav**

- reference: t7-er moddhei kintu ami eventually final address-ta peye jabo. toh eita ar = 27, eta kintu basically same jinish-i bujhacche. toh ebhabe amra ashole oop-er moddhe method-er calculation-gulo kore thaki. thank you.
- base: right, t7 are the first time, but eventually, we will pay the final address. so, eta is equal to 27. basically, we have sent g. so, we will give you the first time of the method of calculation. thank you.
- tuned: t7-er moddhe kintu ami eventually final address-ta pay jabo. toh eta ar equal to 27. eta kintu basically sen ginishi bujhacche. toh ebhabe amra ashole o-pir moddhe method-er calculation gula kore thake. thank you.

**BanglaASR9/seg_007.wav**

- reference: stack pointer ache. toh ekhan theke ki amra nicheo jete pari, uporeo jete pari. ei calculation gulo hoy holo offset-er maddhome. offset ki? jemon dhoro, ekhane ami dhorlam age variable-ta ekhane ache, right? ekhon age-er niche amar name ache.
- base: step pointer. so, this is the one that we have to go down and go up. this calculation is offset. offset is that, when we have to go down to the edge variable, we have to go down to the edge.
- tuned: stack point-er ache. toh ekhane diye ki amra niche ojete pari, upore ojete pari. ei calculation gula hoy holo offset-er maddhora. offset ki? jemon dhoro ekhane ami dhorlam age variable-ta ekhane ache, right? ekhon age-er niche amar name ache.

**BanglaASR9/seg_027.wav**

- reference: result koto? result-er age ekta 4 ache. tahole eta koto amar? 4. right? ekhane kintu ami offset na, etar object. eitar width-ta kotokhani? mane kotokhani par hoye ashtese? koto? 4 par hocche. tahole ki abar 4 add korlam?
- base: 4
- tuned: result koto? result-ta age ekta 4 ache. tahole eta koto amar? 4. right? ekhane kintu ami offset na. etar ob-er, etar width-ta kotokhani, mane kotokhani par hoye ashtese koto? 4 par hocche. tahole ki abar 4 hoye ashtese?
