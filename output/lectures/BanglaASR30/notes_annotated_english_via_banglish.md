# BanglaASR30: Network Layer: IP Addressing and Subnet Masking

The lecturer said: "In this lecture, we will discuss the structure of IP addressing and how subnet masks are used to determine the network portion of an IP address."

[[BOARD]]

## IP Address Structure
An IP address is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. It consists of four octets (8-bit segments), separated by dots. For example, `192.168.1.1`.

### Example:
- **IP Address:** 192.168.1.1

## Subnet Mask
A subnet mask is a 32-bit number used to determine which part of an IP address represents the network and which part represents the host. It is represented in dotted-decimal notation, similar to an IP address.

### Example:
- **Subnet Mask:** 255.255.255.0

### Explanation:
- **255.255.255.0** means that the first three octets (192.168.1) represent the network, and the last octet (0) represents the host.

## Determining the Network Portion
To determine the network portion of an IP address using a subnet mask, we perform a bitwise AND operation between the IP address and the subnet mask.

### Example:
- **IP Address:** 192.168.1.1
- **Subnet Mask:** 255.255.255.0

Performing the bitwise AND:

```
11000000.10101000.00000001.00000001  (192.168.1.1)
AND
11111111.11111111.11111111.00000000  (255.255.255.0)
--------------------------------------
11000000.10101000.00000001.00000000    (192.168.1.0)
```

The resulting value, `192.168.1.0`, is the network portion of the IP address.

## Conclusion
Understanding IP addressing and subnet masking is crucial for managing networks effectively. The network portion helps in routing traffic efficiently within a network.

[[BOARD]]

<!-- boxes: 1=#d62828 -->
## Network Layer: IP Addressing
**In one line:** Network layer er IP addressing er structure ta kemon hoy.

![Board 1: 0:00-6:00](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–6:00, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Layer


1. **Red Box 1 (Network Layer: Network layer IP d. 192.168.0.1 9x8->32bit 0000 0000 0000 0001 IPV4 addr. /24 192.168.0.1/24 1100 0000 192 Network por.)**
   - The lecturer starts by explaining the structure of an IP address. An IP address is divided into blocks, specifically octets, each containing 8 bits.
   - For example, the IP address `192.168.0.1` can be broken down into four octets: `192`, `168`, `0`, and `1`.
   - When we convert these decimal numbers to binary, we get `11000000`, `10101000`, `00000000`, and `00000001` respectively.
   - The prefix is used to indicate how many bits are used for the network portion and how many for the host portion. This is represented by a slash followed by a number, such as `/24` in the example `192.168.0.1/24`.

2. **Explanation:**
   - The lecturer explains that the prefix `24` means that the first 24 bits are used for the network portion, and the remaining 8 bits are used for the host portion.
   - Since there are 4 octets in an IP address, and each octet contains 8 bits, the total number of bits is 32.
   - In IPv4 addressing, the prefix `24` indicates that the first 24 bits are the network portion, and the last 8 bits are the host portion.
   - The lecturer mentions that the network portion is from the most significant bit (MSB) to the 24th bit, and the host portion is from the 25th bit to the least significant bit (LSB).

3. **Background (not said in the lecture):**
   - The network portion is used to identify the network to which the device belongs, while the host portion is used to identify the specific device within that network.
   - The prefix length helps in determining the size of the network and the number of hosts it can support. For example, a prefix of `/24` allows for 254 hosts in a network.

**Remember:** Network portion, host portion, prefix, MSB, LSB, IPv4 addressing.

<!-- boxes: 1=#d62828 -->
## Network Layer: Subnet Masking
**In one line:** Subnet masking is used to determine which part of an IP address is the network address.

![Board 2: 6:10-12:10](figures_annotated/board_era2_610.jpg)

*Figure 2. The whiteboard during 6:10–12:10, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network layer


1. **Red Box 1 (Network layer):** The network layer uses IP addresses to identify hosts on a network. Here, we have an IP address `192.168.0.1/25` and a subnet mask `255.255.255.0`.

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
   - The subnet mask `255.255.255.0` tells us that the first three octets (8 bits each) are the network address.
   - The fourth octet is the host address.
   - To find the network address, we take the first three octets and set them to `1` where the subnet mask is `1`, and set the rest to `0`.
   - This gives us the network address `192.168.0.0`.

5. **Quote:**

6. **Background (not said in the lecture):**
   - When configuring a network, we need to know the network address and the subnet mask to correctly assign IP addresses to devices. This ensures that all devices on the same network can communicate with each other.
   - The subnet mask helps in determining the network and host portions of an IP address, making it easier to manage and route traffic within a network.

---



---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 1.*
