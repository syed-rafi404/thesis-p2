# Database Management System (DBMS)

One sentence: This lecture introduces the basics of Database Management Systems (DBMS) and demonstrates how to create a simple database using SQL.

## Key takeaways
- A database can consist of multiple tables.
- MySQL is a query language used to interact with databases.
- Tables have columns like `student_id`, `first_name`, `last_name`, `cgpa`, `department`, and `enrollment_date`.
- Data types include `VARCHAR` for text and `FLOAT` for numerical values.
- SQL commands are used to create, manipulate, and manage tables.

## Introduction to Database Management System (DBMS)
- **Core Idea**: A DBMS is a system that allows users to create, manage, and manipulate databases.
- **Example**: Consider a database named `University` with a table named `student_info`.

![Board 1:10-10:50](figures_board/board_01_era2.jpg)

*Figure 1. The whiteboard during 1:10–10:50, reconstructed from 5 video frames with the lecturer removed; 100% of the board is unobstructed.*

### Creating a Table
- **Core Idea**: To create a table, we use SQL commands.
- **Example**: 
```sql
CREATE TABLE student_info (
    student_id VARCHAR(10),
    first_name VARCHAR(10),
    last_name VARCHAR(10),
    cgpa FLOAT,
    department VARCHAR(15),
    enrollment_date DATE
);
```
- **Explanation**: 
  - `student_id`: Unique identifier for each student.
  - `first_name`, `last_name`: Names of the students.
  - `cgpa`: Grade Point Average.
  - `department`: Department of the student.
  - `enrollment_date`: Date when the student enrolled.

### Watch out:
- Ensure that the data types match the expected values (e.g., `VARCHAR(10)` for names, `FLOAT` for CGPA).

## Check Yourself
1. What is a database management system?
2. Name the columns in the `student_info` table.
3. What is the purpose of the `VARCHAR` data type?
4. How do you create a table in SQL?
5. What is the difference between `VARCHAR` and `DATE`?

## Answers
1. A database management system (DBMS) is a system that allows users to create, manage, and manipulate databases.
2. Columns in the `student_info` table: `student_id`, `first_name`, `last_name`, `cgpa`, `department`, `enrollment_date`.
3. The `VARCHAR` data type is used for storing variable-length strings.
4. You create a table in SQL using the `CREATE TABLE` statement.
5. `VARCHAR` is used for text data, while `DATE` is used for storing date values.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*