# Database Management System (DBMS)
This lecture introduces the concept of a Database Management System (DBMS) and explains its basic functionality, including how to create tables and define data types using SQL commands.

## Key takeaways
- A Database Management System (DBMS) is a software system designed to manage databases.
- To create a table in a database, use SQL commands to define columns and their data types.
- Correctly defining data types ensures accurate storage and retrieval of data.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Introduction to Database Management System (DBMS)
**In one line:** This board introduces the concept of a Database Management System (DBMS) and explains its basic functionality.

![Board 1: 0:00-0:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Block diagram · 3 Block diagram


- **Box 1 (red):** The title "Database Management System (DBMS)" is displayed, indicating the topic of discussion.
- **Box 3 (orange):** The lecturer explains that a database can store multiple tables, each containing relevant information. These tables can be used to perform various operations such as running different types of software and improving system performance.
- The lecturer gives an example of a simple table to illustrate how a database works. They emphasize that databases are crucial in the digital world, especially on the internet.

>The lecturer said: "so, amader internet er ba amader aa amader ei digital word a database er importance kintu onek." This means: "So, in our internet and in our digital world, the importance of databases is significant."

### Background
A Database Management System (DBMS) is a software system designed to manage databases. It allows users to create, read, update, and delete data stored in a database efficiently. DBMS ensures data integrity, security, and provides a structured way to manage large amounts of data. In the digital age, where data is the new oil, understanding and utilizing DBMS is essential for managing and retrieving information effectively.

**Remember:** A database is a collection of organized data that can be accessed, managed, and updated.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Creating a Table in a Database
**In one line:** This board explains how to create a table in a database using SQL commands.

![Board 2: 1:10-10:50](figures_annotated/board_era2_110.jpg)

*Figure 2. The whiteboard during 1:10–10:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 SQL query · 3 Column header · 4 Column header


1. **Database Name**: The lecturer starts by naming the database as "University". This database will contain a table named `Student_info`.
2. **Table Creation**: The lecturer writes the SQL command to create the `Student_info` table. The table includes columns such as `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
3. **Column Headers**: The lecturer explains that each column represents a specific piece of information about a student. For example, `ID` is a unique identifier, `First_Name` and `Last_Name` store the student's name, `CGPA` stores the cumulative grade point average, `Department` stores the student's department, and `Enrollment_Date` stores the date of enrollment.
4. **Data Types**: The lecturer specifies the data types for each column. For instance, `ID` is an integer (`INT`), while `First_Name` and `Last_Name` are strings (`VARCHAR`).

> The lecturer said: "so first e amar ekta database er nam dite hobe, suppose database er nam hocche university."

### Background
A database management system (DBMS) is used to store, manage, and retrieve large amounts of data efficiently. In this case, we are creating a table to store information about students, including their IDs, names, CGPA, department, and enrollment date. This table structure allows us to organize and access data systematically, making it easier to perform operations like querying, updating, and deleting records.

**Remember:** The key point is understanding how to define and create a table in a database using SQL commands, specifying appropriate data types for each column.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Creating a Table with Data Types in DBMS
**In one line:** This board explains how to define data types for columns in a database table using SQL.

![Board 3: 11:00-13:00](figures_annotated/board_era3_1100.jpg)

*Figure 3. The whiteboard during 11:00–13:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 SQL query · 2 Table


1. **Red Box 1 (SQL Query):**
   - The lecturer said: "varchar hocche variable characters. so eikhane first name and second name doitai kintu amar sob somoy ekta character er variable e thakbe. so dui jaigate ami virtual likhe dilam. varchar likhar shathe amar eikhang kar kichu length ta fix kore dite hoy. jemon ami ekhane koto maximum, koto length er akta nam rakhte hobe."
   - In English, this means: "varchar is a variable character type. Here, first name and last name can be different, but we need to define a single character variable. So, I will virtually write it as varchar. When using varchar, we need to fix a certain length. For example, we can set the maximum length."

2. **Blue Box 2 (Table):**
   - The lecturer said: "suppose dhorlam ten karon ekta student er aa nam er moddhe, up to to ten character e thakte pare, er beshi usually hoy na. so, ten likhi dilam. tar mane holo, ekhane amar aa up to ten length er sob nam consider kora jabe. okay. then cgpa. cgpa te ki thakbe? amar float numbers. so eta jonno, eta data type hobe float."
   - In English, this means: "suppose a student's name can have up to ten characters, more than that is rare. So, I will set the length to ten. This means, here we will consider all names up to ten characters. Okay. Then CGPA. What should CGPA be? It should be floating-point numbers. So, for this, the data type should be float."

3. **Blue Box 2 (Table):**
   - The lecturer said: "department. department o kintu first name ar last name er matoi. so eta teo ami likhbo, word char. etar character limitation dey dela maximum 15 porjonto, for example. ar enrollment date. since eta ekta date, date naame amader eski bole, alata ekta data type e ache. so eta ar data type ta hobe dead."
   - In English, this means: "department. department is similar to first name and last name. So, I will write it as word char. We will set the character limit to a maximum of 15, for example. And enrollment date. Since it is a date, we call it date, which is a data type. So, the data type for this should be date."

4. **Blue Box 2 (Table):**
   - The lecturer said: "eta likhle automatically ebhabe date format e amr skula cholo ashbo. so, eight er je five-s packet ta start with chilo, etake end kore dibo. and last ekta semikron diye dibo."
   - In English, this means: "when we write this, it will automatically be in a date format. So, I will start with the five-character packet, and end it there. Finally, I will put a semicolon."

5. **Blue Box 2 (Table):**
   - The lecturer said: "so, ajker class e amra dekhlam, aa dbms ki, db mh ki babe kaaj kore, dbms er trivel ki bhabe create korte hoye chhu sql. so next class e amra aro kichu operations kula dekhbo."
   - In English, this means: "so, in this class, we see how DBMS and DB MH work, and how to create them using SQL. In the next class, we will see some other operations."

**Remember:** The key point is to correctly define data types for each column in a database table to ensure accurate storage and retrieval of data.

---

## Check yourself
1. What is a Database Management System (DBMS)?
2. How do you create a table in a database using SQL?
3. What are the data types specified for the `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date` columns in the `Student_info` table?

### Answers
1. A Database Management System (DBMS) is a software system designed to manage databases.
2. To create a table in a database using SQL, you use the `CREATE TABLE` command followed by the table name and column definitions.
3. The data types specified are: `ID` - INT, `First_Name` and `Last_Name` - VARCHAR, `CGPA` - FLOAT, `Department` - VARCHAR, and `Enrollment_Date` - DATE.

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. The lecturer's words are given in English translation (2 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
