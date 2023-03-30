from source.util import *
from source.common.base_threading import AdvanceThreading, BaseThreading
from source.flow.flow_template import FlowController
import threading


class TaskEndException(Exception):
    pass

class TaskTemplate(AdvanceThreading):
    def __init__(self):
        super().__init__()
        self.thread_list = []
        self.is_task_running = False
        self.name = ""

    def terminate_task(self):
        logger.info(f"terminate task {self.name}")
        self.stop_threading()
    
    def get_statement(self):
        return "Statement Not Register Yet"
            
            