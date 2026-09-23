# Conditional Statements
We learn how to use `if`, `elif`, and `else` statements to make decisions based on user input.

## Key takeaways
- Understand the structure and usage of `if`, `elif`, and `else` statements.
- Learn how to use these statements to make decisions based on user input.
- Recognize the importance of handling different conditions using `elif` and `else`.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 -->
## Conditional Statements
**In one line:** We learn how to use `if`, `elif`, and `else` statements to make decisions based on user input.

![Board 1: 0:00-5:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Handwritten Note · 3 Code · 4 Code · 5 Handwritten Note · 6 Code · 7 Code


1. **Conditional Statements**
2. **Handwritten Note: Rain user will bring Umbrella**
3. **Code: if**
4. **Code: weather == "Rain": print("Bring Umbrella")**
5. **Handwritten Note: If not doesn't bring umbrella**
6. **Code: elif weather == "Sunny": print("Wear White Coat")**
7. **Code: else: print("Just Come")**

The lecturer explains that in this video, we will see how a computer makes logical decisions based on user input. Specifically, we will learn how to use `if`, `elif`, and `else` statements to decide what action to take based on different conditions.

### Explanation
1. **Variable Declaration**: First, we declare a variable to store the user's input. For example, `weather = input("Today's weather:")`. This line prompts the user to enter the current weather.
   
2. **If Statement**: Next, we use an `if` statement to check if the weather is "Rain". If it is, the program prints "Bring Umbrella". The code in Box 3 (orange) shows this: `if weather == "Rain": print("Bring Umbrella")`.

3. **Else Statement**: If the weather is not "Rain", the program moves to the `else` block, which prints "Just Come". This ensures that if the weather is neither "Rain" nor "Sunny", the user is told to just come without any special instructions.

4. **Elif Statement**: To handle other weather conditions, such as "Sunny", we use an `elif` statement. In Box 6 (pink), the code is `elif weather == "Sunny": print("Wear White Coat")`. This checks if the weather is "Sunny" and prints the appropriate message.

5. **Handwritten Notes**: The handwritten notes in Boxes 2 (blue) and 5 (purple) provide additional context. Box 2 states "Rain user will bring Umbrella", and Box 5 states "If not doesn't bring umbrella". These notes help clarify the logic behind the conditional statements.

**Quote:**
> "so, if-rain, aa user will bring umbrella. okay?"  
> (In English: "if it's rain, the user will bring an umbrella. okay?")

**Remember:** The key point is that we use `if`, `elif`, and `else` statements to make decisions based on user input, ensuring the program takes the correct action depending on the condition.

---

## Check yourself
1. What does the `if` statement do in the provided code?
2. What happens if the weather is not "Rain" but "Sunny"?
3. What is the purpose of the `else` statement in the code?
4. How does the `elif` statement differ from the `else` statement?
5. What would happen if the user inputs a weather condition other than "Rain" or "Sunny"?

### Answers
1. The `if` statement checks if the weather is "Rain" and prints "Bring Umbrella" if true.
2. If the weather is "Sunny", the program prints "Wear White Coat".
3. The `else` statement provides a default action if none of the previous conditions are met.
4. The `elif` statement checks additional conditions after the `if` statement, while the `else` statement is used as a catch-all.
5. If the user inputs a weather condition other than "Rain" or "Sunny", the program will print "Just Come".

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 0.*
