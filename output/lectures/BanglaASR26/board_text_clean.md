# Board transcription (clean)

## Board 0:10-1:50

```
| kP | kI | kD |
|----|----|----|
| xPn | p | pI |
|     |    | pIO |
```

## Board 2:00-4:54

Imagine:
(PID) → kp, ki, ko
Do 4 steps for this problem:

output = kp * error
+ (Σn Error) * ki
+

[illegible]

output = k / ic

## Board 5:00-6:20

Imagine:
(PID) → kP, ki, ko

Do 4 steps for this problem →

output = kP * error
+ (Σn Error) * ki
+ k

[illegible]

output = k
error

## Board 6:30-7:46

Imagine:
(PID) → KP, Ki, KO

Do 4 steps for this problem:

output = KP * error
        + (Σn Err) * Ki
        + (En - E3) * KD = new output

new Actual = [New + old] / 2

## Board 8:10-13:12

Imagine:
(PID) → KP, Ki, KO
Do 4 steps for this problem:

PID
Desired speed → 100 km/h
initial speed → 60 km/h

KP = 0.5 ; Ki = 0.1 , KD = 0.05

Error = (100 - 60) = 40 km/h

1st Step:
out = [0.5 × 40] + 0.1 × 10 + 0.05 × 40
    = out_1

New actual speed = 60 + out_1
