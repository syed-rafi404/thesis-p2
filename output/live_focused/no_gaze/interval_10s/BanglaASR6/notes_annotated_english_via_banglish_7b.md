# Digital Logic Design
THE SECTIONS

## Key takeaways
- Analog signals are continuous, while digital signals are discrete.
- In TTL systems, 5 volts represent logic 1, and 0 volts represent logic 0.
- Logic gates are used to process combinations of high and low voltages.
- An AND gate outputs 1 only when both inputs are 1.
- The OR gate outputs 1 if at least one of its inputs is 1.
- The NOT gate inverts the input signal.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Digital Logic Design
**In one line:** Digital Logic Design is the foundation of how computers process information.

![Board 1: 0:10-3:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula


- **Box 1 (red):** Digital Logic Design
- **Box 2 (blue):** analog → continuous value Digital → Discrete value
- **Box 3 (orange):** (TTL) →5 volt (High) →Logic 1 →0 volt (Ground) →Logic 0 Key→A 011011

The lecturer started by explaining the basics of digital logic design. He mentioned that understanding digital logic is crucial for software development because it helps us comprehend how computers perform tasks. He then contrasted analog and digital systems, stating that analog systems deal with continuous values, while digital systems handle discrete values.

The lecturer gave an example of analog signals, such as temperature and sound waves, which can vary continuously. However, computers cannot process these continuous values directly. Instead, they convert analog signals into digital form using discrete values—zeros and ones. For instance, a light switch is a simple example of a digital system where the switch is either on (high voltage) or off (low voltage).

The lecturer explained that in digital systems, a high voltage represents a logic 1, and a low voltage represents a logic 0. He used the example of a TTL (Transistor-Transistor Logic) system, where 5 volts represent a high voltage (logic 1) and 0 volts represent a ground voltage (logic 0). This means that a computer processes information using only zeros and ones.

He further elaborated that when we press a key on a keyboard, it creates a combination of high and low voltages. For example, if we have a 5-volt high voltage and a 0-volt ground voltage, pressing the key would create a specific combination of zeros and ones. This combination is created by a physical device called a logic gate.

In summary, the key points are:
- Analog systems deal with continuous values, while digital systems use discrete values (zeros and ones).
- High voltage in TTL systems represents logic 1, and low voltage represents logic 0.
- Pressing a key on a keyboard creates a combination of high and low voltages, which is processed by logic gates.

**Remember:** Analog signals are continuous, while digital signals are discrete. In TTL systems, 5 volts represent logic 1, and 0 volts represent logic 0. Logic gates are used to process these combinations of high and low voltages.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Digital Logic Design

**In one line:** Today we will discuss digital logic design and the basic building blocks of digital circuits.

![Board 2: 3:20-5:50](figures_annotated/board_era2_320.jpg)

*Figure 2. The whiteboard during 3:20–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List


The board lists several types of logic gates: AND gate, OR gate, NOT gate, NOR gate, NAND gate, X-OR gate, and X-NOR gate. The lecturer explains that these are the fundamental gates used in digital logic design.

1. **AND Gate**: The first gate mentioned is the AND gate. This gate outputs a high signal (1) only if all its inputs are high. It is a fundamental gate because it forms the basis for more complex logic operations.

2. **OR Gate**: The second gate is the OR gate. This gate outputs a high signal (1) if any of its inputs are high. Like the AND gate, it is also a fundamental gate.

3. **NOT Gate**: The third gate is the NOT gate, which inverts the input signal. If the input is 1, the output is 0, and vice versa. This gate is essential for creating other logic functions.

4. **NOR Gate and NAND Gate**: The fourth and fifth gates are the NOR gate and NAND gate, respectively. These are considered universal gates because any Boolean function can be implemented using just these two gates.

5. **X-OR Gate and X-NOR Gate**: The final two gates are the X-OR gate and X-NOR gate. These gates perform exclusive and inclusive OR operations, respectively.

The lecturer emphasizes that these logic gates are crucial for decision-making processes in digital circuits. They help determine which signals pass through and which do not, effectively making decisions based on the inputs.

>The lecturer said: "So, which logic gate will we use? These logic gates will perform decision-making tasks, like connecting wires, making a single connection."

In this class, we will start with the fundamental gates. Since these gates represent the physical components in real processors, we have billions of these gates working together to perform complex tasks.

### Background (not said in the lecture)
Understanding the basic logic gates is essential for designing digital circuits. These gates form the foundation for more complex digital systems, such as microprocessors and memory units. By mastering these gates, students can better understand how digital devices operate at a fundamental level.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## AND Gate in Digital Logic Design
An AND gate takes two inputs and produces one output.

![Board 3: 6:00-10:00](figures_annotated/board_era3_600.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Worked example


- **Red Box 1 (Title):** Digital Logic Design
- **Blue Box 2 (Truth Table):** The AND gate truth table is shown here. It lists all possible combinations of inputs A and B, and their corresponding outputs Y.
  | A | B | Y |
  |---|---|---|
  | 0 | 0 | 0 |
  | 0 | 1 | 0 |
  | 1 | 0 | 0 |
  | 1 | 1 | 1 |

- **Orange Box 3 (Gate Symbol):** The AND gate symbol is depicted as A B AND gate X. This shows how the inputs A and B are connected to produce the output X.
- **Green Box 4 (Worked Example):** A practical example is given where a bulb blub is used to illustrate the operation of the AND gate. The equation A·B=X is shown, along with the results of the multiplication for different input combinations.

The lecturer said: "An AND gate takes two inputs, A and B, and produces one output, X. When both inputs are 0, the output is 0. When one input is 0 and the other is 1, the output is also 0. Similarly, when one input is 1 and the other is 0, the output is 0. However, when both inputs are 1, the output is 1. This is because the AND gate performs a logical multiplication of the inputs."

>Lecturer: "An AND gate e jeta hoy, suppose eta hocche amar shek physical device ta, which is a gate, jeta ke ami bolchi, and gate."

The lecturer further explained that in digital systems, the inputs and outputs are represented by binary values, 0 and 1. These values correspond to the state of a light being off or on. For instance, if A represents the state of one bulb and B represents the state of another bulb, then the output X will be 1 only when both bulbs are on. Otherwise, the output will be 0.

>Lecturer: "So, zero mane ki amar light off. And one hocche, aikat zero ke ami rakhe light off."

In a real-world scenario, if both bulbs are on, the room will be bright. Conversely, if one bulb is off and the other is on, the room will be dim. Only when both bulbs are on will the room be fully bright. This example helps us understand the functionality of the AND gate in a more tangible way.

**Remember:** An AND gate outputs 1 only when both inputs are 1. Otherwise, the output is 0. This can be visualized using a simple bulb analogy where both bulbs need to be on for the room to be fully bright.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 1 (red): Digital Logic Design
**In one line:** This section covers the basics of digital logic design.

![Board 4: 10:10-11:00](figures_annotated/board_era4_1010.jpg)

*Figure 4. The whiteboard during 10:10–11:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


**Explanation:**
1. **Box 1 (red)**: The title "Digital Logic Design" introduces the topic of the lecture.
2. **Box 2 (blue)**: The truth table for the AND gate is shown. It lists all possible combinations of inputs A and B, and their corresponding outputs Y. The table is:
   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |
3. **Box 3 (orange)**: The gate symbol for the AND gate is depicted. It shows inputs A and B connected to a box labeled "AND", with the output labeled X.
4. **Box 4 (green)**: The formula for the AND gate is given as X = AB.

**Quotes:**

**Background (not said in the lecture):**
The AND gate is a fundamental component in digital logic design. It takes two inputs and produces an output based on the logical AND operation. If either of the inputs is zero, the output will also be zero. This gate is used in various electronic circuits to perform logical operations. Understanding the AND gate is crucial for designing more complex digital systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 2 (blue) and Box 3 (orange) ki shekhano hocche, choto heading
**In one line:** This board explains the OR gate and its representation.

![Board 5: 11:10-13:00](figures_annotated/board_era5_1110.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


- **Box 2 (blue)**: Look at the blue box 2, which shows the truth table for the OR gate. The table has three columns: A, B, and X. A and B represent the inputs, and X represents the output. The table shows all possible combinations of A and B and their corresponding outputs. For example, when both A and B are 0, the output X is 0. When A is 0 and B is 1, the output X is 1. Similarly, when A is 1 and B is 0, the output X is 1. And when both A and B are 1, the output X is 1.

- **Box 3 (orange)**: The orange box 3 shows the gate symbol for the OR gate. It is represented as A OR B X, where A and B are the inputs and X is the output.

- **Box 4 (green)**: The green box 4 provides the formula for the OR gate, which is A + B = X. This formula means that the output X is the logical OR of inputs A and B.

> Lecturer: "Suppose input is a and output is b. So our output which will be there, is x."

### Background (not said in the lecture) (lecture e bola hoy ni)
The OR gate is a fundamental component in digital logic design. It takes two binary inputs and produces an output that is 1 if at least one of the inputs is 1. Understanding the OR gate is crucial for designing more complex digital circuits.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Box 1 (red): Digital Logic Design
**In one line:** Digital Logic Design

![Board 6: 13:10-14:50](figures_annotated/board_era6_1310.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table · 4 Block diagram · 5 Gate symbol


**Explanation:**
1. **Box 1 (red)**: The title of the board is "Digital Logic Design". This is the main topic we are discussing today.
2. **Box 2 (blue)**: The lecturer explains the concept of the **NOT gate**, also known as an inverter. The lecturer said: "NOT gate: (Inverter)".
3. **Box 3 (orange)**: The truth table for the NOT gate is shown. It is a simple table with two columns: `A` and `(A)'` (NOT A). The table looks like this:
   | A | (A)' |
   |---|--------------|
   | 0 | 1            |
   | 1 | 0            |
   The lecturer explains: "NOT gate a ki hoy? Amar je physical device ta seikhane just ekta ei input ber dhukbe and ekta ei output ber hobe. Suppose ekhane jodi ei as a input jay, tahole ami ei bar as a output pabo."
4. **Box 4 (green)**: The block diagram for the NOT gate is shown. It is represented as `A → NOT → (A)'`. The lecturer says: "ekhane ei bar jinish ta ki? ta hobe jabe, a bar hocche alternate of a. tar mane ki? tar mane hocche amar input a and output a bar. input jodi zero hoy, tahole output hobe one. and input jodi one hoy ar output ta hobe zero. ebhabei opposite je signal toh sheita ama ke not get."
5. **Box 5 (purple)**: The gate symbol for the NOT gate is shown. It is represented as `A → (A)'`. The lecturer further explains: "ekhon etar jodi ami logical circuit ta dekhi, ekta input jacche a not get ta dekhte hobe, erokom. okay? so ekta input jacche not hoy, arekta input behocche. so ei gula gelo amar kichhu fundamental gates."

**Quotes:**
> Lecturer: "NOT gate a ki hoy? Amar je physical device ta seikhane just ekta ei input ber dhukbe and ekta ei output ber hobe."

### Background (not said in the lecture) (lecture e bola hoy ni)
The NOT gate is a fundamental component in digital logic design. It takes a single input and produces an output that is the logical opposite of the input. This gate is crucial for creating more complex circuits and is used extensively in digital systems. Understanding the NOT gate is essential for grasping more advanced concepts in digital logic.

---

## Check yourself
1. What does an AND gate output when both inputs are 1?
2. In TTL systems, what voltage represents logic 1?
3. What is the output of an OR gate when both inputs are 0?
4. What does a NOT gate do to its input?
5. What is the output of a NOT gate when the input is 0?

### Answers
1. An AND gate outputs 1 when both inputs are 1.
2. In TTL systems, 5 volts represent logic 1.
3. The output of an OR gate is 0 when both inputs are 0.
4. A NOT gate inverts the input signal.
5. The output of a NOT gate is 1 when the input is 0.

---

*This lecture is `BanglaASR10` in the dataset (`BanglaASR6` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (5 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
