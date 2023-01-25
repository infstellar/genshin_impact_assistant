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
        
    def is_current_page(self, print_log=False):
        ret = itt.get_img_existence(self.check_icon, is_log=print_log)
        return ret
    
    def get_following_page_name(self):
        retp=[]
        for i in self.following_page:
            retp.append(i["page_name"])
        return retp
    
    def add_following_page(self,page_name:str, switch_button):
        self.following_page[page_name]=switch_button
        
    
page_main = UIPage(check_icon = img_manager.ui_main_win, page_name = "main", to_mainpage = [""], to_selfpage = [""])
page_main.add_following_page('bigmap', 'm')
page_main.add_following_page('esc', 'esc')
page_esc = UIPage(check_icon = img_manager.ui_esc_menu, page_name = "esc", to_mainpage = ["esc", "main"], to_selfpage = ["main", "esc"])
page_esc.add_following_page('time', button_manager.button_time_page)
page_esc.add_following_page('main', 'esc')
page_time = UIPage(check_icon = img_manager.ui_time_menu_core, page_name = "time",
                   to_mainpage = ["time", "esc", "main"], to_selfpage = ["main","esc","time"])
page_time.add_following_page('esc', button_manager.button_exit)
page_bigmap = UIPage(check_icon = img_manager.ui_bigmap_win, page_name = "bigmap", 
                  to_mainpage=["bigmap", "main"], to_selfpage=["main", "bigmap"])
page_bigmap.add_following_page('main', 'm')

all_page = {
    "main":page_main, 
    "esc":page_esc, 
    "time":page_time,
    "bigmap":page_bigmap
            }

def get_current_pagename(retry=0):
    current_page = None
    max_rate = 0
    for i in all_page:
        if retry>=35:
            f = all_page[i].is_current_page(print_log=True)
        else:
            f = all_page[i].is_current_page()
        if f:
            if current_page == None:
                current_page = i
            else:
                logger.warning(f"UI界面有多个检测结果：{current_page}, {i} ")
                current_page = "ERROR"
    if current_page == None:
        if retry>=40:
            logger.warning(_("UI界面检测失败，正在尝试按esc返回"))
            itt.key_press("esc")
            logger.warning(_("将在1秒后再次尝试获取UI界面"))
            logger.warning(_("尝试次数：") + f"{retry}")
            time.sleep(1)
            return get_current_pagename(retry+1)
        else:
            if retry == 1:
                logger.debug(_("UI界面检测失败"))
            if retry == 11:
                logger.info(_("UI界面检测失败"))
                logger.info(_("将在0.2秒后再次尝试获取UI界面"))
            
            if retry<=10:
                logger.debug(_("尝试次数：") + f"{retry}")
                time.sleep(0.2)
            else:
                logger.info(_("尝试次数：") + f"{retry}")
                time.sleep(1)
            return get_current_pagename(retry+1)
    return current_page

def switch_to_page(target_page:UIPage, stop_func):
    current_page = all_page[get_current_pagename()]
    
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
                time.sleep(3)
                if all_page[current_page.to_mainpage[i+1]].is_current_page():
                    break
                if stop_func():
                    return
    
    for i in range(len(target_page.to_selfpage)-1):
        following_button = all_page[target_page.to_selfpage[i]].following_page[target_page.to_selfpage[i+1]]
        while 1:
            if isinstance(following_button, button_manager.Button):
                itt.appear_then_click(following_button)
            elif isinstance(following_button, str):
                itt.key_press(following_button)
            time.sleep(3)
            if all_page[target_page.to_selfpage[i+1]].is_current_page():
                break
            if stop_func():
                return
            
if __name__ == "__main__":     
    while 1:
        time.sleep(1)
        print(get_current_pagename())

# def switchto_mainwin(stop_func, max_time=30):
#     i=0
#     while not itt.get_img_existence(img_manager.ui_main_win):
#         if stop_func():
#             return
#         itt.key_press('m')
#         time.sleep(1.5)
#         if i >= max_time:
#             return
#         i+=1
#     time.sleep(0.3)

# def switchto_bigmapwin(stop_func, max_time=30):
#     while not itt.get_img_existence(img_manager.ui_bigmap_win):
#         if stop_func():
#             return
#         itt.key_press('m')
#         time.sleep(1.5)
#     time.sleep(1.2)
    
# def switchto_esc_menu(stop_func, max_time=30):
#     while not itt.get_img_existence(img_manager.ui_esc_menu):
#         if stop_func():
#             return
#         itt.key_press('esc')
#         time.sleep(0.5)
#     time.sleep(0.5)

# def switchto_time_menu(stop_func, max_time=30):
#     switchto_esc_menu(stop_func, max_time)
#     while not itt.get_img_existence(img_manager.ui_time_menu_core):
#         if stop_func():
#             return
#         itt.appear_then_click(img_manager.ui_switch_to_time_menu)
#         time.sleep(0.5)
#     time.sleep(0.5)
