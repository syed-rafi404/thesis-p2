# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_turbo_AC_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.8% | 73.5% |
| WER, per clip mean | 111.9% | 91.1% |
| WER, whole split | 92.0% | 63.3% |
| CER, per clip median | 70.0% | 48.8% |
| CER, per clip mean | 80.7% | 67.9% |
| Term recall | 88.3% | 92.9% |
| Term precision | 60.0% | 65.4% |
| Term F1 | 71.5% | 76.8% |
| Clips that run away | 12 of 184 | 12 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 134 of 184 clips. Wilcoxon signed-rank p = 2.30e-11, sign test p = 4.72e-10.
- **CER**: fine-tune wins on 124 of 184 clips. Wilcoxon signed-rank p = 5.91e-09, sign test p = 2.74e-06.

Paired test on the mean per-clip WER, for reference: p = 0.0116 (sign-flip Monte Carlo, n=169, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_019.wav**

- reference: ekhon ami jodi abar etar jonno similar table create kori. okay. a, b amar duita input. so amar possible combination hocche 0 0, 0 1, 1 0 and 1 1. ekhon ami ki korchi first e?
- base: so, we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will see the same table as we will
- tuned: ekhon ami jodi abar etar jonno similar table create kori, okay. a b amar doita input. so amr possible combination hocche zero, zero, zero.

**BanglaASR7/seg_043.wav**

- reference: now, a and b, x-nor gate er amra logical circuit ta dekhchi. toh x-or gate aage akbo. x-or gate akar pore ami ekta not gate evabe apply kore dibo. tahole ami peye jabo x-nor gate.
- base: x not gate is, i am logical circuit to see x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate
- tuned: so x not gate er amra logical circuit ta dekhi. so x or gate aage akbo, x or gate akar pore ami ekta not gate ebabe apply kache.

**BanglaASR8/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so, mysql er, ami first a, ei je table ta. ei table ta auto kono bhabe create kora hoyeche, right? so, eta o kintu query er mann language ta.

**BanglaASR6/seg_031.wav**

- reference: so eita hocche one kind of analogy. ekhon and gate er jodi ami logic circuit ta dekhi, logic circuit ta dekhte kirokom hoy. and gate ki hocche? duita input jacche. duita input er ei device ta ami kivabe aa visualize kori.
- base: so, this is one kind of analogy. now, i will see the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic
- tuned: so eta hocche one kind of analogy. ekhon, and gate er jodi ami logic side kita dekhi, logic side kita dekhte ki rokom hoy. and gate er ki hocche? duita input jakche. duita input er ei device taake ami kivhabe aa visualize korte parche.

**BanglaASR6/seg_036.wav**

- reference: suppose input ta hocche a and output ta hocche b and amar output jeta ber hobe sheta hocche x. ekhon jodi ami similarly ekta table draw kori a, b as a input and a x output.
- base: so, output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so
- tuned: so amar output jeta ber hobe sheta hocche x. ekhon ami jodi similarly ta table draw kori, a b as a input ar hocche a x output. tahole, zeros and ones tiye ami a and b er kichu hobe?
