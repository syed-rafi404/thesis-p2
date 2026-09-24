# Database Management System (DBMS)
ei lecture e ki cover kora hoyeche Database Management System (DBMS) er moddhe database er concept, SQL query er use, ar table creation process.

## Key takeaways
- Database Management System (DBMS) is a system used to manage and organize data.
- A database can store multiple tables, each containing related data.
- SQL is used to create tables in a database.
- Data types like `INT`, `VARCHAR`, `DECIMAL`, and `DATE` are used to define columns in a table.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Database Management System (DBMS)
**Ek line e:** Database Management System (DBMS) is a system used to manage and organize data.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


- **Red Box 1 (Database Management System (DBMS))**: The title clearly states our topic for today, which is Database Management System, often abbreviated as DBMS. This system helps us manage and organize large amounts of data efficiently.

- **Orange Box 3**: The lecturer starts by explaining what a database is. A database can store multiple tables, each containing related data. For instance, we might have a table for customer information, another for product details, and yet another for sales records. Each table holds specific information that is useful for various purposes such as improving performance and running different types of software.

- **Blue Box 2**: Although there is no block diagram in this box, the lecturer mentions that databases can store multiple tables. He uses an example to illustrate this point. Suppose we want to create a simple database for a small business. We would start by focusing on just one table, perhaps a table for customer information.

> Lecturer: "so, suppose amai ekta jihita amra ekta khub simple aa example diye start korbo, toh amra table o ami ekta gula multiple tables naniye, ami just ekta table e focus kori."

### Extra jana kotha (lecture e bola hoy ni)
Understanding the basics of a database is crucial. A database allows us to store and manage large volumes of data in a structured manner. By organizing data into tables, we can easily retrieve and manipulate information, which is essential for running efficient businesses and applications.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## SQL Query for Creating a Table: Database Management System
**Ek line e:** Create table Student_info( ID First_Name Last_Name)

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


1. **Red Box 1 (Title: Database Management System)**: Ami database er nam dite hobe. Amake university database er nam thakbe. Ei database er moddhe ekta table ache, setar nam student_info.
2. **Blue Box 2 (SQL query: Create table Student_info( ID First_Name Last_Name))**: Ami amake table er head dite hobe. Amake ID, First_Name, Last_Name column thakbe.
3. **Orange Box 3 (Column header: CGPA)**: Amake CGPA column thakbe.
4. **Green Box 4 (Column header: Enrollment_Date)**: Amake Enrollment_Date column thakbe.

> Lecturer: "so first e amar ekta database er nam dite hobe, suppose database er nam hocche university."

Amake amra first er ache student_id, erpor first_name, tarpore last_name thakte pare. Ard horo CGPA, department, ar enrollment_date thakte pare.

> Lecturer: "so eigula hocche amar table er head. toh etar moddhe amar sequentially kichu information sthor kora thakbe, right?"

Amake amra ekhane dummy data rakhlam. Amake amra kintu real life e billion ta information thakte pare. Amake amra ekhane kichu patch ta data rakhlam, ekhane kintu amra kintu unique id thakbe.

| ID | First_Name | Last_Name | CGPA | Enrollment_Date |
|----|------------|-----------|------|-----------------|
| 1  | John       | Doe       | 3.5  | 2022-01-01      |
| 2  | Jane       | Smith     | 3.8  | 2022-02-01      |

Amake amra amar table er head dite hobe. Amake amra amar table er data type ta dekha korte hobe. ID er moddhe integer thakbe, first name er modde string thakbe.

> Lecturer: "so, id. id te ki hobe? ekhane amar mostly thakbe shobshome ki? digits. so, ekhane amra likhte pari. integer. i n d. tarpore, first name. first name er je column ta ekhane ki thakbe? students der name thakbe. ekhon name ki diye tuiri hoy? different characters. abar name gula ki different length ero hoite pare. so characters er jonno amra, ekhane name ki thakbe?"

So, amar SQL query e:

```sql
CREATE TABLE Student_info(
    ID INT,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    CGPA DECIMAL(3,2),
    Enrollment_Date DATE
);
```

**Mone rakho:** ID, First_Name, Last_Name, CGPA, Enrollment_Date, SQL, CREATE TABLE, INT, VARCHAR, DECIMAL, DATE

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## SQL Query for Creating a Table: Database Management System
**Ek line e:** In this section, we will discuss the SQL query for creating a table in a database management system.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


- **Box 1 (red):** The SQL query for creating a table named `Student_info` is shown here. It includes fields such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.

```sql
MySQL->Query Language Create table Student_info(
    ID Int,
    First_Name VARCHAR(10),
    Last_Name VARCHAR(10),
    CGPA float,
    Department VARCHAR(15),
    Enrollment_Date Date
)
```

- **Box 2 (blue):** This is the table created using the above SQL query. It contains sample data for students.

| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|----|------------|-----------|------|------------|-----------------|
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
| 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
| 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |

**Explanation:**
1. **Box 1 (red):** The `VARCHAR` data type is used for storing variable-length strings. Here, `First_Name` and `Last_Name` are stored as `VARCHAR(10)`, meaning each can hold up to 10 characters. We can set a limit to ensure consistency.
2. **Box 1 (red):** For `CGPA`, we use the `float` data type because it stores floating-point numbers.
3. **Box 1 (red):** `Department` is also a string, but it can be longer than `First_Name` and `Last_Name`. Therefore, we set it to `VARCHAR(15)`.
4. **Box 1 (red):** `Enrollment_Date` is a date, so we use the `Date` data type. The date format is `YYYY-MM-DD`.
5. **Box 2 (blue):** This table shows the actual data entered into the `Student_info` table.

> Lecturer: "varchar hocche variable characters. so eikhane first name and second name doitai kintu amar sob somoy ekta character er variable e thakbe. so dui jaigate ami virtual likhe dilam.vurchar likhar shathe amar eikhang kar kichu length ta fix kore dite hoy. jemon ami ekhane koto maximum, koto length er akta nam rakhte hobe."

**Extra jana kotha (lecture e bola hoy ni):**
- When creating a table, we need to define the data types for each column carefully. For example, `VARCHAR` is used for text fields with a fixed maximum length, while `float` is used for numerical data like CGPA.
- The `Date` data type is specifically used for storing dates, ensuring that the data is formatted correctly and can be easily queried.

---

## Check yourself
1. What is a database?
2. What is the purpose of a database management system?
3. Write an SQL query to create a table named `Student_info` with columns `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
4. What is the difference between `VARCHAR` and `INT` data types?
5. How do you define a date in SQL?

### Answers
1. A database can store multiple tables, each containing related data.
2. The purpose of a database management system is to manage and organize data efficiently.
3. ```sql
   CREATE TABLE Student_info(
       ID INT,
       First_Name VARCHAR(255),
       Last_Name VARCHAR(255),
       CGPA DECIMAL(3,2),
       Department VARCHAR(255),
       Enrollment_Date DATE
   );
   ```
4. `VARCHAR` is used for storing variable-length strings, while `INT` is used for storing integers.
5. A date is defined using the `DATE` data type in SQL, with a format like `YYYY-MM-DD`.

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 5 kept, 0 removed. References to boxes that do not exist: 0.*
