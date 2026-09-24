# Lists, Tuple and Arrays
THE SECTIONS COVER LISTS, TUPLES, AND ARRAYS IN PYTHON, INCLUDING THEIR FLEXIBILITY, DATA TYPE ACCOMMODATION, AND CONVERSION TO NUMPY ARRAYS.

## Key takeaways
- Lists are flexible and can store multiple types of data.
- Tuples are similar to lists but are immutable.
- You can convert lists to NumPy arrays but all elements must be of the same data type.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**Ek line e:** Lists, tuples, and arrays are fundamental data structures in Python.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


- **Red Box 1 (Lists, Tuple and Arrays):** The lecturer introduces the topic of lists, tuples, and arrays, explaining that arrays are essentially lists of arrays but cannot be imported directly.

- **Blue Box 2 (List: fruit = ["Apple", "Orange", "Mango"]):** The lecturer demonstrates a list named `fruit` containing strings. He explains that lists are flexible and can store multiple types of data.

- **Orange Box 3 (List: elements = ["Apple", 7, 3.14, 2/3]):** The lecturer creates a list named `elements` that includes a mix of data types: a string, an integer, a float, and a fraction. He emphasizes the flexibility of lists in accommodating various data types.

- **Green Box 4 (Code: print(elements[0])):** The lecturer shows how to access the first element of the list using indexing. He prints `"Apple"` to demonstrate that the first element is indexed as `0`.

- **Purple Box 5 (Code: print(len(elements))):** The lecturer explains that the `len()` function returns the length of the list. He prints `4`, indicating that the list contains four elements.

- **Pink Box 6 (Code: elements[0] = "Mango"):** The lecturer demonstrates how to modify the first element of the list. He changes the first element from `"Apple"` to `"Mango"` and prints the updated list to show the change.

> Lecturer: "Python and Lister are the most advantage of the different data types."

### Extra jana kotha
Lists in Python are highly flexible and can store any type of data. They are indexed starting from `0`, allowing easy access to individual elements. Tuples, on the other hand, are similar to lists but are immutable, meaning their elements cannot be changed after creation.

<!-- boxes: 1=#d62828 -->
## Box 1 (Red): Code Example
**Ek line e:** Lists, Tuple and Arrays Elements=("Apple", 7, 3.1416, True) element_list=list(elements) element_list[2]=5 elements=tuple(element_list) print(elements)

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The lecturer starts by showing us an example of lists, tuples, and arrays. He defines a tuple `Elements` containing four elements: `"Apple"`, `7`, `3.1416`, and `True`. 

1. **Step 1:** The lecturer converts the tuple `Elements` into a list using the `list()` function. This changes the tuple into a mutable list named `element_list`.
2. **Step 2:** Next, he modifies the third element (index 2) of the list `element_list` by setting it to `5`. This demonstrates how we can change the elements of a list.
3. **Step 3:** After modifying the list, the lecturer converts it back into a tuple using the `tuple()` function. The new tuple is stored in the variable `elements`.

The lecturer explains that tuples are immutable, meaning their elements cannot be changed directly. However, since we converted the tuple to a list, we were able to modify it. Once modified, we converted it back to a tuple.


### Extra jana kotha (lecture e bola hoy ni)
When working with tuples, remember that they are immutable, which means you cannot change their elements directly. To modify a tuple, you need to convert it to a list, make the necessary changes, and then convert it back to a tuple if needed. This flexibility allows you to manipulate the data while maintaining the benefits of immutability in other parts of your program.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays

**Ek line e:** In this section, we learned about lists, tuples, and arrays, and how to convert lists into arrays using NumPy.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


- **Box 1 (red)**: The lecturer started by showing a code example where a list was converted into a NumPy array. The code is as follows:

```python
import numpy as np
list_1 = [7, 8, 9, 10]
list_1 = np.array([list_1])
list_2 = ['Apple', 07, True]
```

- **Step-by-step explanation**: 
  - First, the lecturer imported the NumPy library using `import numpy as np`.
  - Then, a list named `list_1` was created with elements `[7, 8, 9, 10]`.
  - The lecturer then converted `list_1` into a NumPy array using `np.array([list_1])`. Note that the outer brackets were changed to match the NumPy array format.
  - Next, a list named `list_2` was created with mixed data types: `['Apple', 07, True]`.

- **Explanation of the conversion**: 
  - The lecturer explained that when converting a list into a NumPy array, all elements in the list must be of the same data type. For example, `list_1` was successfully converted because all elements were integers.
  - However, `list_2` could not be converted directly into an array because it contained different data types (`'Apple'`, `07`, and `True`).

- **Error handling**: 
  - The lecturer mentioned that if the list contains different data types, attempting to convert it into an array will result in an error. To avoid this, ensure that all elements in the list are of the same type before conversion.

- **Quote**:
  > "So, if we have the array to convert the list, obviously, our data types are the same. If we were to see this, we will see the class."

- **Extra jana kotha**: When converting a list into a NumPy array, make sure all elements are of the same data type to avoid errors. For example, if your list contains both strings and integers, you need to convert all elements to the same type before conversion.

---

## Check yourself
1. What is the output of `print(fruit[1])` if `fruit = ["Apple", "Orange", "Mango"]`?
2. How do you find the length of a list in Python?
3. What happens if you try to convert a list with mixed data types to a NumPy array?
4. How can you modify the first element of a list named `elements`?
5. What is the difference between lists and tuples?

### Answers
1. The output is `"Orange"`.
2. You use the `len()` function, e.g., `print(len(elements))`.
3. It will result in an error because NumPy arrays require all elements to be of the same data type.
4. You can modify the first element using indexing, e.g., `elements[0] = "Mango"`.
5. Lists are mutable and can store different data types, whereas tuples are immutable and cannot be changed once created.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
