try:
    from source.util import *
except:
    from util import *
import time
import keyboard
from source.task import task_manager
import threading
from source.ingame_ui.ingame_ui import run_ingame_ui
from source.ingame_assist.manager import IngameAssistManager
from source.semiauto_funcs.manager import SemiautoFuncManager
TASK_MANAGER = task_manager.TASK_MANAGER
INGAME_ASSIST_MANAGER = IngameAssistManager()
SEMIAUTO_FUNC_MANAGER = SemiautoFuncManager()
threading.excepthook = TASK_MANAGER.task_excepthook
TASK_MANAGER.setDaemon(True)
TASK_MANAGER.start()
keyboard.add_hotkey(GIAconfig.Keymap_StartStop, SEMIAUTO_FUNC_MANAGER.apply_change)

# keyboard.add_hotkey(load_json("keymap.json", f"{CONFIG_PATH_SETTING}")["task"], TASK_MANAGER.start_stop_tasklist)

@logger.catch
def listening():
    run_ingame_ui()
    logger.error('pyqt exit')
    # ingame_app.start("python", ["source\\ingame_ui\\ingame_ui.py"])
    # # main_app.waitForFinished()
    # print('start succ\n')
    #
    while 1:
        time.sleep(0.2)


if __name__ == '__main__':
    # 循环监听
    listening()
