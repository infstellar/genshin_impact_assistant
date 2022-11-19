import interaction_background
import threading
import timer_module

from util import *


class Video_Cap(threading.Thread):
    def __init__(self):
        threading.Thread.__init__()
        self.itt = interaction_background.InteractionBGD()
        self.latest_cap = None
        self.event = {}
        self.ret_event = {}
        self.delay = (1 / 10)
        self.video_timer = timer_module.Timer()
        self.stop_flag = False
        pass

    def registered_events(self, event_func: function, ret_func: function, tag: str):
        self.event[tag] = event_func
        self.ret_event[tag] = ret_func

    def logout(self, tag):
        del self.event[tag]
        del self.ret_event[tag]

    def run(self):
        while 1:
            if self.stop_flag:
                time.sleep(1)
                continue

            self.video_timer.reset()
            self.latest_cap = self.itt.capture()

            for i in range(len(self.event)):  # event check
                if self.event[i](self.latest_cap):
                    self.ret_event[i](self.latest_cap)  # do func like: change other thread's variable

            dt = self.delay - self.video_timer.getDiffTime()
            if dt >= 0:
                time.sleep(dt)


video_cap = Video_Cap()
