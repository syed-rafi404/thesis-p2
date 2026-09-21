# SQL Queries and Data Retrieval

This lecture covers the basics of SQL queries, focusing on how to retrieve specific data from a database table.

## Key takeaways
- `SELECT` query is the most commonly used and important command in SQL.
- Use `*` to select all columns from a table.
- Use `WHERE` clause to filter specific rows based on conditions.
- Use `ORDER BY` to sort the results.
- Aggregation functions like `MAX`, `MIN`, `SUM`, and `AVG` can be used to perform calculations on data.

## SELECT Query
The `SELECT` query is used to retrieve data from a database table.

### Core Idea
- `SELECT` is used to fetch data from a specified table.
- The `*` symbol selects all columns from the table.
- The `WHERE` clause filters specific rows based on given conditions.
- The `ORDER BY` clause sorts the results.

### Worked Example
```sql
-- Select all data from the student_info table
SELECT * FROM student_info;

-- Select CGPA from the student_info table
SELECT CGPA FROM student_info;

-- Select CGPA where student ID is 401201
SELECT CGPA FROM student_info WHERE student_id = 401201;
```

![Board 0:10-9:10](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed from 13 video frames with the lecturer removed; 98% of the board is unobstructed.*

### Watch out:
- Ensure the column names are spelled correctly when using the `WHERE` clause.

### Worked Example with Sorting
```sql
-- Select all data from the student_info table and order by student ID
SELECT * FROM student_info ORDER BY student_id;

-- Select CGPA from the student_info table and order by student ID
SELECT CGPA FROM student_info ORDER BY student_id;
```

### Watch out:
- Pay attention to the case sensitivity of column names.

## Aggregation Functions
Aggregation functions are used to perform calculations on data.

### Core Idea
- `MAX`, `MIN`, `SUM`, and `AVG` are used to calculate the maximum, minimum, sum, and average of a column respectively.
- These functions can be combined with `SELECT` and `FROM` clauses.

### Worked Example
```sql
-- Find the maximum CGPA from the student_info table
SELECT MAX(CGPA) FROM student_info;

-- Find the minimum CGPA from the student_info table
SELECT MIN(CGPA) FROM student_info;

-- Calculate the sum of CGPA from the student_info table
SELECT SUM(CGPA) FROM student_info;

-- Calculate the average CGPA from the student_info table
SELECT AVG(CGPA) FROM student_info;
```

![Board 9:20-16:20](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed from 5 video frames with the lecturer removed; 99% of the board is unobstructed.*

### Watch out:
- Ensure the column name is correct when using aggregation functions.

## Nested Queries
Nested queries are used to combine multiple queries into a single query.

### Core Idea
- A nested query is a query within another query.
- The outer query can reference the inner query.

### Worked Example
```sql
-- Find the student ID and maximum CGPA from the student_info table
SELECT student_id, MAX(CGPA) FROM student_info;

-- Find the student ID and CGPA where CGPA is the maximum
SELECT student_id, CGPA FROM student_info WHERE CGPA = (SELECT MAX(CGPA) FROM student_info);
```

## Check Yourself
1. Write a query to select all data from the `student_info` table.
2. Write a query to select the CGPA from the `student_info` table where the student ID is 401201.
3. Write a query to find the maximum CGPA from the `student_info` table.
4. Write a query to find the minimum CGPA from the `student_info` table.
5. Write a query to find the average CGPA from the `student_info` table.

### Answers
1. `SELECT * FROM student_info;`
2. `SELECT CGPA FROM student_info WHERE student_id = 401201;`
3. `SELECT MAX(CGPA) FROM student_info;`
4. `SELECT MIN(CGPA) FROM student_info;`
5. `SELECT AVG(CGPA) FROM student_info;`

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*