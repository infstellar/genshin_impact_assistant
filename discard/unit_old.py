import sys
import time


class Logger(object):
    def __init__(self, fileN='Terminal.log'):
        self.terminal = sys.stdout

        try:
            self.log = open(fileN, 'a')
        except FileNotFoundError:
            open(fileN, 'w')
            self.log = open(fileN, 'a')
        self.messageCache = ''
        self.log.write('\n\n\n')

    def write(self, message):
        """print实际相当于sys.stdout.write"""
        self.terminal.write(message)
        now_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        if message != '\n':
            self.messageCache += message
        else:
            self.log.write(now_time + ':    ' + self.messageCache + '\n')
            self.messageCache = ''
            self.log.flush()

    def flush(self):
        pass


sys.stdout = Logger()  # 'G:/2.0/test.txt'
print('import: math,turtle')
import math

# from turtle import getscreen
print('import: cv2')
import cv2

print('import: paddleocr')
from paddleocr import PaddleOCR
from paddleocr import draw_ocr

print('import: numpy')
import numpy as np

print('import: PIL')
from PIL import ImageGrab, Image

print('import: win32api,win32con,win32gui,random')
import random

print('import: pyautogui')
import pyautogui as ag

print('import: pytweening')
import pytweening

print('import: PyQt5.QtWidgets')
from PyQt5.QtWidgets import QApplication

print('import: win32gui,sys')
import win32gui
import sys

print('import: matplotlib.pyplot')

ag.MINIMUM_SLEEP = 0.03
# from auto_battle import IMG_enemy_bs
# IMG_enemy_frigate=cv2.imread('imgs/enemy_frigate.png',1)
APPROXIMATE_MATCHING = 0
ACCURATE_MATCHING = 1
TWICE_AND_MATCHING = 3
TWICE_OR_MATCHING = 5
TWICE_FRONTANDBACK_MATCHING = 4
TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING = 6
REPEATLY_MATCHING = 7

CHANNEL_RED = 2
RETURN_TEXT = 1
RETURN_POSITION = 0


class winInfo:
    def __init__(self, x, y, w, h, mainHnd):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mainHnd = mainHnd
        self.winpos = [x, y]

    def getRect(self, rangePosition=[0, 0, 0, 0]):
        return [self.x, self.y, self.w + self.x, self.h + self.y]


def GetScreenImg():
    img = ImageGrab.grab()
    imsrc = np.array(img)
    return imsrc


def getWindowsInfo(classname, title):
    mainHnd = win32gui.FindWindow(classname, title)
    rect = win32gui.GetWindowRect(mainHnd)
    x, y = rect[0], rect[1]
    w, h = rect[2] - x, rect[3] - y
    y += 31
    x += 8
    return winInfo(x, y, w, h, mainHnd)


