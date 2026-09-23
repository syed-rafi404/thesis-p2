# SQL SELECT Command and Subqueries
This lecture covers the `SELECT` command in SQL for retrieving data from a database table and using subqueries to find specific records.

## Key takeaways
- The `SELECT` command is used to retrieve data from a database table.
- You can use the `SELECT` command with a star (`*`) to retrieve all columns or list specific columns.
- The `WHERE` clause is used to filter the results based on certain conditions.
- Aggregation functions like `MAX`, `MIN`, and `SUM` are used to perform operations on a set of values.
- A subquery can be used within another query to find specific rows based on conditions derived from other parts of the query.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to SQL Select Command
**In one line:** The `SELECT` command is used to retrieve data from a database table.

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


### Explanation
1. **Introduction to the `SELECT` Command**: The `SELECT` command is the most commonly used and important SQL command for retrieving data from a database table. (Box 1)
2. **Retrieving Data**: To retrieve specific data from a table, you use the `SELECT` command followed by a star (`*`) to indicate that you want all columns. For example, to see the full details of a student with ID 401201, you would use `SELECT * FROM student_info;`. (Box 2)
3. **Selecting Specific Columns**: You can also select specific columns by listing them after the `SELECT` keyword. For instance, to get the first name and last name of a student with ID 151216, you would use `SELECT first_name, last_name FROM student_info;`. (Box 2)
4. **Using the `WHERE` Clause**: To filter the results based on certain conditions, you use the `WHERE` clause. For example, to find the department of a student with ID 151216, you would use `SELECT department FROM student_info WHERE id = 151216;`. (Box 2)
5. **Aggregation Functions**: Aggregation functions like `MAX`, `MIN`, and `SUM` are commonly used to perform operations on a set of values. For example, to find the maximum CGPA in the `student_info` table, you would use `SELECT MAX(cgpa) FROM student_info;`. (Box 2)

**In English: The `SELECT` command is used to retrieve data from a database table.**

**Quotes:**
> "so, shudhu matro data ar amra database er je table sheikhan theke data ke retrive kore."  
> (In English: so, we just want to retrieve data from a table in our database.)

**Remember:** The `SELECT` command is fundamental for querying data in a database table.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Finding Maximum CGPA Using SQL Subquery
**In one line:** This lecture explains how to find the student with the highest CGPA using a SQL subquery.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


### Explanation
1. **Understanding the Query**: The query `select ID, CGPA from Student_Info where CGPA = (select max(CGPA) from Student_Info);` aims to find the student with the highest CGPA. The inner query `(select max(CGPA) from Student_Info)` returns the maximum CGPA from the `Student_Info` table. The outer query then selects the `ID` and `CGPA` of the student whose CGPA matches this maximum value.
   
2. **Worked Example**: 
   - **Table Data**:
     ```markdown
     | ID    | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
     |-------|------------|-----------|------|------------|-----------------|
     | 241412| Syed       | Rafi      | 3.55 | CS         | 01-01-2024      |
     | 151216| Ahsan      | Habib     | 3.7  | Math       | 20-09-2024      |
     | 202011| Adiba      | Noshin    | 3.28 | Economics  | 21-10-2021      |
     | 110112| Maria      | Islam     | 3.98 | English    | 02-02-2020      |
     | 401201| Israt      | Jahan    | 3.40 | MicroBiology | 11-11-2025      |
     ```
   - **Result**:
     ```markdown
     ID | CGPA
     ---|------
     110112 | 3.98
     ```

3. **Lecture Quotes**:
   > Lecturer: "so, etama ki korbe? select kortese cg max of cgpa. mane cgpa ekhane amar path ta row ache."
   > (In English: "So, what will happen? We are selecting the maximum CGPA. This means we are finding the row where the CGPA is the maximum.")

4. **Remember**: The key point is that a subquery can be used to find specific rows based on conditions derived from other parts of the query.

---

## Check yourself
1. What does the `SELECT` command do?
2. How do you retrieve all columns from a table named `student_info`?
3. How do you retrieve specific columns from a table named `student_info`?
4. Explain the purpose of the `WHERE` clause in an SQL query.
5. How can you find the student with the highest CGPA using a subquery?

### Answers
1. The `SELECT` command retrieves data from a database table.
2. To retrieve all columns from a table named `student_info`, you would use `SELECT * FROM student_info;`.
3. To retrieve specific columns from a table named `student_info`, you would use `SELECT first_name, last_name FROM student_info;`.
4. The `WHERE` clause is used to filter the results based on certain conditions.
5. To find the student with the highest CGPA using a subquery, you would use the query `SELECT ID, CGPA FROM Student_Info WHERE CGPA = (SELECT MAX(CGPA) FROM Student_Info);`.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
