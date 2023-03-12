from source.util import *

from source.common.base_threading import BaseThreading
from source.mission.mission_index import get_mission_object

class MissionManager(BaseThreading):
    def __init__(self):
        super().__init__()
        self.missions_list = []
        
    def add_mission(self, mission_name:str):
        mission = get_mission_object(mission_name)
        self.missions_list.append(mission)
        self._add_sub_threading(mission)
    
    def start_missions(self):
        self.continue_threading()
    
    def loop(self):
        for i in self.missions_list:
            logger.info(f"Mission {i.name} Start.")
            i.continue_threading()
            while 1:
                time.sleep(1)
                if i.pause_threading_flag:
                    break
            logger.info(f"Mission {i.name} End.")
        logger.info(f"All Mission End.")
        self.pause_threading()
        
if __name__ == '__main__':
    mm = MissionManager()
    mm.add_mission("MissionTest")
    mm.start()
    mm.start_missions()
    while 1:
        time.sleep(1)
    pass