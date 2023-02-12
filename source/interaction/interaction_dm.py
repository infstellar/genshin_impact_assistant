import bit32_dll_bridge_client as dbc
from source.util import *
from interaction_template import InteractionTemplate

dbc.start_server(python_path="D:\\Program Files\\Anaconda\\envs\\GIA3732\\python.exe")
dbc.connect()

dmdll = dbc.DMDLL()
dmdll.start()
logger.debug(dmdll.ver())

class InteractionDm(InteractionTemplate):
    def __init__(self):
        pass
    
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