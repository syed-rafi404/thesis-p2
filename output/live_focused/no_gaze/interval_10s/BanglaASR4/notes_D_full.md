# Python Fundamentals - Loops

In this lecture, we will learn about loops in Python, specifically focusing on `while` loops and `for` loops. We will also see how to use loops to perform repetitive tasks and calculate the sum of elements in a list.

## Key takeaways
- `while` loops run until a certain condition is no longer met.
- `for` loops iterate over a sequence of items.
- `range()` function generates a sequence of numbers.
- `len()` function returns the length of a list.

## While Loops
### Core Idea
A `while` loop continues to execute a block of code as long as a specified condition is true.

### Worked Example
```python
num = 0
while num < 10:
    print("yes")
    num = num + 1
```
![Board 1:20-3:10](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed from 3 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Watch out:
- The loop will run infinitely if the condition never becomes false.
- Ensure the loop has a way to exit, such as updating the loop variable.

## For Loops
### Core Idea
A `for` loop iterates over a sequence (such as a list, tuple, dictionary, set, or string).

### Worked Example
```python
for i in range(10):
    print("yes")
range(10)
```
![Board 3:20-4:30](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed from 4 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Watch out:
- `range(n)` generates a sequence of numbers from 0 to n-1.
- The loop variable `i` takes on each value in the sequence.

## Using Loops with Lists
### Core Idea
We can use loops to perform operations on lists, such as calculating the sum of all elements.

### Worked Example
```python
list_1 = [70, 80, 50, 60]
length = len(list_1)
Sum = 0
for i in range(length):
    Sum = Sum + list_1[i]
```
![Board 5:30-9:00](figures_board/board_04_era4.jpg)

*Figure 4. The whiteboard during 5:30–9:00, reconstructed from 9 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Watch out:
- `len(list_1)` returns the number of elements in the list.
- The loop updates the `Sum` variable by adding each element of the list.

## Check yourself
1. Write a `while` loop that prints "Hello" 5 times.
2. Write a `for` loop that prints the numbers from 0 to 9.
3. Calculate the sum of the elements in the list `[10, 20, 30, 40]`.

### Answers
1. ```python
   num = 0
   while num < 5:
       print("Hello")
       num += 1
   ```
2. ```python
   for i in range(10):
       print(i)
   ```
3. ```python
   my_list = [10, 20, 30, 40]
   total_sum = 0
   for i in range(len(my_list)):
       total_sum += my_list[i]
   print(total_sum)
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*