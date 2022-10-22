import time

import pyautogui

import cv2
import img_manager
from base_threading import Base_Threading
from interaction_background import Interaction_BGD
from timer_module import Timer
from unit import *

red_num = 245
BG_num = 100


class Aim_Operator(Base_Threading):
    def __init__(self):
        super().__init__()
        self.setName('Aim_Operator')
        self.itt = Interaction_BGD()
        self.loop_timer = Timer()
        autoaimjson = load_json("auto_aim.json")
        self.fps = 1 / autoaimjson["fps"]
        self.max_number_of_enemy_loops = autoaimjson["max_number_of_enemy_loops"]
        self.enemy_loops = 0
        self.enemy_flag = True
        self.reset_time = autoaimjson["reset_time"]
        self.reset_timer = Timer()

    def run(self):
        while (1):
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag == True:
                    self.working_flag = False
                time.sleep(1)
                continue

            if self.working_flag == False:
                self.working_flag = True

            t = self.loop_timer.loop_time()
            if t <= self.fps:
                time.sleep(self.fps - t)

            ret = self.auto_aim()
            if ret == 1:
                self.enemy_flag = False
                self.finding_enemy()
                if self.reset_timer.getDiffTime() >= self.reset_time:
                    self.reset_timer.reset()
                    self.reset_enemy_loops()

    def get_enemy_feature(self):
        if self.checkup_stop_func():
            return 0
        cap = self.itt.capture()
        imsrc = self.itt.png2jpg(cap, channel='ui', alpha_num=254)
        orsrc = cap.copy()
        cv2.cvtColor(orsrc, cv2.COLOR_BGR2RGB)

        imsrc[950:1080, :, :] = 0
        imsrc[0:150, :, :] = 0
        imsrc[:, 1600:1920, :] = 0

        imsrc[:, :, 2][imsrc[:, :, 2] < red_num] = 0
        imsrc[:, :, 2][imsrc[:, :, 0] > BG_num] = 0
        imsrc[:, :, 2][imsrc[:, :, 1] > BG_num] = 0
        _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
        # cv2.imshow('123',retimg)
        # cv2.waitKey(100)
        ret_point = img_manager.get_rect(imsrc2, orsrc, ret_mode=2)
        return ret_point

    def auto_aim(self):
        # time.sleep(0.1)
        if self.checkup_stop_func():
            return 0
        ret_points = self.get_enemy_feature()
        points_length = []
        if len(ret_points) == 0:
            return 1
        else:
            if self.enemy_flag == False:
                self.reset_enemy_loops()
                self.enemy_flag = True

        for point in ret_points:
            mx, my = self.itt.get_mouse_point()
            points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

        closest_point = ret_points[points_length.index(min(points_length))]
        px, py = closest_point
        mx, my = self.itt.get_mouse_point()
        px = (px - mx) / 4
        py = (py - my) / 4 + 35
        # print(px,py)

        self.itt.move_to(px, py, relative=True)
        # print()

    def finding_enemy(self):
        if self.enemy_loops < self.max_number_of_enemy_loops:
            pyautogui.middleClick()
        while self.enemy_loops < self.max_number_of_enemy_loops:
            if self.checkup_stop_func():
                return 0
            self.itt.move_to(50, 0, relative=True)
            ret_points = self.get_enemy_feature()
            if len(ret_points) != 0:
                self.reset_enemy_loops()
                return 0

            self.enemy_loops += 1

            # time.sleep(0.1)

    def reset_enemy_loops(self):
        self.enemy_loops = 0


if __name__ == '__main__':
    ao = Aim_Operator()
    ao.start()
