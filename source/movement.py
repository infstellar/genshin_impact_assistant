import pyautogui
from unit import *
import static_method,small_map
import static_lib
itt=static_lib.sta_itt
AHEAD=0
LEFT=1
RIGHT=2
BACK=3
CORRECT_DEGREE = config_json["corr_degree"]
HORIZONTAL=1
VERTICALLY=2
VERTICALLY_AND_HORIZONTAL=3
# >0:right; <0:left
def move(direction,distance=1):
    if direction==AHEAD:
        itt.keyDown('w')
        itt.delay(0.1*distance)
        itt.keyUp('w')
    if direction==LEFT:
        itt.keyDown('a')
        itt.delay(0.1*distance)
        itt.keyUp('a')
    if direction==RIGHT:
        itt.keyDown('d')
        itt.delay(0.1*distance)
        itt.keyUp('d')
    if direction==BACK:
        itt.keyDown('s')
        itt.delay(0.1*distance)
        itt.keyUp('s')
        
def cview(angle=10, mode=HORIZONTAL): # left<0,right>0
    angle=(2*angle)
    if abs(angle)<1:
        if angle<0:
            angle=-1
        else:
            angle=1
    itt.move_to(int(angle),0,relative=True)

def move_view_p(x,y):
    # x,y=point
    itt.move_to(x,y)

def reset_view():
    pyautogui.click(button='middle')
    
def view_to_angle(angle=0,deltanum=0.65,maxloop=100,corrected_num=CORRECT_DEGREE):
    cap=itt.capture(posi=small_map.posi_map)
    degree=small_map.jwa_3(cap)
    i=0
    while not abs(degree-(angle-corrected_num))<deltanum:
        degree=small_map.jwa_3(itt.capture(posi=small_map.posi_map))
        # print(degree)
        cview((degree-(angle-corrected_num)))
        time.sleep(0.05)
        if i>maxloop:
            break
        i+=1
    logger.debug('last degree: '+str(degree))
    #itt.keyUp('w')
    
def reset_const_val():
    pass

# view_to_angle(-90)
if __name__=='__main__':
    view_to_angle(-90)
    