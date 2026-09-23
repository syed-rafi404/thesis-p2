# Network Addressing and Subnets
The lecture covers network addressing and its subnets, including key components like network address, subnet mask, broadcast address, and host address.

## Key Takeaways
- Network address, subnet mask, broadcast address, and host address are key components in network addressing.
- Understanding the network address and last usable address is crucial.
- When calculating the last usable address, consider the carry-over from the last octet.
- The subnet mask and broadcast address help define the network range.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Network Addressing: B2-22 -> 10 S.R -> N.A -> 192.168.0.0/22 E.R -> B.A -> 192.168.3.255 V.A -> 192.168.0.1 / 23 V.B -> 192.168.2.1 / 24 V.C -> 192.168.3.1 / 25 V.D -> 192.168.3.129 / 30
**In one line:** This is how we represent network addresses and their subnets.

![Board 1: 0:00-2:20](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–2:20, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Addressing · 2 Network Addressing


1. **Red Box 1**: Look at the red box 1. Here, we have a hierarchical representation of network addressing. Starting from B2-22, we move to 10 S.R, then to N.A, which represents the network address 192.168.0.0/22. From there, we go to E.R, which is the broadcast address 192.168.3.255. Then, we have various variable addresses (V.A, V.B, V.C, V.D) with different subnet masks (23, 24, 25, 30).

2. **Blue Box 2**: In the blue box 2, we see more variable addresses (V.E, V.F) with subnet masks 30.

The lecturer explained that in network addressing, we often need to represent the network, subnet, and host parts clearly. For example, if we have a network address like 192.168.0.0/22, it means the first 22 bits are used for the network, and the remaining 10 bits are used for hosts.


The lecturer also mentioned that the last method is better because it follows a consistent structure, making it easier to understand and manage. He emphasized that each node should be properly represented in a tree structure, where each level corresponds to a specific part of the address.

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding network addressing is crucial for managing IP addresses effectively. By breaking down the address into network, subnet, and host parts, we can easily identify and manage different segments of a network. This helps in setting up and troubleshooting networks efficiently.

**Remember:** Network address, subnet mask, broadcast address, and host address are key components in network addressing. Understanding these concepts is essential for managing and troubleshooting networks.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## Network Address Calculation: B2-22 -> 10 S.R -> N.A -> 192.168.0.0/22 E.R -> B.A -> 192.168.3.255 V.A -> 192.168.0.1 / 23 V.B -> 192.168.2.1 / 24 V.C -> 192.168.3.1 / 25 V.D -> 192.168.3.129 / 30

**In one line:** Amader ekhane jokhn ekhane ekta ekta ekta ekta kintu hoy, ekta kintu hoy, as duisho konchan no, 255 porjonto hoy.

![Board 2: 2:30-5:08](figures_annotated/board_era2_230.jpg)

*Figure 2. The whiteboard during 2:30–5:08, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 IP Address · 2 Network Address Calculation · 3 Subnet Mask · 4 Broadcast Address


1. **Box 1 (red):** IP Address: 192.168.0.1
2. **Box 2 (blue):** Network Address Calculation: 192.168.2.0/22 192.168.3.255
3. **Box 3 (orange):** Subnet Mask: 192.168.3.132
4. **Box 4 (green):** Broadcast Address: 192.168.3.137

The lecturer said: "Amader aa ekhon jodi amra neto er jono range ber korre chai, amader aa tomar hocche er last usable like koto hobe, eta hocche ber koto important."

**Box 2 (blue):** The network address calculation involves determining the last usable address. For example, if we have 192.168.2.0/22, the last usable address is 192.168.3.255. This is crucial for setting up the correct network parameters.

**Box 3 (orange):** The subnet mask 192.168.3.132 helps us understand how many addresses are available in the network. It is derived from the /22 notation, which means the first 22 bits are used for the network address.

**Box 4 (green):** The broadcast address 192.168.3.137 is the last address in the network range. It is used to send data to all devices on the network.

The lecturer said: "Amra jodi ekhane zero thake, zero theke jodi amra ek, two or korte chai, toh ki hoy, third octet thake, shekhan deke ek minus hoy, ar fourth octet ta hoy, duisho poronchanno. Toh ei problem er khetre ekhane ki hobe, amra jetoi last octet a zero er"

In summary, the key points are:
- Understanding the network address and last usable address is crucial.
- When calculating the last usable address, consider the carry-over from the last octet.
- The subnet mask and broadcast address help define the network range.

---

## Check Yourself
1. What is the network address for 192.168.2.0/22?
2. What is the last usable address for 192.168.2.0/22?
3. What is the subnet mask for 192.168.3.129/30?
4. What is the broadcast address for 192.168.3.129/30?
5. How do you determine the last usable address when the last octet is 0?

### Answers
1. The network address for 192.168.2.0/22 is 192.168.2.0.
2. The last usable address for 192.168.2.0/22 is 192.168.3.254.
3. The subnet mask for 192.168.3.129/30 is 255.255.255.248.
4. The broadcast address for 192.168.3.129/30 is 192.168.3.131.
5. To determine the last usable address when the last octet is 0, subtract 1 from the last octet and carry over to the next octet.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
