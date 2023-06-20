from source.exceptions.util import *

# 这个类可以调用itt。请注意避免调用循环。

from source.interaction.interaction_core import itt
from source.util import *

class SnapShotException(GIABaseException):
    def __init__(self, *args: object, reason: str = None) -> None:
        super().__init__(*args, reason=reason)
        
    def save_snapshot(self):
        cap = itt.capture(jpgmode=0)
        cv2.imwrite(os.path.join(ROOT_PATH, "Logs/{time:YYYY-MM-DD}", f"{round(time.time(),2)}-.jpg"), cap)

if __name__ == '__main__':
    pass