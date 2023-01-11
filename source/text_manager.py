global lang
lang = 'zh_CN'

class TextTemplate():
    def __init__(self, text, cap_area) -> None:
        self.text = text
        self.cap_area = cap_area
        
    def gettext(self):
        global lang
        return self.text[lang]




start_zh_CNallenge = {
    'zh_CN': '启动',
    'en_US': 'start'
}
LeavingIn = {
    'zh_CN': '自动退出'
}
claim_rewards = {
    'zh_CN': '领取奖励'
}
use_20x2resin = {
    'zh_CN': '使用浓缩树脂'
}
use_20resin = {
    'zh_CN': '使用原粹树脂'
}
clld = {
    'zh_CN': '地脉异常'
}
conti_challenge = {
    'zh_CN': '继续挑战'
}
exit_challenge = {
    'zh_CN': '退出秘境'
}
domain_obtain = {
    'zh_CN': '获得'
}


def text(x):
    return x[lang]
