from util import *
import math
import flow_state as ST
import cvAutoTrack
from interaction_background import InteractionBGD
import teyvat_move_controller
import generic_lib
import img_manager
import pickup_operator
import movement
import posi_manager
import big_map
import combat_loop
import pdocr_api
from base_threading import BaseThreading
import pyautogui
import interaction_background
import text_manager
import timer_module
import combat_lib

IN_MOVE = 0
IN_FLY = 1
IN_WATER = 2
IN_CLIMB = 3
# from pdocr_api import ocr

def get_target_relative_angle(x, y, tx, ty):
    x = -x
    tx = -tx
    k = (ty - y) / (tx - x)
    degree = math.degrees(math.atan(k))
    if degree < 0:
        degree += 180
    if ty < y:
        degree += 180
    degree -= 90
    if degree > 180:
        degree -= 360
    return degree

     

class TeyvatMoveFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        self.itt = InteractionBGD()
        
        self.tmc = teyvat_move_controller.TeyvatMoveController()
        self.tmc.setDaemon(True)
        self.tmc.pause_threading()
        self.tmc.start()
        

        chara_list = combat_loop.get_chara_list()
        self.cct = combat_loop.Combat_Controller(chara_list)
        self.cct.setDaemon(True)
        self.cct.pause_threading()
        self.cct.start()
        
        self.jump_timer = timer_module.Timer()
        
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.target_posi = [0, 0]
        
        self.motion_state = IN_MOVE
        self.is_combat = False

    
    def pause_threading(self):
        self.pause_threading_flag = True

    def continue_threading(self):
        self.pause_threading_flag = False

    def stop_threading(self):
        self.stop_threading_flag = True
    
    def align_position(self, tx, ty):
        b, x, y = cvAutoTrack.cvAutoTrackerLoop.get_position()
        if b:
            angle = get_target_relative_angle(x, y, tx, ty)
            movement.view_to_angle_teyvat(angle)
            print(x, y, angle)
        return 0

    def switchto_mainwin(self):
        while not self.itt.get_img_existence(img_manager.ui_main_win):
            self.itt.key_press('m')
            time.sleep(1)

    def switchto_bigmapwin(self):
        while not self.itt.get_img_existence(img_manager.ui_bigmap_win):
            self.itt.key_press('m')
            time.sleep(1)

    def switch_motion_state(self):
        if self.itt.get_img_existence(img_manager.motion_climbing):
            self.motion_state = IN_CLIMB
        elif self.itt.get_img_existence(img_manager.motion_flying):
            self.motion_state = IN_FLY
        elif self.itt.get_img_existence(img_manager.motion_swimming):
            self.motion_state = IN_WATER
        else:
            self.motion_state = IN_MOVE
    
    def set_target_posi(self, pl):
        self.target_posi = pl
        print()
    
    def run(self):
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

            if self.current_state == ST.INIT_TEYVAT_TELEPORT:
                '''切换到大世界界面'''
                '''设置缩放'''
                self.switchto_mainwin()
                self.tmc.set_target_position(self.target_posi)
                self.current_state = ST.BEFORE_TEYVAT_TELEPORT

            if self.current_state == ST.BEFORE_TEYVAT_TELEPORT:
                '''切换到大世界界面'''
                self.switchto_mainwin()
                self.current_state = ST.IN_TEYVAT_TELEPORT

            if self.current_state == ST.IN_TEYVAT_TELEPORT:

                curr_posi = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
                self.switchto_bigmapwin()
                self.itt.delay(1)
                tw_posi = big_map.nearest_big_map_tw_posi(curr_posi, self.target_posi)
                self.itt.move_to(tw_posi[0], tw_posi[1])
                self.itt.delay(0.2)
                self.itt.left_click()
                self.itt.delay(1)

                p1 = pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=0), "传送锚点")
                if p1 != -1:
                    self.itt.move_to(p1[0] + 30, p1[1] + 30)
                    self.itt.delay(1)
                    self.itt.left_click()
                    self.itt.delay(1)

                self.itt.move_to(posi_manager.tp_button[0], posi_manager.tp_button[1])
                self.itt.delay(1)
                self.itt.left_click()
                while not self.itt.get_img_existence(img_manager.ui_main_win):
                    time.sleep(1)
                while cvAutoTrack.cvAutoTrackerLoop.in_excessive_error:
                    time.sleep(1)
                self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                self.switchto_mainwin()
                time.sleep(2)
                curr_posi = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
                self.switchto_bigmapwin()
                tw_posi = big_map.nearest_teyvat_tw_posi(curr_posi, self.target_posi)[0]
                p1 = generic_lib.euclidean_distance(self.target_posi, tw_posi)
                p2 = generic_lib.euclidean_distance(self.target_posi, curr_posi)
                if p1 < p2:
                    self.switchto_mainwin()
                    self.itt.delay(1)
                    self.current_state = ST.BEFORE_TEYVAT_TELEPORT
                else:
                    self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                self.switchto_mainwin()
                self.current_state = ST.END_TEYVAT_TELEPORT
            if self.current_state == ST.END_TEYVAT_TELEPORT:
                self.current_state = ST.INIT_TEYVAT_MOVE
            if self.current_state == ST.INIT_TEYVAT_MOVE:
                self.tmc.continue_threading()
                self.current_state = ST.IN_TEYVAT_MOVE
                
            if self.current_state == ST.IN_TEYVAT_MOVE:
                self.switch_motion_state()
                
                if self.motion_state == IN_MOVE:
                    if combat_lib.combat_statement_detection(self.itt):
                        '''进入战斗模式'''
                        self.tmc.pause_threading()
                        self.cct.continue_threading()
                        self.cct.pause_threading()
                    else:
                        self.cct.pause_threading()
                        self.tmc.continue_threading()
                        if self.jump_timer.get_diff_time()>=15:
                            self.jump_timer.reset()
                            self.itt.key_press('spacebar')
                        
                if (self.motion_state == IN_FLY) or (self.motion_state == IN_CLIMB) or (self.motion_state == IN_WATER):
                    self.cct.pause_threading()
                    self.tmc.continue_threading()
                    '''可能会加体力条检测'''
                    
                if generic_lib.euclidean_distance(cvAutoTrack.cvAutoTrackerLoop.get_position()[1:], self.target_posi)<=10:
                    self.current_state = ST.END_TEYVAT_MOVE
                    
            if self.current_state == ST.END_TEYVAT_MOVE:
                self.pause_threading()
                print("结束自动行走")
                time.sleep(1)
                    
                    

if __name__ == '__main__':
    tmf = TeyvatMoveFlow()
    tmf.set_target_posi([1175.70934912, -4894.67981738])
    tmf.start()
    while 1:
        time.sleep(0.2)
# print(get_target_relative_angle(0,0,1,1))
