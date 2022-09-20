from unit import *
from interaction_background import Interaction_BGD
import cv2
itt=Interaction_BGD()
i=0
while(1):
    #input('wait')
    i+=1
    cap=itt.capture()
    x=str(time.time())
    cv2.imwrite("tools\\snapshot\\png\\saixi"+x+".png",cap)
    cv2.imwrite("tools\\snapshot\\jpg\\saixi"+x+".jpg",cap[:,:,:3])
    time.sleep(0.5)
    print('pic',i)