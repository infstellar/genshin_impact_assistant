import os, sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_PATH)
SOURCE_PATH = ROOT_PATH + '\\source'
ASSETS_PATH = ROOT_PATH + '\\assets'
if sys.path[0] != ROOT_PATH:
    sys.path.insert(0, ROOT_PATH)
if sys.path[1] != SOURCE_PATH:
    sys.path.insert(1, SOURCE_PATH)

CONFIG_PATH = os.path.join(ROOT_PATH,"config")
CONFIG_PATH_SETTING = os.path.join(ROOT_PATH,"config\\settings")
JSONNAME_CONFIG = "config.json"
ASSETS_IMG = "assets\\imgs\\$device$"
ASSETS_COMMON_IMG = "assets\\imgs\\$device$\\common"
