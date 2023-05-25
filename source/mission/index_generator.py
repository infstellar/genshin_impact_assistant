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
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"missions")):
        for file in files:
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
        f.write("META = {}\n")
        f.write("if __name__ == '__main__':\n")
        f.write(f"    from source.funclib import combat_lib\n")
        f.write(f"    combat_lib.CSDL.stop_threading()\n")
        for i in mission_list:
            f.write(f"    import source.mission.missions.{i}\n")
            f.write(f"    META['{i}'] = source.mission.missions.{i}.META\n")
        for i in extra_mission_list:
            f.write(f"    import missions.{i}\n")
            f.write(f"    META['{i}'] = missions.{i}.META\n")
        path_meta = os.path.join(ROOT_PATH,'missions\\mission_meta.py')
        path_index = os.path.join(ROOT_PATH,'missions\\mission_index.py')
        f.write(f"    with open(r'{path_meta}', 'w', encoding='utf-8') as f:\n")
        f.write("        f.write(f'MISSION_META = {str(META)}')\n")
        f.write(f"    print('index end')\n")


    print(f"sys: python {path_index} start")
    os.system(f"python {path_index}")
    print(f"sys: python {path_index} end")
    
if __name__ == '__main__':
    generate_mission_index()