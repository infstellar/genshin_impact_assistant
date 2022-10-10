try:
    from unit import *
except:
    from source.unit import *
import PyHook3,time
import alpha_loop, domain_flow
combat_flag=False
domain_flag=False
global t1, t2
t1=None
t2=None
# @logger.catch
def switch_combat_loop():
    global t1, combat_flag
    if combat_flag:
        logger.info('正在停止自动战斗')
        t1.stop_thread()
    else:
        logger.info('启动自动战斗')
        t1=alpha_loop.Alpha_Loop()
        t1.start()
    combat_flag = not combat_flag
# @logger.catch    
def switch_domain_loop():
    global t2, domain_flag
    if domain_flag:
        logger.info('正在停止自动秘境')
        t2.stop_thread()
    else:
        logger.info('启动自动秘境')
        t2=domain_flow.Domain_Flow_Control() 
        t2.start()
    domain_flag = not domain_flag


def OnKeyboardEvent(event):
              #同上，共同属性不再赘述
    #print('Message:',event.Message)
    # print('Time:',event.Time)
    # print('Window:',event.Window)
    # print('WindowName:',event.WindowName)
    # print('Ascii:', event.Ascii, chr(event.Ascii))   #按键的ASCII码
                           #按键的名称
    # print('KeyID:', event.KeyID)                     #按键的虚拟键值
    #print('ScanCode:', event.ScanCode)               #按键扫描码
    # print('Extended:', event.Extended)               #判断是否为增强键盘的扩展键
    # print('Injected:', event.Injected)
    # print('Alt', event.Alt)                          #是某同时按下Alt
    #print('Transition', event.Transition)            #判断转换状态
    # print('---')
    #print('Key:', event.Key) 
    
    if event.Key=='Oem_2' and event.MessageName=='key down':
        logger.debug('MessageName: '+event.MessageName)
        logger.debug('Key:', event.Key)  
        switch_combat_loop()
        
    if event.Key=='Oem_6' and event.MessageName=='key down':
        logger.debug('MessageName: '+event.MessageName)
        logger.debug('Key: '+ event.Key)  
        switch_domain_loop()

  # 同上
    return True


hm = PyHook3.HookManager()  # 创建一个HOOK管理对象
hm.KeyDown = OnKeyboardEvent # 绑定键盘处理函数--就是我们创建的函数
hm.HookKeyboard()   # 初始化
data = []

@logger.catch
def listening():
    import pythoncom
    pythoncom.PumpMessages()
    while(1):
        time.sleep(0.1)


if __name__ == '__main__':

    # 循环监听
    listening()