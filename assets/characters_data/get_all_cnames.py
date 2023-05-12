import json, os

j={}
j = json.load(open(r"assets/characters_data/characters_parameters.json", 'r', encoding='utf-8'))
print([i[0] for i in j.items()])