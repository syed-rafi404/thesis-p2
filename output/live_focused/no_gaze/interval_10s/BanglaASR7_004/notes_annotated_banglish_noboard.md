# Digital Logic Design
Today we will learn about universal gates, starting with the NOR gate.

## Key takeaways
- Nor gate diye start kori. Nor gate is a universal gate.
- NOR gate er formula, truth table, and gate symbol diye dekha jai.
- NAND gate er definition, truth table, and gate symbol diye dekha jai.
- X-OR gate er truth table, gate symbol, and formula diye dekha jai.
- X-NOR gate er truth table, gate symbol, and formula diye dekha jai.

<!-- boxes: 1=#d62828 -->
## Digital Logic Design
**Ek line e:** Today we will learn about universal gates, starting with the NOR gate.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title


- **Box 1 (red):** Digital Logic Design

The lecturer started by reminding us that in the previous class, we covered fundamental logic gates. Now, we will focus on universal gates, specifically the NOR gate. There are two types of universal gates: the XOR gate and the NOR gate. The NOR gate is one of these universal gates.

The lecturer explained that we will see how to create inputs and outputs using the NOR gate and understand how to build a logical circuit using it. We will begin with the NOR gate.

> Lecturer: "so, nor gate diye start kori. nor gate."

The NOR gate is named as such, even though it involves an OR gate. However, in this context, the NOR gate is distinct from the OR gate.

**Mone rakho:** The NOR gate is a universal gate, meaning it can be used to implement any other logic gate. We will explore how to use the NOR gate to create inputs and outputs and construct logical circuits.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## NOR Gate
**Ek line e:** This board explains how to build a NOR gate using basic logic operations.

![Board 2: 1:00-4:20](figures_annotated/board_era2_100.jpg)

*Figure 2. The whiteboard during 1:00–4:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 NOR gate · 3 Formula · 4 Truth table · 5 Gate symbol


1. **Red Box (Box 1):** The title "Digital Logic Design" sets the context for the discussion on digital circuits.
2. **Blue Box (Box 2):** The blue box introduces the NOR gate, which is a fundamental logic gate.
3. **Orange Box (Box 3):** The formula "OR + NOT = NOR" is displayed, showing the relationship between the OR operation and the NOT operation to form a NOR gate.
4. **Green Box (Box 4):** The green box contains the truth table for the NOR gate. It shows all possible combinations of inputs A and B and their corresponding outputs.
5. **Purple Box (Box 5):** The purple box illustrates the symbol for the NOR gate, which looks like an OR gate with a bubble on top.

**Explanation:**
The lecturer explains that the NOR gate can be constructed by combining the OR operation with a NOT operation. He starts by defining the inputs and output of the NOR gate. The inputs are labeled as A and B, and the output is the result of the OR operation followed by a NOT operation.

- **Step 1:** The lecturer writes down the inputs A and B and explains that the output is the result of A OR B, followed by a NOT operation.
- **Step 2:** He then constructs the truth table for the NOR gate, showing all possible combinations of A and B and their corresponding outputs. For example, when both A and B are 0, the output is 1; when either A or B is 1, the output is 0.
- **Step 3:** The lecturer points out that the output of the NOR gate is the inverse of the OR operation. He demonstrates this by calculating the output for each combination of A and B.
- **Step 4:** Finally, he explains that the NOR gate is a universal gate, meaning it can be used to construct any other logic gate. He mentions that the NOT gate is similar to the NOR gate but with one input always being 1.


**Extra jana kotha:**
NOR gates are essential in digital logic design because they can be used to create other complex logic functions. By understanding the NOR gate, students can grasp the basics of constructing more intricate digital circuits.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Definition of NAND Gate
**Ek line e:** NAND gate is defined as AND followed by NOT.

![Board 3: 4:40-7:00](figures_annotated/board_era3_440.jpg)

*Figure 3. The whiteboard during 4:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 NAND gate · 3 Definition · 4 Block diagram · 5 Truth table · 6 Gate symbol


- **Box 1 (red):** Digital Logic Design
- **Box 3 (orange):** Definition: = AND+NOT
- **Box 5 (purple):** Truth table: 
  | A | B | AB | (AB)' |
  |---|---|----|-------|
  | 0 | 0 | 0  | 1     |
  | 0 | 1 | 0  | 1     |
  | 1 | 0 | 0  | 1     |
  | 1 | 1 | 1  | 0     |
- **Box 6 (pink):** Gate symbol: A ──┐ ── AB B ──└───

The lecturer explains that we are dealing with primary or fundamental gates, specifically mentioning the NOT gate. He then introduces the NAND gate, which combines AND and NOT operations. For a NAND gate with two inputs A and B, the output is the negation of the AND operation between A and B. 

The lecturer then creates a truth table for the NAND gate, listing all possible combinations of inputs (0,0), (0,1), (1,0), and (1,1). He explains the steps to derive the output:

1. **First Step:** Calculate the AND operation between A and B. For (0,0) and (0,1), the result is 0; for (1,0) and (1,1), the result is 1.
2. **Second Step:** Apply the NOT operation to the AND result. For (0,0), (0,1), and (1,0), the output is 1; for (1,1), the output is 0.

