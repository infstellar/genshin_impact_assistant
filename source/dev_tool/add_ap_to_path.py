from source.util import *

def get_path_file(path_file_name:str):
    return load_json(path_file_name+".json","assets\\TeyvatMovePath")

import os
filePath = fr'{ROOT_PATH}/assets/TeyvatMovePath'
files = os.listdir(filePath)

def add_ap_to_path(name):
    j = get_path_file(f'{name}')
    j['adsorptive_position'] = []
    if 'additional_info' in j:
        if 'pickup_points' in j['additional_info']:
            print(name)
            for p in j['additional_info']['pickup_points']:
                j['adsorptive_position'].append(j['break_position'][p])
            save_json(j, f'{name}'+".json","assets\\TeyvatMovePath")

for i in files:
    if i == '.git':continue
    if i == '.gitignore':continue
    if i == 'LICENSE':continue
    if i == 'TLPS':continue
    add_ap_to_path(i[:i.index('.')])

