# Python Variables
THE SECTIONS

## Key takeaways
- Python variables are containers for storing data values.
- Variables need to be declared with a specific data type.
- Understanding variable types (string, integer, float, boolean) is crucial for effective programming.
- Variable names should be meaningful, lowercase, and without spaces.
- Python is case-sensitive, meaning `age` and `Age` are different variables.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** A variable is a container for storing data values.

![Board 1: 0:00-1:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


- **Box 1 (red):** Python Variables
- **Box 2 (blue):** Definition: What is Variable? → [illegible] ← Apple

The lecturer starts by explaining that understanding variables is crucial for learning Python and any other programming language. He emphasizes that variables are essential for storing data, making other programming tasks much easier.

The lecturer uses an analogy of a box to explain what a variable is. He asks the students to imagine holding a box and placing different items inside it, such as a book. This represents how a variable can hold different types of data. He then extends this analogy by suggesting that if we have another box, we could place fruits inside it, representing different types of data.

To further illustrate, the lecturer mentions placing an apple in the box. He explains that the box itself is the variable, and the apple is the data stored within the variable. Therefore, the name of the variable (the box) is "apple," and the data (the apple) is what we store in the variable.

The lecturer then removes the diagram to focus on the concept. He reiterates that in Python, just like in other programming languages such as C, Java, or C#, when you create a variable, you need to specify its type. For example, if you want to store a number, you would declare the variable as an integer (int).

> Lecturer: "so toh jodi data store korte jano, every other things will be very easy to you."

In summary, a variable in Python is a container where you can store data. It has a name and holds a specific type of data, which makes it easier to manage and manipulate that data throughout your program.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** Python variables are used to store data values.

![Board 2: 1:50-3:20](figures_annotated/board_era2_150.jpg)

*Figure 2. The whiteboard during 1:50–3:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


- **Box 2 (blue):** Definition: `int (num) = 10`  
  Here, `num` is a variable name, and we assign it the value `10`. But what does `int` mean here? In Python, `int` specifies that the variable will hold an integer value. We can assign any integer value to `num`, and Python will understand that it is storing an integer.

> Lecturer: "tumi number nam er je variable ta, etar modhe tumi ei 10 value ta ke takte jacche."

In this example, `num` is assigned the integer value `10`. Python will recognize this as an integer, which means it can perform arithmetic operations on it without any issues related to decimal points.

- **Box 2 (blue):** `num = 10`  
  This line simply assigns the value `10` to the variable `num`. Python is dynamic, meaning it can change the type of data stored in a variable later if needed. For instance, if we initially set `num` to `10`, and then later assign a string or another type of data, Python will handle it accordingly.

> Lecturer: "python deijon hijei bujhe jabe je e ten value ta ashole ekta integer ta o number e monti store kore rakbe."

Python understands that `num` holds an integer value, and it can perform various mathematical operations on it. However, if you try to add a string to `num`, Python will raise an error because it expects both operands to be of the same type.

### Extra jana kotha
Understanding variables and their types is crucial for writing effective Python code. Variables allow us to store and manipulate data, and knowing the type of data they hold helps in performing the correct operations. For example, if you need to perform arithmetic operations, ensure that the variables involved are integers or floats. If you mix types, Python will throw an error, which can help you debug your code more easily.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** Python variables are used to store data values.

![Board 3: 3:40-7:00](figures_annotated/board_era3_340.jpg)

*Figure 3. The whiteboard during 3:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data Type


1. **Red Box 1 (Python Variables):** This box introduces the concept of Python variables. Variables are containers that hold data values.
2. **Blue Box 2 (Data Types):** This box lists four types of data: i) String ii) Integer iii) Float iv) Bool. Each type is represented with an example.

### Explanation
1. **String:** A string is a sequence of characters enclosed in single or double quotes. For example, if we want to store our name, we can do so using a string. Let's take the name "Hasan". We can write `name = 'Hasan'`. Here, 'Hasan' is a string because it is enclosed in single quotes.
2. **Integer:** An integer is a whole number, positive or negative, without decimals. For example, if we want to store the age, we can use an integer. Let's take the age 10. We can write `age = 10`.
3. **Float:** A float is a number with a decimal point. For example, if we want to store a measurement like 3.5, we can use a float. We can write `float_value = 3.5`.
4. **Boolean:** A boolean is a data type that can have only two values: `True` or `False`. For example, if we want to check whether a condition is true or false, we can use a boolean. We can write `is_valid = True`.

The lecturer explained, "string holo je konor jinis je mon dhoro boli je jodi boli je amar nam obuk, amar nam tomo. amar nam dhoro je amar nam holo ahasan. thik ache? toh amra ki likhte pari? string ar moddhe je kono jinis en name. ami je kotha gulo boltesi, eigulo je ekta subtitle ache, shegulo kootumi string hishabe dekhte paro."

### Extra jana kotha
Understanding variables and their data types is crucial for programming. Variables allow us to store and manipulate data efficiently. Knowing the difference between strings, integers, floats, and booleans helps in writing correct and efficient code.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**Ek line e:** Python variables er naming convention er somanikto.

