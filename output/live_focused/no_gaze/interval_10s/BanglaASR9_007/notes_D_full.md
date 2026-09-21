# SQL Queries and Data Retrieval

In this lecture, we learned about SQL queries, focusing on the `SELECT` command and various operations to retrieve data from a database.

## Key Takeaways
- The `SELECT` command is used to retrieve data from a database.
- Aggregation functions like `MAX`, `MIN`, `SUM`, and `AVG` can be used to perform operations on data.
- Nested queries can be used to retrieve specific data based on conditions.

## SELECT Command
The `SELECT` command is used to retrieve data from a database table. It allows us to specify which columns we want to retrieve and apply conditions to filter the results.

### Example: Retrieve Full Data from a Table
```sql
SELECT * FROM Student_Info;
```
This retrieves all columns from the `Student_Info` table.

### Example: Retrieve Specific Columns
```sql
SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 401201;
```
This retrieves the `First_Name` and `Last_Name` of the student with `ID = 401201`.

### Example: Retrieve Department
```sql
SELECT Department FROM Student_Info WHERE ID = 151216;
```
This retrieves the `Department` of the student with `ID = 151216`.

### Example: Order Data
```sql
SELECT ID FROM Student_Info ORDER BY ID ASC;
```
This orders the `ID` column in ascending order.

### Example: Aggregation Functions
#### Maximum CGPA
```sql
SELECT MAX(CGPA) FROM Student_Info;
```
This returns the maximum CGPA from the `Student_Info` table.

#### Minimum CGPA
```sql
SELECT MIN(CGPA) FROM Student_Info;
```
This returns the minimum CGPA from the `Student_Info` table.

#### Sum of CGPA
```sql
SELECT SUM(CGPA) FROM Student_Info;
```
This returns the sum of all CGPAs from the `Student_Info` table.

#### Average CGPA
```sql
SELECT AVG(CGPA) FROM Student_Info;
```
This returns the average CGPA from the `Student_Info` table.

### Example: Retrieve Student with Maximum CGPA
```sql
SELECT ID, CGPA FROM Student_Info WHERE CGPA = (SELECT MAX(CGPA) FROM Student_Info);
```
This retrieves the `ID` and `CGPA` of the student with the highest CGPA.

### Example: Retrieve Student with Minimum CGPA
```sql
SELECT ID, CGPA FROM Student_Info WHERE CGPA = (SELECT MIN(CGPA) FROM Student_Info);
```
This retrieves the `ID` and `CGPA` of the student with the lowest CGPA.

## Check Yourself
1. Write a query to retrieve all columns from the `Student_Info` table.
2. Write a query to retrieve the `First_Name` and `Last_Name` of the student with `ID = 401201`.
3. Write a query to retrieve the `Department` of the student with `ID = 151216`.
4. Write a query to order the `ID` column in ascending order.
5. Write a query to find the maximum CGPA from the `Student_Info` table.

## Answers
1. `SELECT * FROM Student_Info;`
2. `SELECT First_Name, Last_Name FROM Student_Info WHERE ID = 401201;`
3. `SELECT Department FROM Student_Info WHERE ID = 151216;`
4. `SELECT ID FROM Student_Info ORDER BY ID ASC;`
5. `SELECT MAX(CGPA) FROM Student_Info;`

![Board 0:10-9:10](figures_board/board_01_era1.jpg)

*Figure 1. The whiteboard during 0:10–9:10, reconstructed from 13 video frames with the lecturer removed; 98% of the board is unobstructed.*

Database Management System (DBMS) University
| Student Info |  
| --- | --- | --- | --- | --- | --- |  
| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |  
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |  
| 151216 | Ahsan | Habib | 3.77 | Math | 20-09-2024 |  
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |  
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |  
| 401201 | Israt | Jahan | 3.40 | MicroBiology | 11-11-2025 |  

![Board 9:20-16:20](figures_board/board_02_era2.jpg)

*Figure 2. The whiteboard during 9:20–16:20, reconstructed from 5 video frames with the lecturer removed; 99% of the board is unobstructed.*

Database Management System (DBMS) University
| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |  
|----|------------|-----------|-------|-------------|-----------------|  
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |  
| 151216 | Ahsan | Habib | 3.7 | Math | 20-09-2024 |  
| 202011 | Adiba | Noshin | 3.28 | Economics | 21-10-2021 |  
| 110112 | Maria | Islam | 3.98 | English | 02-02-2020 |  
| 401201 | Istrat | Jahan | 3.40 | MicroBiology | 11-11-2025 |  

Watch out: Ensure you use the exact column names and table names as specified in the examples.

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*
