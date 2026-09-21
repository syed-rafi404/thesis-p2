# Digital Logic Design

In this lecture, we cover the fundamental concepts of digital logic design, focusing on universal gates: NOR, NAND, XOR, and XNOR gates.

## Key takeaways
- NOR gate is a universal gate.
- NAND gate is another universal gate.
- XOR gate is an exclusive OR gate.
- XNOR gate is the inverse of XOR gate.
- A NOR gate produces an output of 1 only when both inputs are 0.

## Universal Gates
### NOR Gate
- **Core Idea:** A NOR gate is a universal gate that outputs 1 only when both inputs are 0.
- **Example:**
  - Inputs: A = 0, B = 0
  - Output: 1
  - Inputs: A = 0, B = 1
  - Output: 0
  - Inputs: A = 1, B = 0
  - Output: 0
  - Inputs: A = 1, B = 1
  - Output: 0
![Board 0:00-0:50](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed from 6 video frames with the lecturer removed; 95% of the board is unobstructed.*
- **Watch out:** The output of a NOR gate is the inverse of the OR gate.

### NAND Gate
- **Core Idea:** A NAND gate is another universal gate that outputs 0 only when both inputs are 1.
- **Example:**
  - Inputs: A = 0, B = 0
  - Output: 1
  - Inputs: A = 0, B = 1
  - Output: 1
  - Inputs: A = 1, B = 0
  - Output: 1
  - Inputs: A = 1, B = 1
  - Output: 0
![Board 1:00-4:20](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:00–4:20, reconstructed from 9 video frames with the lecturer removed; 100% of the board is unobstructed.*

### XOR Gate
- **Core Idea:** An XOR gate outputs 1 when the inputs are different and 0 when the inputs are the same.
- **Example:**
  - Inputs: A = 0, B = 0
  - Output: 0
  - Inputs: A = 0, B = 1
  - Output: 1
  - Inputs: A = 1, B = 0
  - Output: 1
  - Inputs: A = 1, B = 1
  - Output: 0
![Board 4:40-7:00](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 4:40–7:00, reconstructed from 6 video frames with the lecturer removed; 100% of the board is unobstructed.*

### XNOR Gate
- **Core Idea:** An XNOR gate is the inverse of the XOR gate, outputting 1 when the inputs are the same and 0 when the inputs are different.
- **Example:**
  - Inputs: A = 0, B = 0
  - Output: 1
  - Inputs: A = 0, B = 1
  - Output: 0
  - Inputs: A = 1, B = 0
  - Output: 0
  - Inputs: A = 1, B = 1
  - Output: 1
![Board 7:20-10:40](figures_board/board_04_era4.jpg)

*Figure 4. The whiteboard during 7:20–10:40, reconstructed from 4 video frames with the lecturer removed; 100% of the board is unobstructed.*

## Check Yourself
1. What is the output of a NOR gate when both inputs are 1?
2. How many possible input combinations are there for a NAND gate?
3. What is the output of an XOR gate when both inputs are 1?
4. What is the output of an XNOR gate when both inputs are 0?
5. Which gate outputs 1 only when both inputs are 0?

## Answers
1. The output of a NOR gate when both inputs are 1 is 0.
2. There are four possible input combinations for a NAND gate.
3. The output of an XOR gate when both inputs are 1 is 0.
4. The output of an XNOR gate when both inputs are 0 is 1.
5. A NOR gate outputs 1 only when both inputs are 0.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*