# Lecture Notes: Database Management System (DBMS)

## Introduction to DBMS
- **Definition**: A Database Management System (DBMS) is a software system designed to manage databases. It allows users to create, maintain, and manage databases efficiently.
- **Key Concepts**:
  - **Database**: A collection of organized data stored and accessed electronically.
  - **Management**: The process of organizing and maintaining the database.
  - **System**: The overall framework and structure that supports the database operations.

## Example Table Creation Using MySQL
- **Example Database**: `University`
- **Table Name**: `StudentInfo`

### Creating the Table
- **SQL Command**:
  ```sql
  CREATE TABLE StudentInfo (
      student_id INT,
      first_name VARCHAR(100),
      last_name VARCHAR(100),
      cgpa DECIMAL(3,2),
      department VARCHAR(15),
      enrollment_date DATE
  );
  ```

### Explanation:
- **student_id**: Integer representing the unique identifier for each student.
- **first_name**: Variable string for the first name of the student (up to 100 characters).
- **last_name**: Variable string for the last name of the student (up to 100 characters).
- **cgpa**: Decimal type for the cumulative grade point average (up to 3 digits, 2 decimal places).
- **department**: Variable string for the department (up to 15 characters).
- **enrollment_date**: Date type for the date of enrollment.

## Key Concepts in DBMS
- **MySQL**: A popular relational database management system that uses SQL (Structured Query Language) for creating and managing databases.
- **Query Language**: A language used to interact with the database, allowing users to perform various operations like creating tables, inserting data, updating records, and retrieving information.


![Board 1:10-10:50](figures_board/board_01_era2.jpg)

**Figure 1.** Whiteboard as it stood during 1:10&ndash;10:50, reconstructed from 5 video frames with the lecturer removed. 100.0% of the board is unobstructed.

## Operations in DBMS
- **Creating Tables**: Using SQL commands to define the structure of the database.
- **Inserting Data**: Adding new records to the table.
- **Updating Data**: Modifying existing records in the table.
- **Deleting Data**: Removing records from the table.

## Example Data Insertion
- **SQL Command**:
  ```sql
  INSERT INTO StudentInfo (student_id, first_name, last_name, cgpa, department, enrollment_date)
  VALUES (110112, 'Syed', 'Ahsan', 3.5, 'Computer Science', '2021-09-01');
  ```

## Summary
- **DBMS Overview**: A system for organizing and managing databases.
- **Key Components**: Database, Management, System.
- **SQL Commands**: Used for creating tables, inserting data, updating, and deleting records.
- **Example Table**: `StudentInfo` with fields like `student_id`, `first_name`, `last_name`, `cgpa`, `department`, and `enrollment_date`.

This lecture provided a foundational understanding of DBMS, focusing on the creation and management of a simple database using MySQL and SQL.

---

*Figures are reconstructed whiteboards. Each is assembled from tiles taken from moments when the lecturer was not standing in front of that part of the board, so every pixel is unmodified video; nothing is generated. A figure shows the board's state across the time range given, not a single instant. Boards less than 95% clear of the lecturer were left out (2 of 3 here).*
