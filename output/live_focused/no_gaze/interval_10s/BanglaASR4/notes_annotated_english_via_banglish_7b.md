# (while and For Loops)
Today we will learn about while and for loops in Python.

## Key takeaways
- While loops allow us to repeat a block of code until a certain condition is met.
- For loops are a convenient way to iterate over a specific number of times.
- The `range()` function generates a sequence of numbers for iteration.
- We can use for loops to perform operations on list elements.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## (while and For Loops)
**In one line:** Today we will learn about while and for loops in Python.

![Board 1: 0:00-1:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Red Box 1 (Title):** (while and For Loops)
- **Blue Box 2 (Code):** print("Yes")

The lecturer started by explaining the importance of loops in computing. He said, "computer e shobtheke powerful mechanism hocche she reputation e khubi expert." This means that computers have become experts due to their powerful mechanisms. The main motivation behind the invention of computers was to automate repetitive tasks that humans would otherwise have to do manually.

Next, the lecturer introduced two types of loops in Python: while loops and for loops. He mentioned, "toh python e amar duitaitar mainly loops reche, while loops and for loops." We will start with while loops and then move on to for loops. To demonstrate, he wrote `print("Yes")` on the board.

The lecturer explained that if we want to print "Yes" 100 times, we would need to write the `print` function 100 times. If we want to print it a thousand or even a million times, writing it out manually would be impractical. Therefore, we need to use loops to automate this process. He wrote `num = 0` on the board and then introduced the while loop syntax: `while`. He asked, "ami ekhane duita value diyeyshi. ekhon amar ka jolo je num zero theke amar ki choto naki, ekhon tenet theke choto naki."

**Remember:** While loops allow us to repeat a block of code until a certain condition is met. In this case, we initialize a variable `num` to 0 and use a while loop to check if `num` is less than a certain value.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## While and For Loops
**In one line:** While and for loops are fundamental concepts in programming.

![Board 2: 1:20-3:10](figures_annotated/board_era2_120.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** While and For Loops
- **Box 2 (blue):** Code: `num=0 while num<10: print("yes") num=num+1`

The lecturer said: "When the value of `num` is less than 10, we enter the loop. Once `num` becomes equal to or greater than 10, the loop stops. He asked if everyone understood, confirming that the initial value of `num` is 0, which is indeed less than 10, so the loop runs. The lecturer then pointed out that we print 'yes' each time the loop runs, but this would continue infinitely without a mechanism to change `num`. To fix this, we need to increment `num` inside the loop."

The lecturer further clarified that in this example, `num` starts at 0 and is printed. Then, `num` is incremented by 1 each time the loop runs. He demonstrated that since 0 is less than 10, "yes" is printed. After the first iteration, `num` becomes 1, and since 1 is also less than 10, "yes" is printed again. This process continues until `num` reaches 10, at which point the condition `num < 10` is no longer true, and the loop stops.

The lecturer then mentioned that we can use a conditional statement within the loop, and that we will learn more about while loops. He transitioned to for loops, stating that for loops are commonly used and very user-friendly in Python. Unlike while loops, for loops do not require an initial value assignment and a condition check; instead, they iterate over a sequence of items.

### Background (not said in the lecture) (lecture e bola hoy ni)
For loops are simpler and more readable compared to while loops. They are particularly useful when you know the number of iterations in advance. For example, if you want to print "yes" 10 times, a for loop would be more straightforward.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## While and For Loops
**In one line:** For loops are a convenient way to iterate over a specific number of times.

![Board 3: 3:20-4:30](figures_annotated/board_era3_320.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code · 3 Function


- **Box 1 (red)**: Title: (While and For Loops)
- **Box 2 (blue)**: Code: `for i in range(10): print("yes")`
- **Box 3 (orange)**: Function: `range(10)`

The lecturer said: "For loops are a convenient way to iterate over a specific number of times."

The lecturer explained that when we use a for loop, we can easily perform an action multiple times. In the example given, the for loop will print "yes" 10 times. The for loop automatically increments the variable `i` after each iteration, making it easier to manage the loop's counter.

The function `range(10)` generates a sequence of numbers starting from 0 up to, but not including, 10. This means the loop will run 10 times, even though the highest number generated is 9. The lecturer pointed out that if we want to count the elements in the range, we need to consider that the range starts from 0 and goes up to 9, making a total of 10 elements.

To clarify further, the lecturer stated:
> "range er value total 9 porontor jabe, 10 porontor jabe na. but ami jodi count khore dekhi, amar total element ekhane 10 e ache."

This means that although the highest number in the range is 9, the total number of iterations is 10 because the range includes 0. Therefore, the value passed to `range()` should be 10 to achieve 10 iterations.

The lecturer also mentioned that in the previous class, they learned about lists. Lists allow us to store multiple elements. For example, we can create a list like `list1 = [70, 80, 50, 60]`. This list contains four elements, and we can use a for loop to iterate over these elements.

**Remember:** for loop, range function, and list elements.

<!-- boxes: 1=#d62828 -->
## While and For Loops
**In one line:** This section explains how to calculate the sum of elements in a list using a for loop.

![Board 4: 5:30-9:00](figures_annotated/board_era4_530.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1:** The code initializes a list `list_1` with four elements: `[70, 80, 50, 60]`. It also calculates the length of the list and initializes a variable `Sum` to zero.

2. **Step 1:** The lecturer explains that the length of the list can be obtained using a built-in function `len()`. This function returns the number of elements in the list. In this case, the list has four elements, so `length` will be 4.

3. **Step 2:** The lecturer introduces a for loop to iterate over each element in the list. The loop variable `i` takes values from 0 to `length - 1`, which is 3 in this case. The loop updates the `Sum` variable by adding each element of the list to it.

4. **Step 3:** During the first iteration, `i` is 0, and `Sum` is updated to `Sum + list_1[0]`, which is `0 + 70`. In the second iteration, `i` is 1, and `Sum` becomes `70 + 80`, resulting in `150`. In the third iteration, `i` is 2, and `Sum` is updated to `150 + 50`, giving `200`. Finally, in the fourth iteration, `i` is 3, and `Sum` is updated to `200 + 60`, resulting in `260`.

5. **Step 4:** The lecturer mentions that if you want to see the value of `Sum` after each iteration, you can place a `print()` statement inside the loop. However, for the final sum, you should place the `print()` statement outside the loop.

6. **Step 5:** The final sum, `260`, is the total of all elements in the list. This demonstrates a basic for loop structure in Python.

> Lecturer: "ekhon arekta khubi important jeta, shetaholo ekta syntax error jeta shobai kore thake je print jinishta ekhane dey."

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding for loops is crucial for performing operations on collections of data. By iterating over each element, you can perform calculations or manipulations that would be tedious to do manually. For example, you can use for loops to find the average of a list of numbers, count the occurrences of a specific value, or even modify each element in a list.

---

## Check yourself
1. What does a while loop do?
2. How many times will the for loop `for i in range(10): print("yes")` print "yes"?
3. What is the purpose of the `range()` function in a for loop?
4. How do you initialize a variable to zero before using it in a for loop to calculate the sum of a list?
5. What is the final value of `Sum` after running the for loop in the example provided?

### Answers
1. A while loop repeats a block of code until a certain condition is met.
2. The for loop `for i in range(10): print("yes")` will print "yes" 10 times.
3. The `range()` function generates a sequence of numbers for iteration.
4. You initialize a variable to zero before using it in a for loop to calculate the sum of a list by setting `Sum = 0`.
5. The final value of `Sum` after running the for loop in the example provided is 260.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (2 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
