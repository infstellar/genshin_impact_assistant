import json
import os
import shutil
import sys
import time  # 8药删了，qq了
import math
import numpy as np
import gettext
import cv2
import win32gui, win32process, psutil
import ctypes, pickle

from utils import *
from constants import *
from logger import logger


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_path = root_path + '\\source'
assets_path = root_path + '\\assets'
if sys.path[0] != root_path:
    sys.path.insert(0, root_path)
if sys.path[1] != source_path:
    sys.path.insert(1, source_path)
    

try:
    config_json = load_json("config.json")
    DEBUG_MODE = config_json["DEBUG"] if "DEBUG" in config_json else False
    GLOBAL_LANG = config_json["lang"]
except:
    logger.error("config文件导入失败，可能由于初次安装。跳过导入。 ERROR_IMPORT_CONFIG_001")
    DEBUG_MODE = False
    GLOBAL_LANG = "$locale$"

try:
    INTERACTION_MODE = load_json("config.json", CONFIG_PATH_SETTING)["interaction_mode"]
    if INTERACTION_MODE not in [INTERACTION_EMULATOR, INTERACTION_DESKTOP_BACKGROUND, INTERACTION_DESKTOP]:
        logger.warning("UNKNOWN INTEACTION MODE. SET TO \'Desktop\' Default.")
        INTERACTION_MODE = INTERACTION_DESKTOP
except:
    logger.error("config文件导入失败，可能由于初次安装。跳过导入。 ERROR_IMPORT_CONFIG_002")
    INTERACTION_MODE = INTERACTION_DESKTOP
IS_DEVICE_PC = (INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND)or(INTERACTION_MODE == INTERACTION_DESKTOP)