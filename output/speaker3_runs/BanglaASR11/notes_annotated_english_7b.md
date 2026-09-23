# Network Parameters and Fragmentation
This lecture explains the network parameters TTL, DF, and MF, and their roles in packet fragmentation.

## Key takeaways
- TTL (Time to Live) indicates how long a packet can travel through a network before being discarded.
- DF (Don't Fragment) and MF (More Fragments) flags control packet fragmentation.
- Router behavior differs based on the values of the DF and MF flags.

<!-- boxes: 1=#d62828 -->
## Network Parameters and Fragmentation
**In one line:** This board explains the network parameters TTL, DF, and MF, and their roles in packet fragmentation.

![Board 1: 0:40-1:30](figures_annotated/board_era1_040.jpg)

*Figure 1. The whiteboard during 0:40–1:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Parameters


### Explanation
1. **TTL (Time to Live)**: Look at the red box 1. TTL is a parameter that indicates how long a packet can travel through a network before being discarded. In the table, TTL is set to 24, which means the packet can traverse up to 24 routers before being dropped.
   
2. **DF (Don't Fragment) and MF (More Fragments)**: The DF and MF flags are crucial for controlling packet fragmentation. The DF flag, shown as 0 in the table, indicates whether a packet should be fragmented or not. If DF is set to 1, the packet must not be fragmented; if it is set to 0, the packet can be fragmented. The MF flag, also set to 0, indicates whether there are more fragments following the current one. If MF is 1, there are more fragments; if it is 0, this is the last fragment.

3. **Router Behavior**: When a packet with DF set to 0 is received, the router will fragment the packet if necessary. However, if DF is set to 1, the router will drop the packet instead of fragmenting it, as it does not have the permission to do so.

**Quotes**
> Lecturer: "so, ekhon ekta drop kore diye ekta error er message pathabe sender e je tumi packet ta fragment kore dek, ponor osho bite e ami eta khorte parbona."  
> (In English: "so, when you drop a packet and send an error message to the sender who fragmented the packet, then that's what I'm talking about.")

**Remember:** The primary function of the DF flag is to prevent unnecessary fragmentation and ensure that packets are handled correctly by routers.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Understanding Packet Fragmentation and TTL
**In one line:** This board explains how packet fragmentation works and the significance of the Time to Live (TTL) field.

![Board 2: 1:40-2:48](figures_annotated/board_era2_140.jpg)

*Figure 2. The whiteboard during 1:40–2:48, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Protocol · 2 Smudge · 3 Packet Size · 4 Packet Size


### Explanation
1. **Time to Live (TTL):** The first row shows the TTL field, which indicates the number of hops a packet can make before being discarded. In the example, the TTL starts at 29 and decreases to 0, indicating an endless loop if not reset. (Look at the red box 1)
2. **Fragmentation Flags:** The next rows show the flags for fragmentation. The "Don't Fragment" (DF) flag is set, meaning the packet cannot be fragmented. The "More Fragments" (MF) flag is also set, indicating there are more fragments of the original packet. (Refer to the red box 1)
3. **Packet Size and Fragmentation:** The packet size is initially 4000 bytes. It is fragmented into smaller packets, each containing 1500 bytes. The first fragment is marked as the last fragment, indicated by the MF flag being set to 0. (See the orange box 3)
4. **Further Fragmentation:** Another packet of size 1000 bytes is created, which is not fragmented further. (Check the green box 4)


**Remember:** Understanding the fragmentation process and the role of the TTL and fragmentation flags is crucial for network communication.

---

## Check yourself
1. What is the purpose of the TTL field?
2. What do the DF and MF flags indicate?
3. How does a router handle a packet with the DF flag set to 1?

### Answers
1. The TTL field indicates how long a packet can travel through a network before being discarded.
2. The DF flag indicates whether a packet should be fragmented or not, while the MF flag indicates whether there are more fragments following the current one.
3. A router drops a packet with the DF flag set to 1 instead of fragmenting it.

---

*How these notes were made. Speech: transcript_loso.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 1 removed. References to boxes that do not exist: 0.*
