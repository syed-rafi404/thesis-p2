# CSE 361 Control theory
CSE 461 Control theory is covered in this lecture, focusing on the fundamentals of control systems and the PID controller.

## Key takeaways
- CSE 461
- Control theory
- PID
- Proportional
- Integral
- Derivative
- Rise time
- Peak time
- Overshoot
- Settling time

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Red Box 1: SUPER BOARD S
**Ek line e:** CSE 461 Control theory

![Board 1: 0:30-4:50](figures_annotated/board_era1_030.jpg)

*Figure 1. The whiteboard during 0:30–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Block diagram · 3 Title


- The lecturer starts by introducing the topic of control theory, specifically focusing on the PID controller.
- The red box 1 introduces the title "CSE 461 Control theory," setting the context for the lecture.
- The lecturer explains that the goal is to understand the components of a control system, such as rise time, peak time, overshoot, and settling time.

### Extra jana kotha
Understanding the basics of control theory is crucial for analyzing and designing control systems. The PID controller, which stands for Proportional, Integral, and Derivative, is a fundamental component in many control systems. By grasping these concepts, students can better comprehend how different parts of a control system interact to achieve desired performance.

**Mone rakho:** CSE 461, Control theory, PID, Proportional, Integral, Derivative, Rise time, Peak time, Overshoot, Settling time

---

## Blue Box 2: Block Diagram
**Ek line e:** PID Proportional Integral Derivative Error Error loop

![Board 1: 0:30-4:50](figures_annotated/board_era1_030.jpg)

*Figure 1. The whiteboard during 0:30–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Block diagram · 3 Title


- The blue box 2 presents a block diagram of the PID controller, highlighting the key components: Proportional, Integral, Derivative, and Error.
- The diagram also shows an error loop, indicating the feedback mechanism in the system.

### Explanation
- The lecturer explains that the PID controller consists of three main components: Proportional, Integral, and Derivative.
- Proportional control is introduced first. The lecturer uses the analogy of Newton's famous equation  F = ma  to illustrate the concept of proportionality. He explains that if force ( F ) is proportional to mass ( m ) times acceleration ( a ), then any change in mass or acceleration will result in a corresponding change in force.
- The lecturer further clarifies that proportional control involves using the error (difference between the desired value and the actual value) to adjust the output. For example, if the drone needs to reach a certain RPM, but the current RPM is different, the proportional controller will adjust the output based on this error.
- The formula for a proportional controller is given as  output = error x gain . Here, the error is multiplied by a gain factor to determine the output adjustment.
- The lecturer emphasizes that the error will decrease over time until it reaches zero, as the system tries to match the desired value with the actual value.
- The gain term represents the sensitivity of the system to the error. If the gain is zero, the system will not respond to any error, meaning the drone's propellers will not receive any additional power. This scenario is not practical, so the lecturer explains the importance of having a non-zero gain to ensure the system responds appropriately to errors.

**Mone rakho:** Proportional control, error, gain, output adjustment, feedback, proportional controller formula, gain sensitivity, error reduction, system response

---

## Orange Box 3: Title
**Ek line e:** CSE 361 Control theory

![Board 1: 0:30-4:50](figures_annotated/board_era1_030.jpg)

*Figure 1. The whiteboard during 0:30–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Block diagram · 3 Title


- The orange box 3 reiterates the title "CSE 361 Control theory," reinforcing the focus of the lecture.

### Explanation
- The lecturer defines proportional control as a method where the output is directly proportional to the error. He explains that this relationship can be expressed mathematically as  output = error x gain .
- The lecturer uses the example of a drone to illustrate how proportional control works. He explains that if the drone needs to reach a specific RPM, but the current RPM is different, the proportional controller will adjust the output based on this error.
- The lecturer emphasizes that the error will continue to decrease until it reaches zero, ensuring that the system converges to the desired value.
- The gain term is crucial as it determines how responsive the system is to the error. A non-zero gain ensures that the system can correct itself effectively.

**Quotes**
> Lecturer: "so, ekhaneo amra jodi ekta variable er jeta korte hobe, chacchi, amra jodi ekhane ki? amra jodi ekhane ki? amra jodi ekhane ki? variable er korte hobe? variable er korte hobe? derivative er korte hobe derivative er korte hobe, derivative er"

**Mone rakho:** Proportional control, error, gain, output adjustment, feedback, proportional controller formula, gain sensitivity, error reduction, system response

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Blue Box 2: Control Theory Diagram
**Ek line e:** This diagram explains the components of a PID controller and how they interact.

![Board 2: 5:00-6:30](figures_annotated/board_era2_500.jpg)

*Figure 2. The whiteboard during 5:00–6:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Control Theory Diagram


- **Box 2 (blue):** The blue box shows a control theory diagram labeled "PI -> PID". This diagram illustrates the relationship between different components of a PID controller: Proportional (P), Integral (I), and Derivative (D).

- **Proportional (P):** The proportional component multiplies the error by a gain factor. It reacts immediately to changes in the error but can cause oscillations if used alone.

- **Integral (I):** The integral component accumulates the error over time and adds it to the output. This helps reduce steady-state error but can also lead to overshooting and oscillations.

- **Derivative (D):** The derivative component measures the rate of change of the error. It helps dampen oscillations and improve stability. However, it requires a good understanding of the system dynamics to be effective.

- **Error:** The error is the difference between the desired setpoint and the actual process variable. It is multiplied by gain factors for P, I, and D components.

