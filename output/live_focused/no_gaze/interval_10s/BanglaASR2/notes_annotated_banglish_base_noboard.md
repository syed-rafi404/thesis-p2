# Input and Type Casting
Today, we will learn about input and type casting in Python.

## Key takeaways
- The `input()` function is used to get user input in Python.
- By default, the `input()` function returns a string.
- We need to use type casting functions like `int()`, `float()`, etc., to convert strings to other data types for arithmetic operations.
- Type casting is essential for manipulating data types in programming.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Today, we will learn about input and type casting in Python.

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Box 1 (red):** Title: Input and Type Casting
- **Box 2 (blue):** Code: `age = 92 input()`

The lecturer started by reminding us that in the previous class, we learned about variables and their data types. Today, we will focus on an important topic: input and type casting.

> Lecturer: "So, normally, what is the variable? We were given the variable, and the age."

The lecturer explained that previously, we had a variable named `age` with a fixed value of 42. However, in real-life scenarios, we often need to take user input. For this purpose, Python provides a built-in function called `input()`.

> Lecturer: "This is Python built-in function that is input. So, I have the link function that is input function. So, this is Python built-in function."

The `input()` function allows us to get input from the user. It returns the input as a string by default. Let's see an example:

```python
age = 92 input()
```

Here, the lecturer demonstrated how to use the `input()` function. However, the code snippet provided is incomplete. The correct usage would be:

```python
age = int(input("Enter your age: "))
```

In this corrected version, the `input()` function is used to get user input, which is then converted to an integer using the `int()` function. This is necessary because the `input()` function returns a string, and if we want to perform arithmetic operations with the input, we need to convert it to an integer.

### Extra jana kotha (lecture e bola hoy ni)
To ensure that the input is treated as a number, we use the `int()` function. For example, if you want to calculate the age in years, you might need to convert the input to an integer before performing any calculations. This is crucial for maintaining the integrity of your program and ensuring that it works correctly with numerical data.

**Mone rakho:** The `input()` function returns a string, and we need to use `int()` or other type conversion functions to work with numerical data.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input function is used to get user input in Python.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


- **Red Box 1 (Input and Type Casting):** This box introduces the concept of input and type casting in Python. The lecturer explains that the `input` function is used to take input from the user. The user will see a message asking for their name, and they will enter their name.

- **Blue Box 2 (Code):** The lecturer writes the following code on the board:
  ```python
  name = input("What is your name?")
  ```
  - The `input` function is called with a string argument `"What is your name?"`. This message is displayed to the user when the program runs.
  - The user's input is stored in the variable `name`.

- **Explanation:** The lecturer then demonstrates how to use the `print` function to display the user's name. They write:
  ```python
  print("Hello", name)
  ```
  - The `print` function is a built-in function in Python that outputs the specified message to the console.
  - The value entered by the user is stored in the variable `name`, and the `print` function uses this variable to greet the user.

- **Quote:** 

- **Extra jana kotha:** When using the `input` function, it always returns a string. Therefore, if you need to perform operations that require a different data type (like integers or floats), you will need to convert the input using type casting functions like `int()`, `float()`, etc. For example, if you want to add the user's age to 10, you would need to cast the input to an integer first.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** Input and type casting are fundamental concepts in programming.

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

The lecturer explained that we need to take input from the user to perform operations. Let's break down the process:

1. **Box 2 (blue):** The lecturer asked, "the first number?" and "the second number?" This indicates that we need to get two numbers from the user.
2. **Box 3 (orange):** The code snippet provided is incomplete. It should be:
   ```python
   num1 = input("What is the first number? ")
   num2 = input("What is the second number? ")
   sum = num1 + num2
   print(sum)
   ```
3. **Box 4 (green) and Box 5 (purple):** The lecturer demonstrated using the strings "10" and "20". When these are inputted, the program will concatenate them rather than add them because the default input type is a string.
4. **Box 6 (pink):** The lecturer mentioned that we need to convert these strings to integers to perform arithmetic operations. He stated, "So, by default always string will be used. So, if you say that 10, you will be used to be used to."

To fix this, we need to explicitly convert the input to integers:
```python
num1 = int(input("What is the first number? "))
num2 = int(input("What is the second number? "))
sum = num1 + num2
print(sum)
```

The lecturer emphasized the importance of understanding type casting. He quoted, "So, by default always string will be used. So, if you say that 10, you will be used to be used to." This highlights the need to convert strings to integers when performing arithmetic operations.

