# VLSM
VLSM stands for Variable Length Subnet Masking.

## Key takeaways
- VLSM is a technique used in IP addressing where subnets can have different lengths.
- The prefix length is determined by the number of host bits required.
- The network address is calculated by setting the host bits to 0.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## VLSM
**In one line:** VLSM stands for Variable Length Subnet Masking.

![Board 1: 0:00-13:32](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–13:32, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Formula · 3 Formula · 4 Formula


1. **VLSM (Red Box 1):**
   - VLSM is a technique used in IP addressing where subnets can have different lengths. This allows for more efficient allocation of IP addresses.

2. **Network Requirements (Blue Box 2):**
   - The table shows the network requirements and the corresponding number of hosts needed.
   - For example, Network A requires 503 additional addresses, which translates to a /23 prefix (256 - 2 - 2 = 252 usable addresses).

3. **Subnet Calculation (Orange Box 3):**
   - To calculate the number of hosts, we use the formula 2^h, where h is the number of host bits.
   - For Network A, 2^{10} = 1024 host addresses are available.
   - The network address is calculated by setting the host bits to 0, resulting in 512 network addresses.

4. **Prefix Calculation (Green Box 4):**
   - The prefix length is determined by the number of host bits required.
   - For Network A, the prefix length is 23 (32 - 10 = 22), meaning 10 bits are allocated for hosts.

5. **Router Configuration (Table):**
   - Router R2 and R3 are configured with specific host addresses.
   - R2 and R3 are connected to a single network, which requires 250 hosts.
   - The table also shows the total number of devices and the required network addresses.

6. **Network Design (Table):**
   - Network A requires 503 additional addresses, Network B requires 253, Network C requires 102, and so on.
   - The table lists the number of devices and the required network addresses for each network.

7. **Example Calculation:**
   - For Network A, the total number of devices is 503.
   - The network address is 102.168.0.17, and the broadcast address is 102.168.0.255.
   - The required addresses are marked as follows: Network A, Network B, Network C, etc.

8. **Shortcut for Prefix Calculation:**
   - The shortcut for calculating the prefix is 32 - number of host bits.
   - For example, for 10 host bits, the prefix is 32 - 10 = 22, which is represented as /22.

9. **Host Bits Calculation:**
   - The number of host bits is determined by the number of devices.
   - For 500 devices, the number of host bits is 9 (32 - 23 = 9).

10. **Network Address Calculation:**
    - The network address is calculated by setting the host bits to 0.
    - For 1024 host addresses, the network address is 102.168.0.0, and the broadcast address is 102.168.0.1023.

11. **Default Gateway Address:**
    - The default gateway address is already provided in the configuration.
    - For example, the default gateway address for Network A is 102.168.0.17.

12. **Summary:**
    - VLSM allows for efficient IP address allocation by using variable-length subnet masks.
    - The prefix length is calculated based on the number of host bits required.

**Remember:** VLSM helps in efficiently allocating IP addresses by allowing different subnet sizes. The prefix length is determined by the number of host bits required, and the network address is calculated by setting the host bits to 0.

---

## Check yourself
1. What does VLSM stand for?
2. How many host addresses are available for a /23 prefix?
3. What is the formula used to calculate the number of hosts?
4. What is the shortcut for calculating the prefix length?
5. How is the network address calculated?

### Answers
1. VLSM stands for Variable Length Subnet Masking.
2. For a /23 prefix, 254 host addresses are available (256 - 2 = 254).
3. The formula used to calculate the number of hosts is \(2^h\), where \(h\) is the number of host bits.
4. The shortcut for calculating the prefix length is \(32 - \text{number of host bits}\).
5. The network address is calculated by setting the host bits to 0.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
