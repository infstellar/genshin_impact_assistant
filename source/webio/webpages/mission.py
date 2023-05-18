from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
from source.mission.mission_index import MISSION_INDEX
from source.mission.mission_meta import MISSION_META

class MissionPage(AdvancePage):
    NAME_PROCESSBAR_MissionRebuild = 'PROCESSBAR_MissionRebuild'
    def __init__(self) -> None:
        super().__init__()
        self.missions = MISSION_INDEX
        self._create_default_settings()
    
    def _create_default_settings(self):
        j = load_json('mission_settings.json', f"{CONFIG_PATH}\\mission", auto_create=True)
        if j == {}: j = []
        save_json(j, 'mission_settings.json', f"{CONFIG_PATH}\\mission")
        j = load_json('mission_group.json', f"{CONFIG_PATH}\\mission", auto_create=True)
        if j == {}: j = []
        save_json(j, 'mission_group.json', f"{CONFIG_PATH}\\mission")
    
    def _render_scopes(self):
        j = load_json('mission_settings.json', f"{CONFIG_PATH}\\mission")
        for mission_name in self.missions:
            output.clear(mission_name)
            if mission_name in MISSION_META:
                if GLOBAL_LANG in MISSION_META[mission_name]['name']:
                    mission_show_name = MISSION_META[mission_name]['name'][GLOBAL_LANG]
                else:
                    mission_show_name = mission_name
            else:
                mission_show_name = mission_name
            output.put_text(mission_show_name, scope=mission_name)
            pv = 999
            ebd = False
            for iii in j:
                if iii['filename'] == mission_name:
                    if 'priority' in iii:
                        pv = iii['priority']
                    if 'enabled' in iii:
                        ebd = iii['enabled']
            if ebd:ebd=['enabled']
            pin.put_checkbox(name=f"CHECKBOX_{mission_name}",options=[{'label':t2t('Enable'),'value':'enabled'}],scope=mission_name,value=ebd)
            pin.put_input(name=f"PRIORITY_{mission_name}",label="Priority",scope=mission_name,type=input.NUMBER,value=pv)
    
    def _generate_mission_index(self):
        mission_list = []
        extra_mission_list = []
        for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"source\\mission\\missions")):
            for file in files:
                if file[file.index('.'):]==".py":
                    mission_list.append(file.replace('.py',''))
        for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"missions")):
            for file in files:
                if file[file.index('.'):]==".py":
                    extra_mission_list.append(file.replace('.py',''))
        output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0.2)
        with open(os.path.join(ROOT_PATH,"source\\mission\\mission_index.py"), "w") as f:
            f.write("\"\"\"This file is generated automatically. Do not manually modify it.\"\"\"\n")
            f.write(f"import os, sys\n")
            f.write(f"sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))\n")
            f.write(f"MISSION_INDEX = {str(mission_list)}\n")
            f.write("def get_mission_object(mission_name:str):\n")
            for i in mission_list:
                f.write(f"    if mission_name == '{i}':\n")
                f.write(f"        import source.mission.missions.{i}\n")
                f.write(f"        return source.mission.missions.{i}.{i}()\n")
            for i in extra_mission_list:
                f.write(f"    if mission_name == '{i}':\n")
                f.write(f"        import missions.{i}\n")
                f.write(f"        return missions.{i}.{i}()\n")
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0.4)
            f.write("META = {}\n")
            f.write("if __name__ == '__main__':\n")
            for i in mission_list:
                f.write(f"    import source.mission.missions.{i}\n")
                f.write(f"    META['{i}'] = source.mission.missions.{i}.META\n")
            for i in extra_mission_list:
                f.write(f"    import missions.{i}\n")
                f.write(f"    META['{i}'] = missions.{i}.META\n")
            path_meta = os.path.join(ROOT_PATH,'source\\mission\\mission_meta.py')
            path_index = os.path.join(ROOT_PATH,'source\\mission\\mission_index.py')
            f.write(f"    with open('{path_meta}', 'w', encoding='utf-8') as f:\n")
            f.write("        f.write(f'MISSION_META = {str(META)}')\n")
            f.write(f"    from source.funclib import combat_lib\n")
            f.write(f"    combat_lib.CSDL.stop_threading()\n")
            f.write(f"    print('index end')\n")
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0.6)

        output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0.65)
        print(f"sys: python {path_index}")
        os.system(f"python {path_index}")
        output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0.95)
        print(f"sys: python {path_index} end")
        output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 1)
    
    def _get_all_mission_info(self):
        mission_info = []
        for i in self.missions:
            is_enable = pin.pin[f'CHECKBOX_{i}']
            if is_enable == []:
                is_enable = False
            else:
                is_enable = True
            mission_info.append(
                {
                    'filename':i,
                    'priority':pin.pin[f'PRIORITY_{i}'],
                    'enabled':is_enable
                }
            )
            
        return mission_info
    
    def _onclick_rebuild_missions(self):
        output.put_processbar(name=self.NAME_PROCESSBAR_MissionRebuild,label=t2t('Rebuild Progress'), auto_close=False, scope='SCOPE_PROCESSBAR')
        self._generate_mission_index()
        output.popup(t2t("Rebuild success, please restart GIA program."))

    def _onclick_add_missions(self):
        pass
    
    def _onclick_save_missions(self):
        mission_info = self._get_all_mission_info()
        def sort_by_priority(x):
            return x['priority']
        mission_info = sorted(mission_info, key=sort_by_priority)
        save_json(mission_info, json_name='mission_settings.json', default_path=fr'{CONFIG_PATH}/mission')
        save_json([i['filename'] for i in mission_info if i['enabled']], json_name='mission_group.json', default_path=fr'{CONFIG_PATH}/mission')
        toast_succ()
    
    def _load(self):
        # put buttons
        output.put_row([output.put_button(label=t2t('Rebuild Mission'), onclick=self._onclick_rebuild_missions),
                        # output.put_button(label=t2t('Add Mission'), onclick=self._onclick_add_missions),
                        output.put_button(label=t2t('Save Changes'), onclick=self._onclick_save_missions)],scope=self.main_scope)
        
        output.put_scope(name='SCOPE_PROCESSBAR',scope=self.main_scope)
        
        # put missions grid
        grid_content = []
        for i in range(len(self.missions)):
            if i%3==0:
                grid_content.append([])
            grid_content[i//3].append(output.put_scope(f"{self.missions[i]}").style('border: 1px solid #ccc; border-radius: 16px'))
        output.put_grid(content=grid_content, scope=self.main_scope)
        
        self._render_scopes()
    
    def _event_thread(self):
        return super()._event_thread()
        