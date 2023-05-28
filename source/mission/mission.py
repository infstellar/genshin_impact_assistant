from source.mission.mission_template import MissionExecutor
from source.mission.cvars import *

"""
这里是Mission的标准类.编写你的mission时,请继承该类.

你可以在下面的函数中找到它们的使用方法和介绍. 如果不清晰或想要添加新的功能以适配你的想法,请提交issue.

函数类型介绍:
阻塞式任务: 内置了while循环,在该任务结束或出错前,不会返回.
非阻塞式任务: 一次性执行完成.
持续式任务: 启动后,将会在之后持续生效,直到手动停止.
注册类函数: 名称以reg开头,用于阻塞类任务,当条件成立时执行一定的操作,例如战斗或退出.
设置类函数: 名称以set开头,设置一些功能的开关.
错误处理类函数: 名称以handle开头,任务类函数结束后会返回错误码,可以将其传入此类函数,执行对应的措施.

在source/commission/commissions中,有一些执行每日委托的Mission示例,你可以看看它们.
Commission的编写与Mission基本相同,但在文件命名上会有所不同.你可以在source/commission/commission.py查看介绍.
"""

class Mission(MissionExecutor):
    def __init__(self, is_CFCF=False, is_TMCF=False, is_PUO=False, is_CCT=False):
        """初始化功能.你可以不手动初始化它们,因为MissionExecutor会自动识别并初始化.
        但如果你需要在功能启动前调用它们的变量,请在这里初始化.

        Args:
            is_CFCF (bool, optional): 初始化采集模块. Defaults to False.
            is_TMCF (bool, optional): 初始化移动模块. Defaults to False.
            is_PUO (bool, optional): 初始化拾取模块. Defaults to False.
            is_CCT (bool, optional): 初始化战斗模块. Defaults to False.
        """
        super().__init__(is_CFCF, is_TMCF, is_PUO, is_CCT)

    def move_straight(self, position, is_tp=False, is_precise_arrival=None, stop_rule=None):
        """向目的地前进。
        阻塞式任务.

        Args:
            position (list): 有多个使用方法:
            1. 目的地坐标。天理坐标格式。
            2. [TLPP_DICT, KEYWORD]: 
                TLPP_DICT: TLPP字典.
                KEYWORD:
                    可以是以下参数:
                    "start_position" : TLPP的开始坐标.
                    "end_position" : TLPP的结束坐标.
            这个传入值表示使用TLPP的开始/结束坐标作为目的地坐标. 无需翻字典手动传入.
            
            is_tp (bool, optional): 是否tp. Defaults to False.
            
            is_precise_arrival (_type_, optional): 是否精确到达目的地(误差小于1m). Defaults to None.
            
            stop_rule (_type_, optional): 停止条件.可选STOP_RULE_ARRIVE(到达后停止)或STOP_RULE_F(在目的地附近看到f后停止)。 Defaults to None.

        注: 在某些Mission中,TLPP_DICT可能会是字符串.这是旧版本所使用的存储TLPP文件的方法,现已弃用. 目前所有的TLPP文件与Mission放在同一个py文件中.
        
        Returns:
            _type_: _description_
        """
        return super().move_straight(position, is_tp, is_precise_arrival, stop_rule)
    
    def move_along(self, path, is_tp=None, is_precise_arrival=None):
        """沿着TLPP行走。
        阻塞式任务.

        Args:
            path (dict): TLPP格式字典。
            is_tp (bool, optional): 是否传送. Defaults to None.
            is_precise_arrival (bool, optional): 是否精确到达目的地(误差小于1m). Defaults to None.

        注: 在某些Mission中,path可能会是字符串.这是旧版本所使用的存储TLPP文件的方法,现已弃用. 目前所有的TLPP文件与Mission放在同一个py文件中.
        
        Returns:
            _type_: _description_
        """
        return super().move_along(path, is_tp, is_precise_arrival)
    
    def start_combat(self, mode="Normal"):
        """开始战斗。
        非阻塞式任务.
        持续式任务. 可能需要手动写循环,判断退出条件.

        Args:
            mode (str, optional): 战斗模式.可填Normal(普通战斗模式)或Shield(只开护盾模式)。 Defaults to "Normal".

        Returns:
            _type_: _description_
        """
        return super().start_combat(mode)
    
    def stop_combat(self):
        """停止战斗。
        非阻塞式任务.

        Returns:
            _type_: _description_
        """
        return super().stop_combat()
    
    def pickup_once(self):
        """拾取1次。
        非阻塞式任务.

        Returns:
            _type_: _description_
        """
        return super().pickup_once()
    
    def collect(self, MODE=None, collection_name=None, collector_type=None, is_combat=None, is_activate_pickup=None, pickup_points=None):
        """启动收集。
        阻塞式任务.

        Args:
            MODE (_type_, optional): 采集模式。没有实际意义。 Defaults to None.
            collection_name (_type_, optional): 采集物名称。选填。 Defaults to None.
            collector_type (_type_, optional): 采集物类型。必填。 Defaults to None.
            is_combat (_type_, optional): 是否战斗. Defaults to None.
            is_activate_pickup (_type_, optional): 是否主动采集(启动搜索式采集，搜索附近的采集物). Defaults to None.
            pickup_points (_type_, optional): 采集点坐标。会主动到这些坐标上采集。选填。 Defaults to None.

        Returns:
            _type_: _description_
        """
        return super().collect(MODE, collection_name, collector_type, is_combat, is_activate_pickup, pickup_points)
    
    def circle_search(self, center_posi, stop_rule='F'):
        """进入一个循环，以中心坐标为圆心向外移动搜索。当符合stop_rule时退出。
        阻塞式任务.

        Args:
            center_posi (_type_): 中心坐标
            stop_rule (str, optional): 停止条件。可选F或Combat。 Defaults to 'F'.

        Returns:
            _type_: _description_
        """
        return super().circle_search(center_posi, stop_rule)
    
    def start_pickup(self):
        """启动自动采集。会采集路上遇到的可交互物品。
        非阻塞式任务.
        持续式任务.

        Returns:
            _type_: _description_
        """
        return super().start_pickup()
    
    def stop_pickup(self):
        """停止自动采集。

        Returns:
            _type_: _description_
        """
        return super().stop_pickup()
    
    def refresh_picked_list(self):
        """刷新已采集物名列表。

        Returns:
            _type_: _description_
        """
        return super().refresh_picked_list()    

    def reg_exception_found_enemy(self, state=True):
        """注册事件：条件:是否遇敌。此后条件成立则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super()._reg_exception_found_enemy(state)
    
    def reg_exception_chara_died(self, state=True):
        """注册事件：条件:角色是否死亡。此后条件成立则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_exception_chara_died(state)
    
    def reg_exception_low_hp(self, state=True):
        """注册事件：条件:检测角色是否低血量。此后条件成立则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_exception_low_hp(state)
    
    def set_default_arrival_mode(self, state=True):
        """设置默认精确到达模式。此后所有移动方法的默认精确到达模式设置为state。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().set_default_arrival_mode(state)
    
    def reg_fight_if_needed(self, state=True):
        """注册事件：设置是否遇到可见的敌人就开战。设置为state。
        
        注意: 该函数暂未实现,因此你暂时不能使用它.

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_fight_if_needed(state)
    
    def set_raise_exception(self, state=True):
        """设置是否遇到异常时抛出异常并强制退出任务。设置为state。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().set_raise_exception(state)
    
    def set_exception_mode(self, mode):
        """设置阻塞式任务遇到异常时的默认处理方式.

        Args:
            mode (_type_): 异常处理模式.可选:
            
            EXCEPTION_RECOVER: 发生异常后,前往七天神像回血.
            
            EXCEPTION_SKIP: 发生异常后,什么也不执行,手动使用handle类函数处理异常.
            
            EXCEPTION_RAISE: 发生异常后,提出异常并终止任务.

        Returns:
            _type_: _description_
        """
        return super().set_exception_mode(mode)
    
    def set_puo_crazy_f(self, mode):
        """设置是否启用疯狂按f模式.启用后,puo将会在按下f拾取后不停按f若干次.
        通常用于拾取调查类采集点.

        Args:
            mode (bool): mode. True|False.

        Returns:
            _type_: _description_
        """
        return super().set_puo_crazy_f(mode)
        
    
    def handle_tmf_stuck_then_skip(self, k) -> bool:
        """传入TMF的错误码，如果出错则跳过。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super().handle_tmf_stuck_then_skip(k)
    
    def handle_tmf_stuck_then_recover(self, k) -> bool:
        """传入TMF的错误码，如果出错则到七天神像回血。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super()._tmf_handle_stuck_then_recover(k)
    
    def handle_tmf_stuck_then_raise(self, k) -> bool:
        """传入TMF的错误码，如果出错则抛出异常，退出任务。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super().handle_tmf_stuck_then_raise(k)
    
    def handle_col_timeout_then_recover(self, k) -> bool:
        """注意: 该函数暂未实现,因此你暂时不能使用它.

        Args:
            k (_type_): _description_

        Returns:
            bool: _description_
        """
        return super().handle_col_timeout_then_recover(k)
    
    def switch_character_to(self, name: str):
        """切换角色到指定角色。角色名为英文。

        Args:
            name (str): 角色名。需要是英文。

        Returns:
            _type_: _description_
        """
        return super().switch_character_to(name)
    
    def use_f(self):
        """按一下f.

        Returns:
            _type_: _description_
        """
        return super().use_f()
    
    def is_combat_end(self) -> bool:
        """战斗是否结束.你可以在while循环中判断它.

        Returns:
            bool: _description_
        """
        return super().is_combat_end()