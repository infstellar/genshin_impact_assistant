from source.util import *
from source.task.task_template import TaskTemplate
from source.mission.mission_manager import MissionManager


class MissionTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.MM=MissionManager()
        self._add_sub_threading(self.MM)
        self.task_name_list = []
        
    def _analyze_mission_group(self):
        r = load_json(load_json()["mission_group"], f"{CONFIG_PATH}\\mission_groups")
        return r
    
    def exec_task(self):
        
        self.MM.start_missions(self._analyze_mission_group())
        while 1:
            time.sleep(1)
            if self.MM.pause_threading_flag:
                break
        self.task_end()
