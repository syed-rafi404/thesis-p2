# Board transcription (clean)

## Board 0:00-17:44

```
Regression Tree

Outlook = {Sunny, Overcast, Rain}

Total SSR (Outlook)
= 12.50 + 0 + 458.00
= 470.50

ΔSSR = 758.83 - 470.50

Number Outlook | Temp | Humidity | Wind | Players
---------------|------|----------|------|--------
1             | Sunny| Hot      | High | Weak  | 25
2             | Sunny| Hot      | High | Strong| 30
3             | Overcast| Hot | High | Weak  | 46
4             | Rain | Mild    | High | Weak  | 45
5             | Rain | Cool    | Normal | Weak | 52
6             | Rain | Cool    | Normal | Strong| 23

SSR(Players) = 758.83
SSR(Outlook = Sunny) = 12.50
SSR(Outlook = Overcast) = 0
SSR(Outlook = Rain) = 458.00
```

## Board 17:50-36:24

```
Regression Tree

| Number | Outlook | Temp | Humidity | Wind | Players |
|--------|---------|------|----------|------|---------|
| 1      | Sunny   | Hot  | High     | weak | 25      |
| 2      | Sunny   | Hot  | High     | Strong| 30      |
| 3      | Overcast| Hot  | High     | weak | 46      |
| 4      | Rain    | Mild | High     | weak | 45      |
| 5      | Rain    | Cool | Normal   | weak | 52      |
| 6      | Rain    | Cool | Normal   | Strong| 23      |

SSR(Players) = 758.83

Weak
Wind
Strong

Outlook
Rain
Outlook
Rain
Sunny
Overcast
Rain
Temp
Mild
Cool
25
46
30
95.0
52.0
```
