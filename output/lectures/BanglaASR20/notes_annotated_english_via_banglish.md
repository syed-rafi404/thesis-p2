# BanglaASR20
The lecture covers Dynamic Routing, including Distance Vector Routing (DVR) and Link State Routing (LSR).

## Key takeaways
- Dynamic Routing includes Distance Vector Routing (DVR) and Link State Routing (LSR).
- DVR is a type of dynamic routing where each router maintains a routing table based on information from its neighbors.
- The Bellman-Ford algorithm is used to find the shortest path but can lead to suboptimal results.
- Split horizon and poison reverse are techniques to prevent routing loops and ensure correct convergence.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Dynamic Routing: DVR and LSR
**In one line:** Dynamic Routing includes Distance Vector Routing (DVR) and Link State Routing (LSR).

![Board 1: 0:00-14:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–14:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Dynamic Routing · 2 Diagram


1. **Dynamic Routing**: The board starts with the definition of dynamic routing, specifically mentioning Distance Vector Routing (DVR) and Link State Routing (LSR). DVR stands for Distance Vector Routing, while LSR stands for Link State Routing.

2. **Diagram**: The diagram on the board shows routers R1, R2, and R3. This visual helps understand the network setup where these routers are interconnected.

3. **Explanation**:
    - **DVR**: The lecturer explains that DVR is a type of dynamic routing where each router maintains a routing table based on the information received from its neighbors. The process involves each router sharing its routing table with its neighbors and updating its table based on the information received.
    - **Routing Table Update**: For example, R1 shares its routing table with R2 and R3, and vice versa. Initially, R1 and R3 have their own information about the network. R1 then updates its table with the information from R3, and similarly, R3 updates its table with the information from R1.
    - **Bellman-Ford Algorithm**: The network uses the Bellman-Ford algorithm to find the shortest path. However, this can lead to suboptimal results due to the nature of the algorithm, which might introduce errors like incorrect hop counts or infinite costs.
    - **Split Horizon Rule**: To avoid issues like poisoned reverse, the split horizon rule is applied. This rule states that a router should not advertise a route back to the neighbor from which it learned the route. Instead, it should only advertise routes that were learned from other neighbors.
    - **Poison Reverse**: The poison reverse technique is used to prevent routing loops. It involves marking a route as unreachable when it is advertised back to the neighbor from which it was learned. This ensures that the network converges correctly without forming loops.

4. **Quotes**:

5. **Background (not said in the lecture)**: Split horizon and poison reverse are crucial techniques in dynamic routing to ensure correct and stable routing. These methods help in preventing routing loops and ensuring that the network converges to the correct state. Understanding these concepts is essential for managing complex network topologies effectively.

---

## Check yourself
1. What does DVR stand for?
2. Explain the split horizon rule.
3. What is the purpose of poison reverse?
4. Which algorithm is commonly used in DVR?
5. How many routers are mentioned in the diagram?

### Answers
1. DVR stands for Distance Vector Routing.
2. The split horizon rule states that a router should not advertise a route back to the neighbor from which it learned the route.
3. The purpose of poison reverse is to mark a route as unreachable when it is advertised back to the neighbor from which it was learned, preventing routing loops.
4. The Bellman-Ford algorithm is commonly used in DVR.
5. Three routers (R1, R2, and R3) are mentioned in the diagram.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
