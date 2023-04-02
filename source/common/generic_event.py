from source.util import *
from source.interaction.interaction_core import itt
from source.common.base_threading import BaseThreading
from source.common import static_lib
from common.timer_module import Timer
from source.path_lib import CONFIG_PATH_SETTING
if load_json("config.json", CONFIG_PATH_SETTING)["interaction_mode"] == INTERACTION_DESKTOP_BACKGROUND:
    from source.interaction.interaction_dm import unbind, bind

global W_KEYDOWN
class GenericEvent(BaseThreading):
    
    def __init__(self):
        super().__init__()
        self.w_down_timer = Timer()
        self.w_down_flag = False
        self.setName("GenericEvent")
        self.while_sleep = 2
            
    def run(self) -> None:
        '''if you're using this class, copy this'''
        pt = time.time()
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return

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
            dilation_rate = self.while_sleep/(time.time()-pt)
            if dilation_rate<0.99:
                logger.trace(f"time dilation rate: {dilation_rate}")
            pt = time.time()
            if INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND or INTERACTION_DESKTOP:
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
            
            if INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND:
                win_name = get_active_window_process_name()
                if win_name in PROCESS_NAME:
                    unbind()
                    while 1:
                        if get_active_window_process_name() not in PROCESS_NAME:
                            logger.info(t2t("恢复操作"))
                            break
                        logger.info(t2t("当前窗口焦点为") + str(win_name) + t2t("是原神窗口") + str(PROCESS_NAME) + t2t("，操作暂停 ") + str(5 - (time.time()%5)) +t2t(" 秒"))
                        time.sleep(5 - (time.time()%5))
                    bind()
                    
                    
            

if INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND:
    import keyboard
    keyboard.add_hotkey("ctrl+alt+9", unbind)
    keyboard.add_hotkey("ctrl+alt+shift+9", bind)
logger.debug("start GenericEventThread")
generic_event = GenericEvent()
generic_event.setDaemon(True)
generic_event.start()