import cv2
import os
import time, math
from img_manager import qshow
from interaction_background import InteractionBGD
import img_manager
import small_map

itt = InteractionBGD()
while 1:
    imsrc = itt.capture().copy()
    imsrc = itt.png2jpg(imsrc, alpha_num=1)
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

    adad = img_manager.get_rect(outputimg, itt.capture(jpgmode=0), ret_mode=1)

    cv2.imshow('123', adad)
    cv2.waitKey(100)
