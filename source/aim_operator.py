import time

import cv2
import pyautogui

import img_manager
import movement
from base_threading import BaseThreading
from interaction_background import InteractionBGD
from timer_module import Timer
from util import *

red_num = 245
BG_num = 100


class AimOperator(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName('Aim_Operator')
        self.itt = InteractionBGD()
        self.loop_timer = Timer()
        auto_aim_json = load_json("auto_aim.json")
        self.fps = 1 / auto_aim_json["fps"]
        self.max_number_of_enemy_loops = auto_aim_json["max_number_of_enemy_loops"]
        self.auto_distance = auto_aim_json["auto_distance"]
        self.auto_move = auto_aim_json["auto_move"]
        self.enemy_loops = 0
        self.enemy_flag = True
        self.reset_time = auto_aim_json["reset_time"]
        self.left_timer = Timer()
        self.reset_timer = Timer()
        self.kdwe_timer = Timer()

    def run(self):
        while 1:

            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True

            t = self.loop_timer.loop_time()
            if t <= self.fps:
                time.sleep(self.fps - t)

            ret = self.auto_aim()
            if ret == -1:
                self.enemy_flag = False
                self.finding_enemy()
                if self.reset_timer.get_diff_time() >= self.reset_time:
                    self.reset_timer.reset()
                    self.reset_enemy_loops()
            elif ret <= 30 and self.auto_distance:
                self.keep_distance_with_enemy()

    def get_enemy_feature(self, ret_mode=1):
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
        if ret_mode == 1:
            ret_point = img_manager.get_rect(imsrc2, orsrc, ret_mode=2)
            return ret_point
        elif ret_mode == 2:
            ret_rect = img_manager.get_rect(imsrc2, orsrc, ret_mode=0)
            if ret_rect is None:
                return None
            return ret_rect[2] - ret_rect[0]

    def auto_aim(self):
        # time.sleep(0.1)
        if self.checkup_stop_func():
            return 0
        ret_points = self.get_enemy_feature()
        points_length = []
        if len(ret_points) == 0:
            return -1
        else:
            if not self.enemy_flag:
                self.reset_enemy_loops()
                self.enemy_flag = True

        for point in ret_points:
            mx, my = self.itt.get_mouse_point()
            points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

        closest_point = ret_points[points_length.index(min(points_length))]
        px, py = closest_point
        mx, my = self.itt.get_mouse_point()
        px = (px - mx) / 2.4
        py = (py - my) / 2 + 35
        # print(px,py)

        self.itt.move_to(px, py, relative=True)
        return px
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

    def keep_distance_with_enemy(self):  # 10px
        target_px = 6
        if self.kdwe_timer.get_diff_time() < 1:
            return 0
        else:
            self.kdwe_timer.reset()
        if self.enemy_flag:
            px = self.get_enemy_feature(ret_mode=2)
            if px is None:
                return 0
            if px < target_px:
                movement.move(movement.AHEAD, distance=target_px - px)
            elif px > target_px + 1:
                movement.move(movement.BACK, distance=px - target_px)

        if self.auto_move:
            if self.left_timer.get_diff_time() >= 15:
                self.itt.key_up('a')
                self.itt.key_down('a')
                self.left_timer.reset()


if __name__ == '__main__':
    ao = AimOperator()
    ao.start()
    # ao.get_enemy_feature(ret_mode=2)
    while 1:
        # ao.keep_distance_with_enemy()
        time.sleep(0.1)
