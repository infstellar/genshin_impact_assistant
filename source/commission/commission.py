from source.commission.commission_template import CommissionTemplate
from source.manager.asset import Text
from source.commission.assets import *
from source.commission.util import *

class Commission(CommissionTemplate):
    """
    每日委托模板类.
    大部分方法与自定义任务一致,添加了对话模块.
    """
    def __init__(self, commission_type:str, commission_position:list, is_CFCF=True, is_PUO=True, is_TMCF=True, is_CCT=False):
        """初始化委托.

        Args:
            commission_type (str): 委托名.英文名.
            commission_position (list): 委托的坐标.天理坐标格式.
        """
        super().__init__(commission_type, commission_position, is_CFCF, is_PUO, is_TMCF, is_CCT)
        
    def talk_skip(self, stop_func=None):
        """跳过对话,直到回到大世界.
        如果有选项,会自动点击最下面的选项.

        Args:
            stop_func (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return super().talk_skip(stop_func)
    
    def talk_switch(self, textobj: Text):
        """选择选项.

        Args:
            textobj (Text): Text类型对象.使用方法: example_text = Text(en="english text", zh="chinese text"). 英语优先,有能力再补充中文.

        Returns:
            _type_: _description_
        """
        return super().talk_switch(textobj)
    
    def talk_until_switch(self):
        """对话直到出现选项.

        Returns:
            _type_: _description_
        """
        return super().talk_until_switch()
    
    def talk_wait(self, x):
        """等待x秒.

        Args:
            x (float): 等待时间,单位为second.

        Returns:
            _type_: _description_
        """
        return super().talk_wait(x)
    
    def talk_with_npc(self, npc_name:Text = None):
        """与指定名称的NPC对话. 会按wasd改变方向来寻找附近的NPC.

        Args:
            npc_name (Text): NPC名称.Text类型对象. 使用方法: example_text = Text(en="english text", zh="chinese text"). 英语优先,有能力再补充中文.

        Returns:
            _type_: _description_
        """
        return super().talk_with_npc(npc_name)
    
    def talk_with_options(self, options: list):
        """我也忘了这个是啥.

        Args:
            options (list): _description_

        Returns:
            _type_: _description_
        """
        return super().talk_with_options(options)
    
    def exit_talk(self) -> bool:
        """退出对话, 直到返回主界面.

        Returns:
            bool: 是否成功.
        """
        return super().exit_talk()
    
    