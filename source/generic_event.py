from util import *
from interaction_background import InteractionBGD
itt = InteractionBGD()
from base_threading import BaseThreading
import static_lib
from timer_module import Timer



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
            if static_lib.W_KEYDOWN == True:
                if self.w_down_flag == False:
                    self.w_down_flag = True
                    self.w_down_timer.reset()
                if self.w_down_timer.get_diff_time() >= 15:
                    itt.key_down('w')
                    self.w_down_timer.reset()
                    logger.debug("static lib keydown: w")
            else:
                if self.w_down_flag == True:
                    self.w_down_flag = False
                    itt.key_up('w')

logger.debug("start GenericEventThread")
generic_event = GenericEvent()
generic_event.setDaemon(True)
generic_event.start()