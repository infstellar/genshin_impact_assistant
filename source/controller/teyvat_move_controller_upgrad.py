from source.util import *
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from source.funclib import generic_lib, movement
from source.common import static_lib
from source.manager import asset
from source.interaction.minimap_tracker import tracker
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
        self.following_points = []
        self.while_sleep=0.5
        self.stop_rule = 0
        self.point_index = 0
        self.posi_offset = 5
    
    def set_parameter(self, following_points, posi_offset = 5):
        self.following_points = following_points
        

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
            self._tp_to_closet_teleport()
            if len(tracker.history_posi) != 0:
                tracker.history_posi = [tracker.history_posi[-1]]

    
    def _is_arrive_current_point(self):
        curr_posi = tracker.get_position()
        if euclidean_distance(curr_posi, self.current_point) <= self.posi_offset:
            return True
        else:
            return False
    
    def _tp_to_closet_teleport(self, mode="Automatic"):
        """
        传送后再行走。
        
        mode: Automatic: 根据目标坐标距离远近自动决定是否传送。默认为目标坐标距离当前坐标超过50单位即传送。
              Never: 从不传送。
              Always: 始终传送。
        """
        pass

    def run(self) -> None:
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
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
                
            '''write your code below'''
            
            self.current_posi = tracker.get_position()
            

            if self._is_arrive_current_point():
                if not self.point_index == len(self.following_points):
                    self.point_index += 1

            p1 = self.following_points[self.point_index]

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
                if self.current_posi == self.current_posi[1:]:
                    if self._is_arrive_current_point():
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
    tmc.set_target_position([1175.70934912 -4894.67981738])
    tmc.start()
    while 1:
        time.sleep(1)
        
    pass
                    
            
                 

                
                
            
        
    


