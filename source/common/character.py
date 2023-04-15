from source.manager import posi_manager
from source.interaction.interaction_core import itt
from common.timer_module import Timer
from source.util import *


def default_trigger_func():
    return True

Q_SKILL_COLOR={
    "Geo":[0.1277,0.8392,1], # 岩
    "Electro":[0.75,0.4549,1], # 雷
    "Hydro":[0.5467,0.8824,1], # 水
    "Pyro":[0.0375,0.6275,1], # 火
    "Cryo":[0.5,0.4549,1], # 冰
    "Dendro":[0.2341,0.7757,1], # 草
    "Anemo":[0.447,0.7426,1] # 风
    
}

def log_format(x, name):
    # 格式化输出日志。#
    variable_name_len = 15
    variable_name = name
    variable_content = str(x)
    var_name = variable_name + (variable_name_len - len(variable_name)) * ' ' + '|' # 垃圾实现，以后改 XCYD
    logger.trace(var_name + variable_content)


class Character:
    @logger.catch
    def __init__(self, name='=', position='', n=0, priority=0,
                 E_short_cd_time:float=0, E_long_cd_time:float=0,
                 Elast_time:float=0,
                 tactic_group='', trigger: str = '=',
                 Epress_time:float=0, Qlast_time = 0, Qcd_time = 12,
                 vision:str = '', long_attack_time:float = 2.5):

        self.name = name
        self.position = position
        self.E_short_cd_time = E_short_cd_time
        self.E_long_cd_time = E_long_cd_time
        self.Elast_time = Elast_time
        self.Qlast_time = Qlast_time
        self.Qcd_time = Qcd_time
        self.tactic_group = tactic_group
        self.priority = priority
        self.n = n
        self.Epress_time = Epress_time
        self.vision = vision
        self.long_attack_time = long_attack_time

        self.itt = itt

        if E_long_cd_time != 0:
            self.Ecd_time = E_long_cd_time
        else:
            self.Ecd_time = E_short_cd_time
        self.triggers = trigger
        self.trigger = default_trigger_func
        self.Ecd_timer = Timer(diff_start_time=self.Ecd_time)
        self.Elast_timer = Timer(diff_start_time=Elast_time)
        self.Qlast_timer = Timer(diff_start_time=Qlast_time)
        
        self.position_tactic = self._get_position_tactic()

        
        # self._init_log()
        self.trigger_list = []
        self._trigger_analyses()

    def _get_position_tactic(self):
        if self.position == "Shield":
            return "e?e~:none;"
        elif self.position == "Core":
            return "a,a"
    
    def _init_log(self):
        logger.debug('---- character info ----')
        log_format(self.name, 'name')
        log_format(self.position, 'position')
        log_format(self.E_short_cd_time, 'E_short_cd_time')
        log_format(self.E_long_cd_time, 'E_long_cd_time')
        log_format(self.Elast_time, 'Elast_time')
        log_format(self.Qlast_time, 'Qlast_time')
        log_format(self.tactic_group, 'tactic_group')
        log_format(self.priority, 'priority')
        log_format(self.n, 'n')
        log_format(self.Epress_time, 'Epress_time')
        log_format(self.Ecd_time, 'Ecd_time')
        logger.debug('---- character info end ----')

    def _trigger_e_ready(self):
        if self.is_E_ready():
            return True

    def _trigger_q_ready(self):
        cap = self.itt.capture()
        cap = self.itt.png2jpg(cap, channel='ui', alpha_num=20)  # BEFORE V3D1
        # cap = self.itt.png2jpg(cap, channel='bg', alpha_num = 175)

        p = posi_manager.posi_charalist_q_point[self.n - 1]
        if cap[p[0], p[1]].max() > 0:
            return True
        else:
            return False

    @staticmethod
    def _trigger_idle():
        return True

    def _trigger_analyses(self):
        """
        将str分析为函数，并加入trigger。
        """
        # if self.triggers == 'e_ready':
        #     self.trigger = self._trigger_e_ready
        # elif self.triggers == 'q_ready':
        #     self.trigger = self._trigger_q_ready
        # elif self.triggers == 'idle':
        #     self.trigger = self._trigger_idle
        c_triggers = self.triggers.split(',')
        if 'e_ready' in c_triggers:
            self.trigger_list.append(self._trigger_e_ready)
        elif 'q_ready' in c_triggers:
            self.trigger_list.append(self._trigger_q_ready)
        elif 'idle' in c_triggers:
            self.trigger_list.append(self._trigger_idle)

        self.trigger = self._is_trigger
        
    def _is_trigger(self):
        for func_i in self.trigger_list:
            if func_i():
                return True
    
    def get_Ecd_time(self):
        """获得该角色E技能cd剩余时间。

        Returns:
            float: cd time
        """
        t = self.Ecd_timer.get_diff_time()
        t = self.Ecd_time - t
        if t <= 0:
            return 0
        else:
            return t

    def used_E(self)->None:
        """
        设置该角色已经使用E技能。
        """
        if self.is_E_ready():
            self.Ecd_time = self.E_short_cd_time
            self.Ecd_timer.reset()
            self.Elast_timer.reset()

    def used_Q(self)->None:
        """
        设置该角色已经使用Q技能。
        """
        self.Qlast_timer.reset()

    def used_longE(self)->None:
        """
        设置该角色已经使用长E技能。
        """
        if self.is_E_ready():
            self.Ecd_time = self.E_long_cd_time
            self.Ecd_timer.reset()
            self.Elast_timer.reset()

    def is_E_ready(self)->bool:
        """获得E技能是否冷却完毕。

        Returns:
            bool: 
        """
        if self.get_Ecd_time() <= 0:
            return True
        else:
            return False

    # def is_chara_Q_ready(self):
    #     name = self.name
    #     filename='imgs/'+name+'_q.png'
    #     if os.path.exists(filename):
    #         img = cv2.imread(filename)
    #         mr = self.itt.similar_img(name+'_q.png',self.itt.capture(),posi_manager.posi_chara_q)
    #         logger.debug('Qmr= '+ str(mr))
    #         if mr>=0.9:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True

    def get_Ecd_last_time(self):
        t = self.Elast_timer.get_diff_time()
        t = self.Elast_time - t
        if t <= 0:
            return 0
        else:
            return t

    def get_Q_last_time(self):
        t = self.Qlast_timer.get_diff_time()
        t = self.Qlast_time - t
        if t <= 0:
            return 0
        else:
            return t

    def is_E_pass(self):
        t = self.get_Ecd_last_time()
        if t <= 0:
            return True
        else:
            return False

    def is_Q_pass(self):
        t = self.get_Q_last_time()
        if t <= 0:
            return True
        else:
            return False

    def is_position_ready(self, position_type):
        if self.position == "Shield" and position_type == "SHIELD":
            if self.is_E_ready():
                return True
        if self.position == "Core" and position_type == "CORE":
            return True
        return False

if __name__ == '__main__':
    chara = Character('4', 'none', 4, 0, 1, 2, 2, 1, 'none', 'q_ready')
    while 1:
        time.sleep(0.1)
        print(chara._trigger_q_ready(), end=' ')
