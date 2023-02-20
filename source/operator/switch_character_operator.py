from source.common import character
from source.funclib import combat_lib
from source.operator import tactic_operator
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from common.timer_module import Timer
from source.util import *
from source.manager import asset


def sort_flag_1(x: character.Character):
    return x.priority


class SwitchCharacterOperator(BaseThreading):
    def __init__(self, chara_list):
        super().__init__()
        self.setName('Switch_Character_Operator')
        self.chara_list = chara_list
        self.itt = itt

        self.tactic_operator = tactic_operator.TacticOperator()
        self._add_sub_threading(self.tactic_operator)
        self.chara_list.sort(key=sort_flag_1, reverse=False)
        self.current_num = 1 # combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
        self.switch_timer = Timer(diff_start_time=2)
        self.tactic_operator.set_enter_timer(self.switch_timer)
    
    def run(self):
        while 1:
            time.sleep(0.1)
            if self.stop_threading_flag:
                self.tactic_operator.stop_threading()
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)

                continue

            if not self.working_flag:  # tactic operator no working
                self.working_flag = True
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            if self.tactic_operator.get_working_statement():  # tactic operator working
                time.sleep(0.1)
            else:
                ret = self.switch_character()
                if not ret:  # able to change character
                    self.tactic_operator.continue_threading()
                    time.sleep(0.2)

                else:  # no changable character
                    pass
    
    def _check_and_reborn(self) -> bool:
        """重生角色

        Returns:
            bool: #zh_CN 若复活成功或不需要复活，返回True，否则返回False. #en_US Returns True if resurrection is successful or not required, otherwise returns False.
            
        """
        if itt.get_img_existence(asset.character_died):
            succ_flag_1 = False
            for i in range(10):
                time.sleep(0.15)
                if self.checkup_stop_func():
                    return
                r = itt.appear_then_click(asset.ButtonEgg)
                if r:
                    succ_flag_1 = True
                    break
            if not succ_flag_1:
                return False
                  
            for i in range(10):
                time.sleep(0.15)
                r = itt.appear_then_click(asset.confirm)
                if r:
                    return True
            return False
        else:
            return True
            
    
    def switch_character(self):
        idle = True
        for chara in self.chara_list:
            logger.debug('check up in: ' + chara.name)
            if self.checkup_stop_func():
                return 0
            if chara.trigger():
                self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
                logger.debug(f"switch_character: targetnum: {chara.n} current num: {self.current_num}")
                if chara.n != self.current_num:
                    r = self._switch_character(chara.n)
                if not r: # Failed
                    pass
                self.tactic_operator.set_parameter(chara.tactic_group, chara)
                self.tactic_operator.restart_executor()
                idle = False
                return idle
        return idle

    def _switch_character(self, x: int):
        self.itt.middle_click()
        t = self.switch_timer.get_diff_time()
        self.tactic_operator.chara_waiting()
        logger.debug('try switching to ' + str(x))
        switch_succ_num = 0
        switch_target_num = 2
        for i in range(120):  # 12 sec
            if self.checkup_stop_func():
                return 0
            self.tactic_operator.chara_waiting()
            combat_lib.unconventionality_situation_detection(self.itt)
            self.itt.key_press(str(x))
            time.sleep(0.03)
            if combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func) == x:
                switch_succ_num += 1
            if i >= 20:
                r = self._check_and_reborn()
                if not r:
                    return False
            if i == 49:
                logger.warning('角色切换失败')
            if switch_succ_num >= switch_target_num:
                logger.debug(f"switch chara to {x} succ")
                break
        self.current_num = x
        self.switch_timer.reset()
        self.itt.delay(0.05)
        return True

    def pause_threading(self):
        self.pause_threading_flag = True
        self.tactic_operator.pause_threading()

    def continue_threading(self):
        self.pause_threading_flag = False
        self.tactic_operator.set_parameter(None, None)
        self.tactic_operator.continue_threading()
        self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)


if __name__ == '__main__':
    pass
    # import combat_loop
    # chara=combat_loop.get_chara_list()
    # sco=Switch_Character_Operator(chara)

    # to.set_parameter(chara.tactic_group,chara)
    # sco.start()
