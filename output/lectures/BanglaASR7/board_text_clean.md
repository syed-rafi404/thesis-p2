# Board transcription (clean)

## Board 0:00-7:12

| T → B { C.i = B.type & C } T.type = C.type |
| --- | --- |
| x B → int { B.type = int } |
| C → [Num] { C.i = c.i } |
| C → ε { C.type = c.i } |

T.type =
C1.type = array (num.val, C1.type)
int [2][4]
C1.type = array (2, array (4, int))

B1.type = int
[num]
[2]

C1.type = array (2, array (4, int))
C2.type = int

num
[4]
