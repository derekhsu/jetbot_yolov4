- 策略
> -
- 模型
>
- 控制
> - 設定

```
from jetbot import Robot
import time

```

> - 控制動作 / 方向

```
robot = Robot()
robot.forward(0.3)      # 前進 單位？ 範圍? 待確認
robot.stop()            # 停止
time.sleep(0.5)         # 暫停 - 單位：秒
```