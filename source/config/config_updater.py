from source.util import *
from source.config.util import *


"""
生成commission index，提供导入。
"""

commission_list = []
commission_dict = {}

with open(os.path.join(ROOT_PATH,r"source/config/config_generated.py"), "w") as f:
    f.write("\"\"\"This file is generated automatically. Do not manually modify it.\"\"\"\n")
    f.write("class GeneratedConfig:\n")
    for jsonname in CONFIG_FILE_NAMES:
        j = load_json(json_name=f"{jsonname}.json")
        for k in j:
            value = j[k]
            if isinstance(j[k], str):
                value=f"\'{value}\'"
            f.write(f"   {jsonname}___{k} = {value}\n")
            print(f"set {jsonname}___{k} to {j[k]}")