from source.util import *

def upd_message():
    ret_message = ""
    version_num = int(load_json()["version"].split('.')[-1])
    if version_num <= 500:
        ret_message+=f"GIA 已升级到{GIA_VERSION}。\n版本升级提示：推荐删除tactic中的team.json和team_example_3.json，然后重启GIA。"
    x=load_json()
    x["version"]=GIA_VERSION
    save_json(x)
    return ret_message