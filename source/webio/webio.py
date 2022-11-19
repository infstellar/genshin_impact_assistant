from source import webio
from source.webio.pages import *


def main():
    webio.manager.reg_page('Main', MainPage())
    webio.manager.reg_page('Setting', SettingPage())

    webio.manager.load_page('Setting')


if __name__ == '__main__':
    platform.tornado.start_server(main, auto_open_webbrowser=True, debug=True)
