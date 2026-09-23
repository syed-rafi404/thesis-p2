# Routing Methods in Networks
This lecture covers dynamic routing methods, their types, and the advantages they offer.

## Key takeaways
- Dynamic Routing
- Distance Vector Routing (DVR)
- Link State Routing (LSR)
- Global Routing Method
- Event Driven Method
- Dijkstra's Algorithm
- Heuristic
- Shortest path
- Map of the entire network
- Convergence time

<!-- boxes: 1=#d62828 -->
## Red Box 1: Flowchart of Routing Methods
**In one line:** Dynamic Routing DVR -> Distance Vector Routing LSR -> Link State Routing Global Routing Method Event driven method Dijkstra's algo. works based on a heuristic creates a map of the Entire network

![Board 1: 0:00-6:30](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Flowchart


- **Red Box 1 (Flowchart):** The flowchart starts with **Dynamic Routing** and moves to **Distance Vector Routing (DVR)**, then to **Link State Routing (LSR)**, and finally to **Global Routing Method**. The **Event Driven Method** uses **Dijkstra's Algorithm**, which is based on a heuristic and creates a map of the entire network.


### Background (not said in the lecture) (lecture e bola hoy ni)
- Dijkstra's Algorithm is a heuristic-based method that guarantees finding the shortest path in a network. It is used in link state routing to create a complete map of the network.
- The event-driven method updates the routing map only when necessary, making it more efficient compared to periodic updates.

**Remember:** Dynamic Routing, Distance Vector Routing, Link State Routing, Global Routing Method, Event Driven Method, Dijkstra's Algorithm, heuristic, shortest path, map of the entire network, convergence time.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Blue Box 2: Advantages of Dynamic Routing
**In one line:** This box lists the advantages of dynamic routing methods.

![Board 2: 6:40-7:48](figures_annotated/board_era2_640.jpg)

*Figure 2. The whiteboard during 6:40–7:48, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Flowchart · 2 Advantages


1. **Dynamic Routing**: The flowchart on the red box introduces three types of dynamic routing methods: Distance Vector Routing (DVR), Link State Routing (LSR), and Global Routing. Each method uses Dijkstra's algorithm for event-driven routing, which is based on a heuristic approach.
   
2. **Distance Vector Routing (DVR)**: DVR creates a map of the entire network and updates routing tables based on changes in the network topology. It works efficiently for larger networks and has a relatively fast convergence time.
   
3. **Link State Routing (LSR)**: LSR also creates a map of the entire network but does so more efficiently, making it suitable for larger networks. It has a very low convergence time, meaning it quickly adapts to changes in the network.
   
4. **Global Routing**: This method also uses Dijkstra's algorithm and is designed to work efficiently for larger networks, similar to LSR. It ensures that routing decisions are made based on the best path available.

5. **Advantages**:
   - **Event-driven method**: This method is highly efficient and works based on a heuristic approach, which helps in creating a map of the entire network.
   - **Creates a map of the entire network**: By maintaining a complete map of the network, these methods ensure that routing decisions are made accurately.
   - **Works efficiently for larger networks**: These methods are particularly useful in large-scale networks where traditional static routing might not be sufficient.
   - **Convergence time very less**: The quick adaptation to changes in the network makes these methods highly reliable and efficient.


### Background (not said in the lecture) (lecture e bola hoy ni)
This section explains the advantages of dynamic routing methods, highlighting their efficiency and ability to handle large networks. Understanding these concepts will help you grasp how routing algorithms adapt to network changes and ensure optimal data transmission.

---

## Check yourself
1. What is the difference between Distance Vector Routing (DVR) and Link State Routing (LSR)?
2. How does Dijkstra's Algorithm work in the context of Link State Routing?
3. What are the advantages of using an event-driven method in dynamic routing?
4. Why is it important to have a map of the entire network in dynamic routing methods?
5. What does the term "convergence time" refer to in the context of routing methods?

### Answers
1. Distance Vector Routing (DVR) creates a map of the entire network and updates routing tables based on changes in the network topology, while Link State Routing (LSR) also creates a map of the entire network but does so more efficiently, making it suitable for larger networks.
2. Dijkstra's Algorithm in Link State Routing is a heuristic-based method that guarantees finding the shortest path in a network by creating a complete map of the network.
3. The advantages of using an event-driven method include high efficiency and the ability to work based on a heuristic approach, which helps in creating a map of the entire network.
4. Having a map of the entire network in dynamic routing methods ensures accurate routing decisions.
5. Convergence time refers to the time it takes for a routing protocol to adapt to changes in the network and update the routing tables accordingly.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
