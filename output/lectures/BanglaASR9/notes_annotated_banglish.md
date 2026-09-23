# BanglaASR9
The lecture covers an introduction to structs and symbol tables, followed by an explanation of three address code and memory address calculations.

## Key takeaways
- Structs are used to group different types of data together.
- A symbol table helps in managing variables and their offsets in memory.
- Three address code is used to calculate memory addresses step by step.

<!-- boxes: 1=#d62828 -->
## Board 1: Introduction to Structs and Symbol Table
**Ek line e:** Today we start with an introduction to structs and how they manage memory.

![Board 1: 0:20-11:00](figures_annotated/board_era1_020.jpg)

*Figure 1. The whiteboard during 0:20–11:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Struct P


1. **Red Box 1 (Struct P):** The red box introduces `Struct P`, which includes various fields such as a single character grade, four integer marks, and a character section array. This struct is used to represent a student's record.

2. **Explanation:**
   - The lecturer explains that a struct is a data type in C and C++ that allows us to group different types of data together. For example, in `Struct P`, we have a character grade, four integer marks, and a character section array.
   - The struct `Struct P` is defined as follows:
     ```markdown
     Struct P {
         char grade; // 1 character grade
         int marks[4]; // 4 integer marks
         char section[10]; // Character section array
     }
     ```
   - The lecturer then moves on to explain the concept of a symbol table, which is necessary for managing variables and their offsets in memory.

3. **Quote:**
   > "symbol table thake lagbe, tai na?" - Lecturer

4. **Extra jana kotha:**
   - A symbol table helps in managing variables and their offsets in memory. It keeps track of all the variables and their corresponding memory locations, making it easier to understand and manage the memory layout.

<!-- boxes: 1=#d62828 -->
## Three Address Code and Calculation
**Ek line e:** In this section, we will understand how to calculate the memory addresses using three address code.

![Board 2: 11:10-14:58](figures_annotated/board_era2_1110.jpg)

*Figure 2. The whiteboard during 11:10–14:58, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Structs


1. **Red Box 1**: First, let's look at the structs defined on the board. We have Struct P, Struct Q, Struct R, and Struct S. Each struct contains different fields like `marks`, `section`, `courseid`, `semesters`, etc.

2. **Red Box 1 (continued)**: Now, let's focus on the calculation of the memory address for the `student record`. The base address is stored in `t1`.

3. **Red Box 2**: To find the address of `info`, we need to add 4 to `t1` because `info` starts after the first 4 bytes. So, `t2 = t1 + 4`.

4. **Red Box 3**: Next, to get the address of `course`, we add 8 more bytes to `t2` since `course` is 8 bytes away from `info`. Thus, `t3 = t2 + 8`.

5. **Red Box 4**: For the `result` field, which is an integer, we add another 4 bytes to `t3`. Therefore, `t4 = t3 + 4`.

6. **Red Box 5**: The `section` field is a character array, so we add 4 more bytes to `t4` to reach the start of the `section` array. Hence, `t5 = t4 + 4`.

7. **Red Box 6**: Finally, to get the address of the last element in the `section` array, we add 4 more bytes to `t5`. This gives us `t6 = t5 + 4`.

8. **Red Box 7**: The total distance from the base address to the last element in the `section` array is 27 bytes. So, `t7 = t6 + 4`.

9. **Red Box 8**: The final address of the `student record` is `t7`. Therefore, `y = studentrecord.info.course.result.section[4]` translates to `y = stdree[t7]`.

> Lecturer: "twenty-sseven. eta kintu basically sin gin ishi bujhacche."

### Extra jana kotha (lecture e bola hoy ni)
In summary, we used three address code to calculate the memory addresses step by step. This method helps in understanding the exact location of each field within the structure. By breaking down the calculation into smaller steps, we can easily determine the offset for any field in the structure.

---

## Check yourself
1. What is a struct and how is it used in C and C++?
2. How many bytes does the `section` array occupy in `Struct P`?
3. What is the final value of `t7` if the base address `t1` is 100?
4. Explain the process of calculating the memory address for the `section` array in `Struct P`.
5. What is the significance of a symbol table in managing memory?

### Answers
1. A struct is a data type in C and C++ that allows us to group different types of data together. In `Struct P`, it includes a character grade, four integer marks, and a character section array.
2. The `section` array occupies 10 bytes in `Struct P`.
3. If the base address `t1` is 100, the final value of `t7` would be 127 (100 + 4 + 8 + 4 + 4 + 4 + 4).
4. The process involves adding 4 bytes for each subsequent field in the struct until reaching the end of the `section` array.
5. A symbol table helps in managing variables and their offsets in memory, keeping track of all variables and their corresponding memory locations.

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 7.*
