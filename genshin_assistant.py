import source.util
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
