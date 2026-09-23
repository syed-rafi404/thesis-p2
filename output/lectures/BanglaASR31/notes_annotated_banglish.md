# .B(D) → Bin to Dec
This lecture covers the process of converting a decimal number to a binary number.

## Key takeaways
- Understand the concept of binary to decimal conversion.
- Learn the powers of 2 and their corresponding decimal values.
- Practice converting binary numbers to decimal numbers using a step-by-step method.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## .B(D) → Bin to Dec
**Ek line e:** This is the process of converting a decimal number to a binary number.

![Board 1: 0:00-4:38](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–4:38, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 List · 3 Worked example


1. **Red Box 1 (Title):** The title of the board is ".B(D) → Bin to Dec", which stands for Binary to Decimal conversion.
2. **Blue Box 2 (List):** The board lists the powers of 2 from 2^0 to 2^7:
   | 2^0 → 1 | 2^1 → 2 | 2^2 → 4 | 2^3 → 8 | 2^4 → 16 | 2^5 → 32 | 2^6 → 64 | 2^7 → 128 |
3. **Orange Box 3 (Worked Example):** The worked example shows the binary number 10101000 and how to convert it to decimal:
   | 128 | 64  | 32  | 16  | 8   | 4   | 2   | 1   |
   |-----|-----|-----|-----|-----|-----|-----|-----|
   | 1   | 0   | 1   | 0   | 1   | 0   | 0   | 0   |

**Explanation:**
- The lecturer explains that we are converting a decimal number to a binary number using a manual method.
- He mentions that the binary system uses only two digits, 0 and 1, and these can be used to represent any number by combining different powers of 2.
- For example, 2^3 = 8 and 2^4 = 16. The highest power of 2 that fits into the number is used first, and then the next lower power is considered until all bits are accounted for.
- The board lists the powers of 2 from 2^0 to 2^7 to show the corresponding decimal values.
- In the worked example, the binary number 10101000 is broken down into its components, where each 1 represents a power of 2 that contributes to the final decimal value. The 1s are added together to get the decimal equivalent.

> Lecturer: "so, moving on. aa amr dekhte pacchi tare tutu jiboha something mane bujhai je amader eije duita unique address zero or one, duita unique number, sorry, duita unique number diye amra koto gula combination, unique combination er address ba digit generate korte pari, eta hocche basically uniquely identify korte pari."

### Extra jana kotha
To understand binary to decimal conversion, think of each bit in a binary number as representing a power of 2. By adding up the values of the bits that are set to 1, you can easily convert a binary number to its decimal equivalent. This method is widely used in computer science and digital electronics.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## B(D) → Bin to Dec
**Ek line e:** This section explains how to convert a binary number to its decimal equivalent.

![Board 2: 4:40-6:30](figures_annotated/board_era2_440.jpg)

*Figure 2. The whiteboard during 4:40–6:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Worked example


1. **Box 1 (red): B CD**
   - This box introduces the concept of converting a binary number to its decimal form. The term "B(D)" stands for Binary to Decimal conversion.
   
2. **Box 2 (blue): Worked example: . B CD Bin to Dec**
   - The example given is 128 64 32 16 8 2 2 1 0 1 0 0 0 0 168. Here, we see the binary representation of 168, which is 10100000.
   - The lecturer explains that 168 in binary is 10100000, and when we add up the values corresponding to the positions where there is a 1, we get 128 + 32 + 8 = 168.
   - The binary number 10100000 can be broken down as follows:
     - 2^7 = 128
     - 2^5 = 32
     - 2^3 = 8
     - Adding these values gives us 168.

> Lecturer: "seto dekhi amra basically eke evolution kore 1680 bi kina. tamano bujhe jabe e je amader evolution thikase likehane."

### Extra jana kotha (lecture e bola hoy ni)
Understanding binary to decimal conversion is crucial for computer science and digital electronics. It helps in comprehending how computers process and store information. By breaking down a binary number into its positional values, you can easily convert it to its decimal equivalent. This skill is fundamental for further studies in programming and digital systems.

---

## Check yourself
1. Convert the binary number 10101000 to its decimal equivalent.
2. What are the powers of 2 listed from 2^0 to 2^7?
3. How do you convert the binary number 10100000 to its decimal equivalent?
4. Explain the process of converting a binary number to decimal.
5. Why is understanding binary to decimal conversion important in computer science?

### Answers
1. The binary number 10101000 converts to 176 in decimal.
2. The powers of 2 listed from 2^0 to 2^7 are: 1, 2, 4, 8, 16, 32, 64, 128.
3. The binary number 10100000 converts to 160 in decimal.
4. To convert a binary number to decimal, break down the binary number into its positional values and add up the values corresponding to the positions where there is a 1.
5. Understanding binary to decimal conversion is important in computer science because it helps in comprehending how computers process and store information.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
