from assest import *
import cv2
from interaction_background import InteractionBGD
itt = InteractionBGD()

def recaputer(img_obj:img_manager.ImgIcon, save_path):
    imsrc = itt.capture(posi=img_obj.cap_posi, jpgmode=img_obj.jpgmode)
    img_manager.qshow(imsrc)
    cv2.imwrite(save_path, imsrc)

# recaputer(img_manager.)
