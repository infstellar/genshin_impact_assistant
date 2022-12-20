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

class ImgIcon:
    def __init__(self, name, path, is_bbg=True, matching_rate=None, alpha=None, bbg_posi=None, cap_posi=[0, 0, 1080, 1920],
                 jpgmode=2, threshold=0.95):
        self.name = name
        self.path = os.path.join(root_path, path)
        self.is_bbg = is_bbg
        self.mr = matching_rate
        self.alpha = alpha
        self.bbg_posi = bbg_posi
        self.jpgmode = jpgmode
        self.threshold = threshold
        self.raw_image = cv2.imread(self.path)
        
        if self.is_bbg and self.bbg_posi is None:
            self.bbg_posi = get_bbox(self.raw_image)
        
        if cap_posi == 'bbg':
            self.cap_posi = self.bbg_posi
        else:
            self.cap_posi = cap_posi
        self.cap_center_position_xy = [(self.cap_posi[1]+self.cap_posi[3])/2, (self.cap_posi[0]+self.cap_posi[2])/2]
        

        if self.is_bbg:
            self.image = crop(self.raw_image, self.bbg_posi)
        else:
            self.image = self.raw_image.copy()


imgs_dict = {}

COMING_OUT_BY_SPACE = ImgIcon(name="coming_out_by_space", path="assests\\imgs\\common\\coming_out_by_space.jpg",
                              is_bbg=True, bbg_posi=[1379,505,  1447,568, ], cap_posi='bbg', threshold=0.8, )
IN_DOMAIN = ImgIcon(name="IN_DOMAIN", path="assests\\imgs\\common\\IN_DOMAIN.jpg",
                    is_bbg=True, bbg_posi=[25,112,  52, 137, ], cap_posi='bbg')
USE_20RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20RESIN_DOBLE_CHOICES",
                                    path="assests\\imgs\\common\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                    is_bbg=True, bbg_posi=[985, 724, 1348, 791 ], cap_posi='bbg')
USE_20X2RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20X2RESIN_DOBLE_CHOICES",
                                      path="assests\\imgs\\common\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                      is_bbg=True, bbg_posi=[567,726 ,934, 793 ], cap_posi='bbg')
F_BUTTON = ImgIcon(name="F_BUTTON", path="assests\\imgs\\common\\F_BUTTON.jpg",
                   is_bbg=True, bbg_posi=[1104,526 , 1128,550 ], cap_posi=[1079,350 ,1162, 751 ],
                   threshold=0.92)
