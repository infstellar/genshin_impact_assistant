import cv2
import numpy as np
from util import *

import posi_manager

# COMING_OUT_BY_SPACE = 
IN_DOMAIN = "IN_DOMAIN"
USE_20RESIN_DOBLE_CHOICES = "USE_20RESIN_DOBLE_CHOICES"
USE_20X2RESIN_DOBLE_CHOICES = "USE_20X2RESIN_DOBLE_CHOICES"
F_BUTTON = 'F_BUTTON'
IMG_RATE = 0
IMG_POSI = 1
IMG_POINT = 2
IMG_RECT = 3

LOG_NONE = 0
LOG_WHEN_TRUE = 1
LOG_WHEN_FALSE = 2
LOG_ALL = 3

def qshow(img1):
    cv2.imshow('123', img1)
    cv2.waitKey(0)
class ImgIcon:
    def __init__(self, name, path, is_bbg=True, matching_rate=None, alpha=None, bbg_posi=None, cap_posi=[0, 0, 1080, 1920],
                 jpgmode=2, threshold=0.91, win_page = 'all', win_text = None, offset = 0, print_log = LOG_NONE):
        self.name = name
        self.origin_path = os.path.join(root_path, path)
        self.path = self.origin_path.replace("$lang$", global_lang)
        self.is_bbg = is_bbg
        self.mr = matching_rate
        self.alpha = alpha
        self.bbg_posi = bbg_posi
        self.jpgmode = jpgmode
        self.threshold = threshold
        self.raw_image = cv2.imread(self.path)
        self.win_page = win_page
        self.win_text = win_text
        self.offset = offset
        self.print_log = print_log
        
        if self.is_bbg and self.bbg_posi is None:
            self.bbg_posi = get_bbox(self.raw_image)
        
        if cap_posi == 'bbg':
            self.cap_posi = self.bbg_posi
        else:
            self.cap_posi = cap_posi
            
        if self.offset != 0:
            self.cap_posi = list(np.array(self.cap_posi) + np.array([-self.offset, -self.offset, self.offset, self.offset]))
            
        self.cap_center_position_xy = [(self.cap_posi[0]+self.cap_posi[2])/2, (self.cap_posi[1]+self.cap_posi[3])/2]
        

        if self.is_bbg:
            self.image = crop(self.raw_image, self.bbg_posi)
        else:
            self.image = self.raw_image.copy()
    
    def show_image(self):
        cv2.imshow('123', self.image)
        cv2.waitKey(0)
        
    def is_print_log(self, b:bool):
        if b:
            if self.print_log == LOG_WHEN_TRUE or self.print_log == LOG_ALL:
                return True
            else:
                return False
        else:
            if self.print_log == LOG_WHEN_FALSE or self.print_log == LOG_ALL:
                return True
            else:
                return False

imgs_dict = {}

COMING_OUT_BY_SPACE = ImgIcon(name="coming_out_by_space", path="assets\\imgs\\common\\coming_out_by_space.jpg",
                              is_bbg=True, bbg_posi=[1379,505,  1447,568, ], cap_posi='bbg', threshold=0.8, print_log=LOG_WHEN_TRUE)
