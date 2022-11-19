from unit import *
import math
import pyautogui
import flow_state as ST
from cvAutoTrack import cvAutoTracker
from interaction_background import InteractionBGD
import generic_lib
import img_manager
import interaction_background
import movement
import posi_manager
import text_manager
import timer_module
import big_map
import pdocr_api
from base_threading import BaseThreading


# from pdocr_api import ocr

def get_target_relative_angle(x, y, tx, ty):
    x = -x
    tx = -tx
    k = (ty - y) / (tx - x)
    degree = math.degrees(math.atan(k))
    if degree < 0:
        degree += 180
    if ty < y:
        degree += 180
    degree -= 90
    if degree > 180:
        degree -= 360
    return degree


class TeyvatMoveFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        self.itt = InteractionBGD()
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.target_posi = [0, 0]

    def align_position(self, tx, ty):
        b, x, y = cvAutoTracker.get_position()
        if b:
            angle = get_target_relative_angle(x, y, tx, ty)
            movement.view_to_angle_teyvat(angle)
            print(x, y, angle)
        return 0

    def switchto_mainwin(self):
        while not self.itt.get_img_existence(img_manager.ui_main_win):
            self.itt.key_press('m')
            time.sleep(1)

    def switchto_bigmapwin(self):
        while not self.itt.get_img_existence(img_manager.ui_bigmap_win):
            self.itt.key_press('m')
            time.sleep(1)

    def run(self):
        while 1:
            time.sleep(self.while_sleep)

            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
            '''write your code below'''

            if self.current_state == ST.INIT_TEYVAT_TELEPORT:
                '''切换到大世界界面'''
                '''设置缩放'''
                self.switchto_mainwin()
                self.current_state = ST.BEFORE_TEYVAT_TELEPORT

            if self.current_state == ST.BEFORE_TEYVAT_TELEPORT:
                '''切换到大世界界面'''
                self.switchto_mainwin()
                self.current_state = ST.IN_TEYVAT_TELEPORT

            if self.current_state == ST.IN_TEYVAT_TELEPORT:

                curr_posi = cvAutoTracker.get_position()[1:]
                self.switchto_bigmapwin()
                self.itt.delay(1)
                tw_posi = big_map.get_nearest_TW_posi_in_bigmap(curr_posi, self.target_posi)
                self.itt.move_to(tw_posi[0], tw_posi[1])
                self.itt.delay(0.2)
                self.itt.left_click()
                self.itt.delay(1)

                p1 = pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=0), "传送锚点")
                if p1 != -1:
                    self.itt.move_to(p1[0] + 30, p1[1] + 30)
                    self.itt.delay(1)
                    self.itt.left_click()
                    self.itt.delay(1)

                self.itt.move_to(posi_manager.tp_button[0], posi_manager.tp_button[1])
                self.itt.delay(1)
                self.itt.left_click()
                while not self.itt.get_img_existence(img_manager.ui_main_win):
                    time.sleep(0.1)
                self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                self.switchto_mainwin()
                time.sleep(2)
                curr_posi = cvAutoTracker.get_position()[1:]
                self.switchto_bigmapwin()
                tw_posi = big_map.get_nearest_TW_posi_in_teyvat(curr_posi, self.target_posi)[0]
                p1 = generic_lib.points_distance(self.target_posi, tw_posi)
                p2 = generic_lib.points_distance(self.target_posi, curr_posi)
                if p1 < p2:
                    self.switchto_mainwin()
                    self.itt.delay(1)
                    self.current_state = ST.BEFORE_TEYVAT_TELEPORT
                else:
                    self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                print()
                pass


if __name__ == '__main__':
    tmf = TeyvatMoveFlow()
    tmf.start()
    while 1:
        time.sleep(0.2)
# print(get_target_relative_angle(0,0,1,1))
