from source.task.task_template import TaskTemplate
from source.flow.domain_flow_upgrad import DomainFlowController
from source.task.task_manager import TaskManager

class MisisonTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.MM=TaskManager()
        self._add_sub_threading(self.MM)
    
    def exec_task(self):
        self.MM.start()
