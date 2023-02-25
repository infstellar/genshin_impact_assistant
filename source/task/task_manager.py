from source.util import *
import keyboard
from source.task.task_template import TaskTemplate


    
class TaskManager():
    def __init__(self) -> None:
        self.reg_task_flag = False
        self.curr_task = None # type: TaskTemplate
    
    def start_stop_task(self, task_name):
        if not self.reg_task_flag:
            if task_name == 'CollectionPathTask':
                from source.task.collection_path_task import CollectionPathTask
                self.curr_task = CollectionPathTask()
                self.curr_task.start()
                self.reg_task_flag = True
                logger.info(t2t("Task CollectionPathTask Start."))
        else:
            logger.info(t2t("End Task"))
            self.curr_task.end_task()
            self.reg_task_flag = not self.reg_task_flag


if __name__ == '__main__':
    tm = TaskManager()
    keyboard.add_hotkey('[', tm.start_stop_task, args=("CollectionPathTask",))
    while 1:
        time.sleep(1)
    