- **Σ^n Error x gain:** This notation represents the summation of the error multiplied by the gain over multiple time intervals, which is characteristic of the integral component.

- **More Oscillation:** The diagram highlights that using just the derivative component can sometimes increase oscillations, making it necessary to balance all three components (P, I, and D) for optimal performance.

> Lecturer: "ei je more obscalation eita handle kora jorlo obar, amra use kore derivative."

### Extra jana kotha
In control theory, a PID controller combines proportional, integral, and derivative actions to achieve stable and precise control. While the derivative action can help reduce oscillations, it needs to be balanced with the other components to avoid unwanted behavior. Understanding the system dynamics is crucial for effective tuning of these parameters.

<!-- boxes: 1=#d62828 -->
## Red Box 1: Control Theory - PID and Ziegler's Theorem
**Ek line e:** Today, we will discuss Ziegler's theorem for finding the gain of a P controller.

![Board 3: 6:40-9:40](figures_annotated/board_era3_640.jpg)

*Figure 3. The whiteboard during 6:40–9:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Control theory


1. **Red Box 1 (Control theory):** The board introduces Ziegler's theorem, which helps in determining the gain for a P controller using trial and error methods. This theorem is specifically useful for PID controllers, where the P controller is the first step.

2. **Ziegler's Theorem:** The lecturer explains that Ziegler's theorem provides a method to find the gain for a P controller by testing different values until a stable system is achieved. For an I controller, the process is similar but involves additional steps.

3. **P Controller Gain:** The lecturer emphasizes that for a P controller, the gain is determined based on the oscillation period of the system. The gain is calculated as 1.2 divided by the oscillation period. This value is used to ensure the system remains stable without oscillations.

4. **I Controller:** The lecturer mentions that for an I controller, the same principle applies, but the focus is on eliminating steady-state errors. By integrating the proportional term, the system can achieve better stability and reduce steady-state errors.

5. **Derivative Term:** The derivative term in the PID controller is also discussed. It works by calculating the difference between two consecutive errors and optimizing the system response over time. The oscillation period is crucial here, as it helps in determining the optimal derivative gain.

6. **Example Calculation:** The lecturer gives an example where the oscillation period is 1.2 seconds. Using Ziegler's theorem, the gain for the P controller is calculated as 0.5 times the oscillation period, resulting in a gain of 0.6.

**Mone rakho:** Ziegler's theorem helps in finding the gain for a P controller by using the oscillation period of the system. The gain is calculated as 0.5 times the oscillation period, ensuring the system remains stable without oscillations.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Red Box 1: SUPER BOARD
**Ek line e:** This board summarizes key concepts from our discussion on PID controllers and Ziegler's theorem.

![Board 4: 9:50-11:40](figures_annotated/board_era4_950.jpg)

*Figure 4. The whiteboard during 9:50–11:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Block diagram · 3 Formula


- **Box 1 (red):** The board starts with the course title, "CSE 461 Control theory," emphasizing the subject matter.
- **Box 2 (blue):** A block diagram is shown, representing the components of a PID controller: Proportional, Integral, and Derivative. Ziegler's theorem is also mentioned, indicating its relevance to the PID controller design.
- **Box 3 (orange):** The formula for the PID controller parameters is displayed:  k_p = 0.6 x k ,  k_i = \frac{2}{P} , and  k_d = \frac{P}{8} . Here,  k  is the gain of the proportional controller,  P  is the period of oscillation, and  k_p ,  k_i , and  k_d  are the proportional, integral, and derivative gains respectively.

The lecturer explained that the proportional gain  k_p  should be 0.6 times the gain  k  of the proportional controller. He noted that this value is derived from empirical data and is a common practice in control systems engineering.

Next, the lecturer discussed the integral gain  k_i , which is given by  \frac{2}{P} . Here,  P  represents the period of oscillation. He emphasized that this formula is straightforward and based on Ziegler's theorem.

Finally, the derivative gain  k_d  is calculated as  \frac{P}{8} . Again,  P  is the period of oscillation. The lecturer mentioned that these values are conventions used in control system design and will be further elaborated in future classes.

> Lecturer: "because pid toh proportional integral to ache, toh dhoro boko thakbe. thikase?"

The lecturer also noted that for a PI controller, the integral gain  k_i  is  \frac{1.2}{P}  and the time constant  T  is 0.95 times the period  k .

### Extra jana kotha
Understanding these parameters is crucial for designing effective PID controllers. By knowing how to calculate these gains, students can better analyze and tune control systems to achieve desired performance.

---

## Check yourself
1. What is the formula for the proportional gain in a PID controller?
2. How does the integral component of a PID controller work?
3. What is the purpose of the derivative component in a PID controller?
4. What is Ziegler's theorem used for in control theory?
5. What are the formulas for the proportional, integral, and derivative gains in a PID controller?

### Answers
1. The formula for the proportional gain in a PID controller is \( \text{output} = \text{error} \times \text{gain} \).
2. The integral component of a PID controller accumulates the error over time and adds it to the output, helping to reduce steady-state error.
3. The derivative component measures the rate of change of the error and helps dampen oscillations and improve stability.
4. Ziegler's theorem is used to find the gain for a P controller by using the oscillation period of the system.
5. The formulas for the proportional, integral, and derivative gains in a PID controller are:
   - \( k_p = 0.6 \times k \)
   - \( k_i = \frac{2}{P} \)
   - \( k_d = \frac{P}{8} \)
   where \( k \) is the gain of the proportional controller and \( P \) is the period of oscillation.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
