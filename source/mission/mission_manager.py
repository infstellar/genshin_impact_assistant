from source.util import *
from source.common.base_threading import AdvanceThreading

from source.mission.index_generator import generate_mission_index
generate_mission_index()
logger.debug(f"generate mission index succ")
import missions.mission_index as MI
    

class MissionManager(AdvanceThreading):
    def __init__(self):
        super().__init__()
        self.missions_list = []
    
    def set_mission_list(self,mission_list:list):
        self.missions_list = mission_list

    def exec_mission(self, mission_name):
        mission = MI.get_mission_object(mission_name)
        if mission != None:
            self._add_sub_threading(mission, start=False)
            self.blocking_startup(mission)
            mission.stop_threading()
        else:
            logger.warning(t2t('Cannot find mission: ')+str(mission_name))
    
    def start_missions(self):
        # self.sub_threading_list = []
        # mission_group = missions_list
        # for i in mission_group:
        #     self.exec_mission(i)
        self.continue_threading()
    
    def loop(self):
        for mission_name in self.missions_list:
            logger.info(f"Mission {mission_name} Start.")
            self.exec_mission(mission_name)
            logger.info(f"Mission {mission_name} End.")
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