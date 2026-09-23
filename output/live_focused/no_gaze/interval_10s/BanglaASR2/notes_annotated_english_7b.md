# Input and Type Casting
We learn about taking user input and the importance of type casting in Python.

## Key takeaways
- Always use the `input()` function to get dynamic user input.
- User inputs are always treated as strings, so use type casting to convert them to integers or floats for arithmetic operations.
- Use string formatting to make the output more readable and meaningful.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**In one line:** We learn about taking user input and the importance of type casting in Python.

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


### Explanation
1. **Introduction to Variables**: The lecturer starts by reminding us that in the previous class, we discussed variables. Variables can hold different types of data such as integers, strings, etc. (Red Box 1)
2. **User Input**: In real-life applications, the value of a variable like `age` might not always be fixed. For instance, `age` could be 92, but in practice, it can vary. To get dynamic input from the user, Python provides a built-in function called `input`. (Blue Box 2)
3. **Example of User Input**: The lecturer demonstrates how to use the `input()` function. Here, we declare a variable `age` and set it to 92, but then we use the `input()` function to take user input. (Blue Box 2)

> Lecturer: "ei variable er value thoro 42. thik ache? but real life e erokom ki 42 daba thake? thake na. amra user e theke input nei."  
> (In English: "The value of this variable is 42. Is that correct? But in real life, can 42 be the value? Can it? So, we need to take input from the user.")

**Remember:** Always use the `input()` function to get dynamic user input, and be aware of the data type of the input to avoid type-related errors.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**In one line:** We learn how to use the `input` function to get user input and store it in a variable.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


### Explanation
1. **Understanding the `input` Function**: Look at the blue box 2, which shows the code `name = input("What is your name?")`. Here, we are using the `input` function to prompt the user to enter their name. The function takes a string as an argument, which is displayed to the user. For example, when the user sees "What is your name?", they will type their name and press Enter. This entered name is then stored in the `name` variable.
   
2. **Using the `print` Function**: After storing the user's input, we can display a personalized greeting. In the board, you see `print("Hello", name)`. This line uses the `print` function to output "Hello" followed by the user's name. The `print` function is a built-in Python function that outputs the specified message to the console.
   
3. **Combining `input` and `print`**: The combination of these functions allows us to create interactive programs where the user can provide input, and the program can respond accordingly. For instance, the board shows `print("Hello", name)`, which prints "Hello R" if the user inputs "R".
   
4. **Important Note**: The lecturer emphasized that when using the `input` function, the value entered by the user is always treated as a string. Even if the user enters a number, it will be stored as a string. Therefore, if you need to perform operations like arithmetic, you would need to convert the string to an integer or float using type casting.

**Quote**

**Remember**: Always ensure that user input is handled correctly, especially when performing operations that require numerical values.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting

**In one line:** We need to handle type casting to ensure arithmetic operations work correctly with user inputs.

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


- **Box 1 (red)**: Title: Input and Type Casting
- **Box 2 (blue)**: Question: the first number? the second number?
- **Box 3 (orange)**: Code: 
  ```python
  num1 = input("What is the first number?")
  num2 = input("What is the second number?")
  sum = num1 + num2
  print(sum)
  ```
- **Box 4 (green)**: String: "10" String
- **Box 5 (purple)**: String: "20" String
- **Box 6 (pink)**: String: String

The lecturer explained that when we take user inputs using the `input()` function, the inputs are always treated as strings. For example, if the user inputs "10" and "20", these are stored as strings. However, if we try to add these strings directly, Python will concatenate them rather than perform arithmetic addition. This means "10" + "20" would result in "1020" instead of 30.

**Quote:**
> "so keo jodi number ta bole je 10, ashole je pacche sheta ekta string hishabe ashtese ekhane."  
> (In English: "so when you say a number like '10', it becomes a string here.")

To fix this issue, we need to convert the string inputs into integers before performing addition. The lecturer demonstrated this by showing how to use the `int()` function to cast the string inputs to integers.

**Remember:** Always use type casting when dealing with user inputs to ensure arithmetic operations work as expected.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**In one line:** This section explains how to take input from the user and convert it into an integer.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


### Explanation
1. **Box 1 (red)**: The title "Input and Type Casting" indicates the topic of the discussion.
2. **Box 2 (blue)**: The questions "the first number?" and "the second number?" are asking the user to input two numbers.
3. **Box 3 (orange)**: The code `num1 = input("What is the first number?")` shows how to take the first number as input from the user. Similarly, `num2 = input("What is the second number?")` takes the second number as input.
4. **Box 4 (green)**: The variable `num` is assigned the value of `int(num1)`, which converts the string input `num1` into an integer.
5. **Box 5 (purple)**: The conversion `"10" String int(num1) -> integer` illustrates that the string `"10"` is converted into an integer when the `int()` function is applied.
6. **Box 6 (pink)**: The function `int(` is used to convert a string into an integer.

> Lecturer: "so ekhane basically ki hocche? ami user theke input niaychi num1. sheta ki? 10. string e chilo. ami jokhon int of aa num1 kore dicchi, ei string ta hoye jacche ki? amar integer."
> (In English: "Here basically what is happening? I am taking input from the user for num1. It is? 10 as a string. When I apply the int function to this num1, this string becomes an integer.")

**Remember:** Always use the `int()` function to convert a string input into an integer before performing arithmetic operations.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**In one line:** This section explains how to handle type casting and string formatting in Python to ensure accurate arithmetic operations and meaningful output.

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


The board shows an example of taking user input and performing arithmetic operations in Python. Let's break down the process step-by-step:

1. **Input Values**: 
   - `num1 = input("What is the first number?")`
   - `num2 = input("What is the second number?")`
   These lines take input from the user and store it as strings.

2. **Type Casting**:
   - `num1 = int(num1)`
   - `num2 = int(num2)`
   Here, we convert the string inputs into integers using the `int()` function to perform arithmetic operations.

3. **Arithmetic Operation**:
   - `sum = num1 + num2`
   We add the two numbers to get their sum.

4. **Output**:
   - `print("Result is", sum)`
   - `print(f"The sum of {num1} and {num2} is {sum}")`
   These lines print the result. The first method prints the sum directly, while the second uses string formatting to include the original input values.

> Lecturer: "ekhon jodi ami sum nei. and tahole ekhon jodi print kori."
> (In English: "now if I have the sum. and then if I print it.")

**Remember:** Always convert user inputs to the appropriate data type before performing arithmetic operations to avoid errors. Using string formatting can make the output more readable and meaningful.

---

## Check yourself
1. What is the `input()` function used for?
2. Why do we need to use type casting when working with user inputs?
3. How do you convert a string to an integer in Python?
4. What is the difference between printing `sum` and using string formatting to print the sum?
5. Give an example of how to take two numbers from the user, convert them to integers, and print their sum.

### Answers
1. The `input()` function is used to get dynamic user input.
2. We need to use type casting because user inputs are always treated as strings, and we need to perform arithmetic operations on numerical values.
3. You convert a string to an integer in Python using the `int()` function.
4. Printing `sum` directly just shows the sum as a number, whereas using string formatting includes the original input values in the output, making it more readable.
5. Example:
    ```python
    num1 = input("What is the first number? ")
    num2 = input("What is the second number? ")
    num1 = int(num1)
    num2 = int(num2)
    sum = num1 + num2
    print("The sum of", num1, "and", num2, "is", sum)
    ```

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 1 removed. References to boxes that do not exist: 0.*
