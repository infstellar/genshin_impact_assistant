from interaction_background import InteractionBGD
import img_manager, time

def f_recognition(itt:InteractionBGD, mode='button_only'):
    if itt.get_img_existence(img_manager.F_BUTTON) == True:
        return True
    else:
        return False

if __name__ == '__main__':
    itt = InteractionBGD()
    while 1:
        time.sleep(0.2)
        print(f_recognition(itt))