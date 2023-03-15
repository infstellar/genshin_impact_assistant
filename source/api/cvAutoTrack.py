# from source.util import *
# from common import timer_module
# from source.common.base_threading import BaseThreading
# from assets.AutoTrackDLLAPI.AutoTrackAPI import AutoTracker
# from source.ui.ui import ui_control
# import source.ui.page as UIPage

# def del_log():
#     logger.debug(t2t("cleaning cvautotrack files"))
#     for root, dirs, files in os.walk(os.path.join(ROOT_PATH)):
#         for f in files:
#             if f == "autoTrack.log":
#                 os.remove(os.path.join(ROOT_PATH, "autoTrack.log"))
#                 logger.debug(t2t("autoTrack.log 1 cleaned"))
#     for root, dirs, files in os.walk(os.path.join(ROOT_PATH, "source")):
#         for f in files:
#             if f == "autoTrack.log":
#                 os.remove(os.path.join(ROOT_PATH, "source", "autoTrack.log"))
#                 logger.debug(t2t("autoTrack.log 2 cleaned"))
#     for root, dirs, files in os.walk(os.path.join(ROOT_PATH, "source", "../webio")):
#         for f in files:
#             if f == "autoTrack.log":
#                 os.remove(os.path.join(ROOT_PATH, "source", "../webio", "autoTrack.log"))
#                 logger.debug(t2t("autoTrack.log 3 cleaned"))
# del_log()



# class AutoTrackerLoop(BaseThreading):
#     def __init__(self):
#         super().__init__()
#         self.setName("AutoTrackerLoop")
#         self.loaded_flag = False
#         self.position = [0,0]
#         self.last_position = self.position
#         self.in_excessive_error = False
#         self.start_sleep_timer = timer_module.Timer(diff_start_time=61)
#         self.history_posi = []
#         self.history_timer = timer_module.Timer()
#         self.load_dll()
    
#     def load_dll(self):
#         self.cvAutoTracker = AutoTracker() # os.path.join(root_path, 'source\\cvAutoTrack_7.2.3\\CVAUTOTRACK.dll')
#         self.cvAutoTracker.init()
#         logger.info(t2t("cvAutoTrack DLL has been loaded."))
#         logger.debug('1) err' + str(self.cvAutoTracker.get_last_error()))
#         r = self.cvAutoTracker.disable_log()
#         logger.debug(f"disable log {r}")
#         time.sleep(2)
#         self.position = self.cvAutoTracker.get_position()
#         self.last_position = self.position
#         self.rotation = self.cvAutoTracker.get_rotation()
#         self.in_excessive_error = False
#         self.start_sleep_timer = timer_module.Timer(diff_start_time=61)
#         self.loaded_flag = True
#         self.warning_times = 0

#     def while_until_no_excessive_error(self, stop_func):
#         logger.info(t2t("等待cvautotrack获取坐标"))
#         self.start_sleep_timer.reset() # type: ignore
#         while self.is_in_excessive_error(): # type: ignore
#             if stop_func():
#                 return 0
#             time.sleep(1)
    
#     def run(self) -> None:
#         ct = 0
#         time.sleep(0.1)
#         while 1:
#             if not self.loaded_flag:
#                 time.sleep(2)
#                 continue
            
#             time.sleep(self.while_sleep)
#             if self.stop_threading_flag:
#                 return
#             if self.pause_threading_flag:
#                 if self.working_flag:
#                     self.working_flag = False
#                 time.sleep(1)
#                 continue

#             if not self.working_flag:
#                 self.working_flag = True

#             if self.checkup_stop_func():
#                 self.pause_threading_flag = True
#                 continue
            
#             if self.start_sleep_timer.get_diff_time() >= 60:
#                 if self.start_sleep_timer.get_diff_time() <= 62:
#                     logger.debug("cvAutoTrackerLoop switch to sleep mode.")
#                 time.sleep(0.8)
#                 continue
            
            
            
