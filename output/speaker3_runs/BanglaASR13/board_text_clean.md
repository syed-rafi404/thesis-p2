# Board transcription (clean)

## Board 0:00-3:50

```
MTU
Maximum transmission unit -> Packet Size

DF -> 0

* Total packet size -> 1. Header Sec.
2. Data Sec.

1500
```

```

## Board 4:00-12:34

```
MTU
Maximum transmission
unit -> Packet Size

Data size -> 4000B
-> 1480

DF -> 0
+ Total packet size -> 1. Header sec.
2. Data sec.

F = 0; MF = 1 -> 0
1479 -> Frag 1
1480 - 2959 -> Frag-2
1480 + 20

F = 0; MF = 1 -> 1480
2960 -> Frag-3
4000 -> Frag-4

F = 0; MF = 0 -> 2960
4000 -> Frag-5

For the
Frag + frag -> 0/8 -> 0 -> fragment offset
=> ceil -> 12.7 -> 3

and -> 1480 -> 185 -> u
""

3rd -> 2960 -> 370 -> " for 3rd
frag.
```
