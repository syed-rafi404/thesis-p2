# Digital Logic Design

This lecture introduces the basics of digital logic design, focusing on understanding how computers process information using discrete values.

## Key takeaways
- Digital signals are discrete values, while analog signals are continuous.
- Logic gates perform basic operations like AND, OR, and NOT.
- AND, OR, and NOT gates are fundamental building blocks of digital circuits.
- The AND gate outputs 1 only when both inputs are 1.

## Digital vs Analog Signals
Digital signals represent information using discrete values, whereas analog signals represent information using continuous values. For example, temperature and sound waves are analog signals, but computers process information using digital signals.

### Digital Signal Example
- **Example**: A light switch can be in two states: `ON` (1) or `OFF` (0).

### Binary Logic
The concept of binary logic involves representing information using `0` and `1`. This is the basis of digital computing.

## Logic Gates
Logic gates are the basic building blocks of digital circuits. They perform simple logical operations on binary inputs.

### AND Gate
An AND gate takes two inputs and produces an output based on the AND operation.

#### Worked Example
- **Inputs**: A = 0, B = 0
- **Output**: X = 0 (0 AND 0 = 0)
- **Inputs**: A = 0, B = 1
- **Output**: X = 0 (0 AND 1 = 0)
- **Inputs**: A = 1, B = 0
- **Output**: X = 0 (1 AND 0 = 0)
- **Inputs**: A = 1, B = 1
- **Output**: X = 1 (1 AND 1 = 1)

```plaintext
A --- AND --- X
B --- gate
```

![Board 6:00-10:00](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 6:00–10:00, reconstructed from 9 video frames with the lecturer removed; 98% of the board is unobstructed.*

### OR Gate
An OR gate takes two inputs and produces an output based on the OR operation.

#### Worked Example
- **Inputs**: A = 0, B = 0
- **Output**: X = 0 (0 OR 0 = 0)
- **Inputs**: A = 0, B = 1
- **Output**: X = 1 (0 OR 1 = 1)
- **Inputs**: A = 1, B = 0
- **Output**: X = 1 (1 OR 0 = 1)
- **Inputs**: A = 1, B = 1
- **Output**: X = 1 (1 OR 1 = 1)

![Board 11:10-13:00](figures_board/board_05_era5.jpg)

*Figure 5. The whiteboard during 11:10–13:00, reconstructed from 8 video frames with the lecturer removed; 97% of the board is unobstructed.*

### NOT Gate
A NOT gate (inverter) takes one input and produces an output that is the inverse of the input.

#### Worked Example
- **Input**: A = 0
- **Output**: ¬A = 1
- **Input**: A = 1
- **Output**: ¬A = 0

![Board 13:10-14:50](figures_board/board_06_era6.jpg)

*Figure 6. The whiteboard during 13:10–14:50, reconstructed from 7 video frames with the lecturer removed; 97% of the board is unobstructed.*

## Check Yourself
1. What is the output of an AND gate when both inputs are 0?
2. What is the output of an OR gate when both inputs are 1?
3. What is the output of a NOT gate when the input is 1?

## Answers
1. The output of an AND gate when both inputs are 0 is 0.
2. The output of an OR gate when both inputs are 1 is 1.
3. The output of a NOT gate when the input is 1 is 0.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*
