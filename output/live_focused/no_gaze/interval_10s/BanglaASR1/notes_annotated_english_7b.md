# Python Variables
This lecture covers the basics of Python variables, including their introduction, definition, data types, naming conventions, and importance.

## Key takeaways
- A variable is a container that holds data which can be manipulated and accessed throughout the program.
- Python variables are dynamically typed, meaning the type of data is determined based on the context.
- Understanding different data types (string, integer, float, boolean) is crucial for effective programming.
- Proper naming conventions (snake_case and camelCase) improve code readability and maintainability.
- Python is case-sensitive, so variable names must be used consistently.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to Python Variables
**In one line:** A variable is a container that holds data which can be manipulated and accessed throughout the program.

![Board 1: 0:00-1:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–1:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


### Explanation
1. **Introduction to Variables**: The lecturer begins by explaining that variables are fundamental in programming, especially in Python. They emphasize that understanding variables is crucial for grasping more complex concepts.
   
2. **Definition of a Variable**: The lecturer uses an analogy to define a variable. They ask the students to imagine a box and then place different items inside it. For instance, placing a book in the box represents storing data in a variable. This helps illustrate that a variable is a container where data can be stored and manipulated.

3. **Example with Fruits**: To further clarify, the lecturer draws a box and places an apple inside it. They explain that the box itself is the variable, and the apple is the data stored within it. This example reinforces the idea that a variable can hold various types of data, such as numbers, strings, or even objects.

4. **Box Removal**: The lecturer then removes the example from the board to focus on the concept of a variable. They reiterate that in Python, just like in other programming languages, a variable must have a specific type assigned to it when data is stored. For example, if a variable is intended to hold an integer, it should be declared as such.

**Quote**
> "so toh jodi data store korte jano, every other things will be very easy to you."  
> (In English: so if you want to store data, everything else will be much easier for you.)

**Remember:** Understanding variables is essential because they allow programmers to store and manipulate data effectively in their programs.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Understanding Python Variables
**In one line:** This section explains how to define and assign integer values to variables in Python.

![Board 2: 1:50-3:20](figures_annotated/board_era2_150.jpg)

*Figure 2. The whiteboard during 1:50–3:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition


### Explanation
1. **Definition of Python Variables**: Look at the blue box 2, which shows `int (num) = 10` and `num = 10`. Here, `num` is a variable that holds an integer value of 10.
   
2. **Type Declaration**: The lecturer explains that while we can simply write `num = 10`, Python needs to know the type of data stored in the variable. In this case, `int` indicates that `num` will hold an integer value.
   
3. **Dynamic Typing**: Python is dynamically typed, meaning it determines the type of data based on the context. When you assign a value to `num`, Python understands that it is an integer and stores it accordingly. Later, when you use `num`, you can perform operations like addition, subtraction, etc., because Python recognizes it as an integer.

4. **Comparison with Other Types**: The lecturer uses the example of `num` to compare it with a hypothetical box. Just as a box can hold a specific value, `num` can hold a specific integer value, which is 10 in this case.

**Quotes**
> Lecturer: "amra shudhu ekhane num likhe amra value ta boshay dite pari. python nije nije bujhe jabe je e value ta asho likhi."
> (In English: "we just write `num` and assign a value to it. Python will understand that this is the value we are assigning.")

**Remember:** Python variables are dynamically typed, allowing you to perform various operations on them based on their assigned values.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to Python Variables and Their Data Types
**In one line:** This board introduces the basic data types in Python: string, integer, float, and boolean.

![Board 3: 3:40-7:00](figures_annotated/board_era3_340.jpg)

*Figure 3. The whiteboard during 3:40–7:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data Type


### Explanation
1. **Data Types in Python**: The board lists four main data types in Python: string, integer, float, and boolean. Each data type is represented by a variable example.
2. **String**: A string is a sequence of characters enclosed in single or double quotes. For example, `Fruit = 'Apple'` or `Fruit = "Apple"`. Strings can represent any text, such as names or sentences.
3. **Integer**: An integer is a whole number, positive or negative, without decimals. For example, `Age = 10`.
4. **Float**: A float is a number with a decimal point. For example, `Float = 3.5`.
5. **Boolean**: A boolean represents one of two values: `True` or `False`. For example, `True` or `False`.

**Quotes**
> Lecturer: "string holo je konor jinis je mon dhoro boli je jodi boli je amar nam obuk, amar nam tomo. amar nam dhoro je amar nam holo ahasan. thik ache? toh amra ki likhte pari? string ar moddhe je kono jinis en name."
> (In English: "A string is like any kind of thing we say, like my name, which is Ahasan. Can we write it? In a string, we put any kind of name.")

**Remember:** Understanding the different data types in Python is crucial for effective programming.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Understanding Python Variable Names and Their Importance
**In one line:** Proper naming conventions for variables are crucial for readability and maintainability.

![Board 4: 7:10-9:50](figures_annotated/board_era4_710.jpg)

*Figure 4. The whiteboard during 7:10–9:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Data · 3 Code


### Python Variables
- **Data Type:** The type of a variable determines how the data is stored and manipulated. It's important to understand the type of each variable you declare.

### Code Example
- **Box 3 (Orange):** `Iname = "Rafi"` - This is an example of a string variable named `Iname`.
- **Box 2 (Blue):** `Name` - This is another variable, but its type is not specified here.
- **Box 1 (Red):** `Python Variables` - This is the title of the section.

The lecturer explained that when you see code like `Iname = "Rafi"` and `Name1 = '1'`, it's important to understand that `Iname` is a string (`str`) and `Name1` is a numeric string. The naming of variables is critical because it helps others (and yourself) understand the purpose of the variable quickly.

### Naming Conventions
1. **First Rule:** Always use lowercase letters for variable names. For example, `name` instead of `Name`. This makes the code more readable and consistent.
2. **Second Rule:** Avoid using spaces in variable names. Instead, use underscores or camelCase. For instance, `name1` or `name_one`.

The lecturer emphasized that if you use an integer value where a string is expected, such as `name = 1`, it will result in an error. This is because `name` is expected to be a string, not an integer. For example, if you try to assign an integer to a string variable, you'll get a direct error.

**Remember:** Proper naming conventions make your code easier to read and maintain. Always follow standard naming practices to ensure clarity and avoid confusion.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Python Variables and Naming Conventions
**In one line:** This board explains the importance of proper naming conventions for Python variables, including snake_case and camelCase.

![Board 5: 10:00-10:50](figures_annotated/board_era5_1000.jpg)

*Figure 5. The whiteboard during 10:00–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Truth table


### Explanation
1. **Box 1 (Red):** The title "Python Variables" sets the context for the discussion.
2. **Box 2 (Blue):** The definition "Data" is crucial as variables store data in Python.
3. **Box 3 (Orange):** The truth table shows valid and invalid variable names:
   - `lname = "Rafi"` (X) - Invalid because it contains a space.
   - `name1="Rafi"` (✓) - Valid because it uses an underscore instead of a space.
   - `my_name = "Rafi"` - Valid, using an underscore.
   - `myNam` - Invalid because it starts with a capital letter.

The lecturer explained why we use underscores instead of spaces in variable names. He stated, "jemon, tumi jodi chau, tumi my name equal roughi. eta tumi likhte parbana. eta likhte parbana karon ki? amar ekhane space ache. toh amra space ta ke kivabi tick korbo? amra korbo ki? amra ekhane ekta underscore diye diite parbo. underscore jodi diye di, eta ke python community te polle holo space ta ke kivabe tick korbo?" (In English: "If you want to write my name equals 'Rafi', you can do it. But why do we use an underscore instead of a space? Because there is a space here. Should we tick the space? We should not. Instead, we use an underscore. Underscore is commonly used in the Python community to replace spaces.")

Additionally, the lecturer introduced camelCase and snake_case naming conventions:
- **Camel Case:** The first word is lowercase, and subsequent words begin with a capital letter. For example, `myVariableName`.
- **Snake Case:** Words are separated by underscores. For example, `my_variable_name`.

The lecturer emphasized that while camelCase is also used, snake_case is the preferred convention in the Python community. He noted, "ar ekta ache shetakolo camel casing. sheta ki? shetakolo dekhoro ami ekhane first er ta small letter e dear kore, sorry. first er ta small letter e dear kore, ami poroborti jotogula word ar shbe shobgula capital letter diye shuru korbo. dekho. camel er jerokom ki? kono ekta jeta or pit ta kichu ucho hoy. similarly, ekhane amar variable er name ta urokom bhabe dekho." (In English: "There is another style called camelCase. Let me show you. Here, the first letter is lowercase, and then each subsequent word starts with a capital letter. Similarly, look at how our variable name changes.")

Finally, the lecturer highlighted the importance of case-sensitivity in Python, stating, "evabe giheche, ototek tu tuhe chabar neicho hoyeche. eta amra boli holo aa variable er camel casing. but python community te ei snake casing tai khubi standard. etai follow kore shobai. arekta important jini sholo python kintu case-sensitive, sheta khub important ekta jini shenish, ebog maximum khetre jeta developer ache, tara actively kore. dekhajata je variable er nam hotat kore tater match korteche na." (In English: "So, you have understood that this is the camelCase for a variable. But in the Python community, snake_case is the standard. Everyone follows this. Another important thing about Python is that it is case-sensitive, which is very important. When developers work, they need to be active and ensure that the variable names match exactly.")

**Remember:** Always use snake_case for variable names in Python to maintain consistency and adhere to the community standards.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Python Variables and Data Types
**In one line:** This board explains the concept of Python variables, their naming conventions, and different data types.

![Board 6: 11:20-12:50](figures_annotated/board_era6_1120.jpg)

*Figure 6. The whiteboard during 11:20–12:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Definition · 3 Formula · 4 Code


### Explanation
1. **Case Sensitivity**: The lecturer emphasized that Python is case-sensitive. For instance, `age` and `Age` are considered different variables. He demonstrated this by showing that `age = 10` and `age = 10` both store an integer value, but if you accidentally write `Age = 10`, it will be treated as a different variable.
   
2. **Variable Naming**: The lecturer explained that a variable is essentially a name for storing data. In the example provided, `age = 10` stores the integer value 10. He then showed `age = 10` again to reinforce the point that the same variable can be assigned the same value multiple times.

3. **Data Types**: The lecturer introduced the concept of data types in Python. He mentioned that we have several data types including string, integer, boolean, and float. To illustrate a float, he used the example `pi = 3.1414`. He noted that `pi` is a floating-point number and is not a whole number.

4. **Boolean Example**: The lecturer also provided an example of a boolean value using `is_valid = True`. He explained that boolean values can be either `True` or `False`. For instance, if a condition is met, the value would be `True`; otherwise, it would be `False`.

**Quote:**
> "aithan holo case-sensitive."  
> (In English: "Python is case-sensitive.")

**Remember:** Understanding case sensitivity and different data types is crucial for correctly defining and using variables in Python.

---

## Check yourself
1. What is a variable in Python?
2. How do you define a variable in Python?
3. List the four main data types in Python.
4. Explain the difference between snake_case and camelCase naming conventions.
5. Why is Python case-sensitive?

### Answers
1. A variable in Python is a container that holds data which can be manipulated and accessed throughout the program.
2. You define a variable in Python by assigning a value to it, e.g., `variable_name = value`.
3. The four main data types in Python are string, integer, float, and boolean.
4. Snake_case uses underscores to separate words (e.g., `my_variable_name`), while camelCase starts each word after the first with a capital letter (e.g., `myVariableName`).
5. Python is case-sensitive, meaning that `variable_name` and `VariableName` are considered different variables.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
