# Lists, Tuple and Arrays
The sections cover lists, tuples, and arrays in Python, including how to create, access, modify, and convert them.

## Key takeaways
- Lists are flexible data types that can store different types of data.
- Tuples are immutable and can be converted to lists for modification.
- Arrays require the NumPy library and must have elements of the same data type.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**In one line:** Lists, tuples, and arrays are fundamental data structures in Python.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


1. **Red Box 1 (Lists, Tuple and Arrays):**
   - Lists are very flexible data types in Python. They allow you to store different types of data in a single variable.
   - For example, we define a list `fruit` with strings: `fruit = ["Apple", "Orange", "Mango"]`.

2. **Blue Box 2 (List):**
   - We can also include different types of data in a list. For instance, `elements = ["Apple", 7, 3.14, True]`.
   - Here, `elements` contains a string, an integer, a float, and a boolean.

3. **Green Box 4 (Code):**
   - To access the first element of the list, we use indexing. For example, `print(elements[0])` prints `"Apple"`.

4. **Purple Box 5 (Code):**
   - To find the length of the list, we use the `len()` function: `print(len(elements))`. This will output `4`, as there are four elements in the list.

5. **Pink Box 6 (Code):**
   - We can modify the list by changing an element. For example, `elements[0] = "Mango"` changes the first element from `"Apple"` to `"Mango"`.
   - After updating the list, printing `elements[0]` again will output `"Mango"`.


### Background (not said in the lecture)
Lists in Python are very versatile. You can store different types of data like strings, integers, floats, and booleans in a single list. This flexibility makes lists a powerful tool for handling various types of data. Additionally, you can easily modify lists by changing individual elements, making them dynamic and adaptable.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**In one line:** Lists, Tuple and Arrays

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1:** The code initializes a `elements` tuple with four values: `"Apple"`, `7`, `3.1416`, and `True`. Then, it converts this tuple into a list named `element_list` using the `list()` function. Next, it changes the value at the second index of `element_list` from `3.1416` to `5`.

2. **Red Box 1 (continued):** After changing the value, the code converts `element_list` back into a tuple named `elements` using the `tuple()` function. Finally, it prints the updated tuple.


### Background (not said in the lecture)
When you need to modify a tuple, you can't directly change its elements because tuples are immutable. Instead, you should convert the tuple to a list, make the necessary changes, and then convert it back to a tuple. This approach allows you to modify the elements while maintaining the immutability property of tuples. Understanding these concepts will help you work effectively with both lists and tuples in Python.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**In one line:** In this section, we will learn about converting lists to arrays using NumPy.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The lecturer started by importing the NumPy library, which is essential for working with arrays in Python. He explained that while Python has built-in support for lists, arrays require an external library like NumPy.

1. **Red Box 1**: The lecturer wrote `import numpy as np` on the board. This line imports the NumPy library under the alias `np`, making it easier to use NumPy functions.

2. **Creating a List**: Next, he created a list named `list_1` containing integers: `list_1 = [7, 8, 9, 10]`. He then converted this list into an array using `np.array([list_1])`.

3. **Creating Another List**: He also created another list named `list_2` containing a mix of different data types: `list_2 = ['Apple', 07, True]`.

4. **Converting List to Array**: The lecturer then demonstrated how to convert `list_1` into an array using `np.array([list_1])`. He explained that this conversion is straightforward when all elements in the list have the same data type.

5. **Error Handling**: He pointed out that if the list contains different data types, such as `list_2`, attempting to convert it directly to an array would result in an error. This is because NumPy requires all elements in an array to be of the same data type.


### Background (not said in the lecture) (lecture e bola hoy ni)
When converting a list to an array, ensure all elements are of the same data type. Otherwise, you will encounter errors. For example, if your list contains both strings and integers, you cannot directly convert it to an array without first ensuring all elements are of the same type.

---

## Check yourself
1. What is the output of `print(elements[0])` after setting `elements = ["Apple", 7, 3.14, True]`?
2. How do you convert a tuple to a list in Python?
3. What is the output of `print(len(elements))` after setting `elements = ["Apple", 7, 3.14, True]`?
4. How do you modify the first element of a list named `elements`?
5. Why can't you directly convert a tuple with mixed data types to an array?

### Answers
1. The output is `"Apple"`.
2. You convert a tuple to a list using the `list()` function, e.g., `list_tuple = list(tuple_name)`.
3. The output is `4`.
4. You modify the first element of a list by assigning a new value to the first index, e.g., `elements[0] = "Mango"`.
5. You can't directly convert a tuple with mixed data types to an array because NumPy requires all elements to be of the same data type.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
