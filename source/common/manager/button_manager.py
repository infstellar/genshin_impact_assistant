from util import *
from img_manager import ImgIcon, qshow, LOG_NONE, LOG_ALL, LOG_WHEN_FALSE, LOG_WHEN_TRUE

def get_cap_posi(path, black_offset):
    path = path.replace("$lang$", global_lang)
    raw_file = cv2.imread(os.path.join(root_path, path))
    bbg_posi = get_bbox(raw_file, black_offset=black_offset)
    return bbg_posi

class Button(ImgIcon):
    def __init__(self, path, button = None, name="button", black_offset=15, threshold=0.85, win_page = "all", win_text = None, print_log = LOG_NONE):
        bbg_posi = get_cap_posi(path, black_offset)
        super().__init__(name=name, path=path, is_bbg = True, bbg_posi = bbg_posi, jpgmode = 0, 
                         threshold=threshold, win_page=win_page, win_text=win_text, print_log=print_log, cap_posi='bbg')
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
        
        self.center_point = [bbg_posi[0]+self.image.shape[1]/2, bbg_posi[1]+self.image.shape[0]/2]
    
    
    
    def click_position(self):
        return [int(self.center_point[0]), int(self.center_point[1])]

button_esc_page = Button(name="button_esc_page", path="assets\\imgs\\common\\ui\\emergency_food.jpg", print_log=LOG_WHEN_TRUE)
button_time_page = Button(name="button_time_page",path="assets\\imgs\\common\\ui\\switch_to_time_menu.jpg", black_offset = 15, print_log=LOG_WHEN_TRUE)
button_exit = Button(path="assets\\imgs\\common\\button\\button_exit.jpg", print_log=LOG_WHEN_TRUE)
button_all_character_died = Button( name="all_character_died", path="assets\\imgs\\$lang$\\all_character_died.jpg", 
                                   threshold=0.988, win_text="复苏", print_log=LOG_WHEN_TRUE)
button_ui_cancel = Button(name="button_ui_cancel", path="assets\\imgs\\common\\ui\\ui_cancel.jpg",  print_log=LOG_WHEN_TRUE)

if __name__ == '__main__':
    button_ui_cancel.show_image()
# print()