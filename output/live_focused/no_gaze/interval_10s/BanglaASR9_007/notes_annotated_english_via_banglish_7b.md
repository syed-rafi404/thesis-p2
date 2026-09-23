# BanglaASR9_007
The lecture covers the basics of SQL queries and how to use them to retrieve and manipulate data from a database table named `Student_Info`.

## Key takeaways
- `SELECT * FROM Student_Info;` retrieves all columns.
- `SELECT CGPA FROM Student_Info WHERE ID = 401201;` retrieves the CGPA of a specific student.
- `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 110112;` retrieves the first and last names of a specific student.
- `SELECT Department FROM Student_Info WHERE ID = 151216;` retrieves the department of a specific student.
- `SELECT ID FROM Student_Info;` retrieves all student IDs.
- `SELECT ID FROM Student_Info ORDER BY ID ASC;` sorts IDs in ascending order.
- `SELECT ID FROM Student_Info ORDER BY ID DESC;` sorts IDs in descending order.
- `SELECT MAX(CGPA) FROM Student_Info;` finds the maximum CGPA in the table.
- The lecturer said: "`select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` finds the student with the highest CGPA."

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Board 1 of 2, on the whiteboard during 0:10-9:10

**Ek line e:** Database Management System (DBMS) University

![Board 1: 0:10-9:10](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Database Management System · 2 SQL query


1. **Red Box 1**: This box shows a table named `Student_Info` containing details of students such as ID, First Name, Last Name, CGPA, Department, and Enrollment Date.
    - | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
    - |----|------------|-----------|-------|------------|-----------------|
    - | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
    - | 151216 | Ahsan | Habib | 2.77 | M-LH | 20-09-2024 |
    - | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
    - | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
    - | 401201 | Israt | Jahan | 3.40 | MicroBiology | 11-11-2025 |

2. **Blue Box 2**: This box lists some SQL commands: `max()`, `min()`, and `sum()`.

### Explanation
The lecturer introduces the concept of a Select query, which is a fundamental and widely used SQL command. A Select query allows us to retrieve specific data from a database table.

- **Step 1**: The lecturer explains that the `select` keyword is used to fetch data from a table. For example, if we want to see the full details of a student with ID 401201, we would use the following command:
  ```sql
  SELECT * FROM Student_Info;
  ```
  Here, the asterisk (`*`) represents all columns in the table.

- **Step 2**: To retrieve specific columns, we can specify the column names after the `SELECT` keyword. For instance, to get the CGPA of a student with ID 401201, we use:
  ```sql
  SELECT CGPA FROM Student_Info WHERE ID = 401201;
  ```

- **Step 3**: The lecturer demonstrates how to retrieve multiple columns using a comma-separated list. For example, to get the first name and last name of a student with ID 110112, we use:
  ```sql
  SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 110112;
  ```

- **Step 4**: To retrieve a specific column like the department, we use:
  ```sql
  SELECT Department FROM Student_Info WHERE ID = 151216;
  ```

- **Step 5**: The lecturer emphasizes the importance of matching the exact column names. For example, if the column name is `Department` and not `department`, the query will not work.

- **Step 6**: To retrieve all student IDs, we use:
  ```sql
  SELECT ID FROM Student_Info;
  ```

- **Step 7**: The lecturer explains how to sort the results in ascending or descending order using the `ORDER BY` clause. For example, to sort the IDs in ascending order:
  ```sql
  SELECT ID FROM Student_Info ORDER BY ID ASC;
  ```
  And to sort in descending order:
  ```sql
  SELECT ID FROM Student_Info ORDER BY ID DESC;
  ```

- **Step 8**: The lecturer introduces aggregation functions like `max()`, `min()`, and `sum()`. For example, to find the maximum CGPA in the table:
  ```sql
  SELECT MAX(CGPA) FROM Student_Info;
  ```

>The lecturer said: "To select a particular column, you have to specify the column name. If you want to get the CGPA of a particular student, you have to write `SELECT CGPA FROM Student_Info WHERE ID equals to that particular ID`."

**Mone rakho:**
- `SELECT * FROM Student_Info;` retrieves all columns.
- `SELECT CGPA FROM Student_Info WHERE ID = 401201;` retrieves the CGPA of a specific student.
- `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 110112;` retrieves the first and last names of a specific student.
- `SELECT Department FROM Student_Info WHERE ID = 151216;` retrieves the department of a specific student.
- `SELECT ID FROM Student_Info;` retrieves all student IDs.
- `SELECT ID FROM Student_Info ORDER BY ID ASC;` sorts IDs in ascending order.
- `SELECT ID FROM Student_Info ORDER BY ID DESC;` sorts IDs in descending order.
- `SELECT MAX(CGPA) FROM Student_Info;` finds the maximum CGPA in the table.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query and Worked Example
**Ek line e:** This board explains an SQL query to find the maximum CGPA and the corresponding student ID.

![Board 2: 9:20-16:20](figures_annotated/board_era2_920.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Worked example


1. **Red Box (Box 1):** The SQL query `select ID, CGPA from Student_Info where CGPA=(select max(CGPA) from Student_Info);` is shown. This query selects the IDs and CGPAs of students whose CGPA is equal to the maximum CGPA in the `Student_Info` table.

2. **Blue Box (Box 2):** The worked example shows the result of the query:
   | ID | CGPA |
   |----|------|
   | 110112 | 3.98 |

### Explanation
1. **Finding Maximum CGPA:**
   - The inner query `(select max(CGPA) from Student_Info)` finds the highest CGPA in the `Student_Info` table.
   - The outer query `select ID, CGPA from Student_Info where CGPA = (select max(CGPA) from Student_Info);` filters the rows in the `Student_Info` table to find the student(s) with the maximum CGPA.

2. **Example Walkthrough:**
   - The table on the board lists student IDs and their CGPAs.
   - The query returns the ID and CGPA of the student with the highest CGPA, which is 110112 with a CGPA of 3.98.

3. **Understanding the Query:**
   - The lecturer said: "The query is used to find the student with the highest CGPA."
   - The lecturer also mentioned that if we want to find the minimum CGPA, we can use a similar query but with `min(CGPA)` instead of `max(CGPA)`.

4. **Average Calculation:**
   - The lecturer briefly mentioned that we can calculate the average CGPA using a similar approach by summing up all CGPAs and dividing by the number of students.

5. **Nested Queries:**
   - The lecturer explained that nested queries are used when we need to perform multiple operations on the data, such as finding the student with the highest CGPA and then retrieving their details.

**Mone rakho:** The query selects the student with the highest CGPA and returns their ID and CGPA. The blue box shows the result of the query, which is the student ID 110112 with a CGPA of 3.98.

---

## Check yourself
1. Write the SQL query to retrieve all columns from the `Student_Info` table.
2. Write the SQL query to get the CGPA of a student with ID 401201.
3. Write the SQL query to get the first and last names of a student with ID 110112.
4. Write the SQL query to get the department of a student with ID 151216.
5. Write the SQL query to get all student IDs.

### Answers
1. `SELECT * FROM Student_Info;`
2. `SELECT CGPA FROM Student_Info WHERE ID = 401201;`
3. `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 110112;`
4. `SELECT Department FROM Student_Info WHERE ID = 151216;`
5. `SELECT ID FROM Student_Info;`

---

*This lecture is `BanglaASR13` in the dataset (`BanglaASR9_007` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
