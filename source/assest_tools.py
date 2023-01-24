from asset import *
import cv2, numpy as np
from interaction_background import InteractionBGD
itt = InteractionBGD()

def recaputer(img_obj:img_manager.ImgIcon, lang):
    cap_imsrc = itt.capture(posi=img_obj.cap_posi, jpgmode=img_obj.jpgmode)
    imsrc = np.zeros([1080,1920,3], dtype='uint8')
    imsrc[img_obj.cap_posi[1]:img_obj.cap_posi[3], img_obj.cap_posi[0]:img_obj.cap_posi[2]] = cap_imsrc
    img_manager.qshow(imsrc)
    save_path = img_obj.origin_path.replace("$lang$", lang)
    cv2.imwrite(save_path, imsrc)

recaputer(img_manager.USE_20X2RESIN_DOBLE_CHOICES,"en_US")