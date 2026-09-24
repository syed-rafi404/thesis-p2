# Digital Logic Design
Today we will start with the concept of universal gates.

## Key takeaways
- Red Box 1 (Title: Digital Logic Design): This box introduces the topic of Digital Logic Design.
- The Universal Gate Concept: There are two types of universal gates, which are the XOR gate and the NAND gate.
- NOR Gate Introduction: The NOR gate is a combination of an OR gate followed by a NOT gate.
- Understanding Inputs and Outputs: We will see how to create inputs and outputs using these gates and understand how to construct logical circuits.
- Example with NOR Gate: The NOR gate is named as such because it involves an OR gate but with a negation. In the NOR gate, if both inputs are low (0), the output is high (1). If either or both inputs are high (1), the output is low (0).

---

<!-- boxes: 1=#d62828 -->
## Digital Logic Design

**In one line:** Today we will start with the concept of universal gates.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title


- **Red Box 1 (Title: Digital Logic Design)**: This box introduces the topic of Digital Logic Design. The lecturer mentioned that we have already covered fundamental gates in the previous class, and today we will focus on universal gates.

- **The Universal Gate Concept**: There are two types of universal gates, which are the XOR gate and the NAND gate. The lecturer emphasized that these gates can be used to implement any other type of logic gate.

- **NOR Gate Introduction**: The lecturer started with the NOR gate. The name "NOR" is kept to remember that it involves an OR gate but with a negation. Essentially, the NOR gate is a combination of an OR gate followed by a NOT gate.

- **Understanding Inputs and Outputs**: The lecturer explained that we will see how to create inputs and outputs using these gates and understand how to construct logical circuits.

- **Example with NOR Gate**: First, we will start with the NOR gate. The NOR gate is named as such because it involves an OR gate but with a negation. In the NOR gate, if both inputs are low (0), the output is high (1). If either or both inputs are high (1), the output is low (0).


**Background (not said in the lecture)**: A universal gate is a gate that can be used to implement any other type of logic gate. The NOR gate is one such universal gate. By understanding the NOR gate, we can build more complex circuits using just this single type of gate.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## NOR Gate: Digital Logic Design
**In one line:** This board explains how to build a NOR gate using basic logic operations.

![Board 2: 1:00-4:20](figures_annotated/board_era2_100.jpg)

*Figure 2. The whiteboard during 1:00–4:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 NOR gate · 3 Formula · 4 Truth table · 5 Gate symbol


1. **Red Box (Box 1):** The title "Digital Logic Design" introduces the topic.
2. **Blue Box (Box 2):** The NOR gate is introduced. It is explained that the NOR gate can be built using an OR operation followed by a NOT operation.
3. **Orange Box (Box 3):** The formula "OR + NOT = NOR" is shown, which is the basis for constructing the NOR gate.
4. **Green Box (Box 4):** The truth table for the NOR gate is displayed. It shows all possible combinations of inputs A and B and their corresponding outputs.
5. **Purple Box (Box 5):** The gate symbol for A NOR B is illustrated.

The lecturer explains that the NOR gate is essentially an OR gate followed by a NOT gate. Here’s a step-by-step breakdown:

- **Step 1:** Start with two inputs, A and B. The output is the result of the OR operation between A and B, followed by a NOT operation.
- **Step 2:** The truth table in Box 4 shows all possible combinations of A and B. For each combination, the output is determined by first performing the OR operation and then applying the NOT operation.
- **Step 3:** The OR operation between A and B results in 1 if either A or B is 1, and 0 otherwise. Then, the NOT operation inverts this result.
- **Step 4:** The output of the NOR gate is 1 only when both A and B are 0. In all other cases, the output is 0.


### Background (not said in the lecture) (lecture e bola hoy ni)
The NOR gate is a universal gate because any Boolean function can be implemented using only NOR gates. This makes it very versatile in digital circuit design. Understanding the NOR gate helps in building more complex circuits and simplifying logic designs.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Definition of NAND Gate: Digital Logic Design
**In one line:** NAND gate = AND + NOT

![Board 3: 4:40-7:00](figures_annotated/board_era3_440.jpg)

*Figure 3. The whiteboard during 4:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 NAND gate · 3 Definition · 4 Block diagram · 5 Truth table · 6 Gate symbol


- **Red Box 1 (Title):** Digital Logic Design
- **Blue Box 2 (NAND gate):** NAND gate
- **Orange Box 3 (Definition):** NAND gate = AND + NOT
- **Green Box 4 (Block diagram):** A ── NAND ── AB B ──
- **Purple Box 5 (Truth table):** 
  | A | B | AB | NOT(AB) |
  |---|---|----|---------|
  | 0 | 0 | 0  | 1       |
  | 0 | 1 | 0  | 1       |
  | 1 | 0 | 0  | 1       |
  | 1 | 1 | 1  | 0       |
- **Pink Box 6 (Gate symbol):** A ──┐ ── AB B ──└───

The lecturer said: "NAND gate = AND + NOT"

