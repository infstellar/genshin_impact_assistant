from unit import *
import combat_loop,character




if __name__=='__main__':
    #character_json=loadjson('character.json')
    team=loadjson('team.json')
    chara_list=[]
    for team_name in team:
        team_item=team[team_name]
        chara_list.append(
            character.Character(team_item['name'],team_item["position"],team_item["priority"],team_item["Ecd_time"],team_item["Elast_time"],
                                team_item["Ecd_float_time"],team_item["tastic_group"],team_item["trigger"]
                                )
            )
    combat=combat_loop.Combat_Loop(chara_list)
    while(True):
        ret=combat.loop()
        print('/n',ret)
        if ret:
            time.sleep(2)
        else:
            time.sleep(0.5)