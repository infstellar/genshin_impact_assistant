from source.map.data.teleporter_en_US import DICT_TELEPORTER
from source.util import *

list1 = []
for i in DICT_TELEPORTER:
    if DICT_TELEPORTER[i].tp=='Domain':
        list1.append(DICT_TELEPORTER[i].name)

save_json(list1, json_name='Domain_Names_en_US.json', default_path=fr"{ROOT_PATH}/assets/domain_names")