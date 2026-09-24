# BanglaASR9_007
Ek line e: Database Management System (DBMS) er moddhe SQL query er kaj korechi.

## Key takeaways
- `SELECT * FROM student_info;` retrieves all data from the `student_info` table.
- `SELECT CGPA FROM student_info WHERE ID = 401201;` retrieves the `CGPA` of the student with `ID 401201`.
- `SELECT First_Name, Last_Name FROM student_info WHERE ID = 202011;` retrieves the `First_Name` and `Last_Name` of the student with `ID 202011`.
- `SELECT Department FROM student_info WHERE ID = 151216;` retrieves the `Department` of the student with `ID 151216`.
- `SELECT MAX(CGPA) FROM student_info;` finds the maximum `CGPA` in the `student_info` table.
- `SELECT ID FROM student_info ORDER BY ID ASC;` orders the `ID` in ascending order.
- `SELECT ID FROM student_info ORDER BY ID DESC;` orders the `ID` in descending order.
- The SQL query `select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` selects the ID and CGPA from the `Student_Info` table where the CGPA is the maximum.
- To find the minimum CGPA, use `select ID, CGPA from Student_Info where CGPA=(select min(CGPA) from Student_Info);`.
- To find the average CGPA, use `select avg(CGPA) from Student_Info;`.
- To find the ID of the student with the maximum CGPA, use `select ID from Student_Info where CGPA = (select max(CGPA) from Student_Info);`.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Board 1 of 2, on the whiteboard during 0:10-9:10
**Ek line e:** Database Management System (DBMS)

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


1. **Database Management System (DBMS):**
   - The lecturer showed a table named `Student_Info` containing details like `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.

2. **SQL Query:**
   - The lecturer introduced the `SELECT` command, explaining that it is the most used and important command in SQL for retrieving data from a database.

3. **Selecting Data:**
   - To retrieve all data from a specific table, you start with the `SELECT * FROM` command followed by the table name. For example, `SELECT * FROM student_info;` will display the entire table.
   - To retrieve specific data, such as the `CGPA` of a student with `ID 401201`, you use `SELECT CGPA FROM student_info WHERE ID = 401201;`.
   - Similarly, to get the `First_Name` and `Last_Name` of a student with `ID 202011`, you would use `SELECT First_Name, Last_Name FROM student_info WHERE ID = 202011;`.
   - To get the `Department` of a student with `ID 151216`, you would use `SELECT Department FROM student_info WHERE ID = 151216;`.

4. **Aggregation Functions:**
   - The lecturer mentioned some common aggregation functions like `MAX`, `MIN`, `SUM`, and `AVG`. These functions can be used to perform operations on the data.
   - For example, to find the maximum `CGPA` in the `Student_Info` table, you would use `SELECT MAX(CGPA) FROM student_info;`.

5. **Ordering Data:**
   - To order the results, you can use the `ORDER BY` clause. For instance, to order the `ID` in ascending order, you would use `SELECT ID FROM student_info ORDER BY ID ASC;`.
   - To order the `ID` in descending order, you would use `SELECT ID FROM student_info ORDER BY ID DESC;`.

**Mone rakho:** 
- `SELECT * FROM student_info;` retrieves all data from the `student_info` table.
- `SELECT CGPA FROM student_info WHERE ID = 401201;` retrieves the `CGPA` of the student with `ID 401201`.
- `SELECT First_Name, Last_Name FROM student_info WHERE ID = 202011;` retrieves the `First_Name` and `Last_Name` of the student with `ID 202011`.
- `SELECT Department FROM student_info WHERE ID = 151216;` retrieves the `Department` of the student with `ID 151216`.
- `SELECT MAX(CGPA) FROM student_info;` finds the maximum `CGPA` in the `student_info` table.
- `SELECT ID FROM student_info ORDER BY ID ASC;` orders the `ID` in ascending order.
- `SELECT ID FROM student_info ORDER BY ID DESC;` orders the `ID` in descending order.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query Explanation
**Ek line e:** This query selects the ID and CGPA from the Student_Info table where the CGPA is equal to the maximum CGPA in the table.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


- **Box 1 (red):** The SQL query `select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` is shown. This query selects the ID and CGPA from the Student_Info table where the CGPA is equal to the maximum CGPA in the table.

- **Box 2 (blue):** The worked example shows a table with two rows: 
  | ID | CGPA |
  | --- | --- |
  | 110112 | 3.98 |

The lecturer explains that the query will find the ID and CGPA where the CGPA is the maximum. In this case, the maximum CGPA is 3.98, so the query returns the row with ID 110112 and CGPA 3.98.

> Lecturer: "so, etama ki korbe? select kortese cg max of cgpa. mane cgpa ekhane amar path ta row ache."

The lecturer further explains that if we want to find the minimum CGPA, we can modify the query to `select ID, CGPA from Student_Info where CGPA=(select min(CGPA) from Student_Info);`.

To find the average CGPA, the lecturer suggests using the `avg()` function. For example, the query would be `select avg(CGPA) from Student_Info;`.

> Lecturer: "tahole ki korbe? ei cgp-e gular average ber korbe. tahole first e ki? shob gula ke sum korte hoy average ber korar jonno, sum korar pore ekhane amar total value kore ta ajta. to divided by five kore je result er ashbe, setai kintu ami."

The lecturer also mentions that we can use nested queries to find the ID of the student with the maximum CGPA. The query would be `select ID from Student_Info where CGPA = (select max(CGPA) from Student_Info);`.


The lecturer concludes by explaining that these queries help us retrieve data from a table in a database, such as finding the student with the highest CGPA or calculating the average CGPA.

**Mone rakho:** The SQL query selects the ID and CGPA from the Student_Info table where the CGPA is the maximum. The worked example shows how the query works with a sample dataset. The lecturer explains how to find the minimum CGPA, calculate the average CGPA, and find the ID of the student with the maximum CGPA using nested queries.

---

## Check yourself
1. What does the SQL query `SELECT * FROM student_info;` do?
2. How would you retrieve the `CGPA` of a student with `ID 401201`?
3. What is the purpose of the `WHERE` clause in an SQL query?
4. How can you find the maximum `CGPA` in the `Student_Info` table?
5. What does the `ORDER BY` clause do in an SQL query?

### Answers
1. It retrieves all data from the `student_info` table.
2. You would use `SELECT CGPA FROM student_info WHERE ID = 401201;`.
3. It filters the rows based on a specified condition.
4. You would use `SELECT MAX(CGPA) FROM student_info;`.
5. It orders the results based on a specified column in ascending or descending order.

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9_007` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 1 removed. References to boxes that do not exist: 0.*
