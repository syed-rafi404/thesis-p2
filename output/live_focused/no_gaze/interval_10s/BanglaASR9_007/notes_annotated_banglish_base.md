# BanglaASR9_007: Database Management System: Introduction to SQL Select Query
Today, we will learn about the `SELECT` query in SQL.

## Key takeaways
- The `SELECT` query is used to retrieve data from a database.
- We can select all columns or specific columns using the `SELECT` command.
- The `WHERE` clause is used to filter data based on specific conditions.
- Aggregation functions like `MAX()`, `MIN()`, and `SUM()` are used to summarize data.
- The `ORDER BY` clause is used to sort data in ascending or descending order.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Database Management System: Introduction to SQL Select Query
**Ek line e:** Today, we will learn about the `SELECT` query in SQL.

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


1. **Red Box 1**: The board shows a table named `Student_Info` containing student details such as ID, First_Name, Last_Name, CGPA, Department, and Enrollment_Date.
2. **Blue Box 2**: The board lists SQL commands `max()`, `min()`, and `sum()`.

The lecturer explains that SQL is the most used and important command for retrieving data from a database. He demonstrates how to use the `SELECT` query to retrieve specific information from the `Student_Info` table.

**Steps:**
1. **Selecting Full Data**: 
   - The lecturer starts by selecting all columns from the `Student_Info` table using the `SELECT * FROM Student_Info;` command. This retrieves all the data in the table.
   
2. **Selecting Specific Columns**:
   - To select specific columns, the lecturer uses the `SELECT` command followed by the column names. For example, to select the `CGPA` column, he writes `SELECT CGPA FROM Student_Info;`.
   - To select multiple columns, he combines them with commas, like `SELECT First_Name, Last_Name FROM Student_Info;`.

3. **Filtering Data**:
   - The lecturer filters the data based on a specific condition using the `WHERE` clause. For instance, to find the `CGPA` of a student with ID `401201`, he writes `SELECT CGPA FROM Student_Info WHERE ID = 401201;`.

4. **Displaying Full Information**:
   - To display the full information of a student with ID `202011`, he uses `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 202011;`.

5. **Displaying Department**:
   - Similarly, to display the department of a student with ID `151216`, he writes `SELECT Department FROM Student_Info WHERE ID = 151216;`.

6. **Ordering Data**:
   - The lecturer orders the data by the `ID` column in ascending or descending order using the `ORDER BY` clause. For example, `SELECT * FROM Student_Info ORDER BY ID ASC;` or `DESC;`.

7. **Aggregation Functions**:
   - Finally, the lecturer introduces aggregation functions like `MAX()`, `MIN()`, and `SUM()`. To find the maximum `CGPA` in the table, he writes `SELECT MAX(CGPA) FROM Student_Info;`.


**Extra jana kotha**: Aggregation functions in SQL help summarize data. For example, `MAX()` returns the highest value in a column, while `SUM()` adds up all the values in a column. Understanding these functions is crucial for data analysis.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query: Finding Maximum CGPA
**Ek line e:** This query finds the student with the highest CGPA.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


1. **Red Box 1 (SQL Query):** The query `select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` is used to find the student with the highest CGPA. Let's break it down step by step.

2. **Blue Box 2 (Worked Example):** The worked example shows the result of the query, which is `| ID | CGPA | | --- | --- | | 110112 | 3.98 |`. This means the student with ID 110112 has the highest CGPA of 3.98.

3. **Explanation:**
   - **Step 1:** The inner query `(select max(CGPA) from Student_Info)` finds the maximum CGPA in the `Student_Info` table.
   - **Step 2:** The outer query `select ID, CGPA from Student_Info where CGPA = (select max(CGPA) from Student_Info);` selects the `ID` and `CGPA` of the student(s) whose CGPA matches the maximum CGPA found in the inner query.

4. **Quote:**

5. **Extra jana kotha:**
   The query uses a subquery to find the maximum CGPA and then filters the `Student_Info` table to get the student(s) with that CGPA. This is a common technique in SQL to perform complex queries involving multiple conditions. Understanding these techniques is crucial for managing and querying large databases efficiently.

---

## Check yourself
1. Write the SQL command to select all columns from the `Student_Info` table.
2. Write the SQL command to select the `CGPA` column from the `Student_Info` table.
3. Write the SQL command to select the `First_Name` and `Last_Name` columns from the `Student_Info` table.
4. Write the SQL command to find the `CGPA` of a student with ID `401201`.
5. Write the SQL command to display the full information of a student with ID `202011`.

### Answers
1. `SELECT * FROM Student_Info;`
2. `SELECT CGPA FROM Student_Info;`
3. `SELECT First_Name, Last_Name FROM Student_Info;`
4. `SELECT CGPA FROM Student_Info WHERE ID = 401201;`
5. `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 202011;`

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9_007` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 0 kept, 2 removed. References to boxes that do not exist: 0.*
