from typing import Union
from source.util import *

def add_to_blacklist(key:str, id: Union[int,list]) -> None:
    blacklist = load_json(json_name="collection_blacklist.json", default_path="config\\auto_collector")
    if isinstance(id, int):
        id = [id]
    for i in id:
        blacklist[key].append(int(i))
    save_json(blacklist, json_name="collection_blacklist.json", default_path="config\\auto_collector")

def add_to_collected(key:str, id: Union[int,list]) -> None:
    if isinstance(id, int):
        id = [id]
    collectedlist = load_json(json_name="collected.json", default_path="config\\auto_collector")
    for i in id:
        collectedlist[key].append(i)
    save_json(collectedlist, json_name="collected.json", default_path="config\\auto_collector")    
global REFRESH_TIME_JSON
REFRESH_TIME_JSON = None
def is_col_refreshed(col_id, col_time):
    col_time = col_time[:col_time.index('.')]
    time_stamp = time.mktime(time.strptime(col_time, "%Y-%m-%d %H:%M:%S"))
    now_stamp = time.time()
    global REFRESH_TIME_JSON
    if REFRESH_TIME_JSON is None:
        REFRESH_TIME_JSON = load_json("REFRESHTIME_INDEX.json", "assets\\POI_JSON_API")
    try:
        t = REFRESH_TIME_JSON[str(col_id)]/1000
    except KeyError as e:
        t = 72*3600
    # logger.trace(t)
    if now_stamp - time_stamp > t:
        return True
    else:
        return False
def generate_collected_from_log(regenerate = True):
    loglist = load_json("collection_log.json", "config\\auto_collector")
    if regenerate:
        collected_list = {}
    else:
        collected_list = load_json("collected.json", "config\\auto_collector")
    for i in loglist:
        key_name = i
        collected_list.setdefault(key_name, [])
        for ii in loglist[i]:
            col_id = ii["id"]
            col_time = ii["time"]
            if not is_col_refreshed(col_id, col_time):
                collected_list[key_name].append(col_id)
                # print(col_id)
    save_json(collected_list, "collected.json", "config\\auto_collector")

def generate_col_succ_rate_from_log():
    loglist = load_json("collection_log.json", "config\\auto_collector")
    dict1 = {}
    for i in loglist:
        for ii in loglist[i]:
            col_id = ii["id"]
            dict1.setdefault(col_id, {
                "total_times":0,
                "succ_times":0,
                "succ_rate":0.0
            })
            col_time = ii["picked item"]
            dict1[col_id]["total_times"]+=1
            if col_time != ["None"]:
                dict1[col_id]["succ_times"]+=1
    for i in dict1:
        dict1[i]["succ_rate"]=round(dict1[i]["succ_times"]/dict1[i]["total_times"],2)
    save_json(dict1, "collection_id_details.json", "config\\auto_collector")
    
def generate_masked_col_from_log(regenerate = True):
    min_times = load_json("auto_collector.json")["minimum_times_mask_col_id"]
    loglist = load_json("collection_log.json", "config\\auto_collector")
    if regenerate:
        bla_list = {}
    else:
        bla_list = load_json("collection_blacklist.json", "config\\auto_collector")
    for i in loglist:
        key_name = i
        bla_list.setdefault(key_name, [])
        fail_times = {}
        for ii in loglist[i]:
            col_id = ii["id"]
            col_time = ii["picked item"]
            if col_time == ["None"]:
                fail_times[str(col_id)] = fail_times.setdefault(str(col_id), 0) + 1
        for ii in fail_times:
            if int(fail_times[str(ii)]) >= min_times:
                bla_list[key_name].append(int(ii))
    save_json(bla_list, "collection_blacklist.json", "config\\auto_collector")

def col_succ_times_from_log(key_name, day=1):
    loglist = load_json("collection_log.json", "config\\auto_collector")
    total_n = 0
    succ_n = 0
    t = day*3600*24
    for i in loglist[key_name]:
        col_time = i["time"]
        col_time = col_time[:col_time.index('.')]
        time_stamp = time.mktime(time.strptime(col_time, "%Y-%m-%d %H:%M:%S"))
        now_stamp = time.time()
        if now_stamp - time_stamp <= t:
            total_n+=1
            if i["picked item"] != ["None"]:
                succ_n+=1
    fail_n = total_n - succ_n
    if total_n == 0:
        succ_rate = 1
    else:
        succ_rate = succ_n/total_n
    return round(succ_rate*100, 1), total_n, succ_n, fail_n


