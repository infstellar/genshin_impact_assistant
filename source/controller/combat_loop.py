
# from source.interaction import *

from source.util import *
from source.common import character
from source.funclib import combat_lib
from source.manager import asset
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from source.operator.switch_character_operator import SwitchCharacterOperator
from source.path_lib import CONFIG_PATH_SETTING

CHARACTER_DIED = 1

def sort_flag_1(x: character.Character):
    return x.priority


def stop_func_example():  # True:stop;False:continue
    return False


class Combat_Controller(BaseThreading):
    def __init__(self, chara_list=None):
        super().__init__()
        if chara_list is None:
            chara_list = combat_lib.get_chara_list()
        self.setName('Combat_Controller')

        self.chara_list = chara_list
        self.pause_threading_flag = False

        self.sco = SwitchCharacterOperator(self.chara_list)
        self.sco.pause_threading()
        self.sco.add_stop_func(self.checkup_stop_func)
        self.sco.setDaemon(True)
        self.sco.start()

        self.is_check_died = False
        
        # self.super_stop_func=super_stop_func
    
    def run(self) -> None:
        while 1:
            time.sleep(0.2)
            if self.checkup_stop_threading():
                self.sco.stop_threading()
                return
            
            
            
            if self.is_check_died:
                if itt.get_img_existence(asset.character_died):
                    logger.info(t2t('有人嘎了，停止自动战斗'))
                    self.last_err_code = CHARACTER_DIED
                    while 1:
                        time.sleep(0.5)
                        r = itt.appear_then_click(asset.button_ui_cancel)
                        if r:
                            break
                    self.pause_threading()
            
            if not self.pause_threading_flag:
                if self.checkup_stop_func():
                    break

                self.sco.continue_threading()
                
            else:
                self.sco.pause_threading()
                
                continue
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            # print('6')
            # time.sleep(1)

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            logger.info(t2t('停止自动战斗'))
            return True
        
        
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            logger.info(t2t('停止自动战斗'))
            return True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.current_num = combat_lib.get_current_chara_num(self.checkup_stop_func)
            # self.current_num = 1
            self.pause_threading_flag = False
            self.sco.continue_threading()

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.sco.pause_threading()


    def checkup_trapped(self):
        pass
        # if itt.capture(posi=posiM)

    def stop_threading(self):
        self.stop_threading_flag = True


if __name__ == '__main__':
    cl = Combat_Controller()
    cl.start()
    # a = get_chara_list()
    # print()
