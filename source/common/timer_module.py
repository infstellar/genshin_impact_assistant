import time
from source.path_lib import *
import pytz, datetime
from source.logger import *

class Timer:
    def __init__(self, diff_start_time:float=0):
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

    def reset_and_get(self):
        t = self.get_diff_time()
        self.reset()
        return t
    

class AdvanceTimer:
    def __init__(self, limit, count=0):
        """
        Args:
            limit (int, float): Timer limit
            count (int): Timer reach confirm count. Default to 0.
                When using a structure like this, must set a count.
                Otherwise it goes wrong, if screenshot time cost greater than limit.

                if self.appear(MAIN_CHECK):
                    if confirm_timer.reached():
                        pass
                else:
                    confirm_timer.reset()

                Also, It's a good idea to set `count`, to make alas run more stable on slow computers.
                Expected speed is 0.35 second / screenshot.
        """
        self.limit = limit
        self.count = count
        self._current = 0
        self._reach_count = count

    def start(self):
        if not self.started():
            self._current = time.time()
            self._reach_count = 0

        return self

    def started(self):
        return bool(self._current)

    def current(self):
        """
        Returns:
            float
        """
        if self.started():
            return time.time() - self._current
        else:
            return 0.

    def reached(self):
        """
        Returns:
            bool
        """
        self._reach_count += 1
        return time.time() - self._current > self.limit and self._reach_count > self.count

    def reset(self):
        self._current = time.time()
        self._reach_count = 0
        return self

    def clear(self):
        self._current = 0
        self._reach_count = self.count
        return self

    def reached_and_reset(self):
        """
        Returns:
            bool:
        """
        if self.reached():
            self.reset()
            return True
        else:
            return False

    def wait(self):
        """
        Wait until timer reached.
        """
        diff = self._current + self.limit - time.time()
        if diff > 0:
            time.sleep(diff)

    # def show(self):
    #     from source.util import logger
    #     logger.info(str(self))

    def __str__(self):
        return f'Timer(limit={round(self.current(), 3)}/{self.limit}, count={self._reach_count}/{self.count})'

    __repr__ = __str__

class CyclicVelocityDetector(Timer):
    def __init__(self):
        super().__init__()
        
    def get_cyclic_velocity(self):
        dt = self.get_diff_time()
        self.reset()
        return int(1/dt)

class CyclicCounter(AdvanceTimer):
    def __init__(self, limit, count=0):
        super().__init__(limit, count)
        self.times = 0

    def count_times(self):
        if self.reached_and_reset():
            c = self.times
            self.times = 1
            return c
        else:
            self.times += 1
            return False
class TimeoutTimer(Timer):
    def __init__(self, timeout_limit):
        super().__init__()
        self.timeout_limit=timeout_limit
        self.reset()
    
    def set_timeout_limit(self, t):
        """set timeout time.

        Args:
            t (_type_): _description_
        """
        self.timeout_limit = t
        
    def istimeout(self):
        if self.timeout_limit < 0:
            return False
        if self.get_diff_time() >= self.timeout_limit:
            return True
        else:
            return False
        
class FileTimer(Timer):
    def __init__(self, timer_name:str):
        super().__init__()
        self.path = os.path.join(ROOT_PATH, "config\\timer", timer_name+".txt")
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

class Genshin400Timer():
    def __init__(self):
        timer_name = "Genshin400"
        self.path = os.path.join(ROOT_PATH, "config\\timer", timer_name+".txt")
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write("0")
    
    def _get_date(self):
        tz = pytz.timezone('Etc/GMT-4') # 该时区为中国服务器的原神时区，GMT+4
        t = datetime.datetime.now(tz)
        date = t.strftime("%Y%m%d")
        return date
    
    def is_new_day(self):
        with open(self.path, 'r') as f:
            filedate = str(f.read())
        return filedate != self._get_date()
    
    def set_today(self):
        with open(self.path, 'w') as f:
                f.write(self._get_date())
                
class Performance(Timer):
    def __init__(self, diff_start_time: float = 0, output_cycle=5):
        super().__init__(diff_start_time)
        self.output_cycle = output_cycle
        self._output_num = 0
    
    def output_log(self, mess=''):
        if self._output_num%self.output_cycle==0:
            logger.info(f"{mess} {self.reset_and_get()}")
            self._output_num+=1
        else:
            self.reset_and_get()
                   
if __name__ == '__main__':
    a = Genshin400Timer()
    print(a.is_new_day())
    tz = pytz.timezone('Etc/GMT-8')
    t = datetime.datetime.now(tz)
    date = t.strftime("%Y%m%d%H%M%S")
    # print(a.get_diff_time())