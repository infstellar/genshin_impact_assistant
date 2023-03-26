from source.util import *
def _domain_text_process(text:str):
    text = text.replace('：', ':')
    text = text.replace(' ', '')
    text = text.replace("Ⅱ", "I")
    replace_dict = {
        "惊垫":"惊蛰"
    }
    if ":" in text:
        text = text[text.index(':')+1:]
    for i in replace_dict:
        if i in text:
            text = text.replace(i, replace_dict[i])
    return text

print(_domain_text_process("惊垫ⅡV"))