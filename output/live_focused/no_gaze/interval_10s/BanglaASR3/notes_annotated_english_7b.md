# Conditional Statements
This lecture explains how to use `if`, `elif`, and `else` statements to make decisions based on user input.

## Key takeaways
- Understand the structure and usage of `if`, `elif`, and `else` statements.
- Learn how to handle multiple conditions using `elif`.
- Recognize the importance of indentation in Python code.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 -->
## Conditional Statements
**In one line:** This board explains how to use `if`, `elif`, and `else` statements to make decisions based on user input.

![Board 1: 0:00-5:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Handwritten Note · 3 Code · 4 Code · 5 Handwritten Note · 6 Code · 7 Code


1. **Understanding Conditional Statements**: The board starts with the title "Conditional Statements," which introduces the concept of making decisions in a program based on certain conditions. The lecturer explains that these statements allow the computer to perform different actions depending on the input provided by the user.

2. **Example with Rain and Umbrella**: In Box 2 (blue), the lecturer writes "Rain user will bring Umbrella." This is an example of a simple conditional statement where the program checks if it is raining and instructs the user to bring an umbrella. The code in Box 3 (orange) and Box 4 (green) demonstrates this logic:
    ```python
    if weather == "Rain":
        print("Bring Umbrella")
    ```
    The lecturer explains that if the weather is rain, the program will print "Bring Umbrella."

3. **Handling Other Conditions**: In Box 5 (purple), the lecturer writes "If not doesn't bring umbrella." This indicates that if the condition for bringing an umbrella is not met, the program will handle other cases. The code in Box 6 (pink) and Box 7 (brown) show how to handle sunny weather and other conditions:
    ```python
    elif weather == "Sunny":
        print("Wear White Coat")
    else:
        print("Just Come")
    ```
    The lecturer explains that if the weather is not rain, the program will check if it is sunny and print "Wear White Coat." If neither condition is met, the program will print "Just Come."

4. **Complete Example**: The full code on the board is:
    ```python
    weather = input("Today's weather:")
    if weather == "Rain":
        print("Bring Umbrella")
    elif weather == "Sunny":
        print("Wear White Coat")
    else:
        print("Just Come")
    ```

5. **Explanation of the Code**: The lecturer explains that the program first asks the user for the current weather using `input("Today's weather:")`. It then checks if the weather is rain. If it is, the program prints "Bring Umbrella." If the weather is not rain, it checks if it is sunny and prints "Wear White Coat." If neither condition is met, it prints "Just Come."

> The lecturer said: "so, if-rain, aa user will bring umbrella. okay? so, arekta jinis je if not, if-ta jinis je if-ta jabe aat kore kore kore kore kore"

**Remember:** The key point is that conditional statements (`if`, `elif`, and `else`) allow the program to make decisions based on user input, performing different actions depending on the conditions met.

---

## Check yourself
1. What does the `if` statement do in a conditional statement?
2. How does the `elif` statement work in relation to the `if` statement?
3. What happens if none of the conditions in an `if`, `elif`, and `else` block are met?

### Answers
1. The `if` statement checks a condition and executes the code inside it if the condition is true.
2. The `elif` statement is used to check additional conditions if the initial `if` condition is false.
3. If none of the conditions are met, the code inside the `else` block is executed.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
