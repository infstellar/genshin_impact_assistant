from util import *
import img_manager
import posi_manager
import button_manager
from interaction_background import InteractionBGD
itt = InteractionBGD()

def default_stop_func():
    return False

class UIPage():
    def __init__(self, check_icon:img_manager.ImgIcon, page_name:str = None, to_mainpage = [""], to_selfpage = [""]):
        self.check_icon = check_icon
        self.page_name = page_name
        self.following_page={}
        self.to_mainpage = to_mainpage
        self.to_selfpage = to_selfpage
        
    def is_current_page(self):
        ret = itt.get_img_existence(self.check_icon)
        return ret
    
    def get_following_page_name(self):
        retp=[]
        for i in self.following_page:
            retp.append(i["page_name"])
        return retp
    
    def add_following_page(self, switch_button, page_name:str):
        self.following_page[page_name]=switch_button
        
    
page_main = UIPage(check_icon = img_manager.ui_main_win, page_name = "main", to_mainpage = [""], to_selfpage = [""])
page_main.add_following_page('m', 'map')
page_main.add_following_page('esc', 'esc')
page_esc = UIPage(check_icon = img_manager.ui_esc_menu, page_name = "esc", to_mainpage = ["esc", "main"], to_selfpage = ["main", "esc"])
page_esc.add_following_page(button_manager.button_time_page, 'time')
page_esc.add_following_page('esc', 'main')
page_time = UIPage(check_icon = img_manager.ui_time_menu_core, page_name = "time",
                   to_mainpage = ["time", "esc", "main"], to_selfpage = ["main","esc","time"])
page_time.add_following_page('esc', button_manager.button_exit)

all_page = {
    "main":page_main, 
    "esc":page_esc, 
    "time":page_time
            }

def switch_to_page(target_page:UIPage):
    current_page = None
    for i in all_page:
        if all_page[i].is_current_page():
            current_page = all_page[i]
    
    if current_page.page_name == target_page.page_name:
        return 0    
            
    if current_page.page_name != "main":
        for i in range(len(current_page.to_mainpage)-1):
            following_button = all_page[current_page.to_mainpage[i]].following_page[current_page.to_mainpage[i+1]]
            while 1:
                if isinstance(following_button, button_manager.Button):
                    itt.appear_then_click(following_button)
                elif isinstance(following_button, str):
                    itt.key_press(following_button)
                time.sleep(2)
                if all_page[current_page.to_mainpage[i+1]].is_current_page():
                    break
    
    for i in range(len(target_page.to_selfpage)-1):
        following_button = all_page[target_page.to_selfpage[i]].following_page[target_page.to_selfpage[i+1]]
        while 1:
            if isinstance(following_button, button_manager.Button):
                itt.appear_then_click(following_button)
            elif isinstance(following_button, str):
                itt.key_press(following_button)
            time.sleep(2)
            if all_page[target_page.to_selfpage[i+1]].is_current_page():
                break
            
if __name__ == "__main__":     
    switch_to_page(page_time)

def switchto_mainwin(stop_func, max_time=30):
    i=0
    while not itt.get_img_existence(img_manager.ui_main_win):
        if stop_func():
            return
        itt.key_press('m')
        time.sleep(1.5)
        if i >= max_time:
            return
        i+=1
    time.sleep(0.3)

def switchto_bigmapwin(stop_func, max_time=30):
    while not itt.get_img_existence(img_manager.ui_bigmap_win):
        if stop_func():
            return
        itt.key_press('m')
        time.sleep(1.5)
    time.sleep(1.2)
    
def switchto_esc_menu(stop_func, max_time=30):
    while not itt.get_img_existence(img_manager.ui_esc_menu):
        if stop_func():
            return
        itt.key_press('esc')
        time.sleep(0.5)
    time.sleep(0.5)

def switchto_time_menu(stop_func, max_time=30):
    switchto_esc_menu(stop_func, max_time)
    while not itt.get_img_existence(img_manager.ui_time_menu_core):
        if stop_func():
            return
        itt.appear_then_click(img_manager.ui_switch_to_time_menu)
        time.sleep(0.5)
    time.sleep(0.5)
