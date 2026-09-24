# Digital Logic Design
Ek line e: Digital Logic Design is the study of how computers process information using binary values.

## Key takeaways
- Digital systems use binary values (0s and 1s).
- There are seven types of logic gates: AND, OR, NOT, NOR, NAND, X-OR, and X-NOR.
- The AND gate performs a logical AND operation on its inputs.
- The OR gate performs a logical OR operation on its inputs.
- The NOT gate inverts the input signal.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Digital Logic Design
**Ek line e:** Digital Logic Design is the study of how computers process information using binary values.

![Board 1: 0:10-3:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula


- **Box 1 (red):** Digital Logic Design
- **Box 2 (blue):** analog → continuous value, Digital → Discrete value
- **Box 3 (orange):** (TTL) →5 volt (High) → Logic 1 →0 volt (Ground) → Logic 0 Key→A 011011

The lecturer starts by introducing the course, Digital Logic Design, which is crucial for understanding how computers operate. He explains that while we deal with continuous values in analog systems, digital systems work with discrete values. An example of an analog system is a temperature sensor or a sound wave, which can take any value within a range. In contrast, digital systems like a light switch or a match can only be in specific states—on or off.

The lecturer then defines digital signals as those that represent discrete values, specifically 0s and 1s. He uses the example of a light switch to illustrate this concept, where the switch can either be on (1) or off (0). He emphasizes that computers operate using these binary values, and in the upcoming lectures, he will delve into how these values are used in circuits and logic.

Next, the lecturer introduces the term TTL (Transistor-Transistor Logic), explaining that in TTL circuits, 5 volts represent a high voltage (Logic 1) and 0 volts represent a low voltage (Logic 0). He provides a key to show the binary representation of these values: A 011011.

> Lecturer: "Continuous value. Analog signaler key example, temperature, sound wave, even analogies."
> 
> Lecturer: "Discrete value. After digital signaler, what example should we do? What is lighter switch? What is on? Not off. What is the condition of the match? Similarly, what is on?"

The lecturer further explains that pressing a key button results in high and low voltages, which correspond to Logic 1 and Logic 0 respectively. He concludes by stating that combining these voltages allows us to create various logical operations, leading to the introduction of logic gates.

**Mone rakho:** Digital systems use binary values (0s and 1s), and TTL circuits define these values as 5 volts (Logic 1) and 0 volts (Logic 0).

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Digital Logic Design
**Ek line e:** Total seven logic gates are there.

![Board 2: 3:20-5:50](figures_annotated/board_era2_320.jpg)

*Figure 2. The whiteboard during 3:20–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List


- **Red Box 1 (Title):** Digital Logic Design
- **Blue Box 2 (List):** Logic gates 1) AND gate 2) OR gate 3) NOT gate 4) NOR gate 5) NAND gate 6) X-OR gate 7) X-NOR gate Fundamental gates Universal gate Exclusive gate

The lecturer explained that there are seven types of logic gates: AND, OR, NOT, NOR, NAND, X-OR, and X-NOR. He further categorized these gates into different groups:

- **Fundamental Gates:** The first three gates—AND, OR, and NOT—are considered fundamental gates.
- **Universal Gates:** The fourth and fifth gates, NOR and NAND, are known as universal gates because any logical function can be implemented using just these two gates.
- **Exclusive Gate:** The last gate, X-NOR, is referred to as the exclusive gate.

The lecturer emphasized that these gates are the building blocks of digital circuits and how they form the basis for more complex logic operations. He mentioned that while we start with individual gates, modern processors can have millions of these gates integrated to perform complex tasks.

> Lecturer: "So, our first 3-tah gate is called fundamental gates."

### Extra jana kotha
Understanding the basic logic gates is crucial as they form the foundation of digital systems. By learning these gates, students can grasp how more complex digital circuits and systems are designed and implemented.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## AND Gate in Digital Logic Design
**Ek line e:** AND gate is a fundamental component in digital logic design.

