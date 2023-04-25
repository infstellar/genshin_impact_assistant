try:
    from source.util import *
except:
    from source.util import *
import time
import keyboard
from source.task import task_manager
from source.mission import mission_manager

combat_flag = False
collector_flag = False
startstop_flag = False
TASK_MANAGER = task_manager.TASK_MANAGER
TASK_MANAGER.setDaemon(True)
# TASK_MANAGER.pause_threading()
TASK_MANAGER.start()
# MISSION_MANAGER = mission_manager.MissionManager()
# MISSION_MANAGER.setDaemon(True)
# MISSION_MANAGER.pause_threading()
# MISSION_MANAGER.start()

t1 = None
t3 = None
# @logger.catch


FLOW_IDLE = 0
FLOW_COMBAT = 1  # 自动战斗
FLOW_COLLECTOR = 3  # 自动采集
FEAT_PICKUP = False  # 拾取辅助

current_flow = FLOW_IDLE
"""
FLOW型功能：同时只能启动一个，空闲时为FLOW_IDLE
FEAT型功能：可以启动多个，用bool值控制
"""

global icm
icm = False
def call_you_import_module():
    global icm
    icm = True

def import_current_module():
    if False:
        if current_flow == FLOW_IDLE:
            pass
        elif current_flow == FLOW_COMBAT:
            # logger.info("正在导入 FLOW_COMBAT 模块，可能需要一些时间。")
            from source.flow import alpha_loop
        elif current_flow == FLOW_DOMAIN:
            # logger.info("正在导入 FLOW_DOMAIN 模块，可能需要一些时间。")
            from source.flow import domain_flow
        elif current_flow == FLOW_COLLECTOR:
            # logger.info("正在导入 FLOW_COLLECTOR 模块，可能需要一些时间。")
            from source.flow import collector_flow
    else:
        try:
            if current_flow == FLOW_IDLE:
                pass
            elif current_flow == FLOW_COMBAT:
                # logger.info("正在导入 FLOW_COMBAT 模块，可能需要一些时间。")
                from source.flow import alpha_loop
            # elif current_flow == FLOW_COLLECTOR:
            #     # logger.info("正在导入 FLOW_COLLECTOR 模块，可能需要一些时间。")
            #     from source.flow import collector_flow
        except Exception as e:
            logger.critical(f"IMPORT ERROR: current_flow: {current_flow}")
            logger.exception(e)
            input(t2t("Program stop."))

def switch_combat_loop():
    global t1, combat_flag
    if combat_flag:
        logger.info(t2t('正在停止自动战斗'))
        t1.stop_threading()
    else:
        from source.controller.combat_controller import CombatController
        logger.info(t2t('启动自动战斗'))
        t1 = CombatController()
        t1.setDaemon(True)
        t1.start()
        time.sleep(1)
        t1.continue_threading()
    combat_flag = not combat_flag

def switch_collector_loop():
    global t3, collector_flag
    if collector_flag:
        logger.info(t2t('正在停止自动采集'))
        t3.stop_threading()
    else:
        logger.info(t2t('启动自动采集'))
        from source.flow import collector_flow
        t3 = collector_flow.CollectorFlow()
        t3.setDaemon(True)
        t3.start()
    collector_flag = not collector_flag

def apply_ui_setting():  # "应用设置"按钮回调函数
    ui_FEAT_PICKUP = None  # ui的设置(bool)
    if ui_FEAT_PICKUP != FEAT_PICKUP:
        FEAT_PICKUP = ui_FEAT_PICKUP  # 同步ui设置
        if FEAT_PICKUP:
            pass  # 启动自动拾取
        else:
            pass  # 关闭自动拾取

@logger.catch
def startstop():
    global startstop_flag
    if current_flow == FLOW_IDLE:
        pass
    elif current_flow == FLOW_COMBAT:
        startstop_flag = not startstop_flag
        switch_combat_loop()
    elif current_flow == FLOW_COLLECTOR:
        startstop_flag = not startstop_flag
        switch_collector_loop()

if GIAconfig.Keymap_StartStop != "":
    keyboard.add_hotkey(GIAconfig.Keymap_StartStop, startstop)
# keyboard.add_hotkey(load_json("keymap.json", f"{CONFIG_PATH_SETTING}")["task"], TASK_MANAGER.start_stop_tasklist)

@logger.catch
def listening():
    global icm
    while 1:
        time.sleep(0.2)
        if icm:
            import_current_module()
            logger.info(t2t("导入完成"))
            icm = False
        # webio.log_handler.webio_poster('213')



if __name__ == '__main__':
    # 循环监听
    listening()
