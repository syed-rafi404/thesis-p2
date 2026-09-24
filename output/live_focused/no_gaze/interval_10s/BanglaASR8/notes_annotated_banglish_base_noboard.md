# Database Management System (DBMS)
Today's topic is Database Management System (DBMS).

## Key takeaways
- Database Management System (DBMS) is essential for managing large amounts of data efficiently.
- Databases allow us to organize, retrieve, and manipulate data using multiple tables.
- Understanding databases is crucial for developing robust software applications and managing information in the digital age.
- SQL commands are used to create tables and manage data within a database.
- The `CREATE TABLE` command is used to define the structure of a table, including column names and data types.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Database Management System (DBMS)
**Ek line e:** Today's topic is Database Management System (DBMS).

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


- **Box 1 (red):** The title of the board is "Database Management System (DBMS)".
- **Box 3 (orange):** The lecturer explains that a database holds data. He mentions that multiple tables are used to store this data, and all these tables are available for use. He uses these tables to improve performance and software functionality.
- **Lecturer:** "So, what do you need to do with these data? Multiple tables. So, I'll give you a comment. And these tables are all available. So, all these tables are all available to us. These tables are all available to us. I use these. I use these to use the performance, to use the software."

The lecturer emphasizes the importance of databases in our internet and digital world. He provides a simple example where he focuses on tables to illustrate how databases are utilized.

### Extra jana kotha (lecture e bola hoy ni)
- Databases are essential for managing large amounts of data efficiently.
- They allow us to organize, retrieve, and manipulate data using multiple tables.
- Understanding databases is crucial for developing robust software applications and managing information in the digital age.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## SQL Command for Creating a Table: Database Management System (DBMS)

**Ek line e:** Today, we will learn how to create a table in a database using SQL commands.

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


1. **Red Box 1 (Title):** Database Management System
2. **Blue Box 2 (SQL query):** `Create table Student_info( ID First_Name Last_Name)`
3. **Orange Box 3 (Column header):** CGPA
4. **Green Box 4 (Column header):** Enrollment_Date

The lecturer explained that a database named "university" contains a table called "student info." This table stores student information such as ID, first name, last name, CGPA, department, and enrollment date.

### Explanation:

1. **Creating the Table:**
   - The lecturer started by explaining that a database named "university" exists and contains a table called "student info."
   - To create this table, the lecturer wrote the SQL command: `Create table Student_info( ID First_Name Last_Name)`.
   - The `ID` column is used to uniquely identify each student.
   - The `First_Name` and `Last_Name` columns store the student's full name.

2. **Additional Columns:**
   - The lecturer mentioned that the table also includes columns for `CGPA`, `Department`, and `Enrollment_Date`.
   - These columns are added to the table using the same `CREATE TABLE` command format.

3. **Data Types:**
   - The lecturer emphasized that when creating a table, it is important to specify the data types for each column.
   - For example, the `ID` column is likely to be an integer or string, while `First_Name` and `Last_Name` would be strings.

4. **Dummy Data:**
   - The lecturer explained that in practice, the table would contain millions or billions of records.
   - As an example, the lecturer mentioned using IDs like 110 and 112 for demonstration purposes.

5. **Query Language:**
   - The lecturer noted that SQL is a query language used to interact with databases.
   - Unlike programming languages like Java or Python, SQL is specifically designed to query and manipulate data in databases.

6. **Creating the Table:**
   - The lecturer demonstrated the creation of the table using the following SQL command:
     ```sql
     Create table Student_info(
       ID int,
       First_Name varchar(255),
       Last_Name varchar(255),
       CGPA float,
       Department varchar(255),
       Enrollment_Date date
     );
     ```
   - Here, `int` is used for the `ID` column, `varchar(255)` for `First_Name` and `Last_Name`, `float` for `CGPA`, `varchar(255)` for `Department`, and `date` for `Enrollment_Date`.

### Extra jana kotha:
In a database management system, creating a table involves specifying the column names and their respective data types. This ensures that the data stored in the table is structured and can be efficiently queried. Understanding these basics is crucial for managing and manipulating data in a database.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Command for Creating a Table: Database Management System (DBMS)
**Ek line e:** In this section, we will learn how to create a table using SQL commands in a database management system.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


- **Red Box 1 (SQL Query):** The lecturer showed an SQL query for creating a table named `Student_info`. The query is as follows:
  ```sql
  CREATE TABLE Student_info(
    ID Int,
    First_Name VARCHAR(10),
    Last_Name VARCHAR(10),
    CGPA float,
    Department VARCHAR(15),
    Enrollment_Date Date
  );
  ```

- **Blue Box 2 (Table):** The lecturer then displayed a table containing sample data for the `Student_info` table:
  | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
  |----|------------|-----------|------|------------|-----------------|
  | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
  | 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |
  | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
  | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
  | 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |

**Explanation:**
- The lecturer explained that `VARCHAR` is used for storing variable-length strings. For `First_Name` and `Last_Name`, the lecturer suggested using `VARCHAR(10)` because each name is expected to be up to 10 characters long. However, `VARCHAR` can store any number of characters, so the lecturer mentioned that if more flexibility is needed, `VARCHAR` without a specific length can be used.
- The `CGPA` field is defined as `float`, which is appropriate for storing floating-point numbers like grades.
- The `Department` field is also defined as `VARCHAR(15)`, indicating that department names should not exceed 15 characters.
- The `Enrollment_Date` field is defined as `Date`, which is a data type in SQL used to store dates.

> Lecturer: "Suppose, for example, 10 students have to have up to 10 characters. So, 10 b. If you have to have to have up to 10, then you can consider them."

The lecturer further explained that the `CREATE TABLE` statement ends with a semicolon (`;`).

### Extra jana kotha (lecture e bola hoy ni)
In the next class, we will learn about the operations on rows within the table. This includes inserting, updating, and deleting records. Understanding these operations is crucial for managing data effectively in a database.

---

## Check yourself
1. What does a database hold?
2. How many columns are specified in the `Student_info` table?
3. What is the data type of the `ID` column in the `Student_info` table?
4. Which SQL command is used to create a table?
5. What is the purpose of the `CREATE TABLE` statement?

### Answers
1. A database holds data.
2. Five columns are specified in the `Student_info` table.
3. The `ID` column is of type `Int`.
4. The `CREATE TABLE` command is used to create a table.
5. The `CREATE TABLE` statement is used to define the structure of a table, including column names and data types.

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 0.*
