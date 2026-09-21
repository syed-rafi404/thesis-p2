# Python Fundamentals - Loops

In this lecture, we will learn about while loops and for loops in Python.

## Key takeaways
- A while loop runs until a condition becomes false.
- A for loop iterates over a sequence (like a list).
- The `range()` function generates a sequence of numbers.

## While Loops
The core idea of a while loop is to repeat a block of code as long as a specified condition is true.

### Example
```python
num = 0
while num < 10:
    print("yes")
    num = num + 1
```
![Board 1:20-3:10](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed from 3 video frames with the lecturer removed; 98% of the board is unobstructed.*

Watch out: Ensure the condition eventually becomes false to avoid an infinite loop.

## For Loops
A for loop is used for iterating over a sequence (such as a list).

### Example
```python
for i in range(10):
    print("yes")
range(10)
```
![Board 3:20-4:30](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed from 4 video frames with the lecturer removed; 98% of the board is unobstructed.*

## Working with Lists
We can use loops to perform operations on lists.

### Example
```python
list_1 = [70, 80, 50, 60]
length = len(list_1)
Sum = 0
for i in range(length):
    Sum = Sum + list_1[i]
```
![Board 5:30-9:00](figures_board/board_04_era4.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed from 9 video frames with the lecturer removed; 98% of the board is unobstructed.*

## Check yourself
1. Write a while loop that prints "yes" 10 times.
2. Write a for loop that prints "yes" 10 times.
3. What is the output of the following code?
   ```python
   list_1 = [70, 80, 50, 60]
   Sum = 0
   for i in range(len(list_1)):
       Sum = Sum + list_1[i]
   print(Sum)
   ```
4. What is the difference between `range(10)` and `range(10, 20)`?
5. How would you modify the above list summing code to include a new element 90?

## Answers
1. ```python
   num = 0
   while num < 10:
       print("yes")
       num = num + 1
   ```
2. ```python
   for i in range(10):
       print("yes")
   ```
3. The output is `260`.
4. `range(10)` generates numbers from 0 to 9, while `range(10, 20)` generates numbers from 10 to 19.
5. ```python
   list_1 = [70, 80, 50, 60, 90]
   Sum = 0
   for i in range(len(list_1)):
       Sum = Sum + list_1[i]
   print(Sum)
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*