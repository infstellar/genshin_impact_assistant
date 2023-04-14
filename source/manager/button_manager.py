from source.manager.img_manager import ImgIcon, LOG_NONE, LOG_WHEN_TRUE
from source.manager.util import *
from source.common.timer_module import AdvanceTimer


CLICK_STATIC = 0
CLICK_DYNAMIC = 1

def get_cap_posi(path, black_offset):
    raw_file = cv2.imread(os.path.join(ROOT_PATH, path))
    bbg_posi = get_bbox(raw_file, black_offset=black_offset)
    return bbg_posi

class Button(ImgIcon):
    def __init__(self, path=None, name=None, black_offset=15, is_bbg = True , threshold=0.9,offset = 0, win_page = "all", win_text = None, print_log = LOG_NONE, cap_posi=None, click_offset=None):
        if name is None:
            name = get_name(traceback.extract_stack()[-2])
        super().__init__(path=path, name=name, jpgmode = 0, is_bbg = is_bbg,
                         threshold=threshold, win_page=win_page, win_text=win_text, print_log=print_log, cap_posi=cap_posi, offset = offset)
        if click_offset is None:
            self.click_offset=np.array([0,0])
        else:
            self.click_offset=np.array(click_offset)
        # self.path = path.replace("$lang$", global_lang)
        # self.raw_file = cv2.imread(os.path.join(root_path, self.path))
        # self.raw_name = name
        
        # self.area = bbg_posi
        # if button is None:
        #     self.button = self.area
        # else:
        #     self.button = button
        
        # qshow(self.image)
        # image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # ___, self.image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.is_bbg:
            self.center_point = [self.bbg_posi[0]+self.image.shape[1]/2, self.bbg_posi[1]+self.image.shape[0]/2]
        self.click_retry_timer = AdvanceTimer(3).start()
        self.click_fail_timer = AdvanceTimer(1,60).start() # 60 retry max, 180 sec max 
        self.click_fail_timer.reset()
    
    
    
    def click_position(self):
        # 在一个范围内随机生成点击位置 还没写
        return [int(self.center_point[0])+self.click_offset[0], int(self.center_point[1])+self.click_offset[1]]

if __name__ == '__main__':
    pass # button_ui_cancel.show_image()
# print()