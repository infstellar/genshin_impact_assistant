from source.api.pdocr_light import ocr_light
from source.common.base_threading import BaseThreading
from source.common.character import Character, Q_SKILL_COLOR
from source.interaction.interaction_core import itt
from common.timer_module import Timer, AdvanceTimer
from source.util import *
import cv2
from source.funclib import combat_lib
from source.manager import posi_manager, asset
from source.path_lib import *

E_STRICT_MODE = True  # may cause more performance overhead
DETERMINING_WEIGHT = GIAconfig.General_DeterminingStrictWeight
USING_ALPHA_CHANNEL = GIAconfig.General_UsingAlphaChannel

def stop_func_example():  # True:stop;False:continue
    return False


class TacticOperator(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName('TacticOperator')
        self.while_sleep = 0.05
        self.hp_chara_list_green = [34, 215, 150, 255]  # BGR
        self.hp_chara_list_red = [102, 102, 255, 255]  # BGR
        self.hp_chara_list_position = [[283, 1698], [379, 1698], [475, 1698], [571, 1698]]
        self.chara_num = 4
        self.enter_timer = Timer()
        self.pause_timer = Timer()
        self.itt = itt
        self.flag_tactic_executing = False # in class
        self.pause_tactic_flag = False
        self.formered_tactic = None
        self.tactic_group = None
        self.character = None
        self.tactic_exec_timer = AdvanceTimer(0.4).start()

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
            time.sleep(0.05)
            if self.checkup_stop_func():
                break
        self.pause_tactic_flag = False
        logger.trace("restart_executor end")
    
    def run(self):
        while 1:
            # time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return

            if self.pause_threading_flag:
                if self.pause_timer.get_diff_time()<=4:
                    time.sleep(0.02)
                elif self.pause_timer.get_diff_time()<=8:
                    time.sleep(0.05)
                elif self.pause_timer.get_diff_time()<=20:
                    time.sleep(0.1)
                elif self.pause_timer.get_diff_time()<=60:
                    time.sleep(0.2)
                else:
                    time.sleep(0.4)
                continue
            self.pause_timer.reset()
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            
            # print('5')

            if (self.formered_tactic is None or len(self.formered_tactic) == 0):
                logger.trace(f"no valid tactic, skip")
                self.pause_threading()
            if not self.pause_threading_flag:
                logger.debug(f"exec tactic start")
                self.execute_tactic(self.formered_tactic)
                self.flag_tactic_executing = False
                logger.debug(f"exec tactic end")
                self.pause_threading()

    def set_parameter(self, tactic_group: str, character: Character):
        if tactic_group is None:
            self.tactic_group = None
            self.formered_tactic = None
            return
        self.tactic_group = tactic_group
        self.character = character
        self.formered_tactic = self._tactic_group_former()
    
    def set_enter_timer(self, timer):
        self.enter_timer = timer

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
        ret, t = ocr_light.is_img_num_plus(cap)

        if ret:
            return True
        else:
            cap = self.itt.capture(posi=posi_manager.posi_chara_e)
            cap = self.itt.png2jpg(cap, channel='ui', alpha_num=100)
            ret, t = ocr_light.is_img_num_plus(cap)

            if ret:
                return True
            else:
                return False
            
    def _is_longE_release(self, show_res = False):
        cap = self.itt.capture(posi=posi_manager.posi_chara_e)
        cap = self.itt.png2jpg(cap, channel='ui', alpha_num=100)
        if show_res:
            cv2.imshow("_is_e_release", cap)
            cv2.waitKey(10)
        ret, t = ocr_light.is_img_num_plus(cap)

        if ret:
            if float(t) <= self.character.E_short_cd_time:
                logger.debug(f"longE failed. Ecd time: {t}; short Ecd time: {self.character.E_long_cd_time}; long Ecd time:{self.character.E_short_cd_time}")
                time.sleep(float(t))
                return False
            else:
                return True
        else:
            return False
        

    def unconventionality_situation_detection(self, autoDispose=True):  # unconventionality situation detection
        # situation 1: coming_out_by_space
        sf = lambda: self.checkup_stop_func() and self.pause_tactic_flag
        return combat_lib.unconventionality_situation_detection(detect_type='ac', stop_func=sf)
        
        situation_code = -1

        while self.itt.get_img_existence(asset.IconCombatComingOutBySpace):
            if self.checkup_stop_func():
                return 0
            if self.pause_tactic_flag:
                return 0
            situation_code = 1
            self.itt.key_press('spacebar')
            logger.debug('Unconventionality Situation: COMING_OUT_BY_SPACE')
            time.sleep(0.1)

        return situation_code

    def _ccw_sf(self):
        return self.pause_tactic_flag or self.checkup_stop_func()
    
    def chara_waiting(self, mode=0):
        self.unconventionality_situation_detection()
        if (mode == 0) and (self.enter_timer.get_diff_time() <= 1.2):
            if self.is_e_available():
                logger.debug('skip waiting')
                return 0
            else:
                logger.debug(f"t: {self.enter_timer.get_diff_time()} but e unavailable")

        combat_lib.chara_waiting(stop_func=self._ccw_sf)
            
            # while self.get_character_busy() and (not self.checkup_stop_func()):
            #     if self.checkup_stop_func():
            #         logger.debug('chara_waiting stop')
            #         return 0
            #     if self.pause_tactic_flag:
            #         return 0
            #     # logger.debug('waiting  ')
            #     self.itt.delay(0.1)

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
        return combat_lib.is_character_busy(self.checkup_stop_func)
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

        self.chara_waiting()
        logger.debug('do_use_longe')
        if self.character.name == 'Zhongli': # 钟离总是放盾把视野挡住了
            self.itt.key_press('s')
            itt.delay(0.1)
        self.itt.key_down('e')
        self.itt.delay(self.character.Epress_time)
        self.itt.key_up('e')
        # if self.character.name == 'Zhongli':
        #     itt.delay(0.3)
        #     self.itt.key_press('w')
        if self.checkup_stop_func():
            return 0
        if self.pause_tactic_flag:
            return 0
        # self.itt.key_press('w')
        self.itt.delay(0.2)
        if (not self._is_longE_release()) and E_STRICT_MODE:
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
        self.itt.delay(self.character.long_attack_time)
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

    def is_q_ready(self, show_res=False):
        """Check Q-State by image recognition

        Args:
            is_show (bool, optional): Whether to display recognized image. Defaults to False.

        Returns:
            bool: Whether Q-Skill can be triggered
        """

        cap = self.itt.capture(jpgmode=0)
        
        imsrc = cap
        imsrc_q_skill = crop(imsrc, posi_manager.posi_complete_chara_q)
        mask = np.zeros_like(imsrc_q_skill[:,:,0])
        hh, ww = imsrc_q_skill.shape[:2]
        xc = hh // 2
        yc = ww // 2
        radius1 = 53
        radius2 = 47
        cv2.circle(mask, (xc,yc), radius1, (255,255,255), -1)
        cv2.circle(mask, (xc,yc), radius2, (0,0,0), -1)
        # mask = cv2.subtract(mask2, mask1)
        res1 = cv2.bitwise_and(imsrc_q_skill,imsrc_q_skill,mask=mask)
        # res1 = imsrc_q_skill.copy()
        HUE_DELTA = 5
        
        # stone HSV=0.12538226299694,0.85490196078431,1
        # fire 
        
        orhsv = Q_SKILL_COLOR[self.character.vision]
        # orhsv = Q_SKILL_COLOR['Hydro']
        hsv_lower = np.array([int(max(0,orhsv[0]*180-HUE_DELTA)), int(max(orhsv[1]*255-60, 50)), 200])
        hsv_upper = np.array([int(min(179,orhsv[0]*180+HUE_DELTA)), int(min(orhsv[1]*255+60, 255)), 255])
        hsv = cv2.cvtColor(res1.copy(), cv2.COLOR_BGR2HSV)
        mask2 = cv2.inRange(hsv, hsv_lower, hsv_upper)
        res = len(np.where(mask2==255)[0])
        if show_res:
            print(f"num: {res}")
            # res2 = cv2.bitwise_and(hsv,hsv, mask=mask2)
            cv2.imshow("res", mask2)
            cv2.waitKey(100)
        r = res>=(650*DETERMINING_WEIGHT)
        return r
            
        # if is_show:
        #     cv2.imshow("is_q_ready", cap)
        #     cv2.waitKey(10)
        # # cap = self.itt.png2jpg(cap, channel='bg', alpha_num=160)
        # # img_manager.qshow(cap)
        # # p = posi_manager.posi_chara_q_point
        # if cap.max() > 10:
        #     # print(cap.max())
        #     return True

        # else:
        #     # print(cap.max())
        #     return False

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
            tas[0] = tas[0].replace('.', ',')
            while (not self.character.is_E_pass()) and (not self.checkup_stop_func()):
                if self.checkup_stop_func():
                    return 0
                if self.pause_tactic_flag:
                    return 0
                self.unconventionality_situation_detection()
                self.execute_tactic([tas[0]])
        else:
            tas[1] = tas[1].replace('.', ',')
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
    # from source.controller import combat_loop

    to = TacticOperator()
    # itt = global_itt
    chara = combat_lib.get_chara_list()[1]
    to.set_parameter(chara.tactic_group, chara)
    # # to.setDaemon(True)
    while 1:
        print(to.is_q_ready(show_res=True))
        time.sleep(0.1)
    pass
