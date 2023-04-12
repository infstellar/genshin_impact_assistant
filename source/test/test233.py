from source.interaction.interaction_core import itt
from source.manager import img_manager, asset
from source.util import *

itt = itt

pickup_blacklist = load_json("auto_pickup.json")["blacklist"]
pickup_blacklist += load_json("auto_pickup_default_blacklist.json")["blacklist"]
pickup_blacklist = list(set(pickup_blacklist))
# print()
a = itt.get_img_existence(asset.ButtonGeneralAllCharacterDied)
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
    


