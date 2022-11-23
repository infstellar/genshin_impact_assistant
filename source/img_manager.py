import cv2
import numpy as np

import posi_manager

# COMING_OUT_BY_SPACE = 
IN_DOMAIN = "IN_DOMAIN"
USE_20RESIN_DOBLE_CHOICES = "USE_20RESIN_DOBLE_CHOICES"
USE_20X2RESIN_DOBLE_CHOICES = "USE_20X2RESIN_DOBLE_CHOICES"
F_BUTTON = 'F_BUTTON'


class ImgIcon:
    def __init__(self, name, path, is_bbg=True, matching_rate=None, alpha=None, bbg_posi=None, cap_posi=[1080, 1920],
                 jpgmode=2, threshold=0.95):
        self.name = name
        self.path = path
        self.is_bbg = is_bbg
        self.mr = matching_rate
        self.alpha = alpha
        self.bbg_posi = bbg_posi
        self.jpgmode = jpgmode
        self.threshold = threshold
        if cap_posi == 'bbg':
            self.cap_posi = self.bbg_posi
        else:
            self.cap_posi = cap_posi

        self.image = cv2.imread(self.path)

        if self.is_bbg:
            self.image = self.image[self.bbg_posi[0]:self.bbg_posi[2], self.bbg_posi[1]:self.bbg_posi[3]]


imgs_dict = {}

COMING_OUT_BY_SPACE = ImgIcon(name="coming_out_by_space", path="assests\\imgs\\common\\coming_out_by_space.jpg",
                              is_bbg=True, bbg_posi=[505, 1379, 568, 1447], cap_posi='bbg', threshold=0.8, )
IN_DOMAIN = ImgIcon(name="IN_DOMAIN", path="assests\\imgs\\common\\IN_DOMAIN.jpg",
                    is_bbg=True, bbg_posi=[112, 25, 137, 52], cap_posi='bbg')
USE_20RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20RESIN_DOBLE_CHOICES",
                                    path="assests\\imgs\\common\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                    is_bbg=True, bbg_posi=[724, 985, 791, 1348], cap_posi='bbg')
USE_20X2RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20X2RESIN_DOBLE_CHOICES",
                                      path="assests\\imgs\\common\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                      is_bbg=True, bbg_posi=[726, 567, 793, 934], cap_posi='bbg')
F_BUTTON = ImgIcon(name="F_BUTTON", path="assests\\imgs\\common\\F_BUTTON.jpg",
                   is_bbg=True, bbg_posi=[526, 1104, 550, 1128], cap_posi=[350, 1079, 751, 1162],
                   threshold=0.92)
bigmap_TeleportWaypoint = ImgIcon(name="bigmap_TeleportWaypoint",
                                  path="assests\\imgs\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
smallmap_AbyssMage = ImgIcon(name="smallmap_AbyssMage", path="assests\\imgs\\map\\small_map\\enemies\\AbyssMage.jpg",
                             is_bbg=False)
bigmap_AbyssMage = ImgIcon(name="bigmap_AbyssMage", path="assests\\imgs\\map\\big_map\\enemies\\AbyssMage.jpg",
                           is_bbg=False)
motion_swimming = ImgIcon(name="motion_swimming", path="assests\\imgs\\common\\motion_swimming.jpg",
                          is_bbg=True, bbg_posi=[968, 1808, 1016, 1872], cap_posi='bbg')
motion_climbing = ImgIcon(name="motion_climbing", path="assests\\imgs\\common\\motion_climbing.jpg",
                          is_bbg=True, bbg_posi=[960, 1706, 1022, 1866], cap_posi='bbg')
motion_flying = ImgIcon(name="motion_flying", path="assests\\imgs\\common\\motion_flying.jpg",
                        is_bbg=True, bbg_posi=[960, 1706, 1022, 1866], cap_posi='bbg')
ui_main_win = ImgIcon(name="ui_main_win", path="assests\\imgs\\common\\ui\\emergency_food.jpg",
                      is_bbg=True, bbg_posi=[34, 39, 78, 73], cap_posi='bbg')
ui_bigmap_win = ImgIcon(name="ui_bigmap_win", path="assests\\imgs\\common\\ui\\bigmap.jpg",
                        is_bbg=True, bbg_posi=[36, 1591, 59, 1614], cap_posi='bbg')
matching_rate_dict = {
    "coming_out_by_space": 0.9,
    "IN_DOMAIN": 0.98,
    "USE_20RESIN_DOBLE_CHOICES": 0.88,
    "USE_20X2RESIN_DOBLE_CHOICES": 0.88,
}

alpha_dict = {
    "F_BUTTON": 254
}


def qshow(img1):
    cv2.imshow('123', img1)
    cv2.waitKey(0)


# def get_img_from_name(img_name: str, reshape=True):
#     ret_img = imgs_dict[img_name]
#     if reshape:
#         posi = posi_manager.get_posi_from_str(img_name)
#         ret_img = ret_img[posi[0]:posi[2], posi[1]:posi[3]]
#     # cv2.imshow('12',ret_img)
#     # cv2.waitKey(0)
#     return ret_img


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
        a, b, c, d = map(int, input('x,y,w,h: ').split(','))
        if a == 0 and b == 0 and c == 0 and d == 0:
            break
        else:
            x += a
            y += b
            w += c
            h += d
    return [y, x, y + h, x + w]
    # p = [x + w / 2, y + h / 2]


def get_rect(im_src, origin_img, ret_mode=0):
    # if origin_img==None:
    #     origin_img = imsrc
    ret, im_src = cv2.threshold(im_src, 1, 255, cv2.THRESH_BINARY)
    contours, hierarcy = cv2.findContours(im_src, 0, 1)
    # qshow(Alpha)
    draw_1 = origin_img.copy()
    max_black = 0
    max_id = 0
    bound_rect = []
    center_points = []
    max_contour = []
    for i in range(len(contours)):
        bound_rect.append([])

        if len(contours[i]) > max_black:
            max_black = len(contours[i])
            max_id = i
        bound_rect[i] = cv2.boundingRect(cv2.Mat(contours[i]))
        x, y, w, h = bound_rect[i]
        center_points.append([(x + w / 2), (y + h / 2)])
        if ret_mode == 1:
            draw_1 = cv2.rectangle(draw_1, (x, y), (x + w, y + h), (0, 255, 0), 10)

        x, y, w, h = bound_rect[max_id]
        
        if ret_mode == 3:
            max_contour = contours[max_id]

    # qshow(draw_1)
    # print('\"'+name+'\"',':',[y,x,y+h,x+w])
    if ret_mode == 0:
        if len(contours) == 0:
            return None
        return [y, x, y + h, x + w]
    elif ret_mode == 1:
        return draw_1
    elif ret_mode == 2:
        return center_points
    elif ret_mode == 3:
        return max_contour


if __name__ == '__main__':
    # img = refrom_img(cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg"),posi_manager.get_posi_from_str('coming_out_by_space'))
    # cv2.imwrite("assests\\imgs\\common\\coming_out_by_space.jpg", img)
    # get_img_from_imgname(COMING_OUT_BY_SPACE)
    # pname = F_BUTTON
    p = auto_import_img("assests\\imgs\\common\\ui\\" + "bigmap" + ".jpg", "swimming")
    print(p)
