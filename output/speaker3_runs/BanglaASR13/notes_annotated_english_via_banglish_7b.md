# BanglaASR13
The lecture covers the concepts of Maximum Transmission Unit (MTU) and packet size, including the structure of packets and the calculation of fragment offsets.

## Key takeaways
- MTU stands for Maximum Transmission Unit.
- Packet size consists of a header section and a data section.
- The DF flag in the header section helps in identifying and reassembling fragmented packets.
- Fragment offset is used to determine the position of each fragment within the original packet.
- The formula for calculating fragment offset is `fragment_offset = (total_size - header_size) / fragment_size`.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Red Box 1: Definition of MTU and Packet Size
**Ek line e:** MTU stands for Maximum Transmission Unit, which defines the total packet size.

![Board 1: 0:00-3:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Definition · 2 Formula


- **Red Box 1 (Definition):** MTU Maximum transmission unit Packet Size
- **Blue Box 2 (Formula):** DF -> 0 * Total packet size -> 1. Header Sec. 2. Data Sec. 1500 Header + Data -> 20B - 60B

The lecturer said: "Total packet size consists of two sections: the header section and the data section. The header section contains information like the DF (Don't Fragment) flag, which helps in identifying fragments of a packet. The data section contains the actual data being transmitted."

> Lecturer: "Total packet jeta amra pathai ekta network theke onno network e, it has two sections."

The DF flag in the header section is crucial because it allows us to identify and reassemble fragmented packets. This process is typically handled by devices at the network layer, such as routers. Therefore, we understand that each packet will have both a header and a data section.

The header size is fixed at 20 bytes, while the data size can vary. The maximum transmission unit (MTU) refers to the largest packet size that can be sent in a single transmission without fragmentation. In this case, the MTU is defined as 1500 bytes, which includes the header and data sections.

> Lecturer: "MTU always refers to the size of a packet. So, I write 1500 bytes here, meaning the header is included. MTU always refers to the size of a packet."

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
> "So, if the size of one packet is, just the data size of the packet, sorry, if the data size is 4000 bytes, that's the total size of the data before including any headers."
> "For the second fragment, we add this value again divided by eight. Let's just take this value for now. What value are we waiting for? Okay, let's calculate it. Divided by eight, that is 185. So, what is the value for the second fragment?"

### Extra jana kotha
Fragment offset helps in reassembling the original packet at the destination. By knowing the fragment offset, the receiver can correctly place each fragment in the correct position. This ensures that the entire packet is reconstructed accurately without any loss or corruption.

---

## Check yourself
1. What does MTU stand for?
2. How many bytes is the fixed header size?
3. What is the maximum size of a packet that can be sent without fragmentation?
4. What is the purpose of the DF flag?
5. How is the fragment offset calculated?

### Answers
1. MTU stands for Maximum Transmission Unit.
2. The fixed header size is 20 bytes.
3. The maximum size of a packet that can be sent without fragmentation is 1500 bytes.
4. The DF flag helps in identifying and reassembling fragmented packets.
5. The fragment offset is calculated using the formula: `fragment_offset = (total_size - header_size) / fragment_size`.

---

*This lecture is `BanglaASR17` in the dataset (`BanglaASR13` is its old number, kept because the answer keys use it).*

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (4 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
