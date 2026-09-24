# While and For Loops
THE SECTIONS

## Key takeaways
- The `while` loop is used to execute a block of code repeatedly until a specified condition becomes false.
- The `for` loop is used to iterate over a sequence of items a specific number of times.
- A `for` loop automatically handles the incrementing of the loop variable.
- To sum elements of a list, initialize a sum variable before the loop and use the length of the list to control the loop.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** Today, we dive into the world of loops in Python, specifically focusing on `while` and `for` loops.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** (while and For Loops)
- **Box 2 (blue):** Code: `print("Yes")`

The lecturer starts by emphasizing the importance of loops in Python. He explains that loops are essential because they allow us to perform repetitive tasks efficiently. The lecturer mentions, "The main reason for this is that the manual level is to use the repetitive work of the computer." This means that instead of manually repeating a task, we can automate it using loops.

Next, the lecturer introduces the concept of a `while` loop. He states, "so yes a genius time print could be small actor yes yes yes to the total hundred times print cut the chai the like a mirror from hundred by the print function of the legal I'm to the thousand or million times try telecom it like a feasible for a human so I'm not a key corvo I'm gonna Python and loop use corvo." This quote highlights how a `while` loop can handle repetitive tasks much more efficiently than a human could.

To demonstrate, the lecturer writes a simple `while` loop where the variable `number` is initialized to 0. He explains, "I will call the initial value in the variable, the number number is 0. So, I will start with the first while loop. Okay, this is the number number. I will give you the number number. This is the number number number."

In summary, today we learned about the power of loops in Python, particularly the `while` loop, which allows us to automate repetitive tasks efficiently.

**Mone rakho:** The `while` loop is used to execute a block of code repeatedly until a specified condition becomes false. The initial value of the variable `number` is set to 0, and the loop continues to run as long as the condition remains true.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** In this section, we will discuss while and for loops in Python.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** While and For Loops
- **Box 2 (blue):** Code: `num=0 while num<10: print("yes") num=num+1`

The lecturer started by explaining the concept of a while loop. He mentioned, "When the name is small, I will go to the loop. When the name is small, I will be in the loop. When the name is small, I will be in the loop." This means that as long as the condition is true, the loop will continue to execute. In the given code, the variable `num` is initially set to 0. The condition `num<10` checks if `num` is less than 10. Since 0 is indeed less than 10, the loop runs and prints "yes".

The lecturer then explained that the loop will run infinitely until the condition becomes false. To stop the loop, the value of `num` is incremented by 1 after each iteration (`num=num+1`). This ensures that eventually, `num` will no longer be less than 10, and the loop will terminate.

Next, the lecturer introduced the for loop, stating, "So, let's get into now for loops. For loops, we used a loop in Python that was very popular, very easy, very user-friendly." For loops are typically used when you know the number of iterations in advance. They provide a more concise way to iterate over a sequence of items.

In summary, the while loop continues to execute as long as a specified condition is true, while the for loop iterates over a sequence of items a specific number of times.

**Mone rakho:** The key points from Box 2 are the code snippet showing a while loop and the explanation of how the loop runs until the condition becomes false.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## While and For Loops
**Ek line e:** For loops are used to iterate over a sequence of numbers.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


- **Red Box 1 (While and For Loops):** This box introduces the concept of while and for loops. For loops are particularly useful for iterating a specific number of times.
  
- **Blue Box 2 (Code):** The code `for i in range(10): print("yes")` demonstrates a for loop. Here, `range(10)` generates a sequence of numbers from 0 to 9. The loop will execute the statement `print("yes")` ten times, printing "yes" each time.

- **Orange Box 3 (Function):** The function `range(10)` is shown here. It generates a sequence of numbers starting from 0 up to, but not including, 10. This means the sequence includes the numbers 0, 1, 2, 3, 4, 5, 6, 7, 8, and 9, totaling 10 elements.

> Lecturer: "I easily 10 times print for looping. I can see how much it is. Automatically, the increment is done, the higher value is changed."

The for loop automatically increments the variable `i` each time it iterates, starting from 0 and ending at 9. This is why the loop runs 10 times.

### Extra jana kotha (lecture e bola hoy ni)
For loops are essential for tasks that require repetitive actions, such as processing a list of items or performing an operation a fixed number of times. Understanding how to use for loops effectively is crucial for writing efficient and readable code.

<!-- boxes: 1=#d62828 -->
## While and For Loops
**Ek line e:** In this section, we will understand how to use for loops to calculate the sum of a list.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1:** The code here initializes a list and calculates the sum using a for loop. Let's break it down step by step.

2. **Step 1:** `list_1 = [70, 80, 50, 60]` - This line creates a list named `list_1` containing four elements: 70, 80, 50, and 60.

3. **Step 2:** `length = len(list_1)` - Here, we find the length of the list, which is 4. This is stored in the variable `length`.

4. **Step 3:** `Sum = 0` - We initialize the variable `Sum` to 0. This will hold the cumulative sum of the list elements.

5. **Step 4:** `for i in range(length):` - This starts a for loop that iterates over the range of the length of the list. In this case, it will run 4 times, from 0 to 3.

6. **Step 5:** `Sum = Sum + list_1[i]` - Inside the loop, we add the current element of the list (`list_1[i]`) to the `Sum`. The loop will add each element of the list to `Sum` in sequence.

7. **Explanation:** The loop runs four times, adding each element of the list to `Sum`. After the loop completes, `Sum` will hold the total sum of all elements in the list.

> Lecturer: "So, we can use length."

The loop iterates over the indices of the list, and `list_1[i]` gives us the value at each index. For example, in the first iteration, `i` is 0, so `list_1[0]` is 70, and `Sum` becomes 70. In the second iteration, `i` is 1, so `list_1[1]` is 80, and `Sum` becomes 150. This process continues until all elements are added.

### Extra jana kotha
When using a for loop to sum elements of a list, it's important to initialize the sum variable before the loop starts. This ensures that the loop can correctly accumulate the values. Also, always check the length of the list to avoid accessing an index that doesn't exist.

---

## Check yourself
1. What does the `while` loop do?
2. How does a `for` loop differ from a `while` loop?
3. What is the purpose of the `range()` function in a `for` loop?
4. How do you initialize a variable to store the sum of a list's elements?
5. Why is it important to use the length of the list when iterating with a `for` loop?

### Answers
1. The `while` loop executes a block of code repeatedly as long as a specified condition is true.
2. The `for` loop iterates over a sequence of items a specific number of times, whereas the `while` loop continues until a condition becomes false.
3. The `range()` function generates a sequence of numbers, which is used to control the number of iterations in a `for` loop.
4. You initialize a variable to store the sum of a list's elements, such as `sum = 0`.
5. It is important to use the length of the list when iterating with a `for` loop to ensure that you do not access an index that does not exist.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
