# Lists, Tuple and Arrays
THE SECTIONS

## Key takeaways
- Lists are flexible data structures in Python that can hold different data types.
- Tuples are similar to lists but are immutable.
- You can convert lists to arrays using the NumPy library.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 -->
## Lists, Tuple and Arrays
**Ek line e:** Lists, tuples, and arrays are fundamental data structures in Python.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 List · 4 Code · 5 Code · 6 Code


- **Box 1 (red)**: Title: Lists, Tuple and Arrays
- **Box 2 (blue)**: List: `fruit = ["Apple", "Orange", "Mango"]`
- **Box 3 (orange)**: List: `elements = ["Apple", 7, 3.14, 2/3]`
- **Box 4 (green)**: Code: `print(elements[0])`
- **Box 5 (purple)**: Code: `print(len(elements))`
- **Box 6 (pink)**: Code: `elements[0] = "Mango"`

### Explanation
Lecturer: "ajke kete video te amra dekhbo python er list couple and arrays."

Lists are very flexible data types in Python. Let's see an example where we define a list called `fruit` containing strings: `"Apple", "Orange", "Mango"`.

Lecturer: "so erokhomi ekta flexible data structure-er hulo amader a list. toh ami khub easily ekhane apple rakhte parbo, string er moddhe over shoi. ekta comma diye. tarpor ami orange rakhte parbo. tarpore ami jayle mango rakhte parbo."

We can also include different data types in a list. For instance, let's define a list called `elements` with various types: `"Apple", 7, 3.14, 2/3`.

Lecturer: "to list er, python er list er shob theke borro je advantage sheta hocche amra different data type e value ekhane rakhte pari. jeemon dhoro ami jodi ekta list nei, list-tar nam dilam dhoro elements. elements er moddhe dhoro thumi rakhte chau. aa tomar total, just je kono ginis rakhte chau. ki rakhte chau? dhoro thomar pebbet ekta fruit rakhte lam."

We can access these elements using indexing. In Python, indexing starts from zero. So, the first element is at index 0, the second at index 1, and so on. Let's print the second element of the `elements` list:

```python
print(elements[1])
```

This will output `7`, because the second element is the integer `7`.

Lecturer: "tarpore arekta mojar jini sholou jeta list diye kora jay, print function er moddhe or m-ne tau ami chaile list er total length jeta sheta python er ekta built-in function length diye check korte pare. jabon length of elements. kache? print korbe length of elements. element er total length jeta sheta print korbe."

To find the length of the list, we can use the `len()` function:

```python
print(len(elements))
```

This will output `4`, because the list contains four elements.

Lecturer: "ebon print korle ki value pabe? ekhane total 1, 2, 3, 4. total charta value ache. e jomno ekhane total amra 4 pabo. thik ache? so eibhabe amra kotte pari. eibom ki? amader aro flexibility ache. ami jelem hotat kore amar fabl fruit hotat kore aa zero theke, sorry, apple theke orange hoye jabe. toh amra ki kotte pari? je ami je ami ki korte pari."

We can modify the list. For example, changing the first element from `"Apple"` to `"Mango"`:

```python
elements[0] = "Mango"
```

Now, if we print the list again:

```python
print(elements)
```

It will output `["Mango", 7, 3.14, 2/3]`.

Lecturer: "tuple and list onekta same but ekta khubi boro difference ache eduitar moddhe. jemon list er moddhe ke amra chelei poshonder moto datatype rakhte parbe. jerokom amra ekhane apple, orange, mango chilo. ekhane ami ki? chele ki? ekhane apple 7 aa amra ekhane integer float, boolean jeekhone jinishta akte pari. tuple er moddhe ami ei jinishta parbo but shobje boro je difference."

Tuples are similar to lists, but they are immutable, meaning their values cannot be changed after they are created. To create a tuple, we use parentheses instead of square brackets:

```python
elements_tuple = ("Apple", 7, 3.14, 2/3)
```

If we try to change the first element of the tuple, it will result in an error:

```python
elements_tuple[0] = "Mango"  # This will raise an error
```

### Extra jana kotha
Lists in Python are mutable, meaning you can change their contents after they are created. Tuples, on the other hand, are immutable, which means their contents cannot be changed once they are defined. Understanding the differences between these data structures is crucial for effective programming in Python.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** In this section, we will discuss how to modify elements in a tuple and introduce arrays.

![Board 2: 7:10-10:40](figures_annotated/board_era2_710.jpg)

*Figure 2. The whiteboard during 7:10–10:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


