from source.manager.asset import *
from source.manager import img_manager
import cv2, numpy as np
from source.interaction.interaction_core import itt
from typing import Tuple
itt = itt

def recaputer(img_obj:ImgIcon, orlang='zh_CN', lang='en_US'):
    cap_imsrc = itt.capture(posi=img_obj.cap_posi, jpgmode=img_obj.jpgmode)
    imsrc = np.zeros([1080,1920,3], dtype='uint8')
    imsrc[img_obj.cap_posi[1]:img_obj.cap_posi[3], img_obj.cap_posi[0]:img_obj.cap_posi[2]] = cap_imsrc
    img_manager.qshow(imsrc)
    save_path = img_obj.origin_path.replace(orlang, lang)
    cv2.imwrite(save_path, imsrc)

recaputer(ButtonBigmapTP, "en_US")