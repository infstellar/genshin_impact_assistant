from source.util import *
from source.assets.launch_genshin import *
from source.task.task_template import TaskTemplate
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.interaction.interaction_core import itt

class LaunchGenshin(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.name = "LaunchGenshin"

    def loop(self):
        while 1:
            time.sleep(2)
            itt.appear_then_click(ClickToEnter)
            if ui_control.verify_page(UIPage.page_main):
                break
        self.pause_threading()
