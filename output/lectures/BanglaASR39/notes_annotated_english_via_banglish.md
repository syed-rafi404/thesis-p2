# VLSM: Variable Length Subnet Mask
In this lecture, we will learn about VLSM and how to allocate network addresses efficiently.

---

## Key takeaways
- VLSM allows for the allocation of subnets of different sizes.
- The formula \(2^h - 2\) is used to calculate the number of usable IP addresses in a subnet.
- The third and fourth octets are calculated based on the required number of hosts and the prefix length.
- Proper subnetting ensures efficient use of IP addresses and reduces waste.

---

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf 6=#d63384 7=#8d5524 8=#0e7c86 9=#6b7f1a 10=#1b2a6b -->
## VLSM: Variable Length Subnet Mask
**In one line:** In this lecture, we will learn about VLSM and how to allocate network addresses efficiently.

![Board 1: 0:00-0:40](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–0:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 IP Address · 2 Board Brand · 3 IP Address · 4 Number · 5 Number · 6 Letter · 7 Slash · 8 Number · 9 Formula · 10 Text


1. **Red Box 1**: IP Address: 192.0.0/22
   - This is our starting IP address. We will use this to understand subnetting.
   
2. **Blue Box 2**: Board Brand: AMICA SUPER BOARD
   - Just noting down the brand of the board for reference.
   
3. **Orange Box 3**: IP Address: 192.168.0.0/22
   - Another IP address, similar to the previous one but in a different network.
   
4. **Green Box 4**: Number: 0
   - This number will help us understand the starting point of our subnetting.
   
5. **Purple Box 5**: Number: 30
   - This number represents the number of hosts we can have in a /30 subnet.
   
6. **Pink Box 6**: Letter: E
   - Just a placeholder for now.
   
7. **Brown Box 7**: Slash: /30
   - This indicates a /30 subnet mask, which allows for 4 hosts.
   
8. **Teal Box 8**: Number: 8
   - This number will be used later to calculate the number of subnets.
   
9. **Olive Box 9**: Formula: 2 -> /30 32 - 2 = 30
   - This formula calculates the number of hosts in a /30 subnet. 32 (total bits) - 2 (network and broadcast bits) = 30 hosts.
   
10. **Navy Box 10**: Text: 3 value
    - This refers to the number of subnets we can create with a /30 mask.

The lecturer said: "Okay guys, so now you will see how to determine the network and host addresses from the VLSM table, and we will also draw the VLSM tree."

### Background (not said in the lecture) (lecture e bola hoy ni)
In VLSM, we can allocate subnets of different sizes based on the number of hosts required. This allows for more efficient use of IP addresses. For example, if you need a small subnet with only a few hosts, you can use a /30 mask, which provides 4 usable IP addresses. If you need a larger subnet, you can use a /24 mask, which provides 254 usable IP addresses. By using VLSM, we can avoid wasting IP addresses and make better use of the available network space.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f 5=#7b2cbf -->
## VLSM: Variable Length Subnet Mask
**In one line:** So amra er broadcast address ta jodpor ber kori broadcast address ba, right.

![Board 2: 0:50-3:30](figures_annotated/board_era2_050.jpg)

*Figure 2. The whiteboard during 0:50–3:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 IP Address · 2 IP Address · 3 VLSM · 4 Math · 5 Networks


1. **Red Box 1 (IP Address: 192.0.0/22)**: This is our initial network address.
2. **Blue Box 2 (IP Address: 192.168.0.1)**: We are considering an IP address within this network.
3. **Orange Box 3 (VLSM: VLSM)**: Variable Length Subnet Mask allows us to allocate subnets of different sizes.
4. **Green Box 4 (Math)**: We will perform some mathematical operations to understand subnetting better.
5. **Purple Box 5 (Networks: Networks Req.Addrs.)**: This table lists the required addresses for different networks.

| Networks | Req.Addrs. | 2^h | Host | Prefix | Subnet | 3rd Octet, 2 Val | 4th Octet, 128 Val |
|----------|------------|-----|------|--------|-------|------------------|--------------------|
| A        | 503        | 512 | 9    | /23    | 11    | 1 Val            | 128 Val            |
| B        | 253        | 256 | 8    | /24    | 11    | 1 Val            | 128 Val            |
| C        | 102        | 128 | 7    | /25    | 11    | 128 Val          | 128 Val            |
| D        | 9          | 7   | 2    | /30    | 11    | 4 Val            | 4 Val              |
| E        | 5          | 4   | 2    | /30    | 11    | 4 Val            | 4 Val              |
| F        | 9          | 4   | 2    | /30    | 11    | 4 Val            | 4 Val              |
| 32-2=30  |            |     |      |        |       |                  |                    |

**Explanation:**
- **Step 1:** The lecturer said: "so amra er broadcast address ta jodpor ber kori broadcast address ba, right."
- **Step 2:** The lecturer said: "ekhon eita pacchi eita same e thakbe, ekta miranom bui, sorry mami state eita bole kortesi ajkal, ekta archorti. ar eikhhan theke choi ta er tar samra 0 dicchi, right? char pacchoi. ar duita address baake teke shei duita hbe 1. ar eikhhan theke shobgula hbe 1. shobgula 1 hole toh amra jaani chodi art ta beiti 1 or ishtetache 2.55 e, june ami beta bhine likhlam right?"
- **Step 3:** The lecturer said: "So amra ekta address kore kori, eita ami kintu begeye ekhon dekhachi, prottek bari kore bege dekhbo right. because jeta ekhon beginner level ami ektu just conversion gula bege dekhano trikortesi. so amra ekhane aa broadcast address pacchi, eksho birer ondoy extra shorti, ten dot dot dot."
- **Step 4:** The lecturer said: "So basically amoddhe ne pura network ta, basically ei jotu bile value orbe shob ei duita moddhe kintu thakbe. ei duita range er moddhe ar baire ki le buzhte beje, mehre koto bhul kese apne. right, shokki chi ei duita range er moddhe thakbe."
- **Step 5:** The lecturer said: "Eiju ta jeta likhe dekhan for sale video, jodi koror deki ei glor moddhe kom o ta value ei range er bair echeo likhase, then amader mrd e mrd ta in kare, right. toh prothom ta jonno amar ber kori, prothom ta amr toh just ei je, eita amr je net rock address hoy, er je next beat, eita theke amra shuru korte abo, right."

<!-- boxes: 1=#d62828 -->
## VLSM Math: VL5M
**In one line:** We will now look at an example of VLSM math using the subnet mask 192.168.0.0/22.

![Board 3: 3:40-4:40](figures_annotated/board_era3_340.jpg)

*Figure 3. The whiteboard during 3:40–4:40, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 VLSM Math


1. **Red Box 1 (VL5M Math):** The first step is to understand the math behind VLSM. We start with the network address 192.168.0.0/22. This means the prefix length is 22, leaving us with 10 host bits.

2. **Step 2:** We need to calculate the number of required addresses. The formula is 2^h - 2, where h is the number of host bits. For 10 host bits, 2^{10} - 2 = 1022 addresses are available. However, we typically subtract 2 to account for the network and broadcast addresses, leaving us with 1020 usable addresses.

3. **Step 3:** Next, we determine the starting and ending network addresses. The starting network address (S.R.) is 192.168.0.0, and the ending network address (E.R.) is 192.168.3.255. This is because the third octet can range from 0 to 3, and the fourth octet can range from 0 to 255.

4. **Step 4:** We then allocate subnets based on the required number of hosts. For example, if we need 503 to 512 hosts, we would use a /24 subnet, which provides 256 addresses. Similarly, for 253 to 256 hosts, another /24 subnet is used, providing 256 addresses. For 102 to 128 hosts, a /25 subnet is used, providing 128 addresses. For 9 to 9 hosts, a /30 subnet is used, providing 4 addresses.

5. **Step 5:** Finally, we verify the calculations. For instance, for a /30 subnet, the calculation is 32 - 2 = 30, meaning we have 2 usable addresses.


### Background (not said in the lecture)
When allocating subnets, it's crucial to ensure that the number of addresses in each subnet meets the requirements. This helps in efficient use of IP addresses and reduces waste. Understanding the math behind VLSM allows network administrators to plan and implement scalable network designs effectively.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 4=#2a9d4f -->
## VLSM
**One Line:** VLSM stands for Variable Length Subnet Masking, which allows us to allocate subnets of different sizes within a larger network.

![Board 4: 4:50-6:50](figures_annotated/board_era4_450.jpg)

*Figure 4. The whiteboard during 4:50–6:50, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Title · 2 Formula · 3 Formula · 4 Formula


1. **Red Box (Box 1):** VLSM
2. **Blue Box (Box 2):** Formula: \sqrt{192.168.0.1}
3. **Orange Box (Box 3):** Formula: F -> 9
4. **Green Box (Box 4):** Formula: F -> 9

The board shows a table with network details and calculations for subnetting. Let's break down the steps:

1. **Network Details:**
   - The network is given as `192.168.0.0/22`.
   - We need to determine how many hosts can be accommodated in each subnet.

2. **Subnet Requirements:**
   - Network A requires 503 addresses.
   - Network B requires 253 addresses.
   - Network C requires 102 addresses.
   - Network D requires 9 addresses.
   - Network E requires 5 addresses.
   - Network F requires 9 addresses.

3. **Calculations:**
   - The formula 2^h is used to find the number of hosts in a subnet.
   - For example, for Network A, 2^9 = 512 addresses, but we need to subtract 2 for the network and broadcast addresses, leaving 503 usable addresses.

4. **Prefix Calculation:**
   - The prefix length is determined based on the required number of addresses.
   - For Network A, the prefix length is `/23` because 2^{23-22} = 2^1 = 2 addresses are left after accounting for the network and broadcast addresses.
   - Similarly, for Network B, the prefix length is `/24` because 2^{24-22} = 2^2 = 4 addresses are left.
   - For Network C, the prefix length is `/24` because 2^{24-22} = 2^2 = 4 addresses are left.
   - For Network D, the prefix length is `/25` because 2^{25-22} = 2^3 = 8 addresses are left.
   - For Network E, the prefix length is `/25` because 2^{25-22} = 2^3 = 8 addresses are left.
   - For Network F, the prefix length is `/25` because 2^{25-22} = 2^3 = 8 addresses are left.

5. **Third Octet Calculation:**
   - The third octet is calculated based on the prefix length.
   - For example, for Network A, the third octet is `130` because the prefix length is `/23`, and the third octet is `130`.

6. **Fourth Octet Calculation:**
   - The fourth octet is calculated based on the prefix length.
   - For example, for Network A, the fourth octet is `255` because the prefix length is `/23`, and the fourth octet is `255`.

7. **Prefixes:**
   - The prefixes for the networks are:
     - Network A: `192.168.3.0/23`
     - Network B: `192.168.4.0/24`
     - Network C: `192.168.4.0/24`
     - Network D: `192.168.5.0/25`
     - Network E: `192.168.5.0/25`
     - Network F: `192.168.5.0/25`

**Remember:** The key points are to understand the calculation of the prefix length based on the required number of addresses, and to correctly determine the third and fourth octets for each network.

<!-- boxes: 1=#d62828 -->
## VLSM Math: VL5M MATH
**In one line:** So, let's clean up the calculations and ensure we understand the process.

![Board 5: 7:00-8:48](figures_annotated/board_era5_700.jpg)

*Figure 5. The whiteboard during 7:00–8:48, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 VLSM Math


The board shows us the VLSM math for different subnets. Each row represents a subnet with its network address, required addresses, number of hosts, prefix length, and the corresponding IP address.

1. **Networks and Required Addresses**: The first column lists the network addresses, and the second column shows the required addresses. For example, the network `192.168.0.0/22` requires `192.168.0.1`.
   
2. **Number of Hosts and Prefix Length**: The third column indicates the number of hosts, and the fourth column shows the prefix length. For instance, `/23` means there are 512 possible host addresses.
   
3. **Third Octet and Values**: The fifth column specifies the third octet and the number of valid values. For example, `192.168.0.1` indicates the first usable IP address in the subnet.
   
4. **Fourth Octet and Values**: The sixth column details the fourth octet and the number of valid values. For example, `192.168.3.1` shows the first usable IP address in another subnet.
   
5. **Subnet Calculation**: The seventh column provides the subnet mask in binary form and the number of available IP addresses. For example, `/24` with `11^h, 1 val` means the subnet mask is `255.255.255.0` and there is one valid IP address.
   
6. **Specific Subnets**: 
   - **Subnet A**: Network `192.168.0.0/23`, required address `192.168.0.1`, 512 hosts, first usable IP `192.168.0.1`.
   - **Subnet B**: Network `192.168.0.0/23`, required address `192.168.0.1`, 256 hosts, first usable IP `192.168.2.1`.
   - **Subnet C**: Network `192.168.0.0/24`, required address `192.168.0.1`, 128 hosts, first usable IP `192.168.3.1`.
   - **Subnet D**: Network `192.168.0.0/25`, required address `192.168.0.1`, 64 hosts, first usable IP `192.168.3.129`.
   - **Subnet E**: Network `192.168.0.0/30`, required address `192.168.0.1`, 4 hosts, first usable IP `192.168.3.133`.
   - **Subnet F**: Network `192.168.0.0/30`, required address `192.168.0.1`, 4 hosts, first usable IP `192.168.3.137`.

The lecturer said: "so, clean ar esha te noyer char, eksho, both eri, tiri, sorry. calculation mistake korre tase ashlar guys onek."

The lecturer mentioned that there were some calculation mistakes, but we need to correct them to ensure accuracy.

The lecturer said: "toh amra jo dia abar eifer jono ber korrte chai, eifer jono ber korlo same bhabe tomar hocche just charge o kore dao."

We need to re-calculate and ensure that the values are correct by simply charging the correct values.

The lecturer said: "ar er porr tao jodi ber kori, porr ta ber korle ei je mane eita toh kono net rock ne abr tar poro range er shabore julo amad eita lagbe. eta amra ber kore rakhi."

If we calculate correctly, we will find that the network will not overlap with other ranges, ensuring proper allocation.

The lecturer said: "so eita hocche amra ekta value saa, eta je value ta chile eta shathe charge o kore eita payachi."

So, we need to ensure that the value we choose is correct and charge it accordingly.

### Background (not said in the lecture) (lecture e bola hoy ni)
Understanding VLSM involves calculating the correct subnet masks and ensuring that the subnets do not overlap. This helps in efficient IP address allocation and reduces waste. By following these steps, we can manage IP addresses more effectively in large networks.

---

## Check yourself
1. What is the formula used to calculate the number of usable IP addresses in a subnet?
2. How many usable IP addresses does a /24 subnet provide?
3. What is the prefix length for a /30 subnet?
4. What is the third octet for the network `192.168.0.0/23`?
5. What is the fourth octet for the network `192.168.0.0/25`?

### Answers
1. The formula used to calculate the number of usable IP addresses in a subnet is \(2^h - 2\).
2. A /24 subnet provides 254 usable IP addresses.
3. The prefix length for a /30 subnet is 30.
4. The third octet for the network `192.168.0.0/23` is 0.
5. The fourth octet for the network `192.168.0.0/25` is 129.

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. These notes were written in Banglish from the board and the transcript, then translated into English by the same model. The lecturer's words are given in English translation (0 quotes); the Banglish version of these notes has the originals, checked word for word against the transcript. References to boxes that do not exist: 0.*
