from util import *
from img_manager import ImgIcon, qshow, LOG_NONE, LOG_ALL, LOG_WHEN_FALSE, LOG_WHEN_TRUE

class Button(ImgIcon):
    def __init__(self, path, button = None, name="button", black_offset=10, threshold=0.85, win_page = "all", win_text = None, print_log = LOG_NONE):
        self.path = path
        self.raw_file = cv2.imread(os.path.join(root_path, self.path))
        self.raw_name = name
        
        
        bbg_posi = get_bbox(self.raw_file, offset=black_offset)
        self.area = bbg_posi
        if button is None:
            self.button = self.area
        else:
            self.button = button
        super().__init__(name=name, path=self.path, is_bbg = True, bbg_posi = bbg_posi, jpgmode = 0, threshold=threshold, win_page=win_page, win_text=win_text, print_log=print_log)
        
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ___, self.image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        self.center_point = [bbg_posi[0]+self.image.shape[1]/2, bbg_posi[1]+self.image.shape[0]/2]
    
    def click_position(self):
        return [int(self.center_point[0]), int(self.center_point[1])]

button_esc_page = Button(path="assests\\imgs\\common\\ui\\emergency_food.jpg", print_log=LOG_WHEN_TRUE)
button_time_page = Button(path="assests\\imgs\\common\\ui\\switch_to_time_menu.jpg", black_offset = 15, print_log=LOG_WHEN_TRUE)
button_exit = Button(path="assests\\imgs\\common\\button\\button_exit.jpg", print_log=LOG_WHEN_TRUE)
button_all_character_died = Button(path="assests\\imgs\\cn\\all_character_died.jpg", name="all_character_died", 
                                   threshold=0.988, win_text="复苏", print_log=LOG_WHEN_TRUE)
button_ui_cancel = Button(path="assests\\imgs\\common\\ui\\ui_cancel.jpg", name="button_ui_cancel", print_log=LOG_WHEN_TRUE)

if __name__ == '__main__':
    button_ui_cancel.show_image()
print()