from source.path_lib import *
from source.config.cvars import *
import json
from collections import OrderedDict

def load_json(json_name='General.json', folder_path='config\\settings', auto_create = False) -> dict:
    all_path = os.path.join(ROOT_PATH, folder_path, json_name)
    try:
        return json.load(open(all_path, 'r', encoding='utf-8'), object_pairs_hook=OrderedDict)
    except:
        if not auto_create:
            raise FileNotFoundError(all_path)
        else:
            json.dump({}, open(all_path, 'w', encoding='utf-8'))
            return json.load(open(all_path, 'r', encoding='utf-8'))

def save_json(x, json_name='config.json', default_path='config\\settings', sort_keys=True):
    if not os.path.exists(default_path):
        print(f"CANNOT FIND PATH: {default_path}")
    json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)
