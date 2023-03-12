from source.util import *

"""
生成mission index，提供导入。
"""

mission_list = []
for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"source\\mission\\missions")):
    for file in files:
        if file[file.index('.'):]==".py":
            mission_list.append(file.replace('.py',''))

with open(os.path.join(ROOT_PATH,"source\\mission\\mission_index.py"), "w") as f:
    f.write("\"\"\"This file is generated automatically. Do not manually modify it.\"\"\"\n")
    f.write(f"MISSION_INDEX = {str(mission_list)}\n")
    f.write("def get_mission_object(mission_name:str):\n")
    for i in mission_list:
        f.write(f"    if mission_name == '{i}':\n")
        f.write(f"        import source.mission.missions.{i}\n")
        f.write(f"        return source.mission.missions.{i}.{i}()\n")