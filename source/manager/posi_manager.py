import cv2
from source.manager.util import *
ly = 96
dx = 0
dy = 0
d2x = 5
d2y = 5

# posi_dict = {
#     "coming_out_by_space": [505, 1379, 568, 1447],
#     "IN_DOMAIN": [112, 25, 137, 52],
#     "USE_20RESIN_DOBLE_CHOICES": [724, 985, 791, 1348],
#     "USE_20X2RESIN_DOBLE_CHOICES": [726, 567, 793, 934],
#     "F_BUTTON": [526, 1104, 550, 1128]
# }

class PosiTemplate(AssetBase):
    def __init__(self, name = None, posi=None, img_path=None):
        """坐标管理类

        Args:
            posi (list, optional): 可选。若有，则使用该坐标. Defaults to None.
            img_path (str, optional): 可选。若有，则使用该图片。图片应符合bbg格式. Defaults to None.
        """
        if name is None:
            super().__init__(get_name(traceback.extract_stack()[-2]))
        else:
            super().__init__(name)
        self.posi_list = []
        self.position = None
        
        if posi is None and img_path is None:
            img_path = self.get_img_path()
        self.add_posi(posi=posi, img_path=img_path)
    
    def add_posi(self, posi=None, img_path:str = None):
        """添加坐标
        
        Args:
            posi (list, optional): 可选。若有，则使用该坐标. Defaults to None.
            img_path (str, optional): 可选。若有，则使用该图片。图片应符合bbg格式. Defaults to None.
        """
        if posi != None:
            position = posi
        else:
            # self.origin_path = img_path
            image = cv2.imread(img_path)
            position = get_bbox(image, black_offset=18)
        self.posi_list.append(position)
        
        if len(self.posi_list) <= 1:
            self.position = self.posi_list[0]
        else:
            self.position = self.posi_list

class Area(PosiTemplate):
    def __init__(self, name=None):
        name = get_name(traceback.extract_stack()[-2])
        super().__init__(name)

posi_charalist_q = [[339 - ly + dy, 1591 + dx, 339 - ly + 55, 1591 + 55], [339 + dy, 1591 + dx, 339 + 55, 1591 + 55],
                    [339 + ly + dy, 1591 + dx, 339 + ly + 55, 1591 + 55],
                    [339 + 2 * ly + dy, 1591 + dx, 339 + 2 * ly + 55, 1591 + 55]]
posi_charalist_q_point = [
    [272, 1623],
    [358, 1616],
    [463, 1616],
    [560, 1616]
]
hp_charalist_posi = [[283, 1698], [379, 1698], [475, 1698], [571, 1698]]
chara_head_list_point = [[270, 1818], [366, 1818], [461, 1818], [557, 1818]]
chara_num_list_point = [[269, 1862], [366, 1862], [460, 1862], [557, 1862]]
posi_chara_list = [[218, 1779, 218 + 68, 1779 + 61], [218 + ly, 1779, 218 + ly + 68, 1779 + 61],
                   [218 + 2 * ly, 1779, 218 + 2 * ly + 68, 1779 + 61],
                   [218 + 3 * ly, 1779, 218 + 3 * ly + 68, 1779 + 61]]
# posi_chara_q=[915+d2x,1766+d2y,1015,1866]
posi_chara_q = [1788,943, 1845, 1002 ]
posi_complete_chara_q = [1763,916, 1876, 1026 ]
posi_chara_q_point = [981, 1812]
posi_chara_e = [1666,965, 1716, 1015 ]
posi_chara_smaller_e = [1671,974, 1710, 1013 ]
posi_coming_out_by_space = [1379,505, 1447, 568 ]
posi_F_button_list = [1079,350,1162, 751 ]
posi_F_button_text = [1152,505, 1503,572 ]
posi_fangdaditu = [48, 429]
posi_suoxiaoditu = [48, 653]
# posi_chara_e_point=[]
posi_arrow = [111 - 3, 156 - 3, 111 + 26 + 2, 156 + 26 + 2]
posi_domain = {
    'LLD': [832,397, 1861, 873 ],  # Ley Lind Disorder 地脉异常
    'CLLD': [940, 832],  # close lld, x,y
    'Start': [1080,484,1428, 585 ],  # 启动
    'LeavingIn': [564,870,1463, 986 ],
    'ClaimRewards': [1147,493,1418, 583 ],
    'UseResin': [537,714,1386, 811 ],
    'LeaveOrContinue': [391,908,1547, 1042 ]
}
tp_button = [1698, 1002]

# def get_posi_from_str(str1: str):
#     try:
#         return posi_dict[str1]
#     except:
#         return [0,0,1080,1920]


if __name__ == '__main__':
    a = cv2.imread("imgs\\-21387.jpg")
    p = posi_coming_out_by_space
    b = a[p[0]:p[2], p[1]:p[3]]
    cv2.imshow("123", b)
    cv2.imwrite("assets\\imgs\\common\\coming_out_by_space.jpg", b)
    cv2.waitKey(0)
