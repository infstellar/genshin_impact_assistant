class GIABaseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = False
        self.possible_reasons = []
    
    
class TaskException(GIABaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = True
