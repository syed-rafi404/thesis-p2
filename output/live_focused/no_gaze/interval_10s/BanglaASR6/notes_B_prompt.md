# Digital Logic Design Lecture Notes

In this lecture, we explore the basics of digital logic design, focusing on understanding digital signals and fundamental logic gates.

## Key takeaways
- Digital signals are discrete values, typically represented as 0 and 1.
- Logic gates are the building blocks of digital circuits.
- AND, OR, NOT, NAND, NOR, XOR, and XNOR gates are fundamental logic gates.
- An inverter is a NOT gate that inverts the input signal.

## Introduction to Digital Logic Design
Digital logic design involves understanding how computers process information using discrete values. Unlike analog systems, which use continuous values, digital systems use binary values (0 and 1).

### Analog vs. Digital
Analog signals represent continuous values, like temperature or sound waves. Digital signals, on the other hand, represent discrete values, such as the state of a light switch (on/off) or a computer's binary states (0/1).

![Board 0:10-3:10](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed from 9 video frames with the lecturer removed; 97% of the board is unobstructed.*

### TTL Logic Levels
TTL (Transistor-Transistor Logic) is a type of digital circuitry. In TTL, a high voltage level is 5V, and a low voltage level is 0V. These levels correspond to logic 1 and logic 0, respectively.

### Example: Light Switch
A light switch is a simple example of a digital signal. It can be either on (logic 1) or off (logic 0). Similarly, a computer processes data using binary digits (bits) that can be either 0 or 1.

## Fundamental Gates
We will discuss several fundamental logic gates and their functions.

### AND Gate
The AND gate outputs 1 only if both inputs are 1. Otherwise, it outputs 0.

#### Example
- Inputs: A = 0, B = 0 → Output: X = 0
- Inputs: A = 0, B = 1 → Output: X = 0
- Inputs: A = 1, B = 0 → Output: X = 0
- Inputs: A = 1, B = 1 → Output: X = 1

![Board 3:20-5:50](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 3:20–5:50, reconstructed from 8 video frames with the lecturer removed; 97% of the board is unobstructed.*

### NOT Gate
The NOT gate inverts the input signal. If the input is 0, the output is 1, and vice versa.

#### Example
- Input: A = 0 → Output: X = 1
- Input: A = 1 → Output: X = 0

### OR Gate
The OR gate outputs 1 if at least one of the inputs is 1. Otherwise, it outputs 0.

#### Example
- Inputs: A = 0, B = 0 → Output: X = 0
- Inputs: A = 0, B = 1 → Output: X = 1
- Inputs: A = 1, B = 0 → Output: X = 1
- Inputs: A = 1, B = 1 → Output: X = 1

### NAND and NOR Gates
NAND and NOR gates are universal gates, meaning they can implement any Boolean function.

### XOR and XNOR Gates
XOR (exclusive OR) and XNOR (exclusive NOR) gates perform specific logical operations.

## Check Yourself
1. What is the output of an AND gate when both inputs are 0?
2. What is the output of a NOT gate when the input is 1?
3. What is the output of an OR gate when both inputs are 1?
4. What is the difference between an AND gate and an OR gate?
5. What are universal gates?

## Answers
1. The output of an AND gate when both inputs are 0 is 0.
2. The output of a NOT gate when the input is 1 is 0.
3. The output of an OR gate when both inputs are 1 is 1.
4. An AND gate outputs 1 only if both inputs are 1, while an OR gate outputs 1 if at least one input is 1.
5. Universal gates (NAND and NOR) can implement any Boolean function.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*