import os,sys
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_path = root_path + '\\source'
assets_path = root_path + '\\assets'
if sys.path[0] != root_path:
    sys.path.insert(0, root_path)
if sys.path[1] != source_path:
    sys.path.insert(1, source_path)
    
CONFIG_SETTING_PATH = os.path.join(root_path,"config\\settings")
