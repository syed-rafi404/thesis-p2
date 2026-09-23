# Input and Type Casting
Ek line e: Input and Type Casting

## Key takeaways
- The `input()` function is used to take input from the user.
- Whatever the user types using the `input()` function is always treated as a string.
- To perform arithmetic operations, we need to convert string inputs to integers using the `int()` function.
- String formatting using f-strings can make the output more readable and user-friendly.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input and Type Casting

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


The lecturer started by revisiting the previous class where they discussed variables. Variables can hold different types of data such as integers, strings, etc. Today, they will focus on an important and interesting topic: input and type casting.

1. **Declaring a Variable**: The lecturer mentioned that we often declare variables to store specific values. For example, they declared a variable named `age` and set its value to 92 using the statement `age = 92`.

2. **User Input**: However, in real-life scenarios, the value of a variable like `age` might not always be fixed. We need to allow users to input their own values. To achieve this, Python provides a built-in function called `input()`. This function allows us to take input from the user.

3. **Using the `input()` Function**: The lecturer demonstrated the usage of the `input()` function by declaring a new variable named `name`. They used the statement `name = input()`. Here, the `input()` function waits for the user to enter some text and then stores that text in the variable `name`.

> Lecturer: "so shei python er ekta built-in function er eche jeta holo input. so ami jodi likhi function ta, jeta holo input function. jeta holo python er built-in ekta function. so ei built-in function er maddome amra user e theke input naya thakeu."

### Extra jana kotha
When you use the `input()` function, the value entered by the user is always treated as a string. If you need to perform operations that require numerical values, you will need to convert the string to an integer or float using type casting functions like `int()` or `float()`. This ensures that the operations are performed correctly.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input function er moddhe user e jonna message dite hobe.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


1. **Red Box 1 (Title):** Input and Type Casting
2. **Blue Box 2 (Code):** `name = input("What is your name?")`

The lecturer said: "We are using the `input` function to get input from the user. Here’s how it works:

- **Step 1:** We start by writing `name = input("What is your name?")`. This line prompts the user to enter their name. When the user types their name and presses Enter, the value entered by the user is stored in the `name` variable.
- **Step 2:** Next, we use the `print` function to display a greeting along with the user's name. The code looks like this: `print("Hello", name)`. The `print` function is a built-in Python function used to output text or variables. In this case, it prints "Hello" followed by the value stored in the `name` variable.

The lecturer emphasized that when you use the `input` function, whatever the user types is treated as a string. For example, if the user types "Rafi", the value of `name` will be "Rafi".

**Quotes:**
> Lecturer: "ami ekhane input function ta likhechi. tarpore ami user e jonna ekta message diyechi. message ta ki je what is your name? user jokhon ei message ta dekhbe user korbe ki? or nijan nam ta o likhbe."

### Extra jana kotha
When you use the `input` function, the value entered by the user is always a string. Even if the user enters a number, it will still be treated as a string. For example, if the user types "123", the value of `name` will be "123". To convert this string to an integer, you would need to use the `int()` function. This is a common mistake beginners make, so always remember to check the data type of the input before performing operations on it.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** Input and type casting are essential for handling data correctly in programming.

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


1. **Red Box (Box 1):** The title "Input and Type Casting" sets the context for the discussion.
2. **Blue Box (Box 2):** The questions "the first number?" and "the second number?" guide the user input process.
3. **Orange Box (Box 3):** The code snippet demonstrates how to take inputs and perform addition.
4. **Purple Box (Box 4):** The string "10" represents the first number input.
5. **Pink Box (Box 5):** The string "20" represents the second number input.
6. **Pink Box (Box 6):** An empty string is shown, indicating a potential placeholder for future use.

The lecturer said: "We need to take two numbers as input from the user and add them together. Here’s a step-by-step breakdown:

- **Step 1:** We start by taking the first number from the user using the `input` function. The prompt asks, "What is the first number?" This is stored in the variable `num1`.
- **Step 2:** Similarly, we take the second number from the user and store it in the variable `num2`. The prompt here is "What is the second number?"
- **Step 3:** We then add these two numbers together and store the result in the variable `sum`.
- **Step 4:** Finally, we print the sum using the `print` function.

However, the lecturer pointed out an important issue: when we take input from the user, it is always treated as a string. For example, if the user inputs "10" and "20", both are stored as strings. To perform arithmetic operations like addition, we need to convert these strings into integers.

- **Step 5:** To fix this, we need to convert the string inputs into integers before performing the addition. This can be done using the `int()` function. So, instead of directly adding `num1` and `num2`, we should use `int(num1) + int(num2)`.

The lecturer emphasized that beginners often forget to convert string inputs to integers, leading to incorrect results. For instance, if `num1` is "10" and `num2` is "20", adding them directly would result in "1020" instead of 30.

