# Conditional Statements and Decision Making in Python

In this lecture, we will learn about conditional statements in Python, specifically focusing on `if`, `elif`, and `else` statements.

## Key takeaways
- Understand how to use `if`, `elif`, and `else` statements.
- Learn to use user input to make decisions.
- Recognize the importance of matching strings correctly.

## Conditional Statements
Conditional statements allow the computer to make decisions based on certain conditions. We will explore how to use `if`, `elif`, and `else` to create decision-making logic.

### Example: Bringing an Umbrella Based on Weather
The lecturer provided an example where the user inputs the weather, and the program decides whether to bring an umbrella.

```python
Weather = input("Today's weather:")
if Weather == "Rain":
    print("Bring Umbrella")
elif Weather == "Sunny":
    print("Wear White Colou")
else:
    print("Just Come")
```

**Lecturer:** If rain user will bring umbrella. Okay? So, if not So, when the range is used, the umbrella does not have that umbrella does not have to use. So, how do you start with this? First, we will show the variable. Weather. So what about the user? The input of this user is an input. The user has to say today's weather. So, user input today's weather has been given. User at the weather that we have seen. Rain or sunny or something. So, if weather equal-equal I am going to say whether rain has been printed Print So, user-elect input the power of whether it has to be written first if block So you can see the range of this area, print the umbrella. If weather is unknown, but rain has a small letter to write it. else Also just come. You don't have to bring umbrella if it doesn't rain. You can just come. So this is what happens. User input has been used by the string We have to match the string. We will check if it is rain or does it equal rain? If yes, we can print bring. If there is rain, then we will use else block. The else block says print just come. So I will say if else, when we do weather is sunny, what happens? So, if I am going to tell you about the details of the else, I will give an elif conditional statement. What do we have? We can print...

### Watch out:
- Ensure the string matches exactly, including case sensitivity.
- Use `==` for comparison, not `=` which is for assignment.

## Check yourself
1. Write a Python program to check if a number is positive, negative, or zero.
2. Write a Python program to check if a year is a leap year.
3. Write a Python program to check if a character is a vowel or consonant.
4. Write a Python program to check if a string is a palindrome.
5. Write a Python program to check if a number is even or odd.

### Answers
1. ```python
   num = int(input("Enter a number:"))
   if num > 0:
       print("Positive")
   elif num < 0:
       print("Negative")
   else:
       print("Zero")
   ```
2. ```python
   year = int(input("Enter a year:"))
   if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
       print("Leap Year")
   else:
       print("Not a Leap Year")
   ```
3. ```python
   char = input("Enter a character:")
   if char.lower() in ['a', 'e', 'i', 'o', 'u']:
       print("Vowel")
   else:
       print("Consonant")
   ```
4. ```python
   string = input("Enter a string:")
   reversed_string = string[::-1]
   if string == reversed_string:
       print("Palindrome")
   else:
       print("Not a Palindrome")
   ```
5. ```python
   num = int(input("Enter a number:"))
   if num % 2 == 0:
       print("Even")
   else:
       print("Odd")
   ```

---

*Figures are reconstructed whiteboards assembled from moments when the lecturer was not standing in front of each part of the board. Every pixel is unmodified video; nothing in them is generated. Each shows the board across the time range given, not a single instant.*