from source.util import *
import keyboard
from source.task.task_template import TaskTemplate
from source.common.base_threading import BaseThreading


COLLECTION_PATH_TASK = "CollectionPathTask"
DOMAIN_TASK = "DomainTask"
    
class TaskManager(BaseThreading):
    def __init__(self) -> None:
        super().__init__()
        self.reg_task_flag = False
        self.curr_task = None # type: TaskTemplate
        self.task_list = []
        self.get_task_list = lambda:["TestTask"]
        self.start_tasklist_flag = False
    
    def append_task(self, task_name):
        self.task_list.append(task_name)

    def clear_task_list(self):
        self.task_list = []

    def remove_task(self, task_name) -> bool:
        for i in range(len(self.task_list)):
            if self.task_list[i] == task_name:
                del(self.task_list[i])
                return True
        return False
        
    def start_stop_tasklist(self):
        self.start_tasklist_flag = not self.start_tasklist_flag

    def start_stop_task(self, task_name):
        if not self.reg_task_flag:
            if task_name == COLLECTION_PATH_TASK:
                from source.task.collection_path_task import CollectionPathTask
                self.curr_task = CollectionPathTask()
                self.curr_task.start()
                self.reg_task_flag = True
                logger.info(t2t("Task CollectionPathTask Start."))

            elif task_name == DOMAIN_TASK:
                from source.task.domain_task import DomainTask
                self.curr_task = DomainTask()
                self.curr_task.start()
                self.reg_task_flag = True
                logger.info(t2t("Task DomainTask Start."))

            elif task_name == 'CollectorTask':
                pass
        else:
            logger.info(t2t("End Task"))
            self.curr_task.end_task()
            self.reg_task_flag = not self.reg_task_flag


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

        if self.start_tasklist_flag:
            if len(self.task_list)>0:
                for i in self.task_list:
                    if self.checkup_stop_func():
                        break
                    if self.start_tasklist_flag == False:
                        break
                    self.start_stop_task(i)
                    while 1:
                        if self.curr_task.stop_threading_flag:
                            break
                        if self.checkup_stop_func():
                            break
                        if self.start_tasklist_flag == False:
                            break
                        time.sleep(1)

if __name__ == '__main__':
    tm = TaskManager()
    keyboard.add_hotkey(load_json("keymap.json", f"{CONFIG_PATH_SETTING}")["task"], tm.start_stop_task, args=("CollectionPathTask",))
    while 1:
        time.sleep(1)
    