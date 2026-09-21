# Lecture Notes on Python Variables and Data Types

## Introduction
Welcome back to the class. We have discussed Python and its environment setup in previous sessions. Today, we will delve deeper into understanding variables and their types.

## Variables
A **variable** is a symbolic name that refers to a value in the computer's memory. Think of it as a box where you can store various types of information.

### Example
Let's consider the example of storing a book in a box:
```python
book = "Harry Potter"
```
Here, `book` is the variable name, and `"Harry Potter"` is the value stored in the variable.

### Box Analogy
- **Box**: Represents a variable.
- **Books, Fruits, etc.**: Represent different types of values that can be stored in the variable.

## Basic Data Types in Python
Python supports several data types. Let's explore the most common ones:

### String
A string is a sequence of characters. It is used to represent text.
```python
fruit = 'Apple'
print(fruit)
```

### Integer
An integer is a whole number, positive or negative, without decimals.
```python
age = 25
print(age)
```

### Float
A float is a number with a decimal point.
```python
pi = 3.14159
print(pi)
```

### Boolean
A boolean can have two possible values: `True` or `False`.
```python
is_student = True
print(is_student)
```

### Set
A set is a collection of unique elements.
```python
numbers = {1, 2, 3, 4, 5}
print(numbers)
```

### Tuple
A tuple is a collection of ordered, immutable elements.
```python
coordinates = (10, 20)
print(coordinates)
```

### List
A list is a collection of ordered, mutable elements.
```python
fruits = ['Apple', 'Banana', 'Cherry']
print(fruits)
```

## Naming Conventions for Variables
When naming variables in Python, follow these conventions:

1. **Use Lowercase Letters**: Start with lowercase letters.
    ```python
    name = "Rafi"
    ```
2. **Avoid Spaces**: Use underscores (`_`) instead of spaces.
    ```python
    name_of_student = "John Doe"
    ```
3. **Camel Case**: Capitalize the first letter of each word except the first one.
    ```python
    nameOfStudent = "Jane Doe"
    ```

### Examples
- **Snake Case**: `snake_case_example`
- **Camel Case**: `camelCaseExample`

## Case Sensitivity
Python is case-sensitive. Therefore, `age` and `Age` would be considered different variables.
```python
age = 25
AGE = 30
print(age)  # 25
print(AGE)  # 30
```

## Summary
In this lecture, we covered the basics of variables and different data types in Python. We learned about strings, integers, floats, booleans, sets, tuples, and lists. We also discussed naming conventions and the importance of case sensitivity. Understanding these concepts will help you effectively use Python for programming tasks.

Feel free to ask any questions!