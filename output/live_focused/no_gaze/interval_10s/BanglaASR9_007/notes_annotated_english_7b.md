# Introduction to SQL Select Command
The `SELECT` command is used to retrieve data from a database table.

## Key takeaways
- The `SELECT` command is the most used and important command in SQL for retrieving data.
- The asterisk (`*`) can be used to select all columns in a table.
- Specific columns can be selected using their exact names.
- Conditions can be applied using the `WHERE` clause to retrieve specific rows.
- Aggregation functions like `MAX`, `MIN`, and `SUM` can be used to perform calculations on a set of values.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Introduction to SQL Select Command
**In one line:** The `SELECT` command is used to retrieve data from a database table.

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


1. **Database Management System (DBMS):**
   - The board shows a sample database table named `Student_Info`. This table contains information such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
   
2. **SQL Query:**
   - The board also lists `max()`, `min()`, and `sum()` functions, which are commonly used in SQL queries for data retrieval and manipulation.

### Explanation
- **Step 1:** The lecturer introduces the `SELECT` command, explaining that it is the most used and important command in SQL for retrieving data from a database table.
  - **Box 1 (red):** The lecturer points to the `Student_Info` table and explains how to use the `SELECT` command to retrieve specific data.
  
- **Step 2:** To retrieve the entire table, the lecturer writes `SELECT * FROM Student_Info`.
  - **Box 2 (blue):** The lecturer explains that the asterisk (`*`) represents all columns in the table.
  
- **Step 3:** To retrieve specific columns, the lecturer demonstrates selecting `CGPA` from the `Student_Info` table.
  - **Box 2 (blue):** The lecturer writes `SELECT CGPA FROM Student_Info` and explains that this will display the `CGPA` of all students in the table.
  
- **Step 4:** To retrieve specific rows based on a condition, the lecturer uses the `WHERE` clause.
  - **Box 2 (blue):** The lecturer writes `SELECT CGPA FROM Student_Info WHERE ID = 401201` and explains that this will display the `CGPA` of the student with `ID = 401201`.
  
- **Step 5:** The lecturer then retrieves multiple columns using the `SELECT` command.
  - **Box 2 (blue):** The lecturer writes `SELECT First_Name, Last_Name FROM Student_Info` and explains that this will display the `First_Name` and `Last_Name` of all students in the table.
  
- **Step 6:** To retrieve a specific column for a particular row, the lecturer uses the `WHERE` clause again.
  - **Box 2 (blue):** The lecturer writes `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 122011` and explains that this will display the `First_Name` and `Last_Name` of the student with `ID = 122011`.
  
- **Step 7:** The lecturer then selects the `Department` column for a specific row.
  - **Box 2 (blue):** The lecturer writes `SELECT Department FROM Student_Info WHERE ID = 151216` and explains that this will display the `Department` of the student with `ID = 151216`.
  
- **Step 8:** The lecturer explains the importance of using exact column names when writing the `SELECT` command.
  - **Box 2 (blue):** The lecturer emphasizes that the column name should be written exactly as it appears in the table.
  
- **Step 9:** The lecturer demonstrates ordering the results.
  - **Box 2 (blue):** The lecturer writes `SELECT ID FROM Student_Info ORDER BY ID ASC` and explains that this will display the `ID` values in ascending order.
  
- **Step 10:** The lecturer introduces aggregation functions like `MAX`, `MIN`, and `SUM`.
  - **Box 2 (blue):** The lecturer writes `SELECT MAX(CGPA) FROM Student_Info` and explains that this will display the maximum `CGPA` in the `Student_Info` table.

### Quotes
> The lecturer said: "so, eikhane amra ki bhabe aa database table ter sathhe communicate korbo?"

### Background
Aggregation functions in SQL are used to perform calculations on a set of values and return a single value. For example, `MAX` returns the highest value, `MIN` returns the lowest value, and `SUM` adds up all the values. These functions are essential for summarizing data and performing complex queries efficiently.

**Remember:** The `SELECT` command is fundamental for retrieving data from a database table, and understanding how to use it effectively is crucial for managing and querying databases.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Finding Maximum CGPA Using SQL Subquery
**In one line:** This SQL query selects the ID and CGPA of the student with the highest CGPA by using a subquery to find the maximum CGPA first.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


1. **Red Box (SQL Query):** The SQL query `select ID, CGPA from Student_Info where CGPA = (select max(CGPA) from Student_Info);` is shown. This query selects the IDs and CGPAs of students whose CGPA matches the maximum CGPA found in the `Student_Info` table.
   
2. **Blue Box (Worked Example):** The worked example shows the result of the query, which is `| ID | CGPA | | --- | --- | | 110112 | 3.98 |`. This indicates that the student with ID 110112 has the highest CGPA of 3.98.

The lecturer explained: "so, etama ki korbe? select kortese cg max of cgpa. mane cgpa ekhane amar path ta row ache. so, ei path ta modhhe compare kore dekhbe jekhane max kora. ekhane max konta 3.98. so, ekhane amar return korbe 3.98. simple."

### Background
A subquery in SQL is a query nested inside another query. It allows you to perform complex data retrieval tasks by breaking down the process into smaller, manageable parts. In this case, the subquery finds the maximum CGPA, and the outer query uses this value to find the corresponding student details. This technique is useful when you need to filter data based on a calculated value or aggregate function.

**Remember:** The SQL query uses a subquery to first find the maximum CGPA and then selects the student information where the CGPA matches this maximum value.

---

## Check yourself
1. What does the `SELECT` command do?
2. How do you select all columns from a table?
3. How do you select specific columns from a table?
4. What is the purpose of the `WHERE` clause in a `SELECT` statement?
5. What does the `MAX` function do?

### Answers
1. The `SELECT` command is used to retrieve data from a database table.
2. You select all columns from a table by using the asterisk (`*`), e.g., `SELECT * FROM Student_Info`.
3. You select specific columns from a table by listing their names, e.g., `SELECT First_Name, Last_Name FROM Student_Info`.
4. The `WHERE` clause is used to apply conditions to retrieve specific rows based on certain criteria.
5. The `MAX` function returns the highest value in a specified column, e.g., `SELECT MAX(CGPA) FROM Student_Info`.

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9_007` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
