from source.mission.mission_template import *
from source.mission.cvars import *


class Mission(MissionExecutor):
    def __init__(self, is_CFCF=False, is_TMCF=False, is_PUO=False, is_CCT=False):
        super().__init__(is_CFCF, is_TMCF, is_PUO, is_CCT)

    def move_straight(self, position, is_tp=False, is_precise_arrival=None, stop_rule=None):
        """像目的地行驶。

        Args:
            position (list): 目的地坐标。天理坐标格式。
            is_tp (bool, optional): 是否tp. Defaults to False.
            is_precise_arrival (_type_, optional): 是否精确到达目的地(误差小于1m). Defaults to None.
            stop_rule (_type_, optional): 停止条件.可选STOP_RULE_ARRIVE(到达后停止)或STOP_RULE_F(在目的地附近看到f后停止)。 Defaults to None.

        Returns:
            _type_: _description_
        """
        return super().move_straight(position, is_tp, is_precise_arrival, stop_rule)
    
    def move_along(self, path, is_tp=None, is_precise_arrival=None):
        """沿着TLPP行走。

        Args:
            path (dict): TLPP格式字典。
            is_tp (bool, optional): 是否传送. Defaults to None.
            is_precise_arrival (bool, optional): 是否精确到达目的地(误差小于1m). Defaults to None.

        Returns:
            _type_: _description_
        """
        return super().move_along(path, is_tp, is_precise_arrival)
    
    def start_combat(self, mode="Normal"):
        """开始战斗。

        Args:
            mode (str, optional): 战斗模式.可填Normal(普通战斗模式)或Shield(只开护盾模式)。 Defaults to "Normal".

        Returns:
            _type_: _description_
        """
        return super().start_combat(mode)
    
    def stop_combat(self):
        """停止战斗。

        Returns:
            _type_: _description_
        """
        return super().stop_combat()
    
    def pickup_once(self):
        """拾取1次。

        Returns:
            _type_: _description_
        """
        return super().pickup_once()
    
    def collect(self, MODE=None, collection_name=None, collector_type=None, is_combat=None, is_activate_pickup=None, pickup_points=None):
        """启动收集。

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

        Args:
            center_posi (_type_): 中心坐标
            stop_rule (str, optional): 停止条件。可选F或Combat。 Defaults to 'F'.

        Returns:
            _type_: _description_
        """
        return super().circle_search(center_posi, stop_rule)
    
    def start_pickup(self):
        """启动自动采集。会采集路上遇到的可交互物品。

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
        """注册事件：检测是否遇敌。如果遇敌则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super()._reg_exception_found_enemy(state)
    
    def reg_exception_chara_died(self, state=True):
        """注册事件：检测角色是否死亡。成立则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_exception_chara_died(state)
    
    def reg_exception_low_hp(self, state=True):
        """注册事件：检测角色是否低血量。成立则跳出阻塞式任务。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_exception_low_hp(state)
    
    def reg_default_arrival_mode(self, state=True):
        """注册事件：设置默认的 精确到达模式 。设置为state。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_default_arrival_mode(state)
    
    def reg_fight_if_needed(self, state=True):
        """注册事件：设置是否遇敌即战。设置为state。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_fight_if_needed(state)
    
    def reg_raise_exception(self, state=True):
        """注册事件：设置是否遇到异常时抛出异常并强制退出任务。设置为state。

        Args:
            state (bool, optional): 是否激活. Defaults to True.

        Returns:
            _type_: _description_
        """
        return super().reg_raise_exception(state)
    
    def set_exception_mode(self, mode):
        return super().set_exception_mode(mode)
    
    def tmf_handle_stuck_then_skip(self, k) -> bool:
        """传入TMF的错误码，如果出错则跳过。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super().tmf_handle_stuck_then_skip(k)
    
    def tmf_handle_stuck_then_recover(self, k) -> bool:
        """传入TMF的错误码，如果出错则到七天神像回血。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super()._tmf_handle_stuck_then_recover(k)
    
    def tmf_handle_stuck_then_raise(self, k) -> bool:
        """传入TMF的错误码，如果出错则抛出异常，退出任务。

        Args:
            k (_type_): 错误码。

        Returns:
            bool: _description_
        """
        return super().tmf_handle_stuck_then_raise(k)
    
    def col_handle_timeout_then_recover(self, k) -> bool:
        return super().col_handle_timeout_then_recover(k)
    
    def switch_character_to(self, name: str):
        """切换角色到指定角色。角色名应该为英文。

        Args:
            name (str): 角色名。需要是英文。

        Returns:
            _type_: _description_
        """
        return super().switch_character_to(name)