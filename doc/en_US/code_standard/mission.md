# Mission

## Introduction

mission is a common template executed in Genshin Teyvat world , including auto collect, auto commission and auto request, etc.

## Usage

## Inherited from the MissionExecutor class.

## Methods

MissionExecutor has the following methods:

1.  move(MODE:str = None,
    stop_rule:int = None,
    target_posi:list = None,
    path_dict:dict = None,
    to_next_posi_offset:float = None,
    special_keys_posi_offset:float = None,
    reaction_to_enemy:str = None,
    is_tp:bool=None)

MODE: 移动模式。有以下两种：

AUTO：朝着target_posi直线行走。
PATH：按照TeyvatMovePath行走。

默认为AUTO。

stop_rule：停止条件。有以下两种：

0：到达目标停止。
1：识别到F停止。

默认为0。

target_posi：目标坐标。使用AUTO模式时填写。按照TIanLi坐标格式。

path_dict：TeyvatMovePath格式文件。使用PATH模式时传入。

is_tp：是否在移动前传送。默认为False。

其他参数为offset或待实现参数。

2. move_straight(self, position, is_tp = False)

position同target_posi。简化版的move。

3. move_along(self, path, is_tp = False)

path：填写TMP格式文件。仅需填写文件名，不用后缀。

4. combat()

打一架。打完就润。

5. collect(self, MODE = None,
                collection_name =  None,
                collector_type =  None,
                is_combat =  None,
                is_activate_pickup = None,
                pickup_points = None
                )

MODE：没什么用。

collection_name: 采集物名称。可留空。

collector_type: 采集物类型。可留空。默认为COLLECTION。

is_combat: 是否战斗。

is_activate_pickup: 是否主动采集。

pickup_points: 是否在指定坐标拾取。若是，则填入坐标，否则留空。

该方法的执行顺序为：战斗->在指定坐标采集->在范围内搜索采集。若在任意阶段搜索到敌人，则会重新进入战斗状态。指定坐标采集不会重复。

6. start_pickup()

开始识别并采集。调用该方法后，会在之后的过程中使用pickup_operator自动识别F键采集。

7. stop_pickup()

停止识别并采集。


## 写一个Mission

首先，继承MissionExecutor。

```python
from source.mission.mission_template import MissionExecutor

class MissionTest(MissionExecutor):
    def __init__(self):
        super().__init__()
        self.setName("MissionTest")
```
注意，类名和文件名必须相同。使用开头大写命名格式。

然后，实现exec_mission方法。

```python
    def exec_mission(self):
        self.move_along("167858534153", is_tp=True)
        self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
```

这是一个示例。

最后，如果你要调试你的mission，在下方加入以下代码：

```python
if __name__ == '__main__':
    mission = MissionTest()
    mission.start()
    mission.continue_threading()
```

运行该文件即可。

## 添加你的Mission

运行mission/index_generator.py。

