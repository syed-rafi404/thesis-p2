# Input and Type Casting
In this section, we will learn about input and type casting in Python.

## Key takeaways
- Input function er moddhe user e jonna message dite hobe.
- Type casting is the process of converting one data type to another.
- When using the `input` function, always provide a clear prompt message to the user.
- Use the `int()` function to convert string inputs to integers for arithmetic operations.
- F-strings can be used to format and print output in a more readable manner.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** In this section, we will learn about input and type casting in Python.

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Input and Type Casting (Red Box 1):**
   - The red box titled "Input and Type Casting" introduces a new and interesting topic for today's discussion.
   - The lecturer starts by reminding us of the previous class where we learned about variables and their types. Variables can hold different types of data such as integers, strings, etc.
   - Today, we will focus on an important aspect related to variables: taking user input.

2. **User Input (Blue Box 2):**
   - The blue box contains a piece of code: `age = 92 input()`.
   - The lecturer explains that usually, we assign fixed values to variables, like `age = 42`. However, in real-life scenarios, the value of a variable might change based on user input.
   - To get user input in Python, we use a built-in function called `input()`. This function allows us to take input from the user and store it in a variable.
   - As an example, the lecturer writes the following code: `age = 92 input()`. Here, `92` is a placeholder value, and `input()` is the function that waits for user input.

3. **Explanation of the Code:**
   - When you run the code `age = 92 input()`, the program will display a prompt asking for user input.
   - Whatever the user types and presses Enter, that value will be stored in the variable `age`.
   - For instance, if the user types `25`, the variable `age` will be assigned the value `25`.

> Lecturer: "so shei python er ekta built-in function er eche jeta holo input. so ami jodi likhi function ta, jeta holo input function. jeta holo python er built-in ekta function."

### Extra jana kotha
Understanding how to take user input is crucial because it allows your programs to interact with users dynamically. This is particularly useful in applications where the user needs to provide specific information, such as in forms or games. By using the `input()` function, you can create more interactive and flexible programs.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input function er moddhe user e jonna message dite hobe.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Red Box 1 (Title):** Input and Type Casting
2. **Blue Box 2 (Code):** `name = input("What is your name?")`

The lecturer explained that we are introducing the `input` function, which allows us to get input from the user. Here’s how it works:

- **Step 1:** We start by writing the `input` function. This function takes a string as an argument, which will be displayed to the user as a prompt.
- **Step 2:** In our example, the prompt is `"What is your name?"`. When the program runs, it will display this message to the user, asking them to enter their name.
- **Step 3:** Whatever the user types and presses Enter, that value will be stored in the `name` variable. For instance, if the user types "Rafi" and presses Enter, the variable `name` will hold the value "Rafi".

The lecturer also mentioned that after getting the input, we can use the `print` function to display a greeting along with the user's name. Here’s how it works:

- **Step 4:** We use the `print` function to display a message like "Hello". After that, we concatenate the `name` variable to the message.
- **Step 5:** The lecturer emphasized that we should not put any additional characters inside the `input` function unless we want to include them in the prompt. For example, if we put a comma inside the `input` function, it might cause unexpected behavior during testing.

The lecturer concluded by saying, "So, we have learned how the basic `input` function works."

### Extra jana kotha
When using the `input` function, always make sure to provide a clear prompt message to the user. This helps in getting accurate input and avoids confusion. Also, remember that the `input` function returns a string, so if you need to perform operations that require numbers, you will need to convert the string to an integer or float using type casting functions like `int()` or `float()`.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** Input and type casting are essential for handling user inputs correctly.

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


- **Box 1 (red):** Title: Input and Type Casting
- **Box 2 (blue):** Question: the first number? the second number?
- **Box 3 (orange):** Code: 
  ```python
  num1 = input("What is num2 = input("What sum = num1 + num2 Print(sum)
  ```
- **Box 4 (green):** String: "10" String
- **Box 5 (purple):** String: "20" String
- **Box 6 (pink):** String: String

The lecturer explained that when we take user inputs, they are initially treated as strings. This can cause issues if we need to perform arithmetic operations on them. Let's break down the process:

1. **Box 2 (blue):** The lecturer asked, "the first number? the second number?" This indicates that we need to take two numbers from the user.
2. **Box 3 (orange):** The code snippet shows how to take these inputs. The `input` function is used to get the first number, which is stored in the variable `num1`. Similarly, the second number is stored in `num2`.
3. **Box 4 (green) and Box 5 (purple):** These represent the string values "10" and "20". When we directly add these strings, Python concatenates them instead of performing arithmetic addition.
4. **Box 6 (pink):** This represents an empty string, indicating that we need to convert these string inputs into integers before performing any arithmetic operations.

The lecturer emphasized that while the `input` function returns a string, we often need to treat the input as a number. For example, if we want to add the numbers 10 and 20, we need to ensure they are treated as integers.

> Lecturer: "so keo jodi number ta bole je 10, ashole je pacche sheta ekta string hishabe ashtese ekhane."

