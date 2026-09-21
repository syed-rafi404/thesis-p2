# Introduction to Variables and User Input in Python

One sentence: This lecture introduces how to use variables and user input in Python.

## Key takeaways
- Variables can hold dynamic values provided by the user.
- The `input()` function is used to get user input.
- By default, `input()` returns a string.
- Type casting is necessary to convert strings to integers.
- Python 3 supports formatted string literals (`f-strings`).

## Declaring Variables and Getting User Input
The core idea is to declare variables and get user input using the `input()` function.

```python
name = input("What is your name? ")
print("Hello", name)
```

![Board 0:00-1:00](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed from 6 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Example
- The `input()` function reads a string from the user.
- The `print()` function outputs the greeting along with the user's name.

Watch out: The `input()` function always returns a string.

## Using Variables for Arithmetic Operations
The core idea is to perform arithmetic operations using user-provided inputs.

```python
num1 = input("What is the first number? ")
num2 = input("What is the second number? ")
sum = int(num1) + int(num2)
print("Result is", sum)
```

![Board 1:10-3:10](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed from 9 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Example
- The user provides two numbers.
- These numbers are converted to integers using `int()`.
- The sum is calculated and printed.

Watch out: Ensure the input is converted to the appropriate data type before performing arithmetic operations.

## Using Formatted String Literals (f-strings)
The core idea is to use f-strings to format strings with variables.

```python
num1 = input("What is the first number? ")
num2 = input("What is the second number? ")
sum = int(num1) + int(num2)
print(f"The sum of {num1} and {num2} is {sum}")
```

![Board 4:20-7:30](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed from 10 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Example
- The user provides two numbers.
- These numbers are converted to integers using `int()`.
- The sum is calculated and printed using an f-string.

## Check Yourself
1. Write a program to get the user's name and greet them.
2. Write a program to get two numbers from the user and print their sum.
3. Write a program to get two numbers from the user and print their sum using an f-string.
4. What happens if you try to add a string and an integer without converting the string to an integer?
5. How can you ensure that the user input is correctly converted to an integer?

## Answers
1. ```python
   name = input("What is your name? ")
   print("Hello", name)
   ```
2. ```python
   num1 = input("What is the first number? ")
   num2 = input("What is the second number? ")
   sum = int(num1) + int(num2)
   print("Result is", sum)
   ```
3. ```python
   num1 = input("What is the first number? ")
   num2 = input("What is the second number? ")
   sum = int(num1) + int(num2)
   print(f"The sum of {num1} and {num2} is {sum}")
   ```
4. If you try to add a string and an integer without converting the string to an integer, Python will raise a TypeError.
5. Convert the string to an integer using `int()` before performing arithmetic operations.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*