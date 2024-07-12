import datetime

from source.util import *
from source.assets.launch_genshin import *
from source.task.task_template import TaskTemplate
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.interaction.interaction_core import itt



class CollectImage(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.name = "CollectImage"
        self.last_imgs = []

    def task_run(self):
        verify_path(f"{ROOT_PATH}\\collected_images")
        while 1:
            if self.checkup_stop_func(): break
            time.sleep(1)
            cap = itt.capture()
            is_new = True
            for i in self.last_imgs:
                if similar_img(cap, i, is_gray=True) > 0.99:
                    is_new = False
            if not is_new:
                continue
            else:
                self.last_imgs.append(cap.copy())
                if len(self.last_imgs)>=5:
                    self.last_imgs.pop(0)
                cv2.imwrite(f"{ROOT_PATH}\\collected_images\\{datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')}.png", cap)

