# Conditional Statements and Decision Making in Python

In this lecture, we will learn how to use conditional statements in Python to make decisions based on user input.

## Key takeaways
- Understand how to use `if`, `elif`, and `else` statements.
- Learn to use user input to make decisions.
- Recognize the importance of matching strings correctly.

## Conditional Statements and Decision Making
Conditional statements allow the program to make decisions based on certain conditions. We will use `if`, `elif`, and `else` to create these decisions.

### Example: Bringing an Umbrella Based on Weather
If the weather is rainy, the user will bring an umbrella. Otherwise, they will not need one.

```python
weather = input("Today's weather: ")
if weather == "rain":
    print("Bring Umbrella")
else:
    print("Don't bring umbrella")
```

![Board 0:00-5:50](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–5:50, reconstructed from 11 video frames with the lecturer removed; 100% of the board is unobstructed.*

### Watch out:
- Ensure the string matches exactly, including case sensitivity.
- Use `==` for comparison, not `=` which is for assignment.

### Example: Handling Multiple Conditions
We can extend the decision-making process to handle multiple conditions using `elif`.

```python
weather = input("Today's weather: ")
if weather == "rain":
    print("Bring Umbrella")
elif weather == "sunny":
    print("Just Come")
else:
    print("Don't bring umbrella")
```

### Example: Additional Conditions
Let's add more conditions to handle different scenarios.

```python
weather = input("Today's weather: ")
if weather == "rain":
    print("Bring Umbrella")
elif weather == "sunny":
    print("Just Come")
elif weather == "cloudy":
    print("Wear White Coat")
else:
    print("Don't bring umbrella")
```


## Check yourself
1. Write a Python program to check if the user input is "rain". If true, print "Bring Umbrella".
2. Write a Python program to check if the user input is "sunny". If true, print "Just Come".
3. Write a Python program to check if the user input is "cloudy". If true, print "Wear White Coat".

### Answers
1. ```python
   weather = input("Today's weather: ")
   if weather == "rain":
       print("Bring Umbrella")
   ```
2. ```python
   weather = input("Today's weather: ")
   if weather == "sunny":
       print("Just Come")
   ```
3. ```python
   weather = input("Today's weather: ")
   if weather == "cloudy":
       print("Wear White Coat")
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*