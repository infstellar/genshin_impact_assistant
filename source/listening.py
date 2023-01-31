try:
    from util import *
except:
    from source.util import *
import time
import keyboard


combat_flag = False
domain_flag = False
collector_flag = False
startstop_flag = False

t1 = None
t2 = None
t3 = None
# @logger.catch


FLOW_IDLE = 0
FLOW_COMBAT = 1  # 自动战斗
FLOW_DOMAIN = 2  # 自动秘境
FLOW_COLLECTOR = 3  # 自动采集
FEAT_PICKUP = False  # 拾取辅助

current_flow = FLOW_IDLE
"""
FLOW型功能：同时只能启动一个，空闲时为FLOW_IDLE
FEAT型功能：可以启动多个，用bool值控制
"""

keymap_json = load_json("keymap.json")
global icm
icm = False
def call_you_import_module():
    global icm
    icm = True

def import_current_module():
    try:
        if current_flow == FLOW_IDLE:
            pass
        elif current_flow == FLOW_COMBAT:
            # logger.info("正在导入 FLOW_COMBAT 模块，可能需要一些时间。")
            import alpha_loop
        elif current_flow == FLOW_DOMAIN:
            # logger.info("正在导入 FLOW_DOMAIN 模块，可能需要一些时间。")
            import domain_flow
        elif current_flow == FLOW_COLLECTOR:
            # logger.info("正在导入 FLOW_COLLECTOR 模块，可能需要一些时间。")
            import collector_flow
    except Exception as e:
        logger.critical(f"IMPORT ERROR: current_flow: {current_flow}")
        print(e)
        input(_("Program stop."))

def switch_combat_loop():
    global t1, combat_flag
    if combat_flag:
        logger.info(_('正在停止自动战斗'))
        t1.stop_threading()
    else:
        import alpha_loop
        logger.info(_('启动自动战斗'))
        t1 = alpha_loop.AlphaLoop()
        t1.setDaemon(True)
        t1.start()
    combat_flag = not combat_flag


def switch_domain_loop():
    global t2, domain_flag
    if domain_flag:
        logger.info(_('正在停止自动秘境'))
        t2.stop_threading()
    else:
        import domain_flow
        logger.info(_('启动自动秘境'))
        t2 = domain_flow.DomainFlow()
        t2.setDaemon(True)
        t2.start()
    domain_flag = not domain_flag

def switch_collector_loop():
    global t3, collector_flag
    if collector_flag:
        logger.info(_('正在停止自动采集'))
        t3.stop_threading()
    else:
        logger.info(_('启动自动采集'))
        import collector_flow
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
    elif current_flow == FLOW_DOMAIN:
        startstop_flag = not startstop_flag
        switch_domain_loop()
    elif current_flow == FLOW_COLLECTOR:
        startstop_flag = not startstop_flag
        switch_collector_loop()

if keymap_json["autoCombat"] != "":
    keyboard.add_hotkey(keymap_json["autoCombat"], switch_combat_loop)
if keymap_json["autoDomain"] != "":
    keyboard.add_hotkey(keymap_json["autoDomain"], switch_domain_loop)
if keymap_json["startstop"] != "":
    keyboard.add_hotkey(keymap_json["startstop"], startstop)


@logger.catch
def listening():
    global icm
    while 1:
        time.sleep(0.2)
        if icm:
            import_current_module()
            logger.info(_("导入完成"))
            icm = False
        # webio.log_handler.webio_poster('213')



if __name__ == '__main__':
    # 循环监听
    listening()
