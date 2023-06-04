from source.util import *

"""
生成mission index，提供导入。
"""
def generate_mission_index():
    mission_list = []
    extra_mission_list = []
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"source\\mission\\missions")):
        for file in files:
            if file[file.index('.'):]==".py":
                mission_list.append(file.replace('.py',''))
    # Only fetch files in the root directory of the missions folder
    # Do not fetch files in subdirectories
    for file in os.listdir(os.path.join(ROOT_PATH,"missions")):
        if os.path.isfile(os.path.join(ROOT_PATH,"missions", file)):
            if file[file.index('.'):]==".py":
                if file[:file.index('.')] not in ['mission_index', 'mission_meta']:
                    extra_mission_list.append(file.replace('.py',''))

    with open(os.path.join(ROOT_PATH,"missions\\mission_index.py"), "w") as f:
        f.write("\"\"\"This file is generated automatically. Do not manually modify it.\"\"\"\n")
        f.write(f"import os, sys\n")
        f.write(f"sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n")
        f.write(f"MISSION_INDEX = {str(mission_list+extra_mission_list)}\n")
        f.write("def get_mission_object(mission_name:str):\n")
        for i in mission_list:
            f.write(f"    if mission_name == '{i}':\n")
            f.write(f"        import source.mission.missions.{i}\n")
            f.write(f"        return source.mission.missions.{i}.MissionMain()\n")
        for i in extra_mission_list:
            f.write(f"    if mission_name == '{i}':\n")
            f.write(f"        import missions.{i}\n")
            f.write(f"        return missions.{i}.MissionMain()\n")
    
if __name__ == '__main__':
    generate_mission_index()