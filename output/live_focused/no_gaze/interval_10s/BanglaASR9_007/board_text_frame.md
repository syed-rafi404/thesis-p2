# Board transcription (frame)

## Board 0:10-9:10

```markdown
| Database Management System (DBMS) |
|------------------------------------|
| University                        |
| Student_Info                      |
| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
| 241412   Syed        Rafi       3.55  CS         01-01-2024    |
| 151216   Ahsan       Habib      3.77  Math       20-09-2024    |
| 202011   Adiba       Noshin     3.28  Economics  21-10-2021    |
| 110112   Maria       Islam      3.98  English    02-02-2020    |
| 401201   Israt       Jahan      3.40  MicroBiology 11-11-2025    |
```

```sql
max()
min()
sum()
avg
```

## Board 9:20-16:20

```markdown
Database Management System
(DBMS)

University

| ID | First_Name | Last_Name | CGPA | Department | Enrollment_Date |
|----|------------|-----------|-------|-------------|-----------------|
| 241412 | Syed | Rafi | 3.55 | CS | 01-01-2024 |
| 151216 | Ahsan | Habib | 3.77 | Math | 20-09-2024 |
| 202011 | Adiba | | 3.87 | Economics | 21-10-2021 |
| 110112 | Maria | | 3.98 | English | 02-02-2020 |
| 401201 | Istrat | | 3.98 | Zoology | 11-11-2025 |

Student_Info

```sql
select ID, CGPA from Student_Info
where CGPA = (select max(CGPA) from Student_Info);
```

ID | CGPA
---|------
110112 | 3.98
```
