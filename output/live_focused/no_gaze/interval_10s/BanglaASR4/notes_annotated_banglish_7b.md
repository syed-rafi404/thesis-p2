# While and For Loops
This lecture covers the basics of while and for loops in Python, explaining their usage and importance in automating repetitive tasks.

## Key takeaways
- While and for loops are essential for performing repetitive tasks in Python.
- A `while` loop continues executing a block of code as long as a specified condition is true.
- A `for` loop is used to iterate over a sequence (such as a list) a specific number of times.
- The `range()` function generates a sequence of numbers that can be used in a `for` loop.
- Loops can be used to calculate the sum of elements in a list.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## (while and For Loops)
**Ek line e:** While and for loops are powerful mechanisms in Python.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


**Red Box 1 (while and For Loops):** The title clearly states that we will be discussing while and for loops. These loops are essential for performing repetitive tasks in Python.

**Blue Box 2 (Code):** print("Yes") - This simple code snippet demonstrates how to print a message. We will use loops to automate more complex tasks like printing "Yes" multiple times.

> Lecturer: "computer e shobtheke powerful mechanism hocche she reputation e khubi expert."

### Explanation
The lecturer explains that computers are designed to handle repetitive tasks efficiently. In the previous classes, we learned about basic concepts and now we are moving on to loops, which are fundamental for automating repetitive processes. Python provides two types of loops: `while` and `for`. We will start with `while` loops and then move on to `for` loops.

### Example
To illustrate the concept, the lecturer mentions that if we want to print "Yes" 100 times, manually writing the `print` statement 100 times would be impractical. Instead, we can use a loop to achieve this. The `while` loop is introduced as a solution to this problem.

### How to Use a `while` Loop
The lecturer demonstrates by initializing a variable `num` to 0. The `while` loop is used to continue executing the block of code as long as the condition `num < 100` is true. Each time the loop runs, the value of `num` is incremented by 1 until it reaches 100.

**Mone rakho:** We will use loops to automate repetitive tasks, starting with the `while` loop.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** While and For Loops

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


**Explanation:**
1. **Red Box 1 (While and For Loops):** The red box introduces the topic of `while` and `for` loops. These are fundamental constructs in programming used for repetition based on certain conditions.
2. **Blue Box 2 (Code):** The blue box contains an example of a `while` loop. The code initializes a variable `num` to 0 and enters a loop that continues as long as `num` is less than 10. Inside the loop, it prints "yes" and increments `num` by 1.

The lecturer explains that when `num` is less than 10, the loop will continue. Once `num` becomes 10, the loop will stop. The lecturer also mentions that the loop will run 10 times, printing "yes" each time.

**Quotes:**
> Lecturer: "jokhon ekhane nam er value ta ten er theke boro hoye jabe or ten er shoman hobe, tokhon ami lupe dhukbo na."
> Lecturer: "so amar ekta kajkotto hobe sheta holo iteration ta dite hobe."

**Mone rakho:** The `while` loop in the blue box runs 10 times, printing "yes" each time. The loop starts with `num = 0`, and it continues as long as `num` is less than 10. After each iteration, `num` is incremented by 1. When `num` reaches 10, the loop stops. This demonstrates how a `while` loop works and how it can be used to repeat a block of code multiple times.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## While and For Loops
**Ek line e:** For loops are a convenient way to iterate over a specific number of times.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


**Explanation:**
1. **Red Box 1 (While and For Loops):** The lecturer introduced the topic of while and for loops, explaining how they are used to perform repetitive tasks.
2. **Blue Box 2 (Code):** The lecturer demonstrated a simple for loop using the code `for i in range(10): print("yes")`. This loop will print "yes" 10 times.
3. **Orange Box 3 (Function):** The function `range(10)` was explained, showing that it generates a sequence of numbers from 0 to 9.

The lecturer then explained the mechanics of the for loop:
- The for loop allows you to easily repeat a block of code a specific number of times.
- Inside the for loop, you can perform operations such as printing a message.
- The loop automatically increments the variable `i` after each iteration.

The lecturer further elaborated on the `range(10)` function:
- `range(10)` generates a sequence of numbers starting from 0 up to, but not including, 10.
- Therefore, the loop will run 10 times, even though the sequence generated by `range(10)` contains only 9 elements (0 through 9).

**Quote:**
> "so range er value shobshomoy amar ekhane je value deoya thake sheta teke 1 minus hobe."

**Mone rakho:** The for loop runs 10 times, even though the range function generates only 9 numbers. The loop starts from 0 and goes up to 9, making a total of 10 iterations.

<!-- boxes: 1=#d62828 -->
## While and For Loops
**Ek line e:** This section explains how to calculate the sum of elements in a list using a for loop.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


**Explanation:**
1. **Red Box 1:** In the red box, we see a simple example of calculating the sum of elements in a list using a for loop. The list `list_1` contains the values `[70, 80, 50, 60]`.
2. **Length Calculation:** The lecturer explains that we need to find the length of the list, which can be done using the built-in `len()` function. This function returns the number of elements in the list.
3. **Initialization:** We initialize a variable `Sum` to zero. This will store the cumulative sum of the list elements.
4. **For Loop:** The for loop iterates over the range of the list's length. In each iteration, the current element of the list is added to `Sum`.
5. **Iteration Process:** The loop runs four times because the list has four elements. In each iteration, the value of the current element is added to `Sum`, updating its value.
6. **Final Sum:** After all iterations, the final value of `Sum` is the total sum of the list elements.

**Quote:**
> "ekhon amra ki? e length ta diye dite pari. for in, range-er moddhe length."

**Mone Rakho:** The important points from the board include initializing `Sum` to zero, using the `len()` function to get the list's length, and iterating over the list elements to calculate the total sum.

---

## Check yourself
1. What is the purpose of a `while` loop?
2. How many times does the for loop `for i in range(10): print("yes")` run?
3. What does the `range(10)` function generate?
4. How do you initialize a variable to store the sum of a list's elements?
5. What is the final value of `Sum` after running the for loop to sum the elements of `[70, 80, 50, 60]`?

### Answers
1. A `while` loop continues executing a block of code as long as a specified condition is true.
2. The for loop `for i in range(10): print("yes")` runs 10 times.
3. The `range(10)` function generates a sequence of numbers from 0 to 9.
4. You initialize a variable to store the sum of a list's elements by setting it to zero, e.g., `Sum = 0`.
5. The final value of `Sum` after running the for loop to sum the elements of `[70, 80, 50, 60]` is 260.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 5 kept, 0 removed. References to boxes that do not exist: 0.*
