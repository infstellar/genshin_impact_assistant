import time

import img_manager
import posi_manager
from interaction_background import Interaction_BGD
from unit import *


def get_current_chara_num(itt: Interaction_BGD):
    cap = itt.capture(jpgmode=2)
    for i in range(4):
        p = posi_manager.chara_num_list_point[i]
        if min(cap[p[0], p[1]]) > 240:
            continue
        else:
            return i + 1


def unconventionality_situlation_detection(itt: Interaction_BGD,
                                           autoDispose=True):  # unconventionality situlation detection
    # situlation 1: coming_out_by_space

    situlation_code = -1

    while itt.get_img_existence(img_manager.COMING_OUT_BY_SPACE, jpgmode=2, min_rate=0.8):
        situlation_code = 1
        itt.keyPress('spacebar')
        logger.debug('Unconventionality Situlation: COMING_OUT_BY_SPACE')
        time.sleep(0.1)

    return situlation_code
