# Lists, Tuple and Arrays
THE SECTIONS ARE WRITTEN BELOW.

## Key takeaways
- Lists are flexible data structures in Python that allow storing different data types.
- You can access elements using indexing, find the length of a list using `len()`, and update elements.
- Tuples are immutable and cannot be changed once defined.
- Importing numpy allows us to work with arrays efficiently.
- All elements in a numpy array must have the same data type.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**Ek line e:** Lists, Tuple and Arrays

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


### Lists
The red box 1 introduces us to lists, which are flexible data structures in Python. The blue box 2 shows an example of a list named `fruit` containing strings: `["Apple", "Orange", "Mango"]`. The orange box 3 demonstrates a more complex list `elements` that includes different data types: `["Apple", 7, 3.14, True]`.

#### Accessing Elements
The green box 4 illustrates how to access the first element of the list `elements` using indexing: `print(elements[0])`. The purple box 5 shows how to find the length of the list using the `len()` function: `print(len(elements))`. The pink box 6 demonstrates updating the first element of the list: `elements[0] = "Mango"`.

### Understanding Indexing
The lecturer explains that in Python, list indexing starts from zero. For the list `elements`, the first element is at index 0, the second at index 1, and so on. When you print `elements[1]`, it outputs `7`, and when you print `elements[3]`, it outputs `True`.

### Length of a List
The lecturer mentions that the `len()` function returns the total number of elements in the list. For the list `elements`, the length is 4, as shown in the purple box 5.

### Updating a List
The lecturer then updates the first element of the list from `"Apple"` to `"Mango"` using `elements[0] = "Mango"`. When you print `elements[0]` after this update, it outputs `"Mango"`.

### Tuple vs. List
The lecturer transitions to discussing tuples, noting that while lists and tuples are similar, tuples are immutable, meaning their values cannot be changed once defined. The example provided in the pink box 6 shows how to convert a tuple to a list, modify it, and then convert it back to a tuple.

### Summary
**Mone rakho:** Lists are flexible data structures in Python that allow storing different data types. You can access elements using indexing, find the length of a list using `len()`, and update elements. Tuples, on the other hand, are immutable and cannot be changed once defined.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** Lists, Tuple and Arrays

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


**Red Box 1:** Here we have an example of creating a tuple and then converting it into a list to make changes. Let's look at the code:

```python
elements=("Apple", 7, 3.1416, True)
element_list=list(elements)
element_list[2]=5
elements=tuple(element_list)
print(elements)
```

The lecturer explained that we can change the structure of a list by using square brackets. In the code, we see that the value at the second index of `elements` is changed from `3.1416` to `5`.

**Quote:**

**Explanation:**
1. The lecturer started by showing how to change the value of an element in a list. Initially, `elements` is a tuple containing four elements: `"Apple"`, `7`, `3.1416`, and `True`.
2. To change the value, the lecturer converted the tuple to a list using `element_list = list(elements)`. This allowed us to modify the list by changing `element_list[2]` to `5`.
3. After making the change, the list was converted back to a tuple using `elements = tuple(element_list)`.
4. The lecturer mentioned that tuples are immutable, meaning their values cannot be changed directly. Trying to change a tuple would result in an error.
5. To work around this, the lecturer suggested creating a new list, modifying it, and then converting it back to a tuple if needed.

**Mone rakho:** The key points are that tuples are immutable, and to change their values, you need to convert them to lists, make the necessary changes, and then convert them back to tuples.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** Importing numpy allows us to work with arrays efficiently.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


**Explanation:**
1. **Importing Numpy**: We started by importing the `numpy` library using `import numpy as np`. This library provides support for arrays, which are more efficient than Python lists for numerical operations.
2. **Creating a List**: We created a list named `list_1` containing the elements `[7, 8, 9, 10]`.
3. **Converting to Array**: To convert `list_1` into an array, we used `np.array([list_1])`. This operation creates a one-dimensional array from the list.
4. **Handling Mixed Data Types**: Next, we tried to create another list `list_2` with mixed data types: `["Apple", 07, True]`. When attempting to convert this list into an array, we encountered an error because numpy arrays require all elements to have the same data type.

**Quotes:**
> Lecturer: "ekhane amar different value ache. so eijonno ki hobe? eta eror ashbe. eta eror ashbe. eta eror ashbe. eta kaj korbe na."
> 
> Lecturer: "thikache? so amar array hoar jonno list theke jodi ami array convert korte chai, obviously amar shobgular data type same hote hobe."

**Mone Rakho:** The key points are to use numpy for efficient numerical operations, converting lists to arrays, and understanding that all elements in an array must have the same data type.

---

## Check yourself
1. What is the output of `print(elements[1])` for the list `elements = ["Apple", 7, 3.14, True]`?
2. How do you convert a tuple to a list in Python?
3. What happens if you try to convert a list with mixed data types to a numpy array?
4. How do you find the length of a list in Python?
5. What is the difference between a list and a tuple?

### Answers
1. The output is `7`.
2. You convert a tuple to a list using `list(tuple_name)`.
3. It results in an error because numpy arrays require all elements to have the same data type.
4. You find the length of a list using the `len()` function.
5. A list is mutable and can be changed, whereas a tuple is immutable and cannot be changed once defined.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 1 removed. References to boxes that do not exist: 0.*
