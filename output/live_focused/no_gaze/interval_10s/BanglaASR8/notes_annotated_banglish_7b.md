# Database Management System (DBMS)
ei lecture e ki cover kora hoyeche database management system (DBMS) er introduction, SQL query er kaj, and table creation process.

## Key takeaways
- Database, DBMS, multiple tables, information, performance, software, digital world, example, single table
- `CREATE TABLE` is used to define a new table
- `INT`, `VARCHAR`, `FLOAT`, and `DATE` are data types used to specify the type of data each column can hold
- `VARCHAR` is used to store variable-length strings
- `float` is used to store floating-point numbers
- `Date` is used to store dates
- Semicolon at the end of the SQL statement signifies the end of the command

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Database Management System (DBMS)
**Ek line e:** Database Management System (DBMS) is a system used to store and manage data.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


- **Box 1 (red):** The title "Database Management System (DBMS)" is clearly mentioned. This introduces the topic we will be discussing today.

- **Explanation:** A database is a collection of data. In Box 1, the lecturer explains that a database can hold multiple tables. Each table contains information that is useful for various purposes, such as improving the performance of a computer system or running specific software applications.

- **Quote:** "so, ei data gula ki thakte pare? multiple tables a thakte pare." - The lecturer emphasizes that a database can contain multiple tables, each holding different types of data.

- **Extra jana kotha:** A database is essential in our digital world. For instance, imagine we have a simple example of a person's information. We can represent this information using a single table, focusing on one table for simplicity.

**Mone rakho:** Database, DBMS, multiple tables, information, performance, software, digital world, example, single table.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## SQL Query for Creating a Table: Database Management System
**Ek line e:** Create table Student_info( ID First_Name Last_Name)

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


The lecturer started by explaining that we need to create a database named `university`. Within this database, we will create a table called `Student_info` to store information about students. The table will have several columns: `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.

1. **ID**: This is the primary identifier for each student. We decided to use a combination of letters and numbers to ensure uniqueness. For example, `241412`, `151216`, etc.
2. **First_Name**: This column will store the first name of the student. Since names can vary in length and consist of different characters, we used the `VARCHAR` data type.
3. **Last_Name**: Similar to `First_Name`, this column will also use the `VARCHAR` data type to accommodate various last names.
4. **CGPA**: This column will store the Cumulative Grade Point Average of the student. We used the `FLOAT` data type to allow for decimal values.
5. **Department**: This column will store the department of the student. Again, using the `VARCHAR` data type to handle different department names.
6. **Enrollment_Date**: This column will store the date when the student enrolled. We used the `DATE` data type to store the date in a standard format.

The lecturer then showed an example of how the table would look with some dummy data:

| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|----|------------|-----------|------|------------|----------------|
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
| 151216 | Ahsan | Habib | 3.77 | Math | 20-09-2024 |
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
| 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |

> Lecturer: "so first e amar ekta database er nam dite hobe, suppose database er nam hocche university."

In real-life scenarios, a database might contain billions of records. The lecturer emphasized that while we are showing only a few rows here, in practice, there could be millions of entries.

> Lecturer: "so eigula hocche amar table er head. toh etar moddhe amar sequentially kichu information sthor kora thakbe, right?"

The lecturer explained that each row in the table represents a specific student, and we can retrieve various pieces of information such as their ID, name, CGPA, department, and enrollment date. This allows us to perform operations like querying, updating, inserting, and deleting data.

> Lecturer: "so, etai hocche query language er kaj. so, my sql er ami first a ei je table ta. ei table ta oto kono bhabe create kora hoye, right?"

SQL (Structured Query Language) is used to interact with databases. MySQL is one such implementation of SQL. The lecturer then demonstrated how to create the `Student_info` table using the `CREATE TABLE` statement:

```sql
CREATE TABLE Student_info (
    ID INT,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    CGPA FLOAT,
    Department VARCHAR(255),
    Enrollment_Date DATE
);
```

This command creates a table with the specified columns and data types. The lecturer highlighted that we can manipulate the table by adding, updating, or deleting rows and columns as needed.

**Mone rakho:** 
- `CREATE TABLE` is used to define a new table.
- `INT`, `VARCHAR`, `FLOAT`, and `DATE` are data types used to specify the type of data each column can hold.
- Each column in the table represents a piece of information about a student.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query for Creating a Table: Database Management System (DBMS)

**Ek line e:** In this section, we will learn how to create a table using SQL in a database management system.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


1. **Red Box 1 (SQL Query):** The lecturer showed an SQL query for creating a table named `Student_info`. The query is as follows:

   ```sql
   Create table Student_info(
       ID Int,
       First_Name Varchar(10),
       Last_Name Varchar(10),
       CGPA float,
       Department Varchar(15),
       Enrollment_Date Date
   );
   ```

2. **Blue Box 2 (Table):** The lecturer then displayed a table containing sample data for the `Student_info` table:

   | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
   |----|------------|-----------|------|------------|-----------------|
   | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
   | 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |
   | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
   | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
   | 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |

**Quotes:**
> Lecturer: "varchar hocche variable characters. so eikhane first name and second name doitai kintu amar sob somoy ekta character er variable e thakbe. so dui jaigate ami virtual likhe dilam."
> 
> Lecturer: "suppose dhorlam ten karon ekta student er aa nam er moddhe, up to to ten character e thakte pare, er beshi usually hoy na. so, ten likhi dilam."

### Extra jana kotha (lecture e bola hoy ni)
In the `First_Name` and `Last_Name` columns, we use `VARCHAR(10)` to store up to 10 characters. This is because typically, a person's first and last names do not exceed 10 characters. For `CGPA`, we use `float` to store decimal values. The `Department` column uses `VARCHAR(15)` to allow up to 15 characters, which is sufficient for most department names. `Enrollment_Date` is stored as a `Date` type, which is appropriate for storing dates.

**Mone rakho:** The `VARCHAR` data type is used to store variable-length strings, and the `float` data type is used to store floating-point numbers. The `Date` data type is used to store dates. The semicolon at the end of the SQL statement signifies the end of the command.

---

## Check yourself
1. What is a database?
2. What does the `CREATE TABLE` statement do?
3. Which data type is used to store variable-length strings?
4. How many characters can be stored in a `VARCHAR(10)` column?
5. What is the purpose of the semicolon at the end of an SQL statement?

### Answers
1. A database is a collection of data.
2. The `CREATE TABLE` statement is used to define a new table.
3. `VARCHAR` is used to store variable-length strings.
4. A `VARCHAR(10)` column can store up to 10 characters.
5. The semicolon at the end of an SQL statement signifies the end of the command.

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 5 kept, 0 removed. References to boxes that do not exist: 0.*
