# CSE 461 Control Theory
This lecture introduces the fundamentals of control theory and its application to various systems, focusing on the basics of control systems and the importance of feedback loops.

## Key takeaways
- Control theory is a branch of engineering that deals with the behavior of dynamical systems with inputs and how their behavior is modified by feedback.
- A DC motor is a type of electric motor that converts electrical energy into mechanical energy.
- A block diagram represents a basic control system setup, showing the interaction between the controller, power amplifier, motor, and feedback.
- Feedback loops are crucial for adjusting the system's behavior based on the difference between the desired output and the actual output.
- Open circuits lack feedback, whereas closed circuits include a feedback loop to correct discrepancies and achieve the desired output.

<!-- boxes: 1=#d62828 -->
## Board 1: Introduction to Control Theory
**Ek line e:** This board introduces the basics of control theory and its application to a DC motor.

![Board 1: 0:10-1:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Control theory


1. **Control theory**: The board starts with the title "CSE461 Control theory". Control theory is a branch of engineering that deals with the behavior of dynamical systems with inputs, and how their behavior is modified by feedback. It is used to design systems that can operate in a desired manner.
   
2. **DC motor**: Next, the lecturer mentions a DC motor, which is a type of electric motor that converts electrical energy into mechanical energy. A DC motor has two poles, positive and negative, which determine the direction of rotation when a voltage is applied.

> Lecturer: "for example, we have ar dc motor, toh ekta dc motor er amra kive be spin korte pari."

3. **Basic operation**: The lecturer explains that a DC motor has two poles, and changing the polarity can reverse the direction of rotation. For instance, if we apply 5 volts to the motor, we need to connect the common ground to ensure the motor spins correctly.

> Lecturer: "for example, ekhn amra ki ki korte pari? 5 volt er porsu sikhane dilam e ekhane ta common ground asha ta kane kore gham. moddhe dc motor kino yabhe chulese."

4. **Decimator structure**: The lecturer then discusses the internal structure of a DC motor, specifically mentioning the armature. The armature is a cylindrical component made of copper wires that rotate within the motor. When the armature rotates, it cuts through the magnetic field created by the stator, generating an electromotive force (EMF).

> Lecturer: "ar kon kon kon jodi decimator er structure er jai, decimator basically heita armature thake. je armature ring ta ei rokon nate shape er, ei armature ring er uport deye abna hocche wires erokom copper wires spin korn o thake right. ekhon basically ki hoy teche? jokhn amader ei amader ei lithe city dicchi, ekta mann a magnet er field er creation hocche, bucche no."

**Mone rakho:** The key points from this board include the introduction to control theory, the basic operation of a DC motor, and the internal structure of the motor, particularly the role of the armature in generating EMF.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Blue Box 2: Block Diagram
**Ek line e:** c p. Ω D.C driverz m

![Board 2: 1:20-4:50](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram


The blue box on the whiteboard shows a block diagram labeled "c p. Ω D.C driverz m". This diagram represents a basic control system setup where `c` stands for the controller, `p` for the power amplifier, `Ω` for the motor, and `m` for the main motor. Let's break down each component and understand their roles in the system.

1. **Controller (c):** The controller is connected to a digital pin and is responsible for receiving inputs and generating appropriate signals. In our example, if the controller receives a 5V input, it will connect the positive terminal of the controller to the common ground of the motor. This setup ensures that the controller and the motor share a common reference point.

2. **Power Amplifier (p):** The power amplifier is used to amplify the signal from the controller to a level suitable for driving the motor. It helps in triggering higher voltages when needed, which is crucial for controlling the motor effectively.

3. **Motor (Ω):** The motor is the actuator in this system. It converts electrical energy into mechanical energy. In our simplified model, we assume that the motor can spin in both directions based on the input signal.

4. **Main Motor (m):** The main motor is the actual device being controlled. It could be a DC motor, and its speed and direction can be controlled using the power amplifier and the controller.

The lecturer explains that the goal is to design a circuit that can control the motor's speed and direction accurately. For instance, in a drone, the propellers need to rotate at specific RPMs to achieve stable flight. The controller and power amplifier work together to ensure that the motor operates at the desired speed.

> Lecturer: "so eita general anti clockwise hore jodi amra polar er shik thake."

The lecturer further clarifies that the system can be designed to operate in either clockwise or counterclockwise direction based on the input signal. This flexibility is essential for various applications like drones, where different propellers need to rotate at specific speeds and directions.

### Extra jana kotha (lecture e bola hoy ni)
Understanding the block diagram is crucial for designing control systems. By breaking down the components and their interactions, we can better grasp how to control motors and other actuators in real-world applications. This knowledge is fundamental for anyone working in control theory and robotics.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Box 1: CSE461 Control theory
**Ek line e:** This box introduces the course title.

![Board 3: 5:00-5:40](figures_annotated/board_era3_500.jpg)

*Figure 3. The whiteboard during 5:00–5:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram


- **Red Box 1 (Title):** CSE461 Control theory

### Explanation
The lecturer starts by explaining the purpose of the current setup. He says, "tahole eita exact major korar jomne amra ki kore?" which translates to "So, how exactly do we achieve this?" The lecturer then introduces a feedback loop into the system. He explains, "ekhan theke amra ekta feedback lakay dei," meaning "from here, we take one feedback." 

Next, he clarifies the components involved. He mentions, "ei je motor er output ta, motor er DC motor output ta ekhan theke tei na," which means "this is the output of the motor, but not directly from here." The output is taken from somewhere else, and then a feedback is introduced. The lecturer further explains, "ei je output gelo, ei output er ekhan theke ekta amra feedback niye, ei je amader control er abr feed korlam," meaning "this output is taken, and from this output, we take a feedback, which we use to control our system."

Finally, he concludes by saying, "so basically amra ki kortesi? pochhe mi amader computer er input dicche, thikache," which translates to "basically, what are we doing? Now, our computer's input is this, right?"

### Extra jana kotha
In control theory, a feedback loop is crucial for adjusting the system's behavior based on the difference between the desired output and the actual output. This helps in stabilizing the system and improving its performance. Understanding the feedback mechanism is fundamental for designing control systems effectively.

<!-- boxes: 1=#d62828 -->
## Board 4: Open Circuit vs Closed Circuit in Control Theory

**Ek line e:** Today, we will discuss the concept of open circuit and closed circuit in control theory.

![Board 4: 5:50-7:38](figures_annotated/board_era4_550.jpg)

*Figure 4. The whiteboard during 5:50–7:38, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Control theory


1. **Red Box 1 (Control theory: CSE 461)**: We start with the basics of control theory, which is the study of how to control systems, like motors, to achieve desired outputs.

2. **Open Circuit**: In the first part of the board, we see an open circuit. An open circuit is a system where there is no feedback loop. This means that the output of the system is not fed back into the system to adjust its behavior. For example, if we have a motor and we want to control its speed, in an open circuit, we do not use any feedback mechanism to correct any discrepancies between the desired speed and the actual speed.

3. **Closed Circuit**: Moving to the second part of the board, we see a closed circuit. A closed circuit includes a feedback loop. Feedback is the process of taking the output of the system and using it to adjust the input, thereby correcting any discrepancies. For instance, if we have a motor and we want to maintain a specific speed, we can use a feedback loop to measure the actual speed and adjust the input to the motor to match the desired speed.

4. **Difference Between Open and Closed Circuits**: The lecturer explains that in an open circuit, we cannot ensure that the required output is achieved exactly as desired. There might be a gap between the desired output and the actual output, and this gap cannot be corrected without feedback. On the other hand, in a closed circuit, we use feedback to correct any discrepancies and ensure that the system behaves as intended.

> Lecturer: "je chai tesilam exho, but for example pai tesi amra poitoli char pir. eie je gap ta, ei gap ta berkor hocche amade ei feedback diye kache."

5. **Open Circuit Controller**: The lecturer emphasizes that when we talk about an open circuit, we are referring to a system without feedback. This is often denoted as "open circuit controller." The term "open circuit" is used more frequently to describe such systems.

6. **Closed Circuit Loop**: When we move to a closed circuit, we are essentially creating a loop where the output is fed back into the system to make adjustments. This is known as a closed circuit loop.

**Mone rakho:** Open circuit refers to a system without feedback, while closed circuit includes a feedback loop. Feedback helps in correcting discrepancies and achieving the desired output.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Board 5: Control System Components and Feedback Loop
**Ek line e:** This board introduces the components of a control system and explains the concept of feedback.

![Board 5: 7:50-9:50](figures_annotated/board_era5_750.jpg)

*Figure 5. The whiteboard during 7:50–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Sticker · 2 Title · 3 Block diagram


- **Red Box 1 (SUPER BOARD):** This sticker indicates that this board is comprehensive and covers key elements of the control system.
- **Blue Box 2 (Title):** The title "CSE 461 Control theory" clearly states the subject of the lecture.
- **Orange Box 3 (Block Diagram):** The block diagram shows the components of a control system including the error controller, P.I.D. actuators, feedback, and sensors.

The lecturer explained that when we have a feedback system, we aim to make the system more efficient by using full proportional control. This is where the controller comes into play. The controller is responsible for adjusting the system based on the error.

- **Controller:** The controller is the component that processes the error and adjusts the system accordingly.
- **Actuators:** These are the devices that actually perform the actions based on the instructions from the controller. For example, they might move a mechanical part in a machine.
- **Feedback Loop:** The feedback loop is a crucial part of the system. It involves taking the output and comparing it to the desired input. The difference between these two is the error, which is then used to adjust the system.
- **Sensors:** Sensors measure the actual output and provide feedback to the controller. They help in determining whether the system is performing as expected.

The lecturer also mentioned that this forms a closed circuit, where the system receives an input, processes it, and provides feedback to correct any discrepancies. Sensors play a vital role in measuring the output and providing feedback to the controller.

> Lecturer: "so ei hocche amader controller ta."

### Extra jana kotha
Understanding the components of a control system and the role of feedback is essential. By knowing how these parts work together, students can better design and analyze control systems. This knowledge helps in ensuring that the system operates efficiently and accurately.

---

## Check yourself
1. What is control theory?
2. Explain the basic operation of a DC motor.
3. Describe the components of a block diagram in a control system.
4. What is the role of a feedback loop in a control system?
5. Differentiate between an open circuit and a closed circuit.

### Answers
1. Control theory is a branch of engineering that deals with the behavior of dynamical systems with inputs and how their behavior is modified by feedback.
2. A DC motor converts electrical energy into mechanical energy. It has two poles, positive and negative, which determine the direction of rotation when a voltage is applied.
3. A block diagram includes the controller, power amplifier, motor, and feedback. The controller processes the error, the power amplifier amplifies the signal, the motor acts as the actuator, and the feedback loop corrects any discrepancies.
4. A feedback loop takes the output of the system and uses it to adjust the input, thereby correcting any discrepancies and ensuring the system behaves as intended.
5. An open circuit lacks feedback, while a closed circuit includes a feedback loop to correct discrepancies and achieve the desired output.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 6 kept, 1 removed. References to boxes that do not exist: 0.*
