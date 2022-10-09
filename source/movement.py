from unit import *
import static_method,small_map
itt=static_method.sta_itt
AHEAD=0
LEFT=1
RIGHT=2
BACK=3
global VIEW_X,VIEW_Y,VIEW_D
VIEW_X=197.5
VIEW_Y=120
VIEW_D=285.75
    
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
        
def cview(angle=10): # left<0,right>0
    itt.move_to(int(2*angle),0,relative=True)
    # itt.keyPress('w')
    
def view_to_angle(angle=0):
    itt.keyUp('w')
    while(small_map.get_direction_angle()!=angle):
        #itt.keyDown('w')
        current_angle=small_map.get_direction_angle()
        cview((angle-current_angle))
        time.sleep(0.05)
    #itt.keyUp('w')
    
def reset_const_val():
    global VIEW_X,VIEW_Y,VIEW_D
    cap=itt.capture()
    p,delta=small_map.jwa_3(cap)
    VIEW_X=p[0]
    VIEW_Y=p[1]
    VIEW_D=delta
    logger.debug(VIEW_X,VIEW_Y,VIEW_D)

def view_to_90(deltanum=1.5,maxloop=50):
    global VIEW_X,VIEW_Y,VIEW_D
    cap=itt.capture()
    p,delta=small_map.jwa_3(cap)
    while(p==None):
        time.sleep(1)
        cap=itt.capture()
        p,delta=small_map.jwa_3(cap)
    
    
    
    # 198,119.5,283.5
    i=0
    while not (abs(p[0]-VIEW_X)<deltanum and abs(p[1]-VIEW_Y<deltanum)):
        itt.keyUp('w')
        cap=itt.capture()
        p,delta=small_map.jwa_3(cap) 
        while(p==None):
            time.sleep(1)
            cap=itt.capture()
            p,delta=small_map.jwa_3(cap)
        cview((VIEW_D-delta))
        if VIEW_D==delta:
            cview(random.randint(-3,3))
        time.sleep(0.1)
        i+=1
        if i>=maxloop:
            break

# view_to_angle(-90)
if __name__=='__main__':
    view_to_90()
    