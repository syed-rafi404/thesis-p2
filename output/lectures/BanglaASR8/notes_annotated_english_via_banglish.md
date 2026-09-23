# Three Address Code
The lecture covers the concept of Three Address Code and its application in deriving the final expression for \( x \) using given formulas and variables.

## Key takeaways
- Three address code is a way to represent instructions in a program using temporary variables.
- Intermediate values like \( t1, t2, t3, t4, t5, \) and \( t6 \) are derived from the given formulas.
- The final value of \( x \) is \( t6 \).

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Three Address Code
**In one line:** Three address code is a way to represent instructions in a program using temporary variables.

![Board 1: 0:30-4:10](figures_annotated/board_era1_030.jpg)

*Figure 1. The whiteboard during 0:30–4:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Formula · 2 Formula


1. **Red Box 1 (Formula: a = (b*c + d) / t1):**
   - The formula here represents an arithmetic operation where `a` is assigned the value of `(b*c + d)` divided by `t1`.
   - `t1` is defined as `b - c`.

2. **Blue Box 2 (Formula: x = a + a*(b-c) + (b-c)*d / t2 + t3):**
   - This formula represents another arithmetic operation where `x` is assigned the value of `a` plus `a*(b-c)` plus `(b-c)*d` divided by `t2`, plus `t3`.

3. **t1 = b - c:**
   - Here, `t1` is calculated as `b - c`.

4. **t2 = t1 * a:**
   - `t2` is then calculated as `t1` multiplied by `a`.

5. **t3 = (b - c):**
   - `t3` is simply the value of `b - c`.

6. **t4 = t3 * d:**
   - Finally, `t4` is calculated as `t3` multiplied by `d`.

The lecturer said: "Three address code is commonly used because it helps in managing operations within a specific architecture. The code is designed to handle operations in a way that respects the precedence of operators, such as multiplication before addition."

> Lecturer: "Three address code er kacheta holo. Defo amader ekhon compiler kintu shobshomoy aa ek ekta architecture ek ekta home er hoye thake."

### Background (not said in the lecture)
Three address code is a fundamental concept in compiler design. It simplifies the process of generating machine code by breaking down complex expressions into simpler steps. This makes it easier for the compiler to manage and optimize the code, ensuring that operations are performed in the correct order according to the rules of precedence.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Three Address Code

**In one line:** In this section, we will see how to derive the final expression for  x  using the given formulas and variables.

![Board 2: 4:20-4:56](figures_annotated/board_era2_420.jpg)

*Figure 2. The whiteboard during 4:20–4:56, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Formula · 2 Formula · 3 Variable · 4 Code


1. **Red Box (Box 1):** The first formula is  a = (b * c + d) / t1 . This equation defines the value of  a  based on the multiplication of  b  and  c , addition of  d , and division by  t1 .

2. **Green Box (Box 4):** The next set of code defines the intermediate values:
   -  t1 = b * c 
   -  t2 = t1 + d 
   -  a = t2 

3. **Blue Box (Box 2):** The second formula is  x = a + a * (b - c) + (b - c) * d / t4 . This equation calculates  x  by adding  a  to the product of  a  and the difference between  b  and  c , and the product of  (b - c)  and  d  divided by  t4 .

4. **Orange Box (Box 3):** The variable  t4  is used in the final formula to represent an intermediate value.

5. **Blue Box (Box 2) and Green Box (Box 4):** To derive the final expression for  x , we need to substitute the values of  a  and other intermediate variables. From the green box, we know  a = t2  and  t2 = t1 + d . So, substituting these into the blue box formula, we get:
   
   x = t2 + t2 * (b - c) + (b - c) * d / t4
   
   Since  t2 = t1 + d , we can further simplify:
   
   x = (t1 + d) + (t1 + d) * (b - c) + (b - c) * d / t4
   

6. **Blue Box (Box 2) and Green Box (Box 4):** The lecturer said: "By substituting the values, we get  t6 . If we add  t4  to  t5 , we get  t6 . Finally,  x  is equal to  t6 ."

7. **Final Expression:** Therefore, the final expression for  x  is:
   
   x = t6
   

**Remember:** The key points are the intermediate values  t1, t2, t3, t4, t5,  and  t6 , and how they are derived from the given formulas. The final value of  x  is  t6 .

---

## Check yourself
1. What is the formula for calculating \( t1 \)?
2. How is \( a \) defined in terms of \( t1 \) and \( d \)?
3. What is the final expression for \( x \) after substituting all intermediate values?
4. Which variable is used to represent the difference between \( b \) and \( c \)?
5. What does the lecturer mean by "tahole t6 niye equal diye, kilikte pari. t6 equal. etar sathe jodi t4 add kore di, tahole t5 plus t4. tamane t6-er modde amare puro jinishte ache"?

### Answers
1. \( t1 = b - c \)
2. \( a = (b * c + d) / t1 \)
3. \( x = t6 \)
4. \( t3 \) or \( t4 \) (depending on the context)
5. By substituting the values, we get \( t6 \). If we add \( t4 \) to \( t5 \), we get \( t6 \). Finally, \( x \) is equal to \( t6 \).

---

*This lecture is `BanglaASR12` in the dataset (`BanglaASR8` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
