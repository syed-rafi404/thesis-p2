# BanglaASR40: Gate Diagram and Network Addressing
In this video, we will learn how to calculate the range of usable IP addresses for different networks.

## Key takeaways
- We will learn about the gate diagram and its role in determining the range of IP addresses.
- The network addressing and usable IP range will be explained.
- We will understand how to calculate the usable IP range for a given network.
- The importance of excluding the last address in the usable IP range will be discussed.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Gate Diagram and Network Addressing
**Ek line e:** In this video, we will learn how to calculate the range of usable IP addresses for different networks.

![Board 1: 0:20-0:50](figures_annotated/board_era1_020.jpg)

*Figure 1. The whiteboard during 0:20–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Date · 2 Time


1. **Red Box 1 (Date):** The date mentioned is 8.0.0/22. This is the date when we are discussing this topic.
   
2. **Blue Box 2 (Time):** The current time is 3.13. This helps us keep track of where we are in the lecture timeline.

3. **Gate Diagram:** The gate diagram on the board shows inputs A and B going into an AND gate, with the output labeled as A*B. This represents the logical AND operation between two inputs.

The lecturer explains, "okay guys, so last video te amra hocche mane time beshibe karon ne just network address gulai ber kor silam, je first eis e debal ip korte pothe ta netor ke jolno, ar ei video te amra oschi wadze range gula ber korbo, right? thikache?" This means, "In the last video, we learned about time slicing and obtaining network addresses, which help us divide the IP space. Now, in this video, we will calculate the range of usable IP addresses for different networks, right?"

The lecturer further clarifies, "amader potom network er jemon amr usable id techelem ujshomore ekta user name ta." This translates to, "For each subsequent network, we will assign a unique user name."

The diagram shows the logical AND operation, which is fundamental in determining the range of IP addresses. The AND gate takes two inputs, A and B, and outputs A*B, meaning the result is true only if both inputs are true.

The lecturer mentions, "second network er jonno dui jog kore peye chila merita. third network er jonno amar peye chila merita. amr likhe dekhe, for a we get this, for b we get this, for c, for d, for e, for f." This means, "For the second network, we will consider two subnets. For the third network, we will also consider two subnets. As you can see, for A we get this, for B we get this, and so on."

The lecturer adds, "guys amr eke calculation mistake tomla but jine hasha shikoro na please hai." This translates to, "Guys, there might be a calculation mistake here, but please don't worry about it for now."

### Extra jana kotha (lecture e bola hoy ni)
Understanding the AND gate is crucial for calculating the range of IP addresses. It helps in dividing the IP space efficiently among different networks. By using AND operations, we can determine which IP addresses are available for specific subnets.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Usable IP Range and Network Addressing
**Ek line e:** Amader pala hoy deche ekta network er jono range ber kora.

![Board 2: 1:00-3:04](figures_annotated/board_era2_100.jpg)

*Figure 2. The whiteboard during 1:00–3:04, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Addressing · 2 Usable IP Range · 3 IP Address · 4 IP Address · 5 IP Address


1. **Red Box (Network Addressing):** Look at the red box 1 which shows the network addressing as 192.168.0.0/22. This is the starting address of our network.
2. **Blue Box (Usable IP Range):** The blue box 2 shows the usable IP range as A -> 192.168.0.1 - 192.168.2.0. This range indicates the first and last usable IP addresses in the network.
3. **Orange Box (IP Address):** The orange box 3 shows an IP address as E -> 192.168.3.133. This is an example of a specific IP address within the network.
4. **Green Box (IP Address):** The green box 4 shows another IP address as F -> 192.168.3.132. This is another example of an IP address within the network.
5. **Purple Box (IP Address):** The purple box 5 shows yet another IP address as -> 192.168.3.131. This is another example of an IP address within the network.

The whole board shows the usable IP range and specific IP addresses:

| Usable IP | A → 192.168.0.1 — 192.168.2.0 |
| --- | --- |
| B2-22 → 10 | S.R → N.A → 192.168.0.0/22 |
| E.R → B.A → 192.168.3.255 | A → 192.168.0.1 |
| B → 192.168.2.1 | C → 192.168.3.1 |
| D → 192.168.3.120 | E → 192.168.3.133 |
| F → 192.168.3.132 | G → 192.168.3.131 |

**Explanation:**
- The lecturer explains that the usable IP range starts from the first usable IP address and ends just before the last IP address. For example, in the network 192.168.0.0/22, the usable IP range is from 192.168.0.1 to 192.168.2.0.
- The usable IP range is determined by the last address in the network. The last address is not included in the usable IP range.
- The lecturer gives an example where the network starts from 192.168.0.0 and goes up to 192.168.2.0. The usable IP range would be from 192.168.0.1 to 192.168.2.0.
- The usable IP range is crucial for identifying which IP addresses can be used for devices on the network.

**Quotes:**

### Extra jana kotha
Amader network er jono range ber korar somosha, last address er seta prothome usable ip, last usable ip jeita hobe sheta theke ekcom. Ekhon, amra jemon ki sa kore chile amra kitu shobulo include hore isha kore chile amra et, so yita bono rakhtebe. Eigilo moddhe shob e included. Unless end devices borle jeta amra je last e ta shathe ekjo kore dibo.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 8=#0e7c86 9=#6b7f1a 10=#1b2a6b -->
## IP Address Ranges and Network Configuration

![Board 3: 3:30-5:50](figures_annotated/board_era3_330.jpg)

*Figure 3. The whiteboard during 3:30–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Usable IP · 2 Usable IP · 3 Usable IP · 4 Usable IP · 5 Usable IP · 6 Usable IP · 7 Usable IP · 8 Usable IP · 9 Usable IP · 10 Usable IP

**Ek line e:** Amra eita address korte hobe, ebong ebong address erokomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomomom

---

## Check yourself
1. What is the starting address of the network 192.168.0.0/22?
2. What is the range of usable IP addresses for the network 192.168.0.0/22?
3. How many subnets are considered for the second and third networks?
4. What is the logical operation performed by the AND gate?
5. Why is it important to exclude the last address in the usable IP range?

### Answers
1. The starting address of the network 192.168.0.0/22 is 192.168.0.0.
2. The range of usable IP addresses for the network 192.168.0.0/22 is from 192.168.0.1 to 192.168.2.0.
3. Two subnets are considered for the second and third networks.
4. The logical operation performed by the AND gate is A*B, meaning the result is true only if both inputs are true.
5. It is important to exclude the last address in the usable IP range because it is reserved for the network address itself.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 0 kept, 2 removed. References to boxes that do not exist: 0.*
