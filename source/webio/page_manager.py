import subprocess


from source.util import *
from source.webio.page import Page




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
