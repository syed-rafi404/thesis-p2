# Lists, Tuples, and Arrays
This lecture covers the introduction to lists, tuples, and arrays, including how to access and modify list elements, converting between lists and tuples, and using NumPy to convert lists into arrays.

## Key takeaways
- Lists in Python are flexible and can hold multiple types of data.
- Tuples are immutable, meaning their elements cannot be changed once defined.
- NumPy arrays provide more functionality and efficiency compared to Python lists, especially when dealing with numerical data.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Introduction to Lists, Tuples, and Arrays
**In one line:** This board introduces lists, their flexibility, and the basics of accessing and modifying list elements.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


### Explanation
1. **Introduction to Lists**
   - The red box titled "Lists, Tuple and Arrays" introduces the concept of lists in Python. Lists are flexible data structures that can hold multiple types of data.
   - The blue box shows an example of a list named `fruit` containing strings: `["Apple", "Orange", "Mango"]`.
   - The orange box demonstrates a more complex list named `elements` containing various data types: `["Apple", 7, 3.14, True]`.

2. **Accessing List Elements**
   - The green box contains the code `print(elements[0])`, which prints the first element of the `elements` list, which is `"Apple"`.
   - The purple box contains the code `print(len(elements))`, which prints the length of the `elements` list, which is `4`.
   - The pink box contains the code `elements[0] = "Mango"`, which changes the first element of the `elements` list from `"Apple"` to `"Mango"`.

3. **Quotes**
   > Lecturer: "so dhoro amra first class e ekta variable ney shilam fruit. fruit er moddhe amra ki diye shilam? apple diye shilam. but fruit ki shudu appali? aro onek jinis toh hote pari. ami o fruit hisate aro onek jinis rakhte pari. orange rakhte pari, mango rakhte pari."
   > (In English: "let's say we have a variable called 'fruit'. What do we put in it? We put 'apple'. But can 'fruit' be just an apple? Other things can also be included. We can include other fruits like 'orange' and 'mango'.")

### Remember
The single most important point of this board is that lists in Python are flexible and can hold multiple types of data, making them very versatile for storing and manipulating collections of items.

<!-- boxes: 1=#d62828 -->
## Converting Between Lists and Tuples
**In one line:** This section explains how to modify elements in a tuple by converting it to a list, then back to a tuple.

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The board shows the following code:

```python
elements=("Apple", 7, 3.1416, True)
element_list=list(elements)
element_list[2]=5
elements=tuple(element_list)
print(elements)
```

1. **Understanding the Code**: The lecturer starts with a tuple `elements` containing four elements: `"Apple"`, `7`, `3.1416`, and `True`. He then converts this tuple into a list called `element_list` using the `list()` function. Next, he changes the third element (index 2) of `element_list` from `3.1416` to `5`. Finally, he converts `element_list` back into a tuple and prints the result.

2. **Mutable vs Immutable**: The lecturer points out an important restriction: tuples are immutable, meaning their elements cannot be changed once defined. If you try to change an element in a tuple, Python will raise an error. For example, if you attempt to change `3.1416` to `5` directly in the tuple, it won't work.

3. **Solution**: To overcome this restriction, the lecturer suggests creating a new list from the tuple. He creates a new variable `element_list` and converts the tuple into a list. Now, he can modify the elements in `element_list` freely. After making the necessary changes, he converts `element_list` back into a tuple.

4. **Example**: The lecturer demonstrates that after changing the third element to `5`, the final output is a tuple with the updated value: `(Apple, 7, 5, True)`.

5. **Arrays**: The lecturer concludes by mentioning that in other programming languages, a list is often referred to as an array. However, Python's lists allow for more flexibility, such as easily changing the length and storing different data types.

> Lecturer: "thali ekta ki change-er cholo? structure-ly."  
> (In English: "Let's change the structure.")

**Remember:** Always convert a tuple to a list if you need to modify its elements, and then convert it back to a tuple when needed.

<!-- boxes: 1=#d62828 -->
## Converting Lists to Arrays Using NumPy
**In one line:** We use NumPy to convert lists into arrays, ensuring all elements have the same data type.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The lecture starts by explaining the importance of using arrays over lists, particularly when dealing with errors. Arrays allow for efficient calculations and handling of data in a structured manner. To demonstrate, the lecturer imports the NumPy library, which is essential for working with arrays in Python.

1. **Importing NumPy**: The lecturer writes `import numpy as np` on the board. This line imports the NumPy library, which provides support for arrays and other numerical operations.

2. **Creating a List**: Next, the lecturer creates a list named `list_1` containing integers: `list_1 = [7, 8, 9, 10]`. This list is then converted into an array using `np.array([list_1])`.

3. **Creating Another List**: The lecturer also creates another list named `list_2` containing mixed data types: `list_2 = ['Apple', 07, True]`.

> Lecturer: "ami jokhon lektesi import num by snp, toh mane ki? erpor amar jokhoni num by ke dor kare hobe."  
> (In English: "When I say import num by snp, what does that mean? Essentially, we need to import the num library.")

The lecturer explains that while Python has built-in lists, NumPy arrays offer more functionality and efficiency. By converting a list to an array, operations can be performed much faster. However, it's important to ensure that all elements in the list have the same data type before conversion.

> Lecturer: "so, ekhane dhoro amader jeta amader list, tai na? eta jodi kom list, eta okintu list. so, i can't just convert list2 into an array, because ekhane dakho amar different type-e data ache."  
> (In English: "so, here we have our list, right? If it's a complex list, it's still a list. So, I can't just convert list2 into an array because here we see different types of data.")

The lecturer points out that attempting to convert `list_2` into an array would result in an error due to the presence of different data types. Therefore, it's crucial to ensure that all elements in the list share the same data type before performing the conversion.

**Remember:** When converting a list to an array, all elements must have the same data type to avoid errors.

---

## Check yourself
1. What is a list in Python?
2. How do you convert a tuple to a list?
3. Why might you want to convert a list to a NumPy array?
4. What happens if you try to convert a list with mixed data types to a NumPy array?
5. What is the difference between a list and an array?

### Answers
1. A list in Python is a flexible data structure that can hold multiple types of data.
2. You convert a tuple to a list by using the `list()` function, e.g., `element_list = list(elements)`.
3. You might want to convert a list to a NumPy array to perform efficient numerical operations and handle data in a structured manner.
4. If you try to convert a list with mixed data types to a NumPy array, it will result in an error.
5. A list in Python can contain different data types, whereas a NumPy array requires all elements to have the same data type.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