1. **Red Box 1 (Code):** The code here shows us how to work with lists and tuples. We start with `elements=("Apple", 7, 3.1416, True)` and create a list `element_list` from these elements. Then, we change the third element (index 2) from `3.1416` to `5`.

2. **Step-by-Step Explanation:**
   - First, we see the initial tuple `elements=("Apple", 7, 3.1416, True)`.
   - We create a list `element_list` from this tuple: `element_list = list(elements)`.
   - Next, we change the third element of `element_list` to `5`: `element_list[2] = 5`.
   - Finally, we convert this modified list back to a tuple: `elements = tuple(element_list)`.

3. **Lecturer's Words:**
   > Lecturer: "thali ekta ki change-er cholo? structure-ly. amar ekhane ami square bracket-er jakai first bracket-ta diyechi. and ami jodi chai je elements of aa second index-er value, payer value jeta, sheita change kore."
   - This means, "Let's change the structure. Here, I use square brackets to denote the first bracket. And if I want to change the value of the second index, I do that."

4. **Restrictions in Tuples:**
   - The lecturer mentions that tuples are immutable, meaning you cannot directly change their elements. If you try, you will get an error.
   - To overcome this, you need to create a new variable. For example, you can create a new list from the tuple, modify the list, and then convert it back to a tuple.

5. **Creating a New List and Converting Back:**
   - We create a new list `element_list` from the original tuple.
   - Modify the list: `element_list[2] = 5`.
   - Convert the modified list back to a tuple: `elements = tuple(element_list)`.

6. **Printing the Updated Tuple:**
   - After all these steps, we print the updated tuple: `print(elements)`.

### Extra jana kotha (lecture e bola hoy ni)
Understanding how to work with tuples and lists is crucial because tuples are immutable, which means you cannot change their elements directly. However, you can achieve similar results by converting tuples to lists, modifying the lists, and then converting them back to tuples. This is a common practice in Python programming.

<!-- boxes: 1=#d62828 -->
## Lists, Tuple and Arrays
**Ek line e:** In this section, we will discuss how to convert lists into arrays using NumPy.

![Board 3: 11:00-14:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–14:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Code


The lecturer started by importing the NumPy library, which is essential for working with arrays in Python. He explained that while Python has built-in support for lists, arrays require an external library like NumPy.

1. **Importing NumPy**: The lecturer wrote `import numpy as np` on the board. This line imports the NumPy library under the alias `np`, making it easier to use NumPy functions.
   
2. **Creating a List**: Next, he created a list named `list_1` containing some integer values: `list_1 = [7, 8, 9, 10]`. Then, he converted this list into an array using `np.array([list_1])`.

   - **Red Box 1**: `import numpy as np list_1 = [7, 8, 9, 10] list_1 = np.array([list_1])`

3. **Creating Another List**: He also created another list named `list_2` containing mixed data types: `list_2 = ['Apple', 07, True]`. The lecturer pointed out that this list contains strings, integers, and booleans.

   - **Red Box 1**: `list_2 = ['Apple', 07, True]`

4. **Converting List to Array**: The lecturer explained that while `list_1` can be easily converted to an array, `list_2` cannot because it contains different data types. Converting a list to an array requires all elements to be of the same type.

   - **Red Box 1**: `np.array([list_1])`

5. **Error Handling**: The lecturer emphasized that when converting a list to an array, if the list contains different data types, it will result in an error. For example, trying to convert `list_2` to an array would fail due to the presence of mixed data types.

   - **Red Box 1**: `list_2 = ['Apple', 07, True]`

**Quotes:**
> Lecturer: "ami jokhon lektesi import num by snp, toh mane ki? erpor amar jokhoni num by ke dor kare hobe."

### Extra jana kotha
When converting a list to an array, ensure all elements are of the same data type. Otherwise, you will encounter errors. For instance, if your list contains both integers and strings, you cannot directly convert it to an array without first converting all elements to a consistent type.

---

## Check yourself
1. What is the output of `print(elements[1])`?
2. How do you find the length of a list in Python?
3. What happens if you try to change an element in a tuple?
4. How do you convert a list to a tuple?
5. Why might converting a list to an array fail?

### Answers
1. The output of `print(elements[1])` is `7`.
2. You find the length of a list in Python using the `len()` function.
3. If you try to change an element in a tuple, it will result in an error.
4. You convert a list to a tuple by using the `tuple()` function, for example, `elements = tuple(elements)`.
5. Converting a list to an array fails if the list contains different data types.

---


*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
