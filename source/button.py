import os
import traceback

import imageio
from PIL import ImageDraw
from util import *
from img_manager import ImgIcon

class Button(ImgIcon):
    def __init__(self, area, color, button, path=None, name=None):
        """Initialize a Button instance.

        Args:
            area (dict[tuple], tuple): Area that the button would appear on the image.
                          (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
            color (dict[tuple], tuple): Color we expect the area would be.
                           (r, g, b)
            button (dict[tuple], tuple): Area to be click if button appears on the image.
                            (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
                            If tuple is empty, this object can be use as a checker.
        Examples:
            BATTLE_PREPARATION = Button(
                area=(1562, 908, 1864, 1003),
                color=(231, 181, 90),
                button=(1562, 908, 1864, 1003)
            )
        """
        self.raw_area = area
        self.raw_color = color
        self.raw_button = button
        self.area = self.raw_area
        self.path = path
        self.raw_file = cv2.imread(os.path.join(root_path, self.path))
        self.raw_name = name
        
        
        bbg_posi = get_bbox(self.raw_file)
        
        
        super().__init__(name=name, path=self.path, is_bbg = True, bbg_posi = bbg_posi)
        
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ___, self.image_binary = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        self.center_point = [bbg_posi[0]+self.image.shape[1]/2, bbg_posi[1]+self.image.shape[0]/2]
        

    def match(self, image, offset=30, threshold=0.85):
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
        
        res = cv2.matchTemplate(self.image, image, cv2.TM_CCOEFF_NORMED)
        _, similarity, _, point = cv2.minMaxLoc(res)
        self._button_offset = area_offset(self.raw_button, offset[:2] + np.array(point))
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
        return self.center_point
    
if __name__ == '__main__':
    a = get_bbox(cv2.imread("assests/imgs/common/ui/emergency_food.jpg"))
    b = crop(cv2.imread("assests/imgs/common/ui/emergency_food.jpg"),a)
    cv2.imshow('123',b)
    cv2.waitKey(0)
    print()