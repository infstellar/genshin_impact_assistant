from unit import *
from base_threading import BaseThreading

class PickupOperator(BaseThreading):
    
    def __init__(self):
        super().__init__()
        
    def operate(self):
        self.pick_flag=True
        
    def run(self):
        while 1:
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True