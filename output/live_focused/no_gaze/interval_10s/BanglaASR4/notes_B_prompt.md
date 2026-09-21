# Python Fundamentals - Loops

In this lecture, we explore the basics of loops in Python, focusing on `while` and `for` loops.

## Key takeaways
- `while` loops execute a block of code repeatedly until a specified condition evaluates to `False`.
- `for` loops iterate over a sequence (such as a list) or a range of numbers.
- `range()` function generates a sequence of numbers.
- `len()` function returns the number of items in an object.

## Loops in Python
### While Loops
While loops are used to repeat a block of code as long as a specified condition is true.

#### Example
```python
name = 0
while name < 10:
    print("Ami Estha")
    name += 1
```
![Board 0:00-1:10](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–1:10, reconstructed from 8 video frames with the lecturer removed; 98% of the board is unobstructed.*

**Watch out:** The loop will run infinitely if the condition is never met.

### For Loops
For loops are used to iterate over a sequence (like a list) or a range of numbers.

#### Example
```python
for i in range(10):
    print(i)
```

#### Explanation
- `range(10)` generates numbers from 0 to 9.
- The loop iterates 10 times, printing each number from 0 to 9.

![Board 1:20-3:10](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:20–3:10, reconstructed from 3 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Working with Lists
We can use loops to perform operations on lists, such as calculating the sum of elements.

#### Example
```python
list1 = [70, 80, 50, 60]
sum = 0
for i in range(len(list1)):
    sum += list1[i]
print(sum)
```

#### Explanation
- `len(list1)` returns the number of elements in the list (4).
- The loop iterates 4 times, updating the `sum` variable with each element of `list1`.

![Board 3:20-4:30](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 3:20–4:30, reconstructed from 4 video frames with the lecturer removed; 98% of the board is unobstructed.*

## Check yourself
1. Write a `while` loop that prints "Hello" 5 times.
2. Write a `for` loop that prints the numbers from 0 to 9.
3. Calculate the sum of the elements in the list `[10, 20, 30, 40]` using a `for` loop.
4. What will happen if the condition in a `while` loop is never met?
5. What does `range(5)` generate?

### Answers
1. ```python
   i = 0
   while i < 5:
       print("Hello")
       i += 1
   ```
2. ```python
   for i in range(10):
       print(i)
   ```
3. ```python
   list1 = [10, 20, 30, 40]
   sum = 0
   for i in range(len(list1)):
       sum += list1[i]
   print(sum)
   ```
4. The loop will run infinitely.
5. `range(5)` generates numbers from 0 to 4.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*