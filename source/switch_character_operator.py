import time

import pyautogui

import character
import combat_lib
import tastic_operator
from base_threading import BaseThreading
from interaction_background import InteractionBGD
from timer_module import Timer
from util import *


def sort_flag_1(x: character.Character):
    return x.priority


class SwitchCharacterOperator(BaseThreading):
    def __init__(self, chara_list: list[character.Character]):
        super().__init__()
        self.setName('Switch_Character_Operator')
        self.chara_list = chara_list
        self.itt = InteractionBGD()

        self.tastic_operator = tastic_operator.TasticOperator()
        self.tastic_operator.pause_threading()
        self.tastic_operator.setDaemon(True)
        self.tastic_operator.start()
        self.chara_list.sort(key=sort_flag_1, reverse=False)
        self.current_num = 1
        self.switch_timer = Timer(diff_start_time=2)

    def run(self):
        while 1:
            time.sleep(0.2)
            if self.stop_threading_flag:
                self.tastic_operator.stop_threading()
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)

                continue

            if not self.working_flag:  # tastic operator no working
                self.working_flag = True
            if self.tastic_operator.get_working_statement():  # tastic operator working
                time.sleep(0.2)

            else:
                ret = self.switch_character()
                if not ret:  # able to change character
                    self.tastic_operator.continue_threading()
                    time.sleep(1)

                else:  # no changable character
                    time.sleep(0.2)

    def switch_character(self):
        idle = True
        for chara in self.chara_list:
            logger.debug('check up in: ' + chara.name)
            if self.checkup_stop_func():
                return 0
            if chara.trigger():
                if chara.n != self.current_num:
                    self._switch_character(chara.n)
                self.tastic_operator.set_parameter(chara.tastic_group, chara)
                idle = False
                return idle
        return idle

    def _switch_character(self, x: int):
        pyautogui.click(button='middle')
        t = self.switch_timer.get_diff_time()
        self.tastic_operator.chara_waiting()
        logger.debug('try switching to ' + str(x))
        for i in range(120):  # 12 sec
            if self.checkup_stop_func():
                return 0
            combat_lib.unconventionality_situlation_detection(self.itt)
            self.itt.key_press(str(x))
            time.sleep(0.1)
            if combat_lib.get_current_chara_num(self.itt) == x:
                break
            if i == 49:
                logger.warning('角色切换失败')
        self.current_num = x
        self.switch_timer.reset()
        self.itt.delay(0.1)

    def pause_threading(self):
        self.pause_threading_flag = True
        self.tastic_operator.pause_threading()

    def continue_threading(self):
        self.pause_threading_flag = False
        self.tastic_operator.continue_threading()


if __name__ == '__main__':
    pass
    # import combat_loop
    # chara=combat_loop.get_chara_list()
    # sco=Switch_Character_Operator(chara)

    # to.set_parameter(chara.tastic_group,chara)
    # sco.start()
