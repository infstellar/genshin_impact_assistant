from util import *
from collector_lib import get_item_id
# save_json(load_json(json_name="icon.json", default_path="assets\\POI_JSON_API"),json_name="icon.json", default_path="assets\\POI_JSON_API")

def reshape_json():
    for i in list(range(1,14))+["area", "icon", "id_stamp", "item", "type"]:
        save_json(load_json(json_name=str(i)+".json", default_path="assets\\POI_JSON_API\\zh_CN\\dataset"),json_name=str(i)+".json", default_path="assets\\POI_JSON_API\\zh_CN\\dataset")
        logger.info(f"{i} succ")

def create_indexes():
    s = {}
    for ii in range(1,14):
        j = load_json(json_name=str(ii)+".json", default_path="assets\\POI_JSON_API\\zh_CN\\dataset")
        for i in j:
            s.setdefault(i["markerTitle"], []).append(str(ii))
            s[i["markerTitle"]] = list(set(s[i["markerTitle"]]))
        print(s)
    save_json(s, "ID_INDEX.json", "assets\\POI_JSON_API\\zh_CN")

def create_name():
    s = []
    for ii in range(1,14):
        j = load_json(json_name=str(ii)+".json", default_path="assets\\POI_JSON_API\\zh_CN\\dataset")
        for i in j:
            s.append(i["markerTitle"])
    s=list(set(s))
    save_json(s, "ITEM_NAME.json", "assets\\POI_JSON_API\\zh_CN")

def create_refreshTime():
    s = {}
    for ii in range(1,14):
        j = load_json(json_name=str(ii)+".json", default_path="assets\\POI_JSON_API\\zh_CN\\dataset")
        for i in j:
            if int(i["refreshTime"]) not in [-1,0]:
                s[str(i["id"])]=i["refreshTime"]
        # print(s)
    save_json(s, "REFRESHTIME_INDEX.json", "assets\\POI_JSON_API\\zh_CN")

create_refreshTime()
reshape_json()
create_indexes()
create_name()
