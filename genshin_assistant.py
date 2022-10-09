import source.unit
import win32api, win32con, win32gui, pyautogui
source.unit.logger.info('正在初始化，请稍后')
source.unit.logger.info('Initializing, please hold on')
import requests, unittest
import source.listening

source.unit.logger.info('初始化完成')
source.unit.logger.info('Initialization Completed')
source.listening.listening()
