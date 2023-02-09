from source.util import *
from source.interaction import interaction_core
itt = interaction_core.InteractionBGD()
from source.common.base_threading import BaseThreading
from source.funclib import static_lib
from source.base.timer_module import Timer



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
def static_lib_init():
    global W_KEYDOWN, cvAutoTrackerLoop
    logger.debug("import cvAutoTrack")
    from source.api import cvAutoTrack
    cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
    cvAutoTrackerLoop.setDaemon(True)
    cvAutoTrackerLoop.start()
    time.sleep(1)

def while_until_no_excessive_error(stop_func):
    logger.info(t2t("等待cvautotrack获取坐标"))
    cvAutoTrackerLoop.start_sleep_timer.reset()
    while cvAutoTrackerLoop.is_in_excessive_error():
        if stop_func():
            return 0
        time.sleep(1)

static_lib_init()


logger.debug("start GenericEventThread")
generic_event = GenericEvent()
generic_event.setDaemon(True)
generic_event.start()