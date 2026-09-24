# BanglaASR13: Red Box 1: Definition: MTU Maximum Transmission Unit Packet Size and Blue Box 2: Fragment Offset
This lecture covers the concepts of MTU (Maximum Transmission Unit) and Fragment Offset in the context of packet size and network communication.

## Key takeaways
- MTU is the maximum size of a packet that can be transferred without fragmentation.
- Header section contains metadata like flags and identification numbers.
- Data section contains the actual data being transmitted.
- DF flag indicates whether the packet can be fragmented.
- Header size is typically 20 bytes.
- Data size varies based on the amount of data.
- Fragment offset helps in determining where a fragment starts within the original data.
- Number of fragments is calculated using the formula: \(\left\lceil \frac{\text{Total data size}}{\text{MTU}} \right\rceil\).

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Box 1: Definition: MTU Maximum Transmission Unit Packet Size
**Ek line e:** Total packet size has two sections: header and data.

![Board 1: 0:00-3:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Definition · 2 Formula


- **Red Box 1 (Definition):** MTU Maximum transmission unit Packet Size
  - **Header Section:** This section contains metadata like flags and identification numbers.
  - **Data Section:** This section contains the actual data being transmitted.
  - **DF Flag:** This flag indicates whether the packet can be fragmented.
  - **Header Size:** Typically 20 bytes.
  - **Data Size:** Varies based on the amount of data, but should be fixed for consistency.
  - **MTU (Maximum Transfer Unit):** The maximum size of a packet that can be transferred without fragmentation.


### Extra jana kotha
MTU (Maximum Transfer Unit) is the largest size of a packet that can be sent over a network without needing to be broken into smaller pieces. In this context, the header size is typically fixed at 20 bytes, while the data size can vary depending on the amount of data being transmitted. Understanding these components helps in managing network traffic efficiently.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Blue Box 2: Fragment Offset
**Ek line e:** Fragment offset: 0/8

![Board 2: 4:00-12:34](figures_annotated/board_era2_400.jpg)

*Figure 2. The whiteboard during 4:00–12:34, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Maximum transmission unit · 2 Fragment offset · 3 Fragment offset · 4 Fragment offset · 5 Fragment offset


The lecturer explained that the maximum transmission unit (MTU) is the size of the data portion of a packet, excluding the header. For our example, let's assume the data size is 4,000 bytes. The fragment offset is used to indicate where a fragment starts within the original data. 

The fragment offset helps us determine how to split the data into fragments. For instance, if we have 2,959 bytes of data, we need to divide this by the MTU size (which is 8 bytes in this case) to find out how many fragments we need. The formula is:

 Number of fragments = \left\lceil \frac{Total data size}{MTU} \right\rceil 

For 2,959 bytes, the calculation gives us 3 fragments. So, the first fragment starts at 0, the second at 14, and the third at 79. The fragment offset for the first fragment is 0, for the second it is 14, and for the third it is 79.

If the first fragment starts from a different position, say from 5, the calculation changes. In this case, the first fragment would start at 0, and the subsequent fragments would adjust accordingly.

| Fragment | Fragment Offset |
|----------|-----------------|
| 1        | 0               |
| 2        | 14              |
| 3        | 79              |

The fragment offset for the first fragment is always 0, as it starts from the beginning. For the second fragment, the offset is calculated as:

 Fragment offset = \left( Fragment number - 1 \right) x MTU 

So, for the second fragment:

 Fragment offset = (2 - 1) x 8 = 14 

Similarly, for the third fragment:

 Fragment offset = (3 - 1) x 8 = 16 

The lecturer also mentioned that if we want to find the fragment offset for the last fragment, we can use the same formula. For the last fragment, the offset is:

 Fragment offset = \left( Number of fragments - 1 \right) x MTU 

In our example, the last fragment's offset is 79.

> Lecturer: "so, second er jonno, abar joddhoro ashi divided by eight."

**Mone rakho:** Fragment offset: 0, 14, 79. Fragment offset for the first fragment is always 0. For other fragments, it is calculated as (fragment number - 1) * MTU.

---

## Check yourself
1. What is the typical size of the header section in bytes?
2. How is the fragment offset calculated for the second fragment?
3. What does the DF flag indicate?
4. What is the formula to calculate the number of fragments?
5. What is the fragment offset for the first fragment?

### Answers
1. The typical size of the header section is 20 bytes.
2. The fragment offset for the second fragment is calculated as (2 - 1) * MTU, which equals 8.
3. The DF flag indicates whether the packet can be fragmented.
4. The formula to calculate the number of fragments is \(\left\lceil \frac{\text{Total data size}}{\text{MTU}} \right\rceil\).
5. The fragment offset for the first fragment is always 0.

---

*This lecture is `BanglaASR17` in the dataset (`BanglaASR13` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 1 removed. References to boxes that do not exist: 0.*
