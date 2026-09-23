# Board transcription (frame)

## Board 0:00-6:00

Lists, Tuple and Arrays

fruit = ["Apple", "Orange", "Mango"]

elements = ["Apple", 7, 3.14, True]

print(elements[0])

print(len(elements))

elements[0] = "Mango"

print(elements[0])

## Board 7:10-10:40

Lists, Tuple and Arrays

elements = ("Apple", 7, 3.1416, True)
element_list = list(elements)
element_list[2] = 5
elements = tuple(element_list)
print(elements)

## Board 11:00-14:00

Lists, Tuple and Arrays

import numpy as np

list_1 = [7, 8, 9, 10]

list_1 = np.array(list_1)

list_2 = ["Apple", 0, True]
