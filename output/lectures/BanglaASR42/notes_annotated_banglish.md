# BanglaASR42: Network Layer Functions
Ei lecture e ki cover kora hoyeche network layer functions, ekhon network layer er key takeaways, and forwarding.

## Key takeaways
- Network layer functions include IP packet switching, routing, and forwarding.
- Routers handle inter-network communication, while switches manage intra-network traffic.
- Routing involves setting up a data graph nature, being a stateless protocol, and packet forwarding.
- Routing algorithms like static and dynamic routing play a critical role in determining the path of data packets.
- Forwarding involves using the routing table to send data packets along the determined path.

<!-- boxes: 1=#d62828 2=#1d4ed8 -->
## Network Layer Functions
**Ek line e:** Network layer functions are one of the most complicated chapters in network layer.

![Board 1: 0:00-4:32](figures_annotated/board_era1_000.jpg)

*Figure 1. The whiteboard during 0:00–4:32, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network layer Functions · 2 Link layer


1. **Red Box 1 (Network layer Functions):** The lecturer starts by explaining that we will cover IP bar functions in this chapter, which is one of the most complex topics in the network layer.
2. **Blue Box 2 (Link layer):** The lecturer mentions that we will discuss network layer functions, including devices like routers and switches, and their roles in the network hierarchy.
3. **Network Layer Device Roles:** The lecturer explains that network layer devices include routers, which operate at level three, and switches, which operate at level two. Routers handle packets between different networks, while switches do not because they operate at a lower level.
4. **Network Communication:** The lecturer emphasizes that when moving from one network to another, only routers can provide the necessary information, whereas switches cannot because they operate at a lower level.
5. **Example of Network Communication:** The lecturer gives an example where a user follows a similar procedure from the application layer (like using Gmail or a web browser) to the transport layer, adding headers to the data, and then to the network layer where the packet is formed.
6. **Packet Delivery:** The lecturer explains that the network layer packet delivery object (PDO) is essentially a packet, and this concept is fundamental to understanding network layer functions.

> 
> Lecturer: "so router ta ekta onno network theya pahono packet er moddhe ki information ache net rock layer er te shegula dekhte pabe."

### Extra jana kotha
Understanding the roles of different network layer devices like routers and switches is crucial. Routers handle inter-network communication, while switches manage intra-network traffic. This distinction helps in designing efficient network architectures.

<!-- boxes:  -->
## Network Layer Functions

**Ek line e:** In this section, we will discuss the encapsulation process in the transport layer and how it relates to the network layer.

![Board 2: 4:50-5:24](figures_annotated/board_era2_450.jpg)

*Figure 2. The whiteboard during 4:50–5:24, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*




The lecturer explained that in the transport layer, packets are encapsulated with headers to facilitate their transfer. This encapsulation is a fundamental process. He further clarified that after this encapsulation, the packets are passed to the next layer, which is the network layer. 

In the network layer, the packets undergo another encapsulation process. The lecturer mentioned, "so basically oi jinish tai hoy, pothom amar der hocche in tari later layer er ekta boishi shoy tese ncapsulation, ma function bolte parer ncap likhlam, ncapsulation osche pothoma ekta fundamental boishi shoto." This means, "basically, this is the end, then comes the next layer where another encapsulation happens, I call it encapsulation, which is a fundamental process."

The network layer inspects the data from the network layer and checks the IP addresses. The lecturer stated, "then amr direktta juni phone e rakhte be, ekhane route ar ta shudhu matro kintu net rock layer er data gula jegula ashe shegula inspect korte pare. onno net rock theke asha, your ip address ki den hocche." This means, "then directly to the network layer, here routing and other network layer data can be inspected, and your IP address is checked."

### Extra jana kotha (lecture e bola hoy ni)
In the network layer, the main task is to ensure that the packets reach the correct destination using IP addresses. The network layer also handles routing, which involves deciding the best path for the packets to travel through the network. Understanding these processes is crucial for effective communication in computer networks.

<!-- boxes: 1=#d62828 -->
## Network Layer Functions
**Ek line e:** Network layer functions include package switching, where a packet travels from one device to another.

![Board 3: 5:30-9:08](figures_annotated/board_era3_530.jpg)

*Figure 3. The whiteboard during 5:30–9:08, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network layer Functions


The board shows the following key points:

1. **Box 1 (Red)**: Network layer functions include package switching. This involves a packet traveling from one device to another. The board lists two types of network: Datagram Network and Virtual Circuit Network (VCN).

2. **Datagram Network**: The lecturer explains that a Datagram Network is a type of network where each packet contains all the necessary information to reach its destination independently. This means that each packet can take a different path through the network.

3. **Virtual Circuit Network (VCN)**: The lecturer mentions that a Virtual Circuit Network is a variation of Datagram Network. It is also known as a Virtual Private Network (VPN). The lecturer clarifies that both VCN and VPN refer to the same concept.

4. **Example**: To illustrate, the lecturer gives an example of a packet traveling through multiple routers. When a packet arrives at a router, it checks if the path to the destination is valid before sending the packet along the chosen path. This process is repeated until the packet reaches its destination.

5. **Advantages and Disadvantages**: Using a Virtual Circuit Network (VCN) offers some advantages, such as security, but it can also make the network slower because packets follow a fixed path, which can lead to congestion.

6. **Use Case**: VCNs are typically used in organizations for secure communication. They allow for end-to-end encryption, ensuring that data is transmitted securely between two users.

