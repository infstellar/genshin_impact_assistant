import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL('user32', use_last_error=True)

WH_KEYBOARD_LL = ctypes.c_int(13)
WM_KEYDOWN = 0x0100

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode', wintypes.DWORD),
        ('scanCode', wintypes.DWORD),
        ('flags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
    ]

def low_level_keyboard_handler(nCode, wParam, lParam):
    if wParam == WM_KEYDOWN:
        hookStruct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        if hookStruct.vkCode == ord('W'):
            print('w key pressed')
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

def main():
    CMPFUNC = ctypes.CFUNCTYPE(wintypes.LPARAM, wintypes.WPARAM, wintypes.LPARAM, wintypes.LPARAM)
    pointer = CMPFUNC(low_level_keyboard_handler)
    hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, None, 0)
    msg = wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageA(ctypes.byref(msg))
    user32.UnhookWindowsHookEx(hook)

if __name__ == '__main__':
    main()