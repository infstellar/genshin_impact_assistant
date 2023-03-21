from source.task.task_template import TaskTemplate
from source.flow.domain_flow_upgrad import DomainFlowController


class CollectorTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.DMC = DomainFlowController()
        self._add_sub_threading(self.DMC)
        

    def exec_task(self):
        self.DMC.continue_threading()
        