from base_threading import BaseThreading
from util import *
import img_manager
import generic_lib
from interaction_background import InteractionBGD
from pdocr_api import ocr
import posi_manager
import timer_module
import static_lib
import pyautogui
import cvAutoTrack
import movement


class PickupOperator(BaseThreading):

    def __init__(self):
        super().__init__()
        self.itt = InteractionBGD()
        self.pickup_blacklist = load_json("auto_pickup.json")["blacklist"]
        self.pickup_item_list = []
        self.flicker_timer = timer_module.Timer(diff_start_time=1)
        self.reset_timer = timer_module.Timer()
        self.reset_time = 120
        self.collecor_loops = 0
        self.collector_flag = True
        self.max_number_of_collector_loops = 200
        self.pickup_timer = timer_module.Timer()
        self.target_posi = []
        self.target_name = 'unknow'

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False
            self.pickup_timer.reset()
    
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.itt.key_up('w')
    
    def set_target_position(self, p):
        self.target_posi = p
    
    def set_target_name(self,x):
        self.target_name = x
    
    def run(self):
        while 1:
            # time.sleep(0.1)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True

            ret = self.pickup_recognize()

            ret = self.auto_pickup()
            if self.target_posi != []:
                self.cview_toward_target()
            if self.flicker_timer.get_diff_time() >= 5:
                self.collector_flag = False
                self.finding_collector()
                if self.reset_timer.get_diff_time() >= self.reset_time:
                    self.reset_timer.reset()
                    self.reset_collector_loops()

    def pickup_recognize(self):
        flag1 = False
        ret = generic_lib.f_recognition(self.itt)
        if ret:
            time.sleep(0.05)
            ret = self.itt.get_img_position(img_manager.F_BUTTON)
            if ret == False:
                return 0
            y1 = img_manager.F_BUTTON.cap_posi[0]
            x1 = img_manager.F_BUTTON.cap_posi[1]
            if static_lib.W_KEYDOWN:
                flag1 = True
                self.itt.key_up('w')
            time.sleep(0.1)
            cap = self.itt.capture()
            cap = self.itt.crop_image(cap, [y1 + ret[1] - 20, x1 + ret[0] + 53, y1 + ret[1] + 54, x1 + ret[0] + 361])
            cap = self.itt.png2jpg(cap, channel='ui', alpha_num=180)
            # img_manager.qshow(cap)
            res = ocr.img_analyse(cap)
            if len(res) != 0:
                if res[0][1][0] not in self.pickup_blacklist:
                    self.itt.key_press('f')
                    # self.itt.delay(0)
                    self.pickup_item_list.append(res[0][1][0])
                    logger.info('pickup: ' + str(res[0][1][0]))
                    if str(res[0][1][0]) in self.target_name:
                        logger.info("已找到：" + self.target_name)
                        self.pause_threading()
                    if flag1:
                        self.itt.key_down('w')
                    return True

        return False

    def find_collector(self):
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
        outputimg = a.astype('uint8') * 255
        # print()

        adad = img_manager.get_rect(outputimg, self.itt.capture(jpgmode=0), ret_mode=2)
        return adad

    def reset_collector_loops(self):
        # print('reset')
        self.collecor_loops = 0
        self.flicker_timer.reset()

    def cview_toward_target(self):
        cp = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
        if generic_lib.euclidean_distance(cp,self.target_posi)>=20:
            logger.debug("too far from the target")
            while generic_lib.euclidean_distance(cvAutoTrack.cvAutoTrackerLoop.get_position()[1:], self.target_posi) >= 8:
                if self.checkup_stop_func():
                    return 0
                movement.change_view_to_posi(self.target_posi)
                movement.move(movement.AHEAD, 4)
                self.itt.key_down('spacebar')

    def auto_pickup(self):
        # time.sleep(0.1)
        if self.checkup_stop_func():
            return 0
        ret_points = self.find_collector()
        points_length = []
        if len(ret_points) == 0:
            if self.flicker_timer.get_diff_time() < 2:
                # print('23')
                if static_lib.W_KEYDOWN:
                    self.itt.key_up('w')
                    time.sleep(0.2)
            return 0
        else:
            self.flicker_timer.reset()
            self.reset_collector_loops()

            if not static_lib.W_KEYDOWN:
                self.itt.key_down('w')

        for point in ret_points:
            mx, my = self.itt.get_mouse_point()
            points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

        closest_point = ret_points[points_length.index(min(points_length))]
        px, py = closest_point
        mx, my = self.itt.get_mouse_point()
        px = (px - mx) / 2.4 + 35
        py = (py - my) / 2 + 40
        if px >= 50:
            px = 50
        if px <= -50:
            px = -50
        if py >= 50:
            py = 50
        if py <= -50:
            py = -50
        # print(px, py)

        self.itt.move_to(px, py, relative=True)
        return px
        # print()

    def finding_collector(self):
        if self.collecor_loops < self.max_number_of_collector_loops:
            pyautogui.middleClick()
        while self.collecor_loops < self.max_number_of_collector_loops:
            if self.checkup_stop_func():
                return 0
            self.itt.move_to(25, 0, relative=True)
            ret_points = self.find_collector()
            if len(ret_points) != 0:
                self.reset_collector_loops()
                return 0

            self.collecor_loops += 1


if __name__ == '__main__':
    po = PickupOperator()
    po.set_target_position([4813.5, -4180.5])
    po.start()
    while 1:
        time.sleep(0.1)
        # po.pickup_recognize()
        # print()
