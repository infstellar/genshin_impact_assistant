from source.util import *
import math
from source.constant import flow_state as ST
from source.base import timer_module
from funclib import big_map, movement, static_lib, combat_lib
from source.manager import scene_manager, posi_manager, asset
from source.interaction.interaction_core import global_itt
from source.controller import teyvat_move_controller
from source.common.base_threading import BaseThreading
from funclib.err_code_lib import ERR_PASS, ERR_STUCK
from source.funclib import scene_lib
from source.common import generic_event
from source.flow.flow_template import FlowConnector, FlowController, FlowTemplate

IN_MOVE = 0
IN_FLY = 1
IN_WATER = 2
IN_CLIMB = 3


class TeyvatMoveFlowConnector(FlowConnector):
    def __init__(self):
        self.tmc = teyvat_move_controller.TeyvatMoveController()
        self.target_posi = None
        self.checkup_stop_func = None



class TeyvatTeleport(FlowTemplate):
    def __init__(self, upper:TeyvatMoveFlowConnector):
        super().__init__(upper)
        self.upper = upper

    def state_init(self):
        scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
        self.upper.tmc.set_target_position(self.upper.target_posi)
        self._next_rfc()

    def state_before(self):
        scene_lib.switch_to_page(scene_manager.page_main, self.upper.checkup_stop_func)
        self._next_rfc()

    def state_in(self):
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
                scene_lib.switch_to_page(scene_manager.page_bigmap, self.checkup_stop_func)
                self.itt.move_and_click([tw_posi[0], tw_posi[1]])
                temporary_timeout_1.reset()
            time.sleep(1)
            # p1 = pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=0, posi=img_manager.bigmap_choose_area.cap_posi), "七天神像", cap_posi_leftup=img_manager.bigmap_choose_area.cap_posi[:2])
            # if p1 != -1:
            #     self.itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)
            
            # p1 = pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=0, posi=img_manager.bigmap_choose_area.cap_posi), "传送锚点", cap_posi_leftup=img_manager.bigmap_choose_area.cap_posi[:2])
            # if p1 != -1:
            #     self.itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)

        self.itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
        
        while not self.itt.get_img_existence(asset.ui_main_win):
            if self.checkup_stop_func():
                break
            time.sleep(1)
        while generic_event.cvAutoTrackerLoop.in_excessive_error:
            if self.checkup_stop_func():
                break
            time.sleep(1)
        self.current_state = ST.AFTER_TEYVAT_TELEPORT
