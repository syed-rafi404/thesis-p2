# Digital Logic Design

One sentence: This lecture covers the introduction to digital logic design, focusing on universal gates: NOR, NAND, XOR, and XNOR.

## Key takeaways
- NOR gate is a universal gate.
- NAND gate is another universal gate.
- XOR gate produces an output of 1 when the inputs are different.
- XNOR gate produces an output of 1 when the inputs are the same.

## Universal Gates
### NOR Gate
The NOR gate is a universal gate that combines OR and NOT operations. It takes two inputs, A and B, and produces an output that is the inverse of the OR operation between A and B.

**Worked Example:**
| A | B | A+B | NOT(A+B) = X |
|---|---|-----|--------------|
| 0 | 0 |   0 |            1 |
| 0 | 1 |   1 |            0 |
| 1 | 0 |   1 |            0 |
| 1 | 1 |   1 |            0 |

Lecturer: OR + NOT = NOR  
Lecturer: A --- NOR --- A+B  
Lecturer: Gate diagram: inputs A, B into a box labelled NOR, output A+B

![Board 1:00-4:20](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:00–4:20, reconstructed from 9 video frames with the lecturer removed; 100% of the board is unobstructed.*

### NAND Gate
The NAND gate is a universal gate that combines AND and NOT operations. It takes two inputs, A and B, and produces an output that is the inverse of the AND operation between A and B.

**Worked Example:**
| A | B | AB | NOT(AB) |
|---|---|----|---------|
| 0 | 0 | 0  | 1       |
| 0 | 1 | 0  | 1       |
| 1 | 0 | 0  | 1       |
| 1 | 1 | 1  | 0       |

Lecturer: NAND gate = AND + NOT  
Lecturer: Gate diagram: inputs A, B into a box labelled NAND, output NOT(AB)

![Board 4:40-7:00](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 4:40–7:00, reconstructed from 6 video frames with the lecturer removed; 100% of the board is unobstructed.*

### XOR Gate
The XOR gate produces an output of 1 when the inputs are different. It takes two inputs, A and B, and produces an output based on the condition that the inputs are not the same.

**Worked Example:**
|   | 0 | 1 |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 1 | 0 |

Lecturer: A → X-OR → A⊕B  
Lecturer: B  
Lecturer: A → AND → A⊕B  
Lecturer: B  
Lecturer: same input = 0  
Lecturer: different input = 1

![Board 7:20-10:40](figures_board/board_04_era4.jpg)

*Figure 4. The whiteboard during 7:20–10:40, reconstructed from 4 video frames with the lecturer removed; 100% of the board is unobstructed.*

### XNOR Gate
The XNOR gate produces an output of 1 when the inputs are the same. It is the inverse of the XOR gate.

**Worked Example:**
| A | B | A⊕B | A⊕B |
|---|---|-----|-----|
| 0 | 0 |   0 |   1 |
| 0 | 1 |   1 |   0 |
| 1 | 0 |   1 |   0 |
| 1 | 1 |   0 |   1 |

Lecturer: X-OR + NOT  
Lecturer: A - X-NOR - A⊕B  
Lecturer: B  
Lecturer: X-NOR → A⊕B + AB

![Board 10:50-14:00](figures_board/board_05_era5.jpg)

*Figure 5. The whiteboard during 10:50–14:00, reconstructed from 9 video frames with the lecturer removed; 100% of the board is unobstructed.*

## Check Yourself
1. What is the output of a NOR gate when both inputs are 1?
2. How many possible input combinations are there for a NAND gate?
3. What is the output of an XOR gate when both inputs are 0?
4. What is the relationship between XNOR and XOR gates?
5. Draw the gate diagram for a NAND gate.

## Answers
1. The output of a NOR gate when both inputs are 1 is 0.
2. There are four possible input combinations for a NAND gate.
3. The output of an XOR gate when both inputs are 0 is 0.
4. XNOR is the inverse of XOR.
5. ![NAND Gate Diagram](https://example.com/nand_gate_diagram.png)

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*