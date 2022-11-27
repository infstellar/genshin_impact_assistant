from util import *
import img_manager
import posi_manager
from interaction_background import InteractionBGD
itt = InteractionBGD()

def switchto_mainwin():
    while not itt.get_img_existence(img_manager.ui_main_win):
        itt.key_press('m')
        time.sleep(1.5)
    time.sleep(0.3)

def switchto_bigmapwin():
    while not itt.get_img_existence(img_manager.ui_bigmap_win):
        itt.key_press('m')
        time.sleep(1.5)
    time.sleep(1.2)
    
def switchto_esc_menu():
    while not itt.get_img_existence(img_manager.ui_esc_menu):
        itt.key_press('esc')
        time.sleep(0.5)
    time.sleep(0.5)

def switchto_time_menu():
    switchto_esc_menu()
    while not itt.get_img_existence(img_manager.ui_time_menu_core):
        itt.appear_then_click(img_manager.ui_switch_to_time_menu)
        time.sleep(0.5)
    time.sleep(0.5)