Thus, the output column in the truth table represents the NAND gate's output. The lecturer concludes that the NAND gate is a universal gate, meaning we can construct any other logic gate using it. Finally, he mentions that the next gate to discuss will be the exclusive OR (XOR) gate.

**Mone rakho:** NAND gate is defined as AND followed by NOT. Its truth table shows the output for all possible input combinations. The NAND gate is a universal gate, allowing us to build other logic gates.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Truth Table and Gate Symbol of X-OR Gate
**Ek line e:** X-OR gate er truth table and gate symbol diye dekha jai.

![Board 4: 7:20-10:40](figures_annotated/board_era4_720.jpg)

*Figure 4. The whiteboard during 7:20–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Gate symbol · 4 Truth table · 5 Gate symbol · 6 Formula


1. **Red Box (Box 1):** Digital Logic Design
2. **Blue Box (Box 2):** Definition: X-OR gate
3. **Orange Box (Box 3):** Gate symbol: A X-OR B
4. **Green Box (Box 4):** Truth table: 
   | 0 | 0 | 1 | 1 |
   |---|---|---|---|
   | 0 | 1 | 0 | 1 |
5. **Purple Box (Box 5):** Gate symbol: A B A⊕B
6. **Pink Box (Box 6):** Formula: same input = 0 different input = 1

The lecturer explained that the X-OR gate takes two inputs and produces one output. He used the symbol A X-OR B to represent the gate. The X-OR gate is also known as the exclusive OR gate, which is denoted by a plus sign with a circle around it (A + B'). The truth table for the X-OR gate is shown in the green box, where the output is 1 if the inputs are different and 0 if they are the same. 

The lecturer then provided the formula for the X-OR gate: same input equals to 0, and different input equals to 1. He demonstrated this by going through each possible input combination:

- For inputs 0 and 0, the output is 0 because the inputs are the same.
- For inputs 0 and 1, the output is 1 because the inputs are different.
- For inputs 1 and 0, the output is 1 because the inputs are different.
- For inputs 1 and 1, the output is 0 because the inputs are the same.

He emphasized that if we understand the X-OR gate, it becomes easier to understand other similar gates like the X-NOR gate. The X-NOR gate is the complement of the X-OR gate, meaning it outputs 1 when the inputs are the same and 0 when they are different.

**Mone rakho:** X-OR gate er truth table, gate symbol, and formula. Same input gives 0, and different input gives 1.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Digital Logic Design

**Ek line e:** X-NOR gate is derived from X-OR gate and NOT gate.

![Board 5: 10:50-14:00](figures_annotated/board_era5_1050.jpg)

*Figure 5. The whiteboard during 10:50–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Block diagram · 5 Formula


- **Box 1 (red):** Digital Logic Design
- **Box 2 (blue):** Truth table of X-NOR gate:  
  | X-OR+NOT A | B | A⊕B | (A⊕B)' |
  |------------|---|-----|--------|
  | 0          | 0 |   0 |      1 |
  | 0          | 1 |   1 |      0 |
  | 1          | 0 |   1 |      0 |
  | 1          | 1 |   0 |      1 |

- **Box 3 (orange):** Gate symbol:  
  ```
  A ── X-NOR ── A⊕B
  B ──
  ```

- **Box 4 (green):** Block diagram:  
  ```
  A ──┐ ── A⊕B
  └───
  ```

- **Box 5 (purple):** Formula: X-NOR → AB + AB'

**Explanation:**
The lecturer explains that the X-NOR gate is derived from the X-OR gate and a NOT gate. First, we start with the X-OR gate, which takes two inputs (A and B) and produces an output (A⊕B). Then, we apply a NOT gate to the output of the X-OR gate to get the final output of the X-NOR gate. 

The truth table for the X-NOR gate is shown in Box 2. It lists all possible combinations of inputs (A and B) and their corresponding outputs. For the X-NOR gate, the output is 1 if both inputs are the same (both 0 or both 1), and 0 if the inputs are different.

The gate symbol for the X-NOR gate is shown in Box 3, and the block diagram is shown in Box 4. The formula for the X-NOR gate is given in Box 5: X-NOR → AB + AB'. This formula represents the logical expression for the X-NOR gate, where AB is the AND operation between A and B, and AB' is the AND operation between A and the NOT of B.


**Extra jana kotha (lecture e bola hoy ni):**
The X-NOR gate is a fundamental logic gate used in digital circuits. It is useful in applications where we need to check if two inputs are equal. Understanding the X-NOR gate helps in designing more complex digital systems.

---

## Check yourself
1. Nor gate er formula kemon dite hobe?
2. X-OR gate er output kemon hole 1?
3. NAND gate er symbol kemon dite hobe?
4. X-NOR gate er formula kemon dite hobe?
5. Nor gate kintu nor operation kintu OR operation kintu NOT operation kintu?

### Answers
1. OR + NOT = NOR
2. X-OR gate er output 1 hole, inputs same na hole.
3. A ──┐ ── AB B ──└───
4. X-NOR → AB + AB'
5. Nor gate kintu nor operation kintu OR operation kintu NOT operation kintu.

---

*This lecture is `BanglaASR11` in the dataset (`BanglaASR7_004` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 2 removed. References to boxes that do not exist: 0.*