To fix this, we need to convert the string inputs into integers using the `int()` function. Here’s how we do it:

```python
sum = num1 + num2
```

However, since `num1` and `num2` are strings, we need to convert them to integers first:

```python
sum = int(num1) + int(num2)
```

This ensures that the addition operation is performed correctly, resulting in the sum of the two numbers.

### Extra jana kotha (lecture e bola hoy ni)
Type casting is crucial when dealing with user inputs in programming. It helps us handle data correctly and avoid common errors like concatenation instead of addition. Always remember to convert string inputs to the appropriate data type before performing arithmetic operations.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** In this section, we will discuss how to take input from the user and convert it into different data types.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


- **Red Box 1 (Input and Type Casting):** This box introduces the concept of taking input from the user and converting it into a specific data type.
  
- **Blue Box 2 (Question):** The lecturer asks, "the first number?" the second number?" This indicates that the user will be prompted to enter two numbers.

- **Orange Box 3 (Code):** The code snippet provided is:
  ```python
  num1 = input("What is num2 = input("What int(num1)
  ```
  Here, `num1` is assigned the value entered by the user using the `input()` function. The value entered by the user is initially a string.

- **Green Box 4 (Variable):** The variable `num` is mentioned, but it is not directly related to the current code snippet. It might be used later in the program.

- **Purple Box 5 (Conversion):** The conversion process is shown here:
  - `"10"` (String) -> `num1` (Integer)
  - When `int(num1)` is called, the string `"10"` is converted into an integer `10`.

- **Pink Box 6 (Function):** The `int()` function is used to convert a string into an integer.

**Explanation:**
The lecturer explains that when you use the `input()` function, the value entered by the user is treated as a string. For example, if the user enters `"10"`, it is stored as a string. To convert this string into an integer, you use the `int()` function. This is demonstrated in the code where `num1` is converted from a string to an integer.

> Lecturer: "so ekhane basically ki hocche? ami user theke input niaychi num1. sheta ki? 10. string e chilo. ami jokhon int of aa num1 kore dicchi, ei string ta hoye jacche ki? amar integer."

In the example, if the user enters `"10"`, it is stored as a string. When you call `int(num1)`, the string `"10"` is converted into the integer `10`.

### Extra jana kotha
When you take input from the user, it is always a string. To use it as a number in your calculations, you need to convert it using functions like `int()`. This ensures that the operations you perform are done on actual numerical values rather than strings.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**Ek line e:** Type casting is the process of converting one data type to another.

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


1. **Box 1 (red):** Input and Type Casting
   - The lecturer explains that we need to convert an input value from one type to another, specifically from a string to an integer. This is called type casting.
   - The lecturer mentions that if we try to add a string to an integer directly, it will result in an error because strings and integers are different data types.

2. **Box 1 (red):** Input and Type Casting
   - The lecturer gives an example where a user inputs a string representing a number. If we try to perform arithmetic operations directly, it will fail.
   - For instance, if the user inputs `first` and we try to add it to a number, it will result in an error.

3. **Box 1 (red):** Input and Type Casting
   - The lecturer demonstrates how to convert a string to an integer using type casting. He shows how to add two integer values and then print their sum.
   - However, when printing the sum, only the final result (an integer) is printed, not the intermediate steps.

4. **Box 1 (red):** Input and Type Casting
   - The lecturer introduces string formatting to print the sum in a more readable format. He explains that we can use the `f-string` feature in Python 3 to achieve this.
   - An `f-string` starts with `f` followed by curly braces `{}` where variables can be placed.

5. **Box 1 (red):** Input and Type Casting
   - The lecturer writes an example of an `f-string`: `print(f"Result is {sum}")`.
   - He explains that within the curly braces, we can place variables like `sum`, which will be replaced by their values when the string is printed.

6. **Box 1 (red):** Input and Type Casting
   - The lecturer provides a practical example: if the sum is 20, the output will be `Result is 20`.
   - He emphasizes that this method makes the output more meaningful and easier to understand.

7. **Box 1 (red):** Input and Type Casting
   - The lecturer concludes by mentioning that in the next class, they will cover arithmetic operations and other operators, including comparison operators.

**Mone rakho:** Type casting, f-string, string formatting, input, output, integer, string, error, meaningful output.

---

## Check yourself
1. What is the purpose of the `input` function in Python?
2. Why is it important to convert string inputs to integers before performing arithmetic operations?
3. How do you convert a string to an integer in Python?
4. What is an f-string and how is it used in Python?
5. What happens if you try to add a string and an integer directly?

### Answers
1. The purpose of the `input` function in Python is to get user input from the console.
2. It is important to convert string inputs to integers before performing arithmetic operations because strings and integers are different data types, and direct addition will result in an error.
3. You convert a string to an integer in Python using the `int()` function.
4. An f-string is a formatted string literal in Python that allows you to embed expressions inside string literals, using curly braces `{}`. For example, `print(f"Result is {sum}")`.
5. If you try to add a string and an integer directly, it will result in a TypeError.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
