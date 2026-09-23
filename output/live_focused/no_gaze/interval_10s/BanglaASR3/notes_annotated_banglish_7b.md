# Conditional Statements
Conditional statements allow the computer to make decisions based on user input.

## Key takeaways
- The `if` statement initiates a conditional check.
- The `elif` statement provides an alternative condition.
- The `else` statement handles the default case.
- User input is taken to determine the condition.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 -->
## Conditional Statements
**Ek line e:** Conditional statements allow the computer to make decisions based on user input.

![Board 1: 0:00-5:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Handwritten Note · 3 Code · 4 Code · 5 Handwritten Note · 6 Code · 7 Code


**Red Box 1 (Conditional Statements):**
The title clearly states that we are dealing with conditional statements, which enable the computer to make decisions.

**Blue Box 2 (Handwritten Note):**
The note "Rain user will bring Umbrella" illustrates a simple condition where the user brings an umbrella if it rains.

**Orange Box 3 (Code):**
```python
if
```
This keyword initiates a conditional statement.

**Green Box 4 (Code):**
```python
weather == "Rain": print("Bring Umbrella")
```
Here, the computer checks if the weather is "Rain" and prints "Bring Umbrella" if true.

**Purple Box 5 (Handwritten Note):**
The note "If not doesn't bring umbrella" explains what happens if the condition is not met.

**Pink Box 6 (Code):**
```python
elif weather == "Sunny": print("Wear White Coat")
```
This is an additional condition that checks if the weather is "Sunny" and prints "Wear White Coat" if true.

**Brown Box 7 (Code):**
```python
else: print("Just Come")
```
This is the default condition that executes if none of the previous conditions are met, printing "Just Come".

**Mone rakho:** In the code, we first declare a variable `weather` by taking input from the user. We then use an `if` statement to check if the weather is "Rain". If it is, the computer prints "Bring Umbrella". If not, it checks the next condition using `elif` to see if the weather is "Sunny". If neither condition is met, the `else` block is executed, printing "Just Come".

> Lecturer: "so, if-rain, aa user will bring umbrella. okay?"

The `if` statement checks if the weather is "Rain" and prints "Bring Umbrella" if true. If the weather is not "Rain", the `elif` statement checks if the weather is "Sunny" and prints "Wear White Coat" if true. If both conditions fail, the `else` block prints "Just Come".

**Mone rakho:** The complete code looks like this:
```python
weather = input("Today's weather:")
if weather == "Rain":
    print("Bring Umbrella")
elif weather == "Sunny":
    print("Wear White Coat")
else:
    print("Just Come")
```

---

## Check yourself
1. What keyword initiates a conditional statement?
2. What does the `elif` statement do?
3. What does the `else` statement handle?
4. How is user input used in the code?
5. What will the program print if the weather is neither "Rain" nor "Sunny"?

### Answers
1. The keyword that initiates a conditional statement is `if`.
2. The `elif` statement provides an alternative condition to check if the initial condition is not met.
3. The `else` statement handles the default case when none of the previous conditions are met.
4. User input is used to assign a value to the `weather` variable.
5. If the weather is neither "Rain" nor "Sunny", the program will print "Just Come".

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 0.*
