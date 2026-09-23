# Input and Type Casting
Ek line e: Input and Type Casting

## Key takeaways
- The `input()` function is a built-in function in Python that allows us to get input from the user.
- The `input()` function returns a string, even if the user enters a number.
- To perform arithmetic operations, we need to convert the string inputs into integers using the `int()` function.
- Using `f-string` for printing results makes the output more readable and formatted.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input and Type Casting

![Board 1: 0:00-1:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


**Red Box 1:** The topic today is input and type casting. Last class we discussed variables and how to declare them. We learned about different data types that can be stored in variables. Today, we will focus on an important and interesting topic related to variables.

**Blue Box 2:** `age = 92 input()`

**Explanation:**
1. In Python, variables are used to store data. For example, we might have a variable named `age` which stores the value `92`.
2. However, in real-life scenarios, the value of `age` can vary. It is not always fixed at `92`. To get dynamic input from the user, we use a built-in function called `input()`.
3. The `input()` function allows us to take input from the user. This function waits for the user to enter some data and then returns that data as a string.

**Quote:**
> "so shei python er ekta built-in function er eche jeta holo input. so ami jodi likhi function ta, jeta holo input function. jeta holo python er built-in ekta function."

**Mone rakho:** The `input()` function is a built-in function in Python that allows us to get input from the user. We can use this function to make our programs more interactive by allowing users to provide dynamic input.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Input and Type Casting
**Ek line e:** Input function er moddhe user e jonna ekta message diyechi.

![Board 2: 1:10-3:10](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–3:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Code


**Red Box 1 (Title):** Input and Type Casting

**Blue Box 2 (Code):** 
```python
name = input("What is your name?")
```

**Explanation:**
1. The lecturer introduced the `input` function, which is used to get input from the user. In the blue box, the lecturer wrote `name = input("What is your name?")`. This line prompts the user to enter their name and stores the input in the `name` variable.
2. After storing the user's input, the lecturer demonstrated how to print a greeting using the `print` function. In the board, the lecturer showed `print("Hello", name)`, which prints "Hello" followed by the user's name stored in the `name` variable.
3. The lecturer explained that the `input` function returns a string, even if the user enters a number. Therefore, when you use the `print` function, it will concatenate the string "Hello" with the user's name, which is also a string.
4. The lecturer emphasized the importance of not adding extra quotation marks around the variable name in the `print` function. If you add extra quotation marks, Python will treat the entire expression as a single string, which might not produce the desired output.

**Quote:**
> "jinis ta asholo evabey kaj kore jokodi user e roughy value ta dek. tarpore e print function er ashbe."

**Mone rakho:** The `input` function stores the user's input as a string, and the `print` function concatenates this string with other strings to display a personalized greeting.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** Input and Type Casting

![Board 3: 4:20-7:30](figures_annotated/board_era3_420.jpg)

*Figure 3. The whiteboard during 4:20–7:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 String · 5 String · 6 String


The lecturer started by explaining how to take inputs from the user and perform basic operations. He wrote the following code on the board:

```python
num1 = input("What is the first number?")
num2 = input("What is the second number?")
sum = num1 + num2
print(sum)
```

**Explanation:**
1. **Box 2 (blue):** The lecturer asked about the first and second numbers, which correspond to `num1` and `num2`. He explained that when the user inputs these values, they are initially treated as strings.
2. **Box 3 (orange):** He then showed the code snippet where `num1` and `num2` are added together using the `+` operator. However, since both variables are strings, the result is also a string concatenation rather than an arithmetic addition.
3. **Box 4 (green) and Box 5 (purple):** To illustrate, he displayed the strings `"10"` and `"20"`, showing how they would be concatenated to form `"1020"` instead of adding up to `30`.
4. **Box 6 (pink):** The lecturer pointed out that to perform actual arithmetic operations, we need to convert the string inputs into integers. He demonstrated this by declaring `num1` as `int(num1)` and `num2` as `int(num2)`.

**Quotes:**
> Lecturer: "so keo jodi number ta bole je 10, ashole je pacche sheta ekta string hishabe ashtese ekhane."
> Lecturer: "but amra kintu eta chacchi na. amra chacchi number, actual integer number, 10 and 20, eta add korle koto? 30 hoy."

**Mone rakho:** To ensure correct arithmetic operations, we need to convert the string inputs into integers using the `int()` function. For example, `num1 = int(input("What is the first number?"))` and `num2 = int(input("What is the second number?"))`. This will allow us to add the numbers correctly.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Input and Type Casting
**Ek line e:** In this section, we will discuss how to take input from the user and convert it into different data types.

![Board 4: 7:40-8:30](figures_annotated/board_era4_740.jpg)

*Figure 4. The whiteboard during 7:40–8:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Question · 3 Code · 4 Variable · 5 Conversion · 6 Function


**Explanation:**
1. **Red Box 1 (Title):** The title of this section is "Input and Type Casting". This section focuses on taking input from the user and converting it into various data types.
2. **Blue Box 2 (Question):** The questions in the blue box ask, "What is the first number?" and "What is the second number?" These questions are meant to guide the user on what to input.
3. **Orange Box 3 (Code):** The code snippet in the orange box shows how to take input from the user. The first line `num1 = input("What is the first number?")` takes the first number as input and stores it in the variable `num1`. The second line `num2 = input("What is the second number?")` does the same for the second number.
4. **Green Box 4 (Variable):** The green box mentions the variable `num`, which is used to store the converted integer value of `num1`.
5. **Purple Box 5 (Conversion):** The conversion shown in the purple box illustrates that the string `"10"` is converted to an integer using the `int()` function. This means that when you use `int(num1)`, the string `num1` is converted to an integer.
6. **Pink Box 6 (Function):** The pink box highlights the `int()` function, which converts a string to an integer.

**Quotes:**
> Lecturer: "so tokhon ar amar quotation lagbe na, tokhon eta ki hobe? shubur tiyan hoye thakbe. thii jace."

**Mone rakho:** In this section, we learned how to take input from the user and convert it into integers using the `int()` function. It is important to remember that the input is initially taken as a string, and we need to convert it to an integer if we want to perform arithmetic operations.

<!-- boxes: 1=#d62828 -->
## Input and Type Casting
**Ek line e:** Input and Type Casting

![Board 5: 8:40-14:00](figures_annotated/board_era5_840.jpg)

*Figure 5. The whiteboard during 8:40–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Input and Type Casting


The board shows an example of input and type casting in Python. Let's break down the process step by step:

1. **Input Values**: 
   - `num1 = input("What is the first number?")`
   - `num2 = input("What is the second number?")`
   These lines take inputs from the user and store them as strings.

2. **Type Casting**:
   - `num1 = int(num1)`
   - `num2 = int(num2)`
   Here, we convert the string inputs into integers using the `int()` function. This is necessary because mathematical operations can only be performed on numerical data types.

3. **Sum Calculation**:
   - `sum = num1 + num2`
   - `print("Result is", sum)`
   After converting the inputs to integers, we calculate their sum and print it. However, if we directly print the sum without any formatting, it will display the result as a single integer value.

4. **String Formatting**:
   - `print(f"The sum of {num1} and {num2} is {sum}")`
   The lecturer explains that using string formatting (`f-string`) allows us to print the result in a more readable format. In Python 3, `f-string` is a powerful feature that enables embedding expressions inside string literals.

**Quotes:**
> Lecturer: "ekhane amra forcefully type ta change kore dicchi."

**Mone rakho:** The key points are:
- We need to convert string inputs to integers before performing arithmetic operations.
- Using `f-string` for printing results makes the output more readable and formatted.

---

## Check yourself
1. What is the purpose of the `input()` function in Python?
2. Why do we need to convert string inputs to integers before performing arithmetic operations?
3. How do you convert a string to an integer in Python?
4. What is the difference between using `print("Hello", name)` and `print(f"Hello {name}")`?
5. What happens if you try to add two strings that represent numbers without converting them to integers?

### Answers
1. The `input()` function is a built-in function in Python that allows us to get input from the user.
2. We need to convert string inputs to integers before performing arithmetic operations because mathematical operations can only be performed on numerical data types.
3. We convert a string to an integer in Python using the `int()` function, like `num = int(input("Enter a number: "))`.
4. `print("Hello", name)` prints "Hello" followed by the string value of `name`, while `print(f"Hello {name}")` uses f-string formatting to insert the value of `name` into the string, making the output more readable.
5. If you try to add two strings that represent numbers without converting them to integers, Python will concatenate the strings instead of performing arithmetic addition, resulting in a string like "1020" instead of the sum `30`.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 6 kept, 0 removed. References to boxes that do not exist: 0.*
