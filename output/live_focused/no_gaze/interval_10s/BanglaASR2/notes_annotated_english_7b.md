# Input and Type Casting
This lecture covers how to take user input in Python and explains type casting.

## Key takeaways
- Understand how to use the `input()` function to get user input.
- Learn how to handle user inputs and perform type casting for arithmetic operations.
- Know the importance of converting string inputs to integers before performing arithmetic operations.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**In one line:** This board introduces how to take user input in Python and explains type casting.

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


### Box 1 (red): Title: Input and Type Casting
The board starts with the title "Input and Type Casting," indicating the topic of the discussion.

### Box 2 (blue): Code: age = 92 input()
The code snippet `age = 92 input()` demonstrates how to take user input in Python. Here, `age` is initially set to 92, but the `input()` function is intended to get user input after this initial assignment.

**Explanation:**
1. **Introduction to Variables:** The lecturer begins by reminding students about variables and their importance. They explain that while we can assign fixed values to variables, in real-life scenarios, these values might change based on user input.
2. **User Input in Python:** The lecturer introduces the `input()` function, which is a built-in function in Python that allows the program to take input from the user. The lecturer emphasizes that using `input()` enables dynamic interaction with the user.
3. **Example Usage:** To illustrate the usage of the `input()` function, the lecturer writes `age = 92 input()`. However, there seems to be a typo in the code where `92 input()` should be `92, input()`. The correct way to use `input()` is to separate the number and the function with a comma, like `age = 92, input()`. This would first assign 92 to `age` and then prompt the user to enter a value, which will be stored in `age`.

> The lecturer said: "so shei python er ekta built-in function er eche jeta holo input. so ami jodi likhi function ta, jeta holo input function. jeta holo python er built-in ekta function. so ei built-in function er maddome amra user e theke input naya thakeu."
This translates to: "so this is a built-in function in Python called input. So when we write this function, it's the input function. It's a built-in function in Python. Using this built-in function, we can take input from the user."

### Background
Type casting in Python involves converting data from one type to another. For example, converting a string to an integer or vice versa. Understanding how to take user input and handle different types of data is crucial for building interactive applications. The `input()` function returns a string, so if you need to perform arithmetic operations, you must convert the input to an appropriate numeric type using functions like `int()` or `float()`.

**Remember:** The key point is to understand how to use the `input()` function to take user input and handle it appropriately in your Python programs.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**In one line:** This section explains how to use the `input` function to get user input and store it in a variable.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Understanding the `input` Function:**
   - Look at the blue box 2, which shows the code `name = input("What is your name?")`. Here, we are using the `input` function to get input from the user. The function displays a message to the user asking for their name.
   - The message inside the `input` function is `"What is your name?"`. When the program runs, the user will see this message and can enter their name.
   - After the user enters their name and presses Enter, the value entered by the user is stored in the variable `name`.

2. **Using the `print` Function:**
   - Now, let's look at the last line of the board, which shows `print("Hello", name)`. This line uses the `print` function to display a greeting along with the user's name.
   - The `print` function is a built-in Python function that outputs the specified message to the console. In this case, it prints "Hello" followed by the value stored in the `name` variable.

3. **Putting It All Together:**
   - When the program runs, the user will be prompted to enter their name. For example, if the user types "Rafi" and presses Enter, the variable `name` will store the value "Rafi".
   - Then, the `print` function will output "Hello Rafi" to the console.

> The lecturer said: "we are using the `input` function to get input from the user and store it in a variable."

**Remember:** The `input` function allows you to get user input, and the `print` function is used to display messages or values to the user.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**In one line:** This section explains how to handle user inputs and perform type casting in Python to ensure correct arithmetic operations.

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


1. **Understanding the Code Structure (Box 1 - Red):**
   The board starts with a title "Input and Type Casting," indicating the topic of the lecture. The code snippet provided demonstrates how to take user inputs and perform an addition operation.

2. **Taking User Inputs (Box 2 - Blue):**
   The lecturer asks, "The first number? the second number?" This indicates that the program will prompt the user to enter two numbers. The code uses the `input()` function to get these values, storing them in variables `num1` and `num2`.

3. **Adding the Numbers (Box 3 - Orange):**
   The code snippet shows:
   ```python
   num1 = input("What is the first number?")
   num2 = input("What is the second number?")
   sum = num1 + num2
   print(sum)
   ```
   Here, the lecturer explains that the program adds the two numbers directly using the `+` operator. However, since both `num1` and `num2` are strings by default, the result will be a concatenated string rather than a numerical sum.

4. **Example of Concatenation (Box 4 - Green and Box 5 - Purple):**
   The lecturer provides an example where `num1` is `"10"` and `num2` is `"20"`. When added together, the output will be `"1020"` instead of `30`, demonstrating the issue with direct string concatenation.

