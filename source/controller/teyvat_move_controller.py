from source.util import *
from source.common.base_threading import BaseThreading
from source.interaction.minimap_tracker import tracker
from source.interaction.interaction_core import itt
from source.funclib import generic_lib, movement
from source.common import static_lib
from source.manager import asset
import numpy as np
from funclib.err_code_lib import ERR_PASS, ERR_STUCK
'''
提瓦特大陆移动辅助控制，包括：
自动F控制 pickup_operator
自动开伞检测 function: auto_wing
体力条检测 function: stamina_check
爬山检测 function: climb_check

auto_wing: climb_check
auto_wing True->space
stamina_check low-> press x left click

statement: in water; in climb; in move; in fly
'''


class TeyvatMoveController(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName("TeyvatMoveController")
        self.itt = itt
        self.priority_waypoints = load_json("priority_waypoints.json", default_path='assets')
        self.priority_waypoints_array = []
        for i in self.priority_waypoints:
            self.priority_waypoints_array.append(i["position"])
        self.priority_waypoints_array = np.array(self.priority_waypoints_array)
        self.target_positon = [0,0]
        self.while_sleep=0.5
        self.stop_rule = 0
    
    def set_target_position(self, posi):
        self.target_positon = posi    

    def set_parameter(self, target_positon):
        self.target_positon = target_positon

    def check_flying(self):
        if self.itt.get_img_existence(asset.IconGeneralMotionFlying):
            return True
        else:
            return False

    def set_stop_rule(self, mode=0):
        self.stop_rule = mode
    
    def check_climbing(self):
        if self.itt.get_img_existence(asset.IconGeneralMotionClimbing):
            return True
        else:
            return False

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.itt.key_up('w')
    
    def check_swimming(self):
        if self.itt.get_img_existence(asset.IconGeneralMotionSwimming):
            return True
        else:
            return False

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False
            if len(tracker.history_posi) != 0:
                tracker.history_posi = [tracker.history_posi[-1]]

    
    def caculate_next_priority_point(self, currentp, targetp):
        float_distance = 35
        # 计算当前点到所有优先点的曼哈顿距离
        md = manhattan_distance_plist(currentp, self.priority_waypoints_array)
        nearly_pp_arg = np.argsort(md)
        # 计算当前点到距离最近的50个优先点的欧拉距离
        nearly_pp = self.priority_waypoints_array[nearly_pp_arg[:50]]
        ed = euclidean_distance_plist(currentp, nearly_pp)
        # 将点按欧拉距离升序排序
        nearly_pp_arg = np.argsort(ed)
        nearly_pp = nearly_pp[nearly_pp_arg]
        # 删除距离目标比现在更远的点
        fd = euclidean_distance_plist(targetp, nearly_pp)
        c2t_distance = euclidean_distance(currentp, targetp)
        nearly_pp = np.delete(nearly_pp, (np.where(fd+float_distance >= (c2t_distance) )[0]), axis=0)
        # 获得最近点
        if len(nearly_pp) == 0:
            return targetp
        closest_pp = nearly_pp[0]
        '''加一个信息输出'''
        # print(currentp, closest_pp)
        return closest_pp
    
    
    def run(self) -> None:
        '''if you're using this class, copy this'''
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
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
                
            '''write your code below'''
            
            self.current_posi = tracker.get_position()
            p1 = self.caculate_next_priority_point(self.current_posi, self.target_positon)
            # print(p1)
            movement.change_view_to_posi(p1, self.checkup_stop_func)
            if (not static_lib.W_KEYDOWN) and (not self.pause_threading_flag):
                self.itt.key_down('w')
                
            if len(tracker.history_posi) >= 29:
                p1 = tracker.history_posi[0][1:]
                p2 = tracker.history_posi[-1][1:]
                if euclidean_distance(p1,p2)<=30:
                    logger.warning("检测到移动卡住，正在退出")
                    self.last_err_code = ERR_STUCK
                    self.pause_threading()
            
            if self.stop_rule == 0:
                if euclidean_distance(self.target_positon, tracker.get_position())<=10:
                    self.last_err_code = ERR_PASS
                    self.pause_threading()
                    logger.info(t2t("已到达目的地附近，本次导航结束。"))
                    self.itt.key_up('w')
            elif self.stop_rule == 1:
                if generic_lib.f_recognition():
                    self.last_err_code = ERR_PASS
                    self.pause_threading()
                    logger.info(t2t("已到达F附近，本次导航结束。"))
                    self.itt.key_up('w')
            
            

if __name__ == '__main__':
    tmc=TeyvatMoveController()
    p1=[3,3]
    tmc.set_parameter([1175.70934912 -4894.67981738])
    tmc.start()
    while 1:
        time.sleep(1)
        
    pass
                    
            
                 

                
                
            
        
    


