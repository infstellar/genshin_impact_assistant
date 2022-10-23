import cv2
import numpy as np

import posi_manager

COMING_OUT_BY_SPACE = "coming_out_by_space"
IN_DOMAIN = "IN_DOMAIN"
USE_20RESIN_DOBLE_CHOICES = "USE_20RESIN_DOBLE_CHOICES"
USE_20X2RESIN_DOBLE_CHOICES = "USE_20X2RESIN_DOBLE_CHOICES"
F_BUTTON = 'F_BUTTON'

imsrc_coming_out_by_space = cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg")
imsrc_IN_DOMAIN = cv2.imread("assests\\imgs\\common\\IN_DOMAIN.jpg")
imsrc_USE_20RESIN_DOBLE_CHOICES = cv2.imread("assests\\imgs\\common\\USE_20RESIN_DOBLE_CHOICES.jpg")
imsrc_USE_20X2RESIN_DOBLE_CHOICES = cv2.imread("assests\\imgs\\common\\USE_20X2RESIN_DOBLE_CHOICES.jpg")
imsrc_F_BUTTON = cv2.imread("assests\\imgs\\common\\F_BUTTON.jpg")

imgs_dict = {
    "coming_out_by_space": imsrc_coming_out_by_space,
    "IN_DOMAIN": imsrc_IN_DOMAIN,
    "USE_20RESIN_DOBLE_CHOICES": imsrc_USE_20RESIN_DOBLE_CHOICES,
    "USE_20X2RESIN_DOBLE_CHOICES": imsrc_USE_20X2RESIN_DOBLE_CHOICES,
    "F_BUTTON":imsrc_F_BUTTON
}

matching_rate_dict = {
    "coming_out_by_space": 0.9,
    "IN_DOMAIN": 0.98,
    "USE_20RESIN_DOBLE_CHOICES": 0.88,
    "USE_20X2RESIN_DOBLE_CHOICES": 0.88,
}

alpha_dict = {
    "F_BUTTON":254
}


def qshow(img1):
    cv2.imshow('123', img1)
    cv2.waitKey(0)


def get_img_from_name(img_name: str):
    im_src = imgs_dict[img_name]
    posi = posi_manager.get_posi_from_str(img_name)
    ret_img = im_src[posi[0]:posi[2], posi[1]:posi[3]]
    # cv2.imshow('12',ret_img)
    # cv2.waitKey(0)
    return ret_img


def refrom_img(im_src, posi):
    img = np.zeros((1080, 1920, 3), dtype=np.uint8)
    img[posi[0]:posi[2], posi[1]:posi[3]] = im_src
    cv2.imshow('12', img)
    cv2.imshow('123', im_src)
    cv2.waitKey(0)
    return img


def auto_import_img(im_path, name):
    im_src = cv2.imread(im_path)
    origin_img = im_src.copy()
    gray_img = cv2.cvtColor(im_src, cv2.COLOR_BGR2GRAY)  # 先要转换为灰度图片
    ret, im_src = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)  # 这里的第二个参数要调，是阈值！！
    qshow(origin_img)

    contours, hierarchy = cv2.findContours(im_src, 0, 1)
    # qshow(Alpha)

    max_black = 0
    max_id = 0
    bound_rect = []
    for i in range(len(contours)):
        bound_rect.append([])
        if len(contours[i]) > max_black:
            max_black = len(contours[i])
            max_id = i
        bound_rect[i] = cv2.boundingRect(cv2.Mat(contours[i]))

    x, y, w, h = bound_rect[max_id]
    while 1:
        d = origin_img.copy()
        draw_1 = cv2.rectangle(d, (x, y), (x + w, y + h), (0, 255, 0), 2)
        qshow(draw_1)
        print('\"' + name + '\"', ':', [y, x, y + h, x + w])
        a,b,c,d=map(int,input('x,y,w,h: ').split(','))
        if a==0 and b==0 and c==0 and d==0:
            break
        else:
            x+=a
            y+=b
            w+=c
            h+=d
    return [y, x, y + h, x + w]
    # p = [x + w / 2, y + h / 2]


def get_rect(im_src, origin_img, ret_mode=0):
    # if origin_img==None:
    #     origin_img = imsrc
    ret, im_src = cv2.threshold(im_src, 1, 255, cv2.THRESH_BINARY)
    contours, hierarcy = cv2.findContours(im_src, 0, 1)
    # qshow(Alpha)
    draw_1 = origin_img
    max_black = 0
    max_id = 0
    bound_rect = []
    center_points = []
    for i in range(len(contours)):
        bound_rect.append([])

        if len(contours[i]) > max_black:
            max_black = len(contours[i])
            max_id = i
        bound_rect[i] = cv2.boundingRect(cv2.Mat(contours[i]))
        x, y, w, h = bound_rect[i]
        center_points.append([(x + w / 2), (y + h / 2)])
        if ret_mode == 1:
            draw_1 = cv2.rectangle(draw_1, (x, y), (x + w, y + h), (0, 255, 0), 1)

        x, y, w, h = bound_rect[max_id]
    
    # qshow(draw_1)
    # print('\"'+name+'\"',':',[y,x,y+h,x+w])
    if ret_mode == 0:
        if len(contours)==0:
            return None
        return [y, x, y + h, x + w]
    elif ret_mode == 1:
        return draw_1
    elif ret_mode == 2:
        return center_points


if __name__ == '__main__':
    # img = refrom_img(cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg"),posi_manager.get_posi_from_str('coming_out_by_space'))
    # cv2.imwrite("assests\\imgs\\common\\coming_out_by_space.jpg", img)
    # get_img_from_imgname(COMING_OUT_BY_SPACE)
    pname = F_BUTTON
    p = auto_import_img("assests\\imgs\\common\\" + pname + ".jpg", pname)
    print(p)
