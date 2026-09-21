# Digital Logic Design

This lecture introduces the basics of digital logic design, focusing on the fundamental concepts of digital signals and logic gates.

## Key takeaways
- Digital signals are discrete values, represented by 0 and 1.
- Logic gates are the building blocks of digital circuits.
- AND gate, OR gate, and NOT gate are fundamental logic gates.
- The AND gate outputs 1 only when both inputs are 1.

## Digital Signals and Logic Gates
Digital signals are discrete values, represented by 0 and 1. In contrast, analog signals are continuous values. For digital systems, the computer uses discrete values, such as 0 (off) and 1 (on), to represent information.

### TTL Logic Levels
TTL (Transistor-Transistor Logic) is a type of digital circuitry. In TTL, a high voltage level (5 volts) represents logic 1, while a low voltage level (0 volts) represents logic 0.

![Board 0:10-3:10](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:10–3:10, reconstructed from 9 video frames with the lecturer removed; 97% of the board is unobstructed.*

## Logic Gates
Logic gates are the basic components of digital circuits. We will cover several types of logic gates: AND, OR, NOT, NOR, NAND, XOR, and XNOR.

### AND Gate
The AND gate outputs 1 only when both inputs are 1. It can be visualized as a physical device that takes two inputs and produces an output based on their combination.

#### Example
| A | B | X |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

A --- AND --- X
B --- gate

Bulb bulb
↑       ↑
A . B = X

0 . 0 = 0
0 . 1 = 0
1 . 0 = 0
1 . 1 = 1

0 → Light OFF
1 → Light ON

![Board 6:00-10:00](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed from 9 video frames with the lecturer removed; 98% of the board is unobstructed.*
![Board 10:10-11:00](figures_board/board_04_era4.jpg)

*Figure 4. The whiteboard during 10:10–11:00, reconstructed from 4 video frames with the lecturer removed; 98% of the board is unobstructed.*

### OR Gate
The OR gate outputs 1 if at least one of the inputs is 1.

#### Example
| A | B | X |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

A + B = X

![Board 11:10-13:00](figures_board/board_05_era5.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed from 8 video frames with the lecturer removed; 97% of the board is unobstructed.*

### NOT Gate
The NOT gate, also known as an inverter, inverts the input. If the input is 0, the output is 1, and vice versa.

#### Example
| A | ¬A |
|---|-----|
| 0 | 1   |
| 1 | 0   |

A → NOT → ¬A
alternate of A

A → ¬A

![Board 13:10-14:50](figures_board/board_06_era6.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed from 7 video frames with the lecturer removed; 97% of the board is unobstructed.*

## Check Yourself
1. What are digital signals?
2. What does the AND gate output when both inputs are 1?
3. How many inputs does an OR gate need to output 1?
4. What is the output of a NOT gate when the input is 0?
5. Draw the truth table for an AND gate.

## Answers
1. Digital signals are discrete values, represented by 0 and 1.
2. The AND gate outputs 1 when both inputs are 1.
3. An OR gate needs at least one input to be 1 to output 1.
4. The output of a NOT gate is 1 when the input is 0.
5. | A | B | X |
     |---|---|---|
     | 0 | 0 | 0 |
     | 0 | 1 | 0 |
     | 1 | 0 | 0 |
     | 1 | 1 | 1 |

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*