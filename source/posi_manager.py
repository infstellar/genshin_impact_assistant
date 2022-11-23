import cv2

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
chara_head_list_point = [[270, 1789], [366, 1792], [461, 1793], [557, 1797]]
chara_num_list_point = [[269, 1862], [366, 1862], [460, 1862], [557, 1862]]
posi_chara_list = [[218, 1779, 218 + 68, 1779 + 61], [218 + ly, 1779, 218 + ly + 68, 1779 + 61],
                   [218 + 2 * ly, 1779, 218 + 2 * ly + 68, 1779 + 61],
                   [218 + 3 * ly, 1779, 218 + 3 * ly + 68, 1779 + 61]]
# posi_chara_q=[915+d2x,1766+d2y,1015,1866]
posi_chara_q = [943, 1788, 1002, 1845]
posi_chara_q_point = [981, 1812]
posi_chara_e = [965, 1666, 1015, 1716]
posi_chara_smaller_e = [974, 1671, 1013, 1710]
posi_coming_out_by_space = [505, 1379, 568, 1447]
posi_F_button_list = [350, 1079, 751, 1162]
posi_F_button_text = [505, 1152, 572, 1503]
posi_fangdaditu = [48, 429]
posi_suoxiaoditu = [48, 653]
# posi_chara_e_point=[]
posi_arrow = [111 - 3, 156 - 3, 111 + 26 + 2, 156 + 26 + 2]
posi_domain = {
    'LLD': [397, 832, 873, 1861],  # Ley Lind Disorder 地脉异常
    'CLLD': [940, 832],  # close lld, x,y
    'Start': [484, 1080, 585, 1428],  # 启动
    'LeavingIn': [870, 564, 986, 1463],
    'ClaimRewards': [493, 1147, 583, 1418],
    'UseResin': [714, 537, 811, 1386],
    'LeaveOrContinue': [908, 391, 1042, 1547]
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
    cv2.imwrite("assests\imgs\common\coming_out_by_space.jpg", b)
    cv2.waitKey(0)
