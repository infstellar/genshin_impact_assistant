from source.util import *
ZH2EN = load_json('en_US.json',r"assets/POI_JSON_API/LANGUAGE")

def zh2en(x):
    if x in ZH2EN:
        return ZH2EN[x]
    else:
        return x