### Background (not said in the lecture) (lecture e bola hoy ni)
The NAND gate is a universal gate because it can be used to implement any other logic gate. By combining NAND gates, we can create complex circuits that perform various logical operations. This makes the NAND gate very versatile in digital logic design.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## X-OR Gate: Digital Logic Design
**In one line:** X-OR gate takes two inputs and produces one output.

![Board 4: 7:20-10:40](figures_annotated/board_era4_720.jpg)

*Figure 4. The whiteboard during 7:20–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Gate symbol · 4 Truth table · 5 Gate symbol · 6 Formula


- **Box 1 (red):** Digital Logic Design
- **Box 2 (blue):** Definition: X-OR gate
- **Box 4 (green):** Truth table
- **Box 5 (purple):** Gate symbol: A X-OR B
- **Box 6 (pink):** Formula: same input = 0, different input = 1

The lecturer said: "The X-OR gate takes two inputs, A and B, and produces an output based on these inputs. He used the example where if A is 0 and B is 0, the output is 0. Similarly, if A is 0 and B is 1, the output is 1. This pattern continues for the other combinations: when A is 1 and B is 0, the output is 1; and when A is 1 and B is 1, the output is 0. The lecturer summarized this with the formula: same input = 0, different input = 1."

The truth table for the X-OR gate is shown in Box 4 (green):

| A | B | Output |
|---|---|--------|
| 0 | 0 |   0    |
| 0 | 1 |   1    |
| 1 | 0 |   1    |
| 1 | 1 |   0    |

He also provided the gate symbol in Box 5 (purple):

A X-OR B

And the formula in Box 6 (pink):

same input = 0  
different input = 1  

The lecturer further said: "While we can derive the output step-by-step using the formula, for practical purposes, we can directly use the X-OR gate to get the output quickly. He mentioned that understanding the X-OR gate will make it easier to understand other similar gates like the X-NOR gate."

### Background (not said in the lecture) (lecture e bola hoy ni)
The X-OR gate is a fundamental component in digital logic design, and understanding its behavior helps in designing more complex circuits. Knowing how to derive the output from the inputs and vice versa is crucial for working with digital systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## X-NOR Gate: Digital Logic Design
**In one line:** X-NOR gate is derived from X-OR gate and NOT gate.

![Board 5: 10:50-14:00](figures_annotated/board_era5_1050.jpg)

*Figure 5. The whiteboard during 10:50–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Block diagram · 5 Formula


- **Box 1 (red):** Digital Logic Design
- **Box 2 (blue):** Truth table
  | A | B | A⊕B | A⊕B |
  |---|---|-----|-----|
  | 0 | 0 |   0 |   1 |
  | 0 | 1 |   1 |   0 |
  | 1 | 0 |   1 |   0 |
  | 1 | 1 |   0 |   1 |
- **Box 3 (orange):** Gate symbol
  A ── X-NOR ── A⊕B
  B
- **Box 4 (green):** Block diagram
  A ──┐ ── A⊕B
  B └───
- **Box 5 (purple):** Formula
  X-NOR → A⊕B + AB

The lecturer said: "X-NOR gate is derived from X-OR gate and NOT gate."

The lecturer explained that the X-NOR gate can be derived by first performing an X-OR operation and then applying a NOT operation. Let's break down the steps:

1. **Truth Table (Box 2):** The truth table for the X-NOR gate is shown above. For each combination of inputs A and B, the output A⊕B is calculated. The output is 1 if both inputs are the same (both 0 or both 1) and 0 if the inputs are different.
2. **Gate Symbol (Box 3):** The symbol for the X-NOR gate is represented as A ── X-NOR ── A⊕B B.
3. **Block Diagram (Box 4):** The block diagram for the X-NOR gate is A ──┐ ── A⊕B B └───, showing the flow of inputs and outputs.
4. **Formula (Box 5):** The formula for the X-NOR gate is given as X-NOR → A⊕B + AB. This means that the output of the X-NOR gate is the sum of the product of A and B and the product of A and B.

> Lecturer: "X-NOR gate is derived from X-OR gate and NOT gate."

### Background (not said in the lecture) (lecture e bola hoy ni)
The X-NOR gate is a universal gate along with AND, OR, and NOR gates. It is useful in digital logic design because it can be used to implement other logical functions. Understanding the X-NOR gate helps in designing more complex digital circuits.

---

## Check yourself
1. What are the two types of universal gates?
2. How is the NOR gate constructed?
3. What is the truth table for the NOR gate?
4. What is the formula for the NAND gate?
5. How is the X-NOR gate derived?

### Answers
1. The two types of universal gates are the XOR gate and the NAND gate.
2. The NOR gate is constructed by performing an OR operation followed by a NOT operation.
3. The truth table for the NOR gate is:
   ```markdown
   | A | B | Output |
   |---|---|--------|
   | 0 | 0 |   1    |
   | 0 | 1 |   0    |
   | 1 | 0 |   0    |
   | 1 | 1 |   0    |
   ```
4. The formula for the NAND gate is NAND = AND + NOT.
5. The X-NOR gate is derived by first performing an X-OR operation and then applying a NOT operation.

---

*This lecture is `BanglaASR11` in the dataset (`BanglaASR7_004` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
