from source.util import *
from source.common.base_threading import AdvanceThreading
from source.flow.flow_template import FlowController
import threading


class TaskEndException(Exception):
    pass

class TaskTemplate():
    def __init__(self):
        super().__init__()
        self.thread_list = []
        self.is_task_running = False
        self.name = ""

    def task_running(self):
        self.is_task_running = True

    def task_end(self):
        self.is_task_running = False

    def terminate_task(self):
        logger.info(f"terminate task {self.name}")
        self.task_end()
        for i in self.thread_list:
            i.stop_threading()

    def _add_sub_threading(self,x:threading.Thread):
        self.thread_list.append(x)
        
    
    def get_statement(self):
        return "Statement Not Register Yet"
    
    def exec_task(self):
        pass
            
            
            