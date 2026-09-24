# While and For Loops
Today we start learning about loops in Python, which are essential for handling repetitive tasks efficiently.

## Key takeaways
- Loops are fundamental in programming because they allow us to repeat a block of code multiple times without writing the same code repeatedly.
- We will learn about two types of loops: `while` loops and `for` loops.
- `while` loops run as long as a specified condition is true.
- `for` loops are used to iterate over a sequence of elements, such as a list or a range of numbers.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** Today we start learning about loops in Python, which are essential for handling repetitive tasks efficiently.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Red Box 1 (Title):** (while and For Loops)
- **Blue Box 2 (Code):** print("Yes")

The lecturer started by explaining the importance of loops in computing. He mentioned that computers are designed to handle repetitive tasks, and programming languages like Python provide mechanisms to make these tasks easier. In this lecture, we will focus on two types of loops: `while` loops and `for` loops.

The lecturer then introduced the `while` loop by showing an example. He wrote the following code on the board:

```python
print("Yes")
```

He explained that this is a simple piece of code that prints "Yes". To demonstrate how loops can simplify repetitive tasks, he asked, "What if we want to print 'Yes' 100 times?" Instead of writing the `print` statement 100 times, which would be impractical for larger numbers like thousands or millions, we can use a loop.

The lecturer then showed how to initialize a variable `num` to 0 and used a `while` loop to check if `num` is less than 100. Here’s the step-by-step breakdown:

1. Initialize `num` to 0.
2. Use a `while` loop to check if `num` is less than 100.
3. Inside the loop, print "Yes".
4. Increment `num` by 1 after each iteration.

The lecturer quoted, "So, amra ki korbo? Amra python e loop use korbo." This means, "So, what should we do? We should use a loop in Python."

### Extra jana kotha
Loops are fundamental in programming because they allow us to repeat a block of code multiple times without writing the same code repeatedly. Understanding how to use `while` loops is crucial for automating repetitive tasks efficiently. By using loops, we can save time and reduce the risk of errors that might occur if we manually write the same code multiple times.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**Ek line e:** In this section, we will understand how to use while and for loops in Python.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** While and For Loops
- **Box 2 (blue):** Code: `num=0 while num<10: print("yes") num=num+1`

The lecturer explained that when the value of `num` is less than 10, we enter the loop. Once `num` becomes greater than or equal to 10, the loop stops. He asked, "So currently, is `num`'s value less than 10?" He confirmed, "Obviously, zero is smaller than 10, so we are inside the loop and will print 'yes'."

The lecturer then pointed out that we need to increment `num` after each iteration to eventually exit the loop. He said, "First, let's do that." He showed the code where `num` is incremented by 1 after each iteration: `num = num + 1`.

He explained, "Here, `num` is 0, which is smaller than 10, so 'yes' will be printed. Next, `num` will become 1, and again, 1 is smaller than 10. This process continues until `num` reaches 10, at which point the loop stops. We have just created a while loop. Now, let's move on to for loops."

### Extra jana kotha (lecture e bola hoy ni)
For loops are widely used in Python because they are simple, easy to use, and user-friendly. They provide a convenient way to iterate over a sequence of items, such as a list or a range of numbers. Understanding both while and for loops is crucial for writing efficient and readable code.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## While and For Loops
**Ek line e:** For loops are used to iterate over a sequence of elements.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


- **Box 1 (red)**: This box introduces the topic of while and for loops.
- **Box 2 (blue)**: The code `for i in range(10): print("yes")` demonstrates how a for loop works. It prints "yes" 10 times.
- **Box 3 (orange)**: The function `range(10)` generates a sequence of numbers from 0 to 9.

**Ekhon amra ekta khub-i interesting jinis dekhbo last class e amra ki koreschilam. amra last class e list shikhechilam. list er moddhe amra onegula element rakhte pari. so amra ekta list nii. list 1. eno amra ekta list nilam. temon eta amardo kotogulam value raklam. je erokom dhoro 70, 80, 50, 60.**

The lecturer explains that in the previous class, we learned about lists. Lists allow us to store multiple elements. For example, we can create a list like `list1 = [70, 80, 50, 60]`.

The for loop in Box 2 (`for i in range(10): print("yes")`) is used to iterate over a sequence of numbers generated by the `range(10)` function. This function creates a sequence of numbers starting from 0 up to 9, which is a total of 10 numbers. However, the loop runs 10 times because the range function includes the start value (0) but excludes the end value (10).

The lecturer mentions that the range function starts from 0 and goes up to 9, making a total of 10 iterations. This is equivalent to a while loop running 10 times.

> Lecturer: "so, range er value shobshomoy amar ekhane je value deoya thake sheta teke 1 minus hobe. so ekhane range er value 10 daoa mane, range total 0 theke start hoy o 9th pojonto jabe total 10 times, which is equivalent to a while loop running total 10 times, okay?"

In summary, the for loop provides a convenient way to iterate over a sequence of numbers generated by the `range()` function. The `range(10)` function generates numbers from 0 to 9, resulting in 10 iterations.

**Mone rakho:** for loop, range function, 10 iterations, while loop equivalent.

<!-- boxes: 1=#d62828 -->
## While and For Loops
**Ek line e:** In this section, we will understand how to calculate the sum of elements in a list using a for loop.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1**: Here, we have a list named `list_1` containing the values `[70, 80, 50, 60]`. We want to find the total sum of these elements.

2. **Step 1**: First, we need to determine the length of the list. The length can be obtained using a built-in function. In Python, you can get the length of a list by using the `len()` function. This function returns the number of elements in the list.

3. **Step 2**: We initialize a variable `Sum` to zero. This variable will store the cumulative sum of the list elements.

4. **Step 3**: Next, we use a for loop to iterate over the list. The for loop runs from `0` to `length - 1`, which in this case is from `0` to `3`.

5. **Step 4**: Inside the loop, we update the `Sum` variable by adding the current element of the list to it. For example, in the first iteration, `Sum` becomes `0 + 70 = 70`. In the second iteration, `Sum` becomes `70 + 80 = 150`, and so on.

6. **Step 5**: After the loop completes, `Sum` will hold the total sum of all elements in the list. To verify this, we can print the value of `Sum` after the loop.

> Lecturer: "ebon ekhane ki anu million million amar velo thakte pare. amra arekta jinis chikhechilam length."

**Extra jana kotha**: When using a for loop, it's important to remember that the loop runs from `0` to `length - 1`. This ensures that all elements in the list are processed. Additionally, initializing variables before the loop and updating them within the loop is crucial for getting the correct result.

**Mone rakho**: Initialize `Sum` to zero, use `range(length)` in the for loop, and update `Sum` by adding each element of the list.

---

## Check yourself
1. What is the purpose of loops in programming?
2. How many times will the loop run in the code `num=0 while num<10: print("yes") num=num+1`?
3. What does the `range(10)` function generate?
4. How do you initialize a variable `Sum` to zero before using it in a for loop?
5. What is the difference between a `while` loop and a `for` loop?

### Answers
1. The purpose of loops in programming is to repeat a block of code multiple times without writing the same code repeatedly.
2. The loop will run 10 times.
3. The `range(10)` function generates a sequence of numbers from 0 to 9.
4. You initialize a variable `Sum` to zero using the statement `Sum = 0`.
5. A `while` loop runs as long as a specified condition is true, whereas a `for` loop is used to iterate over a sequence of elements.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
