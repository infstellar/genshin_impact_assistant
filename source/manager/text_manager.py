from source.util import *

class TextTemplate():
    def __init__(self, text:dict, cap_area=None) -> None:
        if cap_area == None:
            cap_area = [0,0,1920,1080]
        elif isinstance(cap_area, str):
            if IS_DEVICE_PC:
                path = os.path.join(ROOT_PATH, cap_area).replace("$device$", "Windows")
            else:
                path = os.path.join(ROOT_PATH, cap_area).replace("$device$", "Windows")
            cap_area = get_bbox(cv2.imread(os.path.join(ROOT_PATH, path)))
        self.origin_text = text
        self.cap_area = cap_area
        self.text = self.origin_text[GLOBAL_LANG]
        
    def gettext(self):
        return self.origin_text[GLOBAL_LANG]




# start_challenge = {
#     'zh_CN': '启动',
#     'en_US': 'start'
# }
# LeavingIn = {
#     'zh_CN': '自动退出'
# }
# claim_rewards = {
#     'zh_CN': '领取奖励'
# }
# use_20x2resin = {
#     'zh_CN': '使用浓缩树脂'
# }
# use_20resin = {
#     'zh_CN': '使用原粹树脂'
# }
# clld = {
#     'zh_CN': '地脉异常'
# }
# conti_challenge = {
#     'zh_CN': '继续挑战'
# }
# exit_challenge = {
#     'zh_CN': '退出秘境'
# }
# domain_obtain = {
#     'zh_CN': '获得'
# }


# def text(x):
#     return x[global_lang]

# if __name__ == '__main__':  
#     print(text(conti_challenge))