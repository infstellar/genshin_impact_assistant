from source.funclib import movement, combat_lib
from source.manager import img_manager
from source.common.base_threading import BaseThreading, ThreadBlockingRequest
from source.interaction.interaction_core import itt
from common.timer_module import Timer,AdvanceTimer
from source.util import *
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.map.map import genshin_map


red_num = 245
BG_num = 100


"""
先找敌人
如果找到：锁定
找不到：搜索
搜不到：二段搜索

"""
class AimOperator(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName('AimOperator')
        self.itt = itt
        self.loop_timer = Timer()
        # self.fps = 1 / auto_aim_json["fps"]
        self.fps = 5
        # self.max_number_of_enemy_loops = auto_aim_json["max_number_of_enemy_loops"]
        self.auto_distance = False
        # self.auto_move = auto_aim_json["auto_move"]
        self.enemy_loops = 0
        self.enemy_flag = True
        # self.reset_time = auto_aim_json["reset_time"]
        # self.left_timer = Timer()
        # self.reset_timer = Timer()
        self.kdwe_timer = Timer()
        self.circle_search_timer = AdvanceTimer(4,count=3).start() # call 3 times and continue 4 sec.
        self.keep_distance_timer = AdvanceTimer(3,count=3).start()
        self.aim_timeout_retry_timer = AdvanceTimer(6).start()
        self.corr_rate = 1
        self.sco_blocking_request = ThreadBlockingRequest()

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
            
            if self.enemy_flag == False:
                if combat_lib.CSDL.get_combat_state():
                    self.enemy_flag = True
            else: # 处于战斗状态
                r = self._lock_on_enemy() # 锁定敌人
                if self.checkup_stop_func():continue
                if not r: # 没有找到血条
                    r = self._circle_find_enemy() # 转圈寻找
                    if self.checkup_stop_func():continue
                    if r: # 找到了，退出
                        self.enemy_flag = True
                    else: # 没找到，根据红色箭头移动寻找
                        if self.checkup_stop_func():continue
                        if not self.aim_timeout_retry_timer.reached(): continue # 超时后6秒内不寻找
                        self.sco_blocking_request.send_request('_moving_find_enemy') # 向SCO申请暂停Tactic执行
                        if True: # set to False when debug this module
                            print(self.sco_blocking_request.waiting_until_reply(stop_func=self.checkup_stop_func, timeout=60))
                        r = self._moving_find_enemy()
                        self.sco_blocking_request.recovery_request() # 解除申请
                        if not r:
                            if self.checkup_stop_func():continue
                            if not self._is_in_combat(times=3):
                                logger.debug(f"AimOperator: No enemy exist.")
                                self.enemy_flag = False
                else:
                    if self._is_enemy_too_far(): # 敌人是否太远
                        if self.checkup_stop_func():continue
                        if self.keep_distance_timer.reached_and_reset():
                            self.sco_blocking_request.send_request('_keep_distance_with_enemy')
                            if True: # set to False when debug this module
                                print(self.sco_blocking_request.waiting_until_reply(stop_func=self.checkup_stop_func, timeout=60))
                            self._keep_distance_with_enemy()
                            self.sco_blocking_request.recovery_request() # 解除申请
                    else:
                        self.keep_distance_timer.reset()
            
            # ret = self.auto_aim() # 自动瞄准
            # if ret is None:
            #     return
            # if ret == -1:
            #     self.enemy_flag = False # 没找到敌人
            #     self.finding_enemy() # 寻找敌人
            #     if self.reset_timer.get_diff_time() >= self.reset_time: # 重置检测次数
            #         self.reset_timer.reset()
            #         self.reset_enemy_loops()
            # elif ret <= 30 and self.auto_distance:
            #     self.keep_distance_with_enemy() # 与敌人保持距离
            

    def _lock_on_enemy(self):
        ret_points = self.get_enemy_feature() # 获得敌方血条坐标
        if ret_points is None:
            return False
        points_length = []
        if len(ret_points) == 0:
            return False
        else:
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
            return True
    
    def _circle_find_enemy(self):
        if self.circle_search_timer.reached_and_reset():
            logger.debug(f"circle_search_timer reached, skip")
            return False
        else:
            movement.reset_view() # 重置视角
            logger.debug(f" finding_enemy ")
        # while self.enemy_loops < self.max_number_of_enemy_loops: # 当搜索敌人次数小于最大限制次数时，开始搜索
        for i in range(15):
            if i%4==0:
                if self.checkup_stop_func():return
            combat_lib.chara_waiting(self.checkup_stop_func)
            movement.cview(15)
            ret_points = self.get_enemy_feature()
            if ret_points is None:
                continue
            if len(ret_points) != 0:
                # self._reset_enemy_loops()
                if self._is_blood_bar_exist():
                    self.circle_search_timer.reset()
                    return True
                

            # self.enemy_loops += 1
        return False
   
    def _is_blood_bar_exist(self):
        t = AdvanceTimer(1)
        logger.debug("_is_blood_bar_exist")
        while 1:
            time.sleep(0.2)
            if self.checkup_stop_func():return
            if not combat_lib.combat_statement_detection()[0]:
                return False
            if t.reached():
                return True
    
    def _is_in_combat(self, times=1):
        for ii in range(times):
            for i in range(40):
                if i%8==0:
                    if self.checkup_stop_func():return
                movement.cview(12)
                r = combat_lib.combat_statement_detection()
                if r[0] or r[1]:
                    return True
            return False
    
    def _moving_find_enemy(self):
        # enemy_possible_rotation = []
        # origin_rotation = genshin_map.get_rotation()
        # for i in range(100):
        #     movement.cview(8, rate=1)
        #     rotation = genshin_map.get_rotation()
        #     if i>=10:
        #         if abs(movement.calculate_delta_angle(rotation, origin_rotation))<=8:
        #             break
        #     # itt.move_to(50,0,relative=True)
        #     r = combat_lib.combat_statement_detection()
        #     if not r[1]:
        #         enemy_possible_rotation.append(rotation)
        #         print(rotation)
        # if len(enemy_possible_rotation) == 0:
        #     return False
        # if len(enemy_possible_rotation) == i:
        #     return False
        # target_rotation1 = enemy_possible_rotation[(len(enemy_possible_rotation)-1)//2]
        # target_rotation2 = sum(enemy_possible_rotation)/len(enemy_possible_rotation)
        # movement.change_view_to_angle(target_rotation1)
        logger.debug(f"_moving_find_enemy start.")
        movement.reset_view()
        if not self._is_in_combat():
            logger.debug(f"no enemy exist, break")
            return False
        while 1:
            # move view to blood bar exist or arrow no exist, where is the enemy located.
            if self.checkup_stop_func():return
            movement.cview(20)
            # itt.delay(0.1)
            r = combat_lib.combat_statement_detection()
            if r[0] or not r[1]:
                break
        
        itt.key_down('w')
        move_timer = AdvanceTimer(15).start()
        move_timer.start()
        combat_lib.CSDL.freeze_state()
        while 1:
            time.sleep(0.1)
            if self.checkup_stop_func():
                itt.key_up('w')
                combat_lib.CSDL.unfreeze_state()
                return
            if move_timer.reached():
                itt.key_up('w')
                combat_lib.CSDL.unfreeze_state()
                self.aim_timeout_retry_timer.reset()
                logger.debug(f"_moving_find_enemy timeout")
                return False
            if combat_lib.combat_statement_detection()[0]:
                itt.key_up('w')
                if self._is_blood_bar_exist():
                    logger.info(f"_moving_find_enemy: found enemy succ")
                    logger.info(f"_moving_find_enemy: move to enemy closer")
                    r = self._keep_distance_with_enemy()
                    if r:
                        itt.key_up('w')
                        combat_lib.CSDL.unfreeze_state()
                        return True
                    else:
                        logger.info(f"_moving_find_enemy: refind enemy: 2")
                        itt.key_up('w')
                        combat_lib.CSDL.unfreeze_state()
                        return self._moving_find_enemy()
                else:
                    itt.key_down('w')
            if combat_lib.combat_statement_detection()[1]:
                itt.key_up('w')
                logger.info(f"_moving_find_enemy: refind enemy")
                combat_lib.CSDL.unfreeze_state()
                return self._moving_find_enemy()
        combat_lib.CSDL.unfreeze_state()
        return True    
        
                
    
    def get_enemy_feature(self, ret_mode=1):
        """获得敌人位置

        Args:
            ret_mode (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        cap = self.itt.capture()
        orsrc = cap.copy()
        imsrc = combat_lib.get_enemy_blood_bar_img(cap)
        _, imsrc2 = cv2.threshold(imsrc, 1, 255, cv2.THRESH_BINARY)
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

    # def auto_aim(self):
        # # time.sleep(0.1)
        # if self.checkup_stop_func():
        #     return 0
        # # combat_lib.chara_waiting(stop_func = self.checkup_stop_func)
        # if ui_control.verify_page(UIPage.page_main):
        #     ret_points = self.get_enemy_feature() # 获得敌方血条坐标
        #     if ret_points is None:
        #         return None
        #     points_length = []
        #     if len(ret_points) == 0:
        #         return -1
        #     else:
        #         if not self.enemy_flag:
        #             self.reset_enemy_loops() # 如果有敌人，重置搜索敌人次数
        #             self.enemy_flag = True

        #     for point in ret_points:
        #         mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
        #         points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

        #     closest_point = ret_points[points_length.index(min(points_length))] # 获得距离鼠标坐标最近的一个坐标
        #     px, py = closest_point
        #     mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
        #     px = (px - mx) / (2.4*self.corr_rate)
        #     py = (py - my) / (2*self.corr_rate) + 35 # 获得鼠标坐标偏移量
        #     # print(px,py)
        #     px=maxmin(px,200,-200)
        #     py=maxmin(py,200,-200)
        #     self.itt.move_to(px, py, relative=True)
        #     # logger.debug(f"auto_aim: x {px} y {py}")
        #     return px
            # print()

    # def finding_enemy(self):
    #     if self.enemy_loops < self.max_number_of_enemy_loops:
    #         movement.reset_view() # 重置视角
    #         logger.debug(f" finding_enemy ")
    #     while self.enemy_loops < self.max_number_of_enemy_loops: # 当搜索敌人次数小于最大限制次数时，开始搜索
    #         if self.checkup_stop_func():
    #             return 0
    #         self.itt.move_to(150, 0, relative=True)
    #         ret_points = self.get_enemy_feature()
    #         if ret_points is None:
    #             return False
    #         if len(ret_points) != 0:
    #             self._reset_enemy_loops()
    #             return True

    #         self.enemy_loops += 1

    #         # time.sleep(0.1)

    def _reset_enemy_loops(self):
        self.enemy_loops = 0
        self.enemy_flag = True

    def _is_enemy_too_far(self):
        px = self.get_enemy_feature(ret_mode=2)
        if px is None:
            return False
        return px < 6
    
    def _keep_distance_with_enemy(self):  # 期望敌方血条像素高度为7px # 与敌人保持距离
        target_px = 7
        if self.enemy_flag:
            px = self.get_enemy_feature(ret_mode=2)
            if px is None:
                return False
            if px < target_px:
                itt.key_down('w')
                while 1:
                    time.sleep(0.05)
                    if self.checkup_stop_func(): 
                        itt.key_up('w')
                        return False
                    px = self.get_enemy_feature(ret_mode=2)
                    if px is None: 
                        itt.key_up('w')
                        return False
                    if px >= target_px: 
                        itt.key_up('w')
                        return True
            else:
                return True

        # if self.auto_move: # 绕敌旋转
        #     if self.left_timer.get_diff_time() >= 15: # 每15秒重新按一次a
        #         if self.checkup_stop_func():
        #             self.itt.key_up('a')
        #             return 0
        #         self.itt.key_up('a')
        #         self.itt.key_down('a')
        #         self.left_timer.reset()


if __name__ == '__main__':
    # movement.change_view_to_angle(0, angle_function=combat_lib.get_enemy_arrow_direction)
    ao = AimOperator()
    ao._keep_distance_with_enemy()
    # ao.start()
    # ao.get_enemy_feature(ret_mode=2)
    while 1:
        # ao.keep_distance_with_enemy()
        time.sleep(1)
        ao._keep_distance_with_enemy()