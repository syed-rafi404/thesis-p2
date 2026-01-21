```markdown
# Informed Search Lecture Notes

## Introduction to Informed Search

Today, we will delve into Informed Search, focusing on two key algorithms: Greedy Best First Search (GBFS) and the A* Algorithm.

### Greedy Best First Search (GBFS)

#### Key Concepts
- **Heuristic Function**: GBFS uses a heuristic function \( h(n) \) to guide its search.
- **Formula**: \( f(n) = h(n) \)
- **Explanation**: At each step, GBFS selects the node with the lowest heuristic value \( h(n) \), aiming to reach the goal as quickly as possible.
- **Drawback**: GBFS does not guarantee an optimal solution because it only considers the heuristic value without taking into account the actual cost of the path taken so far.

#### Visual Representation
- \( f(n) = h(n) \)
- \( h(n) = h^\infty n \) (This suggests an estimate of the cost to the goal)

### A* Algorithm

#### Key Concepts
- **Heuristic Function**: A* also uses a heuristic function \( h(n) \) but combines it with the actual cost of the path taken so far.
- **Formula**: \( f(n) = g(n) + h(n) \)
  - \( g(n) \): Actual cost from the start node to the current node \( n \).
  - \( h(n) \): Heuristic estimate of the cost from node \( n \) to the goal.
- **Explanation**: A* balances the cost of the path taken so far (\( g(n) \)) with the estimated cost to the goal (\( h(n) \)), making it more efficient than GBFS.
- **Advantage**: A* guarantees an optimal solution if the heuristic function is admissible (never overestimates the true cost).

#### Visual Representation
- \( f(n) = g(n) + h(n) \)
- \( g(n) \): Actual cost from start
- \( h(n) \): Heuristic

### Summary

- **Greedy Best First Search (GBFS)**:
  - Uses \( f(n) = h(n) \)
  - Selects nodes based solely on the heuristic value
  - Does not guarantee an optimal solution

- **A* Algorithm**:
  - Uses \( f(n) = g(n) + h(n) \)
  - Combines the actual cost of the path taken so far with the heuristic estimate
  - Guarantees an optimal solution if the heuristic is admissible

By understanding both GBFS and A*, you can choose the right algorithm depending on your specific problem requirements.
```