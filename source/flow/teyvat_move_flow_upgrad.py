from source.util import *
import math
from source.constant import flow_state as ST
import source.flow.flow_code as FC
from source.base import timer_module
from funclib import big_map, movement, static_lib, combat_lib
from source.manager import scene_manager, posi_manager, asset
from source.interaction.interaction_core import global_itt
from source.controller import teyvat_move_controller
from source.common.base_threading import BaseThreading
from funclib.err_code_lib import ERR_PASS, ERR_STUCK, ERR_NONE
from source.funclib import scene_lib
from source.common import generic_event
from source.flow.flow_template import FlowConnector, FlowController, FlowTemplate

IN_MOVE = 0
IN_FLY = 1
IN_WATER = 2
IN_CLIMB = 3


class TeyvatMoveFlowConnector(FlowConnector):
    def __init__(self):
        super().__init__()
        self.tmc = teyvat_move_controller.TeyvatMoveController()
        self.target_posi = None
        self.checkup_stop_func = None
        self.stop_rule = 0
        self.tmc.set_stop_rule(self.stop_rule)
        self.jump_timer = timer_module.Timer()
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.target_posi = [0, 0]
        self.reaction_to_enemy = 'RUN'
        self.motion_state = IN_MOVE
        self.last_err_code = ERR_NONE
    
    def reset(self):
        self.tmc.reset_err_code()
        self.last_err_code = ERR_NONE
        self.target_posi = None
        self.current_state = ST.INIT_TEYVAT_TELEPORT
        self.target_posi = [0, 0]
        self.motion_state = IN_MOVE

    

    

class TeyvatTeleport(FlowTemplate):
    def __init__(self, upper:TeyvatMoveFlowConnector):
        super().__init__(upper)
        self.upper = upper
        self.flow_id = ST.INIT_TEYVAT_TELEPORT
        self.next_flow_id = ST.INIT_TEYVAT_MOVE

    def state_init(self):
        self.upper.tmc.set_target_position(self.upper.target_posi)
        self._next_rfc()

    def state_before(self):
        scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
        self._next_rfc()

    def state_in(self):
        """
        这个代码是垃圾 之后大地图坐标识别模块接入之后要重写
        """
        curr_posi = generic_event.cvAutoTrackerLoop.get_position()[1:]
        scene_lib.switch_to_page(scene_manager.page_bigmap, self.upper.checkup_stop_func)
        # Obtain the coordinates of the transmission anchor closest to the target coordinates
        tw_posi = big_map.nearest_big_map_tw_posi(curr_posi, self.upper.target_posi, self.upper.checkup_stop_func, include_gs=True) # 获得距离目标坐标最近的传送锚点坐标 
        tw_posi2 = big_map.nearest_big_map_tw_posi(curr_posi, self.upper.target_posi, self.upper.checkup_stop_func, include_gs=False) # 获得距离目标坐标最近的传送锚点坐标 
        if list(tw_posi) != list(tw_posi2):
            check_mode = 0 # Statues of the seven
        else:
            check_mode = 1 # Teleport Waypoint
        if len(tw_posi)==0:
            logger.info(t2t("获取传送锚点失败，正在重试"))
            big_map.reset_map_size()
        global_itt.move_and_click([tw_posi[0], tw_posi[1]])
        # global_itt.delay(0.2)
        # global_itt.left_click()
        # global_itt.delay(0.6)
        temporary_timeout_1 = timer_module.TimeoutTimer(25)
        while 1:
            if self.upper.checkup_stop_func():
                break
            
            if global_itt.appear_then_click(asset.bigmap_tp) : break
            if check_mode == 1:
                logger.debug("tp to tw")
                global_itt.appear_then_click(asset.CSMD)
            else:
                logger.debug("tp to ss")
                global_itt.appear_then_click(asset.QTSX)
            if temporary_timeout_1.istimeout():
                scene_lib.switch_to_page(scene_manager.page_bigmap, self.upper.checkup_stop_func)
                global_itt.move_and_click([tw_posi[0], tw_posi[1]])
                temporary_timeout_1.reset()
            time.sleep(0.5)
            # p1 = pdocr_api.ocr.get_text_position(global_itt.capture(jpgmode=0, posi=img_manager.bigmap_choose_area.cap_posi), "七天神像", cap_posi_leftup=img_manager.bigmap_choose_area.cap_posi[:2])
            # if p1 != -1:
            #     global_itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)
            
            # p1 = pdocr_api.ocr.get_text_position(global_itt.capture(jpgmode=0, posi=img_manager.bigmap_choose_area.cap_posi), "传送锚点", cap_posi_leftup=img_manager.bigmap_choose_area.cap_posi[:2])
            # if p1 != -1:
            #     global_itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)

        global_itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
        
        while not global_itt.get_img_existence(asset.ui_main_win):
            if self.upper.checkup_stop_func():
                break
            time.sleep(1)
        while generic_event.cvAutoTrackerLoop.in_excessive_error:
            if self.upper.checkup_stop_func():
                break
            time.sleep(1)
        self._next_rfc()

    def state_after(self):
        """也是垃圾"""
        scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
        time.sleep(2)
        curr_posi = generic_event.cvAutoTrackerLoop.get_position()[1:]
        scene_lib.switch_to_page(scene_manager.page_bigmap, self.upper.checkup_stop_func)
        tw_posi = big_map.nearest_teyvat_tw_posi(curr_posi, self.upper.target_posi, self.upper.checkup_stop_func)
        p1 = euclidean_distance(self.upper.target_posi, tw_posi)
        p2 = euclidean_distance(self.upper.target_posi, curr_posi)
        if p1 < p2:
            scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
            global_itt.delay(1)
            self.rfc = FC.BEFORE
        else:
            self._next_rfc()

    def state_end(self):
        scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
        return super().state_end()
