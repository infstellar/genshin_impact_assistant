from source.util import *
import json5

with open(f"{ROOT_PATH}\\assets\\LangData\\characters.json5", "r", encoding="utf-8") as f:
    characters = json5.load(f)
    
for item in characters:
    # 遍历字典中的每个键值对
    for key, value in item.items():
        # 如果值等于字符串
        if value == "丽莎·敏兹":
            item["zhCN"] = "丽莎"
        if value == "Lisa Minci":
            # 返回True
            item["en"] = "Lisa"
    
save_json(characters, "characters.json5", f"{ROOT_PATH}\\assets\\LangData")