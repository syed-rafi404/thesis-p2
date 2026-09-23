# BanglaASR38
THE SECTIONS

## Key takeaways
- VLSM, prefix calculation, host bits, network address generation, and signal generation.
- VLSM, network addressing, subnet mask, host bits, valid host addresses, subnet calculation.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 8=#0e7c86 9=#6b7f1a -->
## VLSM and Network Addressing
**In one line:** VLSM stands for Variable Length Subnet Mask.

![Board 1: 0:00-3:36](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–3:36, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 IP Address · 2 Logo · 3 VLSM · 4 Table · 5 IP Address · 6 Math · 7 Table · 8 Binary · 9 Formula


1. **Red Box 1 (IP Address: 192.0.0.1)**: This is the initial IP address mentioned.
2. **Blue Box 2 (Logo: RAMCA SUPER BOARD)**: This is the logo of the board.
3. **Orange Box 3 (VLSM: VLSM)**: VLSM stands for Variable Length Subnet Mask, which allows for more efficient allocation of IP addresses.
4. **Green Box 4 (Table)**: This table shows the network details including required addresses, 2^n, host, prefix, subnet, and third octate values.
5. **Purple Box 5 (IP Address: [192.168.0.1])**: This is another IP address shown.
6. **Pink Box 6 (Math: NATH)**: This refers to Network Address Translation.
7. **Brown Box 7 (Table)**: This table contains some numerical values.
8. **Teal Box 8 (Binary: 0000 0000)**: This binary representation is used in the context of subnetting.
9. **Olive Box 9 (Formula: 2 -> 130 32 - 2 = 30)**: This formula calculates the prefix length.

### Explanation
The lecturer explains the concept of VLSM and how to calculate the prefix length for a given number of required addresses. He starts by saying, "so jeta bolte silam amra je amra hocche, eijeporte eta host porshane jonno, ekta kore hocche ebe prefix ber korbe ekhane." This means, "so let's start, we need to find the host portion, and we will also get the prefix here."

The lecturer then calculates the prefix length using the formula 32 - 2 = 30. He explains, "mane er eijon ami eta kortesi, 32 minus 2 equals to 30. eita hocche am prefix." This means, "so, 32 minus 2 equals 30, and this is our prefix."

Next, he discusses how to determine the network address. He says, "next je address to hobe, for example, address a ba network a toh ami shuru kore dilam je hocche amader jeta amader chilo basically, initially 192, 168, 0.0. eta theke ami toh hocche aam, ei network ta shuru kore dite parbo." This means, "the next address should be, for example, starting from the network address, which is basically 192, 168, 0.0. From there, we will start the network."

He further explains the process of generating signals and bits. He mentions, "so signal generata ta ke amdekaj korbe? eita etu khub bhabe hoy dekhte hobe. prothom tar jonno, prothom tar jonno host bit koto amode nine na, tarole ami ki korbo? both nis ta je bit. both nis ta je bit er pichono e dikhte ki ami noy ta zero dibo age." This means, "so we will generate signals, and you will see it clearly. First, how many host bits do we have, and what will we do? We will have bits, and after the bits, we will put zeros."

The lecturer continues, "so eije chak ta akta zero hoye gache. amerekta octet er o ije full stromater dilam. diar por etar amar noy number zero, and dosh number zero, thikache? etar jono kurata toh ashe hocche ami zero, ar eije one ta je ikhane, one ta kintu ekhon third octet e ache, right?" This means, "so all these zeros are filled in the octet. After that, we have zeros, and then we have zeros, correct? So, we have zeros, and then we have ones here, right?"

Finally, he concludes, "so amra jodi amra jodi amra jodi amra jodi amra jodi same bhabe arekta host bit ta jonno signal generate ta ber kore thakole, ki bhabe value ta ajbe? toh amra dekhi prothome akta zero diye nilam, amra jodi same bhabe arekta zero perjone amra jodi amra jodi amra jodi amra jodi." This means, "so if we generate a signal for the same host bit, what will the value be? We see that we start with a zero, and if we have the same zero, we will have the same value."

**Remember:** VLSM, prefix calculation, host bits, network address generation, and signal generation.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 8=#0e7c86 9=#6b7f1a -->
## VLSM and Network Addressing
**In one line:** VLSM er main tree ta amra next class e shuru kori.

![Board 2: 3:50-6:12](figures_annotated/board_era2_350.jpg)

*Figure 2. The whiteboard during 3:50–6:12, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 IP Address · 2 VLSM · 3 IP Address · 4 Math · 5 Table · 6 Table · 7 Table · 8 Table · 9 Formula


1. **Red Box 1 (IP Address: 02. 0.0/22)**: This represents the initial IP address and its subnet mask.
2. **Blue Box 2 (VLSM: VL5M)**: VLSM stands for Variable Length Subnet Mask, which allows us to allocate subnets of different sizes.
3. **Orange Box 3 (IP Address: 192.168.0.1)**: This is an example IP address we will use to illustrate the concept.
4. **Green Box 4 (Math: MATH)**: We will use mathematical operations to determine the number of hosts and subnets.
5. **Purple Box 5 (Table: Networks | Req.Addrs. | 2^n | Host | Prefix | Subnet | 3rd octate, 2 val)**: This table helps us organize the required addresses, the number of subnets, and their prefixes.
6. **Pink Box 6 (Table: A | 503 | 512 | 9 | /23 | 124 | 11 | 1 val)**: This row shows that network A requires 503 addresses, can accommodate up to 512, has 9 hosts, uses a /23 prefix, and the third octet has 2 valid values.
7. **Brown Box 7 (Table: B | 253 | 256 | 8 | /24 | 11 | 1 | 1 val)**: Network B requires 253 addresses, can accommodate up to 256, has 8 hosts, uses a /24 prefix, and the third octet has 1 valid value.
8. **Teal Box 8 (Table: C | 102 | 128 | 7 | /25 | 4th octate, 128 val)**: Network C requires 102 addresses, can accommodate up to 128, has 7 hosts, uses a /25 prefix, and the fourth octet has 128 valid values.
9. **Olive Box 9 (Formula: 2 -> 130 32 - 2 = 30)**: This formula calculates the number of valid host addresses in a subnet.

### Background (not said in the lecture) (lecture e bola hoy ni)

**Remember:** VLSM, network addressing, subnet mask, host bits, valid host addresses, subnet calculation.

---

## Check yourself
1. What does VLSM stand for?
2. How did the lecturer calculate the prefix length for 503 required addresses?
3. What is the purpose of the table in the first section?
4. How many valid host addresses can Network A accommodate?
5. What is the formula used to calculate the number of valid host addresses in a subnet?

### Answers
1. VLSM stands for Variable Length Subnet Mask.
2. The lecturer calculated the prefix length using the formula \(32 - 2 = 30\).
3. The table in the first section organizes the required addresses, the number of subnets, and their prefixes.
4. Network A can accommodate up to 512 valid host addresses.
5. The formula used to calculate the number of valid host addresses in a subnet is \(2^{(32 - \text{prefix length})}\).

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
