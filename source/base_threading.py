import threading
import time


class BaseThreading(threading.Thread):
    """
    基本线程类，实现了暂停线程、继续线程、终止线程。其他具体参考基本线程规范。
    """
    def __init__(self):
        super().__init__()
        self.pause_threading_flag = False
        self.stop_threading_flag = False
        self.working_flag = False
        self.while_sleep = 0.2

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False

    def stop_threading(self):
        self.stop_threading_flag = True

    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            return True

    def get_working_statement(self):
        return self.working_flag

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            return True

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
