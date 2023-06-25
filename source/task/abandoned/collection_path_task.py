from source.util import *
from source.flow.path_recorder_flow import PathRecorderController
from source.task.task_template import TaskTemplate
from source.interaction.interaction_core import itt
from source.manager import asset, text_manager
from common import flow_state as ST
from source.task import task_id as TI
from source.funclib.err_code_lib import ERR_NONE, ERR_STUCK, ERR_PASS
from source.path_lib import *

class CollectionPathTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.cpc = PathRecorderController()
        self._add_sub_threading(self.cpc)
        
        self.cpc.continue_threading()
        self.json_name = str(time.time())
        
    def run(self) -> None:
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
            
    def end_task(self):
        self.cpc.pause_threading()
        # save_json(self.cpc.flow_connector.total_collection_list, self.json_name, f"{CONFIG_PATH}\\collection_path")
        super().end_task()
        
if __name__ == '__main__':
    cpt = CollectionPathTask()
    cpt.start()
    while 1:
        time.sleep(1)