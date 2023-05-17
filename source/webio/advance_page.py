from source.webio.page import Page
from source import webio
from source.webio import manager
from source.webio.util import *

class AdvancePage(Page):
    """Page的加强版，多了一个显示页面切换的功能

    Args:
        Page (_type_): _description_
    """
    def __init__(self, page_name=""):
        super().__init__(page_name)
    
    def _on_load(self):
        # 标题
        output.put_markdown(t2t('# Config'), scope=self.main_scope)
        # 页面切换按钮
        output.put_buttons(self._value_list2buttons_type(list(manager.page_dict)), onclick=webio.manager.load_page, scope=self.main_scope)
        super()._on_load()
        