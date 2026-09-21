# Database Management System (DBMS)

This lecture introduces the basics of Database Management Systems (DBMS), focusing on creating and manipulating tables using MySQL.

## Key takeaways
- A database can consist of multiple tables.
- MySQL is a query language used to manage databases.
- Tables are created using SQL commands.

## Database Management System (DBMS)
- **Core Idea**: A system for managing and organizing data in a structured manner.
- **Example**: A database named `University` contains a table `Student_Info`.

![Board 1:10-10:50](figures_board/board_01_era2.jpg)

*Figure 1. The whiteboard during 1:10–10:50, reconstructed from 5 video frames with the lecturer removed; 100% of the board is unobstructed.*
```markdown
Database Management System
(DBMS)

University

Student_Info

| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|----|------------|-----------|-------|-------------|------------------|
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
| 151216 | Ahsan | Habib | 3.77 | Math | 20-09-2024 |
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
| 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |
```

## Creating a Table Using SQL
- **Core Idea**: SQL commands are used to create, manipulate, and manage tables.
- **Example**: The `Student_Info` table is created with specific columns and data types.

Lecturer: So, this is the table we have to see. How many columns are our tables? How many columns are there? This is possible that the actual database has multiple tables. So, this database will communicate with us as language. So the language that we have to do is MySQL. MySQL is our programming language. Java, Python, C, C-Sharp, this one is different. MySQL, this is Query Language. Query Language is the user question of which the database has been given. So, it's Query Language. MySQL, I first need to create a table. This table has to create which way? So this is the query in the middle of the table. In other words, we have to manipulate the table, we have to manipulate data, change the table, insert the table or delete the table. For the data, I need to add to the table, add to the row, add to the column, delete the table. In fact, I am only using the table to use the unneccessary table. So this will be fully deleted. So we have our SQL command. First, let's see if SQL has created. So first day jodhi আশী, আমি দিলা, create table. আমি টেবল্য়ে নাম টকো রাখে চাছরে? এজে. এটা হসে আমার টেবল্য়ে নাম, which is student underscore info. And this is the first thing I have to write about. So now we can read this comment. We will see student info on our table. So what should we do with this table? So here we will see the first name, last name, department, enrollment date. So this is what we have to do. Here we can see the sequential sequence. So first we will see ID. Here we will see first name. here for last name last underscore name here for CGPA here for a department In this case we will write the same page as a column by line. We have created this page as a table. So we will mention the data type in the first name of the So, the name of the student has named. The name of the student is called the name. Different characters. The name of the student will be different lengths to get the characters. So, characters which we use, we use the wordchart. The wordchart is variable characters. So first name and second name, only two characters, we have the same character variable. So I will write the wordpress. For example, with the wordpress, we have length of fix. We can use maximum length to make it. Suppose 10 students don't know about this, Up to 10 characters usually have been used. So, it's 10. If you want to use upto 10, we will consider the number of 1. Then CGPA. What do we find? Float numbers. So, this data type is float. Department is only first name or last name. So this will be the word. Character limitations for maximum 15 points. For example, enrollment date. Since it's date, date is not available. The first data type is also available. So this is data type. This link automatically, date form numbers. So 8th hour jephars baguette start to 0, it's end and last semicolon dhe dhe dhu.

```markdown
Database Management System
(DBMS)

University

MySQL->Query Language

Create table Student_info(
ID Int,
First_Name Varchar(10),
Last_Name Varchar(10),
CGPA float,
Department Varchar(15),
Enrollment_Date Date
);

Student_Info
| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|----|------------|-----------|------|------------|----------------|
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
| 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |
| 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |
```

## Check Yourself
1. What is the purpose of a Database Management System (DBMS)?
2. Name the query language used in MySQL.
3. What are the columns in the `Student_Info` table?
4. What is the data type of `Enrollment_Date` in the `Student_Info` table?
5. How many rows are present in the `Student_Info` table?

## Answers
1. The purpose of a Database Management System (DBMS) is to manage and organize data in a structured manner.
2. The query language used in MySQL is SQL.
3. The columns in the `Student_Info` table are `ID`, `First_Name`, `Last_Name`, `CGPA`, `Department`, and `Enrollment_Date`.
4. The data type of `Enrollment_Date` in the `Student_Info` table is `Date`.
5. There are 5 rows present in the `Student_Info` table.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*
