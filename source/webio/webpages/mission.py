from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
from source.mission.mission_index import MISSION_INDEX
from source.mission.mission_meta import MISSION_META

class MissionPage(AdvancePage):
    def __init__(self) -> None:
        super().__init__()
        self.missions = MISSION_INDEX
    
    def _render_scopes(self):
        for i in self.missions:
            output.clear(i)
            if i in MISSION_META:
                if GLOBAL_LANG in MISSION_META[i]['name']:
                    mission_show_name = MISSION_META[i]['name'][GLOBAL_LANG]
                else:
                    mission_show_name = i
            else:
                mission_show_name = i
            output.put_text(mission_show_name, scope=i)
            pin.put_checkbox(name=f"CHECKBOX_{i}",options=[t2t("Enable")],scope=i)
    
    def _load(self):
        grid_content = []
        for i in range(len(self.missions)):
            if i%3==0:
                grid_content.append([])
            grid_content[i//3].append(output.put_scope(f"{self.missions[i]}").style('border: 1px solid #ccc; border-radius: 16px'))
        output.put_grid(content=grid_content, scope=self.main_scope)
        
        self._render_scopes()
    
    def _event_thread(self):
        return super()._event_thread()
        