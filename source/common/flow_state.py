from source.util import t2t

current_statement = {
    "AutoCombat":0,
    "AutoDomain":0,
    "AutoMove":0,
    "AutoCollector":0
}

"""

STATE:

INIT_STATENAME=00
BEFORE_STATENAME=01
IN_STATENAME=02
AFTER_STATENAME=03
END_STATENAME=04

"""

'''auto domain flow'''

END = 0

INIT_MOVETO_CHALLENGE = 1000
BEFORE_MOVETO_CHALLENGE = 1001
IN_MOVETO_CHALLENGE = 1002
AFTER_MOVETO_CHALLENGE = 1003

INIT_CHALLENGE = 1100
IN_CHALLENGE = 1102
AFTER_CHALLENGE = 1103
END_CHALLENGE = 1104

INIT_GETTING_REAWARD = 1200
IN_GETTING_REAWARD = 1202
AFTER_GETTING_REAWARD = 1203
END_GETTING_REAWARD = 1204

INIT_FINGING_TREE = 1300
IN_FINGING_TREE = 1302
AFTER_FINGING_TREE = 1303
END_FINGING_TREE = 1304

INIT_MOVETO_TREE = 1400
IN_MOVETO_TREE = 1402
AFTER_MOVETO_TREE = 1403
END_MOVETO_TREE = 1404

INIT_ATTAIN_REAWARD = 1500
BEFORE_ATTAIN_REAWARD = 1501
IN_ATTAIN_REAWARD = 1502
END_ATTAIN_REAWARD = 1504

END_DOMAIN = -1900

'''teyvat move flow'''

INIT_TEYVAT_TELEPORT = 2100
BEFORE_TEYVAT_TELEPORT = 2101
IN_TEYVAT_TELEPORT = 2102
AFTER_TEYVAT_TELEPORT = 2103
END_TEYVAT_TELEPORT = 2104

INIT_TEYVAT_MOVE = 2200
BEFORE_TEYVAT_MOVE = 2201
IN_TEYVAT_MOVE = 2202
AFTER_TEYVAT_MOVE = 2203
END_TEYVAT_MOVE = 2204

END_TEYVAT_MOVE_PASS = -2300
END_TEYVAT_MOVE_STUCK = -2301

'''collector flow'''

INIT_MOVETO_COLLECTOR = 3100
BEFORE_MOVETO_COLLECTOR = 3101
IN_MOVETO_COLLECTOR = 3102
AFTER_MOVETO_COLLECTOR = 3103
END_MOVETO_COLLECTOR = 3104

INIT_PICKUP_COLLECTOR = 3200
BEFORE_PICKUP_COLLECTOR = 3201
IN_PICKUP_COLLECTOR = 3202
AFTER_PICKUP_COLLECTOR = 3203
END_PICKUP_COLLECTOR = 3204

END_COLLECTOR = 3900

COLLECTION_PATH_RECORD = 4100
COLLECTION_PATH_END = -4900

def get_statement_code_name(code):
    name_prefixion = ""
    name_text = ""
    
    if code == 0:
        return t2t("空闲")
    
    if code%5 == 0:
        name_prefixion = t2t("正在初始化")
    elif code%5 == 1:
        name_prefixion = t2t("正在准备")
    elif code%5 == 2:
        name_prefixion = t2t("正在进行")
    elif code%5 == 3:
        name_prefixion = t2t("准备结束")
    elif code%5 == 4:
        name_prefixion = t2t("结束")
    
    if code//100 == 10:
        name_text = t2t("移动到挑战位置")
    elif code//100 == 11:
        name_text = t2t("挑战秘境中")
    elif code//100 == 12:
        name_text = t2t("准备领取奖励")
    elif code//100 == 13:
        name_text = t2t("正在寻找石化古树位置")
    elif code//100 == 14:
        name_text = t2t("移动到石化古树位置")
    elif code//100 == 15:
        name_text = t2t("领取奖励")
    elif code//100 == 19:
        name_text = t2t("结束秘境")
    elif code//100 == 21:
        name_text = t2t("在地图上传送")
    elif code//100 == 22:
        name_text = t2t("移动到目标坐标位置")
    elif code//100 == 31:
        name_text = t2t("移动到采集物位置")
    elif code//100 == 32:
        name_text = t2t("拾取采集物")
    elif code//100 == 32:
        name_text = t2t("结束自动采集")
        
    return f"{name_prefixion} : {name_text}"

if __name__ == '__main__':
    a = get_statement_code_name(1404)
    print(a)