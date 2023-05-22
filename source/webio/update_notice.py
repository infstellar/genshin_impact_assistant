from source.util import *

def upd_message():
    ret_message = ""
    version_num = int(GIAconfig.General_Version.split('.')[-1])
    if version_num!=int(GIA_VERSION.split(".")[-1]):
        ret_message+=t2t("GIA 已升级到")+f"{GIA_VERSION}. \n"
    if version_num <= 500:
        ret_message+=f"推荐删除tactic中的team.json和team_example_3.json，然后重启GIA。\n"
    if version_num < 753:
        ret_message+=f"战斗策略自动填充已经可用。\n可以删除tactic中的team.json和team_example_3.json，然后重启GIA。\n"
    if version_num < 779:
        ret_message+=f"现已支持多显示器多缩放设置。可能存在问题，欢迎反馈。\n"
    if version_num < 874:
        ret_message+=f"config设置已重置，请重新设置config。\n"\
                        "tactic, collector等设置可以继续使用。\n"\
                        "注意：队伍设置现在默认为自适应，如果需要使用你自己的设置，请将AdaptiveTeamSetup(自适应队伍设置)设置为false。"
    if version_num < 933:
        ret_message+=f"升级自定义任务的UI界面\n\
                       提升自定义任务采集成功率"
    
    x=load_json()
    x["Version"]=GIA_VERSION
    save_json(x)
    GIAconfig.update()
    return ret_message