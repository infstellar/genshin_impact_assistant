from source.util import *
from source.en_tools.lang_data_util import translate_lang
import json5
with open(f"{ROOT_PATH}\\assets\\LangData\\domains.json5", "r", encoding="utf-8") as f:
    DOMAINS = json5.load(f)
ZH2EN = load_json('en_US.json',r"assets/POI_JSON_API/LANGUAGE")

def zh2en(x):
    if x in ZH2EN:
        return ZH2EN[x]
    else:
        r = translate_lang(DOMAINS, x, language='zh_CN')
        if r != None:
            return r
        return x

# print(zh2en('沉眠之庭'))
    
