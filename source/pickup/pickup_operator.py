from source.common.base_threading import BaseThreading
from source.util import *
from source.interaction.interaction_core import itt
from source.api.pdocr_complete import ocr
from common import timer_module, static_lib
from source.funclib import generic_lib, movement
from source.manager import img_manager, asset
import cv2
from source.interaction.minimap_tracker import tracker
from source.assets.pickup import *

SEARCH_MODE_FINDING = 1
SEARCH_MODE_PICKUP = 0

class PickupOperator(BaseThreading):

    def __init__(self):
        super().__init__()
        self.setName("PickupOperator")
        self.itt = itt
        self.pickup_blacklist = GIAconfig.Collector_PickupBlacklist
        self.pickup_blacklist += load_json("auto_pickup_default_blacklist.json", default_path=fr"{ASSETS_PATH}")["blacklist"]
        self.pickup_blacklist = list(set(self.pickup_blacklist))
        self.pickup_item_list = []
        self.flicker_timer = timer_module.Timer(diff_start_time=1)
        self.reset_timer = timer_module.Timer()
        self.reset_time = 120
        self.collector_loops = 0
        self.collector_flag = True
        self.max_number_of_collector_loops = 35
        self.pickup_timer = timer_module.Timer()
        self.pickup_fail_timeout = timer_module.TimeoutTimer(65)
        self.night_timer = timer_module.FileTimer("night_timer")
        self.target_posi = []
        self.target_name = 'unknow'
        self.pickup_succ = False
        self.max_distance_from_target = 20
        self.last_err_code = " "
        self.search_mode = SEARCH_MODE_PICKUP
        self.last_search_times = 2
        self.crazy_f = False
        
    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pickup_timer.reset()
            # movement.change_view_to_posi(self.target_posi)
            self.pickup_succ = False
            # self.pickup_item_list = []
            self.last_search_times = 2
            self.collector_loops = 0
            self.pickup_fail_timeout.reset()
            
            if self.search_mode == SEARCH_MODE_FINDING:
                if self.night_timer.get_diff_time() >= 600:
                    logger.info(t2t("正在设置时间为夜晚"))
                    self.itt.delay(1)
                    generic_lib.set_genshin_time()
                    # scene_manager.switchto_mainwin(self.checkup_stop_func)
                    self.night_timer.reset()
            self.pause_threading_flag = False
    
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            time.sleep(0.5)
            self.itt.key_up('w')
            
    def set_target_position(self, p):
        self.target_posi = p
    
    def set_target_name(self, x):
        self.target_name = x
    
    def set_search_mode(self, x):
        self.search_mode = x
    
    def run(self):
        while 1:
            time.sleep(self.while_sleep)
            # time.sleep(0.1)
            if self.stop_threading_flag:
                logger.info(t2t("停止自动拾取"))
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
            while 1:
                if self.checkup_stop_func():break
                ret = self.pickup_recognize()
                if not ret:
                    break
                self.itt.delay(0.5, comment="Waiting for Genshin picking animation")
            
            if self.search_mode == SEARCH_MODE_FINDING:
                
                ret = self.auto_pickup()
                
                if self.target_posi:
                    self.cview_toward_target()
                if self.flicker_timer.get_diff_time() >= 1.8:
                    logger.debug("searching flicker")
                    self.collector_flag = False
                    self.finding_collector()
                    if self.search_mode == 0 and self.reset_timer.get_diff_time() >= self.reset_time:
                        self.reset_timer.reset()
                        self.reset_collector_loops()
                    
                if self.search_mode == 1 and self.last_search_times <= 0:
                    logger.info(t2t("PICKUP_TIMEOUT_001"))
                    self.last_err_code="PICKUP_TIMEOUT_001"
                    logger.info(t2t("停止拾取"))
                    self.pause_threading()
                        
                if self.pickup_fail_timeout.istimeout():
                    logger.info(t2t("PICKUP_TIMEOUT_002"))
                    self.last_err_code="PICKUP_TIMEOUT_002"
                    logger.info(t2t("停止拾取"))
                    self.pause_threading()
                
                '''当成功找到物品且找不到下一个可能物品后自动停止。'''
                if self.pickup_succ :
                    if self.collector_loops > self.max_number_of_collector_loops:
                        self.last_err_code="PICKUP_END_001"
                        logger.info(t2t("已找到物品且无法找到下一个物品，停止拾取"))
                        self.pause_threading()

    def get_err_code(self):
        return self.last_err_code
    
    def get_pickup_item_names(self, extra_white = False)->list:
        ret = self.itt.get_img_position(asset.IconGeneralFButton)
        y1 = asset.IconGeneralFButton.cap_posi[1]
        x1 = asset.IconGeneralFButton.cap_posi[0]
        cap = self.itt.capture()
        cap = crop(cap, [x1 + ret[0] + 53, y1 + ret[1] - 20, x1 + ret[0] + 361,  y1 + ret[1] + 54])
        # img_manager.qshow(cap)
        cap = self.itt.png2jpg(cap, channel='ui', alpha_num=160)
        if extra_white:
            img = extract_white_letters(cap)
        else:
            img = cap
        res = ocr.get_all_texts(img)
        return res
    
    def pickup_recognize(self):
        ret = generic_lib.f_recognition()
        if ret:
            time.sleep(0.05)
            ret = self.itt.get_img_position(asset.IconGeneralFButton)
            if ret == False:
                return 0
            
            itt.freeze_key('w', operate='up')
            time.sleep(0.1)

            y1 = asset.IconGeneralFButton.cap_posi[1]
            x1 = asset.IconGeneralFButton.cap_posi[0]
            cap = self.itt.capture()
            cap = crop(cap, [x1 + ret[0] + 53, y1 + ret[1] - 20, x1 + ret[0] + 361,  y1 + ret[1] + 54])
            
            if itt.similar_img(cap[:,:,:3], IconGeneralTalkBubble.image)>0.99:
                logger.info(f"pickup recognize: talk bubble; skip")
                return False
            # img_manager.qshow(cap)
            # img = extract_white_letters(cap)
            cap = self.itt.png2jpg(cap, channel='ui', alpha_num=160)
            res = ocr.get_all_texts(cap)
            if len(res) != 0:
                for text in res:
                    if text == '':
                        continue
                    if text not in self.pickup_blacklist:
                        self.pickup_fail_timeout.reset()
                        self.last_search_times = 2
                        self.itt.key_press('f')
                        if self.crazy_f:
                            logger.info(f"crazy f start")
                            for i in range(25):
                                itt.key_press('f')
                                time.sleep(0.05)
                        # self.itt.delay(0)
                        self.pickup_item_list.append(text)
                        logger.info(t2t('pickup: ') + str(text))
                        if str(text) in self.target_name:
                            logger.info(t2t("已找到：") + self.target_name)
                            self.pickup_succ = True
                        itt.unfreeze_key('w')
                        return True
            itt.unfreeze_key('w')
        return False

    def reset_pickup_item_list(self):
        self.pickup_item_list = []
    
    def find_collector(self, show_res=False):
        imsrc = self.itt.capture().copy()
        imsrc = self.itt.png2jpg(imsrc, alpha_num=1)
        # qshow(imsrc)
        imsrc[950:1080, :, :] = 0
        imsrc[0:150, :, :] = 0
        imsrc[:, 0:300, :] = 0
        imsrc[:, 1600:1920, :] = 0
        imsrc[350:751, 1079:1300, :] = 0
        a = ((imsrc[:, :, 0] >= 253).astype('uint8') + (imsrc[:, :, 1] >= 253).astype('uint8') + (
                imsrc[:, :, 2] >= 253).astype('uint8')) >= 3
        output_img = a.astype('uint8') * 255
        # print()
        if show_res:
            cv2.imshow('find_collector', output_img)
            cv2.waitKey(20)
        c_s = img_manager.get_rect(output_img, self.itt.capture(jpgmode=0), ret_mode=2)
        return c_s

    def reset_collector_loops(self):
        # print('reset')
        self.collector_loops = 0
        self.flicker_timer.reset()

    def cview_toward_target(self):
        cp = tracker.get_position()
        if euclidean_distance(cp,self.target_posi)>= self.max_distance_from_target:
            movement.reset_view()
            logger.debug("too far from source.the target")
            while euclidean_distance(tracker.get_position(), self.target_posi) >= 8:
                if self.checkup_stop_func():
                    return 0
                movement.change_view_to_posi(self.target_posi, self.checkup_stop_func)
                movement.move(movement.AHEAD, 4)
                self.itt.key_down('spacebar')

    def auto_pickup(self):
        # time.sleep(0.1)
        if self.checkup_stop_func():
            return 0
        ret_points = self.find_collector()
        points_length = []
        if len(ret_points) == 0: # type: ignore
            if self.flicker_timer.get_diff_time() < 2:
                # print('23')
                if itt.key_status['w']==True:
                    self.itt.key_up('w')
                    time.sleep(0.1)
            return 0
        else:
            self.flicker_timer.reset()
            self.reset_collector_loops()

            if itt.key_status['w']==False:
                self.itt.key_down('w')

        for point in ret_points:
            mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
            points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

        closest_point = ret_points[points_length.index(min(points_length))]
        px, py = closest_point
        mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
        px = (px - mx) / 1.8 + 35
        py = (py - my) / 2 + 40
        logger.debug(f"auto_pickup: px:{px} py:{py}")
        self.itt.move_to(px, py, relative=True)
        return px

    def finding_collector(self):
        if self.collector_loops < self.max_number_of_collector_loops:
            movement.reset_view()
            logger.debug("finding_collector")
            logger.debug("finding_collector: head down")
            for i in range(5):
                movement.cview(60, mode = movement.VERTICALLY)
                time.sleep(0.05)
        elif self.search_mode == 1 and self.last_search_times > 0:
            self.last_search_times-=1
            self.reset_collector_loops()
            return
        while self.collector_loops < self.max_number_of_collector_loops:
            if self.checkup_stop_func():
                return 0
            self.itt.move_to(200, 0, relative=True)
            ret_points = self.find_collector()
            if len(ret_points) != 0:  # type: ignore
                self.reset_collector_loops()
                return 0

            self.collector_loops += 1
        time.sleep(1)


if __name__ == '__main__':
    
    
    po = PickupOperator()
    # po.set_target_position([4813.5, -4180.5])
    # po.pause_threading()
    # po.start()
    # po.set_search_mode(0)
    # po.continue_threading()
    while 1:
        # po.find_collector()
        time.sleep(0.1)
        po.pickup_recognize()
        # po.pickup_recognize()
        # print()
