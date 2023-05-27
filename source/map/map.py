from source.common import timer_module
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.interaction.interaction_core import itt
from source.manager import asset
from source.util import *
if GLOBAL_LANG == 'zh_CN':
    from source.map.data.teleporter_zh_CN import DICT_TELEPORTER
elif GLOBAL_LANG == 'en_US':
    from source.map.data.teleporter_en_US import DICT_TELEPORTER
from source.map.detection.bigmap import BigMap
from source.map.detection.minimap import MiniMap
from source.map.extractor.convert import MapConverter
from source.map.position.position import *

import threading

REGION_TEYVAT = [
    "Inazuma",
    "Liyue",
    "Mondstadt",
    "Sumeru"
]
COORDINATE_TIANLI = "TianLi"
COORDINATE_GIMAP = "GIMAP"
COORDINATE_KONGYING = "KongYing"


class Map(MiniMap, BigMap, MapConverter):
    def __init__(self):
        if IS_DEVICE_PC:
            super().__init__(device_type=MiniMap.DETECT_Desktop_1080p)
        else:
            super().__init__(device_type=MiniMap.DETECT_Mobile_720p)

        # Set bigmap tp arguments
        self.MAP_POSI2MOVE_POSI_RATE = 0.2  # 移动距离与力度的比例
        self.BIGMAP_TP_OFFSET = 100  # 距离目标小于该误差则停止
        self.BIGMAP_MOVE_MAX = 130  # 最大移动力度
        self.TP_RANGE = 350  # 在该像素范围内可tp
        self.MINIMAP_UPDATE_LIMIT = 0.1  # minimap更新最短时间

        self.smallmap_upd_timer = timer_module.Timer(2)
        self.small_map_init_flag = False
        self.lock = threading.Lock()
        self.check_bigmap_timer = timer_module.Timer(5)
        self.init_timer = timer_module.AdvanceTimer(5)

    def _upd_smallmap(self) -> None:
        # self.lock.acquire()
        if itt.get_img_existence(asset.IconUIEmergencyFood, is_log=False):
            self.update_position(itt.capture(jpgmode=0))
        # self.lock.release()

    def _upd_bigmap(self) -> None:
        # self.lock.acquire()
        if ui_control.verify_page(UIPage.page_bigmap):
            self.update_bigmap(itt.capture(jpgmode=0))
        # self.lock.release()

    def get_and_verify_position(self):
        """Not in use

        Returns:
            None
        """
        # print(self.check_bigmap_timer.get_diff_time())
        curr_posi = self.get_position()
        if self.check_bigmap_timer.get_diff_time()<5:
            offset_rate = min(1, (self.check_bigmap_timer.get_diff_time())*0.1+0.5)
        else:
            offset_rate=1
        print(offset_rate, 5-self.check_bigmap_timer.get_diff_time())
        if not self.is_similarity_qualified(offset_rate):
            logger.error(f"Please waiting, similarity too low.")
            logger.info(f"{self.position_similarity} {self.position_similarity_local}")
            i=0
            itt.freeze_key('w', 'up')
            while 1:
                time.sleep(0.05)
                curr_posi = self.get_position()
                if i>=20:
                    logger.warning(f"fail to get minimap position, try using bigmap instead.")
                    ui_control.ensure_page(UIPage.page_bigmap)
                    pp = self.get_bigmap_posi()
                    curr_posi = pp.tianli
                    logger.info(f"init_position:{pp.gimap}")
                    self.init_position(tuple(map(int, list(pp.gimap))))
                    logger.info(f"position: {curr_posi}")
                    ui_control.ensure_page(UIPage.page_main)
                    break
                if self.is_similarity_qualified():
                    logger.info(f"Continue.")
                    break
                i+=1
            itt.unfreeze_key('w')
            self.check_bigmap_timer.reset()
        # print(self.check_bigmap_timer.get_diff_time())
        return curr_posi
    
    def get_position(self):
        """get current character position

        Returns:
            list: TianLiPosition format
        """
        if not self.small_map_init_flag:
            self.reinit_smallmap()
            self.small_map_init_flag = True
        # if self.smallmap_upd_timer.get_diff_time() >= self.MINIMAP_UPDATE_LIMIT:
        self._upd_smallmap()
        #     self.smallmap_upd_timer.reset()
        return self.convert_GIMAP_to_cvAutoTrack(self.position)

    def is_similarity_qualified(self, offset_rate=1):
        return self.position_similarity>=0.4*offset_rate and self.position_similarity_local>=0.05*offset_rate
    
    def reinit_smallmap(self) -> None:
        if ui_control.verify_page(UIPage.page_main):
            if self.init_timer.reached_and_reset():
                ui_control.ui_goto(UIPage.page_bigmap)
                logger.info(f"init_position:{self.get_bigmap_posi().gimap}")
                self.init_position(tuple(map(int, list(self.get_bigmap_posi().gimap))))
                ui_control.ui_goto(UIPage.page_main)
                self.small_map_init_flag = True
            else:
                logger.info(f"init too fast, skip")

    def get_smallmap_from_teleporter(self, area=None):
        if area == None:
            area = ['Inazuma',"Liyue","Mondstadt"]
        rlist = []
        rd = []
        added = []
        for md in range(10,60,10):
            logger.info(f"d: {md}")
            for i in DICT_TELEPORTER:
                tper = DICT_TELEPORTER[i]
                if not tper.region in area:
                    continue
                
                # logger.info(f"init_position:{tper.position}")
                self.init_position(tper.position)
                self.get_position()
                d = euclidean_distance(self.get_position(), self.convert_GIMAP_to_cvAutoTrack(tper.position))
                if d<=md:
                    if tper in added:
                        continue
                    rlist.append(tper)
                    rd.append(d)
                    logger.info(f"id {len(rlist)-1} position {tper.position} {tper.name} {tper.region}, d={d}")
                    added.append(tper)
        
        return rlist, rd         
        # self.init_position(tuple(list(map(int,max_position))))
        # logger.info(f"init_smallmap_from_teleporter:{max_n} {max_position} {max_tper.name}")

    def while_until_no_excessive_error(self) -> None:
        self.reinit_smallmap()

    def get_direction(self) -> float:
        imsrc = cv2.cvtColor(itt.capture(jpgmode=0),cv2.COLOR_BGR2RGB)
        # self.lock.acquire()
        self.update_direction(imsrc)
        # self.lock.release()
        # print(self.direction)
        return self.direction
    
    def get_rotation(self) -> float:
        # self.lock.acquire()
        pt = time.time()
        self.update_rotation(itt.capture(jpgmode=0))
        if time.time()-pt>0.1:
            logger.info(f"get_rotation spent too long: {time.time()-pt}")
        # print(self.direction)
        # self.lock.release()
        return self.rotation

    def check_bigmap_scaling(self) -> None:
        if not itt.get_img_existence(asset.IconBigMapScaling):
            origin_page = ui_control.get_page()
            while not itt.appear_then_click(asset.ButtonBigmapSwitchMap): itt.delay(0.2)
            itt.delay("animation")
            while not itt.appear_then_click(asset.MapAreaCYJY): itt.delay(0.2)
            itt.delay("animation")
            while not itt.appear_then_click(asset.ButtonBigmapSwitchMap): itt.delay(0.2)
            itt.delay("animation")
            while not itt.appear_then_click(asset.MapAreaLY): itt.delay(0.2)
            itt.delay("animation")
            if origin_page == UIPage.page_main:
                ui_control.ui_goto(UIPage.page_main)
            elif origin_page == UIPage.page_bigmap:
                ui_control.ui_goto(UIPage.page_main)
                ui_control.ui_goto(UIPage.page_bigmap)
    
    def get_bigmap_posi(self, is_upd=True) -> GIMAPPosition:
        self.check_bigmap_scaling()
        if is_upd:
            self._upd_bigmap()
        logger.debug(f"bigmap posi: {self.convert_GIMAP_to_cvAutoTrack(self.bigmap)}")
        return GIMAPPosition(self.bigmap)


    def _move_bigmap(self, target_posi, float_posi=0, force_center = False, csf=lambda:False) -> list:
        """move bigmap center to target position

        Args:
            target_posi (_type_): 目标坐标
            float_posi (int, optional): 如果点到了什么东东导致移动失败，自动增加该值. Defaults to 0.

        Returns:
            _type_: _description_
        """

        """需要处理的异常：

        1. 点击到某个东西弹出右侧弹框
        2. 点击到一坨按键弹出一坨东西
        
        警告：此函数为内部函数，不要在外部调用。如果一定要调用应先设置地图缩放。
        
        """
        if IS_DEVICE_PC:
            screen_center_x = 1920 / 2
            screen_center_y = 1080 / 2
        else:
            screen_center_x = 1024 / 2
            screen_center_y = 768 / 2

        if csf():
            return
        
        itt.move_to(screen_center_x + float_posi, screen_center_y + float_posi)  # screen center

        itt.left_down()
        if IS_DEVICE_PC:
            for i in range(5):  # 就是要这么多次(
                itt.move_to(10, 10, relative=True)
                if i % 2 == 0:
                    itt.left_down()
            for i in range(5):
                itt.move_to(-10, -10, relative=True)
                if i % 2 == 0:
                    itt.left_down()
        
        curr_posi = self.get_bigmap_posi().tianli
        dx = min((curr_posi[0] - target_posi[0]) * self.MAP_POSI2MOVE_POSI_RATE, self.BIGMAP_MOVE_MAX)
        dx = max(dx, -self.BIGMAP_MOVE_MAX)
        dy = min((curr_posi[1] - target_posi[1]) * self.MAP_POSI2MOVE_POSI_RATE, self.BIGMAP_MOVE_MAX)
        dy = max(dy, -self.BIGMAP_MOVE_MAX)

        logger.debug(f"curr: {curr_posi} target: {target_posi}")
        logger.debug(f"_move_bigmap: {dx} {dy}")

        itt.move_to(dx, dy, relative=True)
        itt.delay(0.2, comment="waiting genshin")
        itt.left_up()
        # if itt.get_img_existence(asset.confirm):
        # itt.key_press('esc')

        after_move_posi = self.get_bigmap_posi().tianli
        if not force_center:
            if euclidean_distance(self.convert_cvAutoTrack_to_InGenshinMapPX(after_move_posi),
                                self.convert_cvAutoTrack_to_InGenshinMapPX(target_posi)) <= self.TP_RANGE:
                return list(
                    (self.convert_cvAutoTrack_to_InGenshinMapPX(target_posi))
                    -  # type: ignore
                    (self.convert_cvAutoTrack_to_InGenshinMapPX(after_move_posi))
                    +
                    np.array([screen_center_x, screen_center_y])
                )

        if euclidean_distance(self.get_bigmap_posi(is_upd=False).tianli, target_posi) <= self.BIGMAP_TP_OFFSET:
            if IS_DEVICE_PC:
                return list([1920 / 2, 1080 / 2])  # screen center
            else:
                return list([1024 / 2, 768 / 2])
        else:
            itt.delay(0.2, comment="wait for a moment")
            if euclidean_distance(self.get_bigmap_posi(is_upd=False).tianli, curr_posi) <= self.BIGMAP_TP_OFFSET:
                return self._move_bigmap(target_posi=target_posi, float_posi=float_posi + 45)
            else:
                return self._move_bigmap(target_posi=target_posi)

    def _find_closest_teleporter(self, posi: list, regions=REGION_TEYVAT, tp_type: list = None):
        """
        return closest teleporter position: 
        
        input: TianLi format position;
        return: GIMAP format position.
        """
        if tp_type is None:
            tp_type = ["Teleporter", "Statue", "Domain"]
        min_dist = 99999
        min_teleporter = None
        for i in DICT_TELEPORTER:
            if (DICT_TELEPORTER[i].region in regions) and (DICT_TELEPORTER[i].tp in tp_type):
                i_posi = self.convert_GIMAP_to_cvAutoTrack(DICT_TELEPORTER[i].position)
                i_dist = euclidean_distance(posi, i_posi)
                if i_dist < min_dist:
                    min_teleporter = DICT_TELEPORTER[i]
                    min_dist = i_dist
        return min_teleporter

    def _switch_to_area(self, tp_region):
        while 1:
            time.sleep(0.1)
            itt.appear_then_click(asset.ButtonBigmapSwitchMap)
            if not itt.get_img_existence(asset.IconUIBigmap): break
        itt.delay('animation')
        if tp_region == "Mondstadt":
            while not itt.appear_then_click(asset.MapAreaMD): itt.delay(0.2)
        elif tp_region == "Liyue":
            while not itt.appear_then_click(asset.MapAreaLY): itt.delay(0.2)
        elif tp_region == "Inazuma":
            while not itt.appear_then_click(asset.MapAreaDQ): itt.delay(0.2)
        elif tp_region == "Sumeru":
            while not itt.appear_then_click(asset.MapAreaXM): itt.delay(0.2)
        itt.delay('animation')
        while 1:
            time.sleep(0.1)
            if itt.get_img_existence(asset.IconUIBigmap): break
            itt.appear_then_click(asset.ButtonBigmapCloseMarkTableInTP)
        itt.delay('animation')

    def bigmap_tp(self, posi: list, tp_mode=0, tp_type: list = None, csf=lambda:False) -> TianLiPosition:
        """传送到指定坐标。

        Args:
            posi (list): _description_
            tp_mode (int, optional): 0: 自动选择最近的可传送目标传送. Defaults to 0.
            tp_type (list, optional): _description_. Defaults to None.
            csf (_type_, optional): checkup stop func. Defaults to lambda:False.

        Returns:
            TianLiPosition: _description_
        """
        if tp_type == None:
            tp_type = ["Teleporter", "Statue", "Domain"]
        ui_control.ui_goto(UIPage.page_bigmap)
        if tp_mode == 0:
            target_teleporter = self._find_closest_teleporter(posi, tp_type=tp_type)
        tp_posi = self.convert_GIMAP_to_cvAutoTrack(target_teleporter.position)
        tp_type = target_teleporter.tp
        tp_region = target_teleporter.region

        self.check_bigmap_scaling()

        self._switch_to_area(tp_region)

        click_posi = self._move_bigmap(tp_posi, csf=csf)

        if tp_type == "Domain": # 部分domain有特殊名字
            logger.debug("tp to Domain")
            itt.appear_then_click(asset.ButtonBigmapSwitchDomainModeOn)
            itt.delay(0.2)
            # 点一下“仅查看秘境”
        else:
            itt.appear_then_click(asset.ButtonBigmapSwitchDomainModeOff)

        

        tp_timeout_1 = timer_module.TimeoutTimer(15)
        tp_timeout_1.reset()
        tp_timeout_2 = timer_module.TimeoutTimer(5)
        tp_timeout_2.reset()
        
        if not (itt.get_text_existence(asset.CSMD) or itt.get_text_existence(asset.QTSX) or itt.get_img_existence(asset.ButtonBigmapTP)):
            itt.move_and_click(click_posi)
        
        while 1:
            if itt.appear_then_click(asset.ButtonBigmapTP): break
            
            if tp_type == "Teleporter":
                logger.debug("tp to Teleporter")
                r = itt.appear_then_click(asset.CSMD)
            elif tp_type == "Statue":
                logger.debug("tp to Statue")
                r = itt.appear_then_click(asset.QTSX)
            else:
                # itt.appear_then_click(asset.ButtonSwitchDomainModeOn)
                r = False
            if (not r) and tp_timeout_2.istimeout():
                itt.move_and_click(click_posi)
                tp_timeout_2.reset()
            if tp_timeout_1.istimeout():
                ui_control.ui_goto(UIPage.page_bigmap)
                itt.move_and_click(click_posi)
                tp_timeout_1.reset()
            time.sleep(0.5)

        # itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)

        while not (ui_control.get_page() == UIPage.page_main):
            time.sleep(0.2)

        self.reinit_smallmap()
        
        return TianLiPosition(tp_posi)


genshin_map = Map()
logger.info(f"genshin map object created")

if __name__ == '__main__':
    # genshin_map.bigmap_tp(genshin_map.convert_GIMAP_to_cvAutoTrack([6642.003, 5485.38]),
    #                       tp_type=["Domain"])  # tp to *染之庭
    genshin_map.reinit_smallmap()
    while 1:
        time.sleep(0.2)
        # input()
        # itt.key_down('w')
        print(genshin_map.get_and_verify_position())
    
