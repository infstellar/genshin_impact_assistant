from loguru import logger
import types
import os
import json
import time
from source.path_lib import *

def load_json(json_name='General.json', default_path='config\\settings') -> dict:
    all_path = os.path.join(ROOT_PATH, default_path, json_name)
    return json.load(open(all_path, 'r', encoding='utf-8'))

def get_logger_format_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_logger_format_date():
    return time.strftime('%Y-%m-%d', time.localtime())

jpath = fr"{ROOT_PATH}/config/settings/General.json"
if os.path.exists(jpath):
    j = json.load(open(jpath, 'r', encoding='utf-8'))
    DEBUG_MODE = j["DEBUG"]
else:
    DEBUG_MODE = False
warned_dict={}
def warning_once(self, message):
    is_warned = warned_dict.setdefault(message, False)
    if not is_warned:
        self.warning(message)
        warned_dict[message]=True

def demo(self, message):
    self.info(f"DEMO: {message}")

import datetime

def delete_files(path, days):
    now = datetime.datetime.now()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - modified_time).days > days:
                if DEBUG_MODE:
                    print(f"Log File Delete: Deleting file {file_path} Last modified {modified_time} Days since modified {(now - modified_time).days} Days to delete {days}")
                os.remove(file_path)

delete_files(f"{ROOT_PATH}/Logs", 15)


# configure loguru
logger.remove(handler_id=None)
logger.warning_once = types.MethodType(warning_once, logger)
logger.demo = types.MethodType(demo, logger)
logger.add(os.path.join(ROOT_PATH, os.path.join(ROOT_PATH, 'Logs', "{time:YYYY-MM-DD}/{time:YYYY-MM-DD}.log")), level="TRACE", backtrace=True)
if DEBUG_MODE:
    logger.add(sys.stdout, level="TRACE", backtrace=True)
else:
    logger.add(sys.stdout, level="INFO", backtrace=True)

def hr(title, level=3):
    title = str(title).upper()
    if level == 1:
        logger.info('=' * 20 + ' ' + title + ' ' + '=' * 20)
    if level == 2:
        logger.info('-' * 20 + ' ' + title + ' ' + '-' * 20)
    if level == 3:
        logger.info('<' * 3 + ' ' + title + ' ' + '>' * 3)
    if level == 0:
        middle = '|' + ' ' * 20 + title + ' ' * 20 + '|'
        border = '+' + '-' * (len(middle) - 2) + '+'
        logger.info(border)
        logger.info(middle)
        logger.info(border)


def attr(name, text):
    logger.info('[%s] %s' % (str(name), str(text)))


def attr_align(name, text, front='', align=22):
    name = str(name).rjust(align)
    if front:
        name = front + name[len(front):]
    logger.info('%s: %s' % (name, str(text)))


logger.hr = hr
logger.attr = attr
logger.attr_align = attr_align

def add_logger_to_GUI(cb_func):
    logger.add(cb_func, level="INFO", backtrace=True, colorize=True)

if __name__ == "__main__":
    logger.warning_once("123")
    logger.warning_once("123")
    logger.warning_once("123")