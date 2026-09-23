# While and For Loops
This lecture covers the introduction to while and for loops in Python, explaining their basic structure and usage.

## Key takeaways
- Loops are used to perform repetitive tasks efficiently.
- A while loop continues to execute a block of code as long as a specified condition remains true.
- A for loop iterates over a sequence of values, making it easier to perform repetitive tasks.
- The `range()` function generates a sequence of numbers for a for loop to iterate over.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to While and For Loops
**In one line:** This board introduces the concepts of while and for loops in Python.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


### Explanation
1. **Introduction to Loops**: The lecturer begins by explaining that loops are powerful mechanisms that allow us to perform repetitive tasks efficiently. He mentions that computers have been designed to handle such tasks, and that Python provides two main types of loops: `while` and `for` loops.
2. **While Loop Example**: To illustrate the concept, the lecturer writes a simple `while` loop on the board. He initializes a variable `num` to 0 and explains that we will use a `while` loop to check if `num` is less than some value. In the red box, he writes the title "(while and For Loops)".
3. **For Loop Example**: The lecturer then demonstrates a `for` loop using the blue box, which contains the code `print("Yes")`. He explains that while loops are useful when we don't know how many times we need to repeat an action, but for loops are typically used when we know the exact number of iterations.

> Lecturer: "amra khubi interesting ebog powerful ekta jinishnese shipo, shetahole loops."
> (In English: "we learned an interesting and powerful mechanism, loops.")

**Remember:** Loops in Python, specifically `while` and `for` loops, are essential for performing repetitive tasks efficiently.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to While Loops and Basic Example
**In one line:** This example demonstrates how a while loop works by printing "yes" until a condition is met.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


### Explanation
1. **Understanding the While Loop**: The red box titled "While and For Loops" introduces the concept of a while loop. A while loop continues to execute a block of code as long as a specified condition remains true. In our example, we have `num = 0` and the loop runs as long as `num < 10`.
   
2. **Code Example**: The blue box shows the code snippet:
   ```python
   num = 0
   while num < 10:
       print("yes")
       num = num + 1
   ```
   Here, the loop starts with `num` set to 0. As long as `num` is less than 10, the loop will continue to execute.

3. **Loop Execution**: When the loop starts, `num` is 0, which is less than 10, so "yes" is printed. Then, `num` is incremented by 1. This process repeats until `num` becomes 10, at which point the condition `num < 10` is no longer true, and the loop stops.

4. **Iteration**: Each time through the loop, the value of `num` is checked against the condition. Since `num` starts at 0 and increases by 1 each iteration, it will print "yes" a total of 10 times before the loop terminates.

**Quote**
> "jotokhon nam er value ten er theke choto hobe, ami totokhon ei loop er moddhe jabo."  
> (In English: "as long as the value of `num` is less than 10, I will stay in this loop.")

**Remember:** The key point is that a while loop continues executing as long as its condition remains true, and it stops when the condition becomes false.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Introduction to For Loops and Their Mechanism
**In one line:** For loops automate the process of iterating over a sequence of values, making it easier to perform repetitive tasks.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


### Explanation
1. **Understanding the For Loop Structure**: Look at the blue box 2, which shows the code `for i in range(10): print("yes")`. This is a basic example of a for loop. The `for` keyword initiates the loop, `i` is the loop variable, and `range(10)` specifies the sequence of values the loop will iterate over.
   
2. **The Role of `range(10)`**: Refer to the orange box 3, which explains `range(10)`. This function generates a sequence of numbers starting from 0 up to, but not including, 10. Therefore, the loop will run 10 times, printing "yes" each time.

3. **Incrementing the Loop Variable**: In the red box 1, titled "While and For Loops," the lecturer explains that within the loop, we increment the loop variable `i` automatically. This means that after each iteration, the value of `i` changes, allowing the loop to progress through the sequence generated by `range(10)`.

4. **Counting Elements**: The lecturer mentions that when using `range(10)`, the loop will run 10 times because `range(10)` generates values from 0 to 9, inclusive. This means there are 10 elements in the sequence, even though the highest value is 9.

5. **Comparison with While Loops**: The lecturer draws a parallel between for loops and while loops, explaining that a for loop running 10 times is equivalent to a while loop that runs 10 times. For instance, if you have a while loop that increments a counter until it reaches 10, it would also run 10 times.

**Quote**
> "tar mane holo range er value ami ki? highest 9 porontor jabe."  
> (In English: "This means the highest value of range will be 9.")

**Remember:** For loops simplify the process of iterating over a sequence of values, making it easier to perform repetitive tasks without manually managing the loop variable.

<!-- boxes: 1=#d62828 -->
## Introduction to While and For Loops
**In one line:** We use a for loop to iterate over a list and calculate the sum of its elements.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The board shows a Python code snippet that demonstrates how to use a for loop to calculate the sum of elements in a list. Let's break down the code:

1. **Initialization**: `list_1 = [70, 80, 50, 60]` initializes a list with four elements.
2. **Finding Length**: `length = len(list_1)` calculates the number of elements in the list, which is 4.
3. **Initializing Sum**: `Sum = 0` sets the initial sum to zero.
4. **For Loop**: `for i in range(length):` starts a loop that will run 4 times, iterating over each index of the list.
5. **Updating Sum**: Inside the loop, `Sum = Sum + list_1[i]` updates the sum by adding the current element of the list to the existing sum.

The lecturer explains that the length of the list can be obtained using a built-in function. They also mention that the for loop runs from 0 to the length of the list minus one, updating the sum in each iteration.

> Lecturer: "ebon ekhane ki anu million million amar velo thakte pare. amra arekta jinis chikhechilam length. length ta tibabem da ber kori length amar ekta build-in function ache."
> (In English: "here we can have millions of elements. But we need to find the length of the list. We can get the length using a built-in function.")

**Remember:** The for loop is a powerful tool for iterating over collections like lists and performing operations on each element.

---

## Check yourself
1. What is the purpose of loops in Python?
2. How does a while loop work?
3. What does the `range()` function do in a for loop?
4. How do you initialize a variable to store the sum of elements in a list using a for loop?
5. What is the difference between a while loop and a for loop?

### Answers
1. Loops are used to perform repetitive tasks efficiently.
2. A while loop continues to execute a block of code as long as a specified condition remains true.
3. The `range()` function generates a sequence of numbers for a for loop to iterate over.
4. You initialize a variable to store the sum of elements in a list using a for loop by setting the variable to zero before the loop starts.
5. A while loop requires a condition to be specified, whereas a for loop iterates over a sequence of values.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
