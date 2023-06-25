from source.util import *

class GIABaseException(Exception):
    POSSIBLE_REASONS = []
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = False # 当发生该异常时，是否结束所有Task。
        
    def __str__(self) -> str:
        r = '\x1b[31m'
        r += super().__str__()
        r+='\n'
        if len(self.POSSIBLE_REASONS) > 0:
            i = 0
            for pr in self.POSSIBLE_REASONS:
                i+=1
                r+='\x1b[31m'
                r+=(f'{t2t("Possible Reason")} {i}: {pr} \n')
        return r
class TaskException(GIABaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_task_flag = True

class SnapshotException(GIABaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def save_snapshot(self, img:ndarray):
        if img.shape[2] == 4:
            img = img[:,:,:3]
        img_path = os.path.join(ROOT_PATH, "Logs", get_logger_format_date(), f"{self.__str__()} | {time.strftime('%H-%M-%S', time.localtime())}.jpg")
        logger.warning(f"Snapshot saved to {img_path}")
        cv2.imwrite(img_path, img)
