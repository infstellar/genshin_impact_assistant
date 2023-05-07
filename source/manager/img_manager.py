import cv2
import numpy as np
from source.manager.util import *

# COMING_OUT_BY_SPACE = 
# IN_DOMAIN = "IN_DOMAIN"
# USE_20RESIN_DOBLE_CHOICES = "USE_20RESIN_DOBLE_CHOICES"
# USE_20X2RESIN_DOBLE_CHOICES = "USE_20X2RESIN_DOBLE_CHOICES"
# F_BUTTON = 'F_BUTTON'
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
class ImgIcon(AssetBase):
    def __init__(self, path=None, name=None, is_bbg=None, alpha=None, bbg_posi=None, cap_posi = None,
                 jpgmode=2, threshold=0.91, win_page = 'all', win_text = None, offset = 0, print_log = LOG_NONE):
        """创建一个img对象，用于图片识别等。

        Args:
            path (str): 图片路径。
            name (str): 图片名称。默认为图片名。
            is_bbg (bool, optional): 是否为黑色背景图片. Defaults to True.
            alpha (int, optional): 截图时的alpha通道，已废弃. Defaults to None.
            bbg_posi (list/None, optional): 黑色背景的图片坐标，默认自动识别坐标. Defaults to None.
            cap_posi (list/str, optional): 截图坐标。注意：可以填入'bbg'字符串关键字，使用bbg坐标; 可以填入'all'字符串关键字，截图全屏. Defaults to None.
            jpgmode (int, optional): 截图时的jpgmode，将废弃. Defaults to 2.
            threshold (float, optional): 匹配阈值. Defaults to 0.91.
            win_page (str, optional): 匹配时的UI界面. Defaults to 'all'.
            win_text (str, optional): 匹配时图片内应该包含的文字. Defaults to None.
            offset (int, optional): 截图范围偏移. Defaults to 0.
            print_log (int, optional): 打印日志模式. Defaults to LOG_NONE.
        """
        if name is None:
            super().__init__(get_name(traceback.extract_stack()[-2]))
        else:
            super().__init__(name)
        
        if path is None:
            path = self.get_img_path()
        
        
        self.origin_path = path
        self.raw_image = cv2.imread(self.origin_path)
        if is_bbg == None:
            if self.raw_image.shape == (1080,1920,3):
                is_bbg = True
            else:
                is_bbg = False        
        self.is_bbg = is_bbg
        self.alpha = alpha
        if self.is_bbg and bbg_posi is None:
            self.bbg_posi = get_bbox(self.raw_image)
        else:
            self.bbg_posi = bbg_posi
        if cap_posi == 'bbg':
            self.cap_posi = self.bbg_posi
        elif cap_posi == None and is_bbg == True:
            self.cap_posi = self.bbg_posi
        elif cap_posi == 'all':
            self.cap_posi = [0, 0, 1920, 1080]
        else:
            self.cap_posi = cap_posi    
        
        if self.cap_posi == None:
            self.cap_posi = [0, 0, 1080, 1920]
        
        self.jpgmode = jpgmode
        self.threshold = threshold
        self.win_page = win_page
        self.win_text = win_text
        self.offset = offset
        self.print_log = print_log
            
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
