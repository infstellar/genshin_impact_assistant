from util import *
import img_manager
import posi_manager
from interaction_background import InteractionBGD
itt = InteractionBGD()

def default_stop_func():
    return False

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