![Board 3: 6:00-10:00](figures_annotated/board_era3_600.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Worked example


1. **Red Box 1 (Title):** Digital Logic Design
2. **Blue Box 2 (Truth Table):** The AND gate takes two inputs, A and B, and produces an output Y. The truth table for the AND gate is shown below:
   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |
   
3. **Orange Box 3 (Gate Symbol):** The AND gate can be represented by the following symbol:
   ```
   A --- AND --- X
   B
   ```

4. **Green Box 4 (Worked Example):** Let's consider a practical example where the output X is determined by the AND operation between inputs A and B. The worked example is given as follows:
   ```
   Bulb blub
   A . B = X
   0 . 0 = 0
   0 . 1 = 0
   1 . 0 = 0
   1 . 1 = 1
   0 → Light OFF
   1 → Light ON
   ```

The lecturer explained that the AND gate performs a logical AND operation on its inputs. For instance, if both inputs A and B are 0, the output X is 0. Similarly, if A is 0 and B is 1, the output X is also 0. When A is 1 and B is 0, the output X remains 0. However, if both A and B are 1, the output X is 1.


The output of the AND gate can be visualized as controlling a light bulb. If both bulbs A and B are off (0), the room will be dark (0). If one bulb is on and the other is off, the room will have dim lighting (0). Only when both bulbs are on (1) will the room be fully lit (1).


In summary, the AND gate is a crucial element in digital circuits, performing a simple yet essential logical operation. It helps in controlling various devices based on the combination of binary inputs.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 1 (Red): Digital Logic Design
**Ek line e:** This section covers the basics of digital logic design, focusing on the AND gate.

![Board 4: 10:10-11:00](figures_annotated/board_era4_1010.jpg)

*Figure 4. The whiteboard during 10:10–11:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


**Explanation:**
1. **Box 1 (Red):** The title "Digital Logic Design" introduces the topic of the lecture.
2. **Box 2 (Blue):** The truth table for the AND gate is shown. It lists all possible combinations of inputs A and B, and their corresponding outputs Y. For example, when both A and B are 0, the output Y is 0; when A is 0 and B is 1, the output Y is 0; when A is 1 and B is 0, the output Y is 0; and when both A and B are 1, the output Y is 1.
3. **Box 3 (Orange):** The gate symbol for the AND gate is displayed. It shows inputs A and B connected to an AND gate, which produces an output X.
4. **Box 4 (Green):** The formula for the AND gate is given as X = AB. This means that the output X is the logical product of inputs A and B.

> Lecturer: "input and x, so our output is a and b are multiplication."

**Extra jana kotha (lecture e bola hoy ni):**
Understanding the AND gate is crucial because it forms the basis for more complex digital circuits. The AND gate takes two binary inputs and produces an output that is 1 only if both inputs are 1. This simple operation is fundamental in digital logic design.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 2 (Blue) and Box 3 (Orange) ki shekhano hocche, choto heading
**Ek line e:** Digital Logic Design

![Board 5: 11:10-13:00](figures_annotated/board_era5_1110.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


- **Box 2 (Blue)**: Look at the blue box showing the truth table for an OR gate. It lists the inputs A and B and the corresponding output X. The table is as follows:

| A | B | X |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

- **Box 3 (Orange)**: The orange box shows the gate symbol for the OR gate. It is represented as A OR B X.

- **Box 4 (Green)**: The green box provides the formula for the OR gate, which is A + B = X.

The lecturer explained that if the input is A and the output is B, then the output X will be the result of the OR operation between A and B. He demonstrated this by filling in the truth table with combinations of 0s and 1s for A and B, resulting in the output X as shown in the table.

> Lecturer: "Suppose inputta hoche A and outputta hoche B. So, my outputta bheer hobeer, sheta hoche X."

The lecturer then explained the formula A + B = X, which means that when A and B are both 0, the output X is 0. When either A or B is 1, the output X is 1. This is because the OR gate outputs 1 if any of its inputs are 1.

- **Box 4 (Green)**: The formula A + B = X represents the logical OR operation.

Next, the lecturer showed the gate diagram, where inputs A and B are connected to an OR gate, and the output is labeled as X. He also mentioned that this is a fundamental gate, and the next gate he would discuss is the NOT gate.

**Mone rakho:** The OR gate truth table, the gate symbol, and the formula A + B = X are important for understanding digital logic design.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Box 1 (Red): Digital Logic Design
**Ek line e:** Digital Logic Design

![Board 6: 13:10-14:50](figures_annotated/board_era6_1310.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table · 4 Block diagram · 5 Gate symbol


### Box 2 (Blue): NOT gate: (Inverter)
The NOT gate, also known as an inverter, is a fundamental component in digital logic design. It takes a single input and produces an output that is the logical negation of the input. In other words, if the input is 0, the output will be 1, and if the input is 1, the output will be 0.

#### Box 3 (Orange): Truth Table
| A | (A)' |
|---|--------------|
| 0 | 1            |
| 1 | 0            |

This table shows the relationship between the input  A  and the output  (A)' . As you can see, when  A  is 0,  (A)'  is 1, and when  A  is 1,  (A)'  is 0.

#### Box 4 (Green): Block Diagram
The block diagram for the NOT gate is shown as follows:
```
A --- NOT --- (A)'
```
This diagram represents the flow of data through the NOT gate. The input  A  goes into the NOT gate, which inverts the signal, and the output is  (A)' .

#### Box 5 (Purple): Gate Symbol
The symbol for the NOT gate is:
```
A --- (A)'
```

### Explanation
The NOT gate is a basic building block in digital circuits. It simply flips the input signal. For example, if the input  A  is 0, the output  (A)'  will be 1, and if the input  A  is 1, the output  (A)'  will be 0. This is because the NOT gate acts as an inverter, producing the opposite of the input signal.

> Lecturer: "Not get a concept taken to RO easier. Not get a kii hoi? Amarji physical device ta shayi khane just acta i input dhug bhe and acta i output bhe rho bhe."

### Extra jana kotha
The NOT gate is crucial in digital logic design because it helps in creating more complex circuits. By combining multiple NOT gates, we can create more sophisticated logic functions. Understanding the NOT gate is fundamental to grasping how digital circuits work.

---

## Check yourself
1. How many types of logic gates are there in digital logic design?
2. What does the AND gate produce as output when both inputs are 1?
3. Write the truth table for the OR gate.
4. What is the symbol for the NOT gate?
5. What is the formula for the AND gate?

### Answers
1. There are seven types of logic gates in digital logic design.
2. The AND gate produces an output of 1 when both inputs are 1.
3. The truth table for the OR gate is:
   | A | B | X |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 1 |
4. The symbol for the NOT gate is:
   ```
   A --- (A)'
   ```
5. The formula for the AND gate is X = AB.

---

*This lecture is `BanglaASR10` in the dataset (`BanglaASR6` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 6 kept, 2 removed. References to boxes that do not exist: 0.*
