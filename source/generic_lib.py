import img_manager
import time
from interaction_background import InteractionBGD
import posi_manager


def f_recognition(itt: InteractionBGD, mode='button_only'):
    if itt.get_img_existence(img_manager.F_BUTTON, posi=posi_manager.posi_F_button_list):
        return True
    else:
        return False


if __name__ == '__main__':
    itt = InteractionBGD()
    while 1:
        time.sleep(0.2)
        print(f_recognition(itt))
