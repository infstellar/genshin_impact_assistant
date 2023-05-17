from source.util import *
from pywebio import *
from source.webio.util import *
from source.webio.page_manager import Page
from source.config.cvars import *
from source.mission.mission_index import MISSION_INDEX

class MissionPage(Page):
    def __init__(self) -> None:
        super().__init__()
        self.missions = MISSION_INDEX
    
    def _load(self):
        grid_content = []
        for i in range(len(self.missions)):
            if i%3==0:
                grid_content.append([])
            grid_content[i//3]=output.put_scope(f"{self.missions[i]}")
        output.put_grid(
            content=grid_content
        )
    
    def _event_thread(self):
        return super()._event_thread()
        