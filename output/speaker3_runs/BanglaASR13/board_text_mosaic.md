# Board transcription (mosaic)

## Board 0:00-3:50

```
MTU
Maximum transmission
unit → Pak
DF → 0
* Total packet size → 1. Header sec.
2. Data sec.
Header + Data
→ 20B - 60B
```

## Board 4:00-12:30

| M+U | Maximum transmission |
| --- | --- |
| unit | Packet size |

Data size → 1000B
DF → 0

* Total packet size → 1. Header sec.
2. Data sec.

F = 0; MF = 1 → 0 - 1479 → Frag 1
F = 0; MF = 1 → 1480 - 2959 → Frag-2
F = 0; MF = 0 → 2960 - 4000 → Frag-3

For the
First frag → 0/8 → 0 → fragment offset → ceil → √2.7 → 3

2nd → 1480 → 185 →
3rd → 2960 → 370 →
