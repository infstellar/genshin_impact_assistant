try:
    from util import *
except:
    from source.util import *
import time

import keyboard

import alpha_loop
import domain_flow

combat_flag = False
domain_flag = False

t1 = None
t2 = None
# @logger.catch


FLOW_IDLE = 0
FLOW_COMBAT = 1  # 自动战斗
FLOW_DOMAIN = 2  # 自动秘境
FEAT_PICKUP = False  # 拾取辅助
current_flow = FLOW_IDLE
"""
FLOW型功能：同时只能启动一个，空闲时为FLOW_IDLE
FEAT型功能：可以启动多个，用bool值控制
"""

keymap_json = load_json("keymap.json")


def switch_combat_loop():
    global t1, combat_flag
    if combat_flag:
        logger.info('正在停止自动战斗')
        t1.stop_threading()
    else:
        logger.info('启动自动战斗')
        t1 = alpha_loop.AlphaLoop()
        t1.setDaemon(True)
        t1.start()
    combat_flag = not combat_flag


def switch_domain_loop():
    global t2, domain_flag
    if domain_flag:
        logger.info('正在停止自动秘境')
        t2.stop_threading()
    else:
        logger.info('启动自动秘境')

        t2 = domain_flow.DomainFlow()
        t2.setDaemon(True)
        t2.start()
    domain_flag = not domain_flag


def apply_ui_setting():  # "应用设置"按钮回调函数
    ui_FEAT_PICKUP = None  # ui的设置(bool)
    if ui_FEAT_PICKUP != FEAT_PICKUP:
        FEAT_PICKUP = ui_FEAT_PICKUP  # 同步ui设置
        if FEAT_PICKUP:
            pass  # 启动自动拾取
        else:
            pass  # 关闭自动拾取


def startstop():
    if current_flow == FLOW_IDLE:
        pass
    elif current_flow == FLOW_COMBAT:
        switch_combat_loop()
    elif current_flow == FLOW_DOMAIN:
        switch_domain_loop()


keyboard.add_hotkey(keymap_json["autoCombat"], switch_combat_loop)
keyboard.add_hotkey(keymap_json["autoDomain"], switch_domain_loop)
keyboard.add_hotkey(keymap_json["startstop"], startstop)


@logger.catch
def listening():
    while 1:
        time.sleep(0.2)


if __name__ == '__main__':
    # 循环监听
    listening()
