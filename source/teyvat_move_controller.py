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

    def check_swimming(self):
        if self.itt.get_img_existence(img_manager.motion_swimming):
            return True
        else:
            return False

    def change_view_to_posi(self, pl):
        x=pl[0]
        y=pl[1]
        td=0
        degree=100
        while abs(td-degree)>10:
            tx, ty = cvAutoTrack.cvAutoTracker.get_position()[1:]
            td = cvAutoTrack.cvAutoTracker.get_rotation()[1]
            degree = generic_lib.points_angle([tx,ty], pl)
            movement.cview(td-degree)
    
    def caculate_next_priority_point(self, currentp, targetp):
        # 计算当前点到所有优先点的曼哈顿距离
        md = generic_lib.manhattan_distance_plist(currentp, self.priority_waypoints_array)
        nearly_pp_arg = np.argsort(md)
        # 计算当前点到所有优先点的欧拉距离
        nearly_pp = self.priority_waypoints_array[nearly_pp_arg[:9]]
        ed = generic_lib.euclidean_distance_plist(currentp, nearly_pp)
        # 将点按欧拉距离升序排序
        nearly_pp_arg = np.argsort(ed)
        nearly_pp = nearly_pp[nearly_pp_arg]
        # 删除距离目标比现在更远的点
        fd = generic_lib.euclidean_distance_plist(targetp, nearly_pp)
        c2t_distance = generic_lib.euclidean_distance(currentp, targetp)
        nearly_pp = np.delete(nearly_pp, (np.where(fd>=c2t_distance)[0]), axis=0)
        # 获得最近点
        if len(nearly_pp) == 0:
            return targetp
        closest_pp = nearly_pp[0]
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
        

if __name__ == '__main__':
    tmc=TeyvatMoveController()
    p1=[3,3]
    for i in range(10):
        p1 = tmc.caculate_next_priority_point(p1, [0,0])
        print(p1)
    pass
                    
            
                 

                
                
            
        
    


