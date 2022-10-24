# -*- coding: utf-8 -*-

import time

import posi_manager
import static_method

itt = static_method.sta_itt


# imagepath = '.\\imgs\\direction_arrow.png'
# img = cv2.imread(imagepath, 1)

# 将图片的边缘变为白色

# 保存图片
# cv2.imwrite('.\\imgs\\direction_arrow.png',pre_do(img))
# cv2.waitKey(0)

# imagepath = '.\\imgs\\direction_arrow.png'
# img = cv2.imread(imagepath, -1)

# cv2.imshow('123',image[0])
# cv2.waitKey(0)
def get_direction_angle():
    cap = itt.png2jpg(itt.capture(), bgcolor='white', channel='ui')
    val = []
    for i in ['N.jpg', 'NE.jpg', 'E.jpg', 'SE.jpg', 'S.jpg', 'SW.jpg', 'W.jpg', 'NW.jpg']:
        a = itt.similar_img(i, cap, posi_manager.posi_arrow)
        val.append(a)
    return [0, 45, 90, 135, 180, -135, -90, -45][val.index(max(val))]
    # pass


# print()
# cv2.imshow('123', itt.png2jpg(itt.capture(posi_manager.posi_arrow),bgcolor='white',channel='ui'))
# cv2.waitKey(0)
# cv2.imwrite('imgs\\NW.jpg',itt.png2jpg(itt.capture(posi_manager.posi_arrow),bgcolor='white',channel='ui'))
while (1):
    print(get_direction_angle())
    time.sleep(1)
    # input()
    # cv2.imwrite('imgs\\N.jpg',itt.png2jpg(itt.capture(posi_manager.posi_arrow),bgcolor='white',channel='ui'))
    # itt.png2jpg(itt.capture(),bgcolor='black',channel='bg')
    # get_angle(itt.png2jpg(itt.capture(posi_manager.posi_arrow),bgcolor='white',channel='ui'))
#     time.sleep(1)
# 仿射变换,对图片旋转angle角度
# h, w = img.shape
# center = (w//2, h//2)
# M = cv2.getRotationMatrix2D(center, angle, 1.0)
# rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# # 保存旋转后的图片
# cv2.imshow('123', rotated)
# cv2.waitKey(0)
