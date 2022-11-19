class Page:
    def __init__(self):
        self.loaded = False

    def load(self):
        if not self.loaded:
            self.loaded = True
            self._on_load()

    def unload(self):
        if self.loaded:
            self.loaded = False
            self._on_unload()

    def _on_load(self):
        pass

    def _on_unload(self):
        pass


class PageManager:
    def __init__(self):
        self.page_dict: dict = {}
        self.last_page = None

    def load_page(self, idx: str):

        if idx in self.page_dict:

            if self.last_page is not None:
                if Page in self.last_page.__class__.__bases__:
                    self.last_page.unload()

            self.page_dict[idx].load()

            self.last_page = self.page_dict[idx]


    def reg_page(self, idx: str, page: Page):
        self.page_dict[idx] = page

    def get_page(self, idx: str) -> Page:
        return self.page_dict[idx]
