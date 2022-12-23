import cv2
import os
import time, math
from img_manager import qshow
from interaction_background import InteractionBGD
import img_manager, button_manager
import small_map
from util import *

itt = InteractionBGD()

pickup_blacklist = load_json("auto_pickup.json")["blacklist"]
pickup_blacklist += load_json("auto_pickup_default_blacklist.json")["blacklist"]
pickup_blacklist = list(set(pickup_blacklist))
# print()
a = itt.get_img_existence(button_manager.button_all_character_died)
# print()

while 1:
        imsrc = itt.capture().copy()
        imsrc = itt.png2jpg(imsrc, alpha_num=1)
        # qshow(imsrc)
        imsrc[950:1080, :, :] = 0
        imsrc[0:150, :, :] = 0
        imsrc[:, 0:300, :] = 0
        imsrc[:, 1600:1920, :] = 0
        imsrc[350:751, 1079:1300, :] = 0
        a = ((imsrc[:, :, 0] >= 249).astype('uint8') + (imsrc[:, :, 1] >= 249).astype('uint8') + (imsrc[:, :, 2] >= 249).astype('uint8')) >= 3
        outputimg = a.astype('uint8') * 255
        # print()
        cv2.imshow('123', outputimg)
        cv2.waitKey(20)
        adad = img_manager.get_rect(outputimg, itt.capture(jpgmode=0), ret_mode=2)
    


