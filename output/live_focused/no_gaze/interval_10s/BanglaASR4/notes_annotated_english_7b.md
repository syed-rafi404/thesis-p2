# While and For Loops
This lecture covers the introduction to while and for loops in Python, explaining their usage and importance in automating repetitive tasks.

## Key takeaways
- While loops continue to execute a block of code as long as a specified condition remains true.
- For loops are used to iterate over a sequence of values, such as a range of numbers or elements in a list.
- For loops simplify the process of iterating over a specific range of values, handling the increment and termination conditions automatically.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to While and For Loops
**In one line:** This board introduces the concepts of while and for loops in Python, explaining their importance and usage.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** Title: (while and For Loops)
- **Box 2 (blue):** Code: `print("Yes")`

The lecturer said: "hello everyone, welcome back to our last class of this series python fundamentals. In the previous class, we learned an interesting and powerful concept called loops. Computers have many powerful mechanisms, and one of the main motivations behind their invention was to automate repetitive tasks that humans would otherwise have to perform manually."

The lecturer explained that loops allow us to perform repetitive tasks easily. In Python, there are two main types of loops: while loops and for loops. We will start with while loops and then move on to for loops. To demonstrate, the lecturer wrote a simple print statement: `print("Yes")`.

The lecturer continued: "Let's consider a simple example where we want to print 'Yes' just once. That's easy. But what if we want to print 'Yes' 100 times? We would need to write the `print` function 100 times, which is impractical. Similarly, if we want to print it a thousand or a million times, writing it out manually would be impossible. So, how can we solve this problem? We can use loops in Python."

To illustrate, the lecturer introduced a variable `num` initialized to 0. The while loop is used to check a condition repeatedly until it becomes false. The lecturer asked: "Now let's see the condition. I have two values here. Let's check if `num` is less than 0. If `num` is less than 0, the loop will continue."

**Remember:** Using loops in Python allows us to automate repetitive tasks efficiently, making our code more manageable and scalable.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to While Loops and Basic Example
**In one line:** This board introduces the concept of a while loop and demonstrates its basic usage.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Understanding the While Loop**: The red box titled "While and For Loops" introduces the concept of a while loop. A while loop continues to execute a block of code as long as a specified condition remains true. In the blue box, we see an example of a while loop where `num` starts at 0 and increments by 1 until it reaches 10.

2. **Example Code**: The code in the blue box is:
   ```python
   num = 0
   while num < 10:
       print("yes")
       num = num + 1
   ```

3. **Explanation of the Code**:
   - Initially, `num` is set to 0.
   - The condition `num < 10` checks if `num` is less than 10.
   - As long as this condition is true, the code inside the loop will execute.
   - Inside the loop, the string "yes" is printed.
   - After printing, `num` is incremented by 1.
   - This process repeats until `num` becomes 10, at which point the condition `num < 10` becomes false, and the loop stops.

4. **The Loop Execution**:
   - When `num` is 0, the condition `0 < 10` is true, so "yes" is printed.
   - `num` is then incremented to 1.
   - The loop continues, printing "yes" and incrementing `num` until `num` reaches 10.
   - Once `num` is 10, the condition `10 < 10` is false, and the loop terminates.

5. **Importance of Iteration**: The lecturer explains that the loop needs to be controlled by iterating over the value of `num`. This is done by incrementing `num` within the loop body. The loop runs 10 times, printing "yes" each time.

> The lecturer said: "your English translation of what the lecturer said"

### Background
A while loop is a control flow statement that allows code to be executed repeatedly based on a given Boolean condition. It is useful when the number of iterations is not known beforehand. Common uses include scenarios where you need to perform an action until a specific condition is met, such as reading data from a file until the end of the file is reached.

**Remember:** The key point of this board is understanding how a while loop works and how to control the loop using a condition and iteration.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Understanding For Loops and Their Comparison with While Loops
**In one line:** A `for` loop automatically handles the increment and termination conditions, making it easier to iterate over a specific range of values.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


1. **Title: While and For Loops**
   - Look at the red box 1, which introduces the topic of `for` loops alongside `while` loops. The lecturer explains that a `for` loop is used to iterate over a sequence of values, such as a range of numbers.

2. **Code Example:**
   - The blue box 2 shows the code `for i in range(10): print("yes")`. This code snippet demonstrates how a `for` loop can be used to print "yes" 10 times.
   - The orange box 3, `range(10)`, represents the function that generates a sequence of numbers from 0 to 9.