#             self.rotation = self.cvAutoTracker.get_rotation()
#             self.position = self.cvAutoTracker.get_position()
            
            
#             if not self.position[0]:
#                 if scene_lib.get_current_pagename() == 'main':
#                     if self.warning_times >= 2:
#                         logger.warning("获取坐标失败")
#                     self.warning_times += 1
#                 else:
#                     self.warning_times = 0 
#                     time.sleep(0.5)
#                 self.position = (False, 0, 0)
#                 self.in_excessive_error = True
#                 time.sleep(0.5)
#                 continue
#             if ct >= 20:
#                 self.last_position = self.position
#                 self.in_excessive_error = False
#                 logger.debug("位置已重置")
#                 ct = 0
#             if euclidean_distance(self.position[1:], self.last_position[1:]) >= 50:
#                 # print("误差过大")
#                 self.in_excessive_error = True
#                 ct += 1
#             else:
#                 self.last_position = self.position
#                 self.in_excessive_error = False
#                 ct = 0
#             if self.history_timer.get_diff_time()>=1:
#                 self.history_timer.reset()
#                 if len(self.history_posi)<30:
#                     self.history_posi.append(self.position)
#                 else:
#                     del(self.history_posi[0])
#                     self.history_posi.append(self.position)
#             # print(self.last_position)

#     def get_position(self):
#         if not self.loaded_flag:
#             self.load_dll()
#             time.sleep(3)
#         self.start_sleep_timer.reset()
#         return self.position[1:]

#     def get_rotation(self):
#         if not self.loaded_flag:
#             self.load_dll()
#             time.sleep(3)
#         self.start_sleep_timer.reset()
#         return self.cvAutoTracker.get_rotation()[1]

#     def is_in_excessive_error(self):
#         if not self.loaded_flag:
#             self.load_dll()
#             time.sleep(3)
#         self.start_sleep_timer.reset()
#         return self.in_excessive_error

# # 以下是对被封装的类的简单演示。
# # 使用命令行 `python ./main.py` 直接运行本文件即可。
# if __name__ == '__main__':
#     cal=AutoTrackerLoop()
#     a = cal.get_position()
#     print()
#     # # 等待五秒钟以便切换到原神窗口：
#     # # sleep(5)
#     #
#     # # print(cvAutoTracker.SetWorldCenter(793.9, -1237.8))
#     #
#     # # 加载同一目录下的DLL：
#     # # tracker = AutoTracker('source\\CVAUTOTRACK.dll')
#     #
#     # # 初始化并打印错误：
#     # # tracker.init()
#     # # print('1) err', tracker.get_last_error(), '\n')
#     #
#     # # 获取当前人物所在位置以及角度（箭头朝向）并打印错误：
#     # print(cvAutoTrackerLoop.get_position())
#     # print('2) err', cvAutoTrackerLoop.get_position(), '\n')
#     #
#     # # 获取UID并打印错误：
#     # # print(cvAutoTrackerLoop.get_uid())
#     # # print('3) err', cvAutoTrackerLoop.get_last_error(), '\n')
#     #
#     # # print(cvAutoTrackerLoop.get_direction())
#     # # print('4) err', cvAutoTrackerLoop.get_last_error(), '\n')
#     #
#     # print(cvAutoTrackerLoop.get_rotation())
#     # # print('5) err', cvAutoTrackerLoop.get_last_error(), '\n')
#     #
#     # while 1:
#     #     # print(cvAutoTracker.get_rotation())
#     #
#     #     # ret = cvAutoTracker.get_position()
#     #     # posi = cvAutoTracker.translate_posi(ret[1],ret[2])
#     #     print(cvAutoTrackerLoop.get_position())
#     #     time.sleep(0.2)
#     #
#     # # 卸载相关内存：（这一步不是必须的，但还是建议手动调用）
#     # cvAutoTracker.uninit()
#     pass

# # 0 263.25 0 -> 793.9 -1237.8

# # 10 263.8 10 -> 773 -1258

# # -10 -10 -> 811 -1217

# # 740 -1012
# # 684 -1518
# # 3.3 3.4
