# BanglaASR21: Red Box 1 & Blue Box 2

The lecture covers the flowchart of routing methods and the advantages of dynamic routing.

## Key takeaways
- Dynamic Routing, Distance Vector Routing, Link State Routing, Global Routing Method, Event Driven Method, Dijkstra's Algorithm, heuristic, shortest path, map of the entire network, convergence time.

<!-- boxes: 1=#d62828 -->
## Red Box 1: Flowchart of Routing Methods
**Ek line e:** Dynamic Routing DVR -> Distance Vector Routing LSR -> Link State Routing Global Routing Method Event driven method Dijkstra's algo. works based on a heuristic creates a map of the Entire network

![Board 1: 0:00-6:30](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Flowchart


- **Red Box 1 (Flowchart):** The flowchart starts with **Dynamic Routing** and moves to **Distance Vector Routing (DVR)**, then to **Link State Routing (LSR)**, and finally to **Global Routing Method**. The **Event Driven Method** uses **Dijkstra's Algorithm**, which is based on a heuristic and creates a map of the entire network.

> Lecturer: "so ei jone e ahm Lsr e bolai global routing method."

### Extra jana kotha (lecture e bola hoy ni)
- Dijkstra's Algorithm is a heuristic-based method that guarantees finding the shortest path in a network. It is used in link state routing to create a complete map of the network.
- The event-driven method updates the routing map only when necessary, making it more efficient compared to periodic updates.

**Mone rakho:** Dynamic Routing, Distance Vector Routing, Link State Routing, Global Routing Method, Event Driven Method, Dijkstra's Algorithm, heuristic, shortest path, map of the entire network, convergence time.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Blue Box 2: Advantages of Dynamic Routing
**Ek line e:** This box lists the advantages of dynamic routing methods.

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

> Lecturer: "this is very complex to implement."

### Extra jana kotha (lecture e bola hoy ni)
This section explains the advantages of dynamic routing methods, highlighting their efficiency and ability to handle large networks. Understanding these concepts will help you grasp how routing algorithms adapt to network changes and ensure optimal data transmission.

---

## Check yourself
1. What is the first step in the flowchart of routing methods?
2. Which routing method uses Dijkstra's algorithm for event-driven routing?
3. What is the main advantage of the event-driven method?
4. How does the event-driven method update the routing map?
5. Why are dynamic routing methods particularly useful for larger networks?

### Answers
1. The first step in the flowchart of routing methods is Dynamic Routing.
2. Link State Routing (LSR) uses Dijkstra's algorithm for event-driven routing.
3. The main advantage of the event-driven method is its efficiency and the fact that it works based on a heuristic approach.
4. The event-driven method updates the routing map only when necessary.
5. Dynamic routing methods are particularly useful for larger networks because they can efficiently handle changes in the network topology and ensure optimal data transmission.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
