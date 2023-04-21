# TMF TeyvatMoveFlow 提瓦特移动控制流

## 参数

TeyvatMoveController(MODE:str = None,
    stop_rule:int = None,
    target_posi:list = None,
    path_dict:dict = None,
    to_next_posi_offset:float = None,
    special_keys_posi_offset:float = None,
    reaction_to_enemy:str = None,
    is_tp:bool=None,
    precise_arrive:bool=None)

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
precise_arrive: 是否精准抵达（将目标）。默认为False。
其他参数为offset或待实现参数。 

## 工作原理

### AUTO模式

AUTO模式会朝着目标坐标方向直行。在走路状态下每2s按2次空格。

### PATH模式

PATH模式会沿着坐标前进。在循环过程中，执行以下3个步骤：

1. 朝着break position（转折点）前进。距离BP小于规定的offset即切换到下一个BP，直到没有更多BP。
2. 自动识别当前的position，并检测motion和special key并执行。