7. **Comparison**: While VCNs offer better security, they are generally slower than Datagram Networks. The lecturer moves on to discuss more features of Datagram Networks.

**Mone rakho:** Network layer functions involve package switching, where each packet in a Datagram Network contains all necessary information to reach its destination independently. Virtual Circuit Networks (VCNs) or Virtual Private Networks (VPNs) are variations of Datagram Networks, offering enhanced security but potentially slower performance due to fixed paths.

<!-- boxes: 1=#d62828 -->
## Network Layer Functions
**Ek line e:** Routing -> Level -3 device

![Board 4: 9:10-12:30](figures_annotated/board_era4_910.jpg)

*Figure 4. The whiteboard during 9:10–12:30, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network layer Functions


The red box 1 on the board lists the network layer functions, specifically mentioning routing as a level -3 device. Routing is a crucial function in the network layer, responsible for directing data packets to their correct destination.

1. **Data Graph Nature**: The lecturer explains that the first aspect of routing is setting up a data graph nature. This means establishing a framework for data transfer without setting up a call. Essentially, it involves configuring the network to handle data transmission efficiently.

2. **Stateless Protocol**: The second key feature of routing is the stateless protocol. A stateless protocol means that the router does not maintain any state information about the packets it forwards. It simply receives a packet, checks its destination address, and forwards it to the appropriate next hop. The router does not keep track of which packets have been sent or received, making it simpler and more scalable.

3. **Packet Forwarding**: The third aspect is packet forwarding. Packet forwarding allows packets to take different paths through the network. While this can make the system faster, it also introduces potential security risks because the router does not keep track of the entire path taken by each packet.

4. **Stateful vs Stateless**: The lecturer emphasizes the difference between stateless and stateful protocols. Stateful protocols maintain state information about the packets they forward, which can provide better security but at the cost of complexity. Stateless protocols, on the other hand, do not maintain such state information, making them simpler to implement.

5. **Error Checking and Privacy**: The lecturer mentions that while stateless protocols do not maintain state information, they still perform error checking. This ensures that packets are transmitted correctly, but it also means that there is less focus on privacy. In contrast, stateful protocols might provide better privacy but at the expense of additional complexity.

6. **Routing Algorithm**: The final point on the board discusses routing algorithms. These are the methods used by routers to determine the best path for data packets. Routers can follow different routing algorithms, such as static routing, dynamic routing (like OSPF or BGP), or even protocols like DHCP. Each algorithm has its own advantages and disadvantages, and choosing the right one depends on the specific requirements of the network.


### Extra jana kotha
Routing algorithms play a critical role in determining the path of data packets. Static routing is simple and predictable, but it requires manual configuration. Dynamic routing protocols like OSPF and BGP are more complex but adapt to changes in the network topology. Understanding these differences helps in designing efficient and secure network architectures.

<!-- boxes: 1=#d62828 2=#1d4ed8 3=#f77f00 -->
## Forwarding
**Ek line e:** Forwarding is a key function in the network layer.

![Board 5: 12:40-13:44](figures_annotated/board_era5_1240.jpg)

*Figure 5. The whiteboard during 12:40–13:44, reconstructed with the lecturer removed; background whitened for readability (the writing is the camera's own pixels). Boxes found from the ink; names by Qwen/Qwen2.5-VL-7B-Instruct.*

**Boxes:** 1 Network Layer Functions · 2 Routing Algorithm · 3 Forwarding


- **Red Box 1 (Network Layer Functions):** This board introduces the network layer functions, which include routing and forwarding.
- **Blue Box 2 (Routing Algorithm):** The first sub-function is routing, which is performed at level -3 devices.
- **Orange Box 3 (Forwarding):** The second sub-function is forwarding. Let's understand what forwarding means. Forwarding involves two major tasks: one is routing, and the other is actually forwarding based on the routing table.

The routing table is used to determine the best path for data packets to travel from one network to another. For example, if data needs to be sent from one network to another, the routing process decides the path, and the forwarding process implements it by sending the packet along that path.

> Lecturer: "ekta hoche gelo routing, ekta je forwarding."

In our upcoming class, we will delve into the details of IPv forwarding and see the structure of the header. We will also discuss how data packets are forwarded based on the routing table.

**Mone rakho:** Routing and forwarding are the two major functions in the network layer. Routing determines the path, and forwarding sends the data packets along that path using the routing table.

---

## Check yourself
1. What are the two major functions in the network layer?
2. Explain the difference between a router and a switch.
3. What is the purpose of a routing table in the network layer?
4. Describe the process of packet forwarding.
5. Name two types of routing algorithms discussed in the lecture.

### Answers
1. The two major functions in the network layer are routing and forwarding.
2. Routers handle inter-network communication, while switches manage intra-network traffic.
3. The purpose of a routing table in the network layer is to determine the best path for data packets to travel from one network to another.
4. Packet forwarding involves using the routing table to send data packets along the determined path.
5. Two types of routing algorithms discussed in the lecture are static routing and dynamic routing (like OSPF or BGP).

---


*How these notes were made. Speech: transcript.txt. Boards: ink boxes, named by Qwen/Qwen2.5-VL-7B-Instruct. Notes written by Qwen/Qwen2.5-7B-Instruct. Quotes checked word for word against the transcript: 2 kept, 2 removed. References to boxes that do not exist: 0.*
