# BanglaASR9_007
Today we will learn about the `SELECT` query in SQL.

## Key takeaways
- `SELECT` query
- `Student_Info` table
- `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, `Enrollment_Date`
- `max()`, `min()`, `sum()`
- `ORDER BY`, `ASC`, `DESC`

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Database Management System
**Ek line e:** Today we will learn about the `SELECT` query in SQL.

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


- **Red Box 1**: This box shows the `Student_Info` table. It contains columns like `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`. Each row represents a student with their respective details.

- **Blue Box 2**: This box lists the SQL commands `max()`, `min()`, and `sum()`. These are used for aggregation functions in SQL queries.

**Ek line e:** The `SELECT` query allows us to retrieve specific data from a database.


### Extra jana kotha
The `SELECT` query is fundamental in SQL. It helps us fetch data from a database based on certain conditions. For example, if we want to find the maximum CGPA among all students, we use the `MAX()` function.

**Mone rakho:** `SELECT` query, `Student_Info` table, `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, `Enrollment_Date`, `max()`, `min()`, `sum()`, `ORDER BY`, `ASC`, `DESC`.

**Ek line e:** Let's start with a simple `SELECT` query to retrieve the CGPA of a specific student.


**Mone rakho:** `SELECT CGPA FROM Student_Info WHERE ID = 401201`

**Ek line e:** This query retrieves the CGPA of the student with ID 401201.


**Mone rakho:** `3.40`

**Ek line e:** Next, let's retrieve the first name and last name of a student.


**Mone rakho:** `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 202011`

**Ek line e:** This query retrieves the first name and last name of the student with ID 202011.


**Mone rakho:** `Adiba Noshin`

**Ek line e:** Now, let's retrieve the department of a student.


**Mone rakho:** `SELECT Department FROM Student_Info WHERE ID = 151216`

**Ek line e:** This query retrieves the department of the student with ID 151216.


**Mone rakho:** `M-LH`

**Ek line e:** To order the results, we use the `ORDER BY` clause.


**Mone rakho:** `SELECT * FROM Student_Info ORDER BY ID ASC`

**Ek line e:** This query orders the results by `ID` in ascending order.


**Mone rakho:** `401201, 241412, 202011, 110112`

**Ek line e:** Finally, we can use aggregation functions like `MAX()` to find the highest CGPA.


**Mone rakho:** `SELECT MAX(CGPA) FROM Student_Info`

**Ek line e:** This query finds the maximum CGPA among all students.

**Mone rakho:** `3.98`

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query and Worked Example
**Ek line e:** This is an SQL query to find the student with the highest CGPA.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


1. **Red Box 1 (SQL Query):** The query `select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` is used to find the student with the highest CGPA. Here, `Student_Info` is the table name, and `CGPA` is the column name representing the grade point average.
   
2. **Blue Box 2 (Worked Example):** The worked example shows the result of the query. The table contains two columns: `ID` and `CGPA`. The row with the highest CGPA is highlighted.

> Lecturer: "So, this is the CGA max of CGPA."

The query works by first finding the maximum CGPA using the subquery `(select max(CGPA) from Student_Info);`. Then, the main query selects the `ID` and `CGPA` from the `Student_Info` table where the `CGPA` matches the maximum CGPA found in the subquery.

### Extra jana kotha (lecture e bola hoy ni)
This query helps us identify the top-performing student in terms of CGPA. It involves a nested query, where the inner query finds the maximum CGPA, and the outer query retrieves the corresponding student details. This method ensures that we get the exact student who has the highest CGPA in the database.

---

## Check yourself
1. Write a `SELECT` query to retrieve the CGPA of the student with ID 401201.
2. Write a `SELECT` query to retrieve the first name and last name of the student with ID 202011.
3. Write a `SELECT` query to retrieve the department of the student with ID 151216.
4. Write a `SELECT` query to order the results by `ID` in ascending order.
5. Write a `SELECT` query to find the maximum CGPA among all students.

### Answers
1. `SELECT CGPA FROM Student_Info WHERE ID = 401201`
2. `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 202011`
3. `SELECT Department FROM Student_Info WHERE ID = 151216`
4. `SELECT * FROM Student_Info ORDER BY ID ASC`
5. `SELECT MAX(CGPA) FROM Student_Info`

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9_007` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 0.*
