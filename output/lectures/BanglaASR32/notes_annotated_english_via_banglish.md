# Dec to Binary
In this section, we will learn how to convert decimal numbers to binary.

## Key takeaways
- The process involves repeatedly dividing the decimal number by 2 and keeping track of the remainders.
- We read the remainders from bottom to top to form the binary number.
- Understanding the powers of 2 is essential for the conversion process.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Dec to Binary
**In one line:** In this section, we will learn how to convert decimal numbers to binary.

![Board 1: 0:00-2:10](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–2:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Formula · 3 Worked example


1. **Box 1 (red):** The title "Dec to Binary" tells us that we are converting decimal numbers to binary.
2. **Box 2 (blue):** The blue box lists the decimal numbers from 0 to 12. This is a reference for understanding the conversion process.
3. **Box 3 (orange):** The orange box shows a worked example of converting the decimal number 168 to binary. Let's break it down step by step:

    - First, we divide 168 by 2. The quotient is 84 and the remainder is 0.
    - Next, we divide 84 by 2. The quotient is 42 and the remainder is 0.
    - Then, we divide 42 by 2. The quotient is 21 and the remainder is 0.
    - Finally, we divide 21 by 2. The quotient is 10 and the remainder is 1.

    So, the binary representation of 168 is 10101000.

4. **The Table:** The table on the board shows the powers of 2 and their corresponding values. This helps us understand the binary system better. For example, 2^7 = 128, 2^6 = 64, 2^5 = 32, and so on.


### Background (not said in the lecture)
To convert a decimal number to binary, we repeatedly divide the number by 2 and keep track of the remainders. The binary number is formed by reading the remainders from bottom to top. This method ensures that we get the correct binary representation of any decimal number.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Dec to Binary
**In one line:** Decimal to binary conversion involves breaking down the decimal number into powers of 2.

![Board 2: 2:20-4:38](figures_annotated/board_era2_220.jpg)

*Figure 2. The whiteboard during 2:20–4:38, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List


The red box (Box 1) lists the powers of 2, starting from 2^0 to 2^7. Each power of 2 is shown as a column, with the corresponding value in the next column. For example, 2^0 = 1, 2^1 = 2, and so on up to 2^7 = 128.

The blue box (Box 2) shows the binary representation of a decimal number. In this case, the binary number is `011`.

Let's break down the process:

1. **Identify the highest power of 2 less than or equal to the decimal number**: For the decimal number 5, the highest power of 2 less than 5 is 2^2 = 4.
2. **Subtract the identified power of 2 from the decimal number**: 5 - 4 = 1.
3. **Repeat the process with the remainder**: The remainder is 1, which is 2^0.
4. **Write the binary representation**: Since we have 2^2 and 2^0, the binary representation is `101`.

The lecturer explains: "but eikhane remain er koto ashe 0, right? abar hinge 5 er 2 diye korte chai, 5 er 2 diye korte chai le amar 2 to di par 4. toh basically amar amar yash a 2, ara ami ekhane remain er pi 1, because hiest grade 2 er 2 out to 4 hoy, 4 minus 5, 1, right?"

The lecturer further clarifies: "so, last a giye hocche amader ei je one ta ashbe jehane bochhe kami. konne jeta last number o da toh divide korchi. because tu dia je je divide kore one e pabo ar ke ultimately. oita ami just dekhailam. toh basically ami jujh dekhan amar number ta dekhiu."

### Background (not said in the lecture)
When converting a decimal number to binary, we repeatedly subtract the highest possible power of 2 until we reach zero. This method helps us understand the binary representation of any decimal number. For example, the decimal number 168 can be represented in binary as `10101000`, which is the sum of 2^7 + 2^6 + 2^3. Understanding this process is crucial for working with IP addresses and other numerical systems.

---

## Check yourself
1. Convert the decimal number 168 to binary.
2. What is the binary representation of the decimal number 5?
3. Identify the highest power of 2 less than or equal to the decimal number 13.
4. Write the binary representation of the decimal number 12 using the powers of 2.
5. Explain the process of converting a decimal number to binary.

### Answers
1. The binary representation of 168 is 10101000.
2. The binary representation of 5 is 101.
3. The highest power of 2 less than or equal to 13 is \(2^3 = 8\).
4. The binary representation of 12 is 1100.
5. The lecturer said: "To convert a decimal number to binary, we repeatedly divide the number by 2 and keep track of the remainders. The binary number is formed by reading the remainders from bottom to top."

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
