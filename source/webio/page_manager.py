import subprocess

from pywebio import output, session, pin
from source.util import *

class Page:
    def __init__(self):
        self.loaded = False
        self.main_scope = 'Main'


    def load(self):
        if not self.loaded:
            self.loaded = True
            output.put_scope(self.main_scope)  # 创建主scope
            self._on_load()


    def unload(self):
        if self.loaded:
            self.loaded = False
            self._on_unload()
            output.remove(self.main_scope)

    def _on_load(self):
        pin.pin['isSessionExist'] = "1"

    def _on_unload(self):
        pass

    def _value_list2buttons_type(self, l1):
        replace_dict = {
            "MainPage": _("Main"),
            "SettingPage": _("Setting"),
            "CombatSettingPage": _("CombatSetting"),
            "CollectorSettingPage": _("CollectorSetting")
        }
        for i in range(len(l1)):
            l1[i] = (replace_dict[l1[i]], l1[i])
        return l1

class PageManager:
    def __init__(self):
        self.page_dict: dict = {}
        self.last_page = None

    def load_page(self, idx: str):

        if idx in self.page_dict:

            if self.last_page is not None:
                # if Page in self.last_page.__class__.__bases__:
                if isinstance(self.last_page, Page):
                    self.last_page.unload()

            self.page_dict[idx].load()

            self.last_page = self.page_dict[idx]

    def reg_page(self, idx: str, page: Page):
        self.page_dict[idx] = page

    def get_page(self, idx: str) -> Page:
        return self.page_dict[idx]