bigmap_TeleportWaypoint = ImgIcon(name="bigmap_TeleportWaypoint",
                                  path="assests\\imgs\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
smallmap_AbyssMage = ImgIcon(name="smallmap_AbyssMage", path="assests\\imgs\\map\\small_map\\enemies\\AbyssMage.jpg",
                             is_bbg=False)
bigmap_AbyssMage = ImgIcon(name="bigmap_AbyssMage", path="assests\\imgs\\map\\big_map\\enemies\\AbyssMage.jpg",
                           is_bbg=False)
motion_swimming = ImgIcon(name="motion_swimming", path="assests\\imgs\\common\\motion_swimming.jpg",
                          is_bbg=True, bbg_posi=[1808,968,  1872,1016 ], cap_posi='bbg')
motion_climbing = ImgIcon(name="motion_climbing", path="assests\\imgs\\common\\motion_climbing.jpg",
                          is_bbg=True, bbg_posi=[1706,960,1866, 1022 ], cap_posi='bbg')
motion_flying = ImgIcon(name="motion_flying", path="assests\\imgs\\common\\motion_flying.jpg",
                        is_bbg=True, bbg_posi=[1706,960, 1866, 1022 ], cap_posi='bbg')
ui_main_win = ImgIcon(name="ui_main_win", path="assests\\imgs\\common\\ui\\emergency_food.jpg",
                      is_bbg=True, bbg_posi=[39,34, 73, 78 ], cap_posi='bbg')
ui_bigmap_win = ImgIcon(name="ui_bigmap_win", path="assests\\imgs\\common\\ui\\bigmap.jpg",
                        is_bbg=True, bbg_posi=[1591,36,1614, 59 ], cap_posi='bbg')
ui_esc_menu = ImgIcon(name="ui_esc_menu", path="assests\\imgs\\common\\ui\\esc_menu.jpg",
                        is_bbg=True, cap_posi='bbg')
ui_switch_to_time_menu = ImgIcon(name="ui_switch_to_time_menu", path="assests\\imgs\\common\\ui\\switch_to_time_menu.jpg",
                        is_bbg=True, cap_posi='bbg')
ui_time_menu_core = ImgIcon(name="ui_time_menu_core", path="assests\\imgs\\common\\ui\\time_menu_core.jpg",
                        is_bbg=True, cap_posi='bbg')

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

qshow(ui_time_menu_core.image)
def match_img(self, img_name: str, is_show_res: bool = False):
    image = self.capture()
    # image = (image/(image[3]+10)).astype(int)

    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread('imgs/' + img_name, cv2.IMREAD_UNCHANGED)
    # template = template/template[3]
    # 取出Alpha通道
    alpha = template[:, :, 3]
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if is_show_res:
        cv2.imshow('template', template)
        cv2.imshow('gray', gray)
        cv2.waitKey()
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = top_left[0] + w, top_left[1] + h
    # 在窗口截图中匹配位置画红色方框
    if is_show_res:
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imshow('Match Template', image)
        cv2.waitKey()
    matching_rate = max_val
    return matching_rate, top_left, bottom_right

def match_multiple_img(self, img, template, is_gray=False, is_show_res: bool = False, ret_mode=IMG_POINT,
                        threshold=0.98):
    """多图片识别

    Args:
        img (numpy): 截图Mat
        template (numpy): 要匹配的样板图片
        is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
        is_show_res (bool, optional): 结果显示. Defaults to False.
        ret_mode (int, optional): 返回值模式,目前只有IMG_POINT. Defaults to IMG_POINT. 
        threshold (float, optional): 最小匹配度. Defaults to 0.98.

    Returns:
        list[list[], ...]: 匹配成功的坐标列表
    """
    if is_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    res_posi = []
    result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
    # img_manager.qshow(template)
    h, w = template.shape[:2]  # 获取模板高和宽
    loc = np.where(result >= threshold)  # 匹配结果小于阈值的位置
    for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
        right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
        if ret_mode == IMG_RECT:
            res_posi.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        else:
            res_posi.append([pt[0] + w / 2, pt[1] + h / 2])
        # cv2.rectangle((show_img), pt, right_bottom, (0,0,255), 2) #绘制匹配到的矩阵
    if is_show_res:
        show_img = img.copy()
        # print(*loc[::-1])
        for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
            right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
            cv2.rectangle((show_img), pt, right_bottom, (0, 0, 255), 2)  # 绘制匹配到的矩阵
        cv2.imshow("img", show_img)
        cv2.imshow("template", template)
        cv2.waitKey(0)  # 获取按键的ASCLL码
        cv2.destroyAllWindows()  # 释放所有的窗口

    return res_posi

def similar_img(self, img, target, is_gray=False, is_show_res: bool = False, ret_mode=IMG_RATE):
    """单个图片匹配

    Args:
        img (numpy): Mat
        template (numpy): 要匹配的样板图片
        is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
        is_show_res (bool, optional): 结果显示. Defaults to False.
        ret_mode (int, optional): 返回值模式. Defaults to IMG_RATE.

    Returns:
        float/(float, list[]): 匹配度或者匹配度和它的坐标
    """
    if is_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        target = cv2.cvtColor(target, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    # img_manager.qshow(img)
    result = cv2.matchTemplate(img, target, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if is_show_res:
        cv2.waitKey()
    # 在窗口截图中匹配位置画红色方框
    matching_rate = max_val
    if ret_mode == IMG_RATE:
        return matching_rate
    elif ret_mode == IMG_POSI:
        return matching_rate, max_loc

def get_img_position(self, imgicon: ImgIcon, is_gray=False, is_log=False):
    """获得图片在屏幕上的坐标

    Args:
        imgicon (img_manager.ImgIcon): imgicon对象
        is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
        is_log (bool, optional): 是否打印日志. Defaults to False.

    Returns:
        list[]/bool: 返回坐标或False
    """
    upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    # if imgname in img_manager.alpha_dict:
    #     cap = self.capture()
    #     cap = self.png2jpg(cap, bgcolor='black', channel='ui', alpha_num=img_manager.alpha_dict[imgname])
    # else:
    cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)

    matching_rate, max_loc = self.similar_img(cap, imgicon.image, ret_mode=IMG_POSI)

    if is_log:
        logger.debug(
            'imgname: ' + imgicon.name + 'max_loc: ' + str(max_loc) + ' |function name: ' + upper_func_name)

    if matching_rate >= imgicon.threshold:
        return max_loc
    else:
        return False

def is_img_existence(self, imgicon: ImgIcon, is_gray=False, is_log=False):
    """检测图片是否存在

    Args:
        imgicon (img_manager.ImgIcon): imgicon对象
        is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
        is_log (bool, optional): 是否打印日志. Defaults to False.

    Returns:
        bool: bool
    """
    upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

    cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)

    matching_rate = self.similar_img(cap, imgicon.image)
    if is_log:
        logger.debug(
            'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                matching_rate) + ' |function name: ' + upper_func_name)

    return matching_rate >= imgicon.threshold


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
    p = auto_import_img("assests\\imgs\\common\\ui\\" + "time_menu_core" + ".jpg", "swimming")
    print(p)
