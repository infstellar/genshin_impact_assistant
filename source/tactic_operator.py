import time

import img_manager
if True:
    import pdocr_api
else:
    pdocr_api = None
import posi_manager
from base_threading import BaseThreading
from character import Character
from interaction_background import InteractionBGD
from timer_module import Timer
from util import *
import cv2
import combat_lib

E_STRICT_MODE = True  # may cause more performance overhead


def stop_func_example():  # True:stop;False:continue
    return False


class TacticOperator(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName('Tactic_Operator')
        self.while_sleep = 0.1
        self.hp_chara_list_green = [34, 215, 150, 255]  # BGR
        self.hp_chara_list_red = [102, 102, 255, 255]  # BGR
        self.hp_chara_list_position = [[283, 1698], [379, 1698], [475, 1698], [571, 1698]]
        self.chara_num = 4
        self.enter_timer = Timer()
        self.itt = InteractionBGD()
        self.working_flag = False # out of class
        self.flag_tactic_executing = False # in class
        self.pause_tactic_flag = False
        self.formered_tactic = None
        self.tactic_group = None
        self.character = None

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.tactic_group = None
            self.formered_tactic = None
    
    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False
            # self.tactic_group = None
            # self.formered_tactic = None
    
    def restart_executor(self):
        logger.trace("restart_executor start")
        self.pause_tactic_flag = True
        while self.flag_tactic_executing:
            time.sleep(0.1)
            if self.checkup_stop_func():
                break
        self.pause_tactic_flag = False
        logger.trace("restart_executor end")
    
    def run(self):
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(0.3)
                continue
            
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            
            # print('5')

            self.working_flag = True
            if self.formered_tactic is None:
                self.working_flag = False
                continue
            if not self.pause_tactic_flag:
                self.execute_tactic(self.formered_tactic)
                self.flag_tactic_executing = False
                self.working_flag = False

    def set_parameter(self, tactic_group: str, character: Character):
        if tactic_group is None:
            self.tactic_group = None
            self.formered_tactic = None
            return
        self.tactic_group = tactic_group
        self.character = character
        self.formered_tactic = self._tactic_group_former()
        self.enter_timer.reset()

    def _tactic_group_former(self):
        tactic = self.tactic_group.split(';')
        return tactic

    def is_e_available(self):  # 被击飞时不可用
        cap = self.itt.capture(posi=posi_manager.posi_chara_smaller_e, jpgmode=2)
        if cap.max() < 10:
            return False
        else:
            return True

    def _is_e_release(self, show_res = False):
        cap = self.itt.capture(posi=posi_manager.posi_chara_e)
        cap = self.itt.png2jpg(cap, channel='ui', alpha_num=100)
        if show_res:
            cv2.imshow("_is_e_release", cap)
            cv2.waitKey(10)
        ret = pdocr_api.ocr.is_img_num_plus(cap)

        if ret[0]:
            return True
        else:
            cap = self.itt.capture(posi=posi_manager.posi_chara_e)
            cap = self.itt.png2jpg(cap, channel='ui', alpha_num=100)
            ret = pdocr_api.ocr.is_img_num_plus(cap)

            if ret[0]:
                return True
            else:
                return False

    def unconventionality_situation_detection(self, autoDispose=True):  # unconventionality situation detection
        # situation 1: coming_out_by_space

        situation_code = -1

        while self.itt.get_img_existence(img_manager.COMING_OUT_BY_SPACE):
            if self.checkup_stop_func():
                return 0
            if self.pause_tactic_flag:
                return 0
            situation_code = 1
            self.itt.key_press('spacebar')
            logger.debug('Unconventionality Situation: COMING_OUT_BY_SPACE')
            time.sleep(0.1)

        return situation_code

    def chara_waiting(self, mode=0):
        self.unconventionality_situation_detection()
        if (mode == 0) and self.is_e_available() and (self.enter_timer.get_diff_time() <= 1):
            logger.debug('skip waiting')
            return 0
        while self.get_character_busy() and (not self.checkup_stop_func()):
            if self.checkup_stop_func():
                logger.debug('chara_waiting stop')
                return 0
            if self.pause_tactic_flag:
                return 0
            logger.debug('waiting  ')
            self.itt.delay(0.1)

    # def get_current_chara_num(self):
    #     cap = self.itt.capture(jpgmode=2)
    #     for i in range(4):
    #         if self.checkup_stop_func():
    #             return 0
    #         p = posi_manager.chara_num_list_point[i]

    #         if min(cap[p[0], p[1]]) > 240:
    #             continue
    #         else:
    #             return i + 1

    def get_character_busy(self):
        return combat_lib.get_character_busy(self.itt, self.checkup_stop_func)
        # cap = self.itt.capture()
        # cap = self.itt.png2jpg(cap, channel='ui')
        # t = 0
        # for i in range(self.chara_num):
        #     if self.checkup_stop_func():
        #         return 0
        #     p = posi_manager.chara_head_list_point[i]
        #     if cap[p[0], p[1]][0] > 0 and cap[p[0], p[1]][1] > 0 and cap[p[0], p[1]][2] > 0:
        #         t += 1
        # if t >= 3:
        #     return False
        # else:
        #     return True

    def do_attack(self):
        self.chara_waiting()
        self.itt.left_click()
        self.itt.delay(0.1)

    def do_down_attack(self):
        self.itt.left_click()
        self.itt.delay(0.1)

    def do_use_e(self, times=0):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        if times >= 2:
            return -1

        if self.character.Ecd_float_time > 0:
            if self._is_e_release():
                self.itt.delay(self.character.get_Ecd_time() + 0.1)

        self.chara_waiting()
        logger.debug('do_use_e')
        self.itt.key_press('e')
        self.itt.delay(0.2)
        if (not self._is_e_release()) and E_STRICT_MODE:
            self.do_use_e(times=times + 1)
        self.character.used_E()

    def do_use_longe(self, times=0):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        if times >= 2:
            return -1

        if self.character.Ecd_float_time > 0:
            self.itt.delay(self.character.get_Ecd_time() + 0.1)

        self.chara_waiting()
        logger.debug('do_use_longe')
        self.itt.key_press('s')
        self.itt.key_down('e')
        self.itt.delay(self.character.Epress_time)
        self.itt.key_up('e')
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        self.itt.key_press('w')
        self.itt.delay(0.2)
        if (not self._is_e_release()) and E_STRICT_MODE:
            self.do_use_longe(times=times + 1)
        self.character.used_longE()

    def do_use_q(self, times=0):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        if times > 2:
            return -1

        self.chara_waiting()
        self.itt.key_press('q')
        self.itt.delay(0.2)
        self.chara_waiting()
        if (self.is_q_ready()) and E_STRICT_MODE:
            logger.debug('没q到')
            self.do_use_q(times=times + 1)
        self.character.used_Q()

    def do_long_attack(self):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        self.chara_waiting(mode=1)
        self.itt.left_down()
        self.itt.delay(2.5)
        self.itt.left_up()

    def do_jump(self):
        self.chara_waiting(mode=1)
        self.itt.key_press('spacebar')

    def do_jump_attack(self):
        self.chara_waiting(mode=1)
        self.itt.key_press('spacebar')
        self.itt.delay(0.3)
        self.itt.left_click()

    def do_sprint(self):
        self.itt.right_click()

    def do_aim(self):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        self.chara_waiting(mode=1)
        self.itt.key_press('r')

    def do_unaim(self):
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        self.itt.key_press('r')

    def is_q_ready(self, is_show=False):
        cap = self.itt.capture(posi=posi_manager.posi_chara_q)
        cap = self.itt.png2jpg(cap, channel='ui', alpha_num=200)  # BEFOREV3D1
        if is_show:
            cv2.imshow("is_q_ready", cap)
            cv2.waitKey(10)
        # cap = self.itt.png2jpg(cap, channel='bg', alpha_num=160)
        # img_manager.qshow(cap)
        # p = posi_manager.posi_chara_q_point
        if cap.max() > 10:
            # print(cap.max())
            return True

        else:
            # print(cap.max())
            return False

    def estimate_e_ready(self, tactic):
        is_ready = self.character.is_E_ready()
        tas = tactic[tactic.index('?') + 1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tactic([tas[0].replace('.', ',')])
        else:
            self.execute_tactic([tas[1].replace('.', ',')])

    def estimate_q_ready(self, tactic):
        is_ready = self.is_q_ready()
        # print(is_ready)
        tas = tactic[tactic.index('?') + 1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tactic([tas[0].replace('.', ',')])
        else:
            self.execute_tactic([tas[1].replace('.', ',')])

    def estimate_lock_e_ready(self, tactic):  # #@e?
        is_ready = not self.character.is_E_pass()
        tas = tactic[4:]
        tas = tas.split(':')
        if is_ready:
            tas[0].replace('.', ',')
            while (not self.character.is_E_pass()) and (not self.checkup_stop_func()):
                if self.checkup_stop_func():
                    return 0
                if self.pause_tactic_flag:
                    return 0
                self.unconventionality_situation_detection()
                self.execute_tactic([tas[0]])
        else:
            tas[1].replace('.', ',')
            self.execute_tactic([tas[1]])

    def estimate_lock_q_ready(self, tactic):  # #@q?
        is_ready = not self.character.is_Q_pass()
        tas = tactic[4:]
        tas = tas.split(':')
        if is_ready:
            tas[0].replace('.', ',')
            if self.checkup_stop_func():
                logger.debug('lock stop')
            if self.pause_tactic_flag:
                return 0
            while (not self.character.is_Q_pass()) and (not self.checkup_stop_func()):
                if self.checkup_stop_func():
                    return 0
                if self.pause_tactic_flag:
                    return 0
                self.unconventionality_situation_detection()
                self.execute_tactic([tas[0]])
        else:
            tas[1].replace('.', ',')
            self.execute_tactic([tas[1]])

    def execute_tactic(self, tactic_list):
        self.flag_tactic_executing = True
        self.unconventionality_situation_detection()

        for tactic in tactic_list:
            if self.checkup_stop_func():
                return 0
            if self.pause_tactic_flag:
                break
            tactic = tactic.split(',')
            for tas in tactic:
                if self.checkup_stop_func():
                    break
                if self.pause_tactic_flag:
                    break
                if tas == 'a':
                    self.do_attack()
                elif tas == 'da':
                    self.do_down_attack()
                elif tas == 'q':
                    self.do_use_q()
                elif tas == 'e':
                    self.do_use_e()
                elif tas == 'e~':
                    self.do_use_longe()
                elif tas == 'a~':
                    self.do_long_attack()
                elif tas == 'j':
                    self.do_jump()
                elif tas == 'ja':
                    self.do_jump_attack()
                elif tas == 'sp':
                    self.do_sprint()
                elif tas == 'r':
                    self.do_aim()
                elif tas == 'rr':
                    self.do_unaim()
                elif is_int(tas):
                    self.itt.delay(int(tas) / 1000, randtime=False)
                elif tas == '>':
                    break

                if '?' in tas:
                    tas1 = tas[0:tas.index('?') + 1]
                    if tas1 == 'e?':
                        self.estimate_e_ready(tas)
                    elif tas1 == '#@e?':
                        self.estimate_lock_e_ready(tas)
                    elif tas1 == 'q?':
                        self.estimate_q_ready(tas)
                    elif tas1 == '#@q?':
                        self.estimate_lock_q_ready(tas)
        
        

if __name__ == '__main__':
    import combat_loop

    to = TacticOperator()
    itt = InteractionBGD()
    chara = combat_loop.get_chara_list()[1]
    to.set_parameter(chara.tactic_group, chara)
    # to.setDaemon(True)
    while 1:
        print(to._is_e_release(show_res=True))
        time.sleep(0.1)