### Extra jana kotha (lecture e bola hoy ni)
Type casting is crucial in programming to ensure that variables are treated as the correct data type. For example, converting strings to integers allows us to perform mathematical operations. Always remember to check the data types of your variables before performing operations to avoid errors.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** In this section, we will discuss how to convert user inputs into integers.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


- **Box 1 (red):** Input and Type Casting
- **Box 2 (blue):** The lecturer asked, "the first number?" the second number?"
- **Box 3 (orange):** The code snippet shows how to take user inputs and convert them into integers. The code is:
  ```python
  num1 = input("What is num2 = input("What")
  int(num1)
  ```
- **Box 4 (green):** The variable `num` is used to store the integer value.
- **Box 5 (purple):** The conversion process is illustrated here: `"10"` String `num1` integer.
- **Box 6 (pink):** The function `int()` is used to convert a string into an integer.

**Explanation:** When you use the `input()` function, the user's input is always treated as a string. To perform arithmetic operations or use the input in any other context that requires an integer, you need to convert the string into an integer using the `int()` function. For example, if the user inputs "10" and "20", the `int()` function converts these strings into the integer values 10 and 20 respectively.

> Lecturer: "num1 so basically what happens i am user input num1 so that string is now int of num1 is now the string is now integer"

The `int()` function takes a string and converts it into an integer. This is crucial because without this conversion, you cannot perform mathematical operations on the user's input.

### Extra jana kotha (lecture e bola hoy ni)
Understanding type casting is essential for handling user inputs correctly. If you do not convert the input into the appropriate data type, you might encounter errors when trying to perform operations like addition or comparison. For instance, if you try to add a string to an integer, Python will raise a TypeError. Therefore, always ensure that your inputs are converted to the correct data types before performing any operations.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**Ek line e:** Input and typecasting are essential for manipulating data types in programming.

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


1. **Box 1 (Red):** Input and Type Casting
   - The lecturer explains that when you have an integer, you can change its type to another data type, such as a string. This process is called typecasting.
   - For example, if you want to convert an integer to a string, you need to ensure that the integer is correctly assigned to a string variable.
   - The lecturer demonstrates that if you try to assign an integer directly to a string variable without proper typecasting, it will result in an error. This is because the system expects a string value, but it receives an integer instead.
   - To avoid errors, you must explicitly convert the integer to a string using appropriate typecasting methods.

2. **Box 1 (Red) Continued:** 
   - The lecturer shows that you can perform operations like addition on integers and then convert the result back to a string for printing.
   - For instance, if you have two integers, you can add them together and store the result in a variable. Then, you can convert this sum to a string and print it.
   - The lecturer mentions that in Python 3, there is a feature called F-string, which makes string formatting easier and more powerful. An F-string allows you to embed expressions inside string literals, using curly braces `{}`.

3. **Box 1 (Red) Example:**
   - The lecturer provides an example where he calculates the sum of a range of numbers (1 to 20 and 2 to 30) and prints the result using an F-string.
   - He uses the `f` prefix before the string and includes the variable name within curly braces `{}` to insert the value of the variable into the string.

**Quotes:**
> Lecturer: "So, we can see that we have two integers, two first string, so we have to convert the integer. This is the sum."
> Lecturer: "In Python 3, we have found F string and this is very powerful."

### Extra jana kotha
When working with different data types in programming, it's crucial to understand how to convert between them. Typecasting helps in ensuring that your variables hold the correct data type, preventing runtime errors. Additionally, using features like F-strings in Python can make your code more readable and efficient.

---

## Check yourself
1. What does the `input()` function return by default?
2. How do you convert a string to an integer in Python?
3. Why is type casting important when working with user inputs?
4. What is the difference between `int()` and `float()`?
5. What is an F-string in Python and why is it useful?

### Answers
1. The `input()` function returns a string.
2. You convert a string to an integer in Python using the `int()` function.
3. Type casting is important when working with user inputs because it ensures that the data is in the correct format for further processing, preventing errors.
4. `int()` is used to convert a string to an integer, while `float()` is used to convert a string to a floating-point number.
5. An F-string in Python is a formatted string literal that allows you to embed expressions inside string literals, using curly braces `{}`, making string formatting easier and more powerful.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 5 kept, 1 removed. References to boxes that do not exist: 0.*
