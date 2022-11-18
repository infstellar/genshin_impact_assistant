from re import S
from base_threading import BaseThreading
from unit import *
import img_manager
import generic_lib
from interaction_background import InteractionBGD
from pdocr_api import ocr
import posi_manager

class PickupOperator(BaseThreading):

    def __init__(self):
        super().__init__()
        self.itt = InteractionBGD()
        self.pickup_blacklist = load_json("auto_pickup.json")["blacklist"]
        self.pickup_item_list = []
        
    def run(self):
        while 1:
            # time.sleep(0.1)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
                
            ret = self.pickup_recognize()
            if not ret:
                time.sleep(0.1)
                
    def pickup_recognize(self):
        ret = generic_lib.f_recognition(self.itt)
        if ret:
            time.sleep(0.05)
            ret = self.itt.get_img_position(img_manager.F_BUTTON)
            if ret == False:
                return 0
            cap = self.itt.capture()
            cap = self.itt.crop_image(cap, [ret[1]-20, ret[0]+53, ret[1]+54, ret[0]+361])
            cap = self.itt.png2jpg(cap, channel='ui', alpha_num = 180)
            # img_manager.qshow(cap)
            res = ocr.ImgAnalyse(cap)
            if len(res)!=0:
                if res[0][1][0] not in self.pickup_blacklist:
                    self.itt.key_press('f')
                    # self.itt.delay(0)
                    self.pickup_item_list.append(res[0][1][0])
                    logger.info('pickup: '+str(res[0][1][0]))
                    return True
            
        return False  
    
    def find_collector(self):
        pass
                  
if __name__=='__main__':
    po=PickupOperator()
    po.start()
    while 1:
        time.sleep(1)
