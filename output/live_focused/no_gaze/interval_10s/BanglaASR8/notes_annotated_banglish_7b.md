# Database Management System (DBMS)
ei lecture e ki cover kora hoyeche Database Management System (DBMS) er introduction, database and table creation, and SQL queries.

## Key takeaways
- Database Management System (DBMS) is a system that holds and manages data across multiple tables.
- A database can store information in tables, each containing related data.
- Each table has columns representing specific attributes, such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
- SQL is used to create and manipulate databases and tables.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Database Management System (DBMS)
**Ek line e:** Database Management System (DBMS) is a system used to store and manage data.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


**Explanation:**
1. **Red Box 1 (Title):** The red box titled "Database Management System (DBMS)" introduces the topic. DBMS is a system that manages and stores data.
2. The lecturer explains that a database can hold multiple tables, each containing related data. For instance, you might have tables for customers, orders, and products.
3. Each table in the database contains information that is useful for various purposes, such as improving the performance of applications or running specific software.
4. The lecturer gives an example of a simple database to illustrate the concept, focusing on a single table.

> Lecturer: "so, amader internet er ba amader aa amader ei digital word a database er importance kintu onek."

**Mone rakho:** Database Management System (DBMS) is a system that holds and manages data across multiple tables. Each table contains relevant information that can be used for different applications.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Database Management System (DBMS)
**Ek line e:** Database Management System (DBMS) is used to manage and organize data efficiently.

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


**Explanation:**
1. **Database Creation**: The lecturer started by creating a database named `university`. This database will store information about students.
2. **Table Creation**: In the `university` database, a table named `Student_info` was created. This table includes columns such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
3. **Column Headers**: The lecturer explained that each column represents a specific piece of information. For example, `ID` is a unique identifier for each student, `First_Name` and `Last_Name` store the student's full name, `CGPA` stores the student's cumulative grade point average, `Department` stores the student's academic department, and `Enrollment_Date` stores the date when the student enrolled.
4. **Dummy Data**: To illustrate, the lecturer provided some sample data for five students. Each student has a unique `ID`, a `First_Name`, a `Last_Name`, a `CGPA`, a `Department`, and an `Enrollment_Date`.

> Lecturer: "so first e amar ekta database er nam dite hobe, suppose database er nam hocche university."

**Mone rakho:** The lecturer demonstrated how to create a table named `Student_info` with columns for `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`. Each column represents a specific attribute of a student, and the table can store multiple rows of data representing different students.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query and Table Creation
**Ek line e:** Create table Student_info using SQL.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


1. **Red Box 1 (SQL Query):** The lecturer explained that `varchar` stands for variable characters. In the `Student_info` table, we define `First_Name` and `Last_Name` as `varchar`, but we can also use a single character variable if needed. To specify a fixed length, we use a number after `varchar`. For instance, we set the maximum length to 10 characters for `First_Name` and `Last_Name`.

2. **Blue Box 2 (Table):** The lecturer provided an example table with student information. Each row represents a student with their ID, first name, last name, CGPA, department, and enrollment date.

3. **Explanation of Data Types:**
   - **CGPA:** The lecturer mentioned that CGPA should be stored as a floating-point number (`float`).
   - **Department:** This field is treated similarly to `First_Name` and `Last_Name`, so the lecturer used `varchar` with a maximum length of 15 characters.
   - **Enrollment Date:** Since it is a date, the lecturer noted that the appropriate data type is `date`.

4. **Creating the Table:**
   - The SQL command to create the `Student_info` table is shown in the red box. It includes fields such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
   - The table structure is demonstrated in the blue box, showing sample data entries.

**Mone rakho:** The `Student_info` table is created using SQL commands, with specific data types like `varchar` and `float` for different fields. The table includes fields for student ID, names, CGPA, department, and enrollment date.

---

## Check yourself
1. What is a Database Management System (DBMS)?
2. Name two columns in the `Student_info` table.
3. What is the purpose of the `varchar` data type?
4. How is the `Enrollment_Date` column defined in the `Student_info` table?
5. What SQL command is used to create a table?

### Answers
1. Database Management System (DBMS) is a system that holds and manages data across multiple tables.
2. Two columns in the `Student_info` table are `First_Name` and `Last_Name`.
3. The `varchar` data type is used to store variable-length character strings.
4. The `Enrollment_Date` column is defined as `date`.
5. The SQL command used to create a table is `CREATE TABLE`.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
