from source.util import *
from source.common.base_threading import AdvanceThreading


# class TaskEndException(Exception):
#     pass

class TaskTemplate(AdvanceThreading):
    def __init__(self):
        super().__init__()
        self.thread_list = []
        self.is_task_running = False
        self.name = ""

    def terminate_task(self):
        """强制终止任务。
        """
        logger.info(f"terminate task {self.name}")
        self.stop_threading()
    
    def get_statement(self):
        """可以重写此方法，用于在GUI中显示当前任务执行情况。

        Returns:
            _type_: _description_
        """
        return "Statement Not Register Yet"
    
    def task_run(self):
        """
        使用task时，重写此方法。
        该函数只会运行一次。函数结束后任务结束。
        """
        pass

    
    def loop(self):
        """
        如果你已经了解了GIA的（很垃圾的）线程架构，你可以重写此方法以执行任务。
        当然，在task_run中写个while 1也不费事（
        """
        self.task_run()
        self.pause_threading()
   