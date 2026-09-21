# Lecture Notes: Database Management System (DBMS)

## Introduction to DBMS
- **Definition**: A Database Management System (DBMS) is a software system designed to manage databases. It allows users to create, maintain, and manage databases efficiently.
- **Key Concepts**:
  - **Database**: A collection of organized data stored and accessed electronically.
  - **Management**: The process of organizing and maintaining the database.
  - **System**: The overall framework and structure that supports the database operations.


![Figure 1](figures/fig_01_000.jpg)

**Figure 1.** Board during: Introduction to DBMS Frame at 0:00. Highlighted: Database Management System, Database, Management, System.

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


![Figure 2](figures/fig_02_240.jpg)

**Figure 2.** Board during: Explanation: Frame at 2:40. Highlighted: Enrollment Date, Enrollment, Date.

## Key Concepts in DBMS
- **MySQL**: A popular relational database management system that uses SQL (Structured Query Language) for creating and managing databases.
- **Query Language**: A language used to interact with the database, allowing users to perform various operations like creating tables, inserting data, updating records, and retrieving information.


![Figure 3](figures/fig_03_410.jpg)

**Figure 3.** Board during: Key Concepts in DBMS Frame at 4:10. Highlighted: Syed, Ahsan, Adil.

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


![Figure 4](figures/fig_04_550.jpg)

**Figure 4.** Board during: Example Data Insertion Frame at 5:50. Highlighted: Nasir.

## Summary
- **DBMS Overview**: A system for organizing and managing databases.
- **Key Components**: Database, Management, System.
- **SQL Commands**: Used for creating tables, inserting data, updating, and deleting records.
- **Example Table**: `StudentInfo` with fields like `student_id`, `first_name`, `last_name`, `cgpa`, `department`, and `enrollment_date`.

This lecture provided a foundational understanding of DBMS, focusing on the creation and management of a simple database using MySQL and SQL.

![Figure 5](figures/fig_05_600.jpg)

**Figure 5.** Board during: Summary Frame at 6:00. Highlighted: Istro.


![Figure 5](figures/fig_05_600.jpg)

**Figure 5.** Board during: Summary Frame at 6:00. Highlighted: Istro.


---

## Figure Index

| Figure | Time | Section | Source |
|---|---|---|---|
| 1 | 0:00 | Introduction to DBMS | keywords |
| 2 | 2:40 | Explanation: | keywords |
| 3 | 4:10 | Key Concepts in DBMS | keywords |
| 4 | 5:50 | Example Data Insertion | keywords |
| 5 | 6:00 | Summary | keywords |