![Board 4: 7:10-9:50](figures_annotated/board_era4_710.jpg)

*Figure 4. The whiteboard during 7:10–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data · 3 Code


- **Box 1 (red):** Python Variables
- **Box 2 (blue):** Data: Type:
- **Box 3 (orange):** Code: `Iname = "Rafi"` `Name1 = 'I'`

The lecturer explained that when we look at a piece of code, it's important to understand the type of a variable. In the given code, the variable names are `Iname` and `Name1`. The lecturer pointed out that these names are just placeholders for the variable names, not their types. He then asked, "What is the type of these variables?" 

The lecturer emphasized that the names of variables should be meaningful and consistent. He quoted, "Variable naming is very important." He explained that when other people look at your code, they can quickly understand the purpose of your variables based on their names. 

The first rule for naming variables is to use lowercase letters for the names. For example, he wrote `name` instead of `Name`. He said, "We start with small data for variable names." 

He then demonstrated that if you try to assign an integer value to a variable named as a string, it will result in an error. For instance, if you write `name = 1`, it will cause a direct error because `name` is defined as a string. He showed this with the code `name = "Rafi"`. 

The second rule is to avoid using spaces in variable names. He demonstrated this by writing `Name1 = 'I'` and explained that using `Name 1` would be incorrect.

**Mone rakho:** Variable names should be in lowercase, without spaces, and meaningful. Directly assigning an integer to a string variable will result in an error.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**Ek line e:** Python variables are used to store data.

![Board 5: 10:00-10:50](figures_annotated/board_era5_1000.jpg)

*Figure 5. The whiteboard during 10:00–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table


- **Box 1 (red):** Title: Python Variables
- **Box 2 (blue):** Definition: Data
- **Box 3 (orange):** Truth table: Type: Name X Name √ Iname = "Rafi" X name1=“Rafi” √ my_name = “Rafi”

The lecturer explained that when you write `my name = "Rafi"`, you might think it's correct, but it's not because there's a space in the name. To handle spaces, you can use an underscore `_` instead, like `my_name = "Rafi"`. The lecturer mentioned that the Python community prefers underscores over spaces for variable names.

The lecturer also introduced camel casing, where the first word is lowercase and subsequent words are capitalized, such as `myName`. However, the lecturer noted that snake casing, where words are separated by underscores, is the preferred style in the Python community. For example, `my_name` is more common.

Finally, the lecturer emphasized that Python is case-sensitive, meaning `my_name` and `My_Name` would be treated as different variables. This is crucial because developers often need to distinguish between similar variable names, ensuring accurate and efficient coding practices.

**Mone rakho:** Python uses underscores for variable names, follows snake casing, and is case-sensitive.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Python Variables
**Ek line e:** Python variables are case-sensitive.

![Board 6: 11:20-12:50](figures_annotated/board_era6_1120.jpg)

*Figure 6. The whiteboard during 11:20–12:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula · 4 Code


- **Box 1 (red):** Title: Python Variables
- **Box 2 (blue):** Definition: Data Type
- **Box 3 (orange):** Formula: `pi = 3.1414`
- **Box 4 (green):** Code: `age=10`, `age=10`

The lecturer explained that Python variables are case-sensitive. For example, if we define `age` as an integer value, like `10`, and then mistakenly write `Age` instead of `age`, Python will treat these as different variables. This is because the first character of the variable name is a capital letter (`A`) while the correct one is a lowercase letter (`a`). Therefore, it's crucial to maintain consistent naming conventions when working with variables.

The lecturer also demonstrated that even though the values might be the same, the variable names must match exactly. For instance, `age` and `age` are considered the same variable, but `age` and `Age` are treated as different variables. To avoid confusion, we should always use the same name consistently throughout our code.

Next, the lecturer introduced the concept of data types. There are several data types in Python, including integers, strings, booleans, and floats. An example of an integer was shown using the variable `age`. Additionally, the lecturer provided an example of a float, `pi = 3.1414`, which is a decimal number. 

To further illustrate, the lecturer mentioned that `pi` is a common constant used in mathematics, representing the ratio of a circle's circumference to its diameter. It is not a whole number, making it a float. Another example of a data type was given for booleans, where `True` and `False` represent valid boolean values.

In summary, understanding and correctly using variables and their associated data types is fundamental in Python programming. We will explore more about arithmetic operations in the next class.

**Mone rakho:** Variables are case-sensitive, integers, floats, and booleans are different data types in Python.

---

## Check yourself
1. What is a variable in Python?
2. How do you declare an integer variable in Python?
3. What happens if you try to add a string to an integer variable?
4. List four data types in Python.
5. Why is it important to follow case sensitivity in variable naming?

### Answers
1. A variable in Python is a container for storing data values.
2. You declare an integer variable in Python by using the `int` data type, for example, `num = 10`.
3. If you try to add a string to an integer variable, Python will raise an error because it expects both operands to be of the same type.
4. Four data types in Python are string, integer, float, and boolean.
5. It is important to follow case sensitivity in variable naming because Python treats `age` and `Age` as different variables, which can lead to errors in the code.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
