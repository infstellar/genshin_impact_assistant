import time

import cv2

import img_manager
import posi_manager
from interaction_background import InteractionBGD
from util import *
from base_threading import BaseThreading
import numpy as np


def get_current_chara_num(itt: InteractionBGD):
    cap = itt.capture(jpgmode=2)
    for i in range(4):
        p = posi_manager.chara_num_list_point[i]
        if min(cap[p[0], p[1]]) > 240:
            continue
        else:
            return i + 1


def unconventionality_situlation_detection(itt: InteractionBGD,
                                           autoDispose=True):
    # unconventionality situlation detection
    # situlation 1: coming_out_by_space

    situlation_code = -1

    while itt.get_img_existence(img_manager.COMING_OUT_BY_SPACE):
        situlation_code = 1
        itt.key_press('spacebar')
        logger.debug('Unconventionality Situlation: COMING_OUT_BY_SPACE')
        time.sleep(0.1)

    return situlation_code


def combat_statement_detection(itt: InteractionBGD):
    red_num = 250
    blue_num = 90
    green_num = 90
    float_num = 30

    im_src = itt.capture()
    orsrc = im_src.copy()
    im_src = itt.png2jpg(im_src, channel='ui', alpha_num=150)
    # img_manager.qshow(imsrc)

    '''可以用圆形遮挡优化'''

    im_src[950:1080, :, :] = 0
    im_src[0:50, :, :] = 0
    im_src[:, 1650:1920, :] = 0
    # img_manager.qshow(imsrc)
    im_src[:, :, 2][im_src[:, :, 2] < red_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] > blue_num + float_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] < blue_num - float_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] > green_num + float_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] < green_num - float_num] = 0
    
    # img_manager.qshow(imsrc[:, :, 2])
    imsrc2 = im_src.copy()
    _, imsrc2 = cv2.threshold(imsrc2[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    # img_manager.qshow(imsrc2)
    ret_contours = img_manager.get_rect(imsrc2, orsrc, ret_mode=3)
    ret_range = img_manager.get_rect(imsrc2, orsrc, ret_mode=0)
    
    if False:
        if len(ret_contours) != 0:
            angle = cv2.minAreaRect(ret_contours)[2]
            print(angle)
            img = im_src.copy()[:, :, 2]
            img = img[ret_range[0]:ret_range[2],ret_range[1]:ret_range[3]]
            h, w = img.shape
            center = (w//2, h//2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)    
            cv2.imshow('123', rotated)
            cv2.waitKey(50)
        
    red_arrow_num = len(np.where(im_src[:, :, 2]>=254)[-1])
    if red_arrow_num > 180:
        return True
    # print('flag_is_arrow_exist', flag_is_arrow_exist)

    red_num = 245
    bg_num = 100

    im_src = orsrc.copy()
    im_src = itt.png2jpg(im_src, channel='ui', alpha_num=254)

    im_src[990:1080, :, :] = 0
    im_src[0:150, :, :] = 0
    im_src[:, 1650:1920, :] = 0
    
    im_src[:, :, 2][im_src[:, :, 2] < red_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] > bg_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] > bg_num] = 0
    # _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    
    flag_is_lifebar_exist = im_src[:, :, 2].max() > 0
    # print('flag_is_lifebar_exist ',flag_is_lifebar_exist)
    if flag_is_lifebar_exist:
        return True

    return False

class CombatStatementDetectionLoop(BaseThreading):
    def __init__(self):
        super().__init__()
        self.itt = InteractionBGD()
        self.current_state = False
        self.state_counter = 0
        self.while_sleep = 0.1
    
    def get_combat_state(self):
        return self.current_state
    
    def run(self):
        '''if you're using this class, copy this'''
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
            
            state = combat_statement_detection(self.itt)
            if state != self.current_state:
                self.state_counter += 1
                if self.current_state == True: # 切换到无敌人慢一点
                    self.while_sleep = 0.5
                elif self.current_state == False: # 快速切换到遇敌
                    self.while_sleep = 0.02
            else:
                self.state_counter = 0
                self.while_sleep = 0.2
            if self.state_counter >= 10:
                print('change state')
                self.state_counter = 0
                self.current_state = state

CSDL = CombatStatementDetectionLoop()
CSDL.start()

if __name__ == '__main__':
    while 1:
        print(CSDL.get_combat_state())
        time.sleep(0.2)
