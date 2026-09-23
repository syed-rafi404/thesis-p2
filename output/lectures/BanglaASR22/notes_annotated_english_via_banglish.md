# CSE 461 Control Theory
This lecture introduces the fundamental concepts of control theory and its practical applications, focusing on the basics of control systems and their components.

## Key takeaways
- Introduction to control theory and its application to a DC motor.
- Understanding the basic operation and internal structure of a DC motor.
- Explanation of the block diagram representing a basic control system setup.
- Introduction to the concept of open and closed circuits in control systems.
- Overview of the key components of a control system including the controller, actuators, feedback sensors, and the importance of a feedback loop.

<!-- boxes: 1=#d62828 -->
## Board 1: Introduction to Control Theory
**In one line:** This board introduces the basics of control theory and its application to a DC motor.

![Board 1: 0:10-1:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Control theory


1. **Control theory**: The board starts with the title "CSE461 Control theory". Control theory is a branch of engineering that deals with the behavior of dynamical systems with inputs, and how their behavior is modified by feedback. It is used to design systems that can operate in a desired manner.

2. **DC motor**: Next, the lecturer mentions a DC motor, which is a type of electric motor that converts electrical energy into mechanical energy. A DC motor has two poles, positive and negative, which determine the direction of rotation when a voltage is applied.

> Lecturer: "for example, we have a DC motor, so we can make a DC motor spin."

3. **Basic operation**: The lecturer explains that a DC motor has two poles, and changing the polarity can reverse the direction of rotation. For instance, if we apply 5 volts to the motor, we need to connect the common ground to ensure the motor spins correctly.

> Lecturer: "for example, what can we do now? I'm applying 5 volts, so we need to connect the common ground here to make the motor spin properly."

4. **Decimator structure**: The lecturer then discusses the internal structure of a DC motor, specifically mentioning the armature. The armature is a cylindrical component made of copper wires that rotate within the motor. When the armature rotates, it cuts through the magnetic field created by the stator, generating an electromotive force (EMF).

> Lecturer: "now let's talk about the internal structure of a DC motor, specifically the armature. The armature is a cylindrical component made of copper wires that rotate inside the motor. When the armature rotates, it cuts through the magnetic field created by the stator, which generates an electromotive force (EMF)."

**Remember:** The key points from this board include the introduction to control theory, the basic operation of a DC motor, and the internal structure of the motor, particularly the role of the armature in generating EMF.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Blue Box 2: Block Diagram
**In one line:** c p. Ω D.C driverz m

![Board 2: 1:20-4:50](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram


The blue box on the whiteboard shows a block diagram labeled "c p. Ω D.C driverz m". This diagram represents a basic control system setup where `c` stands for the controller, `p` for the power amplifier, `Ω` for the motor, and `m` for the main motor. Let's break down each component and understand their roles in the system.

1. **Controller (c):** The controller is connected to a digital pin and is responsible for receiving inputs and generating appropriate signals. In our example, if the controller receives a 5V input, it will connect the positive terminal of the controller to the common ground of the motor. This setup ensures that the controller and the motor share a common reference point.

2. **Power Amplifier (p):** The power amplifier is used to amplify the signal from the controller to a level suitable for driving the motor. It helps in triggering higher voltages when needed, which is crucial for controlling the motor effectively.

3. **Motor (Ω):** The motor is the actuator in this system. It converts electrical energy into mechanical energy. In our simplified model, we assume that the motor can spin in both directions based on the input signal.

4. **Main Motor (m):** The main motor is the actual device being controlled. It could be a DC motor, and its speed and direction can be controlled using the power amplifier and the controller.

The lecturer explains that the goal is to design a circuit that can control the motor's speed and direction accurately. For instance, in a drone, the propellers need to rotate at specific RPMs to achieve stable flight. The controller and power amplifier work together to ensure that the motor operates at the desired speed.


The lecturer further clarifies that the system can be designed to operate in either clockwise or counterclockwise direction based on the input signal. This flexibility is essential for various applications like drones, where different propellers need to rotate at specific speeds and directions.

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding the block diagram is crucial for designing control systems. By breaking down the components and their interactions, we can better grasp how to control motors and other actuators in real-world applications. This knowledge is fundamental for anyone working in control theory and robotics.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Box 1: CSE461 Control Theory
**In one line:** This box introduces the course title.

![Board 3: 5:00-5:40](figures_annotated/board_era3_500.jpg)

*Figure 3. The whiteboard during 5:00–5:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram


- **Red Box 1 (Title):** CSE461 Control Theory

### Explanation
The lecturer starts by explaining the purpose of the current setup. He says, "tahole eita exact major korar jomne amra ki kore?" which translates to "So, how exactly do we achieve this?" The lecturer then introduces a feedback loop into the system. He explains, "ekhan theke amra ekta feedback lakay dei," meaning "from here, we take one feedback."

Next, he clarifies the components involved. He mentions, "ei je motor er output ta, motor er DC motor output ta ekhan theke tei na," which means "this is the output of the motor, but not directly from here." The output is taken from somewhere else, and then a feedback is introduced. The lecturer further explains, "ei je output gelo, ei output er ekhan theke ekta amra feedback niye, ei je amader control er abr feed korlam," meaning "this output is taken, and from this output, we take a feedback, which we use to control our system."

Finally, he concludes by saying, "so basically amra ki kortesi? pochhe mi amader computer er input dicche, thikache," which translates to "basically, what are we doing? Now, our computer's input is this, right?"

### Background (not said in the lecture)
In control theory, a feedback loop is crucial for adjusting the system's behavior based on the difference between the desired output and the actual output. This helps in stabilizing the system and improving its performance. Understanding the feedback mechanism is fundamental for designing control systems effectively.

<!-- boxes: 1=#d62828 -->
## Board 4: Open Circuit vs Closed Circuit

**In one line:** Today, we will discuss the concept of open circuit and closed circuit in control systems.

![Board 4: 5:50-7:38](figures_annotated/board_era4_550.jpg)

*Figure 4. The whiteboard during 5:50–7:38, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Control theory


1. **Red Box 1 (Control theory):** We start with the basics of control theory, which is the core of CSE 461. The board introduces us to the idea of an open circuit and a closed circuit.

2. **Open Circuit (Box 1, red):** The first part of the board shows an open circuit. An open circuit is a system where there is no feedback loop. This means that the output of the system is not fed back into the system to adjust the input. For example, if we have a motor, the output (like speed) is measured, but no feedback is used to adjust the input (like voltage). This results in a constant error or gap between the desired output and the actual output.

3. **Closed Circuit (Box 1, red):** The second part of the board transitions to a closed circuit. In a closed circuit, feedback is used to correct the error. This means that the output is continuously monitored and fed back into the system to adjust the input. For instance, if we have a motor, the output (speed) is measured, and this information is used to adjust the input (voltage) to minimize the error. This process ensures that the actual output matches the desired output more closely.

4. **Open Circuit Controller (Box 1, red):** The lecturer emphasizes that in an open circuit, we cannot guarantee the exact output we need. There is always a gap or error that remains uncorrected. However, in a closed circuit, we use feedback to correct this error, making the system more precise and reliable.

5. **Basic Idea (Box 1, red):** The lecturer explains that the transition from an open circuit to a closed circuit is fundamental in understanding control systems. By using feedback, we can improve the performance of our systems and achieve better control over the output.


### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding the difference between open and closed circuits is crucial in control theory. An open circuit lacks feedback, leading to constant errors, while a closed circuit uses feedback to correct these errors, ensuring more accurate and stable system performance.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Board 5: Control System Overview
**In one line:** This board introduces the basic components of a control system.

![Board 5: 7:50-9:50](figures_annotated/board_era5_750.jpg)

*Figure 5. The whiteboard during 7:50–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Title · 3 Block diagram


1. **Red Box (Box 1):** The sticker says "SUPER BOARD," indicating this is an important overview.
2. **Blue Box (Box 2):** The title "CSE 461 Control theory" is displayed, confirming the subject of the lecture.
3. **Orange Box (Box 3):** A block diagram showing the key components of a control system: error controller, P.I.D. (Proportional Integral Derivative) actuators, feedback sensors.

The lecturer said: "so ei hocche amader controller ta."

- **Controller:** The controller is responsible for adjusting the system based on the feedback received. It processes the input and generates the necessary output to correct any errors.

- **Actuators:** These are the components that physically move or change the system in response to the controller's commands. For example, if the controller detects an error, it will send signals to the actuators to make adjustments.

- **Feedback Loop:** The feedback loop is a crucial part of the system. It involves taking the output and comparing it to the desired input. Any discrepancy between these values is considered an error, which is then used to adjust the system.

- **Sensors:** Sensors measure the actual output of the system and provide feedback to the controller. They help in determining whether the system is performing as expected or if adjustments are needed.

The lecturer emphasized that this setup forms a closed circuit, where the system continuously monitors and adjusts itself based on the feedback received. Sensors play a vital role in providing the necessary information to the controller, which then uses this data to minimize errors and improve overall performance.

The lecturer said: "so ei hocche amader controller ta."

The error controller, P.I.D. actuators, and feedback sensors work together to create a robust control system. Understanding these components is essential for designing effective control systems.

**Remember:** The key points from this board are the roles of the controller, actuators, feedback sensors, and how they form a closed circuit to improve system performance.

---

## Check yourself
1. What is control theory?
2. What is a DC motor and how does it work?
3. Explain the components of a block diagram in a control system.
4. What is the difference between an open circuit and a closed circuit?
5. Name the key components of a control system and their functions.

### Answers
1. Control theory is a branch of engineering that deals with the behavior of dynamical systems with inputs, and how their behavior is modified by feedback.
2. A DC motor is a type of electric motor that converts electrical energy into mechanical energy. It has two poles, positive and negative, which determine the direction of rotation when a voltage is applied.
3. The components of a block diagram in a control system include the controller, power amplifier, motor, and main motor. The controller receives inputs and generates signals, the power amplifier amplifies the signal, the motor is the actuator, and the main motor is the device being controlled.
4. An open circuit lacks feedback, leading to constant errors, while a closed circuit uses feedback to correct these errors, ensuring more accurate and stable system performance.
5. The key components of a control system are the controller, actuators, and feedback sensors. The controller adjusts the system based on feedback, the actuators physically move or change the system, and the feedback sensors measure the actual output and provide information to the controller.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (3 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