3. **Explanation:**
   - The lecturer explains that in a `for` loop, we don't need to manually handle the increment or termination conditions. Instead, the loop automatically increments the variable `i` and checks if it should continue iterating based on the range provided.
   - The `range(10)` function generates a sequence of numbers from 0 to 9. The lecturer points out that even though there are 10 numbers in the sequence, the loop will run 10 times because the index starts from 0 and goes up to 9, inclusive.
   - The lecturer clarifies that the highest value in the range is 9, and since the range function includes both the start and end values, the loop will run 10 times, equivalent to a `while` loop running 10 times.

4. **Comparison with While Loop:**
   - The lecturer explains that if we were to implement the same functionality using a `while` loop, we would need to manually manage the increment and termination conditions. For example, if we want to print "yes" 10 times, we would need to initialize a counter, increment it within the loop, and check if it has reached 10.
   - The lecturer concludes by mentioning that in the previous class, they learned about lists. Lists allow us to store multiple elements, and in this context, we can use a `for` loop to iterate over the elements of a list.

> The lecturer said: "Your English translation of what the lecturer said" means that the `for` loop simplifies the process of iterating over a specific range of values, handling the increment and termination conditions automatically.

**Remember:** A `for` loop is particularly useful when you need to iterate over a fixed range of values, as it simplifies the code and reduces the risk of errors related to manual increment and termination conditions.

<!-- boxes: 1=#d62828 -->
## Calculating the Sum of List Elements Using a For Loop
**In one line:** This example demonstrates how to calculate the sum of elements in a list using a for loop.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Understanding the Code:**
   - Look at the red box 1. Here, we have a list `list_1` containing the elements `[70, 80, 50, 60]`.
   - We need to find the total sum of these elements.

2. **Finding the Length of the List:**
   - The lecturer said: "ekhane ki anu million million amar velo thakte pare. amra arekta jinis chikhechilam length. length ta tibabem da ber kori length amar ekta build-in function ache."
   - In the code, `length = len(list_1)` calculates the number of elements in the list. `len()` is a built-in function that returns the length of the list.

3. **Initializing the Sum Variable:**
   - The lecturer said: "total list er je length tar sheta ke amra length na amra ekta function aa sorry, variable er moddhe niye raktesi. ekhon ami chacchi je ei list er shobgulo value total sum ta koto hobe. so ami sum equal to zero."
   - We initialize `Sum = 0` to store the cumulative sum of the list elements.

4. **Using a For Loop:**
   - The lecturer said: "ami ekta for loop chalate pari. for i n and for i."
   - The for loop iterates over the range of the list's length. `for i in range(length)` means the loop will run from `0` to `length-1`, which is `0` to `3` in this case.

5. **Updating the Sum:**
   - The lecturer said: "so list 1 er je itemo value, ait value ta diye ami jinishter korbo. jerokom sum er value prothome amar 0 ache. tarpore first iteration e ki hobe? sum er value. aier value jokhon amar 0 length e ashbe o check korte korte korte korte korte"
   - Inside the loop, `Sum = Sum + list_1[i]` updates the sum by adding the current element of the list to the existing sum.

6. **Printing the Result:**
   - The lecturer said: "shetai holo amar total sum. ekhon arekta khubi important jeta, shetaholo ekta syntax error jeta shobai kore thake je print jinishta ekhane dey. print jodi sum-ta ekhane dii, ami pottek iteration e total sum-ta kota hoy sheta dekhte parbo."
   - After the loop, we can print the final sum using `print(Sum)` to see the total sum of the list elements.

### Background
A for loop is a control flow statement that allows code to be executed repeatedly based on a condition. It is particularly useful when you know the exact number of iterations needed, such as iterating over the elements of a list. The concept of a for loop is fundamental in programming and is widely used in various applications, including data processing and algorithm implementation.

**Remember:** The key point is understanding how to use a for loop to iterate over a list and perform operations on its elements, such as calculating the sum.

---

## Check yourself
1. What is the purpose of a while loop in Python?
2. Write a while loop that prints "yes" 10 times.
3. Explain the difference between a while loop and a for loop.
4. How do you calculate the sum of elements in a list using a for loop?
5. What is the role of the `range()` function in a for loop?

### Answers
1. A while loop in Python is used to execute a block of code repeatedly as long as a specified condition remains true.
2. ```python
   num = 0
   while num < 10:
       print("yes")
       num += 1
   ```
3. A while loop requires a condition to be checked before each iteration, whereas a for loop is used to iterate over a sequence of values, such as a range or elements in a list, and handles the increment and termination conditions automatically.
4. You calculate the sum of elements in a list using a for loop by initializing a sum variable to 0, iterating over the list, and adding each element to the sum.
5. The `range()` function in a for loop generates a sequence of numbers, allowing the loop to iterate over a specific range of values.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (2 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
