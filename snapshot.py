from unit import *
from interaction_background import Interaction_BGD
import cv2
itt=Interaction_BGD()
while(1):
    input('wait')
    cap=itt.capture()
    cv2.imwrite("tools/snapshot"+str(time.time())+".png",cap)