from typing import TextIO

from source.webio import manager
from source.util import DEMO_MODE

def ansl_code2col(ansl_code):
    if ansl_code == "0":
        return 'black'
    elif ansl_code == "31":
        return "red"
    elif ansl_code == "32":
        return "green"
    elif ansl_code == "33":
        return "olive"
    elif ansl_code == "34":
        return "blue"
    elif ansl_code == "35":
        return "green"
    elif ansl_code == "36": # cyan
        return "#0099CC"
    elif ansl_code == "37": # white
        return "black"
    
    return "NO_COL"

def webio_poster(record:str):
    if DEMO_MODE:
        if "DEMO" not in record:
            return
    record_list = record.split("\x1b")
    color = "black"
    for text in record_list:
        if text == '':
            continue
        ansl_code = text[text.index("[")+1:text.index("m")]
        c = ansl_code2col(ansl_code)
        if c != "NO_COL":
            color = ansl_code2col(ansl_code)
        text = text[text.index("m")+1:]
        manager.get_page('MainPage').logout(text, color=color)
    
    manager.get_page('MainPage').logout("$$end$$")

class WebioHandler(TextIO):

    def __init__(self, x):
        print(x)
        pass

# '\x1b[32m2022-12-25 22:05:58.814\x1b[0m | \x1b[34m\x1b[1mDEBUG   \x1b[0m | \x1b[36mcvAutoTrack\x1b[0m:\x1b[36mdel_log\x1b[0m:\x1b[36m103\x1b[0m - \x1b[34m\x1b[1m正在清理cvautotrack文件\x1b[0m\n'
# webio_handler = WebioHandler()
