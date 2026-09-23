# BanglaASR40
In this video, we will learn how to calculate the range of usable IP addresses for different networks.

## Key takeaways
- Understand the concept of network addressing and its importance.
- Learn how to determine the range of usable IP addresses for a given network.
- Recognize the difference between the network address and the usable IP range.
- Apply logical AND operations to find the usable IP range for subnets.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Gate Diagram and Network Addressing

In this video, we will learn how to calculate the range of usable IP addresses for different networks.

![Board 1: 0:20-0:50](figures_annotated/board_era1_020.jpg)

*Figure 1. The whiteboard during 0:20–0:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Date · 2 Time


1. **Red Box 1 (Date):** The date mentioned is 8.0.0/22. This is the date when we are discussing this topic.
   
2. **Blue Box 2 (Time):** The current time is 3.13. This helps us keep track of where we are in the lecture timeline.

3. **Gate Diagram:** The gate diagram on the board shows inputs A and B going into an AND gate, with the output labeled as A*B. This represents the logical AND operation between two inputs.

The lecturer said: "Okay guys, so last video te amra hocche mane time beshibe karon ne just network address gulai ber kor silam, je first eis e debal ip korte pothe ta netor ke jolno, ar ei video te amra oschi wadze range gula ber korbo, right? Thikache?" This means, "In the last video, we learned about time slicing and obtaining network addresses, which help us divide the IP space. Now, in this video, we will calculate the range of usable IP addresses for different networks, right?"

The lecturer further clarified: "Amader potom network er jemon amr usable id techelem ujshomore ekta user name ta." This translates to, "For each subsequent network, we will assign a unique user name."

The diagram shows the logical AND operation, which is fundamental in determining the range of IP addresses. The AND gate takes two inputs, A and B, and outputs A*B, meaning the result is true only if both inputs are true.

The lecturer mentioned: "Second network er jonno dui jog kore peye chila merita. Third network er jonno amar peye chila merita. Amr likhe dekhe, for a we get this, for b we get this, for c, for d, for e, for f." This means, "For the second network, we will consider two subnets. For the third network, we will also consider two subnets. As you can see, for A we get this, for B we get this, and so on."

The lecturer added: "Guys, amr eke calculation mistake tomla but jine hasha shikoro na please hai." This translates to, "Guys, there might be a calculation mistake here, but please don't worry about it for now."

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding the AND gate is crucial for calculating the range of IP addresses. It helps in dividing the IP space efficiently among different networks. By using AND operations, we can determine which IP addresses are available for specific subnets.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## Usable IP Range and Network Addressing
**One line:** We have been given the IP range for a network.

![Board 2: 1:00-3:04](figures_annotated/board_era2_100.jpg)

*Figure 2. The whiteboard during 1:00–3:04, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Addressing · 2 Usable IP Range · 3 IP Address · 4 IP Address · 5 IP Address


1. **Red Box (Network Addressing):** The red box 1 shows the network addressing as 192.168.0.0/22. This is the starting address of our network.
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
> Lecturer: "So, etar je range ta hbe mannay last address er seta prothome usable ip, last usable ip jeita hobe sheta theke ekcom."
> Lecturer: "Usable ip nikhe dibe bore. Usable ip. Usable ip. Thikache?"

### Extra Information
For determining the usable IP range in our network, the last address is excluded, and the usable IP range starts from the first usable IP address and ends just before the last address. In this case, we include all the IP addresses except the last one. If the end devices are at the last address, we exclude that address.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 8=#0e7c86 9=#6b7f1a 10=#1b2a6b -->
## IP Address Ranges and Network Configuration

![Board 3: 3:30-5:50](figures_annotated/board_era3_330.jpg)

*Figure 3. The whiteboard during 3:30–5:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Usable IP · 2 Usable IP · 3 Usable IP · 4 Usable IP · 5 Usable IP · 6 Usable IP · 7 Usable IP · 8 Usable IP · 9 Usable IP · 10 Usable IP

**In one line:** We need to assign this address, and then another address.

The lecturer said: "We will configure the network by assigning IP addresses."

---

## Check yourself
1. What is the starting address of the network 192.168.0.0/22?
2. What is the last address in the network 192.168.0.0/22?
3. How many usable IP addresses are there in the network 192.168.0.0/22?
4. What is the range of usable IP addresses for the network 192.168.0.0/22?
5. Explain the difference between the network address and the usable IP range.

### Answers
1. The starting address of the network 192.168.0.0/22 is 192.168.0.0.
2. The last address in the network 192.168.0.0/22 is 192.168.2.255.
3. There are 1022 usable IP addresses in the network 192.168.0.0/22.
4. The range of usable IP addresses for the network 192.168.0.0/22 is from 192.168.0.1 to 192.168.2.254.
5. The network address (192.168.0.0) is the starting address of the network, while the usable IP range includes all IP addresses from the first usable IP (192.168.0.1) to the last usable IP (192.168.2.254), excluding the network address and the broadcast address (192.168.2.255).

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (2 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
