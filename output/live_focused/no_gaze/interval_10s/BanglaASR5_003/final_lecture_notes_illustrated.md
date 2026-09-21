# Python Lists, Tuples, Arrays, and Error Handling

## Introduction
Welcome back to this video where we will explore Python lists, tuples, arrays, and error handling.


![Figure 1](figures/fig_01_000.jpg)

**Figure 1.** Board during: Introduction Frame at 0:00.

## Python Lists

![Figure 2](figures/fig_02_040.jpg)

**Figure 2.** Board during: Python Lists Frame at 0:40.

### Definition
- **List**: A flexible and popular data structure in Python.
- **Variable Fruit**: An example of a list containing various items such as strings and numbers.
- **Flexible Data Structure**: Lists can store different types of data and are mutable.


![Figure 3](figures/fig_03_230.jpg)

**Figure 3.** Board during: Definition Frame at 2:30.

### Example
```python
fruits = ["apple", "orange", "mango"]
print(fruits)
```


![Figure 4](figures/fig_04_350.jpg)

**Figure 4.** Board during: Example Frame at 3:50.

### Accessing Elements
- **Indexing**: Lists are zero-indexed.
- **Accessing an Element**: To access the second element of the list.
    ```python
    print(fruits[1])
    ```


![Figure 5](figures/fig_05_1000.jpg)

**Figure 5.** Board during: Accessing Elements Frame at 10:00.

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

## Figure Index

| Figure | Time | Section | Source |
|---|---|---|---|
| 1 | 0:00 | Introduction | keywords |
| 2 | 0:40 | Python Lists | keywords |
| 3 | 2:30 | Definition | keywords |
| 4 | 3:50 | Example | keywords |
| 5 | 10:00 | Accessing Elements | keywords |
