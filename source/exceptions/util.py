from source.util import *

class GIABaseException(Exception):
    POSSIBLE_REASONS = []
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = False # 当发生该异常时，是否结束所有Task。
    
class TaskException(GIABaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = True

class SnapshotException(GIABaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def save_snapshot(self, img):
        cv2.imwrite(os.path.join(ROOT_PATH, "Logs/{time:YYYY-MM-DD}", f"{round(time.time(),2)}-{self.__str__()}.jpg"), img)
