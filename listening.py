from win32gui import FindWindow
import PyHook3,time
import alpha_loop
combat_flag=False
global t1
t1=None
def switch_combat_loop():
    global t1, combat_flag
    if combat_flag:
        t1.stop_thread()
    else:
        t1=alpha_loop.Alpha_Loop()
        t1.start()
    combat_flag = not combat_flag


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
    
    if event.Key=='Oem_2' and event.MessageName=='key down':
        print('MessageName:',event.MessageName)
        print('Key:', event.Key)  
        switch_combat_loop()
    

  # 同上
    return True


hm = PyHook3.HookManager()  # 创建一个HOOK管理对象
hm.KeyDown = OnKeyboardEvent # 绑定键盘处理函数--就是我们创建的函数
hm.HookKeyboard()   # 初始化
data = []
if __name__ == '__main__':

    # 循环监听
    import pythoncom
    pythoncom.PumpMessages()
    while(1):
        time.sleep(0.1)
