# Python Lists, Tuples, Arrays, and Error Handling

This lecture covers Python lists, tuples, arrays, and error handling.

## Key takeaways
- Lists are flexible and versatile data structures in Python.
- Tuples are immutable, while lists are mutable.
- Arrays in Python are typically implemented as lists.
- Error handling allows for quick and efficient debugging.

## Lists
- Lists are a flexible data type in Python.
- Example: `fruit = ["Apple", "Orange", "Mango"]`
- Lists can contain different data types.
- Example: `elements = ["Apple", 7, 3.14, True]`
- Accessing elements: `print(elements[0])` prints "Apple".
- Length of list: `print(len(elements))` prints 4.
- Modifying elements: `elements[0] = "Mango"` changes the first element to "Mango".
- Example: 
    ```python
    fruit = ["Apple", "Orange", "Mango"]
    elements = ["Apple", 7, 3.14, True]
    print(elements[0])  # Output: Apple
    print(len(elements))  # Output: 4
    elements[0] = "Mango"
    print(elements[0])  # Output: Mango
    ```

![Board 0:00-6:00](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed from 10 video frames with the lecturer removed; 97% of the board is unobstructed.*

## Tuples
- Tuples are immutable, meaning their contents cannot be changed.
- Example: `Elements = ("Apple", 7, 3.1416, True)`
- Converting tuple to list: `element_list = list(elements)`
- Modifying elements: `element_list[2] = 5`
- Converting list back to tuple: `elements = tuple(element_list)`
- Example: 
    ```python
    Elements = ("Apple", 7, 3.1416, True)
    element_list = list(elements)
    element_list[2] = 5
    elements = tuple(element_list)
    print(elements)  # Output: ('Apple', 7, 5, True)
    ```

![Board 7:10-10:40](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed from 10 video frames with the lecturer removed; 96% of the board is unobstructed.*

## Arrays
- Arrays in Python are typically implemented as lists.
- Importing NumPy for array operations: `import numpy as np`
- Creating a NumPy array from a list: `list_1 = [7, 8, 9, 10]; list_1 = np.array([list_1])`
- Example: 
    ```python
    import numpy as np
    list_1 = [7, 8, 9, 10]
    list_1 = np.array([list_1])
    ```

![Board 11:00-14:00](figures_board/board_03_era3.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed from 5 video frames with the lecturer removed; 98% of the board is unobstructed.*

## Check yourself
1. What is the output of `print(fruit[1])`?
2. How do you get the length of a list named `elements`?
3. What happens when you try to modify a tuple?
4. How do you convert a list to a NumPy array?
5. What is the output of `print(list_1)`?

## Answers
1. The output is "Orange".
2. The output is the length of the list, e.g., `4`.
3. You get an error because tuples are immutable.
4. Use `np.array(list_name)`.
5. The output is `[[7 8 9 10]]`.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*