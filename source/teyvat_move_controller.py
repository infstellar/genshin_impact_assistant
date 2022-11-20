from util import *
from base_threading import BaseThreading
import img_manager
import generic_lib
from interaction_background import InteractionBGD
import posi_manager
import cvAutoTrack
import small_map
import movement

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

    def change_view(pl):
        x=pl[0]
        y=pl[1]
        tx, ty = cvAutoTrack.cvAutoTracker.get_position()[1:]
        td = cvAutoTrack.cvAutoTracker.get_rotation()[1]
        degree = generic_lib.points_angle([tx,ty], pl)
        movement.cview(td-degree)
        

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
        

                    
            
                 

                
                
            
        
    


