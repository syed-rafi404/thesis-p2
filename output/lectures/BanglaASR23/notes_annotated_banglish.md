# BanglaASR23: Red and Blue Stickers on the Whiteboard
CSE 461 Control theory

## Key takeaways
- Red and blue stickers on the whiteboard indicate different concepts in control theory.
- Basic concepts of a closed-loop system, including input, error calculation, actuation, and feedback loop.
- Understanding transient and steady states, threshold voltage, and the impact of external factors.
- Rise time and its significance in system response.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red and Blue Stickers on the Whiteboard
**Ek line e:** CSE 461 Control theory

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

> Lecturer: "ekhon olexomai amon hoy ki, je hocche amader electronic device ke amader khubi mane, eta ki bae bujha no jeje khubi aa unpredictable, kokhon ki hobe, bola jay na."

### Extra jana kotha
In a closed-loop system, the output is continuously adjusted based on the error between the desired and actual states. This ensures that the system remains stable even when faced with external disturbances. Understanding these concepts is crucial for designing robust control systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Blue Sticker: CSE 461 Control Theory
**Ek line e:** Amader aman jokhon amader gulume switch chalo bollam, switch ta kintu hocche, amader human er kache lagge je hae, chab deo shom e shom e switch ta chalo hoy decchi, amader babna jole huttese.

![Board 2: 8:20-15:36](figures_annotated/board_era2_820.jpg)

*Figure 2. The whiteboard during 8:20–15:36, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Graph · 3 Formula


1. **Box 1 (red):** SUPER BOARD S
2. **Box 2 (blue):** CSE 461 Control theory
3. **Box 3 (orange):** 5 -> 0.9

The lecturer explains that when we talk about a switch, it represents a momentary change in state, which can be seen as a delay in our human perception. For example, if we consider a switch turning on and off, there is a delay of 0.01 milliseconds.

- **Box 2 (blue):** The graph shows the transient time and steady state of a system. The transient time is the period during which the system moves from one state to another, while the steady state is the final stable state.

The lecturer gives an example where a switch is turned on and off, connecting a light bulb. When the switch is on, the light bulb turns on, and when the switch is off, the light bulb turns off. This is a simple scenario where the expected output is 5 volts.

- **Box 3 (orange):** The formula 5 -> 0.9 indicates the threshold voltage, where the system transitions from one state to another. Here, the threshold is 4.5 volts.

The lecturer explains that in real-world scenarios, there are external factors that can affect the system. For instance, in a real case, the system might have a higher threshold due to various components behaving differently. This can lead to errors in the system, such as overshooting the desired output.

- **Box 2 (blue):** The transient time is the period during which the system moves from the initial state to the steady state. The steady state is the final stable state of the system. In the example given, the transient time is the period during which the system moves from 0 volts to 5 volts and back to 4.8 volts.

The lecturer further explains that in practice, achieving a perfect steady state of 5 volts is not always possible due to factors like resistance. The system might oscillate around the steady state, such as between 4.8 volts and 5.2 volts.

- **Box 2 (blue):** The transient period is the time taken for the system to settle into the steady state after a disturbance. In the example, the transient period is the time taken for the system to move from the initial state to the steady state and back.

The lecturer concludes that understanding these concepts helps in designing better control systems. The graph on the board visually represents the transient and steady states, showing how the system behaves over time.

**Mone rakho:** Switch, transient time, steady state, threshold voltage, external factors, overshoot, control system, transient period.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Sticker: SUPER FORMICA SUPER BOARD
**Ek line e:** Amader egulor vivinno state e bhag kora hoy.

![Board 3: 15:40-19:22](figures_annotated/board_era3_1540.jpg)

*Figure 3. The whiteboard during 15:40–19:22, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Diagram


1. **Box 1 (red):** Amader egulor vivinno state e bhag kora hoy. Je amra boli, ei toko jodi amader 0.2 dhori, ar 4.8 er monek orla hocche, faa amader 90% erokom jodi amader jodi amader 0.2 dhori, ar 4.8 er monek korla hocche, faa amader 90% erokom jodi amader jodi amader 0.2 dhoro.
2. **Box 2 (blue):** Diagram: Control theory 5.2V 5V 4.8 4.5 90% 10% Rise time(t_r) Transient time

> Lecturer: "ekhon apna dekhean je hocche amader egulor vivinno state e bhag kora hoy."

3. **Box 1 (red):** Thikache eitu gure hocche 90 percent dhollam. eitu gure dholam 10 percent. achar 10 percent e homo khena 1 volt dhorai. tu make sense korona 0.2. kine 1 volt dhorai which is 10 percent, ara ekhane 5 volt ka 90 percent 4.80 er eitu kase kache 4.9 dhorai bar thikache dhulam ar ki.
4. **Box 1 (red):** Ekhon shobar age eitichu basic fenomen er nasi gula boner janthe hbe, which is the must.

> Lecturer: "ei je amna 1 volt ache, ei gula shob e hocche ami explain korbo, toh first of all, rice time hocche ei je 1 volt ache, ei 1 volt theke je 4.8 porjontoi, ei je 8 point theke ei point porjontu, portre joto chuk shomelate sheta hocche ami rice time."

5. **Box 1 (red):** Thikache? Eigula kintu porikhar jono khob e important mane finally ekhane te concept ke ol question ashe and even amader final o ashchilo, so eta jana must.

> Lecturer: "so rice time holo t-ar boli abra."

6. **Box 1 (red):** So basically eita mane amader bolteche je, eta koto fast machine ta response korte pare. for example, jekone ekta certain change e, duei e rice time kom hoy, taro mane ki, one quick response kore. mane rice time ta ki? time jode kom, response ta ta totu tele faster.

7. **Box 1 (red):** Accha ami graph ta ektu ya kori. a ekta shundor gula try kori graph ta. khub e methi laghtese. and ami green color er painting. use koru pekhane. khub e vaje laghtese graph ta. ektu khara bortla kaina. yes. yes perfect, perfect!

8. **Box 1 (red):** Okay, so hocche ekhane 4.5 er etta. okay guys, jeta bolte silam, je amode rise time hocche ei 10% theke, 90% utha je time eita hocche moddhe tr. thikase?

9. **Box 1 (red):** Okay, toh omoder ekhon rice time dey bujhte parlem. erpor bujhte pey time. pey time mane hocche konta ei je highest point er jeta kese amar graph, highest point er jeta kese amar tp.

**Mone rakho:** Rise time, 90% of the rise, 10% of the rise, highest point, transient time.

---

## Check yourself
1. What does the red box 1 on the whiteboard indicate?
2. Explain the concept of rise time in a control system.
3. What is the significance of the 90% and 10% points in the rise time calculation?
4. How does the threshold voltage affect the system's behavior?
5. What are the transient and steady states in a control system?

### Answers
1. The red box 1 on the whiteboard indicates the brand of the board used (SUPER FORNICA SUPER BOARD S).
2. Rise time in a control system is the time taken for the system to move from 10% of the final value to 90% of the final value after a step change in input.
3. The 90% and 10% points in the rise time calculation help determine the speed of the system's response to a change in input.
4. The threshold voltage affects the system's behavior by determining the point at which the system transitions from one state to another.
5. The transient state is the period during which the system moves from the initial state to the steady state, while the steady state is the final stable state of the system.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