IN_DOMAIN = ImgIcon(name="IN_DOMAIN", path="assets\\imgs\\common\\IN_DOMAIN.jpg",
                    is_bbg=True, bbg_posi=[25,112,  52, 137, ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20RESIN_DOBLE_CHOICES",
                                    path="assets\\imgs\\$lang$\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                    is_bbg=True, bbg_posi=[985, 724, 1348, 791 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20X2RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20X2RESIN_DOBLE_CHOICES",
                                      path="assets\\imgs\\$lang$\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                      is_bbg=True, bbg_posi=[567,726 ,934, 793 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
F_BUTTON = ImgIcon(name="F_BUTTON", path="assets\\imgs\\common\\F_BUTTON.jpg",
                   is_bbg=True, bbg_posi=[1104,526 , 1128,550 ], cap_posi=[1079,350 ,1162, 751 ],
                   threshold=0.92, print_log=LOG_WHEN_TRUE)
bigmap_TeleportWaypoint = ImgIcon(name="bigmap_TeleportWaypoint",
                                  path="assets\\imgs\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
bigmap_GodStatue = ImgIcon(name="bigmap_GodStatue",
                                  path="assets\\imgs\\map\\big_map\\points\\GodStatue.jpg",
                                  is_bbg=False)
smallmap_AbyssMage = ImgIcon(name="smallmap_AbyssMage", path="assets\\imgs\\map\\small_map\\enemies\\AbyssMage.jpg",
                             is_bbg=False)
bigmap_AbyssMage = ImgIcon(name="bigmap_AbyssMage", path="assets\\imgs\\map\\big_map\\enemies\\AbyssMage.jpg",
                           is_bbg=False)
motion_swimming = ImgIcon(name="motion_swimming", path="assets\\imgs\\common\\motion_swimming.jpg",
                          is_bbg=True, bbg_posi=[1808,968,  1872,1016 ], cap_posi='bbg')
motion_climbing = ImgIcon(name="motion_climbing", path="assets\\imgs\\common\\motion_climbing.jpg",
                          is_bbg=True, bbg_posi=[1706,960,1866, 1022 ], cap_posi='bbg')
motion_flying = ImgIcon(name="motion_flying", path="assets\\imgs\\common\\motion_flying.jpg",
                        is_bbg=True, bbg_posi=[1706,960, 1866, 1022 ], cap_posi='bbg')
ui_main_win = ImgIcon(name="ui_main_win", path="assets\\imgs\\common\\ui\\emergency_food.jpg",
                      is_bbg=True, bbg_posi=[39,34, 73, 78 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_bigmap_win = ImgIcon(name="ui_bigmap_win", path="assets\\imgs\\common\\ui\\bigmap.jpg",
                        is_bbg=True, bbg_posi=[1591,36,1614, 59 ], cap_posi=[1300,36,1750, 59 ], print_log=LOG_WHEN_TRUE, threshold=0.95, offset=10)
ui_esc_menu = ImgIcon(name="ui_esc_menu", path="assets\\imgs\\common\\ui\\esc_menu.jpg",
                        is_bbg=True, cap_posi='bbg', jpgmode=0, print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_switch_to_time_menu = ImgIcon(name="ui_switch_to_time_menu", path="assets\\imgs\\common\\ui\\switch_to_time_menu.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
ui_time_menu_core = ImgIcon(name="ui_time_menu_core", path="assets\\imgs\\common\\ui\\time_menu_core.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.89)
bigmap_choose_area = ImgIcon(name="bigmap_choose_area", path="assets\\imgs\\common\\ui\\bigmap_choose_area.jpg", is_bbg=True, cap_posi='bbg')
bigmap_tp = ImgIcon(name="bigmap_tp", path="assets\\imgs\\$lang$\\bigmap_tp.jpg", is_bbg=True, cap_posi='bbg')

# qshow(ui_esc_menu.image)

# character_died.show_image()


matching_rate_dict = {
    "coming_out_by_space": 0.9,
    "IN_DOMAIN": 0.98,
    "USE_20RESIN_DOBLE_CHOICES": 0.88,
    "USE_20X2RESIN_DOBLE_CHOICES": 0.88,
}

alpha_dict = {
    "F_BUTTON": 254
}




# qshow(ui_time_menu_core.image)


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
    # img = refrom_img(cv2.imread("assets\\imgs\\common\\coming_out_by_space.jpg"),posi_manager.get_posi_from_str('coming_out_by_space'))
    # cv2.imwrite("assets\\imgs\\common\\coming_out_by_space.jpg", img)
    # get_img_from_imgname(COMING_OUT_BY_SPACE)
    # pname = F_BUTTON
    # p = auto_import_img("assets\\imgs\\common\\ui\\" + "time_menu_core" + ".jpg", "swimming")
    # print(p)
    pass
