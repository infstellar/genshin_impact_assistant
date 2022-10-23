try:
    from unit import *
except:
    from source.unit import *
import keyboard
import time

import alpha_loop
import domain_flow

combat_flag = False
domain_flag = False
global t1, t2
t1 = None
t2 = None
# @logger.catch
keymapjson = load_json("keymap.json")


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


# @logger.catch
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


keyboard.add_hotkey(keymapjson["autoCombat"], switch_combat_loop)
keyboard.add_hotkey(keymapjson["autoDomain"], switch_domain_loop)


@logger.catch
def listening():
    while (1):
        time.sleep(0.2)


if __name__ == '__main__':
    # 循环监听
    listening()
