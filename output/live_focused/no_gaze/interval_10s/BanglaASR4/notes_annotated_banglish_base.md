# While and For Loops
Today, we dive into the world of loops in Python, specifically focusing on `while` and `for` loops.

## Key takeaways
- The title of the board is "While and For Loops," indicating that we will cover both types of loops today.
- A `while` loop continues to execute a block of code as long as a specified condition is true.
- A `for` loop is used to iterate over a sequence of numbers or elements in a collection.
- The `range` function generates a sequence of numbers, which the `for` loop can iterate over.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** Today, we dive into the world of loops in Python, specifically focusing on `while` and `for` loops.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Red Box 1 (Title):** (while and For Loops)
- **Blue Box 2 (Code):** `print("Yes")`

The lecturer starts by introducing the importance of loops in programming. He explains that loops are essential for repetitive tasks, making the computer perform actions multiple times without manual intervention. This is particularly useful when the number of iterations is large, such as printing "Yes" a hundred or even a million times.

The lecturer then demonstrates a simple `print` statement using the `print("Yes")` command. This is just a starting point to illustrate how basic output can be achieved using loops.

**Mone rakho:** The title of the board is "While and For Loops," indicating that we will cover both types of loops today. The code in the blue box simply prints "Yes" to the console, showing a basic usage of the `print` function.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** In this section, we will discuss while and for loops.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Box 1 (red):** The title "While and For Loops" introduces the topic.
2. **Box 2 (blue):** The code `num=0 while num<10: print("yes") num=num+1` demonstrates a while loop.

The lecturer starts by explaining the while loop using the provided code. Let's break it down step by step:

- **Step 1:** The variable `num` is initialized to 0.
- **Step 2:** The condition `num < 10` checks if `num` is less than 10. Since 0 is indeed less than 10, the loop starts.
- **Step 3:** Inside the loop, the statement `print("yes")` is executed, printing "yes" to the console.
- **Step 4:** The line `num=num+1` increments the value of `num` by 1.
- **Step 5:** The condition `num < 10` is checked again. As long as `num` is less than 10, the loop continues. Once `num` becomes 10, the condition fails, and the loop stops.

> Lecturer: "When the name is small, I will go to the loop. When the name is small, I will be in the loop. When the name is small, I will be in the loop."

The lecturer explains that when the condition is true, the loop continues. In this case, the condition `num < 10` is initially true because `num` is 0, which is less than 10. Therefore, the loop runs and prints "yes" repeatedly until `num` reaches 10.

### Extra jana kotha (lecture e bola hoy ni)
For loops, on the other hand, are more user-friendly and often used for iterating over sequences like lists or ranges. They provide a straightforward way to perform actions a specific number of times, making the code cleaner and easier to read.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## While and For Loops
**Ek line e:** For loops are used to iterate over a sequence of numbers.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


- **Red Box 1 (While and For Loops)**: This box introduces the topic of while and for loops. The lecturer explains that for loops are used to iterate over a sequence of numbers.
  
- **Blue Box 2 (Code)**: The lecturer demonstrates a simple for loop with the following code:
  ```python
  for i in range(10):
      print("yes")
  ```
  This code will print "yes" ten times. The `range(10)` function generates a sequence of numbers from 0 to 9, which the for loop iterates over.

- **Orange Box 3 (Function range(10))**: The `range(10)` function generates a sequence of numbers from 0 to 9. The lecturer points out that the highest value in this sequence is 9, and there are a total of 10 elements in the sequence.

> Lecturer: "I can see the range of 10 times."

The lecturer emphasizes that the for loop automatically increments the variable `i` and changes its value to the next number in the sequence. This process repeats until the loop has iterated over all the numbers generated by `range(10)`.

### Extra jana kotha (lecture e bola hoy ni)
For loops are useful when you need to perform an action a specific number of times. In this case, the for loop prints "yes" ten times, demonstrating how the loop iterates over the sequence generated by `range(10)`. Understanding the range function and how it works is crucial for using for loops effectively.

**Mone rakho:** For loops use the `range` function to generate a sequence of numbers, which the loop iterates over. The `range(10)` function generates numbers from 0 to 9, and the for loop prints "yes" ten times.

<!-- boxes: 1=#d62828 -->
## While and For Loops
**Ek line e:** This section covers the usage of `for` loops to iterate over lists and calculate sums.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1:** The code initializes a list and calculates the sum of its elements using a `for` loop.
   - `list_1 = [70, 80, 50, 60]`: This line defines a list named `list_1` containing four integers.
   - `length = len(list_1)`: This line calculates the length of the list and stores it in the variable `length`.
   - `Sum = 0`: This line initializes the variable `Sum` to 0, which will store the cumulative sum of the list elements.
   - `for i in range(length):`: This line starts a `for` loop that iterates over the indices of the list.
   - `Sum = Sum + list_1[i]`: Inside the loop, this line adds the current element of the list to the `Sum`.

2. **Explanation:** The `for` loop iterates over each element in the list `list_1`. It starts with the first element (index 0) and adds it to `Sum`. Then it moves to the next element (index 1) and adds it to `Sum`, and so on until all elements have been added. The final value of `Sum` is the total sum of all elements in the list.

> Lecturer: "So, we can use length."

3. **Calculation:** Let's break down the calculation step-by-step:
   - Initially, `Sum = 0`.
   - First iteration: `i = 0`, `Sum = 0 + 70 = 70`.
   - Second iteration: `i = 1`, `Sum = 70 + 80 = 150`.
   - Third iteration: `i = 2`, `Sum = 150 + 50 = 200`.
   - Fourth iteration: `i = 3`, `Sum = 200 + 60 = 260`.

4. **Output:** After the loop completes, the value of `Sum` is 260. To display this result, you would add a `print` statement outside the loop, like `print(Sum)`.

### Extra jana kotha
When using a `for` loop to iterate over a list, it's important to initialize your sum variable before starting the loop. This ensures that the loop correctly accumulates the values. Additionally, always check the length of the list to avoid accessing an index that doesn't exist.

---

## Check yourself
1. What does the `while` loop in the code `num=0 while num<10: print("yes") num=num+1` do?
2. How many times will the `for` loop in the code `for i in range(10): print("yes")` print "yes"?
3. What is the purpose of the `range` function in the `for` loop `for i in range(10): print("yes")`?
4. What is the final value of `Sum` after running the `for` loop in the code `list_1 = [70, 80, 50, 60] length = len(list_1) Sum = 0 for i in range(length): Sum = Sum + list_1[i]`?
5. Why is it important to initialize the `Sum` variable before starting the `for` loop?

### Answers
1. The `while` loop prints "yes" ten times, incrementing `num` by 1 each time until `num` is no longer less than 10.
2. The `for` loop will print "yes" ten times.
3. The `range` function generates a sequence of numbers from 0 to 9, which the `for` loop iterates over.
4. The final value of `Sum` is 260.
5. Initializing the `Sum` variable before starting the `for` loop ensures that the loop correctly accumulates the values.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
