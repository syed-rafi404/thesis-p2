# Board transcription (clean)

## Board 0:00-0:50

Digital Logic Design

Universal gate → NOR gate
→ NAND gate

## Board 1:00-4:20

Digital Logic Design

NOR gate

| A | B | A+B | $\overline{A+B} = X$ |
|---|---|-----|----------------------|
| 0 | 0 | 0   | 1                   |
| 0 | 1 | 1   | 0                   |
| 1 | 0 | 1   | 0                   |
| 1 | 1 | 1   | 0                   |

OR + NOT = NOR

Gate diagram: inputs A, B into a box labelled NOR, output $\overline{A+B}$

## Board 4:40-7:00

Digital Logic Design

NAND gate = AND + NOT

| A | B | AB | NOT(AB) |
|---|---|----|---------|
| 0 | 0 | 0  | 1       |
| 0 | 1 | 0  | 1       |
| 1 | 0 | 0  | 1       |
| 1 | 1 | 1  | 0       |

Gate diagram: inputs A, B into a box labelled NAND, output NOT(AB)

Gate diagram: inputs A, B into a box labelled NAND, output NOT(AB)

## Board 7:20-10:40

Digital Logic Design

X-OR gate:

| A | B | Output |
|---|---|--------|
| 0 | 0 |   0    |
| 0 | 1 |   1    |
| 1 | 0 |   1    |
| 1 | 1 |   0    |

same input = 0  
different input = 1  

A → X-OR → A ⊕ B  
B →  

A → ∧ → A ⊕ B  
B →

## Board 10:50-14:00

Digital Logic Design

X-NOR gate:
| A | B | A⊕B | A⊕B |
|---|---|-----|-----|
| 0 | 0 |   0 |   1 |
| 0 | 1 |   1 |   0 |
| 1 | 0 |   1 |   0 |
| 1 | 1 |   0 |   1 |

X-OR+NOT

A ── X-NOR ── A⊕B
B

A ── XOR ── A⊕B
B

X-NOR → A⊕B + AB
