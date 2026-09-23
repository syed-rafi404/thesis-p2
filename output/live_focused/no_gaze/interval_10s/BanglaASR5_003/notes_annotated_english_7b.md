# Lists, Tuple and Arrays
This lecture covers the basics of lists, tuples, and arrays in Python, including how to create, manipulate, and convert between these data structures.

## Key takeaways
- Lists are flexible data types in Python that can store different types of data and can be manipulated using indexing and updating.
- Tuples are immutable and can be converted to lists for modification, then back to tuples.
- NumPy arrays can be created from lists, providing efficient numerical computation capabilities.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**In one line:** This board introduces lists in Python, their flexibility, and how to manipulate them using indexing and updating.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


1. **Lists**: The lecturer introduced lists as a flexible data type in Python, similar to arrays but more versatile. Lists can store different types of data, such as strings, integers, floats, and booleans. For example, `fruit = ["Apple", "Orange", "Mango"]` creates a list of fruits.
2. **Creating a List**: The lecturer demonstrated creating a list with multiple elements of different types. In the example, `elements = ["Apple", 7, 3.14, True]`, the list contains a string, an integer, a float, and a boolean.
3. **Accessing Elements**: The lecturer explained how to access elements in a list using indexing. For instance, `print(elements[0])` prints the first element of the list, which is `"Apple"`.
4. **Length of a List**: The lecturer showed how to find the length of a list using the `len()` function. The code `print(len(elements))` outputs the number of elements in the list, which is `4` in this case.
5. **Updating Elements**: The lecturer demonstrated updating an element in the list. The code `elements[0] = "Mango"` changes the first element from `"Apple"` to `"Mango"`. When the updated list is printed again, it reflects the change.

> The lecturer said: "so dhoro amra first class e ekta variable ney shilam fruit. fruit er moddhe amra ki diye shilam? apple diye shilam. but fruit ki shudu appali? aro onek jinis toh hote pari. ami o fruit hisate aro onek jinis rakhte pari. orange rakhte pari, mango rakhte pari."

### Background
Lists in Python are dynamic and can hold a collection of items, which can be of different data types. They are widely used in programming for storing and manipulating collections of data efficiently. Lists provide flexibility in terms of adding, removing, and accessing elements, making them a fundamental data structure in Python.

**Remember:** Understanding how to create, access, and update elements in a list is crucial for effective data manipulation in Python.

<!-- boxes: 1=#d62828 -->
## Converting Tuples to Lists and Back to Tuples
**In one line:** This section demonstrates how to modify elements in a tuple by converting it to a list, making changes, and then converting it back to a tuple.

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Understanding the Code:**
   - **Box 1 (Red):** The code starts with defining a tuple `elements=("Apple", 7, 3.1416, True)`. The lecturer said: "Let's change an element in a structured way. Here, I'm using square brackets to access the first element."
   - **Line 2:** `element_list = list(elements)` converts the tuple into a list. The lecturer explained: "We need to create a new variable because tuples are immutable. We can't directly change their elements."
   - **Line 3:** `element_list[2] = 5` changes the third element (index 2) of the list to 5. The lecturer noted: "We can change the value at index 2 to 5."
   - **Line 4:** `elements = tuple(element_list)` converts the modified list back into a tuple.
   - **Line 5:** `print(elements)` prints the updated tuple.

2. **Explanation:**
   - The lecturer emphasized that tuples are immutable, meaning their elements cannot be changed once defined. If we try to change an element, Python will throw an error.
   - To work around this, the lecturer suggested creating a new list from the tuple, modifying the list, and then converting it back to a tuple. This allows us to make changes while maintaining the immutability of the original tuple.

3. **Why This Matters:**
   - Tuples are often used when you want to ensure that the data remains constant. However, there might be situations where you need to modify the data temporarily. By converting to a list, making the necessary changes, and then converting back to a tuple, you can achieve this flexibility.

**Remember:** The key takeaway is that tuples are immutable, but you can modify them by first converting them to lists, making the changes, and then converting them back to tuples.

<!-- boxes: 1=#d62828 -->
## Converting Lists to Arrays Using NumPy
**In one line:** This section explains how to convert lists to arrays using the NumPy library in Python.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Importing NumPy**: First, we need to import the NumPy library. The code `import numpy as np` is used to import NumPy and alias it as `np`. This allows us to use NumPy functions easily.

2. **Creating a List**: Next, we create a list called `list_1` which contains the elements `[7, 8, 9, 10]`. This is shown in the red box 1.

3. **Converting List to Array**: To convert this list to an array, we use the `np.array()` function. The code `list_1 = np.array([list_1])` converts `list_1` into an array. Notice that we pass the list inside another list to ensure it is treated as a single element when creating the array.

4. **Another List**: We also define another list called `list_2` which contains the elements `["Apple", 07, True]`. This list includes a string, an integer, and a boolean, demonstrating that not all elements in a list need to be of the same type.

The lecturer said: "we can perform calculations even within errors, the advantage is that we can quickly perform operations on the array."

### Background
NumPy is a powerful library in Python used for numerical computations. Arrays created using NumPy are more efficient and faster for mathematical operations compared to regular Python lists. When converting a list to an array, all elements must be of the same data type, otherwise, an error will occur. This is why the second list `list_2` cannot be directly converted to an array.

**Remember:** When converting a list to an array using NumPy, ensure all elements are of the same data type to avoid errors.

---

## Check yourself
1. What is a list in Python?
2. How do you create a list with different types of elements?
3. Explain how to access an element in a list using indexing.
4. How do you convert a tuple to a list and then back to a tuple?
5. What is the purpose of converting a list to a NumPy array?

### Answers
1. A list in Python is a flexible data type that can store different types of data, such as strings, integers, floats, and booleans.
2. You create a list with different types of elements by enclosing the elements in square brackets, separated by commas, like `elements = ["Apple", 7, 3.14, True]`.
3. You access an element in a list using indexing, for example, `print(elements[0])` prints the first element of the list.
4. To convert a tuple to a list, you use `element_list = list(elements)`, then convert it back to a tuple with `elements = tuple(element_list)`.
5. The purpose of converting a list to a NumPy array is to enable efficient numerical computations and operations.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
