import threading
import time
from source.funclib.err_code_lib import ERR_NONE
from source.util import *

class ThreadingStopException(Exception):
    pass


class BaseThreading(threading.Thread):
    """
    基本线程类。
    """
    def __init__(self, thread_name = None):
        super().__init__()
        self._init_succ_flag = False # Use in init slow threads
        self.pause_threading_flag = False
        self.stop_threading_flag = False
        self.working_flag = False
        self.while_sleep = 0.2
        self.last_err_code = ERR_NONE
        self.stop_func_list = []
        self.sub_threading_list = []
        if thread_name != None:
            self.setName(thread_name)

    def pause_threading(self):
        if self.pause_threading_flag != True:
            logger.debug(f"{self.name} pause threading")
            self.pause_threading_flag = True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            logger.debug(f"{self.name} continue threading")
            self.pause_threading_flag = False

    def stop_threading(self):
        logger.debug(f"{self.name} stopping.")
        self.stop_threading_flag = True
        self.pause_threading_flag = True
        self._clean_sub_threading()
    
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            return True

    def get_working_statement(self):
        return not self.pause_threading_flag

    def checkup_stop_func(self):
        pt = time.time()
        def output_log(t):
            if t<0.05:
                pass
            elif t<0.1:
                logger.trace(f"checkup_stop_func spend to long: {t} {self.name}")
            else:
                logger.warning(f"checkup_stop_func spend to long: {t} {self.name}")
        if self.pause_threading_flag or self.stop_threading_flag:
            output_log(time.time()-pt)
            return True
        for i in self.stop_func_list:
            if i():
                output_log(time.time()-pt)
                return True
        output_log(time.time()-pt)
        return False

    def add_stop_func(self, x):
        self.stop_func_list.append(x)
    
    def get_last_err_code(self):
        return self.last_err_code
    
    def get_and_reset_err_code(self):
        erc = self.last_err_code
        self.reset_err_code()
        return erc
    
    def reset_err_code(self):
        self.last_err_code = ERR_NONE
    
    def _add_sub_threading(self, threading_obj, start=True):
        threading_obj.setDaemon(True)
        threading_obj.add_stop_func(self.checkup_stop_func)
        threading_obj.pause_threading()
        if start:
            threading_obj.start()
        self.sub_threading_list.append(threading_obj)
        logger.debug(f"sub threading {threading_obj.name} has been add.")

    def _clean_sub_threading(self):
        for thread_obj in self.sub_threading_list:
            logger.debug(f"{self.name} stop {thread_obj.name}")
            thread_obj.stop_threading()
        self.sub_threading_list = []
    
    def loop(self):
        pass
    
    def run(self):
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                logger.debug(f"{self.name} stop.")
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

            self.loop()

class AdvanceThreading(BaseThreading):
    def __init__(self, thread_name=None):
        super().__init__(thread_name)
    
    def blocking_startup(self, threading_obj:BaseThreading):
        if threading_obj.is_alive():
            threading_obj.stop_threading()
        threading_obj.continue_threading()
        while 1:
            time.sleep(self.while_sleep)
            threading_obj.loop()
            if threading_obj.pause_threading_flag:
                break
        return threading_obj.get_last_err_code()
    
class ThreadBlockingRequest():
    def __init__(self) -> None:
        self.blocking_request_flag = False
        self.reply_request_flag = False
    
    def send_request(self, message=''):
        logger.debug(f"ThreadBlockingRequest sent request: {message}")
        self.blocking_request_flag = True
        
    def reply_request(self):
        if self.reply_request_flag != True:
            logger.debug(f"ThreadBlockingRequest reply request.")
            self.reply_request_flag = True

    def waiting_until_reply(self, stop_func = lambda:False, timeout=10):
        t = time.time()
        while 1:
            time.sleep(0.1)
            if stop_func():
                return False
            if time.time()-t>=10:
                return False
            if self.reply_request_flag:
                return True
    
    def is_blocking(self):
        return self.blocking_request_flag
    
    def recovery_request(self):
        logger.debug(f"ThreadBlockingRequest recovery request.")
        self.blocking_request_flag = False
        self.reply_request_flag = False