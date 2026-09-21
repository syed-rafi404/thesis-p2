# Board transcription (frame)

## Board 0:00-3:50

```
MTU
Maximum transmission
unit -> Packet Size

DF -> 0

* Total packet size -> 1. Header Sec.
2. Data Sec.

1500
```

```

## Board 4:00-12:30

| Maximum transmission unit → Packet Size |
| --- | --- |
| Data size → 1000B | DF → 0 |
| 1480 | * Total packet size → 1. Header sec. |
| 1500 → MTU | 2. Data sec. |
| F=0; MF=1 → 0 - 1479 → Frag 1 | Header + Data |
| F=0; MF=1 → 1480 - 2959 → Frag-2 | 20B - 60B |
| F=0; MF=0 → 2960 - 4000 → Frag-3 | # fragments → 4000/1480 |
| For the first+frag → 0/8 → 0 → fragment offset | => ceil → √2.7 → 3 |
| 2nd → 1480/8 → 185 → " | " |
| 3rd → 2960/8 → 370 → " | " |
| " for 3rd frag. |
