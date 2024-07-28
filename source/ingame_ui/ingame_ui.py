import sys
import threading
import time

import win32gui
import win32con
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from source.config.config import GIAconfig
from source.common import static_lib, timer_module
from source.cvars import PROCESS_NAME
from source.util import DEMO_MODE, ansl_code2col, DEBUG_MODE
from source.logger import add_logger_to_GUI, logger
from source.interaction.interaction_core import itt
K = 5


class IngameUI(QWidget):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("IngameUI")
        self.QTextEdit_log_output = QTextEdit(self)
        _ = 300 if DEBUG_MODE else 0
        self.QTextEdit_log_output.setGeometry(0, 850 - _, 550, 230 + _)
        # self.log_output.setHtml("QTextEdit Demo!<font color='blue' size='8'><red>Hello PyQt5!</font>")
        self.QTextEdit_log_output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.notice_label = QLabel(self)
        self.notice_label.setAlignment(Qt.AlignCenter)
        self.notice_label.setGeometry(0,130,1920,170)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # layout = QLayout(self)
        # layout.addWidget(self.label, 1, 3)
        # self.setLayout(layout)
        self.notice_label.setText(f'<font color=white size=32><b>123456<br>test</b>')
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Qt.Tool
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(int(1000 / K))
        self.setGeometry(0, 0, 1920, 1080)  # 设置窗口位置和大小
        # self.setWindowOpacity(0)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TransparentForMouseEvents, on=True) # Qt.WA_TranslucentBackground | Qt.WA_ShowWithoutActivating |
        self.setAttribute(Qt.WA_ShowWithoutActivating, on=True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)
        # 设置窗口样式为 WS_EX_TRANSPARENT
        hwnd = int(self.winId())
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT)
        self.notice_label.setText(f'')
        self.stop_output_flag = False


        # MISC
        self.last_bbox = 0
        self.log_history = []
        self.notice_text = ''
        self.last_notice_text = '1'
        self.notice_timer = timer_module.AdvanceTimer(9999999999999999999999999999)

        self.handle_settled = False

    def mousePressEvent(self, event):
        # 不处理鼠标点击事件
        pass

    def mouseMoveEvent(self, event):
        # 不处理鼠标移动事件
        pass

    def mouseReleaseEvent(self, event):
        # 不处理鼠标释放事件
        pass

    def show_win(self):

        self.setAttribute(Qt.WA_TransparentForMouseEvents, on=True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, on=True)
        self.show()

    def update_time(self):



        if not static_lib.get_active_window_process_name() in PROCESS_NAME:
            if self.isVisible():
                self.hide()
        else:
            if not self.handle_settled:
                if not itt.is_vaild_handel():
                    return
                else:
                    static_lib.HANDLE = static_lib.get_handle()
                    self.handle_settled = True
            if not self.isVisible():
                self.stop_output_flag = False
                self.show_win()
                self.stop_output_flag = True

        if self.isVisible():
            win_bbox = win32gui.GetWindowRect(static_lib.HANDLE)  # wx, wy, w, h.
            if self.last_bbox != win_bbox:
                dy = 0
                if not GIAconfig.General_BorderlessWindow:
                    dy = 31
                self.move(int(win_bbox[0]+4), int(win_bbox[1]+dy)) # 31
                self.last_bbox = win_bbox
            self.QTextEdit_log_output.setHtml(self.generate_log_html())
            self.QTextEdit_log_output.moveCursor(QTextCursor.End)

            if self.last_notice_text != self.notice_text:
                self.notice_label.setText(self.notice_text)
                self.last_notice_text = self.notice_text
                if self.notice_text == '':
                    self.notice_label.hide()
                else:
                    self.notice_label.show()

            if self.notice_text != '' and self.notice_timer.reached():
                self.notice_text = ''
                self.notice_timer = timer_module.AdvanceTimer(9999999999999999999999999)

            # self.label.setText(f'<font color=white size=32><b>{time.time()}<br>test</b>')

    def log_poster(self, log_str:str):
        if DEMO_MODE:
            if "DEMO" not in log_str:
                return
        record_list = log_str.split("\x1b")
        color = "white"
        for text in record_list:
            if text == '':
                continue
            ansl_code = text[text.index("[") + 1:text.index("m")]
            c = ansl_code2col(ansl_code)
            if c != "NO_COL":
                color = ansl_code2col(ansl_code, reserve=False)
            text = text[text.index("m") + 1:]
            self.logout(text, color=color)
        self.logout("<br>", color='white')
    def logout(self, text, color):
        html_str = f"<font color={color} size='5'>{text}</font>"
        self.log_history.append(html_str)
        # logger.info(html_str) # I was going to try to see if it would dead loop, but the clever loguru detected the deadlock :)


    def generate_log_html(self):
        if len(self.log_history) > 500:
            logger.debug('clean log history')
            self.log_history = self.log_history[-210:]
        html_paragraphs = self.log_history[-min(50 if not DEBUG_MODE else 200, len(self.log_history)):]
        output_html = ''
        for i in html_paragraphs: output_html+=i
        return output_html



ingame_ui_app = QApplication(sys.argv)
win_ingame_ui = IngameUI()
_style = """
QTextEdit {
    border: none;
    background-color: rgba(0, 0, 0, 150);
}
QLabel {
    border: none;
    background-color: rgba(0, 0, 0, 150);
}


"""

ingame_ui_app.setStyleSheet(_style)


def run_ingame_ui():

    win_ingame_ui.show()
    ingame_ui_app.exec_()

def append_notice(info:str, color:str='white', size:int='32', end='<br>'):
    win_ingame_ui.notice_text+=(f'<font color={color} size={size}><b>{info}</b>{end}')
def clean_notice():
    win_ingame_ui.notice_text = ''

def set_notice(info:str, color:str='white', size:int='32', end='<br>', timeout = 999, is_log = True):
    if is_log:
        logger.info(f'set_notice: {info}')
    win_ingame_ui.notice_text = (f'<font color={color} size={size}><b>{info}</b>{end}')
    win_ingame_ui.notice_timer = timer_module.AdvanceTimer(timeout).start()

#
# class IngameUIRunner(AdvanceThreading):
#     def __init__(self):
#         super().__init__()
#         self.ingame_ui_app = QApplication(sys.argv)
#         self.win_ingame_ui = IngameUI()
#     def loop(self):
#         self.win_ingame_ui.show()
#         print('run')
#         self.ingame_ui_app.exec_()
#         print('run')
#
# INGAME_UI = IngameUIRunner()

if __name__ == '__main__':
    def func1():
        while 1:
            win_ingame_ui.logout("test1", 'white')
            win_ingame_ui.logout("test1", 'white')
            win_ingame_ui.logout("<br>", 'white')
    # threading.Thread(target=func1).start()
    run_ingame_ui()

    print('running')

    # INGAME_UI.start_threading()
    while 1:
        win_ingame_ui.logout("test1", 'white')
        time.sleep(0.5)
        win_ingame_ui.logout("<br>", 'white')
        time.sleep(0.5)
