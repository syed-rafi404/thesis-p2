# BanglaASR13: MTU and Fragmentation
Ei lecture e MTU (Maximum Transmission Unit) and fragmentation er concept er moddhe bhalo achi kore discus kora hoyeche.

## Key takeaways
- MTU is the maximum size of a packet that can be transmitted over a network.
- The header section contains metadata and flags like the DF (Don't Fragment) flag.
- Packet reassembly is done using the DF flag and other metadata in the header.
- Fragmentation is the process of breaking large packets into smaller ones to fit within the MTU limit.
- The fragment offset is calculated to ensure correct reassembly of fragmented packets.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## MTU: Maximum Transmission Unit
**Ek line e:** MTU is the maximum size of a packet that can be transmitted over a network.

![Board 1: 0:00-3:50](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Definition · 2 Formula


**Explanation:**
1. **Total Packet Size:** The total packet size refers to the combined size of the header section and the data section. The header section contains metadata about the packet, while the data section holds the actual data.
2. **Header Section:** The header section includes information such as flags like the DF (Don't Fragment) flag. This flag helps in identifying fragments of a packet and ensuring they are reassembled correctly.
3. **Data Section:** The data section contains the actual data being transmitted. It is the part of the packet where the payload resides.
4. **DF Flag:** The DF flag is used to indicate whether a packet can be fragmented or not. When set, it means the packet should not be fragmented and must be sent as a whole.
5. **Packet Reassembly:** With the help of the DF flag and other metadata in the header, we can reassemble fragmented packets. This process is typically handled by devices at the network layer.

**Quotes:**
> Lecturer: "so, what is basically total packet size? total packet jeta amra pathai ekta network theke onno network e, it has two sections."
> Lecturer: "so, ami je fragmented packet gula reabar actually dekhte korte pari reassemble korte pari."

**Mone rakho:** The header size is fixed at 20 bytes, and the data size can vary based on the amount of data being transmitted. MTU refers to the maximum size of a packet that can be transmitted, including the header.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Fragmentation and Fragment Offset Calculation
**Ek line e:** Fragmentation and Fragment Offset Calculation

![Board 2: 4:00-12:34](figures_annotated/board_era2_400.jpg)

*Figure 2. The whiteboard during 4:00–12:34, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Maximum transmission unit · 2 Fragment offset · 3 Fragment offset · 4 Fragment offset · 5 Fragment offset


**Red Box 1 (MTU):** MTU stands for Maximum Transmission Unit, which is the maximum size of a single packet that can be transmitted without being fragmented. It includes both the header and data sections.

**Blue Box 2 (Fragment offset: 0/8):** Let's consider a scenario where we have a data size of 4000 bytes. The MTU is 1480 bytes, which means the header size is 20 bytes. Therefore, the data size that can be transmitted in one packet is 1460 bytes (1480 - 20).

**Orange Box 3 (Fragment offset: 1/8):** We need to calculate the fragment offset for different parts of the data. For instance, if the first fragment starts at 0, the offset will be 0. The size of the first fragment is 1479 bytes (1480 - 1).

**Green Box 4 (Fragment offset: 2/8):** The second fragment starts at 1480 and ends at 2959, so the offset for the second fragment is 1480.

**Purple Box 5 (Fragment offset: 3/8):** The third fragment starts at 2960 and ends at 4000, so the offset for the third fragment is 2960.

**Quotes:**
> Lecturer: "tahole amr jodi ekta packet er size hoy, just packet er data size, sorry, amr jodi ekta data size hoy, mone koro char haajar byte. char haajar byte, right."

**Mone rakho:** To calculate the fragment offset, we divide the data size by the MTU minus the header size. For the first fragment, the offset is 0. For the second fragment, the offset is 1480. For the third fragment, the offset is 2960. The fragment offset is calculated using the formula: `offset = (total data size - (number of fragments * MTU)) / 8`. The ceiling function is used to round up to the nearest whole number. In this case, the fragment offset for the third fragment is 370.

---

## Check yourself
1. What is the total packet size?
2. What does the DF flag do?
3. How is the fragment offset calculated?
4. What is the maximum size of a packet that can be transmitted without being fragmented?
5. Why is packet reassembly important?

### Answers
1. The total packet size is the combined size of the header section and the data section.
2. The DF flag indicates whether a packet can be fragmented or not; when set, it means the packet should not be fragmented.
3. The fragment offset is calculated using the formula: `offset = (total data size - (number of fragments * MTU)) / 8`.
4. The maximum size of a packet that can be transmitted without being fragmented is the MTU, which is 1480 bytes in this example.
5. Packet reassembly is important because it ensures that fragmented packets are correctly reassembled at the destination.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 3 kept, 0 removed. References to boxes that do not exist: 0.*
