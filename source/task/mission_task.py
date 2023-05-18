from source.util import *
from source.task.task_template import TaskTemplate
from source.mission.mission_manager import MissionManager


class MissionTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.name = "MissionTask"
        self.MM=MissionManager()
        self._add_sub_threading(self.MM)
        self.task_name_list = []
        
    def _analyze_mission_group(self):
        r = load_json('mission_group.json', f"{CONFIG_PATH}\\mission")
        return r
    
    def loop(self):
        self.MM.set_mission_list(self._analyze_mission_group())
        self.MM.start_missions()
        while 1:
            if self.checkup_stop_func():return
            time.sleep(1)
            if self.MM.pause_threading_flag:
                break
        self.pause_threading()
