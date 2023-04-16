
# from source.interaction import *

from source.util import *
from source.common import character
from source.funclib import combat_lib
from source.manager import asset
from source.common.base_threading import AdvanceThreading
from source.interaction.interaction_core import itt
from source.operator.switch_character_operator import SwitchCharacterOperator
from source.path_lib import CONFIG_PATH_SETTING

CHARACTER_DIED = 1
MODE_NORMAL = 'Normal'
MODE_SHIELD = 'Shield'
MODE_CORE = "Core"




def sort_flag_1(x: character.Character):
    return x.priority


def stop_func_example():  # True:stop;False:continue
    return False


class CombatController(AdvanceThreading):
    def __init__(self, chara_list=None):
        super().__init__()
        self.setName('CombatController')

        self.pause_threading_flag = True

        self.sco = SwitchCharacterOperator()
        self._add_sub_threading(self.sco)
        self.sco.pause_threading()

        self.is_check_died = False
        self.mode="Normal"
        self.sco.mode = self.mode
        # self.super_stop_func=super_stop_func
    
    def loop(self):
        if self.is_check_died:
            if itt.get_img_existence(asset.IconCombatCharacterDied):
                logger.info(t2t('有人嘎了，停止自动战斗'))
                self.last_err_code = CHARACTER_DIED
                while 1:
                    time.sleep(0.5)
                    r = itt.appear_then_click(asset.ButtonUICancel)
                    if r:
                        break
                self.pause_threading()

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            logger.info(t2t('停止自动战斗'))
            return True
        return False

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.current_num = combat_lib.get_current_chara_num(self.checkup_stop_func)
            self.pause_threading_flag = False
            self.sco.mode = self.mode
            self.sco.continue_threading()

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.sco.pause_threading()


    def checkup_trapped(self):
        pass
        # if itt.capture(posi=posiM)


if __name__ == '__main__':
    cl = CombatController()
    cl.start()
    # a = get_chara_list()
    # print()
