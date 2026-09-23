# Understanding MTU and Packet Structure
This lecture covers the concept of Maximum Transmission Unit (MTU) and how it relates to the structure of network packets, including the header and data sections, and the process of packet fragmentation.

## Key takeaways
- MTU stands for Maximum Transmission Unit, which is the total packet size including the header and data sections.
- The header section contains important flags like the DF (Don't Fragment) flag, which helps in reassembling the packet correctly.
- Packet fragmentation involves dividing large packets into smaller fragments, each with a fragment offset value.
- The fragment offset is calculated using the formula: `fragment_offset = (total_size - header_size) / fragment_size`.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Understanding MTU and Packet Structure
**In one line:** MTU is the maximum transmission unit that includes both header and data sections of a packet.

![Board 1: 0:00-3:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Definition · 2 Formula


- **Definition of MTU (Box 1, Red):** MTU stands for Maximum Transmission Unit, which refers to the total packet size. This includes two main sections: the header section and the data section.

- **Total Packet Size (Box 2, Blue):** The total packet size consists of two parts: the header section and the data section. The header section contains information about the packet, such as the DF (Don't Fragment) flag, which helps in identifying fragments. The data section contains the actual data being transmitted.

- **Header Section:** The header section is crucial for identifying the packet. It includes flags like the DF flag, which indicates whether the packet can be fragmented or not. This helps in reassembling the packet correctly when it reaches its destination.

- **Data Section:** The data section contains the actual data being sent. For example, if a packet is 1500 bytes in total, the header might be 20 bytes, leaving the rest for the data section.

- **DF Flag:** The DF flag in the header section is significant because it tells us whether the packet can be fragmented. If the DF flag is set to 0, the packet cannot be fragmented, and if it is set to 1, the packet can be fragmented.

- **Example Calculation:** For instance, if a packet is 1500 bytes in total, the header size is fixed at 20 bytes, and the data size is 1500 - 20 = 1480 bytes. This shows how the total packet size is calculated.

**Quote:**
> "so, what is basically total packet size? total packet jeta amra pathai ekta network theke onno network e, it has two sections."  
> (In English: So, what is the basic total packet size? It is the size of a packet that we read from one network to another, which has two sections.)

**Remember:** MTU is the maximum size of a packet that can be transmitted, including both the header and data sections.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Calculating Fragment Offset in Network Packets
**In one line:** This board explains how to calculate the fragment offset for network packets based on their size and MTU.

![Board 2: 4:00-12:34](figures_annotated/board_era2_400.jpg)

*Figure 2. The whiteboard during 4:00–12:34, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Maximum transmission unit · 2 Fragment offset · 3 Fragment offset · 4 Fragment offset · 5 Fragment offset


### Explanation
1. **Understanding MTU and Packet Size**
   - The maximum transmission unit (MTU) is the largest packet size that can be sent without fragmentation. For our example, let's assume a data size of 4000 bytes.
   
2. **Fragmentation Process**
   - When the data size exceeds the MTU, the packet needs to be fragmented into smaller parts. Each fragment will have an offset value starting from 0.
   - The formula to calculate the fragment offset is `fragment_offset = (total_size - header_size) / fragment_size`.

3. **Calculating Fragment Offsets**
   - **First Fragment (Box 2, Fragment offset: 0/8):**
     - Fragment offset = 0
     - Fragment size = 1479 bytes
     - Total size = 1480 bytes (including header)
   - **Second Fragment (Box 3, Fragment offset: 1/8):**
     - Fragment offset = 1480
     - Fragment size = 2960 bytes
     - Total size = 4000 bytes (including header)
   - **Third Fragment (Box 4, Fragment offset: 2/8):**
     - Fragment offset = 2960
     - Fragment size = 370 bytes
     - Total size = 4000 bytes (including header)

4. **DF and MF Flags**
   - DF (Don't Fragment) flag is set to 0, indicating that fragmentation is allowed.
   - MF (More Fragments) flag is set to 1 for all but the last fragment, and 0 for the last fragment.

**Quotes:**
> "tahole amr jodi ekta packet er size hoy, just packet er data size, sorry, amr jodi ekta data size hoy, mone koro char haajar byte."  
> (In English: "if the size of a packet is just the data size, sorry, let's take a data size of 4000 bytes.")

**Remember:** The fragment offset is calculated based on the total size of the packet minus the header size, divided by the fragment size.

---

## Check yourself
1. What does MTU stand for?
2. Explain the purpose of the DF flag in the header section.
3. How is the fragment offset calculated?
4. What do the DF and MF flags indicate in the context of packet fragmentation?
5. If a packet is 1500 bytes in total and the header size is 20 bytes, what is the size of the data section?

### Answers
1. MTU stands for Maximum Transmission Unit.
2. The DF flag in the header section indicates whether the packet can be fragmented or not. If set to 0, the packet cannot be fragmented.
3. The fragment offset is calculated using the formula: `fragment_offset = (total_size - header_size) / fragment_size`.
4. The DF flag is set to 0 if fragmentation is not allowed, and the MF (More Fragments) flag is set to 1 for all but the last fragment, and 0 for the last fragment.
5. If a packet is 1500 bytes in total and the header size is 20 bytes, the size of the data section is 1480 bytes.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 0 removed. References to boxes that do not exist: 0.*
