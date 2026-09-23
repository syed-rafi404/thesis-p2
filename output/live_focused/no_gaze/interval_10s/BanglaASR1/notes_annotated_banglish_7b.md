# Python Variables
THE SECTIONS COVER THE CONCEPT OF PYTHON VARIABLES, INCLUDING THEIR DEFINITION, TYPES, NAMING CONVENTIONS, AND CASE SENSITIVITY.

## Key takeaways
- Variables in Python are used to store data.
- Variables can hold different types of data such as strings, integers, floats, and booleans.
- Variable names should start with a lowercase letter and avoid spaces, following the snake casing convention.
- Python is case-sensitive, so `age` and `Age` are considered different variables.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** Python er variable jinishta ashole important ekta topic.

![Board 1: 0:00-1:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


**Red Box 1 (Title):** Python Variables

The lecturer started by introducing the concept of variables in Python. He explained that understanding variables is crucial for learning any programming language, including Python. Variables are essentially containers where we can store data. To illustrate, he asked us to imagine a box and then placed an apple inside it. This apple represents the data stored in a variable.

**Blue Box 2 (Definition):** What is Variable? → [illegible] ← Apple

The lecturer used the analogy of a box to explain variables. He said, "Think of like a box." He then asked us to visualize a box and place different items inside it, such as a book. He continued, "So, if you put a book in the box, that book is your data stored in the variable."

He further explained, "Now, if you want to store a fruit, you might put an apple in the box. In this case, the box itself is the variable, and the apple is the data stored within it." He emphasized that the name of the variable (the box) and the data (the apple) are separate but related concepts.

**Quotes:**
> Lecturer: "Think of like a box."

**Mone Rakho:** The key points from the board include the definition of a variable as a container for storing data, and the example of a box containing an apple to represent a variable storing data.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** Python variables are used to store data values.

![Board 2: 1:50-3:20](figures_annotated/board_era2_150.jpg)

*Figure 2. The whiteboard during 1:50–3:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


**Red Box 1 (Title):** Python Variables

**Blue Box 2 (Definition):** `int (num) = 10`  
`num = 10`  
Box Value

**Explanation:**
1. In the blue box, we see an example of how to define a variable in Python. Here, `num` is assigned the integer value `10`.
2. The lecturer explains that while we can simply write `num`, Python needs to know the type of data we are working with. In this case, we are dealing with an integer (`int`).
3. The lecturer emphasizes that Python will understand that `10` is an integer and will store it accordingly. This is an example of dynamic typing, where Python determines the type at runtime.
4. The lecturer mentions that if we had a decimal value, like `10.5`, it would still be stored as an integer here because there is no decimal point. However, in real-life scenarios, such values are often represented as floating-point numbers.
5. The lecturer uses the example of a box to illustrate that `num` is just a placeholder for the value `10`. When we change the value of `num`, Python will update it accordingly.

**Quote:**
> "etar modhe tumi ei 10 value ta ke takte jacche."

**Mone Rakho:** The key points from the board include understanding how to assign integer values to variables in Python and recognizing the importance of specifying the data type.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Python Variables
**Ek line e:** Python variables are used to store data.

![Board 3: 3:40-7:00](figures_annotated/board_era3_340.jpg)

*Figure 3. The whiteboard during 3:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data Type


**Red Box 1 (Python Variables):** This box introduces the concept of Python variables.

**Blue Box 2 (Data Type):** This box lists four types of data: String, Integer, Float, and Bool.

**Explanation:**
1. **String:** A string is a sequence of characters enclosed in single or double quotes. For example, `Fruit = 'Apple'` or `Fruit = "Apple"`. Strings can represent any text, like your name.
2. **Integer:** An integer is a whole number, positive or negative, without decimals. For example, `Age = 10`.
3. **Float:** A float is a number with a decimal point. For example, `Float = 3.5`.
4. **Bool:** A boolean can have two values: `True` or `False`. For example, `True` or `False`.

**Quotes:**
> Lecturer: "string holo je konor jinis je mon dhoro boli je jodi boli je amar nam obuk, amar nam tomo."

**Mone rakho:** In Python, you can store different types of data using variables. Each type of data is represented by a specific data type. Strings are used to store text, integers for whole numbers, floats for numbers with decimals, and booleans for logical values (`True` or `False`).

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**Ek line e:** Python variables are named to indicate their type.

![Board 4: 7:10-9:50](figures_annotated/board_era4_710.jpg)

*Figure 4. The whiteboard during 7:10–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data · 3 Code


**Red Box 1 (Title):** Python Variables
- The title clearly states we are discussing Python variables.

**Blue Box 2 (Data):** Type:
- This box indicates that we need to determine the type of a variable.

**Orange Box 3 (Code):** Iname = "Rafi" Name1 = '1'
- Here, we see two variable assignments: `Iname` and `Name1`.

**Explanation:**
The lecturer explains that when working with variables, it is crucial to understand their types. In the given code snippet, `Iname` is assigned the string `"Rafi"` and `Name1` is assigned the string `'1'`. The lecturer emphasizes that the name of the variable should be meaningful and consistent. He mentions that the name `Iname` is a good choice because it starts with a lowercase letter, adhering to the naming convention where variable names should begin with a small letter. 

The lecturer also points out that using meaningful names helps in understanding the purpose of the variable later. For instance, if someone else reads your code, they can easily infer the type of the variable based on its name. He gives an example where if you assign an integer value to a variable named `num`, it would cause an error because the name does not match the type of the value being assigned. 

He then introduces two rules for naming variables:
1. Start variable names with a small letter.
2. Avoid using spaces in variable names.

**Quotes:**
> Lecturer: "so eta cross, eta holo right away. okay?"
> Lecturer: "par tumi jeta korte paro sheta ki? name 1."

**Mone Rakho:** 
- Variable names should start with a small letter.
- Avoid using spaces in variable names.
- Use meaningful names to indicate the type of the variable.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables
**Ek line e:** Python variables are used to store data.

![Board 5: 10:00-10:50](figures_annotated/board_era5_1000.jpg)

*Figure 5. The whiteboard during 10:00–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table


**Explanation:**
1. **Red Box 1 (Python Variables):** This box introduces the concept of Python variables, which are used to store data.
2. **Blue Box 2 (Definition of Data):** In the context of programming, data refers to any information that can be processed by a computer. Variables are containers that hold this data.
3. **Orange Box 3 (Truth Table):** The truth table in box 3 shows different ways to define a variable named `my_name`. The correct way is `my_name = "Rafi"`.

**Quotes:**
> Lecturer: "but python community te ei snake casing tai khubi standard."

**Mone rakho:** In Python, it's important to follow the naming conventions. For example, if you want to define a variable named `my name`, you should replace the space with an underscore, like `my_name`. This is because Python does not allow spaces in variable names. Additionally, Python follows a convention called snake casing, where words are separated by underscores. For instance, `my_name` is written in snake casing. It's also important to note that Python is case-sensitive, meaning `my_name` and `My_Name` would be considered different variables.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Python Variables
**Ek line e:** Python variables are case-sensitive.

![Board 6: 11:20-12:50](figures_annotated/board_era6_1120.jpg)

*Figure 6. The whiteboard during 11:20–12:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula · 4 Code


**Red Box 1 (Title):** Python Variables

**Blue Box 2 (Definition):** Data Type:

- **Integer:** `age = 10`
- **Boolean:** `is_valid = True` or `False`

**Orange Box 3 (Formula):** `pi = 3.1414`

**Green Box 4 (Code):** `age = 10`

The lecturer explained that variables are case-sensitive. For example, `age` and `Age` are considered different variables. He demonstrated this by showing that both `age = 10` and `age = 10` store an integer value between the same edges. However, if we accidentally write `a, g, e` instead of `age`, it would be treated as three separate variables because they are written in lowercase letters. Therefore, if we mistakenly write `Age` instead of `age`, it would be recognized as a different variable.

**Quote:**

**Mone rakho:** In Python, variables are case-sensitive. We saw that `age` and `Age` are treated as different variables. The data type of `age` is an integer, which can be stored using the assignment operator `=`. We also learned about other data types such as boolean (`True` or `False`) and floating-point numbers (e.g., `pi = 3.1414`). In the next class, we will start learning about arithmetic operations.

---

## Check yourself
1. What is a variable in Python?
2. Give an example of an integer variable in Python.
3. List the four main data types in Python.
4. Why is it important to follow the snake casing convention for variable names in Python?
5. Explain why `age` and `Age` are considered different variables in Python.

### Answers
1. A variable in Python is a container that holds data.
2. Example: `age = 10`
3. Four main data types: String, Integer, Float, Boolean.
4. Following the snake casing convention ensures consistency and readability in code, making it easier to understand the purpose of the variable.
5. In Python, `age` and `Age` are considered different variables because Python is case-sensitive.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 6 kept, 3 removed. References to boxes that do not exist: 0.*
