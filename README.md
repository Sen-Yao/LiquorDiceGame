# LiquorDiceGame
这是一个在酒桌上常见的骰子游戏。本程序用 Python 实现此游戏。

## 规则描述

### 基本规则

此游戏玩家为 2 名及以上，所有玩家绕桌子围成一圈。按逆时针进行游戏。每位玩家有五颗骰子。上一局输掉的玩家作为本局游戏的第一个玩家。若是第一局游戏，则随机选择一位玩家来作为本局游戏的第一个玩家。

每局游戏开始时，每位玩家掷自己的五颗骰子，骰子结果**仅自己可见**。此时第一位玩家需要做出一次「**猜测**」。**猜测**指的是此玩家根据自己的骰子结果和对场上其他玩家的估计，猜测某个点数在所有玩家的骰子中的和。注意在本游戏中，点数为 1 的骰子可以看成是任意点数。例如 “7 个 4” 是一个猜测，它表示此玩家认为场上所有玩家手里的骰子中，点数为 4 的骰子和点数为 1 的骰子加起来共有 7 个及以上。一般来说，起始的个数应大于当前玩家数。比如对于一局 5 个玩家的游戏，通常第一个猜测应从 6 个 X 及以上开始。

当一位玩家做出一个「**猜测**」后，下一个玩家有两种选择，「**继续猜测**」或是「**开**」。其中，「**继续猜测**」要求此玩家的猜测「**大于**」下一个玩家。这里的「**大于**」可以是猜测的个数更大，也可以是个数持平但点数更大。比如对于猜测 “7 个 4”，有：

- “8 个 4” 是一个合法的猜测
- “7 个 6” 是一个合法的猜测
- “7 个 3” 不是一个合法的猜测

若玩家选择「**开**」，则场上所有玩家展示自己的骰子结果，并且检验上一个猜测是否为真。若猜测为真，则选择**开**的玩家输掉此游戏，反之上一个玩家输掉此游戏。在酒桌上，输掉游戏的玩家通常需要罚酒一杯。

### 进阶规则

#### 斋和飞

玩家在提出「猜测」时，可以在「**斋猜测**」和「**飞猜测**」中进行选择。其中「**斋**」指的是在本次猜测中，不将点数为 1 的骰子计算在内，例如 “7 个 4 斋” 表示此玩家认为场上所有玩家手里的骰子中，真正的点数为 4 的骰子加起来共有 7 个及以上，而不考虑点数为 1 的骰子。与「**斋猜测**」对应，「**飞猜测**」就是采用传统的规则，即重新将点数为 1 的骰子计算在内。在一局游戏中，玩家可以根据场上局势来在**斋**和**飞**中选择最有利于自己的猜测方式。

从概率论的角度来说，“7 个 4 斋” 的可能性或是期望约为 “7 个 4 飞” 的一半。这是因为「**飞猜测**」计算的骰子是点数为 1 和点数为 4 的骰子，而「**斋猜测**」只计算了点数为 4 的骰子。因此规则规定，若上一个玩家喊出的是「**飞猜测**」，若此时的玩家的继续猜测改为「**斋猜测**」，则继续猜测所需要的个数可以是原来的一半，严格来说是除二后向上取整。例如若上一个玩家的猜测为 “7 个 4 飞”，则此玩家的斋猜测只需要从 $7/2=3.5$ 向上取整，即 4 个开始喊，如 "4 个 3 斋” 就是一个合法猜测。

与之对应的，如果上一个玩家喊出的是「**斋猜测**」，若此时的玩家的继续猜测改为「**飞猜测**」，则点数需要在原来的基础上乘二。例如若上一个玩家的猜测为 “7 个 4 斋”，则此玩家的「**飞猜测**」需要从 14 个开始喊，如 "14 个 3 飞” 就是一个合法猜测。

#### 喊 1

由于点数为 1 的骰子可以看成是任意点数，因此如果玩家喊的猜测为“X 个 1”，此时相当于只计算点数为 1 的骰子，这从某种意义上来说就是一种「**斋猜测**」。因此它的继续猜测规则等同于「**斋猜测**」，即：如果从上一个玩家的常规的「**飞猜测**」改为喊 1，则此时继续猜测所需要的个数是原来的除二后向上取整；如果从上一个玩家喊 1，而此时的玩家改为猜测其他点数的「**飞猜测**」，则继续猜测所需要的个数是原来的两倍。

#### 跳开

对于三个人及以上的游戏，玩家允许进行「**跳开**」。一般来说，玩家只能**开**上家的猜测，但是「**跳开**」规则允许玩家对场上任何其他玩家的猜测产生质疑时，都可以**开**。此时的输赢惩罚将根据两位玩家的「**顺位距离**」来成倍计算。「**顺位距离**」指的是**提出猜测的人和开的人的逆时针距离**。例如**甲乙丙丁戊己庚辛**八人逆时针就座，根据游戏规则，游戏顺序就是**甲乙丙丁戊己庚辛**。若甲「**跳开**」丙，则甲跳过了「丁戊己庚辛」五个玩家来**开**丙，故名为「**跳开**」。此时两人的「**顺位距离**」为 6，如果甲输了，则需要罚酒 6 杯，反之则丙需要罚酒 6 杯。

