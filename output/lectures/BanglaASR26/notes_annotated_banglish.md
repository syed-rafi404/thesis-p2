# PID Controller
Today we will start with the basics of the PID controller.

## Key takeaways
- **Proportional (kP):** Adjusting the output based on the current error.
- **Integral (kI):** Eliminating the steady-state error by considering the sum of past errors.
- **Derivative (kD):** Improving the transient response by considering the rate of change of the error.
- **Output Formula:** Combining proportional, integral, and derivative terms to get the final output.
- **Step-by-step Calculation:** Breaking down the process into four steps to calculate the new output.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## PID Controller: Introduction
**Ek line e:** Today we will start with the basics of the PID controller.

![Board 1: 0:10-1:50](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–1:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Formula · 3 Formula


- **Red Box 1 (SUPER BOARD):** This box is labeled as SUPER BOARD, indicating it's an important section.
- **Blue Box 2 (Formula):** The formula shown here is [kP, kI, kD], which represents the three components of a PID controller.
- **Orange Box 3 (Formula):** The term PIO is mentioned, which stands for Proportional Integral Derivative.

The board shows a table with the following values:
| kP | kI | kD |
|----|----|----|
| xPn | p | pI |
|     |    | pIO |

**Explanation:**
1. **Proportional (kP):** The lecturer explains that proportional control is about adjusting the output based on the current error. He mentions that the term "pi" is used for proportional gain, and asks if everyone understands this concept. He clarifies that proportional control is essentially adjusting the output based on the error without any delay.
2. **Integral (kI):** The lecturer points out that when kP is set to a certain value, it becomes proportional control. However, when kP is set to a specific value, such as p, and kI is also set to a value, it becomes proportional integral control. The term "pI" is used to denote the integral component.
3. **Derivative (kD):** The lecturer then introduces the derivative component, represented by "pIO," and explains that the full PID controller combines proportional, integral, and derivative actions.
4. **Output Formula:** The lecturer emphasizes that the output formula is crucial. For example, if we have a system where the output is cost, we can determine the initial value and observe how it changes over four steps. This helps in understanding the behavior of the system under different PID settings.


**Extra jana kotha:**
Understanding the PID controller is essential for designing control systems. By breaking down the components—proportional, integral, and derivative—we can better manage and optimize the performance of our systems. This knowledge is fundamental for anyone working in control engineering.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## PID Controller: Step-by-Step Calculation
**Ek line e:** Imagine: (PID) -> kp, ki, ko

![Board 2: 2:00-4:54](figures_annotated/board_era2_200.jpg)

*Figure 2. The whiteboard during 2:00–4:54, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Instruction · 2 Formula


1. **Red Box 1**: The lecturer starts by imagining the process of solving a problem using a PID controller. He mentions that we need to do four steps for this problem. Initially, we can set some default values for kp, ki, and ko, but these can be adjusted later based on the system's response.
2. **Blue Box 2**: The lecturer writes down the output formula for a PID controller: `output = kp * error + (∑n Error) * ki + output = k / ic`. Here, `kp` is the proportional gain, `ki` is the integral gain, and `ko` is the derivative gain. The lecturer explains that `kp` and `ki` will be used as values in the PID controller equation.
3. **Step-by-Step Explanation**:
    - First, we calculate the error. The error is the difference between the desired setpoint and the current measured value.
    - Next, we accumulate the error over time to get the integral term. This is represented by `∑n Error`.
    - Then, we calculate the derivative term, which is the rate of change of the error.
    - Finally, we combine these terms to get the output of the PID controller.
4. **Output Feedback**: The lecturer emphasizes that the output is fed back into the system as an error signal. This feedback loop is crucial for the PID controller to adjust its output continuously.

> Lecturer: "output er formula ta hocche, amra first of all je bolla je amader je kp er value ta ber korbo, mane eita amra dhore nicchi, eta o mention korte ba obviously."
> 
> Lecturer: "ei jinish ta ki hbe? ei jinish ta ki?"

### Extra jana kotha
In a PID controller, the proportional term helps to reduce the steady-state error, the integral term eliminates the offset, and the derivative term improves the transient response. Understanding these components is essential for designing effective control systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## PID Controller: Step-by-Step Calculation
**Ek line e:** Amra eita process e kintu straight forward kore korte hobe.

![Board 3: 5:00-6:20](figures_annotated/board_era3_500.jpg)

*Figure 3. The whiteboard during 5:00–6:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Instruction · 3 Formula


- **Box 1 (red)**: This sticker says "SUPER BOARD", indicating that this is an important section.
- **Box 2 (blue)**: The instruction here is to imagine converting (PID) into kP, kI, and kD. We need to do 4 steps for this problem.
- **Box 3 (orange)**: The formula given is `output = kP * error + (Σn Error) * kI + kD`. This represents the basic structure of a PID controller.

The lecturer explained that we are designing a system where we multiply the error by a constant (kP) and also consider the integral of the error multiplied by another constant (kI). The derivative term (kD) is also included in the final output.

> Lecturer: "eita ekhane ekta jinish ta macha kore dilei amra kintu era design kora. eije protte ekta error arche tar sheta gain ta multiply kolay le amra output ta pabo. eita ekhane straight forward."

The lecturer further clarified that if we directly use the given equation, it becomes simpler. However, the trick is to break down the process step by step.

> Lecturer: "tokhon nito i bhabe ebhlo ber korthebe. but jodi direct diye de equation e ziggler formula use kore kore kore, thikase ora easier hoye gelo. tokhon er occhi aladebore eta ber kore lakene. trick question e etar ekta ekta ekta ekta ekta diya ache ke rojda ber kore lake."

In summary, the basic formula for a PID controller is:
- Multiply the current error by kP.
- Sum up all past errors and multiply by kI.
- Add the derivative term kD.

**Mone rakho:** output = kP * error + (Σn Error) * kI + kD.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## PID Controller: Step-by-Step Calculation
**Ek line e:** So, we need to calculate the new output using the given formula.

![Board 4: 6:30-7:46](figures_annotated/board_era4_630.jpg)

*Figure 4. The whiteboard during 6:30–7:46, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Instruction · 3 Formula


- **Box 2 (blue):** The lecturer instructed us to imagine the PID controller with parameters KP, KI, and KO. He mentioned doing 4 steps for the problem.
- **Box 3 (orange):** The formula for the new output is given as: 
  ```
  output = kP * error + (∑nErr) * kI + (En - E3) * KD = new output
  new Actual = [New + old] / 2
  ```
  Here, `kP` is the proportional gain, `KI` is the integral gain, and `KD` is the derivative gain. `error` is the difference between the desired speed and the current speed.

**Explanation:**
1. **Step 1:** Calculate the derivative term `(En - E3) * KD`. This term represents the change in error over time, which helps in adjusting the output based on how quickly the error is changing.
2. **Step 2:** Add the proportional term `kP * error`, which is the current error multiplied by the proportional gain.
3. **Step 3:** Add the integral term `(∑nErr) * kI`, where `∑nErr` is the sum of all past errors multiplied by the integral gain. This term helps in eliminating steady-state error.
4. **Step 4:** Combine the above terms to get the new output. Then, update the actual output using the formula `new Actual = [New + old] / 2`.

**Quotes:**
> Lecturer: "so, error four minus error three je ta hobe, sheita multiplied by kd. right."
> Lecturer: "so amra hocche tokho amader actual output ta ke amader ber korbo, previous output plus new output."

### Extra jana kotha (lecture e bola hoy ni)
The PID controller is used to control the speed of a motor or any other system by adjusting the output based on the error between the desired speed and the actual speed. By following these 4 steps, we can ensure that the system maintains the desired speed accurately.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## PID Controller: Step-by-Step Calculation
**Ek line e:** Desired speed → 100 km/h, initial speed → 60 km/h

![Board 5: 8:10-13:12](figures_annotated/board_era5_810.jpg)

*Figure 5. The whiteboard during 8:10–13:12, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Title · 3 Formula · 4 Formula · 5 Formula · 6 Formula


- **Box 2 (blue):** (PID)
- **Box 3 (orange):** Formula: Desired speed → 100 km/h, initial speed → 60 km/h, kp=0.5; ki=0.1, ko=0.05
- **Box 4 (green):** Formula: Error = (100 - 60) = 40 km/h
- **Box 5 (purple):** Formula: out = [0.5×40] + 0.1×40 + 0.05×40
- **Box 6 (pink):** Formula: New actual speed = 60 + out

The lecturer explained that the desired speed is 100 km/h, and the initial speed of the car is 60 km/h. He mentioned that if we start the car, the initial speed will be 60 km/h, and the PID controller will adjust the speed based on the error between the desired speed and the actual speed.

### Extra jana kotha (lecture e bola hoy ni)
The PID controller uses three gains: proportional (kp), integral (ki), and derivative (ko). In this case, kp = 0.5, ki = 0.1, and ko = 0.05. The error is calculated as the difference between the desired speed and the initial speed, which is 40 km/h. The output of the controller is then calculated using these gains and the error.

**Mone rakho:** Desired speed, initial speed, kp, ki, ko, error, output, new actual speed

---

## Check yourself
1. What are the three components of a PID controller?
2. How does the integral component help in the PID controller?
3. What is the formula for the output of a PID controller?
4. Explain the steps involved in calculating the new output using a PID controller.
5. If the desired speed is 100 km/h and the initial speed is 60 km/h, what would be the error?

### Answers
1. The three components of a PID controller are proportional (kP), integral (kI), and derivative (kD).
2. The integral component helps in eliminating the steady-state error by considering the sum of past errors.
3. The formula for the output of a PID controller is `output = kP * error + (Σn Error) * kI + kD`.
4. The steps involved in calculating the new output using a PID controller are: (1) Calculate the derivative term, (2) Add the proportional term, (3) Add the integral term, (4) Combine the terms to get the new output.
5. The error would be 40 km/h (100 km/h - 60 km/h).

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 6 kept, 1 removed. References to boxes that do not exist: 0.*
