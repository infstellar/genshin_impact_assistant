import asyncio
import threading
from pywebio import platform

# import source.config
# print(source.config.template_translator())
# print(source.config.template_translator_tactic())

from source.webio import webio



def server_thread():
    # https://zhuanlan.zhihu.com/p/101586682
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ###

    platform.tornado.start_server(webio.main, auto_open_webbrowser=True, port = 22268, debug=False)

threading.Thread(target=server_thread, daemon=False).start()

import source.util
from source.error_code.main_err import *

source.util.logger.info(source.util.t2t('正在初始化，请稍后'))
# source.unit.logger.info('Initializing, please hold on')


try:
    import source.listening
except Exception as error:
    source.util.logger.critical(source.util.t2t("导入依赖时错误"))
    IMPORT_ERROR_1.log()
    source.util.logger.exception(error)
    input(source.util.t2t('程序暂停。按任意键退出'))

try:
    import source.common.generic_event
except Exception as error:
    source.util.logger.critical(source.util.t2t("导入依赖时错误"))
    IMPORT_ERROR_2.log()
    source.util.logger.exception(error)
    input(source.util.t2t('程序暂停。按任意键退出'))

source.util.logger.info(source.util.t2t('初始化完成'))
source.util.logger.info(source.util.t2t("正在等待webio启动"))
source.util.logger.info(source.util.t2t("启动键盘监听"))
source.listening.listening()
