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
        itt.key_press('m')
        time.sleep(1.5)
        if i >= max_time:
            return
        i+=1
    time.sleep(0.3)

def switchto_bigmapwin(max_time=30):
    while not itt.get_img_existence(img_manager.ui_bigmap_win):
        itt.key_press('m')
        time.sleep(1.5)
    time.sleep(1.2)
    
def switchto_esc_menu(max_time=30):
    while not itt.get_img_existence(img_manager.ui_esc_menu):
        itt.key_press('esc')
        time.sleep(0.5)
    time.sleep(0.5)

def switchto_time_menu(max_time=30):
    switchto_esc_menu()
    while not itt.get_img_existence(img_manager.ui_time_menu_core):
        itt.appear_then_click(img_manager.ui_switch_to_time_menu)
        time.sleep(0.5)
    time.sleep(0.5)
