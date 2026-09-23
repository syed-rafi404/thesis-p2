# VLSM Variable Length Subnet Masking
The lecturer said: "The lecture covers the concept of VLSM (Variable Length Subnet Masking) and its importance in managing IP addresses efficiently."

## Key takeaways
- VLSM stands for Variable Length Subnet Masking.
- VLSM is a short-term solution for managing IP addresses efficiently.
- IPv6 is the long-term solution for addressing needs, using 128 bits.
- VLSM allows flexible subnetting and efficient IP address allocation.
- The network address is calculated by determining the network portion and setting the remaining bits to zero.
- VLSM helps in managing large networks by dividing them into smaller subnets.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## VLSM Variable Length Subnet Masking
**In one line:** VLSM stands for Variable Length Subnet Masking.

![Board 1: 0:10-3:12](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–3:12, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Topic · 2 Long term · 3 Bits · 4 Formula


- **Box 1 (red):** Topic: VLSM Variable Length Subnet Masking
- **Box 2 (blue):** Long term: Long term IPv6
- **Box 3 (orange):** Bits: 128 bits
- **Box 4 (green):** Formula: 1/2^128

The lecturer starts by explaining VLSM, which stands for Variable Length Subnet Masking. He mentions that VLSM is a short-term solution for managing IP addresses efficiently. The motivation behind VLSM is to provide flexibility in subnetting, allowing us to allocate different sizes of subnets based on the network requirements.

The lecturer then explains that VLSM is a process used for short-term solutions, specifically for IPv4 addressing. He contrasts this with long-term solutions, which involve using IPv6 addresses. IPv6 is mentioned as the long-term solution for addressing needs.

The board shows that IPv6 uses 128 bits, which is indicated in Box 3. The lecturer emphasizes that with 128 bits, we can accommodate a vast number of devices, estimated to be in the billions or trillions. This is represented mathematically as 2^{128} in Box 4.

The lecturer further explains that while 2^{128} is a very large number, it is still a finite quantity. He suggests that this is a short-term solution for now, but it will eventually run out. The key point is that IPv6 addresses are more efficient than IPv4 addresses, especially when considering the header size. The next video will delve into the details of IPv4 headers and how they compare to IPv6 headers.

The lecturer concludes by stating that VLSM is a clear and straightforward concept, and we don't need to complicate it with too many terms. The main idea is that VLSM provides an efficient way to manage IP addresses in the short term.

**Remember:** VLSM allows flexible subnetting, 2^{128} represents the number of devices IPv6 can support, and IPv6 is more efficient than IPv4.

<!-- boxes: 1=#d62828 -->
## VLSM Variable Length Subnet Masking
**In one line:** Amra aage jeta korsi, je amar je sub er sub network ta bhag kori.

![Board 2: 3:20-8:50](figures_annotated/board_era2_320.jpg)

*Figure 2. The whiteboard during 3:20–8:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Address


1. **Red Box 1 (Network Address):** Net Add2. 192.168.0.0/2

The lecturer starts by explaining that we will divide a network into smaller subnetworks, similar to how branches can be divided. He gives an example where we start with a single address and divide it into multiple subnetworks. This example involves a network address, which is 24 bits long.

2. **Explanation:**
   - The lecturer explains that the network address is 24 bits long, meaning there are 256 possible addresses in this network.
   - He introduces a scenario with three routers: R1, R2, and R3, and mentions that there are some devices connected to these routers.
   - To make the scenario more complex, he states that there are 850 devices in total, with 500 devices being end devices.
   - The lecturer then discusses the concept of a prefix, which is 24 bits, and explains that beyond the prefix, we need to consider the host portion of the address.
   - He mentions that we can have up to 250 devices in this network, but we need to ensure that we allocate enough space for hosts.
   - The lecturer then calculates the number of bits required for the host portion. He explains that if we need to accommodate 850 devices, we need to use 2^{10}, which is 1024, to cover all devices.
   - He clarifies that 2^{10} requires 10 bits for the host portion, leaving us with 22 bits for the network portion.
   - The lecturer emphasizes that we need to use 2^{10} to ensure we have enough space for hosts, and this will allow us to create multiple subnets.


### Background (not said in the lecture)
Ami jemon er ekta gula host er host portion er kototuk door kor, host portion. eta pori er ke deya thake, ami just maner trial and error kore, apnode back team ta kora dekhi je apnara basically ini, maner kiboy bujh when jemon er ekta gula host er.

<!-- boxes: 1=#d62828 -->
## VLSM: Variable Length Subnet Masking
**In one line:** VLSM is a method to allocate IP addresses efficiently.

![Board 3: 9:00-11:24](figures_annotated/board_era3_900.jpg)

*Figure 3. The whiteboard during 9:00–11:24, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 VLSM


1. **Red Box 1 (VLSM):** The board starts with the term "VLSM" which stands for Variable Length Subnet Masking. This technique allows us to allocate IP addresses more flexibly within a network.

2. **IP Address 192.168.0.2/22:** The lecturer mentions an IP address `192.168.0.2/22`. Here, `/22` indicates the subnet mask, meaning the first 22 bits are used for the network portion.

3. **Network Address Calculation:** The lecturer explains that we need to calculate the network address. He breaks down the calculation as follows: `128 + 64 + 32 + 16 = 250`. This sum represents the network address in decimal form.

4. **Broadcast Address:** The lecturer clarifies that we cannot use the broadcast address, which would be the last address in the network. Instead, we use the network address and fill in the remaining bits with zeros to get the network address.

5. **Subnet Masking:** The lecturer emphasizes that when we apply subnet masking, the bits after the network portion should be zeros. For example, if we have a subnet mask of `/22`, the remaining bits will be zeros, indicating the end of the network address.

6. **Network Address Calculation:** The lecturer states that the network address is `192.168.240.0`. He explains that this is derived from the given IP address and subnet mask.

7. **Device Count:** The lecturer mentions that there can be up to 250 end devices (`250 (END devices)`), 850 total devices, 500 end devices, and 100 end devices. These numbers help in understanding the capacity of the network.

> Lecturer: "so, amader jodi overall jinish ta hoy je hocche amader ekhane byche ta bit, apner network potion, amader ei je netlock address ta khetre, amra broadcast address dhoro korte parbo na."

The lecturer said: "So, if our goal is to have a certain number of devices, we need to consider the bits we have for the network portion, and we cannot use the broadcast address."

---

## Check yourself
1. What does VLSM stand for?
2. How many bits does IPv6 use?
3. What is the network address for 192.168.0.2/22?
4. How many end devices can be accommodated in a /22 subnet?
5. Why is VLSM important in modern networking?

### Answers
1. VLSM stands for Variable Length Subnet Masking.
2. IPv6 uses 128 bits.
3. The network address for 192.168.0.2/22 is 192.168.0.0.
4. A /22 subnet can accommodate up to 254 end devices.
5. VLSM is important in modern networking because it allows efficient IP address allocation and management of large networks by dividing them into smaller subnets.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (1 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
