from source.interaction.interaction_core import itt
from source.manager import scene_manager, button_manager
from source.util import *

itt = itt
def get_current_pagename(retry=0):
    current_page = None
    max_rate = 0
    for i in scene_manager.all_page:
        if retry>=35:
            f = scene_manager.all_page[i].is_current_page(itt, print_log=True)
        else:
            f = scene_manager.all_page[i].is_current_page(itt)
        if f:
            if current_page == None:
                current_page = i
            else:
                logger.warning(f"UI界面有多个检测结果：{current_page}, {i} ")
                current_page = "ERROR"
    if current_page == None:
        if retry>=40:
            logger.warning(t2t("UI界面检测失败，正在尝试按esc返回"))
            itt.key_press("esc")
            logger.warning(t2t("将在1秒后再次尝试获取UI界面"))
            logger.warning(t2t("尝试次数：") + f"{retry}")
            time.sleep(1)
            return get_current_pagename(retry+1)
        else:
            if retry == 1:
                logger.debug(t2t("UI界面检测失败"))
            if retry == 11:
                logger.info(t2t("UI界面检测失败"))
                logger.info(t2t("将在0.2秒后再次尝试获取UI界面"))
            
            if retry<=10:
                logger.debug(t2t("尝试次数：") + f"{retry}")
                time.sleep(0.2)
            else:
                logger.info(t2t("尝试次数：") + f"{retry}")
                time.sleep(1)
            return get_current_pagename(retry+1)
    return current_page

def switch_to_page(target_page:scene_manager.UIPage, stop_func):
    current_page = scene_manager.all_page[get_current_pagename()]
    
    if current_page.page_name == target_page.page_name:
        return 0    
            
    if current_page.page_name != "main":
        for i in range(len(current_page.to_mainpage)-1):
            following_button = scene_manager.all_page[current_page.to_mainpage[i]].following_page[current_page.to_mainpage[i+1]]
            while 1:
                if isinstance(following_button, button_manager.Button):
                    itt.appear_then_click(following_button)
                elif isinstance(following_button, str):
                    itt.key_press(following_button)
                time.sleep(3)
                if scene_manager.all_page[current_page.to_mainpage[i+1]].is_current_page(itt):
                    break
                if stop_func():
                    return
    
    for i in range(len(target_page.to_selfpage)-1):
        following_button = scene_manager.all_page[target_page.to_selfpage[i]].following_page[target_page.to_selfpage[i+1]]
        while 1:
            if isinstance(following_button, button_manager.Button):
                itt.appear_then_click(following_button)
            elif isinstance(following_button, str):
                itt.key_press(following_button)
            time.sleep(3)
            if scene_manager.all_page[target_page.to_selfpage[i+1]].is_current_page(itt):
                break
            if stop_func():
                return