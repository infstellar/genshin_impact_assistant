from util import *
from base_threading import BaseThreading
import img_manager
import generic_lib
from interaction_background import InteractionBGD
import posi_manager
from pickup_operator import PickupOperator
import combat_lib
import combat_loop

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

IN_MOVE = 0
IN_FLY = 1
IN_WATER = 2
IN_CLIMB = 3


class TeyvatMoveController(BaseThreading):
    def __init__(self):
        super().__init__()
        self.puo = PickupOperator()
        self.puo.setDaemon(True)
        self.puo.pause_threading()
        self.puo.start()

        chara_list = combat_loop.get_chara_list()
        self.combat_loop = combat_loop.Combat_Controller(chara_list)
        self.combat_loop.setDaemon(True)
        self.combat_loop.pause_threading()
        self.combat_loop.start()

        self.itt = InteractionBGD()

        self.statement = IN_MOVE
        self.is_combat = False

    def pause_threading(self):
        self.puo.pause_threading()
        self.pause_threading_flag = True

    def continue_threading(self):
        self.puo.continue_threading()
        self.pause_threading_flag = False

    def stop_threading(self):
        self.puo.stop_threading()
        self.stop_threading_flag = True

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

    def switch_statement(self):
        if self.check_climbing():
            self.statement = IN_CLIMB
        elif self.statement == IN_CLIMB:
            self.statement = IN_MOVE

        if self.check_flying():
            self.statement = IN_FLY
        elif self.statement == IN_FLY:
            self.statement = IN_MOVE

        if self.check_swimming():
            self.statement = IN_WATER
        elif self.statement == IN_WATER:
            self.statement = IN_MOVE

    def run(self):
        while 1:
            time.sleep(0.2)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True

            if combat_lib.combat_statement_detection(self.itt):
                self.is_combat = True
            else:
                self.is_combat = False

            if self.is_combat:
                if self.combat_loop.pause_threading_flag:
                    self.combat_loop.continue_threading()
                if not self.puo.pause_threading_flag:
                    self.puo.pause_threading()

            else:
                self.switch_statement()
                if not self.combat_loop.pause_threading_flag:
                    self.combat_loop.pause_threading()       
                # if self.puo.pause_threading_flag:
                #     self.puo.continue_threading()
                    
            
                 

                
                
            
        
    


