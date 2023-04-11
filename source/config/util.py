from source.path_lib import *
import json
CONFIGNAME_CONFIG = "General"
CONFIGNAME_AIM = "Aim"
CONFIGNAME_COLLECTOR = "Collector"
CONFIGNAME_COMBAT = "Combat"
CONFIGNAME_DOMAIN = "Domain"
CONFIGNAME_PICKUP = "Pickup"
CONFIGNAME_KEYMAP = "Keymap"
CONFIG_FILE_NAMES = [CONFIGNAME_CONFIG, CONFIGNAME_COLLECTOR, CONFIGNAME_COMBAT,
                         CONFIGNAME_DOMAIN, CONFIGNAME_KEYMAP]

def load_json(json_name='config.json', default_path='config\\settings') -> dict:
    all_path = os.path.join(ROOT_PATH, default_path, json_name)
    return json.load(open(all_path, 'r', encoding='utf-8'))

def save_json(x, json_name='config.json', default_path='config\\settings', sort_keys=True):
    if not os.path.exists(default_path):
        print(f"CANNOT FIND PATH: {default_path}")
    json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)