AREA_MD = [5,6]
AREA_LY = [1,2,3]
AREA_DQ = [11,12,13,14]
AREA_DQ_CORE = [11,12,13]
AREA_DQ_HG = [14]
AREA_XM = [18,19,21,22]
AREA_XM_CORE = [18]
AREA_XM_FOREST = [19]
AREA_XM_DESERT = [21,22]
AREA_ALL = AREA_MD+AREA_LY+AREA_DQ+AREA_XM
def get_item_id(item_name:str, area_id:list, match_mode = 0) -> list:
    j = load_json("item.json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}\\dataset")
    ret_id = []
    for i in j:
        if int(i["areaId"]) in area_id:
            if match_mode == 0:
                if i["name"] == item_name:
                    ret_id.append(i["itemId"])
            elif match_mode == 1:
                if i["name"] in item_name:
                    ret_id.append(i["itemId"])
    ret_id = list(set(ret_id))
    return ret_id
    if len(ret_id) == 1:
        return ret_id[0]
    else:
        logger.critical("不止一个id"+item_name)
        return ret_id[0]

from source.map.extractor.convert import MapConverter

def load_items_position(marker_title:str, mode=0, area_id=None, blacklist_id=None, ret_mode = 0, check_mode = 0, match_mode = 0):
    if area_id == None:
        # area_i = load_json("auto_collector.json", "config\\settings")["collection_area"]
        area_i = GIAconfig.Collector_CollectionArea
        if area_i == 'ALL':
            area_id = AREA_ALL
        elif area_i == 'MD':
            area_id = AREA_MD
        elif area_i == 'LY':
            area_id = AREA_LY
        elif area_i == 'DQ':
            area_id = AREA_DQ
        elif area_i == 'XM':
            area_id = AREA_XM
    logger.debug(f"item_name {marker_title} area_id {area_i}")
    if match_mode == 0:
        id_index = load_json("ID_INDEX.json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}")[marker_title]
    elif match_mode == 1:
        id_index = list(range(1,14))
    ita = []
    for i in id_index:
        ita += load_json(str(i)+".json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}\\dataset")
    # print()
    
    
    common_name = []
    if mode == 0:
        item_id = get_item_id(marker_title, area_id, match_mode=match_mode)
        for i in ita:
            if len(i["itemList"])>0:
                if i["itemList"][0]["itemId"] in item_id:
                    common_name.append(i)
    if mode == 1:
        for i in ita:
            if len(i["itemList"])>0:
                if i["markerTitle"] in marker_title:
                    common_name.append(i)
    
    if blacklist_id == None:
        blacklist_id = []
    ret_dict=[]
    i=0
    for item in common_name:
        i+=1
        if item == None:
            continue

        if check_mode == 0:
            if item["id"] in blacklist_id:
                continue
        elif check_mode == 1:
            if item["id"] not in blacklist_id:
                continue
        
        if ret_mode == 0:
            ret_dict.append({
                "id":item["id"], # id&posi
                "position":list(np.array(list(map(float,item["position"].split(','))) )*1.5),
                "refreshTime":item["refreshTime"]
            })
        elif ret_mode == 1: # posi list only
                ret_dict.append(list(np.array( list(map(float,item["position"].split(','))))*1.5))
    # print()
    return ret_dict  
if __name__ == '__main__':
    from source.manager import asset
    s = load_items_position(marker_title=asset.QTSX.text, ret_mode=1, match_mode=1)
    print()
def load_feature_position(text, blacklist_id=None, ret_mode = 0, check_mode = 0):
    ita = load_json("itemall.json", "assets")
    if blacklist_id == None:
        blacklist_id = []
    ret_dict=[]
    i=0
    for feature in ita:
        i+=1
        if feature == None:
            continue
        for item in feature["features"]:
            if check_mode == 0:
                if item["id"] in blacklist_id:
                    continue
            elif check_mode == 1:
                if item["id"] not in blacklist_id:
                    continue
            if text in item["properties"]["popTitle"] :
                if ret_mode == 0:
                    ret_dict.append({
                        "id":item["id"],
                        "position":list(np.array( list(map(float,item["geometry"]["coordinates"])) )*1.5)
                    })
                elif ret_mode == 1:
                     ret_dict.append(list(np.array( list(map(float,item["geometry"]["coordinates"])) )*1.5))
    # print()
    return ret_dict  

