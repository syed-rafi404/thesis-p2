# BanglaASR9_007
The lecture covers the basics of Database Management Systems (DBMS) and SQL queries.

## Key takeaways
- The `SELECT` command is used to retrieve data from a database table.
- To get all data from a table, use `SELECT * FROM table_name`.
- To get specific data, use `SELECT column_name(s) FROM table_name WHERE condition`.
- Aggregation functions like `MAX`, `MIN`, and `SUM` can be used to perform operations on the data.
- Nested queries can be used to find detailed information based on certain conditions.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Board 1 of 2, on the whiteboard during 0:10-9:10
**Ek line e:** Database Management System (DBMS)

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


### Explanation
1. **Database Management System (DBMS):**
   - The lecturer introduced the concept of a Database Management System (DBMS) and displayed a sample student information table.
   
2. **SQL Query Basics:**
   - The lecturer explained that the `SELECT` command is one of the most commonly used and important commands in SQL.
   - The `SELECT` command is used to retrieve data from a database table.

3. **Selecting Data:**
   - To retrieve all data from a table, you use `SELECT * FROM table_name`.
   - For example, to see the entire student information table, the lecturer wrote `SELECT * FROM student_info`.

4. **Retrieving Specific Data:**
   - To retrieve specific data like CGPA, the lecturer showed how to use `SELECT cgpa FROM student_info WHERE id = 401201`.
   - Similarly, to get the first name and last name of a student, the query would be `SELECT first_name, last_name FROM student_info WHERE id = 151216`.

5. **Aggregation Functions:**
   - The lecturer then introduced aggregation functions such as `MAX`, `MIN`, and `SUM`.
   - An example of using `MAX` was given: `SELECT MAX(cgpa) FROM student_info` to find the maximum CGPA in the table.

**Quotes:**
> Lecturer: "so, amr ekhane amr ekta type korte pari, korte pari."

**Mone Rakho:** 
- The `SELECT` command is used to retrieve data from a database table.
- To get all data from a table, use `SELECT * FROM table_name`.
- To get specific data, use `SELECT column_name(s) FROM table_name WHERE condition`.
- Aggregation functions like `MAX`, `MIN`, and `SUM` can be used to perform operations on the data.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Database Management System (DBMS)
**Ek line e:** This section covers SQL queries and their usage.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


**Explanation:**
1. **Understanding the Query**: The lecturer explains the SQL query `select ID, CGPA from Student_Info where CGPA = (select max(CGPA) from Student_Info);`. This query selects the IDs and CGPAs of students whose CGPA is the maximum in the `Student_Info` table.
2. **Example Table**: The lecturer shows the `Student_Info` table with sample data. The query returns the row where the CGPA is 3.98.
3. **Aggregation Functions**: The lecturer then discusses how to calculate the sum and average of CGPAs using aggregation functions like `SUM()` and `AVG()`.
4. **Nested Queries**: The lecturer explains the concept of nested queries, demonstrating how to find the student with the highest CGPA and then retrieve all details of that student.

**Quotes:**
> Lecturer: "so, etama ki korbe? select kortese cg max of cgpa. mane cgpa ekhane amar path ta row ache."
> Lecturer: "tahole ami ekhane main of cgpa diye dilam."

**Mone rakho:** The key points from the board include understanding the SQL query structure, identifying the student with the highest CGPA, and using nested queries to retrieve detailed information about that student.

---

## Check yourself
1. What command is used to retrieve all data from a table named `student_info`?
2. How would you retrieve the CGPA of a student with ID 401201?
3. What is the purpose of the `MAX` function in SQL?
4. How would you find the student with the highest CGPA and retrieve all their details?
5. What does the `SELECT * FROM table_name` statement do?

### Answers
1. `SELECT * FROM student_info`
2. `SELECT cgpa FROM student_info WHERE id = 401201`
3. The `MAX` function is used to find the maximum value in a specified column.
4. `SELECT * FROM student_info WHERE cgpa = (SELECT MAX(cgpa) FROM student_info)`
5. It retrieves all columns from the specified table.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 1 removed. References to boxes that do not exist: 0.*
