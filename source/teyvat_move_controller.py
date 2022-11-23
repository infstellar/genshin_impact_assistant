from util import *
from base_threading import BaseThreading
import img_manager
import generic_lib
from interaction_background import InteractionBGD
import posi_manager
import cvAutoTrack
import small_map
import movement
import numpy as np
import static_lib
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
        self.itt = InteractionBGD()
        self.priority_waypoints = load_json("priority_waypoints.json", default_path='assests')
        self.priority_waypoints_array = []
        for i in self.priority_waypoints:
            self.priority_waypoints_array.append(i["position"])
        self.priority_waypoints_array = np.array(self.priority_waypoints_array)
        self.target_positon = [0,0]
        self.while_sleep=0.5
    
    def set_target_position(self, posi):
        self.target_positon = posi    

    def check_flying(self):
        if self.itt.get_img_existence(img_manager.motion_flying):
            return True
        else:
            return False

    def check_climbing(self):
        if self.itt.get_img_existence(img_manager.motion_climbing):
            return True
        else:
            return False

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.itt.key_up('w')
    
    def check_swimming(self):
        if self.itt.get_img_existence(img_manager.motion_swimming):
            return True
        else:
            return False

    
    
    def caculate_next_priority_point(self, currentp, targetp):
        float_distance = 30
        # 计算当前点到所有优先点的曼哈顿距离
        md = generic_lib.manhattan_distance_plist(currentp, self.priority_waypoints_array)
        nearly_pp_arg = np.argsort(md)
        # 计算当前点到所有优先点的欧拉距离
        nearly_pp = self.priority_waypoints_array[nearly_pp_arg[:50]]
        ed = generic_lib.euclidean_distance_plist(currentp, nearly_pp)
        # 将点按欧拉距离升序排序
        nearly_pp_arg = np.argsort(ed)
        nearly_pp = nearly_pp[nearly_pp_arg]
        # 删除距离目标比现在更远的点
        fd = generic_lib.euclidean_distance_plist(targetp, nearly_pp)
        c2t_distance = generic_lib.euclidean_distance(currentp, targetp)
        nearly_pp = np.delete(nearly_pp, (np.where(fd+float_distance >= (c2t_distance) )[0]), axis=0)
        # 获得最近点
        if len(nearly_pp) == 0:
            return targetp
        closest_pp = nearly_pp[0]
        '''加一个信息输出'''
        # print(currentp, closest_pp)
        return closest_pp
    
    
    def run(self):
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
            '''write your code below'''
            self.current_posi = cvAutoTrack.cvAutoTrackerLoop.get_position()
            if not self.current_posi[0]==False:
                self.current_posi=self.current_posi[1:]
            else:
                logger.debug("position ERROR")
                continue
            p1 = self.caculate_next_priority_point(self.current_posi, self.target_positon)
            # print(p1)
            movement.change_view_to_posi(p1)
            if not static_lib.W_KEYDOWN:
                self.itt.key_down('w')
                
            if generic_lib.euclidean_distance(self.target_positon, cvAutoTrack.cvAutoTrackerLoop.get_position()[1:])<=10:
                self.pause_threading()
                logger.info("已到达目的地附近，本次导航结束。")
                self.itt.key_up('w')
            
            

if __name__ == '__main__':
    tmc=TeyvatMoveController()
    p1=[3,3]
    tmc.set_target_position([1175.70934912 -4894.67981738])
    tmc.start()
    while 1:
        time.sleep(1)
        
    pass
                    
            
                 

                
                
            
        
    


