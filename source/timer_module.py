import time
import os
from path_lib import *

class Timer:
    def __init__(self, diff_start_time=0):
        self.start_time = time.time()
        self.start_time = self.start_time - diff_start_time
        self.end_time = time.time()

    def reset(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    # def get_delta_time(self):
    #     self.stop()
    #     return self.end_time - self.start_time

    def get_diff_time(self):  # new
        self.stop()
        return self.end_time - self.start_time

    def loop_time(self):
        t = self.get_diff_time()
        self.reset()
        return t


class CyclicVelocityDetector(Timer):
    def __init__(self):
        super().__init__()
        
    def getandset_cyclic_velocity(self):
        dt = self.get_diff_time()
        self.reset()
        return int(1/dt)

class TimeoutTimer(Timer):
    def __init__(self, timeout_limit):
        super().__init__()
        self.timeout_limit=timeout_limit
        self.reset()
    
    def set_timeout_limit(self, t):
        self.timeout_limit = t
        
    def istimeout(self):
        if self.get_diff_time() >= self.timeout_limit:
            return True
        else:
            return False
        
class FileTimer(Timer):
    def __init__(self, timer_name:str):
        super().__init__()
        self.path = os.path.join(root_path, "config\\timer", timer_name+".txt")
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write('0')
                f.close()
        
        with open(self.path, 'r') as f:
            self.start_time = float(f.read())
            f.close()
    
    def reset(self):
        self.start_time = time.time()
        with open(self.path, 'w') as f:
            f.write(str(self.start_time))
            f.close()
            
if __name__ == '__main__':
    a = FileTimer("test1")
    print(a.get_diff_time())