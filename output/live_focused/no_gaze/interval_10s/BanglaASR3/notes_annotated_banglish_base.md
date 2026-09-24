# Conditional Statements
Conditional statements are used to make decisions in a program based on certain conditions.

## Key takeaways
- Conditional statements allow programs to make decisions based on conditions.
- The `if` keyword starts a conditional statement that checks a condition and executes the code inside the block if the condition is true.
- The `elif` keyword is used to check another condition if the previous `if` condition is false.
- The `else` keyword provides a default action if none of the previous conditions are met.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 -->
## Conditional Statements
**Ek line e:** Conditional statements are used to make decisions in a program based on certain conditions.

![Board 1: 0:00-5:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Handwritten Note · 3 Code · 4 Code · 5 Handwritten Note · 6 Code · 7 Code


1. **Box 1 (red):** The title "Conditional Statements" introduces us to the concept of making decisions in programming.
2. **Box 2 (blue):** The handwritten note "Rain user will bring Umbrella" provides an example of a condition where the user brings an umbrella if it rains.
3. **Box 3 (orange):** The `if` keyword is used to start a conditional statement. It checks a condition and executes the code inside the block if the condition is true.
4. **Box 4 (green):** The code snippet `if weather == "Rain": print("Bring Umbrella")` demonstrates how to use the `if` statement to print a message when the weather is rainy.
5. **Box 5 (purple):** The handwritten note "If not doesn't bring umbrella" explains what happens if the condition is false.
6. **Box 6 (pink):** The `elif` keyword is used to check another condition if the previous `if` condition is false. Here, `elif weather == "Sunny": print("Wear White Coat")` prints a message when the weather is sunny.
7. **Box 7 (brown):** The `else` keyword is used to provide a default action if none of the previous conditions are met. The code `else: print("Just Come")` prints a message when the weather is neither rainy nor sunny.

The full code looks like this:

```python
weather = input("Today's weather:")
if weather == "Rain":
    print("Bring Umbrella")
elif weather == "Sunny":
    print("Wear White Coat")
else:
    print("Just Come")
```

> Lecturer: "if rain user will bring umbrella okay so arectogenes j if not"

In this example, the program asks the user for the current weather. If the weather is rainy, it prints "Bring Umbrella". If the weather is sunny, it prints "Wear White Coat". If the weather is neither rainy nor sunny, it prints "Just Come".

### Extra jana kotha (lecture e bola hoy ni)
Understanding conditional statements is crucial because they allow programs to make decisions based on different conditions. This helps in creating more dynamic and interactive applications. For instance, in a weather app, these statements can determine what advice to give the user based on the current weather conditions.

---

## Check yourself
1. What keyword is used to start a conditional statement?
2. What does the `elif` keyword do?
3. What does the `else` keyword do?
4. Write a simple conditional statement that prints "Bring Umbrella" if the weather is rainy.
5. Explain the difference between `if`, `elif`, and `else`.

### Answers
1. The keyword used to start a conditional statement is `if`.
2. The `elif` keyword is used to check another condition if the previous `if` condition is false.
3. The `else` keyword provides a default action if none of the previous conditions are met.
4. ```python
   if weather == "Rain":
       print("Bring Umbrella")
   ```
5. `if` checks a condition and executes the code inside the block if the condition is true. `elif` checks another condition if the first condition is false. `else` provides a default action if none of the previous conditions are met.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 0.*
