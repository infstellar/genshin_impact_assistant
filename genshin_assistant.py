import asyncio
import threading

from pywebio import platform

import time
import source.util
from pywebio import platform
from source.webio import webio


def server_thread():
    # https://zhuanlan.zhihu.com/p/101586682
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ###

    platform.tornado.start_server(webio.main, auto_open_webbrowser=True, debug=source.util.DEBUG_MODE)


threading.Thread(target=server_thread, daemon=False).start()
time.sleep(10)

import win32api, win32con, win32gui, pyautogui, requests, unittest, xml, inspect, keyboard  # 用于pyinstaller，不要删除！

source.util.logger.info('正在初始化，请稍后')
# source.unit.logger.info('Initializing, please hold on')


try:
    import source.listening
except Exception as error:
    source.util.logger.critical("导入依赖时错误; err code: 001_1")
    source.util.logger.exception(error)
    input('程序暂停。按任意键退出')

source.util.logger.info('初始化完成')

# source.unit.logger.info('Initialization Completed')

source.listening.listening()
