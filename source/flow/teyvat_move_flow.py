from source.util import *
import math
from common import flow_state as ST, timer_module
from funclib import big_map, movement, combat_lib
from source.manager import scene_manager, posi_manager, asset
from source.interaction.interaction_core import itt
from source.controller import teyvat_move_controller
from source.common.base_threading import BaseThreading
from funclib.err_code_lib import ERR_PASS, ERR_STUCK
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.interaction.minimap_tracker import tracker
from source.ui.ui import ui_control
import source.ui.page as UIPage

IN_MOVE = 0
IN_FLY = 1
IN_WATER = 2
IN_CLIMB = 3

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
        self.setName("TeyvatMoveFlow")
        self.itt = itt
        self.stop_rule = 0
        self.tmc = teyvat_move_controller.TeyvatMoveController()
        self.tmc.setDaemon(True)
        self.tmc.add_stop_func(self.checkup_stop_func)
        self.tmc.pause_threading()
        self.tmc.start()
        self.tmc.set_stop_rule(self.stop_rule)
        
        
        self.jump_timer = timer_module.Timer()
        
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.target_posi = [0, 0]
        
        self.reaction_to_enemy = 'RUN'
        self.motion_state = IN_MOVE
        
        '''设置缩放'''
        reset_map_size_timer = timer_module.FileTimer("reset_map_size_timer")
        if reset_map_size_timer.get_diff_time()>=120:
            ui_control.ui_goto(UIPage.page_bigmap)
            big_map.reset_map_size()
            ui_control.ui_goto(UIPage.page_main)
            reset_map_size_timer.reset()
        # self.is_combat = False

    
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.tmc.pause_threading()
            self.itt.key_up('w')

    def continue_threading(self):
        self.pause_threading_flag = False

    def stop_threading(self):
        self.stop_threading_flag = True
        self.tmc.stop_threading()
    
    def reset_setting(self):
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.motion_state = IN_MOVE
    
    def align_position(self, tx, ty):
        x, y = tracker.get_position()
        angle = get_target_relative_angle(x, y, tx, ty)
        movement.change_view_to_angle(angle, self.checkup_stop_func)
        # print(x, y, angle)
    
    def set_stop_rule(self, mode=0):
        self.stop_rule = mode
        self.tmc.set_stop_rule(self.stop_rule)

    def switch_motion_state(self):
        if self.itt.get_img_existence(asset.motion_climbing):
            self.motion_state = IN_CLIMB
        elif self.itt.get_img_existence(asset.motion_flying):
            self.motion_state = IN_FLY
        elif self.itt.get_img_existence(asset.motion_swimming):
            self.motion_state = IN_WATER
        else:
            self.motion_state = IN_MOVE
    
    def set_target_position(self, pl):
        self.target_posi = pl
        # print()
    
    def run(self):
        while 1:
            time.sleep(self.while_sleep)

            if self.stop_threading_flag:
                logger.info(t2t("停止自动移动"))
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

            if self.current_state == ST.INIT_TEYVAT_TELEPORT:
                
                '''切换到大世界界面'''
                ui_control.ui_goto(UIPage.page_main)
                self.tmc.set_parameter(self.target_posi)
                self.current_state = ST.BEFORE_TEYVAT_TELEPORT

            if self.current_state == ST.BEFORE_TEYVAT_TELEPORT:
                '''切换到大世界界面'''
                ui_control.ui_goto(UIPage.page_main)
                self.current_state = ST.IN_TEYVAT_TELEPORT

            if self.current_state == ST.IN_TEYVAT_TELEPORT:
                curr_posi = tracker.get_position()
                ui_control.ui_goto(UIPage.page_bigmap)
                # Obtain the coordinates of the transmission anchor closest to the target coordinates
                tw_posi = big_map.nearest_big_map_tw_posi(curr_posi, self.target_posi, self.checkup_stop_func, include_gs=True) # 获得距离目标坐标最近的传送锚点坐标 
                tw_posi2 = big_map.nearest_big_map_tw_posi(curr_posi, self.target_posi, self.checkup_stop_func, include_gs=False) # 获得距离目标坐标最近的传送锚点坐标 
                if list(tw_posi) != list(tw_posi2):
                    check_mode = 0 # Statues of the seven
                else:
                    check_mode = 1 # Teleport Waypoint
                if len(tw_posi)==0:
                    logger.info(t2t("获取传送锚点失败，正在重试"))
                    big_map.reset_map_size()
                    self.current_state = ST.IN_TEYVAT_TELEPORT
                    continue
                self.itt.move_and_click([tw_posi[0], tw_posi[1]])
                # self.itt.delay(0.2)
                # self.itt.left_click()
                # self.itt.delay(0.6)
                temporary_timeout_1 = timer_module.TimeoutTimer(25)
                while 1:
                    if self.checkup_stop_func():
                        break
                    
                    if self.itt.appear_then_click(asset.bigmap_tp) : break
                    if check_mode == 1:
                        logger.debug("tp to tw")
                        self.itt.appear_then_click(asset.CSMD)
                    else:
                        logger.debug("tp to ss")
                        self.itt.appear_then_click(asset.QTSX)
                    if temporary_timeout_1.istimeout():
                        ui_control.ui_goto(UIPage.page_bigmap)
                        self.itt.move_and_click([tw_posi[0], tw_posi[1]])
                        temporary_timeout_1.reset()
                    time.sleep(1)

                self.itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
                
                while not self.itt.get_img_existence(asset.ui_main_win):
                    if self.checkup_stop_func():
                        break
                    time.sleep(1)
                while tracker.in_excessive_error:
                    if self.checkup_stop_func():
                        break
                    time.sleep(1)
                self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                ui_control.ui_goto(UIPage.page_main)
                time.sleep(2)
                curr_posi = tracker.get_position()
                ui_control.ui_goto(UIPage.page_bigmap)
                tw_posi = big_map.nearest_teyvat_tw_posi(curr_posi, self.target_posi, self.checkup_stop_func)
                p1 = euclidean_distance(self.target_posi, tw_posi)
                p2 = euclidean_distance(self.target_posi, curr_posi)
                if p1 < p2:
                    ui_control.ui_goto(UIPage.page_main)
                    self.itt.delay(1)
                    self.current_state = ST.BEFORE_TEYVAT_TELEPORT
                else:
                    self.current_state = ST.AFTER_TEYVAT_TELEPORT

            if self.current_state == ST.AFTER_TEYVAT_TELEPORT:
                ui_control.ui_goto(UIPage.page_main)
                self.current_state = ST.END_TEYVAT_TELEPORT
            if self.current_state == ST.END_TEYVAT_TELEPORT:
                self.current_state = ST.INIT_TEYVAT_MOVE
            if self.current_state == ST.INIT_TEYVAT_MOVE:
                self.tmc.continue_threading()
                self.current_state = ST.IN_TEYVAT_MOVE
                
            if self.current_state == ST.IN_TEYVAT_MOVE:
                self.switch_motion_state()
                
                if self.motion_state == IN_MOVE:
                    if combat_lib.CSDL.get_combat_state():
                        '''进入战斗模式'''
                        if self.reaction_to_enemy == 'RUN':
                            '''越级执行护盾命令 还没想好怎么写'''
                            # shield_chara_num = 2
                            # self.cct.sco._switch_character(shield_chara_num)
                            # self.cct.sco.tactic_operator.set_parameter(self.cct.sco.chara_list[shield_chara_num-1].tactic_group, self.cct.sco.chara_list[shield_chara_num-1])
                            # self.cct.sco.tactic_operator.continue_threading()
                            pass
                        else:
                            self.tmc.pause_threading()
                    else:
                        self.tmc.continue_threading()
                        if self.jump_timer.get_diff_time()>=2:
                            self.jump_timer.reset()
                            self.itt.key_press('spacebar')
                            time.sleep(0.3)
                            self.itt.key_press('spacebar') # fly
                    
                    
                        
                if (self.motion_state == IN_FLY) or (self.motion_state == IN_CLIMB) or (self.motion_state == IN_WATER):
                    self.tmc.continue_threading()
                    
                if self.motion_state == IN_CLIMB:
                    if self.jump_timer.get_diff_time()>=5:
                        self.jump_timer.reset()
                        self.itt.key_press('spacebar')
                        time.sleep(0.3)
                        self.itt.key_press('spacebar') # fly    
                
                    '''可能会加体力条检测'''
                # if self.stop_rule == 0:    
                #     if euclidean_distance(tracker.get_position(), self.target_posi)<=10:
                #         self.current_state = ST.END_TEYVAT_MOVE
                # elif self.stop_rule == 1:
                #     if generic_lib.f_recognition():
                #         self.current_state = ST.END_TEYVAT_MOVE
                # elif self.
                
                if self.tmc.get_last_err_code() == ERR_PASS:
                    self.tmc.reset_err_code()
                    self.last_err_code = ERR_PASS
                    self.current_state = ST.END_TEYVAT_MOVE
                elif self.tmc.get_last_err_code() == ERR_STUCK:
                    self.tmc.reset_err_code()
                    self.last_err_code = ERR_STUCK
                    self.current_state = ST.END_TEYVAT_MOVE
                
            if self.current_state == ST.END_TEYVAT_MOVE:
                self.pause_threading()
                if self.motion_state == IN_FLY:
                    logger.info(t2t("正在落地"))
                    self.itt.left_click()
                logger.info(t2t("结束自动行走"))
                time.sleep(1)
                    
                    

if __name__ == '__main__':
    tmf = TeyvatMoveFlow()
    tmf.set_target_position([1175.70934912, -4894.67981738])
    tmf.start()
    while 1:
        time.sleep(0.2)
# print(get_target_relative_angle(0,0,1,1))
