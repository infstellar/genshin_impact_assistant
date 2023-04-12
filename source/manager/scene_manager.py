from source.util import *
from source.manager import img_manager
from source.manager import asset


def default_stop_func():
    return False

class UIPage():
    def __init__(self, check_icon: img_manager.ImgIcon, page_name:str = None, to_mainpage = None, to_selfpage = None):
        self.page_name = page_name
        self.check_icon_list = []
        self.check_icon_list.append(check_icon)
        self.following_page={}
        if to_mainpage == None:
            to_mainpage = [""]
        if to_selfpage == None:
            to_selfpage = [""]
        self.to_mainpage = to_mainpage
        self.to_selfpage = to_selfpage
        
    def is_current_page(self, itt, print_log=False):
        for i in self.check_icon_list:
            ret = itt.get_img_existence(i, is_log=print_log)
            if ret:
                return True
        return False
    
    def add_check_icon(self, check_icon: img_manager.ImgIcon):
        self.check_icon_list.append(check_icon)

    def get_following_page_name(self):
        retp=[]
        for i in self.following_page:
            retp.append(i["page_name"])
        return retp
    
    def add_following_page(self, page_name:str, switch_button):
        """
        page_name: 按下switch_button后可以切换到的页面名
        switch_button: 按钮/按键。可以为str(键盘)或button对象(鼠标)
        """
        self.following_page[page_name]=switch_button
        
    
page_main = UIPage(check_icon = asset.IconUIEmergencyFood, page_name ="main", to_mainpage = [""], to_selfpage = [""])
page_main.add_following_page('bigmap', 'm')
page_main.add_following_page('esc', 'esc')
page_domain = UIPage(check_icon = asset.IconUIInDomain, page_name ="domain")
page_esc = UIPage(check_icon = asset.IconUIEscMenu, page_name ="esc", to_mainpage = ["esc", "main"], to_selfpage = ["main", "esc"])
page_esc.add_following_page('time', asset.ButtonUISwitchToTimeMenu)
page_esc.add_following_page('main', 'esc')
page_time = UIPage(check_icon = asset.IconUITimeMenuCore, page_name ="time",
                   to_mainpage = ["time", "esc", "main"], to_selfpage = ["main","esc","time"])
page_time.add_following_page('esc', asset.ButtonGeneralExit)
page_bigmap = UIPage(check_icon = asset.IconUIBigmap, page_name ="bigmap",
                     to_mainpage=["bigmap", "main"], to_selfpage=["main", "bigmap"])
page_bigmap.add_following_page('main', 'm')

all_page = {
    "main":page_main, 
    "domain":page_domain,
    "esc":page_esc, 
    "time":page_time,
    "bigmap":page_bigmap
            }


            
# if __name__ == "__main__":     
#     while 1:
#         time.sleep(1)
#         print(get_current_pagename())

# def switchto_mainwin(stop_func, max_time=30):
#     i=0
#     while not itt.get_img_existence(asset.ui_main_win):
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
