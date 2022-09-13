import time, math, random, pytweening, sys, os
import pyautogui
print('import: cv2')
import cv2
# print('import: paddleocr')
# from paddleocr import PaddleOCR
# from paddleocr import draw_ocr
print('import: numpy')
import numpy as np
print('import: PIL')
from PIL import ImageGrab,Image
print('import: win32api,win32con,win32gui,random')
import win32api,win32con,win32gui,random
print('import: PyQt5.QtWidgets')
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
print('import: matplotlib.pyplot')
import matplotlib.pyplot as plt


class winInfo():
    def __init__(self,x,y,w,h,mainHnd):
        self.x=x    
        self.y=y
        self.w=w
        self.h=h
        self.mainHnd=mainHnd
        self.winpos=[x,y]
        
    def getRect(self,rangePosition=[0,0,0,0]):
        return [self.x,self.y,self.w+self.x,self.h+self.y]

def winMoveTo(posi,win_pos,max_float=3,duration_base=0.2,xadd=0,yadd=0,message=''):
    if posi==-1:
        print('\n\n\n\n\n ERROR: winMoveToError, please check up the program. \n\n\n\n\n')
        if True:
            raise RuntimeError('winMoveToError: posi should not be -1')
    x=posi[0]
    y=posi[1]   
    k=1000#放大倍率,越大随机数越准
    mouse_position=pyautogui.position()
    rel_x=x+xadd+win_pos[0]+random.randint(0,max_float)
    rel_y=y+yadd+win_pos[1]+random.randint(0,max_float)
    
    if duration_base==0.2:
        distance=math.sqrt(((mouse_position[0]-rel_x)**2+(mouse_position[1]-rel_y)**2))
        delaytime=distance/random.randint(35,50)
        duration_base=delaytime/100
    
    duration=(duration_base+(random.randint(int(-duration_base*k),int(k*duration_base)))/k)
    print('winMoveTo: ',message,posi)
    pyautogui.moveTo(rel_x,rel_y,duration=duration,tween=pytweening.easeInOutQuad)
    delay(0.1)

def GetScreenImg():
    img = ImageGrab.grab()
    imsrc=np.array(img)
    return imsrc

def getWindowsInfo(classname,title):
    mainHnd=win32gui.FindWindow(classname,title)
    rect = win32gui.GetWindowRect(mainHnd)
    x,y=rect[0],rect[1]
    w,h=rect[2] - x,rect[3] - y
    y+=31
    x+=8
    return winInfo(x,y,w,h,mainHnd)
    

def GetScrWindowsImg(wininfo:winInfo,rangePosition=[0,0,0,0]):
 
    hwnd = wininfo.mainHnd
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    size = img.size()
    s = img.bits().asstring(size.width() * size.height() * img.depth() // 8)  # format 0xffRRGGBB
    arr = np.fromstring(s, dtype=np.uint8).reshape((size.height(), size.width(), img.depth() // 8))
    new_image = Image.fromarray(arr)
    bbox=wininfo.getRect()
    bbox[2]=bbox[0]+rangePosition[2]
    bbox[3]=bbox[1]+rangePosition[3]
    bbox[0]+=rangePosition[0]
    bbox[1]+=rangePosition[1]
    

    imsrc=np.array(new_image)
    imsrc=imsrc[rangePosition[1]:rangePosition[3],rangePosition[0]:rangePosition[2],:3]
    #plt.imshow(imsrc)
    #plt.show()
    #plt.savefig('img.jpg')#
    imsrc=cv2.cvtColor(imsrc,cv2.COLOR_RGB2BGR)
    return imsrc,[bbox[0],bbox[1]]#BGR

def leftClick():
    pyautogui.leftClick()

def leftDoubleClick(dt=0.05):
    pyautogui.leftClick()
    pyautogui.leftClick()
    
    
def rightClick():
    pyautogui.rightClick()
    delay(0.1)
    
def leftDrag(target,win_pos,max_float=3,duration_base=0.2,xadd=0,yadd=0):
    pyautogui.mouseDown()
    delay(0.2)
    winMoveTo(target,win_pos,max_float,duration_base,xadd,yadd)
    delay(0.4)
    pyautogui.mouseUp()
    delay(0.1)

def keyDown(key):
    pyautogui.keyDown(key)
    delay(0.1)

def keyUp(key):
    pyautogui.keyUp(key)
    delay(0.1)

def keyPress(key):
    pyautogui.keyDown(key)
    delay(0.05)
    pyautogui.keyUp(key)
    delay(0.1)

def getMousePosi(hwnd:winInfo):
    p=pyautogui.position()
    return [p[0]-hwnd.x,p[1]-hwnd.y]

def delay(x,randtime=True,isprint=True):
    a=random.randint(-10,10)
    if randtime:
        a=a*x*0.02
        if  x>0.2 and isprint:
            print('delay: ',x,'rand: ',x+a)
        time.sleep(x+a)
    else:
        if  x>0.2 and isprint:
            print('delay: ',x)
        time.sleep(x)