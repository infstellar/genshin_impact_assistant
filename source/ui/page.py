import traceback
from source.manager import asset, img_manager

class UIPage():

    parent = None

    def __init__(self, check_icon: img_manager.ImgIcon):
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.check_icon_list = []
        self.check_icon_list.append(check_icon)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        """
        
        button:Button/Str
        """
        self.links[destination] = button
        
    def is_current_page(self, itt, print_log=False):
        for imgicon in self.check_icon_list:
            ret = itt.get_img_existence(imgicon, is_log=print_log)
            if ret:
                return True
        return False
    
    def add_check_icon(self, check_icon: img_manager.ImgIcon):
        self.check_icon_list.append(check_icon)


page_main = UIPage(check_icon = asset.ui_main_win)
page_esc = UIPage(check_icon = asset.ui_esc_menu)
page_domain = UIPage(check_icon = asset.IN_DOMAIN)
page_bigmap = UIPage(check_icon = asset.ui_bigmap_win)
page_time = UIPage(check_icon = asset.ui_time_menu_core)
page_configure_team = UIPage(check_icon=asset.UIConfigureTeam)

page_main.link('m', page_bigmap)
page_main.link('esc', page_esc)
page_esc.link(asset.button_time_page, page_time)
page_esc.link('esc', page_main)
page_esc.link(asset.ConfigureTeam, page_configure_team)
page_time.link(asset.button_exit, page_esc)
page_bigmap.link('m', page_main)
page_configure_team.link('esc', page_esc)

