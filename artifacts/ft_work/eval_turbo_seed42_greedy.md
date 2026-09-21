# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_turbo_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 93.8% | 82.8% |
| WER, per clip mean | 111.9% | 133.1% |
| WER, whole split | 92.0% | 92.8% |
| CER, per clip median | 70.0% | 61.4% |
| CER, per clip mean | 80.7% | 99.7% |
| Term recall | 88.3% | 87.2% |
| Term precision | 60.0% | 74.2% |
| Term F1 | 71.5% | 80.2% |
| Clips that run away | 12 of 184 | 26 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 116 of 184 clips. Wilcoxon signed-rank p = 5.10e-03, sign test p = 4.97e-04.
- **CER**: fine-tune wins on 111 of 184 clips. Wilcoxon signed-rank p = 1.45e-02, sign test p = 6.22e-03.

Paired test on the mean per-clip WER, for reference: p = 0.1594 (sign-flip Monte Carlo, n=173, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_043.wav**

- reference: now, a and b, x-nor gate er amra logical circuit ta dekhchi. toh x-or gate aage akbo. x-or gate akar pore ami ekta not gate evabe apply kore dibo. tahole ami peye jabo x-nor gate.
- base: x not gate is, i am logical circuit to see x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate is a good x or gate
- tuned: so, x nor gate er amra logical circuit ta dekchi. so, x or gate age agbo, x or gate akar pore ami ekta not gate ebhabe apply kache.

**BanglaASR8/seg_022.wav**

- reference: so eitai hocche query language er kaj. so mysql e ami first e eije table ta, ei table tao toh kono bhabe create kora hoyeche, right? so eitao kintu query er maddhomei create kora hoy.
- base: result a output is a bit different so it is a query language so mysql is first a is a table that a table that is create a table that is a table that is a table that is create a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a table that is a
- tuned: so, my squb a l or ami first a ei jitei table ta, ei table teo toh kono bhabe create kora hoyeche, right? so, etau kintu query er my language er kache.

**BanglaASR6/seg_031.wav**

- reference: so eita hocche one kind of analogy. ekhon and gate er jodi ami logic circuit ta dekhi, logic circuit ta dekhte kirokom hoy. and gate ki hocche? duita input jacche. duita input er ei device ta ami kivabe aa visualize kori.
- base: so, this is one kind of analogy. now, i will see the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic side of the logic
- tuned: so, eta hocche one kind of analogy. ekhn and get er jodi ami logic sar kita dekhi, logic sar kita dekhte ki rokhom hoy? and get er ki hocche? dui ta input jakche, dui ta input er ei device taake ami ki bhabe visualize korte pari.

**BanglaASR6/seg_036.wav**

- reference: suppose input ta hocche a and output ta hocche b and amar output jeta ber hobe sheta hocche x. ekhon jodi ami similarly ekta table draw kori a, b as a input and a x output.
- base: so, output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so, the output is not available. so
- tuned: so amar output jeta der hobe jeta hocche x. akhn ami jodi similarly ta table draw kori, a b aje input r hocche a x output. tahole zeros and ones diye ami a and b er kichu ki hobe?

**BanglaASR9/seg_042.wav**

- reference: kintu ei student id er cgpa ki eita? na kintu. ei student er cgpa hocche eta. 3.98 je hold kore ache sheta hocche 110112. tahole eta kintu amake ekta wrong output dilo. so eitar jonno amake ektu onno bhabe approach nite hobe.
- base: cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student cgp is a student
- tuned: eta o thikache. kintu? ei student i ger cgpa ki eta? naa kintu. ei student er cgpa hocche? eta. 3.9 er je whole kora ache, se hoche one one zero, one one two. ta hole eta kintu amar ke ekta wrong output dilon. so, ei tar jonno ama ke ektu onno bhabe ar proshche hobe.
