# BanglaASR30: Network Layer: IP Addressing and Subnet Masking
Network layer er ip addressing er structure ta kemon hoy.

## Key takeaways
- Network portion
- Host portion
- Prefix
- MSB
- LSB
- IPv4 addressing
- Subnet masking
- Network address
- Subnet mask

<!-- boxes: 1=#d62828 -->
## Network Layer: IP Addressing
**Ek line e:** Network layer er ip addressing er structure ta kemon hoy.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Layer


1. **Red Box 1 (Network Layer: Network layer Ip d. 192.168.0.1 9x8->32bit 0000 0000 0000 0001 IpV4 addr. /24 192.168.0.1/24 1100 0000 192 Network por.)**
   - The lecturer starts by explaining the structure of an IP address. An IP address is divided into blocks, specifically octets, each containing 8 bits.
   - For example, the IP address `192.168.0.1` can be broken down into four octets: `192`, `168`, `0`, and `1`.
   - When we convert these decimal numbers to binary, we get `11000000`, `10101000`, `00000000`, and `00000001` respectively.
   - The prefix is used to indicate how many bits are used for the network portion and how many for the host portion. This is represented by a slash followed by a number, such as `/24` in the example `192.168.0.1/24`.

2. **Explanation:**
   - The lecturer explains that the prefix `24` means that the first 24 bits are used for the network portion, and the remaining 8 bits are used for the host portion.
   - Since there are 4 octets in an IP address, and each octet contains 8 bits, the total number of bits is 32.
   - In IPv4 addressing, the prefix `24` indicates that the first 24 bits are the network portion, and the last 8 bits are the host portion.
   - The lecturer mentions that the network portion is from the most significant bit (MSB) to the 24th bit, and the host portion is from the 25th bit to the least significant bit (LSB).

3. **Extra jana kotha:**
   - The network portion is used to identify the network to which the device belongs, while the host portion is used to identify the specific device within that network.
   - The prefix length helps in determining the size of the network and the number of hosts it can support. For example, a prefix of `/24` allows for 254 hosts in a network.

**Mone rakho:** Network portion, host portion, prefix, MSB, LSB, IPv4 addressing.

<!-- boxes: 1=#d62828 -->
## Network Layer: Subnet Masking
**Ek line e:** Subnet masking is used to determine which part of an IP address is the network address.

![Board 2: 6:10-12:10](figures_annotated/board_era2_610.jpg)

*Figure 2. The whiteboard during 6:10–12:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network layer


1. **Red Box 1 (Network layer):** The network layer uses IP addresses to identify hosts on a network. Here, we have an IP address `192.168.0.1/25` and a subnet mask `1111 1111. 1111 1111. 1111 1111. 0000 0000`.

2. **Explanation:**
   - The subnet mask helps us understand which part of the IP address is the network address and which part is the host address.
   - For example, if our prefix is `1100 0000. 1010 1000. 0000 0000. 0000 0001`, the subnet mask will help us determine the network address.
   - We start by identifying the network portion and setting all bits in that portion to `1`.
   - The remaining bits are set to `0`.

3. **Truth Table in Box 5:**
   - | IPv4 Addr. | Subnet Mask | Network Address |
   - |------------|-------------|-----------------|
   - | 1100 0000. 1010 1000. 0000 0000. 0000 0001 | 1111 1111. 1111 1111. 1111 1111. 0000 0000 | 1100 0000. 1010 1000. 0000 0000. 0000 0000 |

4. **Explanation:**
   - The subnet mask `1111 1111. 1111 1111. 1111 1111. 0000 0000` tells us that the first three octets (8 bits each) are the network address.
   - The fourth octet is the host address.
   - To find the network address, we take the first three octets and set them to `1` where the subnet mask is `1`, and set the rest to `0`.
   - This gives us the network address `192.168.0.0`.

5. **Quote:**
   > "toh basically eita amade total man subnet mask kintu."

6. **Extra jana kotha:**
   - When configuring a network, we need to know the network address and the subnet mask to correctly assign IP addresses to devices. This ensures that all devices on the same network can communicate with each other.
   - The subnet mask helps in determining the network and host portions of an IP address, making it easier to manage and route traffic within a network.

---

## Check yourself
1. What is the binary representation of the IP address `192.168.0.1`?
2. What does the prefix `/24` indicate in an IP address?
3. How do you determine the network address using a subnet mask?
4. What is the purpose of a subnet mask in network configuration?
5. Explain the difference between the network portion and the host portion of an IP address.

### Answers
1. The binary representation of the IP address `192.168.0.1` is `11000000.10101000.00000000.00000001`.
2. The prefix `/24` indicates that the first 24 bits are used for the network portion, and the remaining 8 bits are used for the host portion.
3. To determine the network address using a subnet mask, you take the IP address and apply the AND operation with the subnet mask. The result is the network address.
4. The purpose of a subnet mask is to help determine which part of an IP address is the network address and which part is the host address, ensuring correct routing and communication within a network.
5. The network portion identifies the network to which the device belongs, while the host portion identifies the specific device within that network.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 1 kept, 0 removed. References to boxes that do not exist: 1.*
