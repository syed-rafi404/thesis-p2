# Python Lists, Tuples, Arrays, and Error Handling

## Introduction
Welcome back to this video where we will explore Python lists, tuples, arrays, and error handling.

## Python Lists
### Definition
- **List**: A flexible and popular data structure in Python.
- **Variable Fruit**: An example of a list containing various items such as strings and numbers.
- **Flexible Data Structure**: Lists can store different types of data and are mutable.

### Example
```python
fruits = ["apple", "orange", "mango"]
print(fruits)
```


![Board 0:00-6:00](figures_board/board_01_era1.jpg)

**Figure 1.** Whiteboard as it stood during 0:00&ndash;6:00, reconstructed from 10 video frames with the lecturer removed. 96.7% of the board is unobstructed.

### Accessing Elements
- **Indexing**: Lists are zero-indexed.
- **Accessing an Element**: To access the second element of the list.
    ```python
    print(fruits[1])
    ```

### Length of List
- **Length Function**: To find the length of the list.
    ```python
    print(len(fruits))
    ```

### Updating Elements
- **Changing an Element**: Modify the list by changing an element.
    ```python
    fruits[0] = "mango"
    print(fruits)
    ```

## Tuples
### Definition
- **Tuple**: Similar to lists but immutable (cannot be modified after creation).

### Example
```python
fruits_tuple = ("apple", "orange", "mango")
print(fruits_tuple)
```

### Accessing Elements
- **Accessing an Element**: Same as lists.
    ```python
    print(fruits_tuple[1])
    ```

### Updating Elements
- **Immutable Nature**: Once created, tuples cannot be updated.
    ```python
    # This will raise an error
    fruits_tuple[0] = "mango"
    ```


![Board 7:10-10:40](figures_board/board_02_era2.jpg)

**Figure 2.** Whiteboard as it stood during 7:10&ndash;10:40, reconstructed from 10 video frames with the lecturer removed. 96.2% of the board is unobstructed.

### Converting Lists to Tuples
- **Converting a List to a Tuple**: 
    ```python
    fruits_list = ["apple", "orange", "mango"]
    fruits_tuple = tuple(fruits_list)
    print(fruits_tuple)
    ```

## Arrays
### Definition
- **Array**: A built-in data structure in Python, typically used for numerical operations.

### Importing Array Library
- **Importing Numpy**: 
    ```python
    import numpy as np
    ```

### Creating an Array
- **Creating an Array from a List**:
    ```python
    list1 = [1, 2, 3, 4]
    array1 = np.array(list1)
    print(array1)
    ```

### Converting List to Array
- **Example**: Convert `list2` to an array.
    ```python
    list2 = ["Apple072"]
    array2 = np.array(list2)
    print(array2)
    ```

## Errors in Python

![Board 11:00-14:00](figures_board/board_03_era3.jpg)

**Figure 3.** Whiteboard as it stood during 11:00&ndash;14:00, reconstructed from 5 video frames with the lecturer removed. 97.8% of the board is unobstructed.

### Definition
- **Error Handling**: Managing exceptions in Python to handle unexpected situations.

### Example
- **Handling Different Data Types**: 
    ```python
    try:
        num1 = int(input("Enter a number: "))
        num2 = int(input("Enter another number: "))
        result = num1 / num2
        print("Result:", result)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except ValueError:
        print("Error: Please enter valid numbers.")
    ```

### Summary
- **Lists**: Flexible, mutable data structures in Python.
- **Tuples**: Immutable data structures, useful when data needs to remain unchanged.
- **Arrays**: Numerical data structures, often imported from libraries like NumPy.
- **Errors**: Essential for robust programming, handling exceptions to prevent program crashes.

This concludes the lecture on Python lists, tuples, arrays, and error handling.

---

*Figures are reconstructed whiteboards. Each is assembled from tiles taken from moments when the lecturer was not standing in front of that part of the board, so every pixel is unmodified video; nothing is generated. A figure shows the board's state across the time range given, not a single instant. Boards less than 95% clear of the lecturer were left out.*
