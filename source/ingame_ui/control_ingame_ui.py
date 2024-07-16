# from PyQt5.QtCore import QProcess
# ingame_app = QProcess()
#
# def show_ui():
#     ingame_app.writeData('ShowUI'.encode())
#
#
#
# def run_main_app():
#
#     main_app.writeData("Hello, main app!".encode())
#
#     # 接收主应用程序发送的数据
#     main_app.readyReadStandardOutput.connect(on_data_received)
#
#     main_app.waitForFinished()
#
# def on_data_received():
#     data = main_app.readAllStandardOutput().data().decode()
#     print("Received data from main app:", data)
