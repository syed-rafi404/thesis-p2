# Python Lists, Tuples, Arrays, and Error Handling

In this lecture, we will explore Python lists, tuples, arrays, and error handling.

## Key takeaways
- Python lists are flexible and can store various data types.
- Tuples are similar to lists but are immutable.
- Arrays in Python can be created using the `numpy` library.
- Error handling in Python allows for robust code execution.

## Python Lists
Lists are a flexible data type in Python that can store multiple items in a single variable.

### Core Idea
A list is defined using square brackets and can contain any type of data.

### Example
```python
fruit = ['apple', 'orange', 'mango']
```

### Indexing
Python lists are zero-indexed, meaning the first element is at index 0.

### Example
```python
fruits = ['apple', 7, 3.1416, True]
print(fruits[2])  # Output: 3.1416
```

### Updating Elements
Lists can be updated by reassigning elements.

### Example
```python
fruits[0] = 'mango'
print(fruits)  # Output: ['mango', 7, 3.1416, True]
```

![Board 0:00-6:00](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed from 10 video frames with the lecturer removed; 97% of the board is unobstructed.*

## Tuples
Tuples are similar to lists but are immutable, meaning their values cannot be changed after creation.

### Core Idea
A tuple is defined using parentheses and can contain any type of data.

### Example
```python
fruits_tuple = ('apple', 7, 3.1416, True)
```

### Attempting to Update a Tuple
Attempting to update a tuple will result in an error.

### Example
```python
fruits_tuple[0] = 'mango'  # Raises TypeError: 'tuple' object does not support item assignment
```

### Converting a List to a Tuple
A list can be converted to a tuple using the `tuple()` function.

### Example
```python
fruits_list = ['apple', 7, 3.1416, True]
fruits_tuple = tuple(fruits_list)
print(fruits_tuple)  # Output: ('apple', 7, 3.1416, True)
```

![Board 7:10-10:40](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed from 10 video frames with the lecturer removed; 96% of the board is unobstructed.*

## Arrays
Arrays in Python can be created using the `numpy` library.

### Core Idea
An array is a data structure that stores elements of the same data type.

### Example
```python
import numpy as np
list1 = [7, 8, 9, 10]
array1 = np.array(list1)
print(array1)  # Output: [ 7  8  9 10]
```

### Attempting to Change Data Type
Attempting to change the data type of an array will result in an error.

### Example
```python
array1[0] = 'apple'  # Raises ValueError: invalid literal for int() with base 10: 'apple'
```

## Error Handling
Error handling in Python allows for robust code execution by catching and handling exceptions.

### Core Idea
Use `try`, `except`, and `finally` blocks to handle errors.

### Example
```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("This will always execute")
```

## Check Yourself
1. Create a list with three fruits.
2. Print the second element of the list.
3. Update the first element of the list to 'mango'.
4. Create a tuple with four elements.
5. Try to update the first element of the tuple.

### Answers
1. ```python
   fruits = ['apple', 'banana', 'cherry']
   ```
2. ```python
   print(fruits[1])  # Output: banana
   ```
3. ```python
   fruits[0] = 'mango'
   print(fruits)  # Output: ['mango', 'banana', 'cherry']
   ```
4. ```python
   fruits_tuple = ('apple', 'banana', 'cherry', 'date')
   ```
5. ```python
   fruits_tuple[0] = 'mango'  # Raises TypeError: 'tuple' object does not support item assignment
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*