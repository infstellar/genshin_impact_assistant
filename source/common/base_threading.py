import threading
import time
from source.funclib.err_code_lib import ERR_NONE
from source.util import *
from source.exceptions import *
from source.cvars import THREAD_PAUSE_FORCE_TERMINATE, THREAD_PAUSE_SET_FLAG_ONLY


class ThreadingStopException(Exception):
    pass


class BaseThreading(threading.Thread):
    """
    基本线程类。
    """

    pause_method = THREAD_PAUSE_SET_FLAG_ONLY

    def __init__(self, thread_name=None):
        super().__init__()
        self._init_succ_flag = False  # 在初始化很慢的线程中使用
        self.pause_threading_flag = False  # 暂停线程标记
        self.stop_threading_flag = False  # 线程停止标记
        self.working_flag = False  # 废物
        self.while_sleep = 0.2  # 每次循环间隔
        self.last_err_code = ERR_NONE  # 错误码
        self.stop_func_list = []  # 停止函数列表。check_up_stop_func时循环执行里面的函数，如果有返回值为true的函数即停止。
        self.sub_threading_list = []  # 子线程列表
        if thread_name != None:
            self.setName(thread_name)

    def set_pause_method(self, mode=THREAD_PAUSE_SET_FLAG_ONLY):
        self.pause_method = mode

    def pause_threading(self):
        """
        暂停线程执行。线程会进行等待。
        
        如果不是想要线程彻底结束，而是暂时停止，使用此方法。
        
        需要在内部使用checkup_stop_func退出到run函数中，才能有效停止。
        """
        if self.pause_threading_flag != True:
            logger.debug(f"{self.name} pause threading")
            for thread_obj in self.sub_threading_list:
                logger.debug(f"{self.name} pause {thread_obj.name}")
                thread_obj.pause_threading()
            self.pause_threading_flag = True


    def continue_threading(self, ignore_warning=False):
        """
        继续线程执行。
        """
        if self.pause_threading_flag != False:
            logger.debug(f"{self.name} continue threading")
            if not self.is_alive():
                if not ignore_warning: logger.warning("Thread has not start yet, but continued.")
            self.pause_threading_flag = False

    def start_threading(self):
        self.start()
        self.continue_threading()

    def stop_threading(self):
        """
        终止线程。
        
        需要在内部使用checkup_stop_threading或checkup_stop_func（推荐）退出到run函数中，才能有效停止。
        """
        logger.debug(f"{self.name} stopping.")
        self.stop_threading_flag = True
        self.pause_threading_flag = True
        self._clean_sub_threading()

    def __force_terminate(self):
        logger.debug(f'Thread {self.name} terminated by exception.')
        raise ThreadTerminated(t2t('If you see this error, it\'s just because the thread was terminated normally, not a fatal error.'))

    def checkup_stop_func(self):
        """
        检查是否要退出。会检查暂停flag和停止flag。
        使用方法：
        在函数中使用：
            if self.checkup_stop_func(): return 适当的返回值
        在循环中：
            if self.checkup_stop_func(): break

        Returns:
            _type_: _description_
        """
        pt = time.time()

        def force_terminate_check():
            if (self.stop_threading_flag
                    or
                    ((self.pause_method == THREAD_PAUSE_FORCE_TERMINATE) and self.pause_threading_flag)):
                self.__force_terminate()


        def output_log(t):
            if t < 0.05:
                pass
            elif t < 0.1:
                logger.trace(f"checkup_stop_func spend to long: {t} {self.name}")
            else:
                logger.warning(f"checkup_stop_func spend to long: {t} {self.name}")

        if self.pause_threading_flag or self.stop_threading_flag:
            output_log(time.time() - pt)
            force_terminate_check()
            return True
        for i in self.stop_func_list:
            if i():
                output_log(time.time() - pt)
                force_terminate_check()
                return True
        output_log(time.time() - pt)
        return False

    def checkup_stop_threading(self):
        """
        检查是否要结束线程。只检查停止flag。

        Returns:
            _type_: _description_
        """
        if self.stop_threading_flag:
            return True

    def get_last_err_code(self):
        """获得最后的错误代码。

        Returns:
            _type_: _description_
        """
        return self.last_err_code

    def get_and_reset_err_code(self):
        """获得并重置错误代码。

        Returns:
            _type_: _description_
        """
        erc = self.last_err_code
        self.reset_err_code()
        return erc

    def reset_err_code(self):
        """重置错误代码。
        """
        self.last_err_code = ERR_NONE

    def _add_sub_threading(self, threading_obj, start=True):
        """添加子线程。

        Args:
            threading_obj (_type_): 子线程对象
            start (bool, optional): 是否开启子线程. Defaults to True.
        """
        threading_obj.setDaemon(True)
        threading_obj.add_stop_func(self.checkup_stop_func)
        threading_obj.pause_threading()
        if start:
            threading_obj.start()
        self.sub_threading_list.append(threading_obj)
        logger.debug(f"sub threading {threading_obj.name} has been add by {self.name}.")

    def _clean_sub_threading(self):
        """移除所有子线程。
        """
        for thread_obj in self.sub_threading_list:
            logger.debug(f"{self.name} stop {thread_obj.name}")
            thread_obj.stop_threading()
        self.sub_threading_list = []

    def loop(self):
        """
        在这里写要循环执行的代码。
        """
        pass

    _thread_paused_flag = False
    def is_thread_paused(self):
        return self._thread_paused_flag

    def run(self):
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                logger.debug(f"{self.name} stop.")
                return

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                self._thread_paused_flag=True
                time.sleep(1)
                continue
            else:
                self._thread_paused_flag = False

            if not self.working_flag:
                self.working_flag = True

            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue

            self.loop()

    def get_working_statement(self):
        return not self.pause_threading_flag

    def add_stop_func(self, x):
        self.stop_func_list.append(x)


