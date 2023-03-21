from source.util import *

from source.common.base_threading import AdvanceThreading
from source.mission.mission_index import get_mission_object

class MissionManager(AdvanceThreading):
    def __init__(self):
        super().__init__()
        self.missions_list = []
        
    def add_mission(self, mission_name:str):
        mission = get_mission_object(mission_name)
        self.missions_list.append(mission)
        self._add_sub_threading(mission, start=False)
    
    def start_missions(self,mission_group):
        self.sub_threading_list = []
        self.missions_list = []
        for i in mission_group:
            self.add_mission(i)
        self.continue_threading()
    
    def loop(self):
        for mission in self.missions_list:
            logger.info(f"Mission {mission.name} Start.")
            self.blocking_startup(mission)
            logger.info(f"Mission {mission.name} End.")
            mission.stop_threading()
        logger.info(f"All Mission End.")
        self.pause_threading()
        
if __name__ == '__main__':
    mm = MissionManager()
    # mm.add_mission()
    mm.start()
    mm.start_missions(["MissionCrystalfly","MissionCrystalfly"])
    while 1:
        time.sleep(1)
    pass