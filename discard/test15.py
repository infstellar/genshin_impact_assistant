from interaction_background import InteractionBGD
from util import *

itt = InteractionBGD()
import cv2, img_manager

# imsrc = cv2.imread("test21.jpg")
# orsrc = cv2.imread("test21.jpg")

red_num = 245
BG_num = 100


# over_item_list= imsrc[:,:,0]<BG_num or imsrc[:,:,2]>red_num or imsrc[:,:,1]<BG_num
# imsrc[:,:,2][imsrc[:,:,2]<red_num]=0
# imsrc[:,:,2][imsrc[:,:,0]>BG_num]=0
# imsrc[:,:,2][imsrc[:,:,1]>BG_num]=0

# ret, imsrc2 = cv2.threshold(imsrc[:,:,2], 1, 255,cv2.THRESH_BINARY)
# img_manager.qshow(imsrc2)
# img_manager.get_rect(imsrc2,orsrc)

# cv2.imshow('123',imsrc[:,:,2])
# cv2.waitKey(0)

# 要截取一些区域
def get_enemy_feature():
    cap = itt.capture()
    imsrc = itt.png2jpg(cap, channel='ui', alpha_num=254)
    orsrc = cap.copy()
    cv2.cvtColor(orsrc, cv2.COLOR_BGR2RGB)
    imsrc[:, :, 2][imsrc[:, :, 2] < red_num] = 0
    imsrc[:, :, 2][imsrc[:, :, 0] > BG_num] = 0
    imsrc[:, :, 2][imsrc[:, :, 1] > BG_num] = 0
    _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    # cv2.imshow('123',retimg)
    # cv2.waitKey(100)
    ret_point = img_manager.get_rect(imsrc2, orsrc, ret_mode=2)
    return ret_point


#
for i in range(1000):
    time.sleep(0.1)
    ret_points = get_enemy_feature()
    points_length = []
    if len(ret_points) == 0:
        continue
    for point in ret_points:
        mx, my = itt.get_mouse_point()
        points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)

    closest_point = ret_points[points_length.index(min(points_length))]
    px, py = closest_point
    mx, my = itt.get_mouse_point()
    px = (px - mx) / 4
    py = (py - my) / 4 + 35
    print(px, py)

    itt.move_to(px, py, relative=True)
    # print()
