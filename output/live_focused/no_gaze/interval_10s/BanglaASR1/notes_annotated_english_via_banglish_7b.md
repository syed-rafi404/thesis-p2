# Python Variables
The sections cover the concept of Python variables, including what they are, how to use them, and the importance of naming conventions.

## Key takeaways
- Variable, container, data storage, box analogy, variable name, data.
- Python variables are used to store data values.
- String, integer, float, and boolean are the four main data types in Python.
- Use underscores in variable names and follow snake case convention.
- Python is case-sensitive.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**In one line:** A variable is a container for storing data values.

![Board 1: 0:00-1:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


- **Box 1 (red):** Python Variables
- **Box 2 (blue):** Definition: What is Variable? → [illegible] ← Apple

The lecturer starts by explaining the importance of variables in Python and programming in general. He emphasizes that understanding variables is crucial because they allow us to store and manipulate data easily.

The lecturer uses an analogy of a box to explain what a variable is. He asks the students to imagine holding a box and placing different items inside it, such as a book. This represents how we can store various types of data in a variable.

Next, he introduces the concept of a variable name and the data stored within it. For instance, if we place an apple in the box, the box itself represents the variable name, while the apple represents the data stored in that variable.

To illustrate, the lecturer writes `Apple` on the board and explains that this is the name of the variable, and the apple is the data stored in it.

> Lecturer: "so think of like a box."

The lecturer then removes the `Apple` from the board to emphasize that the variable name can hold different types of data, just like the box can hold different items.

> Lecturer: "so eita ami mujhhe feltesi."

In summary, a variable in Python is a container where we can store data. The name of the variable is like the label on the box, and the data stored in it is like the item inside the box.

**Remember:** Variable, container, data storage, box analogy, variable name, data.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**In one line:** Python variables are used to store data values.

![Board 2: 1:50-3:20](figures_annotated/board_era2_150.jpg)

*Figure 2. The whiteboard during 1:50–3:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


- **Box 2 (blue):** This box defines an integer variable `num` with the value `10`. The line `int(num) = 10` indicates that `num` is an integer type variable initialized with the value `10`.

The lecturer said: "When we define a variable like `num = 10`, we are assigning the value `10` to the variable `num`. However, the question arises, 'What is the module here?' In Python, we need to specify the type of data that the variable will hold. Here, we simply write `num` and assign the value `10`. Python will understand that this value is an integer."

The lecturer further clarified that the `num` variable here is an example of how we can assign a value to a variable. If we consider a box, the value inside the box is `10`, which represents the assigned value. The lecturer emphasized that Python is dynamic, meaning it can store the integer value `10` in the variable `num`. When we perform operations on `num`, we just refer to it as `num`, not its specific value. This allows us to perform various mathematical operations on the variable.

The lecturer mentioned that in the next video, we will explore more about different data types and how to use them with variables. For now, we have covered the basics of variables in Python.

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding variables in Python is crucial. Variables allow us to store and manipulate data. By specifying the type of data (like integer, string, etc.), we ensure that the operations performed on the variable are meaningful and correct.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**In one line:** Python variables are used to store data values.

![Board 3: 3:40-7:00](figures_annotated/board_era3_340.jpg)

*Figure 3. The whiteboard during 3:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data Type


1. **Red Box 1 (Python Variables):** This box introduces the concept of Python variables. Variables are containers that hold data values.
2. **Blue Box 2 (Data Type):** There are four main types of data in Python: String, Integer, Float, and Boolean.

### Explanation
The lecturer explained the different data types in Python step-by-step:

- **String:** A string is a sequence of characters. For example, `Fruit = 'Apple'`. Strings are enclosed in single or double quotes. The lecturer demonstrated this by showing how to assign the word "Apple" to a variable named `Fruit`.
- **Integer:** An integer is a whole number, positive or negative, without decimals. For example, `Age = 10`. The lecturer mentioned that integers can be used to represent whole numbers like age.
- **Float:** A float is a number with a decimal point. For example, `Float = 3.5`. The lecturer gave an example of `3.5` and `2.5`, showing that floats can represent numbers with fractional parts.
- **Boolean:** A boolean can have only two values: `True` or `False`. For example, `True` or `False`. The lecturer explained that booleans are used to represent logical values.

The lecturer also provided an example to illustrate the use of strings:
```python
Fruit = 'Apple'
```
He then showed how to use multiple strings in a program:
```python
food = 'fruit'
fruit = 'apple'
```
Here, `fruit` is assigned the value `'apple'`.

The lecturer further explained:
- **Integer Example:** `Age = 10` represents a whole number.
- **Float Example:** `3.1416` is a float.
- **Boolean Example:** `True` or `False` are the only possible values for a boolean variable.

The lecturer concluded by mentioning that Python has a built-in function called `type()` which can be used to determine the data type of a variable. For example, if you have a variable `name`, you can check its type using `type(name)`.

### Background (not said in the lecture)
Understanding Python variables and their data types is crucial for writing effective programs. Variables allow you to store and manipulate data, and knowing the correct data type helps in performing operations accurately. For instance, using the wrong data type can lead to errors in your program.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**In one line:** Python variables er naming convention er somanikto hocche.

![Board 4: 7:10-9:50](figures_annotated/board_era4_710.jpg)

*Figure 4. The whiteboard during 7:10–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data · 3 Code


1. **Box 1 (red):** Python Variables
2. **Box 2 (blue):** Data: Type:
3. **Box 3 (orange):** Code: `Iname = "Rafi"` `Name1 = '1'`

The lecturer said: "When we look at a piece of code, it's important to understand the type of a variable. In the given code, `Iname` and `Name1` are defined, but the type is not explicitly mentioned. The lecturer pointed out that the names `Iname` and `Name1` are the names of the variables, which can be confusing. However, the type of these variables can be determined by their values. Here, `Iname` is assigned a string value `"Rafi"`, and `Name1` is assigned the string `'1'`. Therefore, both variables are of type `str`, which stands for string."

> Lecturer: "So variable er naming ta khubi important dekhte jinis."

The lecturer said: "Variable naming is crucial because when someone else reads your code, they should be able to understand the purpose of the variable just by looking at its name. For instance, if you see a variable named `Iname`, you would expect it to hold a string value like `"Rafi"`."

### Background (not said in the lecture) (lecture e bola hoy ni)
The first rule for naming variables is to use lowercase letters. This makes the code more readable and consistent. For example, instead of using `Iname`, you should use `iname`. Additionally, avoid using spaces in variable names; instead, use underscores if needed. For instance, `name_1` is better than `name 1`.

**Remember:** Variable er naming convention, type er detection, and consistency in naming.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**In one line:** Python variables are used to store data.

![Board 5: 10:00-10:50](figures_annotated/board_era5_1000.jpg)

*Figure 5. The whiteboard during 10:00–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table


- **Box 1 (red):** This box introduces the topic of Python variables.
- **Box 2 (blue):** The blue box defines data, which is stored in variables.
- **Box 3 (orange):** The orange box provides examples of valid variable names. It shows three different ways to define a variable named `my_name`:
  - `lname = "Rafi"` (X) - This is incorrect because it uses a space, which is not allowed in variable names.
  - `name1="Rafi"` (√) - This is correct because it uses an underscore, which is acceptable in Python.
  - `my_name = "Rafi"` - This is also correct and follows the snake_case convention.
  - `myNam` - This is incorrect because it doesn't follow any naming convention.

The lecturer said: "When you write `my name = "Rafi"`, you need to use an underscore instead of a space. Why? Because there is a space in the name, and we need to indicate how to handle spaces in variable names. The lecturer suggested using an underscore, which is commonly accepted in the Python community."

The lecturer also introduced camel case, where the first word is lowercase and subsequent words start with uppercase letters. For example, `myName`. However, the lecturer noted that in the Python community, snake case (using underscores) is the preferred convention.

Finally, the lecturer emphasized that Python is case-sensitive, meaning `my_name` and `My_Name` would be considered different variables. This is crucial for developers to remember, as it can lead to bugs if not handled correctly.

**Remember:** 
- Use underscores in variable names.
- Follow snake case convention in Python.
- Python is case-sensitive.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Python Variables
**In one line:** Python variables are case-sensitive.

![Board 6: 11:20-12:50](figures_annotated/board_era6_1120.jpg)

*Figure 6. The whiteboard during 11:20–12:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula · 4 Code


- **Box 1 (red):** Title: Python Variables
- **Box 2 (blue):** Definition: Data Type:
- **Box 3 (orange):** Formula: `pi = 3.1414`
- **Box 4 (green):** Code: `age = 10`, `age = 10`

The lecturer said: "Python variables are case-sensitive."

For example, `age` and `Age` would be considered different variables. He demonstrated this by showing that `age = 10` and `age = 10` both store an integer value of 10. However, if we mistakenly write `Age = 10`, it would be treated as a different variable.

The lecturer then showed us the definition of a variable, which is essentially a name given to a piece of data that can be stored and manipulated. He used the example of `age = 10` to illustrate how a variable can hold an integer value. He also mentioned that Python supports several data types including string, integer, boolean, and float. To demonstrate a float, he wrote `pi = 3.1414`.

He further explained that `pi` is a floating-point number, which is not a whole number. He also gave an example of a boolean value, such as `True` and `False`. The lecturer concluded by saying that in the next class, we will start learning about arithmetic operations using these data types.

> Lecturer: "Python variables are case-sensitive."

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding that variables are case-sensitive is crucial because it prevents common mistakes. For instance, writing `age` and `Age` separately ensures that you are working with distinct variables, which can lead to bugs if not handled carefully.

---

## Check yourself
1. What is a variable in Python?
2. How do you define an integer variable in Python?
3. List the four main data types in Python.
4. What is the difference between `age` and `Age` in Python?
5. Why is it important to use underscores in variable names?

### Answers
1. A variable in Python is a container where we can store data.
2. You define an integer variable in Python by writing `variable_name = integer_value`, for example, `num = 10`.
3. The four main data types in Python are string, integer, float, and boolean.
4. In Python, `age` and `Age` are considered different variables because Python is case-sensitive.
5. Using underscores in variable names helps in making the code more readable and consistent, following the snake case convention.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (4 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
