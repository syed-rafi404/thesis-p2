# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_BCtoA\lora_turbo_seed1`
Split: `test.jsonl`, clips scored: 172

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 97.5% | 75.8% |
| WER, per clip mean | 122.8% | 84.5% |
| WER, whole split | 97.6% | 56.9% |
| CER, per clip median | 74.2% | 49.9% |
| CER, per clip mean | 90.6% | 58.0% |
| Term recall | 70.4% | 86.8% |
| Term precision | 40.9% | 98.8% |
| Term F1 | 51.7% | 92.4% |
| Clips that run away | 15 of 172 | 6 of 172 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 138 of 172 clips. Wilcoxon signed-rank p = 2.04e-14, sign test p = 4.61e-16.
- **CER**: fine-tune wins on 138 of 172 clips. Wilcoxon signed-rank p = 4.44e-16, sign test p = 4.61e-16.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=168, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR5/seg_024.wav**

- reference: ekhane ki hobe, tuple amake eta korte dibenah. ekhane ekta restriction ache, tuple holo immutable. so user chailei jinish ta change korte parenah. eta amake directly error dibe.
- base: so user i-lay change this directly error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error error
- tuned: ekhon ekta restriction ache, tapal holo immutable, so user ally jinishta change korte pare na. eta amake directly error dibe. error dibe. eta hobe na. eijonno amake ki koto hobe? first e amake ekta korte dibe.

**BanglaASR2/seg_030.wav**

- reference: and ekhon jodi ami sum nei, and tahole ekhon jodi print kori, tahole amra dekhbo ki, ekhan theke dui ta integer value, dui ta first a string ashbe. ogulake amra integer a convert korsi, ebong sum korchi.
- base: and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this is what i am going to do and this
- tuned: and ekhon jodi ami sum name. and tahole ekhon jodi print kori. tahole amra dekhbo ki? print kori. tahole amra dekhbo ki? print kori.

**BanglaASR5/seg_025.wav**

- reference: error dibe, eta hobe naah. ejonno amake ki korte hobe, first a, ekta notun variable nia ni. element list naamer notun ekta variable nilam. ami korbo ki, ei element naamer je tuple ta, etaake ekta list a convert krbo.
- base: so, we will convert the element of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of list of
- tuned: element list nama notun ekta variable nilam. ami korbo ki? ei element nama je tuple ta, eta amra ekta list e convert korbo. so list of list nama.

**BanglaASR3/seg_008.wav**

- reference: tarpore jodi dekhe je rain, if block a dhuklo, print korbe se bring umbrella. ebong jodi weather jodi onno kichu dei, rain baade jekono jinish, jemon ki rain er jodi aa spelling ta se small letter dia o
- base: so user is input and input power is not weather rain check first if block is stuck then the range is stuck print bring umbrella weather is not a rain but the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the same kind of the
- tuned: so user ekta input dibe, eibon input power pore whether rain na ki, eta check korbe. first ei if block e duke jabe. tarpore jodi jekheche range, if block e thuklo, print korbeshe bring umbrella. eibon jodi weather jodi onno ki chhudai, rain ba je kono jinis. eibon ki rain er jodi aa spelling kache small letter deoya likhe, tobuo jinis te evabe jabe.

**BanglaASR1/seg_029.wav**

- reference: sheta holo standard rule jerokom dhoro name ta ke likhe amra shobai name likhi. name likhle hoy ki, dekho ekhane ami small letter diye shuru korechi. ebong evabei amar variable er name ta hoyeche. so eta cross eta holo right. okay?
- base: so this is the name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name name
- tuned: abobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobobob
