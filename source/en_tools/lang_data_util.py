from source.util import *

def translate_lang(dicts, content, language:str = GLOBAL_LANG):
    language = language.replace("zh_CN",'zhCN')
    language = language.replace("en_US",'en')
    # 遍历data中的每个字典
    for item in dicts:
        # 如果字典中有对应的语言键值，并且值等于内容
        if language in item and item[language] == content:
            # 返回字典中的英文键值
            return item["en"]
        if language in item and item["en"] == content:
            # 返回字典中的英文键值
            return item["en"]
    # 如果没有找到匹配的内容，返回None
    return None