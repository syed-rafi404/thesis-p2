# BanglaASR35: Subnetting and Subnet Masking
Subnetting is the process of dividing a network into smaller parts.

## Key takeaways
- Subnetting helps in managing IP addresses efficiently by dividing a large network into smaller subnets.
- The prefix /16 provides 1024 usable host addresses, while /20 provides 2048 addresses.
- Fixed length subnet masking uses a constant number of bits for the subnet mask.
- Variable length subnet masking allows for more flexibility in allocating IP addresses within a network.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Subnetting: Introduction to Subnetting
**Ek line e:** Subnetting is the process of dividing a network into smaller parts.

![Board 1: 0:10-4:50](figures_annotated/board_era1_010.jpg)

*Figure 1. The whiteboard during 0:10–4:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Subnetting · 2 Prefix · 3 Calculation


- **Box 1 (red):** Subnetting
- **Box 2 (blue):** Prefix: /16
- **Box 3 (orange):** Calculation: 2^{16} \rightarrow 1024, 2^{11} \rightarrow 2048, 2^{16} \rightarrow 500

The lecturer explains that subnetting is the process of dividing a network into smaller portions, similar to how a tree-like structure branches out. This is done to manage IP addresses more efficiently.

> Lecturer: "subneting er bangla hocche, mane sub division korar ki ekta network bonek bor portion thake, so basically oita ter bi window branch er branch er bhag kora thikase, tree-like structure er ekta."

The lecturer then discusses the motivation behind subnetting. The primary reason is to avoid wasting IP addresses. For instance, if you have a network with multiple devices, you don't need all possible host addresses. Instead, you can allocate a smaller range of addresses that meet your needs.

> Lecturer: "but the main thing is, do we need all the host addresses for our network? amader ki shob gula host address dorkar director ker jonno? eoko hoite pare na, je for example amader host e ache macho ak ta, phar amader generate kore lakse tutu di por 11 ta host address amader ki dorkar ache."

The lecturer points out that the total number of possible IP addresses for IPv4 is 2^{32}, which is a huge number. However, for practical purposes, we often use a smaller prefix, such as /16, which provides 2^{16} \rightarrow 1024 usable host addresses.


The lecturer gives an example of a network with multiple devices and subnets. He calculates that using a /16 prefix, we get 1024 usable host addresses. However, if we need fewer addresses, we can use a smaller prefix, such as /20, which provides 2^{11} \rightarrow 2048 addresses.

> Lecturer: "for example, eto network ke onek dulla device ache, ebong dosader er devices ache, right. total ekta network ke jonno, not like mane ekta area er jonno, pura network er area jonno ekta dosader device shob mile ache. ebong prottekta branch ekba dosader er kore lage na, taina."

The lecturer then explains the calculation for a /16 prefix, showing that 2^{16} \rightarrow 1024 addresses are available. He also mentions that using a /20 prefix, we get 2^{11} \rightarrow 2048 addresses, which is more than enough for most networks.

> Lecturer: "so, amra ki bujhlam je for example ekta network deyo ache, je ekhane for example dhoro 16 ta beat deo, ekhn eto dula aa hosted diese beat ta amader laghtese na, ami eitul likhe feli, achae for example, etenar likhi eta khubi common hoye jekhane, like network dekhte chai,"

**Mone rakho:** Subnetting helps in managing IP addresses efficiently by dividing a large network into smaller subnets. The prefix /16 provides 1024 usable host addresses, while /20 provides 2048 addresses.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Subnetting: Fixed Length vs Variable Length Subnet Masking
**Ek line e:** In this section, we will discuss two types of subnetting: fixed length and variable length subnet masking.

![Board 2: 5:00-7:06](figures_annotated/board_era2_500.jpg)

*Figure 2. The whiteboard during 5:00–7:06, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Subnetting · 2 masking


1. **Fixed Length Subnet Masking (Box 1, Red):**
   - Look at the red box 1. Here, we have "Fixed length X ~ = LSM X". This represents a fixed-length subnet mask where the number of bits used for the subnet is constant across all subnets.
   - The formula LSM X indicates that the length of the subnet mask is fixed and equal to X.

2. **Variable Length Subnet Masking (Box 2, Blue):**
   - Now, let's move to the blue box 2. It says "Variable length subnet masking". This method allows for more flexibility in allocating IP addresses within a network.
   - The notation Y = LSM X here suggests that the length of the subnet mask can vary, depending on the specific needs of different subnets.

**Quotes:**
> Lecturer: "so now we are motivated to divide our network into several pieces, but oro ake jantheo beje koyta style e amra ke jinish e korte pari."

### Extra jana kotha (lecture e bola hoy ni)
In subnetting, we often need to divide a large network into smaller, manageable segments. Fixed length subnet masking is straightforward but less flexible, while variable length subnet masking offers more customization. Typically, we prefer to use variable length subnet masking (VLSM) because it allows us to allocate IP addresses more efficiently and effectively.

---

## Check yourself
1. What is the main reason for subnetting?
2. How many usable host addresses does a /16 prefix provide?
3. What is the difference between fixed length and variable length subnet masking?
4. Why is variable length subnet masking preferred over fixed length subnet masking?
5. What does the notation Y = LSM X represent?

### Answers
1. To avoid wasting IP addresses and manage them more efficiently.
2. A /16 prefix provides 1024 usable host addresses.
3. Fixed length subnet masking uses a constant number of bits for the subnet mask, while variable length subnet masking allows for more flexibility in allocating IP addresses within a network.
4. Because it allows for more efficient and effective allocation of IP addresses.
5. Y = LSM X represents that the length of the subnet mask can vary, depending on the specific needs of different subnets.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 5 kept, 1 removed. References to boxes that do not exist: 0.*
