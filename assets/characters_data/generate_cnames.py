from source.util import *

j = load_json('characters_name.json', "assets/characters_data")
cnames = []
for i in j:
    cnames.append(
        {
            "standard_name":i['en'],
            "alias":[i['zhCN'],i['ja']]
        }
    )
save_json(cnames, 'characters_name_dict.json', "assets/characters_data")