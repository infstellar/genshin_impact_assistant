import os
import traceback

import imageio
from PIL import ImageDraw
from util import *
from img_manager import ImgIcon


    
if __name__ == '__main__':
    a = get_bbox(cv2.imread("assets/imgs/common/ui/emergency_food.jpg"))
    b = crop(cv2.imread("assets/imgs/common/ui/emergency_food.jpg"),a)
    cv2.imshow('123',b)
    cv2.waitKey(0)
    print()