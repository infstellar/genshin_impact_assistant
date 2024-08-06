import time

import numpy as np
import random

from source.common.base_threading import BaseThreading
from source.util import *
from source.interaction.interaction_core import itt
from source.api.pdocr_complete import ocr
from source.common import timer_module, static_lib
from source.funclib import generic_lib, movement, combat_lib
from source.manager import img_manager, asset
import cv2
from source.interaction.minimap_tracker import tracker
from source.assets.pickup import *
from source.map.map import genshin_map
from source.funclib.cvars import *


# USE_YAP = False if sys.gettrace() else True
USE_YAP = True # Fixed!!! print debug is useful.
# if sys.gettrace():
#     logger.warning("YAP disabled in debug mode. Pickupper may work slower.")

if USE_YAP:
    from source.pickup.yap_pickup import yap_pickupper, PickupResult

SEARCH_MODE_FINDING = 1
SEARCH_MODE_PICKUP = 0





class PickupOperator(BaseThreading):

    ABSORPTION_THRESHOLD = 10

    def __init__(self):
        super().__init__()
        self.setName("PickupOperator")
        self.itt = itt
        self.pickup_blacklist = GIAconfig.Collector_PickupBlacklist
        self.pickup_blacklist += load_json("auto_pickup_default_blacklist.json", folder_path=fr"{ASSETS_PATH}")["blacklist"]
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
        self.pickup_fail_cooldown = timer_module.AdvanceTimer(limit=2).reset()
        self.while_sleep = 0.3 if USE_YAP else 0.1
        self.pause_threading_flag = True  # TODO: formalize it, consider that expand this method to all threading in case the init funcs in 'continue_threading' don't run, and make some bugs.
        self.absorptive_positions = []
        
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
            if USE_YAP:
                yap_pickupper.start()
            self.pause_threading_flag = False

    def add_absorptive_position(self, pos):
        self.absorptive_positions.append(pos)

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            time.sleep(0.5)
            self.itt.key_up('w')
            if USE_YAP:
                yap_pickupper.stop()
            
    def set_target_position(self, p):
        self.target_posi = p
    
    def set_target_name(self, x):
        self.target_name = x
    
    def set_search_mode(self, x):
        self.search_mode = x

    def before_terminate(self):
        if USE_YAP:
            if not self.pause_threading_flag:
                yap_pickupper.stop()

    def is_absorb(self):
        if len(self.absorptive_positions) > 0:
            return euclidean_distance_plist(genshin_map.get_position(use_cache=True), self.absorptive_positions).min() < self.ABSORPTION_THRESHOLD

    def absorb(self):
        curr_pos = genshin_map.get_position()
        for abs_pos in self.absorptive_positions:
            if euclidean_distance(abs_pos, curr_pos) < self.ABSORPTION_THRESHOLD:
                if movement.get_current_motion_state() == FLYING:
                    for i in range(20):
                        itt.left_click()
                        time.sleep(2)
                        if movement.get_current_motion_state() != FLYING:
                            break
                if movement.get_current_motion_state() != FLYING:
                    self.absorptive_pickup(abs_pos)
                else:
                    logger.error(f"LAND FAIL")
                self.absorptive_positions.pop(self.absorptive_positions.index(abs_pos))
                return

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
            ret = generic_lib.f_recognition()
            if ret:
                itt.delay(0.1, comment='Waiting for Genshin picking animation')
                while 1:
                    if self.checkup_stop_func():break
                    # logger.info('enter 1')
                    ret = self.pickup_recognize()
                    if not ret:
                        break
                # self.itt.delay(0.4, comment="Waiting for Genshin picking animation")

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
        cap = self.itt.capture(jpgmode=FOUR_CHANNELS)
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
        if not self.pickup_fail_cooldown.reached():
            return False
        if not USE_YAP:
            ret = generic_lib.f_recognition(cap=itt.capture(jpgmode=NORMAL_CHANNELS, recapture_limit=0.1, posi=asset.IconGeneralFButton.cap_posi))
            if ret:
                ret = self.itt.get_img_position(asset.IconGeneralFButton)
                if ret == False: return 0

                # itt.freeze_key('w', operate='up')
                # time.sleep(0.1)

                y1 = asset.IconGeneralFButton.cap_posi[1]
                x1 = asset.IconGeneralFButton.cap_posi[0]
                cap = self.itt.capture(jpgmode=FOUR_CHANNELS)
                cap = crop(cap, [x1 + ret[0] + 53, y1 + ret[1] - 20, x1 + ret[0] + 361,  y1 + ret[1] + 54])

                if similar_img(cap[:,:,:3], IconGeneralTalkBubble.image)>0.99:
                    logger.info(f"pickup recognize: talk bubble; skip")
                    self.pickup_fail_cooldown.reset()
                    return False
                # img_manager.qshow(cap)
                # img = extract_white_letters(cap)
                cap = self.itt.png2jpg(cap, channel='ui', alpha_num=160)
                res = ocr.get_all_texts(cap, per_monitor=True)
                # logger.info('enter 2')
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
                            self.pickup_item_list.append(text)
                            logger.info(t2t('pickup: ') + str(text))

                            if str(text) in self.target_name:
                                logger.info(t2t("已找到：") + self.target_name)
                                self.pickup_succ = True
                            # logger.info('out 1')
                            return True
            return False
        else:
            return True

    def reset_pickup_item_list(self):
        self.pickup_item_list = []
    
    def find_collector(self, show_res=False):
        imsrc = self.itt.capture(jpgmode=FOUR_CHANNELS).copy()
        imsrc = self.itt.png2jpg(imsrc, alpha_num=1)
        # qshow(imsrc)
        imsrc[950:1080, :, :] = 0
        imsrc[0:150, :, :] = 0
        imsrc[:, 0:300, :] = 0
        imsrc[:, 1600:1920, :] = 0
        imsrc[350:751, 1079:1300, :] = 0
        # a = ((imsrc[:, :, 0] >= 253).astype('uint8') + (imsrc[:, :, 1] >= 253).astype('uint8') + (
        #         imsrc[:, :, 2] >= 253).astype('uint8')) >= 3
        # output_img = a.astype('uint8') * 255
        mask = np.logical_not(np.all(imsrc > 200, axis=-1))
        imsrc[mask] = [0, 0, 0]
        output_img = imsrc.copy()
        # print()
        if show_res:
            cv2.imshow('find_collector', output_img)
            cv2.imwrite(os.path.join(ROOT_PATH, 'tools', 'pickup', f'{time.time()}.jpg'), output_img)
            cv2.waitKey(1)
        # c_s = img_manager.get_rect(output_img, self.itt.capture(jpgmode=NORMAL_CHANNELS), ret_mode=2)
        c_s = self.match_blink(output_img)
        # c_s = 0
        return c_s

    BLINK_THRESHOLD = 0.82
    
    def match_blink(self, img:np.ndarray, ignore_close=False, show_res = False):
        raw_img = img.copy()
        img = img.astype('float')
        img = ((img[:,:,0]+img[:,:,1]+img[:,:,2])/3).astype('uint8')
        mask = np.ones_like(IconGeneralBlink.image[:,:,0]).astype('uint8')
        # mask = mask*255
        res = cv2.matchTemplate(img, IconGeneralBlink.image[:,:,0], cv2.TM_CCORR_NORMED) # , mask=mask
        res[np.where(res == np.nan)] = 0
        loc = np.where(res >= self.BLINK_THRESHOLD)
        matched_coordinates = sorted(zip(*loc[::-1]), key=lambda x: res[x[1], x[0]], reverse=True)
        if show_res:
            show_img = raw_img.copy()
            for p in matched_coordinates:
                cv2.drawMarker(show_img, position=(int(p[0]), int(p[1])), color=(0, 0, 255), markerSize=3,markerType=cv2.MARKER_CROSS, thickness=5)
            cv2.imshow('match_blink', show_img)
            cv2.waitKey(1)
            print(res.max(), res.min())
        if ignore_close:
            ret_coordinates = []
            for i in matched_coordinates:
                if len(ret_coordinates) == 0:
                    ret_coordinates.append(i)
                    continue
                if min(euclidean_distance_plist(i, ret_coordinates))>=15:
                    ret_coordinates.append(i)
            return ret_coordinates
        else:
            return matched_coordinates

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
                movement.move(movement.MOVE_AHEAD, 4)
                self.itt.key_down('spacebar')

    def absorptive_pickup(self, pos, is_active_pickup = True):
        pt=time.time()
        arrive_flag = False
        arrive_i = 9999
        or_len = len(yap_pickupper.pickup_result)
        for i in range(50):
            if time.time()-pt>5:
                offset = 2
            else:
                offset = 1

            curr_posi = genshin_map.get_position()
            movement.change_view_to_posi(pos, offset=offset, stop_func=self.checkup_stop_func, curr_posi=curr_posi)
            dist = euclidean_distance(curr_posi, pos)
            logger.debug(f'absorption: dist: {dist}')
            if dist > 2:
                dura = 1
            else:
                dura = 0.5
            movement.move(MOVE_AHEAD, distance=dura)

            if len(yap_pickupper.pickup_result) > or_len:
                logger.info(f'collected {yap_pickupper.get_last_picked_item().pk_name}, adsorption end.')
                return True
            if dist < offset:
                if not arrive_flag:
                    logger.info(f'absorption: arrive')
                    arrive_flag = True
                    arrive_i = i
                    if is_active_pickup:
                        self.active_pickup()
            if i - arrive_i > 10:
                logger.info(f'absorption: arrive but not find, break.')
                return False
        logger.info(f'adsorption: timeout.')
        return False
            # movement.move_to_posi_LoopMode(pos, stop_func=self.checkup_stop_func, threshold=offset)


    def active_pickup(self, is_nahida = None):
        if is_nahida is None:
            is_nahida = 'Nahida' in combat_lib.get_characters_name(max_retry=30)
            logger.debug(f'is nahida: {is_nahida}')
            is_nahida = is_nahida and (movement.get_current_motion_state() == WALKING)
            logger.info(f'is nahida: {is_nahida}')
        if is_nahida: # 'Nahida' in combat_lib.get_characters_name(max_retry=30)
            names = combat_lib.get_characters_name()
            nahida_index = names.index('Nahida') + 1
            origin_chara_index = combat_lib.get_current_chara_num(self.checkup_stop_func)
            while not combat_lib.get_current_chara_num(self.checkup_stop_func) == nahida_index:
                itt.key_press(str(nahida_index))
                time.sleep(0.2)
            
            # itt.middle_click()
            # itt.delay(0.3, comment='reset view')
            
            itt.key_down('e')
            itt.delay(0.4, comment='waiting the Nahida E skill start')
            itt.key_down('e')
            
            for i in range(10):
                itt.move_to(0,800,relative=True)
                time.sleep(0.02)  
            
            rate = 1.2
            
            for i in range(int(108*rate)):
                if i%int(8*rate)==0:
                    if i >= 90*rate:
                        itt.move_to(0,-1500,relative=True)
                    if i >= 80*rate:
                        itt.move_to(0,-1000,relative=True)
                    elif i >= 60*rate:
                        itt.move_to(0,-600,relative=True)
                    elif i >= 20*rate:
                        itt.move_to(0,-200,relative=True)
                    else:
                        itt.move_to(0,-100,relative=True)
                    time.sleep(0.02)
                itt.move_to(int(400/rate)+random.randint(-100, 100),0,relative=True)
                time.sleep(0.02)
            
            itt.key_up('e')
            
            itt.delay(0.4, comment='waiting the Nahida E skill end')
            itt.middle_click()
            
            while not combat_lib.get_current_chara_num(self.checkup_stop_func) == origin_chara_index:
                itt.key_press(str(origin_chara_index))
                time.sleep(0.2)
            
            return 0
            
        else:
            return self.auto_pickup()
        
        
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
    # while 1:
    #     print(po.find_collector(show_res=True))
    # po.set_target_position([4813.5, -4180.5])
    # po.pause_threading()
    po.start()
    # po.set_search_mode(0)
    # po.active_pickup(is_nahida=True)
    po.absorptive_pickup([7541.5, 5466.5])
    while 1:
        time.sleep(1)

        # po.find_collector()
        # po.pickup_recognize()
        # po.pickup_recognize()
        # print()
