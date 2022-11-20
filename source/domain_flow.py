import pyautogui
import combat_loop
import flow_state as ST
import generic_lib
import img_manager
import interaction_background
import movement
import pdocr_api
import posi_manager as PosiM
import text_manager as textM
import timer_module
import yolox_api
from base_threading import BaseThreading
from util import *


class DomainFlow(BaseThreading):
    @logger.catch
    def __init__(self):
        super().__init__()
        self.setName('Domain_Flow')

        self.current_state = ST.INIT_MOVETO_CHALLENGE
        # self.current_state = ST.IN_MOVETO_TREE

        self.itt = interaction_background.InteractionBGD()
        chara_list = combat_loop.get_chara_list()
        self.combat_loop = combat_loop.Combat_Controller(chara_list)
        self.combat_loop.setDaemon(True)

        self.combat_loop.pause_threading()
        self.combat_loop.start()

        domain_json = load_json("auto_domain.json")

        domain_times = domain_json["domain_times"]
        if domain_times == 0:
            x = input("请输入秘境次数")
            # x.replace(']','')
            domain_times = int(x)
        self.lockOnFlag = 0
        self.move_num = 2.5

        reflash_config()
        self.isLiYue = domain_json["isLiYueDomain"]
        self.resin_mode = domain_json["resin"]
        self.fast_mode = domain_json["fast_mode"]
        self.move_timer = timer_module.Timer()
        self.ahead_timer = timer_module.Timer()
        self.fast_move_timer = timer_module.Timer()

        self.last_domain_times = domain_times - 1
        logger.info('秘境次数：' + str(domain_times))

    def stop_threading(self):
        logger.info('停止自动秘境')
        self.combat_loop.stop_threading()
        self.stop_threading_flag = True

    def checkup_stop_func(self):
        if self.stop_threading_flag or self.pause_threading_flag:
            return True

    def get_stop_flag(self):
        return self.stop_threading_flag

    def auto_start_init(self):
        self.current_state = ST.INIT_MOVETO_CHALLENGE
        # self.domaininitflag=False
        # self.automatic_start=True

    def _state_check(self):  # Not in using
        cap = self.itt.capture()
        cap = self.itt.png2jpg(cap, channel='ui')
        if self.current_state == ST.BEFORE_MOVETO_CHALLENGE:
            for func_item in [self._Trigger_AFTER_MOVETO_CHALLENGE]:
                if func_item(cap):
                    self.current_state = ST.AFTER_MOVETO_CHALLENGE

        elif self.current_state == ST.IN_CHALLENGE:
            for func_item in [self._Trigger_AFTER_CHALLENGE]:
                if func_item(cap):
                    self.current_state = ST.END_CHALLENGE

        elif self.current_state == ST.IN_GETTING_REAWARD:
            for func_item in [self._Trigger_GETTING_REAWARD]:
                if func_item(cap):
                    self.current_state = ST.AFTER_GETTING_REAWARD

        elif self.current_state == ST.END_DOMAIN:
            pass

    def _Trigger_AFTER_MOVETO_CHALLENGE(self, cap=None):
        if cap is None:
            cap = self.itt.capture()
            cap = self.itt.png2jpg(cap, channel='ui')

        if generic_lib.f_recognition(self.itt):
            # if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['Start']),
            #                                    textM.text(textM.start_challenge)) != -1:
            return True
        else:
            return False

    def _Trigger_AFTER_CHALLENGE(self, cap=None):
        if cap is None:
            cap = self.itt.capture()
            cap = self.itt.png2jpg(cap, channel='ui')
        if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['LeavingIn']),
                                           textM.text(textM.LeavingIn)) != -1:
            return True
        else:
            return False

    def _Trigger_GETTING_REAWARD(self, cap):  # Not in using
        if generic_lib.f_recognition(self.itt):
            # if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['ClaimRewards']),
            #                                    textM.text(textM.claim_rewards)) != -1:
            return True
        else:
            return False

    def Flow_INIT_MOVETO_CHALLENGE(self):
        logger.info('正在开始挑战秘境')
        movement.reset_view()
        # cap=self.itt.capture(jpgmode=2)
        while 1:
            cap = self.itt.capture(jpgmode=2)
            if self.checkup_stop_func():
                return 0

            if pdocr_api.ocr.get_text_position(cap, textM.text(textM.clld)) != -1:
                break
            if self.itt.get_img_existence(img_manager.IN_DOMAIN):
                break
            time.sleep(1)
            # cap=self.itt.capture(jpgmode=2)

        if self.checkup_stop_func():
            return 0

        cap = self.itt.capture(jpgmode=2)
        if pdocr_api.ocr.get_text_position(cap, textM.text(textM.clld)) != -1:
            self.itt.move_to(PosiM.posi_domain['CLLD'][0], PosiM.posi_domain['CLLD'][1])
            time.sleep(1)
            pyautogui.leftClick()

        if self.checkup_stop_func():
            return 0
        time.sleep(2)
        movement.reset_view()
        time.sleep(3)
        movement.view_to_angle_domain(-90)

        self.current_state = ST.BEFORE_MOVETO_CHALLENGE

    def Flow_IN_FINGING_TREE(self):
        if self.lockOnFlag <= 5:
            is_tree = self.align_to_tree()
            self.ahead_timer.reset()
            if not is_tree:
                movement.view_to_angle_domain(-90)

                if self.isLiYue:  # barrier treatment
                    if self.move_timer.get_diff_time() >= 20:
                        direc = not direc
                        self.move_timer.reset()
                    if direc:
                        movement.move(movement.LEFT, distance=4)
                    else:
                        movement.move(movement.RIGHT, distance=4)

                else:  # maybe can't look at tree
                    logger.debug('can not find tree. moving back.')
                    movement.move(movement.BACK, distance=2)
        else:
            self.current_state = ST.END_FINGING_TREE

    def Flow_IN_MOVETO_TREE(self):
        self.itt.key_down('w')
        while 1:
            if self.ahead_timer.get_diff_time() >= 5:
                self.itt.key_press('spacebar')
                self.ahead_timer.reset()

            movement.view_to_angle_domain(-90)

            # time.sleep(0.2)

            # cap = self.itt.capture(posi=PosiM.posi_domain["ClaimRewards"])  # posi=PosiM.posi_domain["ClaimRewards"]
            # cap = self.itt.png2jpg(cap, channel='ui')

            if generic_lib.f_recognition(self.itt):
                break

            t = self.fast_move_timer.loop_time()  # max check up speed: 1/10 second
            if t <= 1 / 10:
                time.sleep(1 / 10 - t)

            # if pdocr_api.ocr.get_text_position(cap, textM.text(textM.claim_rewards)) != -1:
            #     self.current_state = ST.END_MOVETO_TREE
            #     return 0

        self.current_state = ST.AFTER_MOVETO_TREE

    def Flow_IN_ATTAIN_REAWARD(self):

        while 1:
            if self.resin_mode == '40':
                self.itt.appear_then_click(img_manager.USE_20X2RESIN_DOBLE_CHOICES)
            elif self.resin_mode == '20':
                self.itt.appear_then_click(img_manager.USE_20RESIN_DOBLE_CHOICES)

            if pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=3), textM.text(textM.domain_obtain)) != -1:
                break

        time.sleep(2)
        self.current_state = ST.END_ATTAIN_REAWARD
        return 0

    @logger.catch
    def run(self):
        cap = self.itt.capture()
        cap = self.itt.png2jpg(cap, channel='ui')
        while 1:
            time.sleep(self.while_sleep)
            if self.checkup_stop_threading():
                self.stop_threading()
                time.sleep(2)
                return 0

            # if self.domaininitflag==False:

            #     continue
            # self._state_check()

            if self.current_state == ST.INIT_MOVETO_CHALLENGE:
                self.Flow_INIT_MOVETO_CHALLENGE()

            elif self.current_state == ST.BEFORE_MOVETO_CHALLENGE:

                if self.checkup_stop_func():
                    break
                time.sleep(5)

                if self.fast_mode:
                    self.itt.key_down('w')

                self.while_sleep = 0
                self.current_state = ST.IN_MOVETO_CHALLENGE

            elif self.current_state == ST.IN_MOVETO_CHALLENGE:
                movement.view_to_angle_domain(-90)
                if self.fast_mode:
                    pass
                else:
                    movement.move(movement.AHEAD, 4)

                if self._Trigger_AFTER_MOVETO_CHALLENGE():
                    self.while_sleep = 0.2
                    self.current_state = ST.INIT_CHALLENGE

                t = self.fast_move_timer.loop_time()  # max check up speed: 1/10 second
                if t <= 1 / 10:
                    time.sleep(1 / 10 - t)
                else:
                    pass
                    # logger.debug('low speed: ' + str(t))

            elif self.current_state == ST.INIT_CHALLENGE:
                self.itt.key_up('w')
                logger.info('正在开始战斗')
                self.combat_loop.continue_threading()
                self.itt.key_press('f')
                time.sleep(0.1)

                self.current_state = ST.IN_CHALLENGE

            elif self.current_state == ST.IN_CHALLENGE:

                time.sleep(3)
                if self._Trigger_AFTER_CHALLENGE():
                    self.current_state = ST.AFTER_CHALLENGE

            elif self.current_state == ST.AFTER_CHALLENGE:
                logger.info('正在停止战斗')
                self.combat_loop.pause_threading()
                time.sleep(5)
                logger.info('等待岩造物消失')
                time.sleep(20)
                self.current_state = ST.END_CHALLENGE

            elif self.current_state == ST.END_CHALLENGE:
                self.current_state = ST.INIT_FINGING_TREE

            elif self.current_state == ST.INIT_FINGING_TREE:
                logger.info('正在激活石化古树')
                self.lockOnFlag = 0
                self.current_state = ST.IN_FINGING_TREE

            elif self.current_state == ST.IN_FINGING_TREE:
                self.Flow_IN_FINGING_TREE()

            elif self.current_state == ST.END_FINGING_TREE:
                self.current_state = ST.INIT_MOVETO_TREE

            elif self.current_state == ST.INIT_MOVETO_TREE:
                self.current_state = ST.IN_MOVETO_TREE

            elif self.current_state == ST.IN_MOVETO_TREE:
                self.Flow_IN_MOVETO_TREE()
                self.itt.key_up('w')
                self.current_state = ST.AFTER_MOVETO_TREE

            elif self.current_state == ST.AFTER_MOVETO_TREE:
                time.sleep(0.2)
                if not generic_lib.f_recognition():
                    self.current_state = ST.END_MOVETO_TREE
                else:
                    self.itt.key_up('w')
                    self.itt.key_press('f')

            elif self.current_state == ST.END_MOVETO_TREE:
                self.current_state = ST.INIT_ATTAIN_REAWARD

            elif self.current_state == ST.INIT_ATTAIN_REAWARD:
                self.current_state = ST.BEFORE_ATTAIN_REAWARD

            elif self.current_state == ST.BEFORE_ATTAIN_REAWARD:
                self.itt.key_press('f')
                time.sleep(0.2)
                if not generic_lib.f_recognition():
                    self.current_state = ST.IN_ATTAIN_REAWARD

            elif self.current_state == ST.IN_ATTAIN_REAWARD:
                self.Flow_IN_ATTAIN_REAWARD()

            elif self.current_state == ST.END_ATTAIN_REAWARD:
                self.current_state = ST.END_GETTING_REAWARD

            elif self.current_state == ST.END_GETTING_REAWARD:
                logger.info('秘境结束。')
                # logger.info('domain over. restart next domain in 5 sec.')
                self.current_state = ST.END_DOMAIN

            elif self.current_state == ST.END_DOMAIN:
                time.sleep(5)
                if self.checkup_stop_func():
                    break
                cap = self.itt.capture()
                cap = self.itt.png2jpg(cap, channel='ui')
                if self.last_domain_times >= 1:
                    logger.info('开始下一次秘境')
                    # logger.info('start next domain.')
                    self.last_domain_times -= 1

                    posi = pdocr_api.ocr.get_text_position(cap, textM.text(textM.conti_challenge))
                    if posi != -1:
                        self.itt.move_to(posi[0], posi[1] + 30)
                    else:
                        self.itt.move_to(0, 0)
                    time.sleep(0.5)
                    self.itt.left_click()
                    self.auto_start_init()
                    if self.checkup_stop_func():
                        break
                    time.sleep(5)
                    if self.checkup_stop_func():
                        break
                else:
                    logger.info('次数结束。退出秘境')
                    # logger.info('no more times. exit domain.')
                    posi = pdocr_api.ocr.get_text_position(cap, textM.text(textM.exit_challenge))
                    if posi != -1:
                        self.itt.move_to(posi[0], posi[1] + 30)
                    else:
                        self.itt.move_to(0, 0)
                    time.sleep(0.5)
                    self.itt.left_click()
                    # exit all threads
                    self.combat_loop.stop_threading()
                    self.stop_threading()
                    time.sleep(10)
                    break

    def get_tree_posi(self):
        cap = self.itt.capture(shape='xy')
        cap = self.itt.png2jpg(cap)
        # cv2.imshow('123',cap)
        # cv2.waitKey(0)
        addition_info, ret2 = yolox_api.yolo_tree.predicte(cap)
        # logger.debug(addition_info)
        if addition_info is not None:
            if addition_info[0][1][0] >= 0.5:
                tree_x, tree_y = yolox_api.yolo_tree.get_center(addition_info)
                return tree_x, tree_y
        return False

    def align_to_tree(self):
        movement.view_to_angle_domain(-90)
        t_posi = self.get_tree_posi()
        if t_posi:
            tx, ty = self.itt.get_mouse_point()
            dx = int(t_posi[0] - tx)
            logger.debug(dx)

            if dx >= 0:
                movement.move(movement.RIGHT, self.move_num)
            else:
                movement.move(movement.LEFT, self.move_num)
            if abs(dx) <= 20:
                self.lockOnFlag += 1
                self.move_num = 1
            return True
        else:
            self.move_num = 4
            return False


if __name__ == '__main__':

    # domain_times=configjson["domain_times"]
    dfc = DomainFlow()
    dfc.start()
    while 1:
        time.sleep(1)
