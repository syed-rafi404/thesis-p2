# Digital Logic Design
THE SECTIONS

## Key takeaways
- Digital systems use binary logic, where high voltage (5 volts) represents Logic 1 and low voltage (0 volts) represents Logic 0.
- Logic gates are the building blocks of digital circuits, including AND, OR, NOT, NOR, NAND, X-OR, and X-NOR gates.
- The AND gate outputs a high signal (1) only if all its inputs are high.
- The OR gate outputs a high signal (1) if any of its inputs are high.
- The NOT gate inverts the input signal; if the input is high (1), the output is low (0), and vice versa.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Digital Logic Design
**Ek line e:** Digital Logic Design

![Board 1: 0:10-3:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula


**Red Box 1 (Title):** Digital Logic Design

**Blue Box 2 (Definition):** analog → continuous value  
Digital → Discrete value

**Orange Box 3 (Formula):** (TTL) →5 volt (High) → Logic 1  
0 volt (Ground) → Logic 0  
Key → A  
c 011011

The lecturer explained that in digital logic design, we need to understand how computers work. Analog signals are continuous, whereas digital signals are discrete. For example, an analog signal like temperature or sound waves can vary continuously, but a computer processes signals that are either on or off, represented by zeros and ones.

**Mone rakho:** In digital systems, a light switch is a good example. When the switch is on, it represents a high voltage (Logic 1), and when it is off, it represents a low voltage (Logic 0). This means that a computer will only process zeros and ones. The computer uses these binary values to perform operations through logic gates, which are physical devices that create combinations of high and low voltages.

> Lecturer: "analog er kintu amader computer ki? analoge chole? naah. eta chole digital e."
> 
> Lecturer: "so, ei computer hocche logic one and logic zero niye shobshomoy kaaj korbe."

The key concept here is that digital systems use binary logic, where high voltage (5 volts) represents Logic 1 and low voltage (0 volts) represents Logic 0. When you press a key on a keyboard, it creates a combination of high and low voltages, which the computer interprets as binary data. These combinations are then processed by logic gates, which are the building blocks of digital circuits.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Digital Logic Design
**Ek line e:** Digital Logic Design covers various types of logic gates.

![Board 2: 3:20-5:50](figures_annotated/board_era2_320.jpg)

*Figure 2. The whiteboard during 3:20–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List


**Mone rakho:** We have discussed digital logic design and introduced several types of logic gates. These gates form the building blocks of digital circuits and are essential for performing logical operations.

1. **AND Gate**: The first type of logic gate we covered is the AND gate. It outputs a high signal (1) only if all its inputs are high. This gate is fundamental because it forms the basis for more complex logic operations.

2. **OR Gate**: Following the AND gate, we have the OR gate. This gate outputs a high signal (1) if any of its inputs are high. Like the AND gate, the OR gate is also a fundamental gate and is crucial for logical operations.

3. **NOT Gate**: The third type of gate is the NOT gate, which is also fundamental. It inverts the input signal; if the input is high (1), the output is low (0), and vice versa. This gate is essential for creating other logic functions.

4. **NOR Gate & NAND Gate**: Moving on to the NOR and NAND gates, these are considered universal gates. A universal gate means that any Boolean function can be implemented using just these gates. The NOR gate outputs a high signal only when all its inputs are low, while the NAND gate does the opposite—it outputs a high signal only when at least one input is low.

5. **X-OR Gate & X-NOR Gate**: Lastly, we have the X-OR and X-NOR gates, which are also important. The X-OR gate outputs a high signal if the number of high inputs is odd, while the X-NOR gate outputs a high signal if the number of high inputs is even. These gates are used in various applications where specific conditions need to be met.

6. **Exclusive Gate**: The final type of gate we discussed is the exclusive gate, which is essentially another name for the X-OR gate. This gate is used for making decisions based on specific conditions, similar to how the other gates operate.

The lecturer emphasized that these logic gates are used to make decisions in digital circuits. For instance, in a processor, millions of these gates work together to perform complex operations. Understanding these gates is crucial for designing and analyzing digital systems.

> Lecturer: "so, ei shakta logic gate ki korbe? ei shakta logic gate hocche amar decision making a kaaj korbe, je ekta connection ki hoy, wire er maddhome hoy, ekta connection korebhe hobe."

**Mone rakho:** In summary, the AND, OR, NOT, NOR, NAND, X-OR, and X-NOR gates are fundamental components of digital logic design. Each gate performs a specific logical operation and is essential for building complex digital circuits.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## AND Gate in Digital Logic Design
**Ek line e:** AND gate is a fundamental component in digital logic design.

![Board 3: 6:00-10:00](figures_annotated/board_era3_600.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Worked example


**Explanation:**
1. **Red Box 1 (Title):** The red box titled "Digital Logic Design" sets the context for the discussion on digital logic components.
2. **Blue Box 2 (Truth Table):** The blue box shows the truth table for an AND gate. It lists all possible combinations of inputs \(A\) and \(B\) and their corresponding output \(Y\). The table is as follows:
   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |
3. **Orange Box 3 (Gate Symbol):** The orange box illustrates the symbol for an AND gate. It shows how inputs \(A\) and \(B\) connect to the gate, which produces an output \(X\).
4. **Green Box 4 (Worked Example):** The green box provides a practical example of how the AND gate works. It uses the equation \(A \cdot B = X\) to show the output for different input combinations. The worked example also explains the relationship between the inputs and the output in terms of a light bulb, where 0 represents "light off" and 1 represents "light on."

**Quotes:**
> Lecturer: "so, ektu age amra jeta bollam, computer sudhu ki ki niye kaaj kore? zero and one."

**Mone rakho:** The AND gate takes two inputs and produces one output. For the inputs 0 and 0, the output is 0. For 0 and 1, the output is 0. For 1 and 0, the output is 0. For 1 and 1, the output is 1. This can be visualized using a truth table and a simple equation. In a real-world application, such as controlling a light bulb, 0 represents "light off" and 1 represents "light on."

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 1 (red): Digital Logic Design
**Ek line e:** Digital Logic Design

![Board 4: 10:10-11:00](figures_annotated/board_era4_1010.jpg)

*Figure 4. The whiteboard during 10:10–11:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


**Box 2 (blue): Truth table**
The truth table for the AND gate is shown here:
| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Box 3 (orange): Gate symbol**
The gate symbol for the AND gate is:
A B AND gate X

**Box 4 (green): Formula**
The formula for the AND gate is:
A B X = AB

**Mone rakho:** The AND gate takes two inputs, A and B, and produces an output Y which is the result of their multiplication. So, if either A or B is zero, the output will also be zero. This is because the AND operation requires both inputs to be one for the output to be one.


**Mone rakho:** Next, we will move on to the OR gate. The pattern for the OR gate will be similar to the AND gate. We will have a physical device called an OR gate, which will take two inputs and produce one output.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Box 2 (blue) and Box 3 (orange) on the whiteboard
**Ek line e:** Digital Logic Design

![Board 5: 11:10-13:00](figures_annotated/board_era5_1110.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Truth table · 3 Gate symbol · 4 Formula


The orange box 3 shows the gate symbol for an OR gate, which is represented as \( A \text{ OR } B \rightarrow X \). The blue box 2 provides the truth table for the OR gate, where the inputs \( A \) and \( B \) produce the output \( X \).

- **Truth Table in Box 2 (blue):**
  - \( A \) | \( B \) | \( X \)
  - 0 | 0 | 0
  - 0 | 1 | 1
  - 1 | 0 | 1
  - 1 | 1 | 1

- **Gate Symbol in Box 3 (orange):**
  - \( A \text{ OR } B \rightarrow X \)

The green box 4 gives the formula for the OR gate, which is \( A + B = X \).

> Lecturer: "suppose input ta hocche a and output ta hocche b. so amar output jeta there hobe, seta hocche x."

**Mone rakho:** The OR gate outputs a 1 if any of the inputs are 1. For example, if both inputs are 0, the output is 0. If one input is 1, the output is 1. This is true regardless of the other input's value.

> Lecturer: "okay, ekhon or gete jeta hoy, x equals to hobe a plus b. tar mane, zero plus zero equals to hobe zero. zero plus one equals to ibar kintu hoye jabe one."

**Mone rakho:** The OR gate can be represented by the formula \( A + B = X \). For instance, when both inputs are 0, the output is 0. When one input is 0 and the other is 1, the output is 1. This holds true for all combinations of inputs.

> Lecturer: "then zero plus, one, zero, one plus zero equals to abar one. then zero one plus one equals to hobe one."

**Mone rakho:** The OR gate will output 1 if either or both of the inputs are 1. For example, if the inputs are 0 and 1, the output is 1. Similarly, if the inputs are 1 and 0, the output is also 1.

Next, we will look at the logic circuit representation of the OR gate, where inputs \( A \) and \( B \) are connected to an OR gate, producing the output \( X \).

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Digital Logic Design
**Ek line e:** NOT gate: (Inverter)

![Board 6: 13:10-14:50](figures_annotated/board_era6_1310.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table · 4 Block diagram · 5 Gate symbol


**Explanation:**
1. **Box 1 (red):** The title of the board is "Digital Logic Design", which sets the context for the discussion on digital circuits and logic gates.
2. **Box 2 (blue):** The NOT gate, also known as an inverter, is defined as a device that takes one input and produces an output that is the logical opposite of the input. This means if the input is 0, the output will be 1, and if the input is 1, the output will be 0.
3. **Box 3 (orange):** The truth table for the NOT gate is provided, showing the relationship between the input \( A \) and the output \( \overline{A} \). It clearly illustrates that when \( A = 0 \), \( \overline{A} = 1 \), and when \( A = 1 \), \( \overline{A} = 0 \).
4. **Box 4 (green):** A block diagram of the NOT gate is shown, indicating the flow of data: \( A \) goes into the NOT gate and comes out as \( \overline{A} \). An alternative notation is also given, where \( A \) is directly connected to \( \overline{A} \) through the NOT gate.
5. **Box 5 (purple):** The symbol for the NOT gate is depicted, showing the input \( A \) and the output \( \overline{A} \).

**Quotes:**
> Lecturer: "not get a ki hoy? amar je physical device ta seikhane just ekta ei input ber dhukbe and ekta ei output ber hobe."
> Lecturer: "tar mane ki? tar mane hocche amar input a and output a bar."

**Mone rakho:** The NOT gate, or inverter, is a fundamental component in digital logic design. It takes an input and produces an output that is the logical opposite of the input. The truth table and block diagram clearly illustrate this behavior. The NOT gate is represented by the symbol \( A \rightarrow \overline{A} \).

---

## Check yourself
1. What are the two main types of signals in digital systems?
2. Name three fundamental logic gates.
3. How does an AND gate determine its output?
4. What is the output of an OR gate when both inputs are 0?
5. What does a NOT gate do to its input?

### Answers
1. The two main types of signals in digital systems are analog and digital. Analog signals are continuous, whereas digital signals are discrete.
2. Three fundamental logic gates are AND, OR, and NOT.
3. An AND gate outputs a high signal (1) only if all its inputs are high.
4. The output of an OR gate when both inputs are 0 is 0.
5. A NOT gate inverts the input signal; if the input is high (1), the output is low (0), and vice versa.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 9 kept, 1 removed. References to boxes that do not exist: 0.*