**Quotes:**
> Lecturer: "so keo jodi number ta bole je 10, ashole je pacche sheta ekta string hishabe ashtese ekhane."
> Lecturer: "but amra kintu eta chacchi na. amra chacchi number, actual integer number, 10 and 20, eta add korle koto? 30 hoy."

### Extra jana kotha
When dealing with user inputs, always remember to convert string inputs to integers before performing any arithmetic operations. This ensures that your program works correctly and gives the expected results.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** In this section, we learn how to take user inputs and convert them into integers.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


- **Red Box 1 (Input and Type Casting):** This box introduces the topic of input and type casting. We will take user inputs and convert them into different data types.

- **Blue Box 2 (Question):** The lecturer asked, "the first number?" the second number?" These questions indicate that we are taking two inputs from the user.

- **Orange Box 3 (Code):** The code snippet here is `num1 = input("What is the first number?")` and `num2 = input("What is the second number?")`. This shows how to take two inputs from the user. The inputs are stored in variables `num1` and `num2`.

- **Green Box 4 (Variable):** The variable `num` is introduced here. It will store the converted integer value of `num1`.

- **Purple Box 5 (Conversion):** The conversion process is shown here. `"10" String` is converted to an integer using `int(num1)`. This means that the string `"10"` is being converted to the integer `10`.

- **Pink Box 6 (Function):** The function `int(` is used to convert a string to an integer. For example, `int("10")` converts the string `"10"` to the integer `10`.

> Lecturer: "so ekhane basically ki hocche? ami user theke input niaychi num1. sheta ki? 10. string e chilo. ami jokhon int of aa num1 kore dicchi, ei string ta hoye jacche ki? amar integer."

### Extra jana kotha
When you take input from the user, it is always a string. To use it as an integer, you need to convert it using the `int()` function. For example, if the user inputs `"10"`, you can convert it to the integer `10` using `int("10")`. Similarly, if you want to convert `num1` to an integer, you would use `int(num1)`.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**Ek line e:** Input and Type Casting

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


The red box 1 on the board introduces the topic of Input and Type Casting. The lecturer explains that we need to convert input values from strings to integers, which is known as type casting. Here’s how it works:

1. **Step 1:** We start by assigning values to `num1` and `num2`.
    ```python
    num1 = 20
    num2 = 30
    ```
    The lecturer writes these lines on the board and explains that initially, these values are integers.

2. **Step 2:** The lecturer then calculates the sum of `num1` and `num2` and prints the result.
    ```python
    The Sum of 20 and 30 is 50
    ```
    This is straightforward addition, resulting in `50`.

3. **Step 3:** Next, the lecturer demonstrates how to take user input and convert it to an integer.
    ```python
    num1 = input("What is the first number?")
    num2 = input("What is the second number?")
    ```
    The lecturer explains that if the user inputs a string instead of an integer, we will get an error because Python cannot add a string to an integer.

4. **Step 4:** To avoid this error, we need to convert the user input from a string to an integer using the `int()` function.
    ```python
    num1 = int(num1)
    num2 = int(num2)
    ```
    The lecturer points out that if the user inputs a non-integer value, like "hello", the program will raise a `ValueError`.

5. **Step 5:** After converting the inputs to integers, we can calculate the sum and print it.
    ```python
    sum = num1 + num2
    print("Result is", sum)
    ```
    The lecturer emphasizes that the final output will be an integer, not a string.

6. **Step 6:** To make the output more readable, the lecturer introduces string formatting using the `f-string` feature in Python 3.
    ```python
    print(f"The sum of {num1} and {num2} is {sum}")
    ```
    The lecturer explains that this method allows us to embed variables directly into the string, making the output more meaningful and easier to read.


### Extra jana kotha (lecture e bola hoy ni)
String formatting is a powerful feature in Python that helps in creating more readable and formatted output. It is particularly useful when you want to include variable values within a string. For example, if you have `num1 = 20` and `num2 = 30`, the output will be "The sum of 20 and 30 is 50". This makes the output more user-friendly and easier to understand.

---

## Check yourself
1. What is the purpose of the `input()` function?
2. Why do we need to convert string inputs to integers before performing arithmetic operations?
3. How do you convert a string to an integer in Python?
4. What happens if you try to add a string and an integer without converting the string to an integer?
5. How can you use f-strings to format the output?

### Answers
1. The purpose of the `input()` function is to take input from the user.
2. We need to convert string inputs to integers before performing arithmetic operations because Python cannot perform arithmetic operations on strings.
3. You convert a string to an integer in Python using the `int()` function.
4. If you try to add a string and an integer without converting the string to an integer, you will get a `TypeError`.
5. You can use f-strings to format the output by embedding variables directly into the string using the `f` prefix, like `f"The sum of {num1} and {num2} is {sum}"`.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (5 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
