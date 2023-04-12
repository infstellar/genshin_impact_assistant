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


page_main = UIPage(check_icon = asset.IconUIEmergencyFood)
page_esc = UIPage(check_icon = asset.IconUIEscMenu)
page_domain = UIPage(check_icon = asset.IconUIInDomain)
page_bigmap = UIPage(check_icon = asset.IconUIBigmap)
page_time = UIPage(check_icon = asset.IconUITimeMenuCore)
page_configure_team = UIPage(check_icon=asset.IconUIPartySetup)

page_main.link('m', page_bigmap)
page_main.link('esc', page_esc)
page_esc.link(asset.ButtonUISwitchToTimeMenu, page_time)
page_esc.link('esc', page_main)
page_esc.link(asset.ButtonUIEnterPartySetup, page_configure_team)
page_time.link(asset.ButtonGeneralExit, page_esc)
page_bigmap.link('m', page_main)
page_configure_team.link('esc', page_esc)

