from util import *
import img_manager
import posi_manager
from interaction_background import InteractionBGD
itt = InteractionBGD()

def switchto_mainwin():
    while not itt.get_img_existence(img_manager.ui_main_win):
        itt.key_press('m')
        time.sleep(1)
    time.sleep(0.3)

def switchto_bigmapwin():
    while not itt.get_img_existence(img_manager.ui_bigmap_win):
        itt.key_press('m')
        time.sleep(1)
    time.sleep(1.2)