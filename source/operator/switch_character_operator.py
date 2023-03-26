from source.common import character
from source.funclib import combat_lib
from source.operator import tactic_operator
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from common.timer_module import Timer, AdvanceTimer
from source.util import *
from source.manager import asset
from source.operator.aim_operator import AimOperator
from source.api.pdocr_complete import ocr


SHIELD = 'Shield'
CORE = 'Core'
SUB_CORE = 'SubCore'
ASSIST = "Assist"

def sort_flag_1(x: character.Character):
    return x.priority


class SwitchCharacterOperator(BaseThreading):
    def __init__(self, chara_list):
        super().__init__()
        self.setName('SwitchCharacterOperator')
        self.chara_list = chara_list
        self.itt = itt

        self.tactic_operator = tactic_operator.TacticOperator()
        self.aim_operator = AimOperator()
        self._add_sub_threading(self.tactic_operator)
        self._add_sub_threading(self.aim_operator)
        self.chara_list.sort(key=sort_flag_1, reverse=False)
        self.current_num = 1 # combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
        self.switch_timer = Timer(diff_start_time=2)
        self.tactic_operator.set_enter_timer(self.switch_timer)

        self.died_character = [] # 存储的是n而非name
        self.reborn_timer = Timer(diff_start_time=150)
        self.position_check_timer = AdvanceTimer(0.5)
    
    def run(self):
        while 1:
            time.sleep(0.1)
            if self.stop_threading_flag:
                self.tactic_operator.stop_threading()
                return

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
            if self.aim_operator.sco_blocking_request.is_blocking():
                self.aim_operator.sco_blocking_request.reply_request()
                self.switch_character(switch_type="POSITION")
                time.sleep(0.5)
                continue
            if self.tactic_operator.get_working_statement():  # tactic operator working
                time.sleep(0.1)
                if self.position_check_timer.reached_and_reset():
                    self.switch_character(switch_type="POSITION")
            else:
                self.switch_character(switch_type="TRIGGER")
                time.sleep(0.5)

    
    def _check_and_reborn(self) -> bool:
        """重生角色

        Returns:
            bool: #zh_CN 若复活成功或不需要复活，返回True，否则返回False. #en_US Returns True if resurrection is successful or not required, otherwise returns False.
            
        """
        if itt.get_img_existence(asset.character_died, is_log=True):
            succ_flag_1 = False
            print(self.died_character)
            for i in range(10):
                if ocr.is_img_num_plus(itt.capture(posi=asset.Area_revival_foods.position, jpgmode=0))[0]:
                    break
                time.sleep(0.15)
                if self.checkup_stop_func(): # break
                    return True
                r = itt.appear_then_click(asset.ButtonEgg, is_log=True)
                if r:
                    succ_flag_1 = True 
                    break
            if not succ_flag_1:
                logger.info("reborn failed")
                self.reborn_timer.reset()
                return False # failed
                  
            for i in range(3):
                time.sleep(0.15)
                ret_check_and_reborn_2 = itt.appear_then_click(asset.confirm, is_log=True)
                print(f"ret_check_and_reborn_2 {ret_check_and_reborn_2}")
                if ret_check_and_reborn_2:
                    self.reborn_timer.reset()
                    self.died_character = [] # clean list
                    time.sleep(0.3) # 防止重复检测
                    return True # reborn succ
            self.reborn_timer.reset()
            itt.key_press('esc')
            time.sleep(0.3) # 防止重复检测
            return False # failed
        else:
            return True
            
    
    def switch_character(self, switch_type="TRIGGER"):
        """_summary_

        Args:
            switch_type (str, optional): _description_. Defaults to "TRIGGER". "TRIGGER" "POSITION

        Returns:
            _type_: _description_
        """
        for chara in self.chara_list:
            logger.debug('check up in: ' + chara.name)
            if self.checkup_stop_func():
                return 0
            if chara.n in self.died_character: # died
                if self.reborn_timer.get_diff_time()<=125: # reborn cd
                    continue
            if (switch_type == "TRIGGER" and chara.trigger()) or (switch_type == "POSITION" and chara.is_position_ready()):
                if chara.trigger():
                    self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
                    logger.debug(f"switch_character: {switch_type}: targetnum: {chara.n} current num: {self.current_num}")
                    if chara.n != self.current_num:
                        self.aim_operator.pause_threading()
                        self.tactic_operator.pause_threading()
                        r = self._switch_character(chara.n)
                        if not r: # Failed
                            continue
                        self.tactic_operator.set_parameter(chara.tactic_group, chara)
                        self.tactic_operator.restart_executor()
                        self.tactic_operator.continue_threading()
                        self.aim_operator.continue_threading()
                        return True
       

    def _switch_character(self, x: int) -> bool:
        """_summary_

        Args:
            x (int): _description_

        Returns:
            bool: True: 切换成功; False: 切换失败
        """
        # self.itt.middle_click()
        t = self.switch_timer.get_diff_time()
        self.tactic_operator.chara_waiting()
        logger.debug('try switching to ' + str(x))
        switch_succ_num = 0
        switch_target_num = 2
        for i in range(60):
            if self.checkup_stop_func():
                return True
            if i > 3:
                is_busy = combat_lib.is_character_busy(self.checkup_stop_func)
            else:
                is_busy = False
            if not is_busy:
                if i > 3:
                    combat_lib.unconventionality_situation_detection(self.itt)
                self.itt.key_press(str(x))
                if combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func, max_times = 5) == x:
                    switch_succ_num += 1
            if i >= 5 or is_busy == True:
                r = self._check_and_reborn()
                if not r: # if r == False
                    self.died_character.append(x)
                    itt.key_press('esc')
                    return True
            if i > 55:
                logger.warning('角色切换失败')
            if switch_succ_num >= switch_target_num:
                logger.debug(f"switch chara to {x} succ")
                self.current_num = x
                self.switch_timer.reset()
                # self.itt.delay(0.05)
                return True
        # self.current_num = x
        self.switch_timer.reset()
        # self.itt.delay(0.05)
        return False

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.tactic_operator.pause_threading()
            self.aim_operator.pause_threading()

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False
            self.tactic_operator.set_parameter(None, None)
            self.tactic_operator.continue_threading()
            self.aim_operator.continue_threading()
            self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)


if __name__ == '__main__':
    pass
    # import combat_loop
    # chara=combat_loop.get_chara_list()
    # sco=Switch_Character_Operator(chara)

    # to.set_parameter(chara.tactic_group,chara)
    # sco.start()
