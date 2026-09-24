# Database Management System (DBMS)
Today's topic is Database Management System (DBMS).

## Key takeaways
- A database holds data and uses multiple tables to manage this data.
- Databases are essential in the internet and digital world.
- A DBMS is a system that manages the storage, retrieval, and management of data in a database.
- The `CREATE TABLE` statement in SQL is used to define the structure of a database table.
- Each column in a table serves a specific purpose, and the `ID` column is crucial for ensuring uniqueness.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Database Management System (DBMS)
**Ek line e:** Today's topic is Database Management System (DBMS).

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


- **Box 1 (red):** The title "Database Management System (DBMS)" is clearly stated.
- **Box 3 (orange):** The lecturer explains that a database holds data. He mentions that multiple tables are used to manage this data. He emphasizes that these tables are all available and can be used for various purposes like improving performance and using software.
- **Box 3 (orange):** The lecturer gives an example of starting with a simple table to understand how databases work. He stresses the importance of databases in our internet and digital world.

> Lecturer: "So, what do you need to do with these data? Multiple tables."

### Extra jana kotha (lecture e bola hoy ni)
Understanding the basics of a database involves recognizing that it is a structured collection of data organized into tables. Each table can hold different types of information, and these tables are interconnected to provide comprehensive data management. This structure allows for efficient querying and manipulation of data, which is crucial for modern applications and digital systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Database Management System (DBMS)
**Ek line e:** Database Management System (DBMS) is a system that manages the storage, retrieval, and management of data in a database.

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


1. **Box 1 (red):** The title "Database Management System" introduces us to the concept of managing data efficiently.
2. **Box 2 (blue):** The SQL query `CREATE TABLE Student_info(ID, First_Name, Last_Name)` demonstrates how to create a table named `Student_info` with specific columns.
3. **Box 3 (orange):** The column header `CGPA` stands for Cumulative Grade Point Average.
4. **Box 4 (green):** The column header `Enrollment_Date` represents the date when a student enrolled in the program.

The lecturer explained that a database named "university" contains a table called `Student_info`, which stores information about students. The table includes columns such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.

> Lecturer: "So, first time we have student ID, we have random numbers."

The `ID` column is a unique identifier for each student, ensuring that each student has a distinct entry in the database. The `First_Name` and `Last_Name` columns store the names of the students. The `CGPA` column holds the cumulative grade point average of the students, while the `Department` column indicates the academic department of the students. The `Enrollment_Date` column records the date when the student enrolled in the program.

The lecturer then showed a table with sample data:

| ID    | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|-------|------------|-----------|------|------------|----------------|
| 241412 | Syed       | Rafi      | 3.55 | CS         | 01-01-2024      |
| 151216 | Ahsan      | Habib     | 3.77 | Math       | 20-09-2024      |
| 202011 | Adiba      | Noshin    | 3.28 | Economics  | 21-10-2021      |
| 110112 | Maria      | Islam     | 3.98 | English    | 02-02-2020      |
| 401201 | Istrat     | Jahan     | 3.40 | MicroBiology | 11-11-2025      |

This table illustrates how the `Student_info` table can store various pieces of information about students. The lecturer emphasized that the `ID` column is crucial as it ensures uniqueness among students.

> Lecturer: "It's a very fascinating column."

The `ID` column is indeed unique and essential for identifying individual students. The `First_Name` and `Last_Name` columns provide the names of the students, while the `CGPA` column stores their academic performance. The `Department` column specifies the academic department, and the `Enrollment_Date` column records the date of enrollment.

### Extra jana kotha (lecture e bola hoy ni)
Understanding the structure of a database table is fundamental in managing data effectively. Each column in a table serves a specific purpose, and the `ID` column is particularly important for ensuring that each record is uniquely identifiable. This knowledge helps in designing efficient and effective database systems.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query in Database Management System (DBMS)
**Ek line e:** This is how we create a table in SQL using MySQL.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


1. **Red Box 1 (SQL Query):** The lecturer showed the SQL query to create a table named `Student_info`. The query includes fields like `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.

   ```sql
   MySQL->Query Language
   Create table Student_info(
       ID Int,
       First_Name Varchar(10),
       Last_Name Varchar(10),
       CGPA float,
       Department Varchar(15),
       Enrollment_Date Date
   );
   ```

2. **Blue Box 2 (Table):** The lecturer then displayed a table filled with sample data for the `Student_info` table.

   | ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
   |----|------------|-----------|------|------------|-----------------|
   | 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
   | 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |
   | 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
   | 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
   | 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |

**Explanation:**
- **Red Box 1 (SQL Query):** The lecturer explained that `VARCHAR` is used for storing variable-length strings. For `First_Name` and `Last_Name`, since each name can have up to 10 characters, `VARCHAR(10)` was used. However, `VARCHAR` can store any number of characters, so the lecturer suggested using `VARCHAR` even if the maximum length is known.
- **Red Box 1 (SQL Query):** The `CGPA` field is defined as `float`, which is used for storing floating-point numbers.
- **Red Box 1 (SQL Query):** The `Department` field is also defined as `VARCHAR(15)`, meaning it can hold up to 15 characters.
- **Red Box 1 (SQL Query):** The `Enrollment_Date` field is defined as `Date`, which stores dates in the format `YYYY-MM-DD`.
- **Red Box 1 (SQL Query):** The query ends with a semicolon (`;`).

**Quotes:**
> Lecturer: "use kori varchar varchar hukkxhe variable characters so eekhaan e first name and second name ndoji taj kiintu aamar shabhshumoy aakta character e variable e thakte so dhuji jagaat e aamini varchar likhe dila varchar likhar sath e aamar eekhaan kar kichu length topics kore dita hoja jamon aam eekhaan e aaktsimam koto length e raka tata nama raka"

**Extra jana kotha (lecture e bola hoy ni):**
The `CREATE TABLE` statement in SQL is used to define the structure of a database table. Each field in the table has a specific data type, such as `INT` for integer, `VARCHAR` for variable-length strings, `FLOAT` for floating-point numbers, and `DATE` for dates. Understanding these data types is crucial for managing and querying data effectively.

---

## Check yourself
1. What does a database hold?
2. How many tables are typically used in a database?
3. What is the purpose of the `ID` column in a database table?
4. What data type is used for storing variable-length strings in SQL?
5. How is the `Enrollment_Date` stored in the `Student_info` table?

### Answers
1. A database holds data.
2. Multiple tables are typically used in a database.
3. The `ID` column is crucial for ensuring uniqueness among records.
4. The `VARCHAR` data type is used for storing variable-length strings in SQL.
5. The `Enrollment_Date` is stored as a `Date` in the `Student_info` table.

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_base.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