class TeyvatMove(FlowTemplate):
    def __init__(self, upper: TeyvatMoveFlowConnector):
        super().__init__(upper)
        self.upper = upper
        self.flow_id = ST.INIT_TEYVAT_MOVE
        self.next_flow_id = ST.END

    def switch_motion_state(self):
        if global_itt.get_img_existence(asset.motion_climbing):
            self.motion_state = IN_CLIMB
        elif global_itt.get_img_existence(asset.motion_flying):
            self.motion_state = IN_FLY
        elif global_itt.get_img_existence(asset.motion_swimming):
            self.motion_state = IN_WATER
        else:
            self.motion_state = IN_MOVE



    def state_init(self):
        self.upper.tmc.continue_threading()
        return super().state_init()

    def state_in(self):
        self.switch_motion_state()
        
        if self.motion_state == IN_MOVE:
            if combat_lib.combat_statement_detection(global_itt):
                '''进入战斗模式'''
                if self.upper.reaction_to_enemy == 'RUN':
                    '''越级执行护盾命令 还没想好怎么写'''
                    pass
                else:
                    self.upper.tmc.pause_threading()
            else:
                self.upper.tmc.continue_threading()
                if self.upper.jump_timer.get_diff_time()>=2:
                    self.upper.jump_timer.reset()
                    global_itt.key_press('spacebar')
                    time.sleep(0.3)
                    global_itt.key_press('spacebar') # fly
            
            
                
        if (self.motion_state == IN_FLY) or (self.motion_state == IN_CLIMB) or (self.motion_state == IN_WATER):
            self.upper.tmc.continue_threading()
            
        if self.motion_state == IN_CLIMB:
            if self.upper.jump_timer.get_diff_time()>=5:
                self.upper.jump_timer.reset()
                global_itt.key_press('spacebar')
                time.sleep(0.3)
                global_itt.key_press('spacebar') # fly    

            '''可能会加体力条检测'''
        # if self.stop_rule == 0:    
        #     if euclidean_distance(generic_event.cvAutoTrackerLoop.get_position()[1:], self.target_posi)<=10:
        #         self.current_state = ST.END_TEYVAT_MOVE
        # elif self.stop_rule == 1:
        #     if generic_lib.f_recognition():
        #         self.current_state = ST.END_TEYVAT_MOVE
        # elif self.

        if self.upper.tmc.get_last_err_code() == ERR_PASS:
            self.upper.tmc.reset_err_code()
            self.upper.last_err_code = ERR_PASS
            self._next_rfc()
        elif self.upper.tmc.get_last_err_code() == ERR_STUCK:
            self.upper.tmc.reset_err_code()
            self.upper.last_err_code = ERR_STUCK
            self._next_rfc()

class TeyvatMoveFlowController(FlowController):
    def __init__(self):
        super().__init__()
        self.current_flow_id = ST.INIT_TEYVAT_TELEPORT
        
        self.flow_connector = TeyvatMoveFlowConnector()
        self.flow_connector.checkup_stop_func = self.checkup_stop_func
        self._add_sub_threading(self.flow_connector.tmc)
        self.get_while_sleep = self.flow_connector.get_while_sleep

        self.f1 = TeyvatTeleport(self.flow_connector)
        self.f2 = TeyvatMove(self.flow_connector)

        self.append_flow(self.f1)
        self.append_flow(self.f2)

    
    def set_target_posi(self, tp:list):
        self.flow_connector.target_posi = tp
        
    def set_stop_rule(self, r:int):
        """设置停止条件

        Args:
            r (int): 0: 距离目的地小于10. 1:识别到F后停止。
        """
        self.flow_connector.stop_rule = r

