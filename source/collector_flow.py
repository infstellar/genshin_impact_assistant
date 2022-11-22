from util import *
import math
import flow_state as ST
import cvAutoTrack
from interaction_background import InteractionBGD
import teyvat_move_controller
import generic_lib
import img_manager
import pickup_operator
import movement
import posi_manager
import big_map
import combat_loop
import pdocr_api
from base_threading import BaseThreading
import pyautogui
import interaction_background
import text_manager
import timer_module
import combat_lib

class CollectorFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False

    def stop_threading(self):
        self.stop_threading_flag = True

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
        '''write your code below'''