# 导入json5模块
import json5
from source.util import *

# 打开并读取data.json5文件
with open(f"{ROOT_PATH}\\assets\\LangData\\characters.json5", "r", encoding="utf-8") as f:
    data = json5.load(f)

# 定义一个函数，根据内容和语言输出英文翻译
def translate(content, language):
    # 遍历data中的每个字典
    for item in data:
        # 如果字典中有对应的语言键值，并且值等于内容
        if language in item and item[language] == content:
            # 返回字典中的英文键值
            return item["en"]
    # 如果没有找到匹配的内容，返回None
    return None

# 测试函数
print(translate("旅人", "ja")) # Traveler
print(translate("旅行者", "zhCN")) # Traveler
print(translate("Traveler", "en")) # Traveler
print(translate("旅客", "zhCN")) # None

def query(string):
    # 遍历data中的每个字典
    for item in data:
        # 遍历字典中的每个键值对
        for key, value in item.items():
            # 如果值等于字符串
            if value == string:
                # 返回True
                return True
    # 如果没有找到匹配的字符串，返回False
    return False

# 测试函数
print(query("Traveler")) # True
print(query("旅人")) # True
print(query("旅客")) # False