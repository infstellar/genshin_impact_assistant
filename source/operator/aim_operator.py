from source.funclib import movement, combat_lib
from source.manager import img_manager
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from common.timer_module import Timer
from source.util import *
from source.ui.ui import ui_control
from source.ui import page as UIPage


red_num = 245
BG_num = 100


class AimOperator(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName('Aim_Operator')
        self.itt = itt
        self.loop_timer = Timer()
        auto_aim_json = load_json("auto_aim.json")
        self.fps = 1 / auto_aim_json["fps"]
        self.fps = 5
        self.max_number_of_enemy_loops = auto_aim_json["max_number_of_enemy_loops"]
        self.auto_distance = auto_aim_json["auto_distance"]
        self.auto_distance = False
        self.auto_move = auto_aim_json["auto_move"]
        self.enemy_loops = 0
        self.enemy_flag = True
        self.reset_time = auto_aim_json["reset_time"]
        self.left_timer = Timer()
        self.reset_timer = Timer()
        self.kdwe_timer = Timer()
        self.corr_rate = 1

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            time.sleep(0.5)
            self.itt.key_up('a')
            self.itt.key_up('d')
    
    def run(self):
        while 1:
            time.sleep(0.1)
            # t = self.loop_timer.loop_time() # 设置最大检查时间
            # if t <= self.fps:
            #     time.sleep(self.fps - t)
            # logger.trace(f"cost time: {t} | {self.fps}")
                
            if self.stop_threading_flag:
                return

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
            
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            
            ret = self.auto_aim() # 自动瞄准
            if ret is None:
                return
            if ret == -1:
                self.enemy_flag = False # 没找到敌人
                self.finding_enemy() # 寻找敌人
                if self.reset_timer.get_diff_time() >= self.reset_time: # 重置检测次数
                    self.reset_timer.reset()
                    self.reset_enemy_loops()
            elif ret <= 30 and self.auto_distance:
                self.keep_distance_with_enemy() # 与敌人保持距离
            

    def get_enemy_feature(self, ret_mode=1):
        """获得敌人位置

        Args:
            ret_mode (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        if self.checkup_stop_func():
            return None
        cap = self.itt.capture()
        imsrc = self.itt.png2jpg(cap, channel='ui', alpha_num=254)
        # cv2.imshow("1231",imsrc)
        # cv2.waitKey(1)
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
        if ret_mode == 1: # 返回点坐标
            ret_point = img_manager.get_rect(imsrc2, orsrc, ret_mode=2)
            return ret_point
        elif ret_mode == 2: # 返回高度差
            ret_rect = img_manager.get_rect(imsrc2, orsrc, ret_mode=0)
            if ret_rect is None:
                return None
            return ret_rect[2] - ret_rect[0]

    def auto_aim(self):
        # time.sleep(0.1)
        if self.checkup_stop_func():
            return 0
        # combat_lib.chara_waiting(itt, stop_func = self.checkup_stop_func)
        if ui_control.verify_page(UIPage.page_main):
            ret_points = self.get_enemy_feature() # 获得敌方血条坐标
            if ret_points is None:
                return None
            points_length = []
            if len(ret_points) == 0:
                return -1
            else:
                if not self.enemy_flag:
                    self.reset_enemy_loops() # 如果有敌人，重置搜索敌人次数
                    self.enemy_flag = True

            for point in ret_points:
                mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
                points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

            closest_point = ret_points[points_length.index(min(points_length))] # 获得距离鼠标坐标最近的一个坐标
            px, py = closest_point
            mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
            px = (px - mx) / (2.4*self.corr_rate)
            py = (py - my) / (2*self.corr_rate) + 35 # 获得鼠标坐标偏移量
            # print(px,py)
            px=maxmin(px,200,-200)
            py=maxmin(py,200,-200)
            self.itt.move_to(px, py, relative=True)
            # logger.debug(f"auto_aim: x {px} y {py}")
            return px
            # print()

    def finding_enemy(self):
        if self.enemy_loops < self.max_number_of_enemy_loops:
            self.itt.middle_click() # 重置视角
            logger.debug(f" finding_enemy ")
        while self.enemy_loops < self.max_number_of_enemy_loops: # 当搜索敌人次数小于最大限制次数时，开始搜索
            if self.checkup_stop_func():
                return 0
            self.itt.move_to(150, 0, relative=True)
            ret_points = self.get_enemy_feature()
            if ret_points is None:
                return None
            if len(ret_points) != 0:
                self.reset_enemy_loops()
                return 0

            self.enemy_loops += 1

            # time.sleep(0.1)

    def reset_enemy_loops(self):
        self.enemy_loops = 0

    def keep_distance_with_enemy(self):  # 期望敌方血条像素高度为6px # 与敌人保持距离
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
                movement.move(movement.AHEAD, distance=target_px - px) # 
            elif px > target_px + 1:
                movement.move(movement.BACK, distance=px - target_px)

        # if self.auto_move: # 绕敌旋转
        #     if self.left_timer.get_diff_time() >= 15: # 每15秒重新按一次a
        #         if self.checkup_stop_func():
        #             self.itt.key_up('a')
        #             return 0
        #         self.itt.key_up('a')
        #         self.itt.key_down('a')
        #         self.left_timer.reset()


if __name__ == '__main__':
    ao = AimOperator()
    ao.start()
    # ao.get_enemy_feature(ret_mode=2)
    while 1:
        # ao.keep_distance_with_enemy()
        time.sleep(0.1)
