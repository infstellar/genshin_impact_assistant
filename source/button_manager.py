from util import *
from img_manager import ImgIcon, qshow

class Button(ImgIcon):
    def __init__(self, path, button = None, name=None, black_offset=10, threshold=0.85):
        self.path = path
        self.raw_file = cv2.imread(os.path.join(root_path, self.path))
        self.raw_name = name
        
        
        bbg_posi = get_bbox(self.raw_file, offset=black_offset)
        self.area = bbg_posi
        if button is None:
            self.button = self.area
        else:
            self.button = button
        
        super().__init__(name=name, path=self.path, is_bbg = True, bbg_posi = bbg_posi, jpgmode = 0, threshold=threshold)
        
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ___, self.image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        self.center_point = [bbg_posi[0]+self.image.shape[1]/2, bbg_posi[1]+self.image.shape[0]/2]
    
    def match(self, image, offset=10, threshold=0.85):
        """Detects button by template matching. To Some button, its location may not be static.
        Args:
            image: Screenshot.
            offset (int, tuple): Detection area offset.
            threshold (float): 0-1. Similarity.
        Returns:
            bool.
        """
        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        image = crop(image, offset + self.area)
        # qshow(image)
        # qshow(self.image)
        res = cv2.matchTemplate(self.image, image, cv2.TM_CCOEFF_NORMED)
        _, similarity, _, point = cv2.minMaxLoc(res)
        # self._button_offset = area_offset(self.raw_button, offset[:2] + np.array(point))
        return similarity > threshold
    
    def match_binary(self, image, offset=30, threshold=0.85):
        """Detects button by template matching. To Some button, its location may not be static.
           This method will apply template matching under binarization.
        Args:
            image: Screenshot.
            offset (int, tuple): Detection area offset.
            threshold (float): 0-1. Similarity.
        Returns:
            bool.
        """

        if isinstance(offset, tuple):
            if len(offset) == 2:
                offset = np.array((-offset[0], -offset[1], offset[0], offset[1]))
            else:
                offset = np.array(offset)
        else:
            offset = np.array((-3, -offset, 3, offset))
        image = crop(image, offset + self.area)

        # graying
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # binarization
        _, image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # template matching
        res = cv2.matchTemplate(self.image_binary, image_binary, cv2.TM_CCOEFF_NORMED)
        _, similarity, _, point = cv2.minMaxLoc(res)
        self._button_offset = area_offset(self.raw_button, offset[:2] + np.array(point))
        return similarity > threshold
    
    def click_position(self):
        return [int(self.center_point[0]), int(self.center_point[1])]

button_esc_page = Button(path="assests\\imgs\\common\\ui\\emergency_food.jpg")
button_time_page = Button(path="assests\\imgs\\common\\ui\\switch_to_time_menu.jpg", black_offset = 15)
button_exit = Button(path="assests\\imgs\\common\\button\\button_exit.jpg")
button_all_character_died = Button(path="assests\\imgs\\cn\\all_character_died.jpg", name="all_character_died", threshold=0.99)

if __name__ == '__main__':
    button_time_page.show_image()
print()