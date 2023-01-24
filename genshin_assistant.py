import asyncio
import threading
import time
from pywebio import platform
from source.webio import webio
import source.webio.log_handler
def server_thread():
    # https://zhuanlan.zhihu.com/p/101586682
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ###

    platform.tornado.start_server(webio.main, auto_open_webbrowser=True, reconnect_timeout = 10, port = 22268)

threading.Thread(target=server_thread, daemon=False).start()

import source.util


source.util.logger.info(source.util._('正在初始化，请稍后'))
# source.unit.logger.info('Initializing, please hold on')


try:
    import source.listening
except Exception as error:
    source.util.logger.critical(source.util._("导入依赖时错误; err code: 001_1"))
    source.util.logger.exception(error)
    input(source.util._('程序暂停。按任意键退出'))

try:
    import source.generic_event
except Exception as error:
    source.util.logger.critical(source.util._("导入依赖时错误; err code: 001_2"))
    source.util.logger.exception(error)
    input(source.util._('程序暂停。按任意键退出'))

source.util.logger.info(source.util._('初始化完成'))
source.util.logger.info(source.util._("正在等待webio启动"))
source.util.logger.info(source.util._("启动键盘监听"))
source.listening.listening()
