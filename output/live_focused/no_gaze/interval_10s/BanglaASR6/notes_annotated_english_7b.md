# Digital Logic Design
This lecture covers the fundamental concepts of digital logic design, including the introduction to basic logic gates and their representations.

## Key takeaways
- Digital systems operate on discrete values (0s and 1s) rather than continuous signals.
- The AND, OR, and NOT gates are fundamental logic gates that form the basis of more complex digital circuits.
- The NOT gate inverts the input signal, while the AND and OR gates perform logical operations on binary inputs.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Introduction to Digital Logic Design
**In one line:** This board introduces the fundamental concepts of digital versus analog signals and explains how computers process information using binary logic.

![Board 1: 0:10-3:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula


1. **Digital Logic Design**: The board starts with the title "Digital Logic Design," which sets the context for the lecture.
2. **Analog vs. Digital**: The blue box defines analog as continuous value and digital as discrete value. This distinction is crucial because analog signals can take any value within a range, whereas digital signals can only take specific, distinct values.
3. **TTL Logic Levels**: The orange box provides the specific logic levels for TTL (Transistor-Transistor Logic). It states that 5 volts represent a high logic level (Logic 1), while 0 volts represent a low logic level (Logic 0). The key 'A' followed by '011011' is likely a reference to a specific example or key points discussed.

>The lecturer said: "so, our computer will only work with zeros and ones."

### Background
Digital systems use binary logic to process information, where data is represented as sequences of 0s and 1s. This binary representation allows for precise and reliable computation, making digital devices like computers and microcontrollers essential in modern technology. Understanding the basics of digital logic is fundamental for designing and analyzing digital circuits.

**Remember:** The key concept here is that digital systems operate on discrete values (0s and 1s) rather than continuous signals, which is why we use logic gates to process these binary inputs.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to Basic Logic Gates
**In one line:** This board introduces the basic logic gates and their significance in digital logic design.

![Board 2: 3:20-5:50](figures_annotated/board_era2_320.jpg)

*Figure 2. The whiteboard during 3:20–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List


The board starts with the title "Digital Logic Design" in red, followed by a list of logic gates. The first three gates—AND, OR, and NOT—are highlighted as fundamental gates. The next two gates, NOR and NAND, are identified as universal gates. Finally, the board mentions the X-OR and X-NOR gates, which are also considered exclusive gates.

1. **AND Gate**: The lecturer explains that the first gate is the AND gate. This gate outputs a high signal (1) only when all its inputs are high. It is a fundamental gate because it forms the basis for more complex logic operations.
   
2. **OR Gate**: The second gate is the OR gate, which outputs a high signal (1) if at least one of its inputs is high. Like the AND gate, the OR gate is also fundamental and essential for building complex logic circuits.

3. **NOT Gate**: The third gate is the NOT gate, which inverts the input signal. If the input is high (1), the output is low (0), and vice versa. This gate is crucial for creating other logic gates and is often used to generate new signals based on existing ones.

4. **NOR and NAND Gates**: The fourth and fifth gates are NOR and NAND, respectively. These gates are universal gates, meaning they can be used to implement any other logic gate. The lecturer emphasizes that these gates are versatile and can be used to create complex circuits.

5. **X-OR and X-NOR Gates**: The final two gates mentioned are the X-OR and X-NOR gates, which are exclusive gates. These gates perform specific logical operations and are useful in various applications.

The lecturer explains that these logic gates are used for decision-making processes in digital circuits. They help determine which signals pass through and which do not, effectively making decisions based on the input connections. For this class, the lecturer will start by covering the fundamental gates, as they form the building blocks of more complex circuits.

> The lecturer said: "so, ei shakta logic gate ki korbe? ei shakta logic gate hocche amar decision making a kaaj korbe, je ekta connection ki hoy, wire er maddhome hoy, ekta connection korebhe hobe."  
This means: "So, which of these logic gates can we use? These logic gates will be used for decision-making processes, where a single connection is made, like a wire, and a decision is based on that connection."

**Remember:** The fundamental logic gates (AND, OR, NOT) are the building blocks of more complex digital circuits and are essential for understanding how digital systems make decisions.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Digital Logic Design: Introduction to AND Gate
**In one line:** An AND gate takes two inputs and produces an output based on their logical AND operation.

![Board 3: 6:00-10:00](figures_annotated/board_era3_600.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Worked example


1. **Red Box (Title):** The red box titled "Digital Logic Design" introduces the topic of digital logic design, which deals with the fundamental building blocks of digital circuits.
2. **Blue Box (Truth Table):** The blue box shows the truth table for the AND gate. It lists all possible combinations of inputs (A and B) and their corresponding outputs (Y). Specifically, the table is:
   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |
3. **Orange Box (Gate Symbol):** The orange box displays the symbol for an AND gate. It shows how the inputs (A and B) connect to the output (X) via the AND operation.
4. **Green Box (Worked Example):** The green box provides a practical example using a bulb. It explains that when both inputs (A and B) are 1, the output (X) is 1, turning the bulb on. Conversely, if either input is 0, the output is 0, turning the bulb off. The worked example is:
   - 0 . 0 = 0 (Light OFF)
   - 0 . 1 = 0 (Light OFF)
   - 1 . 0 = 0 (Light OFF)
   - 1 . 1 = 1 (Light ON)

>The lecturer said: "so, and gate basically jinish ta ki? and gate e jeta hoy, suppose eta hocche amar şey physical device ta, which is a gate, jeta ke ami bolchi, and gate. eta ki korbe? etar moddhe duita input jaite pare. suppose first input is a, and second input is b."

The AND gate takes two inputs and produces an output based on their logical AND operation. If both inputs are 1, the output is 1; otherwise, the output is 0.

### Background
An AND gate is a basic component in digital logic circuits. It performs a logical AND operation on two binary inputs, producing a single binary output. This operation is crucial in various applications such as data processing, control systems, and digital communication. Understanding AND gates is essential for designing more complex digital circuits.

**Remember:** An AND gate outputs 1 only when both inputs are 1; otherwise, it outputs 0.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Digital Logic Design: Introduction to AND Gate and Its Representation
**In one line:** This board introduces the AND gate, its truth table, and the corresponding gate symbol and formula.

![Board 4: 10:10-11:00](figures_annotated/board_era4_1010.jpg)

*Figure 4. The whiteboard during 10:10–11:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


1. **Red Box (Title):** The title "Digital Logic Design" sets the context for the lecture.
2. **Blue Box (Truth Table):** The truth table for the AND gate is shown:
   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |
   This table shows the output `Y` for all possible combinations of inputs `A` and `B`. The lecturer explained that the output `Y` is the result of multiplying `A` and `B`, which is equivalent to their logical AND operation.
3. **Orange Box (Gate Symbol):** The gate symbol for the AND gate is depicted as follows:
   - Inputs `A` and `B` are connected to an AND gate, which produces an output `X`.
   - The symbol for the AND gate is a box with the inputs `A` and `B` entering from the left and the output `X` exiting from the right.
4. **Green Box (Formula):** The formula for the AND gate is given as:
   - `X = AB`
   - This formula represents the output `X` as the product of inputs `A` and `B`.

The lecturer said: "input and x hocche amr output jeta ki chilo? a and b er multiplication. so etai hocche amr and keidh. tar mane amr duita input thakbe, ekta output thakbe, duitar multiplication, input er multiplication hoy ami output ta pabo, ekta jodi zero thake jekono output er moddhe, tahole kinto ami zero as a output pay jabo."
This means: "What is the output when we take the input and x? It is the result of multiplying A and B. So, this is the AND gate. In other words, the AND gate will have two inputs and one output, and the output will be the multiplication of the inputs. If any input is zero, the output will also be zero."

### Background
An AND gate is a fundamental component in digital logic design. It performs a logical AND operation on its inputs, producing an output that is true only if both inputs are true. The AND gate is widely used in various digital circuits and systems, such as data processing and control systems, where binary decisions need to be made based on multiple conditions.

**Remember:** The AND gate outputs a high signal (1) only when both of its inputs are high (1). If either or both inputs are low (0), the output is low (0).

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Digital Logic Design: Introduction to OR Gate and Its Representation
**In one line:** This board introduces the OR gate, its truth table, and the corresponding gate symbol and formula.

![Board 5: 11:10-13:00](figures_annotated/board_era5_1110.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


1. **Understanding the OR Gate**: Look at the red box titled "Digital Logic Design." The lecturer introduced the concept of the OR gate, which is a fundamental component in digital logic design. The truth table for the OR gate is shown in Box 2 (blue). It lists all possible combinations of inputs A and B and their corresponding outputs X. The table is as follows:

   | A | B | X |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 1 |

2. **OR Gate Symbol and Formula**: The orange box (3) displays the gate symbol for the OR gate, which is represented as  A  OR  B . The green box (4) provides the formula for the OR operation, which is  A + B = X .

3. **Explanation of the OR Operation**: The lecturer explained that when both inputs A and B are 0, the output X is also 0. However, if either A or B is 1, the output X will be 1. This means that the OR gate outputs 1 if at least one of its inputs is 1. The lecturer further illustrated this by stating that the OR gate can be used to combine different binary values from inputs A and B.

4. **Logic Circuit Representation**: The lecturer then moved on to explain how the OR gate can be represented in a logic circuit diagram. The diagram shows inputs A and B connected to an OR gate, with the output labeled as X.

5. **Introduction to NOT Gate**: Finally, the lecturer mentioned that the last fundamental gate is the NOT gate, but this was discussed after explaining the OR gate.

> The lecturer said: "when we have two inputs, A and B, and we want to find the output, X, we need to consider all possible combinations of these inputs."

**Remember:** The OR gate outputs 1 if at least one of its inputs is 1, and it is represented by the formula  A + B = X .

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Introduction to NOT Gate and Its Representation
**In one line:** This board introduces the NOT gate, also known as an inverter, and explains its truth table, block diagram, and gate symbol.

![Board 6: 13:10-14:50](figures_annotated/board_era6_1310.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table · 4 Block diagram · 5 Gate symbol


### Box 1 (red): Digital Logic Design
The board starts with the title "Digital Logic Design," setting the context for the discussion on digital logic components.

### Box 2 (blue): Definition: NOT gate: (Inverter)
The lecturer defines the NOT gate, also referred to as an inverter, explaining that it is a basic logic gate that takes one input and produces an output that is the logical complement of the input. In other words, if the input is 0, the output will be 1, and if the input is 1, the output will be 0.

### Box 3 (orange): Truth table
The truth table for the NOT gate is shown:
| A | (A)' |
|---|--------------|
| 0 | 1            |
| 1 | 0            |
This table clearly illustrates that the output (A)' is the opposite of the input A. If A is 0, (A)' is 1, and if A is 1, (A)' is 0.

### Box 4 (green): Block diagram
The block diagram for the NOT gate is represented as:
A --- NOT --- (A)' ↓ alternate of A
This diagram visually shows how the input A passes through the NOT gate to produce the output (A)', which is the alternate of A.

### Box 5 (purple): Gate symbol
The gate symbol for the NOT gate is shown as:
A --- (A)'
This symbol represents the relationship between the input A and the output (A)'.

### Quotes
> The lecturer said: "it might seem complex but it is actually quite simple. An inverter is a device where, if we give it an input, it gives us an output that is the opposite of the input."

### Background
The NOT gate is a fundamental component in digital logic design. It is used to invert the state of a binary signal, which is crucial in various applications such as creating complements, implementing logical operations, and simplifying complex circuits. Understanding the NOT gate is essential for designing more complex digital systems.

**Remember:** The NOT gate is a basic yet critical component in digital logic, as it allows for the inversion of binary signals, enabling the implementation of various logical functions.

---

## Check yourself
1. What is the difference between analog and digital signals?
2. Explain the function of the AND gate and provide an example.
3. Describe the truth table and gate symbol for the OR gate.
4. What does the NOT gate do, and how is it represented?

### Answers
1. Analog signals can take any value within a range, whereas digital signals can only take specific, distinct values (0s and 1s).
2. The AND gate outputs a high signal (1) only when all its inputs are high. For example, if both inputs A and B are 1, the output X is 1; otherwise, the output is 0.
3. The truth table for the OR gate is:
   | A | B | X |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 1 |
   The gate symbol for the OR gate is:
   ```
   A --- OR --- X
   ```
4. The NOT gate inverts the input signal. If the input is 0, the output is 1, and if the input is 1, the output is 0. It is represented by the symbol:
   ```
   A --- (A)'
   ```

---

*This lecture is `BanglaASR10` in the dataset (`BanglaASR6` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (5 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
