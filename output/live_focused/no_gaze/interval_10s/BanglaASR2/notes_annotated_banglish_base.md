# Input and Type Casting
Ek line e: Today, we will learn about input and type casting in Python.

## Key takeaways
- Input function always returns a string.
- Type casting is necessary for performing arithmetic operations on user inputs.
- `int()` and `float()` functions are used for type casting.
- User inputs should be converted to appropriate data types before performing operations.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Today, we will learn about input and type casting in Python.

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Red Box 1 (Title):** Input and Type Casting
- **Blue Box 2 (Code):** `age = 92 input()`

The lecturer started by reminding us that in the previous class, we learned about variables and their data types. Today, we will focus on an important concept called input and type casting.

### Explanation
1. **Understanding Variables:** The lecturer explained that a variable, like `age`, can be assigned a specific value, such as `92`. However, in real-life scenarios, we often need to get input from the user rather than hardcoding the value.
2. **Introduction to the Input Function:** The lecturer introduced the `input()` function, which is a built-in Python function used to take input from the user. It is important to note that the `input()` function always returns a string, regardless of the input provided by the user.
3. **Example Usage:** To demonstrate, the lecturer wrote the following code on the board:
   ```python
   age = 92 input()
   ```
   Here, `age` is initially set to `92`, but the `input()` function will prompt the user to enter a value, which will be stored as a string.

### Quotes
> Lecturer: "So, in this built-in function, we don't have the input."

### Extra jana kotha
When using the `input()` function, it is crucial to understand that the input is always treated as a string. If you need to perform operations that require numerical values, you will need to convert the string to an integer or float using type casting functions like `int()` or `float()`. For example:
```python
age = int(input("Enter your age: "))
```
This ensures that the input is correctly interpreted as a number, allowing you to perform arithmetic operations.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input function and type casting are fundamental concepts in programming.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Red Box 1 (Input and Type Casting):**
   - The red box introduces the concept of input and type casting. The lecturer explains that the `input()` function is used to get input from the user. The user will see a message asking for their name, and the name entered will be stored as a string.

2. **Blue Box 2 (Code):**
   - The blue box shows the actual code: `name = input("What is your name?")`. Here, the user is prompted to enter their name, and the name is stored in the variable `name`.

3. **Board:**
   - The board also includes an example of printing the name: `print("Hello", name)`. The lecturer explains that when the user runs this code, they will be asked to enter their name, and the program will print "Hello" followed by the name entered.

**Quotes:**

### Extra jana kotha
When using the `input()` function, it's important to remember that whatever the user types is stored as a string. If you need to perform operations that require numerical values, you will need to convert the string to an integer or float using type casting functions like `int()` or `float()`. This ensures that the data is in the correct format for further processing in your program.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** Input and type casting are essential for handling user inputs in programming.

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


- **Red Box 1 (Title):** Input and Type Casting
- **Blue Box 2 (Question):** the first number? the second number?
- **Orange Box 3 (Code):** 
  ```python
  num1 = input("What is the first number?")
  num2 = input("What is the second number?")
  sum = num1 + num2
  print(sum)
  ```
- **Purple Box 5 (String):** "10" String
- **Pink Box 6 (String):** "20" String
- **Green Box 4 (String):** " " String

**Explanation:**
The lecturer starts by explaining that initially, there are no variables defined for numbers. He then introduces the `input` function to get user input. In the blue box, he asks the user for the first and second numbers. The orange box shows the code where `num1` and `num2` are assigned the user's input using the `input` function. The user's input is treated as a string by default, as shown in the purple and green boxes ("10" and "20" respectively).

The lecturer then demonstrates what happens when the user inputs "10" and "20". He explains that the sum is calculated as a string concatenation rather than an arithmetic operation because both `num1` and `num2` are strings. To fix this, the numbers need to be converted to integers before performing the addition. However, for the current demonstration, he keeps the numbers as strings to show the importance of type casting.

**Quotes:**
> Lecturer: "So, if you say that 10, you will be used to be used to"

