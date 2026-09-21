# Conditional Statements and Decision Making in Python

## Introduction
In this lecture, we will explore how computers make logical decisions using conditional statements. Specifically, we will cover `if`, `elif`, and `else` statements and how they are used to handle different conditions based on user inputs.

## Key Definitions
- **Weather**: This is the input provided by the user regarding the current weather condition. It can be "rain", "sunny", or any other condition.
  
## Conditional Statements
Conditional statements allow the program to execute different blocks of code based on certain conditions. The basic structure of a conditional statement in Python is as follows:

```python
if condition:
    # code to be executed if the condition is true
else:
    # code to be executed if the condition is false
```

### Example: Using `if` and `else`
Let's create a program that checks the weather and decides whether the user needs to bring an umbrella or not.


![Board 0:00-5:50](figures_board/board_01_era1.jpg)

**Figure 1.** Whiteboard as it stood during 0:00&ndash;5:50, reconstructed from 11 video frames with the lecturer removed. 100.0% of the board is unobstructed.

#### Code Snippet
```python
# Get user input for today's weather
weather = input("Today's weather: ")

# Check if it is raining
if weather == "rain":
    print("Bring umbrella")
else:
    print("Just come")
```

### Example: Using `if-elif-else`
We can also use `elif` to handle multiple conditions.

#### Code Snippet
```python
# Get user input for today's weather
weather = input("Today's weather: ")

# Check the weather and decide accordingly
if weather == "rain":
    print("Bring umbrella")
elif weather == "sunny":
    print("Just come")
else:
    print("Just come")
```

### Explanation
- The `input()` function is used to get user input.
- The `==` operator is used to compare the input with different conditions.
- Based on the condition, the appropriate message is printed.

## Summary
In this lecture, we learned about conditional statements in Python, specifically `if`, `elif`, and `else`. We saw how these statements allow us to make decisions based on user inputs. The key concept is to use conditions to determine which block of code should be executed. We covered the syntax and provided examples to illustrate how to implement these statements effectively.

By understanding and utilizing conditional statements, we can create more dynamic and interactive programs that respond to various user inputs.

---

*Figures are reconstructed whiteboards. Each is assembled from tiles taken from moments when the lecturer was not standing in front of that part of the board, so every pixel is unmodified video; nothing is generated. A figure shows the board's state across the time range given, not a single instant. Boards less than 95% clear of the lecturer were left out.*
