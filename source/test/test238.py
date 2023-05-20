from source.util import *


# save_json(load_json(json_name="icon.json", default_path="assets\\POI_JSON_API"),json_name="icon.json", default_path="assets\\POI_JSON_API")
LANG = 'en_US'
EN2ZH = load_json('en_US.json',r"assets/POI_JSON_API/LANGUAGE")

def en2zh(x):
    if LANG == 'en_US':
        if x in EN2ZH:
            return EN2ZH[x]
        else:
            return x
    else:
        return x

def replace_str(d):
    if LANG == 'en_US':
        if isinstance(d,dict):
            for k, v in d.items():
                if isinstance(v, dict):
                    replace_str(v)
                elif isinstance(v, list):
                    for i in v:
                        if isinstance(i, dict):
                            replace_str(i)
                        elif isinstance(i, str):
                            v[v.index(i)] = en2zh(v[v.index(i)])
                elif isinstance(v, str):
                    d[k] = en2zh(d[k])
        elif isinstance(d,list):
            for i in d:
                if isinstance(i, dict):
                    replace_str(i)
                elif isinstance(i, str):
                    d[d.index(i)] = en2zh(d[d.index(i)])
        return d
    else:
        return d

def reshape_json():
    for i in list(range(1,15))+["area", "icon", "id_stamp", "item", "type"]:
        s = load_json(json_name=str(i)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        s = replace_str(s)
        save_json(s,json_name=str(i)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        logger.info(f"{i} succ")

def create_indexes():
    s = {}
    for ii in range(1,15):
        j = load_json(json_name=str(ii)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        for i in j:
            s.setdefault(i["markerTitle"], []).append(str(ii))
            s[i["markerTitle"]] = list(set(s[i["markerTitle"]]))
            if en2zh(i["markerTitle"]) != i["markerTitle"]:
                s.setdefault(en2zh(i["markerTitle"]), []).append(str(ii))
            s[en2zh(i["markerTitle"])] = list(set(s[en2zh(i["markerTitle"])]))
        print(s)
    # replace_str(s)
    save_json(s, "ID_INDEX.json", f"assets\\POI_JSON_API\\{LANG}")

def create_name():
    s = []
    for ii in range(1,15):
        j = load_json(json_name=str(ii)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        for i in j:
            s.append(i["markerTitle"])
    s=list(set(s))
    replace_str(s)
    save_json(s, "ITEM_NAME.json", f"assets\\POI_JSON_API\\{LANG}")

def create_refreshTime():
    s = {}
    for ii in range(1,15):
        j = load_json(json_name=str(ii)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        for i in j:
            if int(i["refreshTime"]) not in [-1,0]:
                s[str(i["id"])]=i["refreshTime"]
        # print(s)
    save_json(s, "REFRESHTIME_INDEX.json", f"assets\\POI_JSON_API")

def get_all_position():
    rl = []
    for ii in range(1,15):
        j = load_json(json_name=str(ii)+".json", default_path=f"assets\\POI_JSON_API\\{LANG}\\dataset")
        for i in j:
            rl.append(list(map(float,i['position'].split(',') )))
    save_json(rl, "all_position.json", f"assets\\POI_JSON_API", sort_keys=False)
create_refreshTime()
# reshape_json()
create_indexes()
create_name()
get_all_position()
#test