**Extra jana kotha:**
When dealing with user inputs, it's crucial to understand that the `input` function always returns a string. Therefore, if you need to perform arithmetic operations, you must convert the string to an integer using functions like `int()`. This ensures that the operations are performed correctly. Always remember to check the data types of your variables to avoid unexpected results.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** In this section, we learn about input and type casting.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


1. **Red Box 1 (Input and Type Casting):** This title introduces the topic of input and type casting.
2. **Blue Box 2 (Question):** The lecturer asks, "What is the first number?" and "What is the second number?" These questions guide us to understand how to take user inputs.
3. **Orange Box 3 (Code):** The code snippet provided is:
   ```python
   num1 = input("What is the first number?")
   num2 = input("What is the second number?")
   ```
   Here, `input()` function takes user input as a string.
4. **Green Box 4 (Variable):** The variable `num` is assigned the integer value of `num1` using the `int()` function:
   ```python
   num = int(num1)
   ```
   This converts the string `num1` into an integer.
5. **Purple Box 5 (Conversion):** The conversion process is shown as:
   ```plaintext
   "10" String -> integer
   ```
   This demonstrates that the string `"10"` is converted to the integer `10`.
6. **Pink Box 6 (Function):** The `int()` function is used to convert a string to an integer.

**Quotes:**
> Lecturer: "num1 so basically what happens i am user input num1 so that string is now int of num1 is now the string is now integer"

The `int()` function is crucial because it allows us to perform arithmetic operations on user inputs, which are initially received as strings. Without converting these strings to integers, we cannot add or subtract them.

### Extra jana kotha (lecture e bola hoy ni)
Understanding type casting is essential for performing mathematical operations on user inputs. For example, if you want to add two numbers entered by the user, you need to convert their string inputs to integers first. This ensures that the operations are performed correctly.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**Ek line e:** Input and typecasting are essential for handling user inputs correctly in Python.

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


1. **Red Box 1**: The title "Input and Type Casting" is clearly stated.
2. **Orange Box 3**: The code initializes `num1` and `num2` with integer values: `num1 = 20` and `num2 = 30`.
3. **Orange Box 4**: The sum of these two numbers is calculated and printed: `The Sum of 20 and 30 is 50`.
4. **Orange Box 5**: The code then uses `input()` to get user input for `num1` and `num2`, which are initially strings.
5. **Orange Box 6**: To perform arithmetic operations, typecasting is necessary. The code converts the string inputs to integers using `int(num1)` and `int(num2)`.
6. **Orange Box 7**: The sum is calculated and stored in the variable `sum`: `sum = num1 + num2`.
7. **Orange Box 8**: Finally, the result is printed using both methods: `print("Result is", sum)` and `print(f"The sum of {num1} and {num2} is {sum}")`.

> Lecturer: "So, this is typecasting. I have forcefully typecast change, but I have to say that I don't have string value, so I can give the integer the first thing."

### Extra jana kotha
In Python, when you take input from the user, it is always treated as a string. Therefore, if you want to perform arithmetic operations, you need to convert the string to an integer using the `int()` function. This ensures that the operations are performed correctly. For example, if you input "20" and "30", without typecasting, you would get an error because you cannot add strings directly. By using `int()`, you can convert these strings into integers and then perform addition.

---

## Check yourself
1. What does the `input()` function return?
2. Why is type casting necessary when working with user inputs?
3. How do you convert a string to an integer in Python?
4. What will happen if you try to add two strings using the `+` operator?
5. Can you provide an example of using the `int()` function in a Python program?

### Answers
1. The `input()` function returns a string.
2. Type casting is necessary because the `input()` function always returns a string, and arithmetic operations require numerical values.
3. You convert a string to an integer using the `int()` function.
4. If you try to add two strings using the `+` operator, it will concatenate the strings instead of performing arithmetic addition.
5. Example: `num = int(input("Enter a number: "))`

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 1 removed. References to boxes that do not exist: 6.*
