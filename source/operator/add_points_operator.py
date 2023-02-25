from source.util import *
from source.interaction.minimap_tracker import tracker
from source.common.base_threading import BaseThreading


class add_point(BaseThreading):

    def __init__(self):
        super().__init__()

    def get_points(self):
        tracker.get_position()
        pass



    def run(self):
        '''if you're using this class, copy this'''
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
    



if __name__ == '__main__':
    pass