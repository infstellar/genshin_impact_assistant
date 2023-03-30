from source.map.map import genshin_map
from source.map.position.position import *
from source.ui.ui import ui_control
from source.ui import page as UIPages


class CommissionParser():
    TRAVERSE_MONDSTADT_POSITION=[TianLiPosition([0,0])]
    
    def __init__(self) -> None:
        pass

    def traverse_mondstant(self):
        ui_control.ensure_page(UIPages.page_bigmap)
        # for posi in self.TRAVERSE_MONDSTADT_POSITION:
            # genshin_map._move_bigmap(posi)