def GetScrWindowsImg(wininfo: winInfo, rangePosition=[0, 0, 0, 0]):
    hwnd = wininfo.mainHnd
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    size = img.size()
    s = img.bits().asstring(size.width() * size.height() * img.depth() // 8)  # format 0xffRRGGBB
    arr = np.fromstring(s, dtype=np.uint8).reshape((size.height(), size.width(), img.depth() // 8))
    new_image = Image.fromarray(arr)
    bbox = wininfo.getRect()
    bbox[2] = bbox[0] + rangePosition[2]
    bbox[3] = bbox[1] + rangePosition[3]
    bbox[0] += rangePosition[0]
    bbox[1] += rangePosition[1]

    imsrc = np.array(new_image)
    imsrc = imsrc[rangePosition[1]:rangePosition[3], rangePosition[0]:rangePosition[2], :3]
    # plt.imshow(imsrc)
    # plt.show()
    # plt.savefig('img.jpg')#
    imsrc = cv2.cvtColor(imsrc, cv2.COLOR_RGB2BGR)
    return imsrc, [bbox[0], bbox[1]]  # BGR


class ImgAnalyse:

    def __init__(self, lang='ch'):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang,
                             show_log=False)  # need to run only once to download and load model into memory

    def ImgAnalyse(self, imsrc):
        result = self.ocr.ocr(imsrc, cls=False)
        '''for line in result:
            print(line)'''
        return result

    def imgAnalysePlus(self, hwnd: winInfo, rangePosition):
        imsrc, position = GetScrWindowsImg(hwnd, rangePosition)
        res = self.ImgAnalyse(imsrc)
        return res, position

    @staticmethod
    def SaveResult(imsrc, result):
        from PIL import Image
        # image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(imsrc, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')

    @staticmethod
    def findText(result, text, mode=APPROXIMATE_MATCHING):
        if mode == APPROXIMATE_MATCHING:
            for i in range(len(result)):
                if text in result[i][1][0]:
                    return result[i]
        elif mode == ACCURATE_MATCHING:
            for i in range(len(result)):
                if result[i][1][0] == text:
                    return result[i]
        elif mode == TWICE_AND_MATCHING:
            for i in range(len(result)):
                if text[0] in result[i][1][0] and text[1] in result[i][1][0]:
                    print('TWICE_AND_MATCHING found ', text, end='')
                    return result[i]
        elif mode == TWICE_FRONTANDBACK_MATCHING:
            for i in range(len(result)):
                if i != len(result) - 1:
                    if (text[0] in result[i][1][0] or text[1] in result[i][1][0]) and (
                            text[0] in result[i + 1][1][0] or text[1] in result[i + 1][1][0]):
                        return result[i]
        elif mode == TWICE_OR_MATCHING:
            for i in range(len(result)):
                if text[0] in result[i][1][0] or text[1] in result[i][1][0]:
                    return result[i]
        elif mode == TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING:
            for i in range(len(result)):
                if (i != len(result) - 1) and (text[0] in result[i][1][0]) and (text[1] in result[i + 1][1][0]):
                    print('TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING found ', text, end='')
                    return result[i]
        elif mode == REPEATLY_MATCHING:
            result = []
            for i in range(len(result)):
                if (i != len(result) - 1) and (text[0] in result[i][1][0]) and (text[1] in result[i + 1][1][0]):
                    print('TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING found ', text, end='')
                    result.append(result[i])
            if result:
                return result
        return None

    def getTextPosition(self, hwnd: winInfo, rangePosition, text, mode=APPROXIMATE_MATCHING, returnMode=RETURN_POSITION,
                        isprintlog=True, message='', defaultend='\n'):
        imsrc, position = GetScrWindowsImg(hwnd, rangePosition)
        res = self.ImgAnalyse(imsrc)
        resposition = self.findText(res, text, mode=mode)
        print('getTextPosition:  ', message, end=' | ')
        if isprintlog:
            print('res: ', end='')
            for i in res:
                print(i[1][0], end=', ')
            print(end=defaultend)
        # cv2.imshow('pic',imsrc)
        # cv2.waitKey(0)
        if resposition is not None:
            # print('resposition',resposition)
            if mode == REPEATLY_MATCHING and returnMode == RETURN_POSITION:
                result = []
                for i in resposition:
                    result.append(
                        [resposition[0][0][0] + position[0] - hwnd.x, resposition[0][0][1] + position[1] - hwnd.y])
                return result
            if returnMode == RETURN_POSITION:
                print('found the text:', text)
                return [resposition[0][0][0] + position[0] - hwnd.x, resposition[0][0][1] + position[1] - hwnd.y]
            elif returnMode == RETURN_TEXT:
                print('found the text:', text)
                return resposition[1][0]
        else:
            print('can not find the text:', text)
            return -1

    @staticmethod
    def imgComparison(hwnd: winInfo, rangePosition, objectImg, mode=0, minThreshold=0, name='', channel=-1):
        imsrc, position = GetScrWindowsImg(hwnd, rangePosition)

        img = cv2.cvtColor(imsrc, cv2.COLOR_RGB2BGR)
        # img = objectImg

        if channel == -1:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(objectImg, cv2.COLOR_BGR2GRAY)  # BGR format
        else:
            gray = img[:, :, channel]
            img2 = objectImg[:, :, channel]
        w, h = img2.shape[::-1]
        res = cv2.matchTemplate(gray, img2, cv2.TM_CCOEFF_NORMED)
        # print(res)
        threshold = 0.9
        loc = np.where(res >= threshold)
        # print(loc)
        L = 0
        R = 1
        count = 0
        while 1:
            threshold = (L + R) / 2
            count += 1
            # print(count)
            loc = np.where(res >= threshold)
            if len(loc[0]) > 1:
                L += (R - L) / 2
            elif len(loc[0]) == 1:
                # print(loc)
                pt = loc[::-1]
                # print('目标区域的左上角坐标:',pt[0],pt[1])
                # print('次数:',count)
                # print('阀值',threshold)
                break
            elif len(loc[0]) < 1:
                R -= (R - L) / 2
            if count >= 100:
                return -1
        print('name: ', name, end='   ')
        print('imgComparison:', [pt[0][0] + position[0], pt[1][0] + position[1]], end=' ')
        print('threshold:', threshold)
        cv2.rectangle(img, (pt[0][0], pt[1][0]), (pt[0][0] + w, pt[1][0] + h), (34, 139, 139), 2)

        cropImg = img[pt[1][0]:pt[1][0] + h, pt[0][0]:pt[0][0] + w]
        '''cv2.imshow('pic',cropImg)
        cv2.imshow('pic2',img)
        cv2.waitKey(0)'''
        if mode == 1:
            return cropImg
        if threshold <= minThreshold:
            return -1
        return [pt[0][0] + position[0] - hwnd.x, pt[1][0] + position[1] - hwnd.y]


def winMoveTo(posi, win_pos, max_float=3, duration_base=0.2, xadd=0, yadd=0, message=''):
    if posi == -1:
        print('\n\n\n\n\n ERROR: winMoveToError, please check up the program. \n\n\n\n\n')
        if True:
            raise RuntimeError('winMoveToError: posi should not be -1')
    x = posi[0]
    y = posi[1]
    k = 1000  # 放大倍率,越大随机数越准
    mouse_position = ag.position()
    rel_x = x + xadd + win_pos[0] + random.randint(0, max_float)
    rel_y = y + yadd + win_pos[1] + random.randint(0, max_float)

    if duration_base == 0.2:
        distance = math.sqrt(((mouse_position[0] - rel_x) ** 2 + (mouse_position[1] - rel_y) ** 2))
        delaytime = distance / random.randint(35, 50)
        duration_base = delaytime / 100

    duration = (duration_base + (random.randint(int(-duration_base * k), int(k * duration_base))) / k)
    print('winMoveTo: ', message, posi)
    ag.moveTo(rel_x, rel_y, duration=duration, tween=pytweening.easeInOutQuad)
    delay(0.1)


def leftClick():
    ag.leftClick()


def leftDoubleClick(dt=0.05):
    ag.leftClick()
    ag.leftClick()


def rightClick():
    ag.rightClick()
    delay(0.1)


def leftDrag(target, win_pos, max_float=3, duration_base=0.2, xadd=0, yadd=0):
    ag.mouseDown()
    delay(0.2)
    winMoveTo(target, win_pos, max_float, duration_base, xadd, yadd)
    delay(0.4)
    ag.mouseUp()
    delay(0.1)


def keyDown(key):
    ag.keyDown(key)
    delay(0.1)


def keyUp(key):
    ag.keyUp(key)
    delay(0.1)


def keyPress(key):
    ag.keyDown(key)
    delay(0.05)
    ag.keyUp(key)
    delay(0.1)


def getMousePosi(hwnd: winInfo):
    p = ag.position()
    return [p[0] - hwnd.x, p[1] - hwnd.y]


def delay(x, randtime=True, isprint=True):
    a = random.randint(-10, 10)
    if randtime:
        a = a * x * 0.02
        if x > 0.2 and isprint:
            print('delay: ', x, 'rand: ', x + a)
        time.sleep(x + a)
    else:
        if x > 0.2 and isprint:
            print('delay: ', x)
        time.sleep(x)


if __name__ == '__main__':
    # winMoveTo([0,0])
    hwnd = getWindowsInfo("trinityWindow", "原神")
    print("窗口相对偏移：", hwnd.winpos)
    ia = ImgAnalyse()
    # GetScrWindowsImg(hwnd,hwnd.getRect())
    d = ia.getTextPosition(hwnd, hwnd.getRect(), ':', returnMode=RETURN_TEXT)
