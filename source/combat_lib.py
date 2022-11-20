import time

import cv2

import img_manager
import posi_manager
from interaction_background import InteractionBGD
from util import *


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
    blue_num = 113
    green_num = 92
    float_num = 13

    im_src = itt.capture()
    orsrc = im_src.copy()
    im_src = itt.png2jpg(im_src, channel='ui', alpha_num=150)
    # img_manager.qshow(imsrc)

    '''可以用圆形遮挡优化'''

    # imsrc[950:1080, :, :] = 0
    # imsrc[0:50, :, :] = 0
    # imsrc[:, 1800:1920, :] = 0
    # img_manager.qshow(imsrc)
    im_src[:, :, 2][im_src[:, :, 2] < red_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] > blue_num + float_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] < blue_num - float_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] > green_num + float_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] < green_num - float_num] = 0
    # img_manager.qshow(imsrc[:, :, 2])
    # _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    # img_manager.qshow(imsrc2)
    # ret_point = img_manager.get_rect(imsrc2, orsrc, ret_mode=2)
    flag_is_arrow_exist = im_src[:, :, 2].max() > 0
    if flag_is_arrow_exist:
        return True
    # print('flag_is_arrow_exist', flag_is_arrow_exist)

    red_num = 245
    bg_num = 100

    im_src = orsrc.copy()
    im_src = itt.png2jpg(im_src, channel='ui', alpha_num=254)

    im_src[950:1080, :, :] = 0
    im_src[0:150, :, :] = 0
    im_src[:, 1600:1920, :] = 0

    im_src[:, :, 2][im_src[:, :, 2] < red_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] > bg_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] > bg_num] = 0
    # _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    # img_manager.qshow(imsrc[:, :, 2])
    flag_is_lifebar_exist = im_src[:, :, 2].max() > 0
    # print('flag_is_lifebar_exist ',flag_is_lifebar_exist)
    if flag_is_lifebar_exist:
        return True

    return False

# while 1:
#     print(combat_statement_detection(InteractionBGD()))
#     time.sleep(0.5)
