from base_threading import BaseThreading
from interaction_background import InteractionBGD

import numpy as np

from timer_module import Timer
from util import *

global W_KEYDOWN, cvAutoTrackerLoop
W_KEYDOWN = False
cvAutoTrackerLoop = None
itt = InteractionBGD()

def get_handle():
    if not config_json["cloud_genshin"]:
        handle = ctypes.windll.user32.FindWindowW(None, '原神')
        if handle != 0:
            return handle
        handle = ctypes.windll.user32.FindWindowW(None, 'Genshin Impact')
        if handle != 0:
            return handle
    else:
        handle = ctypes.windll.user32.FindWindowW("Qt5152QWindowIcon", '云·原神')
        if handle != 0:
            return 331454

class GenericEvent(BaseThreading):
    
    def __init__(self):
        super().__init__()
        self.w_down_timer = Timer()
        self.w_down_flag = False
        self.setName("GenericEvent")
    
    def run(self):
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            '''write your code below'''
            if W_KEYDOWN == True:
                if self.w_down_flag == False:
                    self.w_down_flag = True
                    self.w_down_timer.reset()
                if self.w_down_timer.get_diff_time() >= 15:
                    itt.key_down('w')
                    logger.debug("static lib keydown: w")
            else:
                if self.w_down_flag == True:
                    self.w_down_flag = False
                    itt.key_up('w')
def static_lib_init():
    global W_KEYDOWN, cvAutoTrackerLoop
    logger.debug("import cvAutoTrack")
    import cvAutoTrack
    cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
    cvAutoTrackerLoop.setDaemon(True)
    cvAutoTrackerLoop.start()
    logger.debug("start GenericEventThread")
    generic_event = GenericEvent()
    generic_event.setDaemon(True)
    generic_event.start()
    time.sleep(1)

def while_until_no_excessive_error(stop_func):
    logger.info(_("等待cvautotrack获取坐标"))
    while cvAutoTrackerLoop.is_in_excessive_error():
        if stop_func():
            return 0
        time.sleep(1)

static_lib_init()


if __name__ == '__main__':
    import cv2
    while_until_no_excessive_error()
