from source.task.task_template import TaskTemplate
from source.task.domain.domain_flow_upgrade import DomainFlowController


class CollectorTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.DMC = DomainFlowController()
        self._add_sub_threading(self.DMC)
        

    def exec_task(self):
        self.DMC.continue_threading()
        