class AdvanceThreading(BaseThreading):
    """升级版线程。推荐使用这个。

    Args:
        BaseThreading (_type_): _description_
    """

    def __init__(self, thread_name=None):
        super().__init__(thread_name)

    def blocking_startup(self, threading_obj: BaseThreading):
        """阻塞启动模式。
        使用该模式启动线程时，会阻塞当前线程，循环执行threading_obj的loop函数。
        此时，threading_obj不会作为线程启动。使用此方法可以避免启动过多线程。

        Args:
            threading_obj (BaseThreading): _description_

        Returns:
            _type_: _description_
        """
        if threading_obj.is_alive():
            threading_obj.stop_threading()
        threading_obj.continue_threading(ignore_warning=True)
        while 1:
            time.sleep(threading_obj.while_sleep)
            threading_obj.loop()
            if threading_obj.pause_threading_flag:
                break
            if self.checkup_stop_func():
                break
        return threading_obj.get_last_err_code()


class FunctionThreading(AdvanceThreading):
    """目前没啥用

    Args:
        AdvanceThreading (_type_): _description_
    """

    def __init__(self, target, thread_name=None):
        super().__init__(thread_name)
        self.target = target
        self.while_sleep = 0

    def loop(self):
        self.target()


class ThreadBlockingRequest():
    """线程阻塞请求
    """

    def __init__(self) -> None:
        self.blocking_request_flag = False
        self.reply_request_flag = False

    def send_request(self, message=''):
        logger.debug(f"ThreadBlockingRequest sent request: {message}")
        self.blocking_request_flag = True

    def reply_request(self):
        if self.reply_request_flag != True:
            logger.debug(f"ThreadBlockingRequest reply request.")
            self.reply_request_flag = True

    def waiting_until_reply(self, stop_func=lambda: False, timeout=10):
        t = time.time()
        while 1:
            time.sleep(0.1)
            if stop_func():
                return False
            if time.time() - t >= 10:
                return False
            if self.reply_request_flag:
                return True

    def is_blocking(self):
        return self.blocking_request_flag

    def recovery_request(self):
        logger.debug(f"ThreadBlockingRequest recovery request.")
        self.blocking_request_flag = False
        self.reply_request_flag = False
