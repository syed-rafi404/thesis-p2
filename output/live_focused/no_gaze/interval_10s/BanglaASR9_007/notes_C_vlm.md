# SQL Queries and Data Retrieval

In this lecture, we learned about SQL queries and how to retrieve specific data from a database table.

## Key takeaways
- `SELECT` query is the most commonly used and important command in SQL.
- Use `*` to select all columns in a table.
- Use `WHERE` clause to filter specific rows based on conditions.
- Aggregation functions like `MAX`, `MIN`, `SUM`, and `AVG` can be used to perform calculations on data.
- Nested queries can be used to retrieve complex data.

## SELECT Query
The `SELECT` query is used to retrieve data from a database table.

### Core Idea
The `SELECT` query allows you to specify which columns or all columns you want to retrieve from a table.

### Worked Example
- **Example**: Retrieve all data from the `student_info` table.
  ```sql
  SELECT * FROM student_info;
  ```

- **Example**: Retrieve the CGPA of a specific student with ID 401201.
  ```sql
  SELECT CGPA FROM student_info WHERE ID = 401201;
  ```

- **Example**: Retrieve the first name and last name of a specific student with ID 202011.
  ```sql
  SELECT first_name, last_name FROM student_info WHERE ID = 202011;
  ```

- **Example**: Retrieve the department of a specific student with ID 151216.
  ```sql
  SELECT department FROM student_info WHERE ID = 151216;
  ```

- **Example**: Retrieve all student IDs.
  ```sql
  SELECT ID FROM student_info;
  ```

- **Example**: Retrieve all student IDs in ascending order.
  ```sql
  SELECT ID FROM student_info ORDER BY ID ASC;
  ```

- **Example**: Retrieve all student IDs in descending order.
  ```sql
  SELECT ID FROM student_info ORDER BY ID DESC;
  ```

- **Example**: Retrieve the maximum CGPA from the `student_info` table.
  ```sql
  SELECT MAX(CGPA) FROM student_info;
  ```

- **Example**: Retrieve the minimum CGPA from the `student_info` table.
  ```sql
  SELECT MIN(CGPA) FROM student_info;
  ```

- **Example**: Retrieve the sum of all CGPAs from the `student_info` table.
  ```sql
  SELECT SUM(CGPA) FROM student_info;
  ```

- **Example**: Retrieve the average CGPA from the `student_info` table.
  ```sql
  SELECT AVG(CGPA) FROM student_info;
  ```

- **Example**: Retrieve the student ID and maximum CGPA from the `student_info` table.
  ```sql
  SELECT ID, MAX(CGPA) FROM student_info;
  ```

- **Example**: Retrieve the student ID and maximum CGPA from the `student_info` table using a subquery.
  ```sql
  SELECT ID, (SELECT MAX(CGPA) FROM student_info) AS max_cgpa FROM student_info;
  ```

- **Example**: Retrieve the student ID and maximum CGPA from the `student_info` table using a nested query.
  ```sql
  SELECT ID, (SELECT CGPA FROM student_info WHERE CGPA = (SELECT MAX(CGPA) FROM student_info)) AS max_cgpa FROM student_info;
  ```

[[FIGURE 1]]  board during 0:10-9:10: ```markdown Database Management System (DBMS) University | Student Info | | --- | --- | --- | --- | --- | --- | | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date | | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 | | 151216 | Ahsan | Habib | 3.77 | Math | 20-09-2024 | | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 | | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 | | 401201 | Israt | Jahan | 3.40 | MicroBiology | 11-11-2025 |

[[FIGURE 2]]  board during 9:20-16:20: ```markdown Database Management System (DBMS) University | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date | |----|------------|-----------|-------|-------------|-----------------| | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 | | 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 | | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 | | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 | | 401201 | Israt | Jahan | 3.40 | MicroBiology | 11-11-2025 |

## Check yourself
1. Write a query to retrieve all data from the `student_info` table.
2. Write a query to retrieve the CGPA of a student with ID 401201.
3. Write a query to retrieve the first name and last name of a student with ID 202011.
4. Write a query to retrieve the department of a student with ID 151216.
5. Write a query to retrieve all student IDs in ascending order.

## Answers
1. ```sql
   SELECT * FROM student_info;
   ```
2. ```sql
   SELECT CGPA FROM student_info WHERE ID = 401201;
   ```
3. ```sql
   SELECT first_name, last_name FROM student_info WHERE ID = 202011;
   ```
4. ```sql
   SELECT department FROM student_info WHERE ID = 151216;
   ```
5. ```sql
   SELECT ID FROM student_info ORDER BY ID ASC;
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*