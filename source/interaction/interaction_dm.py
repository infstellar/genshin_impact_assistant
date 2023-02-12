import source.interaction.bit32_dll_bridge_client as dbc
from source.util import *
from source.interaction.interaction_template import InteractionTemplate
from source.funclib import static_lib

dbc.start_server(python_path="D:\\Program Files\\Anaconda\\envs\\GIA3732\\python.exe")
dbc.connect()

dmdll = dbc.DMDLL()
dmdll.start()
logger.debug(dmdll.ver())

class InteractionDm(InteractionTemplate):
    def __init__(self):
        dmdll.BindWindow(hwnd=static_lib.get_handle(), display='dx',
                        mouse="dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.state.message|dx.mouse.raw.input|dx.mouse.input.lock.api2|dx.mouse.api",
                        keypad='dx.keypad.raw.input', mode=101)
        err = dmdll.GetLastError()
        print(err)
        dmdll.EnableBind(1)
        # time.sleep(3)

        err = dmdll.GetLastError()
        print(err)
    
    def left_click(self):
        dmdll.LeftClick()
    
    def left_down(self):
        dmdll.LeftDown()
    
    def left_up(self):
        dmdll.LeftUp()
    
    def left_double_click(self):
        dmdll.LeftClick()
    
    def right_click(self):
        dmdll.RightClick()
    
    def key_down(self, key):
        dmdll.KeyDown(self.get_virtual_keycode(key))
    
    def key_up(self, key):
        dmdll.KeyUp(self.get_virtual_keycode(key))
    
    def key_press(self, key):
        dmdll.KeyPress(self.get_virtual_keycode(key))
    
    def move_to(self, x: int, y: int, relative=False, isChromelessWindow=False):
        if relative:
            dmdll.MoveR(x, y)
        else:
            dmdll.MoveTo(x, y)