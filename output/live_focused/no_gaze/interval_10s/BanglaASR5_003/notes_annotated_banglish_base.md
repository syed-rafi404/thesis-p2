# Lists, Tuple and Arrays
THE SECTIONS COVER THE DIFFERENCES BETWEEN LISTS, TUPLES, AND ARRAYS IN PYTHON, INCLUDING HOW TO MANIPULATE THEM AND WORK WITH NUMPY ARRAYS FOR FASTER OPERATIONS.

## Key takeaways
- Lists are versatile and flexible data types in Python that can hold multiple items of different data types.
- Tuples are immutable and are used when you want to ensure that the data does not change.
- Numpy arrays provide faster operations but require all elements to be of the same data type.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**Ek line e:** Lists, tuple, and arrays are fundamental data structures in Python.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


- **Red Box 1 (Lists, Tuple and Arrays):** The title of the board introduces us to the concepts of lists, tuples, and arrays. Lists are a versatile and flexible data type in Python.

- **Blue Box 2 (List: fruit = ["Apple", "Orange", "Mango]):** The lecturer demonstrates a list named `fruit` containing strings. He explains that lists allow you to store multiple items in a single variable.

- **Orange Box 3 (List: elements = ["Apple", 7, 3.14, 2/3]):** The lecturer then creates a more complex list named `elements` that includes different data types such as strings, integers, floats, and fractions. He emphasizes the flexibility of lists in accommodating various types of data.

- **Green Box 4 (Code: print(elements[0])):** The lecturer shows how to access the first element of the list using indexing. He prints the first element, which is `"Apple"`.

- **Purple Box 5 (Code: print(len(elements))):** Next, he demonstrates how to find the length of the list using the `len()` function, which returns the number of elements in the list. Here, the length is `4`.

- **Pink Box 6 (Code: elements[0] = "Mango"):** Finally, the lecturer changes the first element of the list from `"Apple"` to `"Mango"` and prints the updated first element to show the flexibility of lists.

> Lecturer: "Python and Lister are the most advantage of the different data types."

### Extra jana kotha (lecture e bola hoy ni)
Lists in Python are very flexible and can hold different types of data. They are indexed starting from 0, meaning the first element is at index 0, the second at index 1, and so on. This flexibility allows you to easily modify and manipulate the elements within a list.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** We are working with lists, tuples, and arrays.

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The board shows us how to manipulate data structures in Python. Let's break down the steps:

1. **Box 1 (Red):** The initial elements are defined as a tuple: `elements=("Apple", 7, 3.1416, True)`. This tuple contains four elements: a string, an integer, a float, and a boolean.
2. **Step 2:** We convert the tuple to a list using the `list()` function: `element_list=list(elements)`. Now, `element_list` is a mutable list containing the same elements as the tuple.
3. **Step 3:** We modify the third element (index 2) of the list: `element_list[2]=5`. This changes the float value `3.1416` to `5`.
4. **Step 4:** We convert the modified list back to a tuple: `elements=tuple(element_list)`. Now, `elements` is a new tuple with the updated value.
5. **Step 5:** Finally, we print the new tuple: `print(elements)`.

> Lecturer: "We have to change the structure. We have to change the square bracket and give the first bracket."

The lecturer explains that since tuples are immutable, we cannot directly change their elements. Instead, we convert the tuple to a list, make the necessary changes, and then convert it back to a tuple.

### Extra jana kotha (lecture e bola hoy ni)
Understanding the difference between mutable and immutable data structures is crucial. Lists are mutable, meaning you can change their elements after creation, while tuples are immutable, and you cannot change their elements once they are created. This distinction helps in choosing the right data structure based on the requirements of your program.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** We can use numpy arrays for faster operations on lists.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The lecturer starts by importing the numpy library using `import numpy as np`. This allows us to work with arrays more efficiently. He then defines a list `list_1` containing the numbers 7, 8, 9, and 10. Next, he converts this list into a numpy array using `list_1 = np.array([list_1])`.

- **Box 1 (red):** The code `import numpy as np` is used to import the numpy library. Then, `list_1 = [7, 8, 9, 10]` creates a list with four elements. The line `list_1 = np.array([list_1])` converts this list into a numpy array.

The lecturer then defines another list `list_2` containing 'Apple', 07, and True. However, he points out that converting `list_2` directly into a numpy array would result in an error because the elements in `list_2` are of different data types (string, integer, and boolean).

- **Box 1 (red):** The code `list_2 = ['Apple', 07, True]` shows the definition of `list_2`.

The lecturer explains that since the data types in `list_2` are not consistent, attempting to convert it directly into a numpy array would lead to an error. He emphasizes that all elements in a numpy array must be of the same data type.

> Lecturer: "So, if we have the array to convert the list, obviously, our data types are the same."

### Extra jana kotha (lecture e bola hoy ni)
When working with numpy arrays, it's crucial to ensure that all elements are of the same data type. This consistency allows for efficient and error-free operations. If your list contains elements of different types, you might need to preprocess the list to convert all elements to a compatible type before creating a numpy array.

---

## Check yourself
1. What is the output of `print(fruit[0])` if `fruit = ["Apple", "Orange", "Mango"]`?
2. How do you find the length of a list in Python?
3. What happens if you try to change an element in a tuple?
4. How do you convert a tuple to a list in Python?
5. Why do numpy arrays require all elements to be of the same data type?

### Answers
1. The output is `"Apple"`.
2. You use the `len()` function, e.g., `len(fruit)`.
3. You cannot change an element in a tuple directly; you need to convert it to a list first.
4. You use the `list()` function, e.g., `list_tuple = list(my_tuple)`.
5. Numpy arrays require all elements to be of the same data type to ensure efficient operations.

---


*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