5. **Type Casting (Box 6 - Pink):**
   To fix this, the lecturer suggests converting the string inputs to integers before performing the addition. The correct way to do this is:
   ```python
   sum = int(num1) + int(num2)
   ```
   By using the `int()` function, the program ensures that the inputs are treated as integers, allowing for proper arithmetic operations.

> The lecturer said: "Your English translation of what the lecturer said" means that the program will add the numbers correctly if we convert the string inputs to integers.

### Background (not said in the lecture)
Type casting is essential in programming when you need to change the data type of a variable. In this case, converting string inputs to integers allows for accurate arithmetic operations. Understanding type casting is crucial for handling user inputs and ensuring that operations like addition work as expected.

**Remember:** Always convert string inputs to the appropriate data type (like integers) before performing arithmetic operations to avoid concatenation instead of addition.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**In one line:** This section explains how to take user inputs and convert them into integers for arithmetic operations.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


1. **Input and Type Casting (Box 1, Red):**
   - The board starts with a title, "Input and Type Casting," which introduces the concept of taking user inputs and converting them into different data types.

2. **Question (Box 2, Blue):**
   - The lecturer asks, "the first number?" and "the second number?" These questions represent the prompts given to the user when taking inputs.

3. **Code (Box 3, Orange):**
   - The code snippet provided is:
     ```python
     num1 = input("What is the first number?")
     num2 = input("What is the second number?")
     ```
   - Here, `num1` and `num2` are variables that store the user's input. The `input()` function takes a string prompt and returns the user's input as a string.

4. **Variable (Box 4, Green):**
   - The variable `num` is introduced, which will hold the converted integer value of `num1`.

5. **Conversion (Box 5, Purple):**
   - The conversion process is shown with the example `"10" String`. When the `int()` function is applied to `num1`, it converts the string `"10"` into an integer `10`.

6. **Function (Box 6, Pink):**
   - The `int()` function is highlighted, showing how it converts a string into an integer. For instance, `int("10")` results in the integer `10`.

> The lecturer said: "so ekhane basically ki hocche? ami user theke input niaychi num1. sheta ki? 10. string e chilo. ami jokhon int of aa num1 kore dicchi, ei string ta hoye jacche ki? amar integer." 
   - In English, this translates to: "Here, basically, I am taking input from the user for `num1`. It is `10` as a string. When I apply the `int()` function to `num1`, this string becomes an integer."

### Background (not said in the lecture)
Type casting is essential in programming to ensure that operations are performed correctly. Converting user inputs from strings to integers allows for arithmetic operations like addition, subtraction, etc., to be carried out without errors.

**Remember:** The key point is to understand how to convert string inputs into integers using the `int()` function for performing arithmetic operations.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**In one line:** This section explains how to handle user inputs and perform type casting in Python.

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


1. **Input and Type Casting**: The board starts with a title indicating the topic of discussion.
2. **Assigning Values**: The lecturer assigns `num1` and `num2` with integer values (`20` and `30`) respectively.
3. **Sum Calculation**: The sum of `20` and `30` is calculated and printed as `50`.
4. **User Input**: The lecturer demonstrates how to take user input using the `input()` function, which returns a string.
5. **Type Casting**: To perform arithmetic operations, the values need to be converted from strings to integers using `int()`.
6. **Sum Calculation with User Input**: The sum of the user-provided numbers is calculated and printed.
7. **String Formatting**: The lecturer explains how to format the output string using f-strings in Python 3.

> The lecturer said: "Your English translation of what the lecturer said" means that when we take user input, it comes as a string, and we need to convert it to an integer to perform arithmetic operations.

### Background
When dealing with user inputs in Python, the `input()` function always returns a string. Therefore, if you want to perform arithmetic operations, you need to convert these string values into integers using the `int()` function. This process is called type casting. F-strings provide a convenient way to format strings and include variables within them, making the output more readable and meaningful.

**Remember:** Always convert user inputs to the appropriate data type before performing arithmetic operations to avoid errors.

---

## Check yourself
1. What does the `input()` function do in Python?
2. How can you convert a string to an integer in Python?
3. Why is it important to convert user inputs to integers before performing arithmetic operations?
4. What will happen if you try to add two strings using the `+` operator in Python?
5. How can you format the output string to include a variable using f-strings?

### Answers
1. The `input()` function in Python is used to get input from the user and returns the input as a string.
2. You can convert a string to an integer in Python using the `int()` function, like `int(string_value)`.
3. It is important to convert user inputs to integers before performing arithmetic operations because the `+` operator performs string concatenation if both operands are strings, leading to incorrect results.
4. If you try to add two strings using the `+` operator in Python, it will concatenate the strings instead of performing arithmetic addition.
5. You can format the output string to include a variable using f-strings by prefixing the string with `f` and enclosing the variable in curly braces, like `f"Hello {variable}"`.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (5 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
