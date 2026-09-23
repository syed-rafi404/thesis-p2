# BanglaASR13: Red Box 1 and Blue Box 2

This lecture covers the definitions and calculations related to Maximum Transmission Unit (MTU) and packet size, as well as the concept of fragment offset in packet fragmentation.

## Key takeaways
- MTU
- Header size
- Data size
- DF flag
- Reassembly
- Network layer
- Fragment offset calculation

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Box 1: Definition of MTU and Packet Size
**Ek line e:** MTU stands for Maximum Transmission Unit, which defines the total packet size.

![Board 1: 0:00-3:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Definition · 2 Formula


- **Red Box 1 (Definition):** MTU Maximum transmission unit Packet Size
- **Blue Box 2 (Formula):** DF -> 0 * Total packet size -> 1. Header Sec. 2. Data Sec. 1500 Header + Data -> 20B - 60B

The lecturer explains that the total packet size consists of two sections: the header section and the data section. The header section contains information like the DF (Don't Fragment) flag, which helps in identifying fragments of a packet. The data section contains the actual data being transmitted.

> Lecturer: "total packet jeta amra pathai ekta network theke onno network e, it has two sections."

The DF flag in the header section is crucial because it allows us to identify and reassemble fragmented packets. This process is typically handled by devices at the network layer, such as routers. Therefore, we understand that each packet will have both a header and a data section.

The header size is fixed at 20 bytes, while the data size can vary. The maximum transmission unit (MTU) refers to the largest packet size that can be sent in a single transmission without fragmentation. In this case, the MTU is defined as 1500 bytes, which includes the header and data sections.

> Lecturer: "mtu always pack er size te bole. so, ami jeta ponno masho baytekanan likhe chai, tar mane ekhane kintu aa header ta included. mtu always pack er size ta bole."

In summary, the total packet size is the sum of the header and data sections, with the header size fixed at 20 bytes and the data size varying based on the actual data being transmitted. The MTU is the maximum size of a packet that can be sent without fragmentation, which in this case is 1500 bytes.

**Mone rakho:** MTU, header size, data size, DF flag, reassembly, network layer, 1500 bytes.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Blue Box 2: Fragment Offset Calculation
**Ek line e:** Fragment offset is used to determine the position of each fragment within the original packet.

![Board 2: 4:00-12:34](figures_annotated/board_era2_400.jpg)

*Figure 2. The whiteboard during 4:00–12:34, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Maximum transmission unit · 2 Fragment offset · 3 Fragment offset · 4 Fragment offset · 5 Fragment offset


1. **MTU (Maximum Transmission Unit):**
   - The MTU is the maximum size of a single packet that can be transmitted over a network without being fragmented. It includes both the header and the data section.
   
2. **Packet Size:**
   - Suppose we have a data size of 4000 bytes. This is the total size of the data before including any headers.
   
3. **Fragmentation:**
   - When the data size exceeds the MTU, the packet is split into smaller fragments. Each fragment has a fragment offset to indicate its position within the original packet.
   
4. **Fragment Offset Calculation:**
   - The fragment offset is calculated using the formula: `fragment_offset = (total_size - header_size) / fragment_size`.
   - For example, if the total size is 4000 bytes and the fragment size is 1480 bytes (including header), the first fragment will have an offset of 0.
   - The second fragment will start at 1480 bytes, and so on.
   
5. **Example Calculation:**
   - For the first fragment: `fragment_offset = 0/8 = 0`. This means the first fragment starts at the beginning of the packet.
   - For the second fragment: `fragment_offset = 1479/8 = 185`. This means the second fragment starts at 1479 bytes.
   - For the third fragment: `fragment_offset = 2960/8 = 370`. This means the third fragment starts at 2960 bytes.
   
6. **Final Fragment:**
   - The final fragment will have a fragment offset of 3, indicating it is the last fragment.

**Quotes:**
> "tahole amr jodi ekta packet er size hoy, just packet er data size, sorry, amr jodi ekta data size hoy, mone koro char haajar byte. char haajar byte, right."
> "so, second er jonno, abar joddhoro ashi divided by eight. amra just ei value gular nivore thikase? kothomer je value ta waita? aa dhoro jodi sho asha eta ekta just calculate er kore dekhi. joddhor ashi divided by eight, that is 185. erocche second je value ta par fragment offset."

### Extra jana kotha
Fragment offset helps in reassembling the original packet at the destination. By knowing the fragment offset, the receiver can correctly place each fragment in the correct position. This ensures that the entire packet is reconstructed accurately without any loss or corruption.

---

## Check yourself
1. What does MTU stand for and what does it define?
2. How is the total packet size calculated?
3. What is the purpose of the DF flag in the header section?
4. Calculate the fragment offset for a data size of 4000 bytes with a fragment size of 1480 bytes.
5. Why is fragment offset important in packet reassembly?

### Answers
1. MTU stands for Maximum Transmission Unit, which defines the total packet size.
2. The total packet size is calculated by adding the header size (fixed at 20 bytes) and the data size (which varies).
3. The DF flag in the header section helps in identifying and reassembling fragmented packets.
4. The fragment offset for a data size of 4000 bytes with a fragment size of 1480 bytes is:
   - First fragment: 0
   - Second fragment: 185
   - Third fragment: 370
5. Fragment offset is important in packet reassembly because it helps the receiver correctly place each fragment in the correct position, ensuring accurate reconstruction of the original packet.

---

*This lecture is `BanglaASR17` in the dataset (`BanglaASR13` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 4 kept, 0 removed. References to boxes that do not exist: 0.*
