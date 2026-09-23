# BanglaASR23 Lecture: BanglaASR23
<ek line: ei lecture e ki cover kora hoyeche>

## Key takeaways
- Ekhon olexomai amon hoy ki, je hocche amader electronic device ke amader khubi mane, eta ki bae bujha no jeje khubi aa unpredictable, kokhon ki hobe, bola jay na.
- Switch, transient time, steady state, threshold voltage, external factors, overshoot, control system, transient period.
- Rise time, 90% of the rise, 10% of the rise, highest point, transient time.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red and Blue Stickers on the Whiteboard
**In one line:** CSE 461 Control theory

![Board 1: 0:00-8:16](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–8:16, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Block diagram


- **Red Box 1 (SUPERFORNICA SUPER BOARD S)**: This sticker indicates the brand of the board used.
- **Blue Box 2 (Block diagram: CSE 2 G1 Control theory)**: This block diagram represents the basic components of a control system.

### Explanation
The lecturer starts by explaining the basics of a closed-loop system, which is a fundamental concept in control theory. He explains that a closed-loop system uses feedback to adjust the output based on the difference between the desired input and the actual output.

1. **Input and Command**: The lecturer mentions that the first step in a closed-loop system is to take a command input. This command is given at specific time intervals, `t`. The system then measures the output using sensors.
   
2. **Error Calculation**: After obtaining the sensor measurements, the system calculates the error by comparing the command input with the sensor readings. The error is calculated as the difference between the desired output and the actual output.

3. **Actuation**: The next step involves actuating the system based on the calculated error. The lecturer explains that the actuator receives an actuation command, which is essentially a signal to perform a specific action.

4. **Addition and Subtraction**: The lecturer draws an addition symbol to represent the summation of different inputs and outputs. He explains that in a control system, you can add or subtract signals based on their signs. For example, if there is an external disturbance, it is added to the system to account for it.

5. **Feedback Loop**: The lecturer emphasizes the importance of considering external disturbances and how they affect the system. He explains that these disturbances are added to the error calculation to ensure the system remains stable.

6. **Stability**: The lecturer discusses the concept of stability in a closed-loop system. He gives an example of a drone that needs to maintain a specific altitude. Even though the drone might experience unexpected movements, the system should be able to correct these movements using feedback.

7. **Controller**: The lecturer explains that a controller is used to manage the feedback and ensure the system remains stable. He provides an example of a server motor, which needs to maintain a specific position under varying conditions.


### Background (not said in the lecture)
In a closed-loop system, the output is continuously adjusted based on the error between the desired and actual states. This ensures that the system remains stable even when faced with external disturbances. Understanding these concepts is crucial for designing robust control systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Blue Sticker: CSE 461 Control Theory
**In one line:** Amader aman jokhon amader gulume switch chalo bollam, switch ta kintu hocche, amader human er kache lagge je hae, chab deo shom e shom e switch ta chalo hoy decchi, amader babna jole huttese.

![Board 2: 8:20-15:36](figures_annotated/board_era2_820.jpg)

*Figure 2. The whiteboard during 8:20–15:36, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Graph · 3 Formula


1. **Box 1 (red):** SUPER BOARD S
2. **Box 2 (blue):** CSE 461 Control theory
3. **Box 3 (orange):** 5 -> 0.9

The lecturer said: "When we talk about a switch, it represents a momentary change in state, which can be seen as a delay in our human perception. For example, if we consider a switch turning on and off, there is a delay of 0.01 milliseconds."

- **Box 2 (blue):** The graph shows the transient time and steady state of a system. The transient time is the period during which the system moves from one state to another, while the steady state is the final stable state.

The lecturer said: "In the example where a switch is turned on and off, connecting a light bulb, when the switch is on, the light bulb turns on, and when the switch is off, the light bulb turns off. This is a simple scenario where the expected output is 5 volts."

- **Box 3 (orange):** The formula 5 -> 0.9 indicates the threshold voltage, where the system transitions from one state to another. Here, the threshold is 4.5 volts.

The lecturer said: "In real-world scenarios, there are external factors that can affect the system. For instance, in a real case, the system might have a higher threshold due to various components behaving differently. This can lead to errors in the system, such as overshooting the desired output."

- **Box 2 (blue):** The transient time is the period during which the system moves from the initial state to the steady state. The steady state is the final stable state of the system. In the example given, the transient time is the period during which the system moves from 0 volts to 5 volts and back to 4.8 volts.

The lecturer said: "In practice, achieving a perfect steady state of 5 volts is not always possible due to factors like resistance. The system might oscillate around the steady state, such as between 4.8 volts and 5.2 volts."

- **Box 2 (blue):** The transient period is the time taken for the system to settle into the steady state after a disturbance. In the example, the transient period is the time taken for the system to move from the initial state to the steady state and back.

The lecturer concluded: "Understanding these concepts helps in designing better control systems. The graph on the board visually represents the transient and steady states, showing how the system behaves over time."

**Remember:** Switch, transient time, steady state, threshold voltage, external factors, overshoot, control system, transient period.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Sticker: SUPER FORMICA SUPER BOARD
**One Line:** We divide our regular voltage state.

![Board 3: 15:40-19:22](figures_annotated/board_era3_1540.jpg)

*Figure 3. The whiteboard during 15:40–19:22, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Diagram


1. **Box 1 (red):** We divide our regular voltage state. If we say, this means that if we have 0.2 volts and 4.8 volts, then if we increase by 0.2 volts and 4.8 volts, then if we increase by 0.2 volts, we are at 90%. If we increase by 0.2 volts and 4.8 volts, then if we increase by 0.2 volts, we are at 90%.
2. **Box 2 (blue):** Diagram: Control theory 5.2V 5V 4.8 4.5 90% 10% Rise time(t_r) Transient time

> Lecturer: "Now let's see what happens when we divide our regular voltage state."

3. **Box 1 (red):** So, we have 90 percent here. We have 10 percent here. For the remaining 10 percent, we drop by 1 volt. This makes sense for 0.2 volts. If we drop by 1 volt, which is 10 percent, then here 5 volts is 90 percent, so we get 4.80. So, we are at 4.9 volts and we drop.
4. **Box 1 (red):** We need to understand some basic phenomena, which is essential.

> Lecturer: "This is just 1 volt, I will explain this, first of all, rise time is the time when it goes from 1 volt to 4.8 volts."

5. **Box 1 (red):** Is that correct? So, this is important, meaning finally, this concept is the key, and even in our final answer, we must understand this.

> Lecturer: "So, rise time is the time when it rises."

6. **Box 1 (red):** So, basically, this means that we are saying how quickly the machine can respond. For example, if there is a certain change, the rise time is short, which means it responds quickly. What is rise time? It is the time that is short, and the response is very fast.

7. **Box 1 (red):** Alright, so let's draw the graph. I will draw a nice one. It should be clear. And I will use the green color to mark it. It should be clear on the graph. A bit darker. Yes, yes, perfect, perfect!

8. **Box 1 (red):** Okay, so here we have 4.5 volts. Okay guys, as we said, the rise time is from 10% to 90%, so what is the time between these two points?

9. **Box 1 (red):** Okay, now we understand the rise time. The time we need to measure is the time from the lowest point to the highest point on the graph, which is the peak point.

**Mention:** Rise time, 90% of the rise, 10% of the rise, highest point, transient time.

---

## Check yourself
1. What does the red sticker on the whiteboard indicate?
2. Explain the concept of rise time in a control system.
3. What is the significance of the 90% rise in a control system?
4. How does the transient time differ from the steady state?
5. What does the blue sticker on the whiteboard represent?

### Answers
1. The red sticker on the whiteboard indicates the brand of the board used.
2. The rise time in a control system is the time taken for the system to move from 10% of its final value to 90% of its final value.
3. The 90% rise in a control system signifies the time taken for the system to reach 90% of its final value from its initial state.
4. Transient time is the period during which the system moves from the initial state to the steady state, while the steady state is the final stable state of the system.
5. The blue sticker on the whiteboard represents the basic components of a control system and the graph showing the transient time and steady state.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (3 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
