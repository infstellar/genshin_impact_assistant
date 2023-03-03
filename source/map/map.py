from source.map.detection.bigmap import BigMap
from source.map.detection.minimap import MiniMap
from source.util import *
from source.funclib import scene_lib
from source.interaction.interaction_core import itt
from source.map.data.teleporter import DICT_TELEPORTER
from source.manager import asset, posi_manager, scene_manager
from source.common import timer_module

class Map(MiniMap, BigMap):
    def __init__(self):
        MiniMap.__init__(self)
        BigMap.__init__(self)
        self._upd_smallmap()
        self._upd_bigmap()

    def _upd_smallmap(self):
        if scene_lib.get_current_pagename() == "main":
            self.update_position(itt.capture(jpgmode=0))

    def _upd_bigmap(self):
        if scene_lib.get_current_pagename() == "bigmap":
            self.update_bigmap(itt.capture(jpgmode=0))

    def get_smallmap_posi(self):
        self._upd_smallmap()
        return self.position

    def get_bigmap_posi(self):
        self._upd_bigmap()
        return self.bigmap

    def _move_bigmap(self, target_posi):
        """
        move bigmap center to target position
        """

        itt.left_down()
        itt.delay(0.2, comment="waiting genshin")
        curr_posi = self.get_bigmap_posi()
        dx = min( (curr_posi[0] - target_posi[0])*self.MAP_POSI2MOVE_POSI_RATE, 200)
        dx = max( (curr_posi[0] - target_posi[0])*self.MAP_POSI2MOVE_POSI_RATE, -200)
        dy = min( (curr_posi[1] - target_posi[1])*self.MAP_POSI2MOVE_POSI_RATE, 200)
        dy = max( (curr_posi[1] - target_posi[1])*self.MAP_POSI2MOVE_POSI_RATE, -200)

        logger.debug(f"_move_bigmap: {dx} {dy}")

        itt.move_to(dx, dy)
        itt.delay(0.2, comment="waiting genshin")
        itt.left_up()

        if euclidean_distance(self.get_bigmap_posi(), target_posi) <= self.BIGMAP_TP_OFFSET:
            return True
        else:
            itt.delay(0.2, comment="wait for a moment")
            self._move_bigmap(target_posi = target_posi)
    
    def _find_closest_teleporter(self, posi:list):
        """
        return closest teleporter position
        """
        min_dist = 99999
        min_point = [9999,9999]
        for i in DICT_TELEPORTER:
            if euclidean_distance(posi, DICT_TELEPORTER[i].position) < min_dist:
                min_point = DICT_TELEPORTER[i].position
        return min_point

    def tp2posi(self, posi:list, tp_mode = 0):
        """

        传送到指定坐标。
        模式: 
        0: 自动选择最近的可传送目标传送
        
        """
        if tp_mode == 0:
            tp_posi = self._find_closest_teleporter(posi)
        self._move_bigmap(tp_posi)
        if IS_DEVICE_PC:
            itt.move_and_click([1920/2, 1080/2]) # screen center
        else:
            itt.move_and_click([1024/2, 768/2])
        check_mode = 1
        temporary_timeout_1 = timer_module.TimeoutTimer(45)
        while 1:            
            if itt.appear_then_click(asset.bigmap_tp) : break
            if check_mode == 1:
                logger.debug("tp to tw")
                itt.appear_then_click(asset.CSMD)
            else:
                logger.debug("tp to ss")
                itt.appear_then_click(asset.QTSX)
            if temporary_timeout_1.istimeout():
                scene_lib.switch_to_page(scene_manager.page_bigmap, lambda:False)
                if IS_DEVICE_PC:
                    itt.move_and_click([1920/2, 1080/2]) # screen center
                else:
                    itt.move_and_click([1024/2, 768/2])
                temporary_timeout_1.reset()
            time.sleep(0.5)

        # itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
        
        while not (scene_lib.get_current_pagename() == "main"):
            time.sleep(1)
        
