import source.interaction.bit32_dll_bridge_client as dbc
from source.util import *
from source.interaction.interaction_template import InteractionTemplate
from source.common import static_lib

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
jso = json.load(open(os.path.join(root_path, "config\\settings\\dm.json"), 'r', encoding='utf-8'))
dbc.start_server(python_path=jso["python32_path"])
dbc.connect()

dmdll = dbc.DMDLL()
dmdll.start()
logger.debug(dmdll.ver())
global bind_flag
bind_flag = False
def unbind():
    global bind_flag
    if bind_flag != False:
        bind_flag = False
        dmdll.EnableBind(0)
        logger.debug(dmdll.GetLastError())
        dmdll.UnBindWindow()
        logger.debug(dmdll.GetLastError())

def bind():
    global bind_flag
    if bind_flag != True:
        bind_flag = True
        dmdll.BindWindow(hwnd=static_lib.get_handle(), display='dx',
                        mouse="dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.state.message|dx.mouse.raw.input|dx.mouse.input.lock.api2|dx.mouse.api|dx.mouse.input.lock.api3",
                        keypad='dx.keypad.raw.input', mode=101)
        logger.debug(dmdll.GetLastError())
        dmdll.EnableBind(1)
        logger.debug(dmdll.GetLastError())

class InteractionDm(InteractionTemplate):
    def __init__(self):
        bind()
    
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
    
    def middle_click(self):
        dmdll.MiddleClick()
    
    def key_down(self, key):
        dmdll.KeyDown(self.get_virtual_keycode(key))
    
    def key_up(self, key):
        dmdll.KeyUp(self.get_virtual_keycode(key))
    
    def key_press(self, key):
        dmdll.KeyPress(self.get_virtual_keycode(key))
    
    def move_to(self, x: int, y: int, relative=False, isBorderlessWindow=False):
        if relative:
            dmdll.MoveR(x, y)
        else:
            dmdll.MoveTo(x, y)